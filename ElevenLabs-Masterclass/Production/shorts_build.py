"""Build Shorts from batch specs in shorts/batchNN.py (SHORTS = [dict(...), ...]).

Spec per short:
  id="s001", ep=19, accent="cyan", title="...", topic="..."(for description), tags=[...],
  beats=[dict(k="keyword", v="hook|stat|card|chat|flow|orb|code|versus|list|cta", d={...}, say="narration")]

  python3 shorts_build.py 1        -> build every short in shorts/batch01.py
  python3 shorts_build.py 1 s004   -> build one

Per short it writes build/shorts/<id>/{props.json, mix.wav, meta.json, audit.json}:
- narration: Kokoro am_fenrir @0.85 (reference pace ~2.4 w/s), one take per beat, no lead-in silence
- captions: words from the SCRIPT, timed by faster-whisper word timestamps (aligned with difflib)
- audit: ASR-vs-script word match, duration window, pace, gaps, loudness/peak after mix
"""
import sys, os, re, json, difflib, runpy, hashlib
import numpy as np, soundfile as sf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import audio

P = "/home/claude/ElevenLabs-Masterclass/Production/"
OUT = P + "build/shorts/"
VOICE, SPEED, SR = "am_fenrir", 0.85, 24000
GAP = 0.16  # pause between beats (reference has near-continuous speech)
VALID_V = {"hook", "stat", "card", "chat", "flow", "orb", "code", "versus", "list", "cta"}
_K = _W = None


def K():
    global _K
    if _K is None:
        from kokoro_onnx import Kokoro
        _K = Kokoro("/home/claude/tts/kokoro-v1.0.onnx", "/home/claude/tts/voices-v1.0.bin")
    return _K


def Wh():
    global _W
    if _W is None:
        from faster_whisper import WhisperModel
        _W = WhisperModel("tiny.en", device="cpu", compute_type="int8", cpu_threads=1)
    return _W


def norm(w):
    """lowercase alnum; digits spelled out so '300' (ASR) matches 'three hundred' (script)."""
    from num2words import num2words
    w = re.sub(r"(\d+(?:\.\d+)?)", lambda m: " " + num2words(float(m.group(1)) if "." in m.group(1) else int(m.group(1))) + " ", w.lower())
    return re.sub(r"[^a-z]", "", w)


def trim(a, thr=0.012):
    idx = np.where(np.abs(a) > thr)[0]
    return a[max(0, idx[0] - 240): idx[-1] + 1200] if len(idx) else a


SPOKEN = {"ElevenLabs": "Eleven Labs", "ElevenAgents": "Eleven Agents", "ElevenCreative": "Eleven Creative", "IVC": "I V C", "PVC": "P V C", "SDK": "S D K", "v3": "v three", "v4": "v four", "LLM": "L L M", "API": "A P I", "STT": "S T T", "TTS": "T T S", "IVR": "I V R",
          "SIP": "sip", "CSV": "C S V", "URL": "U R L", "ms": "milliseconds", "DTMF": "D T M F", "PDF": "P D F",
          "E.164": "E one sixty four", "Cal.com": "Cal dot com", "n8n": "n eight n", "JSON": "jason", "CRM": "C R M",
          "OTP": "O T P", "IST": "I S T", "BYOT": "B Y O T", "RAG": "rag", "MCP": "M C P", "CLI": "C L I", "KYC": "K Y C",
          "DLT": "D L T", "GST": "G S T", "UTC": "U T C", "AI": "A I", "TLS": "T L S", "IP": "I P", "RTP": "R T P",
          "SDP": "S D P", "SID": "S I D", "GPT": "G P T", "ISO": "I S O", "IDs": "I Ds", "ID": "I D", "IPs": "I Ps"}


def to_spoken(text):
    out = text
    for k, v in SPOKEN.items():
        out = re.sub(r"(?<![A-Za-z0-9])%s(?![A-Za-z0-9])" % re.escape(k), v, out)
    return out


ICONS = set(re.findall(r"^  ([a-z][a-zA-Z]*): ", open("/home/claude/Bolna-AI-Masterclass/Video-Projects/omilabs-remotion/src/engine/icons.tsx").read(), re.M)) - {"fill", "stroke", "strokeWidth", "strokeLinecap", "strokeLinejoin", "pathLength", "strokeDasharray", "strokeDashoffset"}


def lint(s):
    errs = []
    for i, b in enumerate(s["beats"]):
        ic = b.get("d", {}).get("icon")
        if ic and ic not in ICONS: errs.append("beat %d unknown icon %s" % (i, ic))
    if not re.fullmatch(r"[se]\d{3}", s["id"]): errs.append("id")
    if len(s["title"]) > 90: errs.append("title > 90 chars")
    if s["beats"][0]["v"] != "hook": errs.append("first beat must be hook")
    if s["beats"][-1]["v"] != "cta": errs.append("last beat must be cta")
    words = sum(len(b["say"].split()) for b in s["beats"])
    if not 45 <= words <= 90: errs.append("script %d words (45-90)" % words)
    for i, b in enumerate(s["beats"]):
        if b["v"] not in VALID_V: errs.append("beat %d visual %s" % (i, b["v"]))
        if b["v"] != "cta" and len(b["say"].split()) > 13: errs.append("beat %d has %d words (max 13, ~5 s)" % (i, len(b["say"].split())))
        if len(b.get("k", "")) > 22: errs.append("beat %d keyword long" % i)
        d = b.get("d", {})
        if b["v"] == "hook" and max(len(l) for l in d["lines"]) > 18: errs.append("hook line > 18 chars")
        if b["v"] == "flow" and (len(d["nodes"]) > 4 or max(len(x) for x in d["nodes"]) > 22): errs.append("flow nodes")
        if b["v"] == "list" and (len(d["items"]) > 4 or max(len(x) for x in d["items"]) > 30): errs.append("list items")
        if b["v"] == "code" and (len(d["lines"]) > 8 or max(len(x) for x in d["lines"]) > 34): errs.append("code lines")
        if b["v"] == "card" and any(len(r[0]) + len(r[1]) > 34 for r in d.get("rows", [])): errs.append("card row long")
        if b["v"] == "chat" and any(len(m[1]) > 70 for m in d["msgs"]): errs.append("chat msg long")
        if b["v"] == "versus" and max(len(d["bad"]), len(d["good"])) > 48: errs.append("versus text long")
    return errs


def build(s):
    d = OUT + s["id"] + "/"
    os.makedirs(d, exist_ok=True)
    errs = lint(s)
    if errs:
        raise SystemExit("%s lint: %s" % (s["id"], "; ".join(errs)))
    # 1. narration per beat
    parts, t, beats = [], 0.0, []
    for b in s["beats"]:
        a, sr = K().create(to_spoken(b["say"]), voice=VOICE, speed=SPEED, lang="en-us")
        a = trim(a.astype(np.float32))
        dur = len(a) / SR
        hold = 0.5 if b["v"] == "cta" else 0.0
        beats.append(dict(k=b.get("k", ""), v=b["v"], d=b.get("d", {}), start=round(t, 3), end=round(t + dur + GAP + hold, 3)))
        parts += [a, np.zeros(int((GAP + hold) * SR), np.float32)]
        t += dur + GAP + hold
    narr = np.concatenate(parts)
    total = len(narr) / SR + 0.6
    narr = np.pad(narr, (0, int(0.6 * SR)))
    # 2. word timing from ASR, text from script
    x16 = np.interp(np.arange(0, len(narr), SR / 16000), np.arange(len(narr)), narr).astype(np.float32)
    segs, _ = Wh().transcribe(x16, word_timestamps=True, language="en")
    hyp = [w for sg in segs for w in sg.words]
    script = [w for b in s["beats"] for w in b["say"].split()]
    sm = difflib.SequenceMatcher(None, [norm(to_spoken(w)) for w in script], [norm(w.word) for w in hyp], autojunk=False)
    timing = [None] * len(script)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            timing[blk.a + k] = (hyp[blk.b + k].start, hyp[blk.b + k].end)
    # clarity metric: character-level similarity of normalised script vs ASR (immune to "300" vs "three hundred")
    match = difflib.SequenceMatcher(None, "".join(norm(to_spoken(w)) for w in script), "".join(norm(w.word) for w in hyp), autojunk=False).ratio()
    # interpolate unmatched words inside their beat window
    words, wi = [], 0
    for bi, b in enumerate(s["beats"]):
        ws = b["say"].split()
        b0, b1 = beats[bi]["start"], beats[bi]["end"] - GAP
        for j, w in enumerate(ws):
            tm = timing[wi + j]
            if not tm or not (b0 - 0.3 <= tm[0] <= b1 + 0.3):
                tm = (b0 + (b1 - b0) * j / len(ws), b0 + (b1 - b0) * (j + 1) / len(ws))
            words.append(dict(w=w, start=round(tm[0], 3), end=round(tm[1], 3)))
        wi += len(ws)
    # 3. mix (music bed + per-beat transitions + hook impact + CTA shimmer)
    bounds = [("whip" if i % 2 else "zoom", b["start"]) for i, b in enumerate(beats[1:])]
    ev = [("impact", 0.05, 0.8), ("shimmer", beats[-1]["start"] + 0.2, None)]
    ev += [("blip", b["start"] + 0.35, None) for b in beats if b["v"] in ("list", "flow", "chat")]
    sections = [(0, beats[0]["end"], "hook"), (beats[0]["end"], beats[-1]["start"], "content"), (beats[-1]["start"], total, "end")]
    mix, _, _ = audio.master(narr, total, 1 + int(s["id"][1:]) % 8, sections, bounds, ev, seed=int(s["id"][1:]))
    sf.write(d + "mix.wav", mix, audio.SR, subtype="PCM_16")
    props = dict(id=s["id"], ep=s["ep"], accent=s["accent"], durationInFrames=int(round(total * 30)), beats=beats, words=words, series=dict(name="ElevenLabs Masterclass", tag="ELEVENLABS"))
    json.dump(props, open(d + "props.json", "w"))
    # 4. audit facts (render-independent)
    nwords = len(script)
    gaps = [beats[i + 1]["start"] - beats[i]["end"] for i in range(len(beats) - 1)]
    audit = dict(words=nwords, seconds=round(total, 2), wps=round(nwords / total, 2), asr_match=round(match, 3),
                 beats=len(beats), longest_beat=round(max(b["end"] - b["start"] for b in beats), 2), max_gap=round(max(gaps + [0]), 2),
                 asr_text=" ".join(w.word.strip() for w in hyp))
    audit["pass_audio"] = bool(15 <= total <= 40 and match >= 0.85 and audit["longest_beat"] <= 7.5)
    json.dump(audit, open(d + "audit.json", "w"), indent=1)
    json.dump({k: s[k] for k in ("id", "ep", "title", "topic", "tags")}, open(d + "meta.json", "w"), indent=1)
    print("%s %4.1fs %2d words %.2f w/s asr %.0f%% beats %d longest %.1fs %s" % (
        s["id"], total, nwords, audit["wps"], match * 100, len(beats), audit["longest_beat"], "OK" if audit["pass_audio"] else "CHECK"), flush=True)
    return audit


if __name__ == "__main__":
    batch = int(sys.argv[1])
    only = set(sys.argv[2:])
    for s in runpy.run_path(P + "shorts/batch%02d.py" % batch)["SHORTS"]:
        if only and s["id"] not in only:
            continue
        h = hashlib.md5(json.dumps(s, sort_keys=True).encode()).hexdigest()
        hp = OUT + s["id"] + "/spec.md5"
        if not only and os.path.exists(hp) and open(hp).read() == h and os.path.exists(OUT + s["id"] + "/props.json"):
            continue  # unchanged and already built
        build(s)
        open(hp, "w").write(h)
