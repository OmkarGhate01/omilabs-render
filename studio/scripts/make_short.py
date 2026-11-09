# Omilabs motion Short: spec.json -> Edge TTS (word timings) -> props -> Remotion render -> master.
# usage: py -3.12 scripts/make_short.py mu001 [--no-render]
import asyncio, json, os, re, subprocess, sys, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REELS = os.path.join(ROOT, "reels")
FPS = 30
GAP = 0.28      # silence between beats (s)
TAIL = 1.4      # hold after the last beat (s)


def run(cmd, **kw):
    print(">", " ".join(cmd)); subprocess.run(cmd, check=True, **kw)


def dur(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True, check=True).stdout
    return float(out.strip())


async def tts(text, voice, rate, mp3):
    import edge_tts
    try:
        com = edge_tts.Communicate(text, voice, rate=rate, boundary="WordBoundary")
    except TypeError:
        com = edge_tts.Communicate(text, voice, rate=rate)
    words = []
    with open(mp3, "wb") as f:
        async for ch in com.stream():
            if ch["type"] == "audio":
                f.write(ch["data"])
            elif ch["type"] == "WordBoundary":
                words.append({"t": ch["text"], "s": ch["offset"] / 1e7, "e": (ch["offset"] + ch["duration"]) / 1e7})
    return words


def norm(w):
    return re.sub(r"[^\wऀ-ॿ]", "", w).lower()


def even_words(text, total):
    toks = [t for t in re.split(r"\s+", re.sub(r"[—–]", " ", text)) if norm(t)]
    weight = [max(2, len(t)) for t in toks]; s = sum(weight); t0 = 0.05; out = []
    for tok, w in zip(toks, weight):
        d = (total - 0.1) * w / s; out.append({"t": tok, "s": t0, "e": t0 + d}); t0 += d
    return out


def main():
    vid = sys.argv[1]; render = "--no-render" not in sys.argv
    if vid == "all":
        ids = sorted(d for d in os.listdir(os.path.join(ROOT, "edit")) if os.path.exists(os.path.join(ROOT, "edit", d, "spec.json")) and d[:2] in ("mu", "kl", "cm", "ev"))
        for v in ids:
            if os.path.exists(os.path.join(ROOT, "..", "export", f"{v}.mp4")) and "--force" not in sys.argv:
                print("skip", v); continue
            subprocess.run([sys.executable, os.path.abspath(__file__), v] + [x for x in sys.argv[2:] if x != "--force"])
        return
    ed = os.path.join(ROOT, "edit", vid); spec = json.load(open(os.path.join(ed, "spec.json"), encoding="utf-8"))
    tmp = os.path.join(ed, "tts"); os.makedirs(tmp, exist_ok=True)
    pub = os.path.join(REELS, "public", vid); os.makedirs(pub, exist_ok=True)

    beats, parts, t = [], [], 0.0
    for i, b in enumerate(spec["beats"]):
        mp3 = os.path.join(tmp, f"b{i}.mp3")
        words = asyncio.run(tts(b["say"], spec["voice"], spec.get("rate", "+0%"), mp3))
        d = dur(mp3)
        if not words:
            words = even_words(b["say"], d)
        hl = {norm(x) for x in b.get("hl", [])}; chip = norm(b.get("chip", ""))
        for w in words:
            k = norm(w["t"]); w["hl"] = k in hl; w["chip"] = bool(chip) and k == chip
            w["s"] = round(w["s"] + t, 3); w["e"] = round(w["e"] + t, 3)
        end = t + d + (TAIL if i == len(spec["beats"]) - 1 else GAP)
        beats.append({"tag": b["tag"], "v": b["v"], "d": b["d"], "start": round(t, 3), "end": round(end, 3), "words": words})
        parts.append((mp3, d)); t = end

    # voice track: each beat + silence gap, 48 kHz mono
    wav = os.path.join(pub, "voice.wav")
    inputs, filt = [], []
    for i, (mp3, d) in enumerate(parts):
        inputs += ["-i", mp3]
        pad = (beats[i]["end"] - beats[i]["start"]) - d
        filt.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=mono,apad=pad_dur={pad:.3f}[a{i}]")
    filt.append("".join(f"[a{i}]" for i in range(len(parts))) + f"concat=n={len(parts)}:v=0:a=1[out]")
    run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filt), "-map", "[out]", wav])

    LONG = spec.get("format") == "long"
    COMP = "OmiLong" if LONG else "OmiShort"
    props = {"id": vid, "series": spec["series"], "title": spec.get("title", ""), "accent": spec["accent"], "watermark": spec["watermark"],
             "audio": f"{vid}/voice.wav", "duration": round(t, 3), "beats": beats}
    pp = os.path.join(ed, "props.json")
    json.dump(props, open(pp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"props: {pp}  ({t:.1f}s, {len(beats)} beats, {sum(len(b['words']) for b in beats)} words)")
    if not render:
        return
    # sound design: whoosh on every beat change, pop on the accent chip, click on browser beats, ding on the CTA
    sys.path.insert(0, os.path.join(ROOT, "scripts")); import sound_kit
    sd = sound_kit.ensure(ROOT); snd = []
    for i, b in enumerate(beats):
        if i > 0:
            snd.append(dict(file=os.path.join(sd, "whoosh.wav"), at=max(0.0, b["start"] - 0.12), gain_db=-24, what="beat change"))
        for w in b["words"]:
            if w.get("chip"):
                snd.append(dict(file=os.path.join(sd, "pop.wav"), at=w["s"], gain_db=-20, what="chip " + w["t"])); break
        if b["v"] == "browser":
            snd.append(dict(file=os.path.join(sd, "click.wav"), at=b["start"] + 46 / FPS, gain_db=-18, what="click"))
        if b["v"] == "cta":
            snd.append(dict(file=os.path.join(sd, "ding.wav"), at=b["start"] + 0.6, gain_db=-26, what="cta"))
    snd = [x for x in snd if x["at"] < t - 0.2]
    sfx = os.path.join(ed, "sfx.json")
    json.dump({"sounds": snd}, open(sfx, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    out = os.path.join(ed, "render.mp4"); master = os.path.join(ROOT, "..", "export", f"{vid}.mp4")
    os.makedirs(os.path.dirname(master), exist_ok=True)
    npx = shutil.which("npx") or "npx"
    if "--reuse-render" not in sys.argv or not os.path.exists(out):
        run([npx, "remotion", "render", "src/index.ts", COMP, out, f"--props={pp}", "--concurrency=" + os.environ.get("RENDER_CONC", "50%")], cwd=REELS)
    # make the render's audio exactly as long as its video (Remotion can leave ~0.1 s extra audio)
    nf = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets", "-show_entries", "stream=nb_read_packets",
                         "-of", "csv=p=0", out], capture_output=True, text=True, check=True).stdout.strip().split(",")[0]
    sd = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=duration",
                         "-of", "csv=p=0", out], capture_output=True, text=True, check=True).stdout.strip().split(",")[0]
    vdur = min(int(nf) / FPS, float(sd or 1e9))
    fixed = os.path.join(ed, "render_fixed.mp4")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", out, "-map", "0:v:0", "-map", "0:a:0", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-bf", "0", "-pix_fmt", "yuv420p", "-r", "30",
         "-af", f"apad,atrim=0:{vdur:.3f}", "-c:a", "aac", "-b:a", "256k", "-t", f"{vdur:.3f}", fixed])
    music = sound_kit.music_path(ROOT, spec.get("music", spec["series"]))
    if LONG or t > 44:   # long videos need a bed as long as the video
        music = sound_kit.music_long(ROOT, spec.get("music", spec["series"]), t + 6)
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "master_audio.py"), fixed, "-o", master,
                        "--sfx", sfx, "--music", music, "--gap", "16", "--no-denoise"])
    if r.returncode != 0:
        if os.path.exists(master):
            os.replace(master, master.replace(".mp4", ".FAILED.mp4"))
        sys.exit(f"master failed for {vid}")
    if spec.get("thumb"):
        tp = os.path.join(ed, "thumb-props.json"); json.dump(spec["thumb"], open(tp, "w", encoding="utf-8"), ensure_ascii=False)
        thumb = master.replace(".mp4", ".jpg")
        run([npx, "remotion", "still", "src/index.ts", "OmiThumb", thumb, f"--props={tp}", "--image-format=jpeg", "--jpeg-quality=92"], cwd=REELS)
    print("DONE:", os.path.abspath(master))


if __name__ == "__main__":
    main()
