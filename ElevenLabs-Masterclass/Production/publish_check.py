"""YouTube-readiness check for rendered episodes: metadata limits, chapters, thumbnails, masters."""
import re, os, json, subprocess, sys
R = "/home/claude/ElevenLabs-Masterclass/"
def ts(s):
    p = [int(x) for x in s.split(":")]; return p[0]*60+p[1] if len(p)==2 else p[0]*3600+p[1]*60+p[2]
def meta(n):
    t = open(R+"SEO/episode-%02d-seo.md"%n).read()
    title = re.search(r"1\. (.+?) \*\*\(recommended\)\*\*", t).group(1).strip()
    desc = re.search(r"## Description\s+```\n(.*?)\n```", t, re.S).group(1)
    tags = [x.strip() for x in re.search(r"## Tags\s+\n(.+?)\n", t).group(1).split(",")]
    pin = re.search(r"## Pinned comment\s+```\n(.*?)\n```", t, re.S)
    return title, desc, tags, (pin.group(1) if pin else "")
if __name__ == "__main__":
    out=[]; bad=0
    for n in [int(a) for a in sys.argv[1:]]:
        issues=[]
        title, desc, tags, pin = meta(n)
        if len(title)>100: issues.append("title %d chars"%len(title))
        if len(desc)>5000: issues.append("desc %d chars"%len(desc))
        if "<" in desc or ">" in desc: issues.append("angle bracket in desc")
        if "<" in title or ">" in title: issues.append("angle bracket in title")
        tl = sum(len(x)+(2 if " " in x else 0) for x in tags)+len(tags)-1
        if tl>500: issues.append("tags %d chars"%tl)
        ch = re.findall(r"^(\d{1,2}:\d{2}(?::\d{2})?) (.+)$", desc, re.M)
        secs=[ts(a) for a,_ in ch]
        m = R+"Published-Assets/ep%02d-master.mp4"%n
        dur = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",m],capture_output=True,text=True).stdout or 0)
        if not secs or secs[0]!=0: issues.append("chapters must start 00:00")
        if len(secs)<3: issues.append("fewer than 3 chapters")
        if any(b-a<10 for a,b in zip(secs,secs[1:])) or (secs and dur-secs[-1]<10): issues.append("chapter shorter than 10s")
        if secs and secs[-1]>=dur: issues.append("chapter past end")
        th = R+"Thumbnails/ep%02d-thumbnail.png"%n
        wh = subprocess.run(["ffprobe","-v","error","-select_streams","v","-show_entries","stream=width,height","-of","csv=p=0",th],capture_output=True,text=True).stdout.strip()
        w,h = map(int,wh.split(","))
        if abs(w/h-16/9)>0.01 or w<1280: issues.append("thumb %s"%wh)
        if os.path.getsize(th)>2e6: issues.append("thumb %.1f MB"%(os.path.getsize(th)/1e6))
        if not os.path.exists(m): issues.append("no master")
        out.append(dict(n=n,title=title,dur=round(dur,1),chapters=len(secs),tags_chars=tl,desc_chars=len(desc),thumb=wh,issues=issues))
        bad+=bool(issues)
    for o in out: print("ep%02d %-4s %5.0fs ch=%2d desc=%4d tags=%3d thumb=%s  %s"%(o["n"],"OK" if not o["issues"] else "FIX",o["dur"],o["chapters"],o["desc_chars"],o["tags_chars"],o["thumb"],"; ".join(o["issues"])))
    print("episodes with issues:",bad)
