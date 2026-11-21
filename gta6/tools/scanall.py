"""PC: python scanall.py <id> [<id> ...]  -> work/scan/<id>.json (candidate moments with subtitle text + loudness score).
Uses YouTube auto-subs (json3) + a low-bitrate audio track for loudness. No Whisper needed for finished VODs."""
import json, os, subprocess, sys, glob, math
D = os.path.dirname(os.path.abspath(__file__)); PY = sys.executable
W = os.path.join(D, "work", "scan"); os.makedirs(W, exist_ok=True)
CONF = os.path.join(D, "tools", "yt-dlp.conf")
HOOK = ["oh my god", "no way", "bro", "what the", "let's go", "lets go", "yo", "chat", "crazy", "insane", "realistic",
        "rockstar", "police", "cops", "wanted", "crash", "jail", "died", "dead", "kill", "run", "help", "ending", "the end",
        "credits", "beat the game", "finished", "mission", "lucia", "jason", "money", "bank", "heist", "glitch", "funny"]
def ydl(*a): return subprocess.run([PY, "-m", "yt_dlp", "--config-locations", CONF, *a], capture_output=True, text=True, encoding="utf-8")
def subs(vid):
    out = os.path.join(W, vid)
    if not glob.glob(out + "*.json3"):
        ydl("--skip-download", "--write-auto-subs", "--write-subs", "--sub-langs", "en.*,en", "--sub-format", "json3", "-o", out, "https://www.youtube.com/watch?v=" + vid)
    f = sorted(glob.glob(out + "*.json3"))
    if not f: return []
    ev = json.load(open(f[0], encoding="utf-8")).get("events", [])
    return [(e["tStartMs"] / 1000, "".join(s.get("utf8", "") for s in e.get("segs", [])).strip()) for e in ev if e.get("segs")]
def loud(vid):
    a = os.path.join(W, vid + ".m4a")
    if not os.path.exists(a):
        ydl("-f", "139/140/ba", "-N", "8", "-o", a, "https://www.youtube.com/watch?v=" + vid)
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", a, "-ac", "1", "-ar", "400", "-f", "s16le", "-"], capture_output=True)
    import numpy as np
    x = np.frombuffer(r.stdout, np.int16).astype(np.float32)
    n = len(x) // 400; x = x[:n * 400].reshape(n, 400)
    return 10 * np.log10((x * x).mean(1) + 1)
def scan(vid, top=140):
    import numpy as np
    S = subs(vid); L = loud(vid); n = len(L)
    words = np.zeros(n); hooks = np.zeros(n)
    for t, s in S:
        i = int(t)
        if i < n:
            words[i] += len(s.split()); lo = s.lower(); hooks[i] += sum(lo.count(h) for h in HOOK)
    def roll(v, w): c = np.concatenate([[0], np.cumsum(v)]); return np.array([(c[min(n, i + w)] - c[i]) / w for i in range(n)])
    l20, base = roll(L, 20), roll(L, 600)
    base = np.concatenate([base[:300] * 0 + base[0], base])[:n] if n > 300 else base
    sc = (l20 - base) + 2.0 * roll(hooks, 20) * 20 / 20 + 0.05 * roll(words, 20) * 20
    order = np.argsort(-sc); picks = []
    for i in order:
        if i < 120: continue
        if all(abs(i - p) > 90 for p in picks): picks.append(int(i))
        if len(picks) >= top: break
    res = []
    for i in sorted(picks):
        txt = " ".join("[%d] %s" % (t, s) for t, s in S if i - 25 <= t <= i + 45)
        res.append({"t": i, "score": round(float(sc[i]), 2), "text": txt[:900]})
    end = " ".join("[%d] %s" % (t, s) for t, s in S if t >= n - 900)
    json.dump({"id": vid, "dur": n, "cands": res, "last15min": end[:6000]}, open(os.path.join(W, vid + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("DONE", vid, n, len(res), flush=True)
if __name__ == "__main__":
    for v in sys.argv[1:]: scan(v)
