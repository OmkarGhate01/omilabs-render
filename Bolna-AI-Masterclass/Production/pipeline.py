"""Bundle, QA contact sheets, background render queue and post-processing.
  python3 pipeline.py bundle
  python3 pipeline.py qa 2            -> Production/qa/ep02-sheet.jpg
  python3 pipeline.py ready 2 3       -> mark episodes ready for the render queue
  python3 pipeline.py queue           -> run the render queue (use nohup ... &)
  python3 pipeline.py post 2          -> mux audio, loudnorm, thumbnail, preview copy
"""
import sys, os, json, subprocess, time, glob, shutil
from common import *

BUNDLE = BUILD + "bundle"
PUB = ROOT + "Published-Assets/"
PREV = PUB + "previews/"
LOG = PROD + "queue.log"


def sh(cmd, cwd=PROJ, check=True):
    r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError("FAILED: %s\n%s\n%s" % (cmd, r.stdout[-2000:], r.stderr[-3000:]))
    return r.stdout


def log(msg):
    with open(LOG, "a") as f:
        f.write(time.strftime("%H:%M:%S ") + msg + "\n")


def bundle():
    out = BUILD + "bundle-" + time.strftime("%m%d%H%M%S")
    sh("npx remotion bundle src/index.ts --out-dir %s --log=error" % out)
    open(BUILD + "bundle.txt", "w").write(out)
    print("bundled", out)


def cur_bundle():
    p = BUILD + "bundle.txt"
    return open(p).read().strip() if os.path.exists(p) else BUNDLE


def qa_frames(n):
    p = json.load(open(BUILD + "ep%02d/props.json" % n))
    segs, scenes = p["segments"], p["scenes"]
    fr = []
    for sg in segs:
        if sg["kind"] == "title":
            fr.append(sg["from"] + 75)
            continue
        sc = scenes[sg["scene"]]
        cues = [l for l in sc["lines"] if l["cue"]]
        if sc["type"] == "hook":
            for l in cues[:2] + cues[-1:]:
                fr.append(int(l["start"] * FPS) + 30)
            continue
        last = cues[-1]["start"] if cues else sc["start"]
        if sc["type"] == "recap":
            nx = [l for l in sc["lines"] if l["cue"] == "bye"]
            fr.append(int(((cues[-3]["start"] if len(cues) >= 3 else last) + 1.2) * FPS))
            fr.append(int((nx[0]["end"] + 0.8) * FPS) if nx else sg["to"] - 30)
            continue
        fr.append(min(sg["to"] - 12, int((last + 1.6) * FPS)))
    return sorted(set(max(0, min(p["durationInFrames"] - 1, f)) for f in fr))


def qa(n):
    from PIL import Image, ImageDraw
    fr = qa_frames(n)
    od = PROD + "qa/ep%02d" % n
    if os.path.exists(od):
        shutil.rmtree(od)
    sh("node qa.mjs %s %s %s %s" % (cur_bundle(), BUILD + "ep%02d/props.json" % n, od, ",".join(map(str, fr))))
    ims = sorted(glob.glob(od + "/*.jpeg"))
    cols = 4
    rows = (len(ims) + cols - 1) // cols
    W, H = 480, 270
    sheet = Image.new("RGB", (W * cols, H * rows), (20, 20, 20))
    d = ImageDraw.Draw(sheet)
    for i, f in enumerate(ims):
        im = Image.open(f).convert("RGB").resize((W, H))
        sheet.paste(im, ((i % cols) * W, (i // cols) * H))
        d.text(((i % cols) * W + 6, (i // cols) * H + 4), os.path.basename(f)[1:-5], fill=(255, 255, 0))
    out = PROD + "qa/ep%02d-sheet.jpg" % n
    sheet.save(out, quality=78)
    print(out, len(ims), "frames")


def master_path(n):
    return PUB + "ep%02d-master.mp4" % n


def post(n, bun=None):
    bun = bun or cur_bundle()
    b = BUILD + "ep%02d/" % n
    os.makedirs(PREV, exist_ok=True)
    dur = json.load(open(b + "props.json"))["durationInFrames"] / FPS
    sh("ffmpeg -y -hide_banner -loglevel error -i %ssilent.mp4 -i %smix.wav -map 0:v -map 1:a -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=9 -ar 48000 -c:a aac -b:a 256k -shortest -movflags +faststart %s" % (b, b, master_path(n) + ".tmp.mp4"), cwd=b)
    os.replace(master_path(n) + ".tmp.mp4", master_path(n))
    sh("npx remotion still %s Thumb %sThumbnails/ep%02d-thumbnail.png --props=%sthumb.json --log=error" % (bun, ROOT, n, b))
    # QA gate 1: master must match the planned duration and carry audio
    probe = json.loads(sh("ffprobe -v error -show_entries format=duration:stream=codec_type -of json %s" % master_path(n)))
    mdur = float(probe["format"]["duration"])
    kinds = [s["codec_type"] for s in probe["streams"]]
    if abs(mdur - dur) > 0.3 or kinds.count("video") != 1 or kinds.count("audio") != 1:
        raise RuntimeError("master check failed ep%02d: dur %.2f vs %.2f, streams %s" % (n, mdur, dur, kinds))
    pv = PREV + "ep%02d-preview.mp4" % n
    target = 26.5e6
    for attempt in range(3):  # single-pass ABR (fast); QA gate 2 re-encodes lower if over 29.5 MB
        vb = int((target * 8 / dur - 112e3) * 0.97)
        sh("ffmpeg -y -hide_banner -loglevel error -i %s -vf scale=1280:720:flags=lanczos -c:v libx264 -preset veryfast -b:v %d -maxrate %d -bufsize %d -pix_fmt yuv420p -c:a aac -b:a 112k -movflags +faststart %s" % (master_path(n), vb, int(vb * 1.5), int(vb * 2), pv), cwd=b)
        if os.path.getsize(pv) <= 29.5e6:
            break
        target *= 0.85
    else:
        raise RuntimeError("preview over size ep%02d" % n)
    for f in glob.glob(b + "x264*") + [b + "silent.mp4", b + "RENDERED"]:
        if os.path.exists(f):
            os.remove(f)
    log("post done ep%02d (master %.1fs ok, %.1f MB preview)" % (n, mdur, os.path.getsize(pv) / 1e6))


def render(n):
    b = BUILD + "ep%02d/" % n
    t0 = time.time()
    bun = cur_bundle()
    log("render start ep%02d (%s)" % (n, os.path.basename(bun)))
    sh("npx remotion render %s Episode %ssilent.mp4 --props=%sprops.json --muted --concurrency=2 --crf=17 --x264-preset=veryfast --log=error" % (bun, b, b))
    log("render done ep%02d in %.1f min" % (n, (time.time() - t0) / 60))
    open(b + "RENDERED", "w").write(bun)


def queue():
    """Render back-to-back; post-processing of the previous episode runs in the background."""
    log("queue started (overlapped post)")
    posting = None
    E = lambda n, f: os.path.exists(BUILD + "ep%02d/%s" % (n, f))

    def pump():
        nonlocal posting
        if posting and posting[1].poll() is not None:
            pn, p = posting
            if p.returncode != 0:
                open(BUILD + "ep%02d/POSTFAIL" % pn, "w").write("see post.log")
                log("ERROR post ep%02d (see post.log)" % pn)
            posting = None
        if not posting:
            pend = [n for n, _, _ in EPS if E(n, "RENDERED") and not E(n, "POSTFAIL")]  # post() removes RENDERED on success
            if pend:
                pn = pend[0]
                posting = (pn, subprocess.Popen([sys.executable, "pipeline.py", "post", str(pn)], cwd=PROD,
                                                stdout=open(PROD + "post.log", "a"), stderr=subprocess.STDOUT))

    while not os.path.exists(PROD + "STOP"):
        pump()
        todo = [n for n, _, _ in EPS if E(n, "READY") and not E(n, "RENDERED") and not E(n, "CLOUD") and not os.path.exists(master_path(n))]
        if not todo:
            time.sleep(20)
            continue
        n = todo[0]
        try:
            render(n)
        except Exception as e:
            log("ERROR ep%02d: %s" % (n, str(e)[:600]))
            if not E(n, "RETRIED"):  # transient (e.g. browser start timeout under load): one automatic retry
                open(BUILD + "ep%02d/RETRIED" % n, "w").write("1")
                time.sleep(30)
                continue
            open(BUILD + "ep%02d/FAILED" % n, "w").write(str(e))
            os.remove(BUILD + "ep%02d/READY" % n)
    while posting:
        time.sleep(10)
        pump()
    log("queue stopped")


if __name__ == "__main__":
    cmd, args = sys.argv[1], [int(a) for a in sys.argv[2:] if a.isdigit()]
    if cmd == "bundle":
        bundle()
    elif cmd == "qa":
        for n in args:
            qa(n)
    elif cmd == "ready":
        for n in args:
            open(BUILD + "ep%02d/READY" % n, "w").write("ok")
            fp = BUILD + "ep%02d/FAILED" % n
            if os.path.exists(fp):
                os.remove(fp)
        print("ready", args)
    elif cmd == "queue":
        queue()
    elif cmd == "post":
        for n in args:
            post(n)
    elif cmd == "render":
        for n in args:
            render(n)
