"""Build one episode: lint spec -> TTS -> timeline -> music/SFX mix -> Remotion props + SRT/chapters/SEO/script/grounding.
Usage: python3 build.py 2 [3 4 ...]"""
import sys, os, re, json, hashlib, math
import numpy as np, soundfile as sf
from common import *
import audio

VOICE, SPEED, SR24 = "am_michael", 1.0, 24000
GAP, SCENE_TAIL, TITLE_GAP, END_TAIL, LEAD = 0.28, 0.52, 4.4, 4.6, 0.35
CACHE = PROD + "tts_cache/"
os.makedirs(CACHE, exist_ok=True)
_K = None


def kokoro():
    global _K
    if _K is None:
        from kokoro_onnx import Kokoro
        _K = Kokoro("/home/claude/tts/kokoro-v1.0.onnx", "/home/claude/tts/voices-v1.0.bin")
    return _K


def trim(a):
    idx = np.where(np.abs(a) > 0.004)[0]
    return a if len(idx) == 0 else a[max(0, idx[0] - 600): min(len(a), idx[-1] + 1800)]


def synth(say):
    h = hashlib.sha1((VOICE + str(SPEED) + say).encode()).hexdigest()[:18]
    p = CACHE + h + ".npy"
    if os.path.exists(p):
        return np.load(p)
    a, sr = kokoro().create(say, voice=VOICE, speed=SPEED, lang="en-us")
    assert sr == SR24
    a = trim(np.asarray(a, np.float32))
    np.save(p, a)
    return a


def parse_line(s):
    cue = None
    s = s.strip()
    m = re.match(r"^@(\S+)\s+(.*)$", s, re.S)
    if m:
        cue, s = m.group(1), m.group(2)
    say = None
    if "||" in s:
        s, say = [x.strip() for x in s.split("||", 1)]
    return cue, s.strip(), say


# ---------------- lint ----------------
TYPES = ["hook", "statement", "cards", "pipeline", "timeline", "steps", "code", "terminal", "compare", "stat",
         "checklist", "callout", "graph", "chips", "bars", "table", "sequence", "recap"]


def lint(ep):
    E = []

    def chk(c, m):
        if not c:
            E.append(m)

    def L(x):
        return len(x or "")

    for k in ("n", "title", "short", "thumb", "icon", "seo", "scenes"):
        chk(k in ep, "missing field " + k)
    chk(L(ep.get("short")) <= 40, "short too long")
    sc0 = ep["scenes"]
    chk(sc0[0]["type"] == "hook", "first scene must be hook")
    chk(sc0[-1]["type"] == "recap", "last scene must be recap")
    for i, s in enumerate(sc0):
        T = s["type"]
        tg = "scene %d (%s %s)" % (i, T, s.get("label", ""))
        chk(T in TYPES, tg + ": unknown type")
        chk(L(s.get("label")) <= 30 and s.get("label"), tg + ": label missing/too long")
        lines = s.get("lines", [])
        chk(len(lines) > 0, tg + ": no lines")
        cues = [parse_line(x)[0] for x in lines]
        for x in lines:
            chk(L(parse_line(x)[1]) <= 260, tg + ": narration line too long: " + parse_line(x)[1][:40])
        if s.get("title"):
            chk(L(s["title"]) <= 48, tg + ": title %d>48" % L(s["title"]))
        if T == "hook":
            b = s.get("beats", [])
            chk(1 <= len(b) <= 6, tg + ": beats 1-6")
            for j, x in enumerate(b):
                chk(L(x["t"]) <= 42, tg + ": beat too long " + x["t"])
                chk(L(x.get("sub")) <= 80, tg + ": beat sub too long")
                if j > 0:
                    chk(str(j + 1) in cues, tg + ": missing cue @%d" % (j + 1))
        if T == "statement":
            chk(L(s.get("sub")) <= 120, tg + ": sub too long")
            for c in s.get("chips", []):
                chk(L(c if isinstance(c, str) else c["t"]) <= 26, tg + ": chip too long")
            chk(len(s.get("chips", [])) <= 6, tg + ": max 6 chips")
        if T == "cards":
            it = s.get("items", [])
            chk(2 <= len(it) <= 4, tg + ": 2-4 items")
            for x in it:
                chk(L(x["h"]) <= 26, tg + ": card h too long " + x["h"])
                chk(L(x.get("d")) <= 96, tg + ": card d too long " + x["h"])
                chk(L(x.get("tag")) <= 22, tg + ": tag too long")
        if T == "pipeline":
            nd = s.get("nodes", [])
            chk(2 <= len(nd) <= 5, tg + ": 2-5 nodes")
            for x in nd:
                chk(L(x["h"]) <= 12, tg + ": node h too long " + x["h"])
                chk(L(x.get("s")) <= 24, tg + ": node s too long")
                chk(L(x.get("d")) <= (48 if len(nd) >= 4 else 66), tg + ": node d too long " + x["h"])
        if T == "timeline":
            st = s.get("steps", [])
            chk(3 <= len(st) <= 7, tg + ": 3-7 steps")
            for x in st:
                chk(L(x["k"]) <= 20, tg + ": step k too long " + x["k"])
                chk(L(x.get("d")) <= 30, tg + ": step d too long " + x["k"])
            for x in s.get("notes", []):
                chk(L(x["t"]) <= 64, tg + ": note too long")
        if T == "steps":
            st = s.get("steps", [])
            chk(2 <= len(st) <= 6, tg + ": 2-6 steps")
            for x in st:
                chk(L(x["h"]) <= 54, tg + ": step h too long " + x["h"])
                chk(len(x.get("path", [])) <= 4, tg + ": max 4 path items")
                for pth in x.get("path", []):
                    chk(L(pth) <= 26, tg + ": path item too long " + pth)
                chk(L(x.get("d")) <= 90, tg + ": step d too long")
        if T == "code":
            cl = s.get("code", "").split("\n")
            chk(len(cl) <= (13 if s.get("title") else 16), tg + ": too many code lines %d" % len(cl))
            for x in cl:
                chk(len(x) <= 66, tg + ": code line too long: " + x[:30])
            for h in s.get("hl", []):
                chk(L(h.get("note")) <= 74, tg + ": hl note too long")
                chk(1 <= h["l"][0] <= h["l"][1] <= len(cl), tg + ": bad hl range")
        if T == "terminal":
            n = sum(1 + len(c.get("out", [])) for c in s.get("cmds", []))
            chk(n <= 13, tg + ": terminal too many lines")
            for c in s.get("cmds", []):
                for x in [c["c"]] + c.get("out", []):
                    chk(len(x) <= 84, tg + ": terminal line too long")
        if T == "compare":
            chk(2 <= len(s.get("rows", [])) <= 5, tg + ": 2-5 rows")
            for r in s.get("rows", []):
                chk(L(r["l"]) <= 46 and L(r["r"]) <= 46, tg + ": compare cell too long")
            chk(L(s["left"]["h"]) <= 20 and L(s["right"]["h"]) <= 20, tg + ": compare header too long")
        if T == "stat":
            chk(isinstance(s.get("value"), (int, float)), tg + ": value numeric")
            chk(L(s.get("caveat")) <= 64, tg + ": caveat too long")
        if T == "checklist":
            it = s.get("items", [])
            chk(3 <= len(it) <= 8, tg + ": 3-8 items")
            for x in it:
                t = x if isinstance(x, str) else x["t"]
                chk(L(t) <= (40 if len(it) > 5 else 50), tg + ": item too long " + t)
        if T == "callout":
            chk(L(s.get("body")) <= 150, tg + ": body too long")
            chk(L(s.get("code")) <= 52, tg + ": code too long")
        if T == "graph":
            nd = s.get("nodes", [])
            chk(2 <= len(nd) <= 8, tg + ": 2-8 nodes")
            ids = [x["id"] for x in nd]
            for x in nd:
                chk(L(x["h"]) <= 22, tg + ": graph node h too long")
                chk(0 <= x["x"] <= 100 and 0 <= x["y"] <= 100, tg + ": bad coords")
            for e in s.get("edges", []):
                chk(e[0] in ids and e[1] in ids, tg + ": bad edge")
                if len(e) > 2:
                    chk(L(e[2]) <= 18, tg + ": edge label too long")
        if T == "chips":
            g = s.get("groups", [])
            chk(2 <= len(g) <= 4, tg + ": 2-4 groups")
            for x in g:
                chk(L(x["h"]) <= 22, tg + ": group h too long")
                chk(len(x["items"]) <= 9, tg + ": too many chips")
                for c in x["items"]:
                    chk(L(c) <= 26, tg + ": chip too long " + c)
        if T == "bars":
            chk(2 <= len(s.get("bars", [])) <= 5, tg + ": 2-5 bars")
        if T == "table":
            chk(2 <= len(s.get("cols", [])) <= 3, tg + ": 2-3 cols")
            chk(len(s.get("rows", [])) <= 7, tg + ": max 7 rows")
            for r in s.get("rows", []):
                for j, c in enumerate(r):
                    chk(L(c) <= (24 if j == 0 else 40), tg + ": cell too long " + c)
        if T == "sequence":
            chk(2 <= len(s.get("actors", [])) <= 4, tg + ": 2-4 actors")
            chk(len(s.get("msgs", [])) <= 6, tg + ": max 6 msgs")
            for m in s.get("msgs", []):
                chk(L(m["t"]) <= 36, tg + ": msg too long " + m["t"])
        if T == "recap":
            it = s.get("items", [])
            chk(3 <= len(it) <= 6, tg + ": 3-6 items")
            for x in it:
                chk(L(x) <= 46, tg + ": recap item too long " + x)
            chk("next" in cues and "bye" in cues, tg + ": needs @next and @bye")
    return E


# ---------------- transitions ----------------
D = {"whip": 16, "push": 18, "zoom": 18, "glitch": 14, "iris": 22, "wipe": 20, "shutter": 22, "cube": 24, "flash": 16, "split": 20}
ROT = ["whip", "cube", "wipe", "zoom", "shutter", "push", "split", "whip", "iris", "cube", "wipe", "zoom", "glitch"]


def fmt_srt(t):
    ms = int(round(t * 1000))
    return "%02d:%02d:%02d,%03d" % (ms // 3600000, ms % 3600000 // 60000, ms % 60000 // 1000, ms % 1000)


def mmss(t):
    t = int(t)
    return "%02d:%02d" % (t // 60, t % 60)


def build(n, do_audio=True):
    ep = load_spec(n)
    assert ep, "no spec for %d" % n
    errs = lint(ep)
    if errs:
        print("LINT FAIL ep%02d:\n  " % n + "\n  ".join(errs))
        return False
    mod, ctitle = CURR[n]
    out = BUILD + "ep%02d/" % n
    os.makedirs(out, exist_ok=True)
    # --- narration + timing ---
    t = 0.45
    parts = []
    scenes = []
    for k, sc in enumerate(ep["scenes"]):
        timed = []
        for raw in sc["lines"]:
            cue, disp, say = parse_line(raw)
            a = synth(say if say else spoken(disp))
            d = len(a) / SR24
            timed.append(dict(t=disp, cue=cue, start=round(t, 3), end=round(t + d, 3)))
            parts.append((t, a))
            t += d + GAP
        s2 = {kk: vv for kk, vv in sc.items() if kk != "lines"}
        s2.update(lines=timed, start=timed[0]["start"], end=timed[-1]["end"])
        scenes.append(s2)
        t = timed[-1]["end"] + (TITLE_GAP if k == 0 else GAP + SCENE_TAIL)
    dur = scenes[-1]["end"] + END_TAIL
    narr = np.zeros(int(dur * SR24) + 10, np.float32)
    for st, a in parts:
        s0 = int(st * SR24)
        narr[s0:s0 + len(a)] += a[: len(narr) - s0]
    peak = np.max(np.abs(narr))
    narr = narr / peak * 0.89
    # --- segments ---
    starts = [0.0, scenes[0]["end"] + 0.25] + [s["start"] - LEAD for s in scenes[1:]]
    kinds = [("scene", 0), ("title", -1)] + [("scene", i) for i in range(1, len(scenes))]
    trs = [None, ("glitch", 1), ("iris", 1)]
    used = ["iris"]
    for i in range(3, len(starts)):
        sc = scenes[kinds[i][1]]
        ty = sc.get("tr")
        if not ty:
            if sc["type"] == "recap":
                ty = "flash"
            else:
                ty = ROT[(i + n * 3) % len(ROT)]
                if used and ty == used[-1]:
                    ty = ROT[(i + n * 3 + 1) % len(ROT)]
        used.append(ty)
        trs.append((ty, 1 if i % 2 else -1))
    nf = int(math.ceil(dur * FPS))
    segs = []
    for i, st in enumerate(starts):
        fr = int(round(st * FPS))
        to = int(round(starts[i + 1] * FPS)) if i + 1 < len(starts) else nf
        tin = dict(type=trs[i][0], d=D[trs[i][0]], dir=trs[i][1]) if trs[i] else None
        tout = dict(type=trs[i + 1][0], d=D[trs[i + 1][0]], dir=trs[i + 1][1]) if i + 1 < len(starts) else None
        segs.append(dict(kind=kinds[i][0], scene=kinds[i][1], **{"from": fr}, to=to, tin=tin, tout=tout))
    nxt = None
    if n + 1 in CURR:
        nxt = dict(n=n + 1, title=short_title(n + 1))
    props = dict(n=n, title=ep["title"], short=ep["short"], module=mod, moduleN=MODULE_N[mod], icon=ep["icon"],
                 next=nxt, durationInFrames=nf, scenes=scenes, segments=segs, style="v3", series=dict(name="ElevenLabs Masterclass", tag="ELEVENLABS"))
    json.dump(props, open(out + "props.json", "w"))
    json.dump(dict(n=n, l1=ep["thumb"][0], l2=ep["thumb"][1], icon=ep.get("thumb_icon", ep["icon"]), module=mod, series=dict(name="ElevenLabs Masterclass", tag="ELEVENLABS")), open(out + "thumb.json", "w"))
    # --- audio ---
    if do_audio:
        title_t = starts[1]
        s1 = starts[2]
        recap = scenes[-1]
        nx = next((l["start"] for l in recap["lines"] if l["cue"] == "next"), recap["end"] - 4)
        sections = [(0, title_t - 1.2, "hook"), (title_t - 1.2, s1 + 0.6, "title"), (s1 + 0.6, nx - 0.3, "content"), (nx - 0.3, dur + 1, "end")]
        bounds = [(trs[i][0], starts[i]) for i in range(1, len(starts))]
        ev = [("riser", title_t, 1.4), ("impact", title_t + 0.05, 1.0), ("shimmer", title_t + 0.35, None), ("impact", title_t + 40 / FPS, 0.6)]
        for k, sc in enumerate(scenes):
            vstart = starts[k + 1] if k > 0 else 0
            cueT = {l["cue"]: l["start"] for l in sc["lines"] if l["cue"]}
            T = sc["type"]
            if T == "hook":
                for j, b in enumerate(sc.get("beats", [])):
                    at = cueT.get(str(j + 1), sc["start"] if j == 0 else None)
                    if at is not None:
                        ev.append(("impact", at, 0.3))
                        if b.get("fx") == "glitch" or (not b.get("fx") and j % 5 == 0):
                            ev.append(("glitch", at + 0.05, None))
            elif T == "code":
                chars = len(sc.get("code", ""))
                ev.append(("type", vstart + (28 if sc.get("title") else 20) / FPS, min(1.8, chars / max(2.5, chars / 50) / FPS)))
                for c, at in cueT.items():
                    if c.isdigit():
                        ev.append(("tick", at, None))
            elif T == "terminal":
                for j, cm in enumerate(sc.get("cmds", [])):
                    at = cueT.get(str(j + 1))
                    if at is not None:
                        ev.append(("type", at, len(cm["c"]) / 1.7 / FPS))
            elif T == "stat":
                if "s" in cueT:
                    ev.append(("roll", cueT["s"], 1.4))
                if "c" in cueT:
                    ev.append(("alert", cueT["c"], None))
            elif T == "callout":
                ev.append(("alert" if sc.get("tone", "warn") == "warn" else "blip", vstart + 0.4, None))
            elif T == "recap":
                for c, at in cueT.items():
                    if c.isdigit():
                        ev.append(("tick", at, None))
                if "next" in cueT:
                    ev.append(("shimmer", cueT["next"], None))
                if "bye" in cueT:
                    ev.append(("blip", cueT["bye"], None))
            else:
                for c, at in cueT.items():
                    if c == "c" and T == "cards" and sc.get("callout", {}).get("tone", "warn") == "warn":
                        ev.append(("alert", at, None))
                    elif c == "c" or c.startswith("n"):
                        ev.append(("blip", at, None))
                    elif c == "go":
                        ev.append(("blip", at, None))
                    else:
                        ev.append(("tick", at, None))
        mix, mus, sfx = audio.master(narr, dur, MODULE_N[mod], sections, bounds, ev, seed=n)
        sf.write(out + "mix.wav", mix, audio.SR, subtype="PCM_16")
        os.makedirs(ROOT + "Voiceovers/", exist_ok=True)
        sf.write(ROOT + "Voiceovers/ep%02d-narration.wav" % n, narr, SR24, subtype="PCM_16")
    # --- SRT ---
    srt = []
    i = 0
    for sc in scenes:
        for l in sc["lines"]:
            i += 1
            txt = l["t"]
            if len(txt) > 84:
                words = txt.split()
                h = len(words) // 2
                txt = " ".join(words[:h]) + "\n" + " ".join(words[h:])
            srt.append("%d\n%s --> %s\n%s\n" % (i, fmt_srt(l["start"]), fmt_srt(l["end"] + 0.15), txt))
    open(ROOT + "Subtitles/ep%02d-en.srt" % n, "w").write("\n".join(srt))
    # --- chapters ---
    ch = [(0.0, "Intro")]
    for k in range(1, len(scenes)):
        st = starts[k + 1]
        if st - ch[-1][0] >= 10 and dur - st >= 10:
            ch.append((st, scenes[k]["label"]))
    chapters = "\n".join("%s %s" % (mmss(a), b) for a, b in ch)
    # --- docs links ---
    srcs = []
    for s in ep.get("sources", []) + [sc.get("src") for sc in ep["scenes"] if sc.get("src")]:
        if s and s not in srcs:
            srcs.append(s)
    pmap = {p["path"]: p["title"] for p in json.load(open(ROOT + "Research/packets/page-map.json"))}
    links = "\n".join("- %s: https://elevenlabs.io/docs/%s" % (pmap.get(s, s), s) for s in srcs)
    seo = ep["seo"]
    nxt_line = ("Next episode: Ep %d, %s" % (nxt["n"], nxt["title"])) if nxt else "This is the final episode of the series."
    desc = "%s\n\nThis episode is a documented walkthrough built from the official ElevenLabs documentation (links below). It does not include a live product recording.\n\nCHAPTERS\n%s\n\nOFFICIAL DOCS USED\n%s\n\n%s\nFull playlist: ElevenLabs Masterclass: How to Create AI Agents and Voices\n\nCreated by Omkar Ghate (Omilabs). Independent educational content; not affiliated with or endorsed by ElevenLabs. Narration uses a synthetic (AI) voice.\n\nMY ELEVENLABS VOICE (use it in your projects): https://elevenlabs.io/app/voice-lab/share/0ca97729faff22ee3841f4eb985cd7e58e4a7687ba6d4afde460babdf249999d/8WqHCYyrnUqoK70Px5EJ\nTry ElevenLabs (affiliate link: I may earn a commission at no extra cost to you): https://try.elevenlabs.io/c9bnghlu9434\n\nFeatures and pricing change, so check the official docs for current details." % (seo["desc"], chapters, links, nxt_line)
    md = ["# Episode %d SEO Package: %s" % (n, ep["title"]), "", "Creator: Omkar Ghate. Keywords are research hypotheses (no search-volume tool available).", "",
          "## Titles", ""] + ["%d. %s%s" % (j + 1, x, " **(recommended)**" if j == 0 else "") for j, x in enumerate(seo["titles"])] + [
          "", "## Keywords", "", "- Primary: `%s`" % seo["kw"], "- Secondary: " + ", ".join(seo["kws"]), "- Search intent: " + seo["intent"], "",
          "## Description", "", "```", desc, "```", "", "## Tags", "", ", ".join(seo["tags"]), "", "Hashtags: " + " ".join(seo.get("hashtags", ["#ElevenLabs", "#AIVoice", "#AIAgents"])), "",
          "## Pinned comment", "", "```", seo["pinned"], "```", "", "## Playlist and end screen", "", "- Playlists: ElevenLabs Masterclass (Full Course); Module %d: %s" % (MODULE_N[mod], mod),
          "- End screen: " + nxt_line, "", "## Shorts ideas", ""] + ["%d. %s" % (j + 1, x) for j, x in enumerate(seo["shorts"])] + [
          "", "## Thumbnail", "", "- Text: **%s / %s**" % tuple(ep["thumb"]), "- File: Thumbnails/ep%02d-thumbnail.png" % n, ""]
    open(ROOT + "SEO/episode-%02d-seo.md" % n, "w").write("\n".join(md))
    open(ROOT + "SEO/episode-%02d-chapters.txt" % n, "w").write(chapters + "\n")
    # --- script ---
    sm = ["# Episode %d: %s" % (n, ep["title"]), "", "Creator: Omkar Ghate. Status: documented explainer built from official docs; not tested in a live ElevenLabs account. Runtime %s." % mmss(dur), "", "Sources:", links, ""]
    for k, sc in enumerate(scenes):
        st = starts[k + 1] if k > 0 else 0
        src = (" · Source: https://elevenlabs.io/docs/" + sc["src"]) if sc.get("src") else ""
        sm += ["## [%s] %s (%s)%s" % (mmss(st), sc["label"], sc["type"], src), ""]
        sm += [" ".join(l["t"] for l in sc["lines"]), ""]
    open(ROOT + "Scripts/episode-%02d-script.md" % n, "w").write("\n".join(sm))
    # --- grounding check ---
    grounding(n, ep, scenes)
    print("built ep%02d  %s  scenes=%d  transitions=%s" % (n, mmss(dur), len(scenes), ",".join(x[0] for x in trs[1:])))
    return True


WL = set("""omkar ghate omilabs elevenlabs eleven episode masterclass recap next intro bye""".split())


def grounding(n, ep, scenes):
    pk = open(ROOT + "Research/packets/ep%02d.md" % n).read().lower()
    for extra in ("ep01", "ep02", "ep03", "ep04"):
        pk += open(ROOT + "Research/packets/%s.md" % extra).read().lower()
    for x in ep.get("extra_packets", []):
        pk += open(ROOT + "Research/packets/ep%02d.md" % x).read().lower()
    found = {}

    def scan(txt, where):
        for m in re.finditer(r"[A-Za-z0-9{}]+(?:[_\-./:][A-Za-z0-9{}]+)+", txt):
            found.setdefault(m.group(0), where)
        for m in re.finditer(r"\b\d[\d,]*(?:\.\d+)?\b", txt):
            if len(m.group(0)) >= 2:
                found.setdefault(m.group(0), where)
        for m in re.finditer(r"\b[A-Z][A-Za-z0-9]*[A-Z][A-Za-z0-9]*\b", txt):
            found.setdefault(m.group(0), where)
        for m in re.finditer(r"(?<=[a-z,;:] )[A-Z][a-z]{2,}\b", txt):
            found.setdefault(m.group(0), where)

    def walk(o, where):
        if isinstance(o, str):
            scan(o, where)
        elif isinstance(o, dict):
            for kk, v in o.items():
                if kk not in ("type", "tr", "fx", "bg", "icon", "tone", "src", "visual", "label", "cue", "start", "end", "id"):
                    walk(v, where)
        elif isinstance(o, list):
            for v in o:
                walk(v, where)

    ui = []
    for k, sc in enumerate(scenes):
        walk(sc, "scene %d %s" % (k, sc["label"]))
        for st in sc.get("steps", []) if sc["type"] == "steps" else []:
            for p in st.get("path", []):
                if p.lower() not in pk:
                    ui.append((p, sc["label"]))
    miss = [(t, w) for t, w in found.items() if t.lower().strip(".:") not in pk and t.lower() not in WL]
    rep = ["# Ep %02d grounding check" % n, "", "Tokens in narration/on-screen text not found verbatim in this episode's docs packet (review each):", ""]
    rep += ["- `%s` (%s)" % (t, w) for t, w in miss] or ["- none"]
    rep += ["", "UI labels (steps path chips) not found verbatim in docs:", ""] + (["- `%s` (%s)" % u for u in ui] or ["- none"])
    os.makedirs(ROOT + "Research/validation", exist_ok=True)
    open(ROOT + "Research/validation/ep%02d-grounding.md" % n, "w").write("\n".join(rep) + "\n")
    print("grounding ep%02d: %d unverified tokens, %d unverified UI labels" % (n, len(miss), len(ui)))
    if miss or ui:
        print("   ", ", ".join(t for t, _ in miss[:40]), "|", ", ".join(u for u, _ in ui))


if __name__ == "__main__":
    args = sys.argv[1:]
    noaudio = "--noaudio" in args
    for a in args:
        if a.isdigit():
            build(int(a), do_audio=not noaudio)
