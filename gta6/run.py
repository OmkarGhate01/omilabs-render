"""GTA 6 Moments - cloud clip engine (runs on GitHub Actions, no PC needed).

python gta6/run.py <job_id>          job comes from gta6/queue.json
Output: out/<job>-cNN.mp4 + out/pkg/Published-Assets/gta6/pkg/<job>.json

A job:
  {"id": "speed-zelda", "url": "...", "streamer": "IShowSpeed", "channel": "https://youtube.com/@IShowSpeed",
   "lang": "en" | "hi",                  # en -> word captions, hi -> no captions
   "cam": "0,330,450,272" | null,         # facecam box in 1920x1080 source; null -> blurred full-frame layout
   "game": "450,0,1215,1080" | null,      # gameplay crop for split layout
   "max": 10,                             # clips to cut (auto mode)
   "clips": [{"start": 7132, "len": 58, "title": "...", "score": 9}]   # optional: hand-picked moments
  }
"""
import json, os, re, subprocess, sys
import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.getcwd(), "out")
FONTS = os.path.join(ROOT, "fonts")
YTDLP = [sys.executable, "-m", "yt_dlp", "--js-runtimes", "node", "--remote-components", "ejs:github", "--no-warnings"]
if os.environ.get("GTA_COOKIES") and os.path.exists(os.environ["GTA_COOKIES"]):
    YTDLP += ["--cookies", os.environ["GTA_COOKIES"]]
HYPE = set("""wtf what no way oh god omg bro dude insane crazy lol lmao yo wait police cops wanted chase crash
explode boom run help dead died die kill holy damn bruh cheat glitch secret yes let's go chat stop why how""".split())
HYPE_HI = ["अरे", "भाई", "क्या", "नहीं", "मर", "भाग", "बचा", "हंसी", "हँसी", "गया", "पागल", "बाप"]


def sh(cmd, **kw):
    print(">", " ".join(map(str, cmd))[:200], flush=True)
    r = subprocess.run(cmd, **kw)
    if r.returncode:
        print("STDERR:", (r.stderr or "")[-1500:] if isinstance(r.stderr, str) else "", flush=True)
        raise subprocess.CalledProcessError(r.returncode, cmd)
    return r


def info(url):
    r = sh(YTDLP + ["-J", "--skip-download", url], capture_output=True, text=True)
    return json.loads(r.stdout)


def caption_words(url, lang, work):
    """Auto-captions with word timestamps (json3). Returns [(t, word)]."""
    langs = "en,en-orig" if lang == "en" else "hi,hi-orig,en"
    try:
        sh(YTDLP + ["--skip-download", "--write-auto-subs", "--sub-langs", langs, "--sub-format", "json3",
                    "-o", os.path.join(work, "subs"), url])
    except subprocess.CalledProcessError:
        return []
    for f in sorted(os.listdir(work)):
        if f.startswith("subs") and f.endswith(".json3"):
            d = json.load(open(os.path.join(work, f), encoding="utf-8"))
            W = []
            for e in d.get("events", []):
                t0 = e.get("tStartMs", 0)
                for s in e.get("segs") or []:
                    w = s.get("utf8", "").strip()
                    if w:
                        W.append(((t0 + s.get("tOffsetMs", 0)) / 1000.0, w))
            return W
    return []


def audio_loudness(url, work):
    """Fallback signal: low-bitrate audio of the whole stream -> per-second loudness z-score."""
    a = os.path.join(work, "audio.m4a")
    sh(YTDLP + ["-f", "ba[abr<=64]/worstaudio/ba", "-o", a, url])
    raw = subprocess.run(["ffmpeg", "-v", "quiet", "-i", a, "-ac", "1", "-ar", "4000", "-f", "s16le", "-"],
                         capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32)
    n = len(x) // 4000
    db = 20 * np.log10(np.sqrt((x[: n * 4000].reshape(n, 4000) ** 2).mean(1) + 1e-6))
    return (db - db.mean()) / (db.std() + 1e-6)


def pick(words, dur, n, L, loud=None):
    """Score every second, slide an L-second window, take the n best non-overlapping windows."""
    T = int(dur) + 1
    sc = np.zeros(T)
    for t, w in words:
        i = int(t)
        if i >= T:
            continue
        lw = re.sub(r"\W", "", w.lower())
        sc[i] += 0.15
        if lw in HYPE or any(h in w for h in HYPE_HI):
            sc[i] += 1.0
        if "scream" in w.lower() or "laugh" in w.lower() or "हंसी" in w:
            sc[i] += 4.0
        if w.isupper() and len(w) > 2:
            sc[i] += 0.5
    if loud is not None:
        m = min(T, len(loud))
        sc[:m] += np.clip(loud[:m], 0, None) * 0.8
    sc[:120] = 0  # skip stream intro / starting-soon screen
    win = np.convolve(sc, np.ones(L), "valid")
    out = []
    for i in np.argsort(-win):
        if win[i] <= 0:
            break
        if all(abs(i - p) >= L + 30 for p, _ in out):
            out.append((int(i), float(win[i])))
        if len(out) == n:
            break
    top = max([s for _, s in out] or [1])
    return [{"start": max(0, p - 2), "len": L, "score": round(10 * s / top, 1)} for p, s in sorted(out)]


def fetch_section(url, start, L, dst):
    """Direct stream URLs + ffmpeg seek (works on long VODs where --download-sections hangs)."""
    u = sh(YTDLP + ["-f", "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/bv*[height<=1080]+ba", "-g", url],
           capture_output=True, text=True).stdout.split()
    s0 = max(0, start - 5)
    if len(u) >= 2:
        sh(["ffmpeg", "-y", "-v", "error", "-ss", str(s0), "-t", str(L + 10), "-i", u[0], "-ss", str(s0),
            "-t", str(L + 10), "-i", u[1], "-map", "0:v", "-map", "1:a", "-c", "copy", dst])
    else:
        sh(["ffmpeg", "-y", "-v", "error", "-ss", str(s0), "-t", str(L + 10), "-i", u[0], "-c", "copy", dst])
    return start - s0


def T(t):
    return "%d:%02d:%05.2f" % (t // 3600, t % 3600 // 60, t % 60)


_model = None


def whisper_words(src, off, L):
    global _model
    raw = subprocess.run(["ffmpeg", "-v", "quiet", "-ss", str(off), "-t", str(L), "-i", src, "-ac", "1", "-ar", "16000",
                          "-f", "s16le", "-"], capture_output=True).stdout
    audio = np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0
    from faster_whisper import WhisperModel
    _model = _model or WhisperModel("small", device="cpu", compute_type="int8")
    segs, _ = _model.transcribe(audio, word_timestamps=True, language="en", vad_filter=True)
    return [(w.start, w.end, w.word.strip()) for s in segs for w in (s.words or [])]


def make_ass(words, L, path, wm="GTA 6 MOMENTS"):
    ass = ["[Script Info]", "PlayResX: 1080", "PlayResY: 1920", "", "[V4+ Styles]",
           "Format: Name,Fontname,Fontsize,PrimaryColour,OutlineColour,BackColour,Bold,BorderStyle,Outline,Shadow,Alignment,MarginV",
           "Style: W,Anton,118,&H0000F0FF,&H00000000,&H00000000,0,1,9,0,5,0",
           "Style: M,Anton,56,&HA0FFFFFF,&HC0000000,&H00000000,0,1,2,0,5,0", "", "[Events]",
           "Format: Layer,Start,End,Style,Text"]
    for i, (s, e, w) in enumerate(words):
        w = re.sub(r"[{}\\]", "", w).upper().strip(",.")
        if not w:
            continue
        nxt = words[i + 1][0] if i + 1 < len(words) else e + 0.4
        ass.append("Dialogue: 0,%s,%s,W,{\\pos(540,960)\\fscx80\\fscy80\\t(0,80,\\fscx100\\fscy100)}%s"
                   % (T(s), T(min(max(e, s + 0.25), nxt)), w))
    pts = [(300, 1180), (780, 1300), (620, 1760), (260, 1600), (800, 1150), (540, 1700)]
    t, k = 0.0, 0
    while t < L:
        p, q = pts[k % 6], pts[(k + 1) % 6]
        ass.append("Dialogue: 1,%s,%s,M,{\\move(%d,%d,%d,%d)}%s" % (T(t), T(min(t + 6, L)), p[0], p[1], q[0], q[1], wm))
        t += 6; k += 1
    open(path, "w", encoding="utf-8").write("\n".join(ass))


def render(src, off, L, job, ass, dst):
    if job.get("cam"):
        cx, cy, cw, ch = map(int, job["cam"].split(","))
        gx, gy, gw, gh = map(int, (job.get("game") or "352,0,1215,1080").split(","))
        fc = ("[0:v]scale=1920:1080,split[s1][s2];"
              "[s1]crop=%d:%d:%d:%d,scale=1080:960:force_original_aspect_ratio=increase,crop=1080:960,setsar=1[cam];"
              "[s2]crop=%d:%d:%d:%d,scale=1080:960:force_original_aspect_ratio=increase,crop=1080:960,setsar=1[game];"
              "[cam][game]vstack[v0];" % (cw, ch, cx, cy, gw, gh, gx, gy))
    else:  # no facecam known: full frame centred over a blurred fill
        fc = ("[0:v]scale=1920:1080,split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,"
              "crop=1080:1920,boxblur=25:2[bg];[b]scale=1080:-2,setsar=1[fg];[bg][fg]overlay=0:(H-h)/2[v0];")
    fc += "[v0]subtitles=%s:fontsdir=%s[v]" % (os.path.basename(ass), FONTS)
    sh(["ffmpeg", "-y", "-v", "error", "-ss", str(off), "-t", str(L), "-i", src, "-filter_complex", fc,
        "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-r", "30",
        "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-movflags", "+faststart", dst],
       cwd=os.path.dirname(ass))


def main():
    jid = sys.argv[1]
    job = next(j for j in json.load(open(os.path.join(ROOT, "queue.json"), encoding="utf-8")) if j["id"] == jid)
    work = os.path.join(OUT, "work-" + jid); os.makedirs(work, exist_ok=True)
    meta = info(job["url"])
    dur = meta.get("duration") or 0
    lang = job.get("lang", "en")
    L = int(job.get("len", 45))
    clips = job.get("clips")
    if not clips:
        words = caption_words(job["url"], lang, work)
        loud = None
        if len(words) < 200:
            try:
                loud = audio_loudness(job["url"], work)
            except Exception as e:  # noqa
                print("loudness fallback failed:", e)
        clips = pick(words, dur, int(job.get("max", 10)), L, loud)
    pkg = {"id": jid, "url": job["url"], "streamer": job.get("streamer") or meta.get("channel"),
           "channel": job.get("channel") or meta.get("channel_url"), "source_title": meta.get("title"), "clips": []}
    for n, c in enumerate(clips, 1):
        name = "gta-%s-c%02d.mp4" % (jid, n)
        try:
            src = os.path.join(work, "src%02d.mp4" % n)
            off = fetch_section(job["url"], c["start"], c["len"], src)
            words = whisper_words(src, off, c["len"]) if lang == "en" else []
            ass = os.path.join(work, "c%02d.ass" % n)
            make_ass(words, c["len"], ass)
            render(src, off, c["len"], job, ass, os.path.join(OUT, name))
            pkg["clips"].append({"file": name, "start": c["start"], "len": c["len"], "score": c.get("score", 5),
                                 "title": c.get("title"), "transcript": " ".join(w for _, _, w in words)[:400]})
            os.remove(src)
        except Exception as e:  # one bad clip must not kill the job
            print("CLIP %d FAILED: %s" % (n, e), flush=True)
    d = os.path.join(OUT, "pkg", "Published-Assets", "gta6", "pkg"); os.makedirs(d, exist_ok=True)
    json.dump(pkg, open(os.path.join(d, jid + ".json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("DONE %d clips" % len(pkg["clips"]))
    if not pkg["clips"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
