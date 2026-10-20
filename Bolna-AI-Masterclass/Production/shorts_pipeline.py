"""Render + audit Shorts.
  python3 shorts_pipeline.py bundle            -> bundle engine for shorts (build/shorts/bundle.txt)
  python3 shorts_pipeline.py render s001 ...   -> render, mux, audit each
  python3 shorts_pipeline.py queue             -> render every built short without a passing master, after long-form is done
  python3 shorts_pipeline.py sheet 1           -> contact sheet of batch NN for visual review (qa/shorts-bNN.jpg)

A short is PUBLISHABLE only if audit.json has pass_audio, pass_render and pass_visual all true.
"""
import sys, os, json, glob, subprocess, time, re, runpy
import numpy as np
P = "/home/claude/Bolna-AI-Masterclass/Production/"
PROJ = "/home/claude/Bolna-AI-Masterclass/Video-Projects/omilabs-remotion"
B = P + "build/shorts/"
OUT = "/home/claude/Bolna-AI-Masterclass/Published-Assets/shorts/"
LOG = P + "shorts_queue.log"


def sh(c, cwd=PROJ):
    r = subprocess.run(c, shell=True, cwd=cwd, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError("FAILED %s\n%s" % (c[:200], r.stderr[-1500:]))
    return r.stdout + r.stderr


def log(m):
    open(LOG, "a").write(time.strftime("%H:%M:%S ") + m + "\n")


def bundle():
    out = P + "build/shorts-bundle-" + time.strftime("%m%d%H%M%S")
    sh("npx remotion bundle src/index.ts --out-dir %s --log=error" % out)
    open(B + "bundle.txt", "w").write(out)
    print(out)


def frames_gray(mp4, times):
    """Return list of (H,W) float luminance arrays at given seconds (full 1080x1920)."""
    res = []
    for t in times:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", "%.2f" % t, "-i", mp4, "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "gray", "-"],
                             capture_output=True).stdout
        res.append(np.frombuffer(raw, np.uint8).reshape(1920, 1080).astype(np.float32) if len(raw) == 1920 * 1080 else None)
    return res


def audit_render(sid):
    d = B + sid + "/"
    a = json.load(open(d + "audit.json"))
    props = json.load(open(d + "props.json"))
    mp4 = OUT + sid + ".mp4"
    issues = []
    dur = float(sh("ffprobe -v error -show_entries format=duration -of csv=p=0 %s" % mp4).strip())
    plan = props["durationInFrames"] / 30
    if abs(dur - plan) > 0.25:
        issues.append("duration %.2f vs %.2f" % (dur, plan))
    # loudness / true peak
    o = sh("ffmpeg -hide_banner -nostats -i %s -af ebur128=peak=true -f null -" % mp4)
    I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", o)[-1]); TP = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", o)[-1])
    if not -15.5 <= I <= -12.5: issues.append("loudness %.1f LUFS" % I)
    if TP > -0.5: issues.append("true peak %.1f dBTP" % TP)
    # silence gaps in narration region
    sil = re.findall(r"silence_duration: ([\d.]+)", sh("ffmpeg -hide_banner -i %s -af silencedetect=n=-45dB:d=0.9 -f null -" % mp4))
    if sil: issues.append("silence gaps %s" % sil)
    a["pass_render"] = not issues
    # visual safe zones: sample each beat (entry+0.6s and mid) and the last frame
    times = []
    for b in props["beats"]:
        times += [b["start"] + 0.6, (b["start"] + b["end"]) / 2]
    vis = []
    for t, g in zip(times, frames_gray(mp4, times)):
        if g is None:
            vis.append("no frame at %.1fs" % t); continue
        rail = g[300:1500, 960:1080]          # right action rail
        foot = g[1560:1900, 0:1080]           # title/description overlay
        if np.percentile(rail, 99.7) > 150: vis.append("content in right rail @%.1fs" % t)
        if np.percentile(foot, 99.7) > 150: vis.append("content under overlay @%.1fs" % t)
        if g[400:1300, 100:900].std() < 6: vis.append("near-empty frame @%.1fs" % t)
    a["pass_visual_auto"] = not vis
    a["render_issues"], a["visual_issues"] = issues, vis
    a["loudness"], a["true_peak"] = I, TP
    json.dump(a, open(d + "audit.json", "w"), indent=1)
    return a


def render(sid):
    d = B + sid + "/"
    os.makedirs(OUT, exist_ok=True)
    bun = open(B + "bundle.txt").read().strip()
    t0 = time.time()
    sh("npx remotion render %s Short %ssilent.mp4 --props=%sprops.json --muted --concurrency=2 --crf=18 --x264-preset=veryfast --log=error" % (bun, d, d))
    sh("ffmpeg -y -hide_banner -loglevel error -i %ssilent.mp4 -i %smix.wav -map 0:v -map 1:a -c:v copy -af loudnorm=I=-14:TP=-2:LRA=7,alimiter=limit=0.7:attack=1:level=false -ar 48000 -c:a aac -b:a 192k -shortest -movflags +faststart %s%s.tmp.mp4" % (d, d, OUT, sid), cwd=d)
    os.replace(OUT + sid + ".tmp.mp4", OUT + sid + ".mp4")  # atomic: a killed render never leaves a half file
    os.remove(d + "silent.mp4")
    a = audit_render(sid)
    log("%s rendered %.1f min | audio %s render %s visual-auto %s %s" % (sid, (time.time() - t0) / 60, a["pass_audio"], a["pass_render"], a["pass_visual_auto"],
                                                                     "; ".join(a["render_issues"] + a["visual_issues"])))


def sheet(batch):
    ids = [s["id"] for s in runpy.run_path(P + "shorts/batch%02d.py" % batch)["SHORTS"]]
    rows = []
    for sid in ids:
        mp4 = OUT + sid + ".mp4"
        if not os.path.exists(mp4): continue
        props = json.load(open(B + sid + "/props.json"))
        ts = [0.05] + [(b["start"] + b["end"]) / 2 for b in props["beats"]]
        ts = ts[:8]
        row = "/tmp/claude-0/sh_%s.jpg" % sid
        ins = " ".join("-ss %.2f -i %s" % (t, mp4) for t in ts)
        fc = "".join("[%d:v]scale=180:320,trim=end_frame=1[v%d];" % (i, i) for i in range(len(ts))) + "".join("[v%d]" % i for i in range(len(ts))) + "hstack=%d" % len(ts)
        sh("ffmpeg -y -hide_banner -loglevel error %s -frames:v 1 -filter_complex '%s' %s" % (ins, fc, row))
        rows.append(row)
    os.makedirs(P + "qa", exist_ok=True)
    out = P + "qa/shorts-b%02d.jpg" % batch
    if len(rows) == 1:
        import shutil; shutil.copy(rows[0], out); print(out); return
    sh("ffmpeg -y -hide_banner -loglevel error %s -filter_complex '%s' %s" % (" ".join("-i " + r for r in rows),
       "".join("[%d:v]pad=1440:320:0:0:black[p%d];" % (i, i) for i in range(len(rows))) + "".join("[p%d]" % i for i in range(len(rows))) + "vstack=%d" % len(rows), out))
    print(out)


def queue():
    log("shorts queue started")
    while not os.path.exists(P + "STOP_SHORTS"):
        if any(not os.path.exists("/home/claude/Bolna-AI-Masterclass/Published-Assets/ep%02d-master.mp4" % n) for n in range(1, 54)):
            time.sleep(60); continue  # long-form has priority on the CPU
        todo = sorted(os.path.basename(os.path.dirname(p)) for p in glob.glob(B + "s*/mix.wav") if not os.path.exists(OUT + os.path.basename(os.path.dirname(p)) + ".mp4") and not os.path.exists(os.path.dirname(p) + "/FAILED"))
        if not todo:
            time.sleep(60); continue
        try:
            render(todo[0])
        except Exception as e:
            log("ERROR %s %s" % (todo[0], str(e)[:600])); open(B + todo[0] + "/FAILED", "w").write(str(e)); time.sleep(30)


if __name__ == "__main__":
    c = sys.argv[1]
    if c == "bundle": bundle()
    elif c == "render": [render(s) for s in sys.argv[2:]]
    elif c == "queue": queue()
    elif c == "sheet": sheet(int(sys.argv[2]))
    elif c == "audit": [print(audit_render(s)) for s in sys.argv[2:]]
    elif c == "approve":  # human-eye visual review of the contact sheet passed
        for s in sys.argv[2:]:
            a = json.load(open(B + s + "/audit.json")); a["pass_visual_review"] = True; json.dump(a, open(B + s + "/audit.json", "w"), indent=1)
        print("approved", sys.argv[2:])
