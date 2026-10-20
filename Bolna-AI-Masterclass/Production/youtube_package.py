"""Build the YouTube Studio upload package for rendered, QA-passed episodes.
  python3 youtube_package.py 1 2 ... -> Published-Assets/youtube-upload/"""
import sys, os, re, csv, datetime, shutil
sys.path.insert(0, os.path.dirname(__file__))
from publish_check import meta
R = "/home/claude/Bolna-AI-Masterclass/"; OUT = R + "Published-Assets/youtube-upload/"
os.makedirs(OUT, exist_ok=True)
DISCLOSE = "Narration uses a synthetic text-to-speech voice; visuals are motion graphics built from the docs, not screen recordings of the Bolna dashboard."
from youtube_upload import long_time
PLAYLIST_TITLE = "Bolna AI Masterclass (Full Course)"
PLAYLIST_DESC = ("A 53-episode course on building voice AI agents with Bolna: agent setup, prompts, graph agents, "
                 "speech and models, telephony, the API, tools and automation, and running in production. "
                 "Every episode is a documented walkthrough built from the official Bolna documentation, with sources in each description. "
                 "Created by Omkar Ghate (Omilabs). Independent educational content; not affiliated with or endorsed by Bolna.")
open(OUT + "00-playlist.txt", "w").write("PLAYLIST TITLE\n%s\n\nPLAYLIST DESCRIPTION\n%s\n\nVisibility: Public\nOrder: Manual, Episode 1 first\n" % (PLAYLIST_TITLE, PLAYLIST_DESC))
rows = []
for i, n in enumerate([int(a) for a in sys.argv[1:]]):
    title, desc, tags, pin = meta(n)
    desc = desc.replace("It does not include a live product recording.", "It does not include a live product recording. " + DISCLOSE)
    if DISCLOSE not in desc: desc += "\n\n" + DISCLOSE
    desc = desc.replace("Full playlist: Bolna AI Masterclass", "Full playlist: " + PLAYLIST_TITLE)
    assert len(desc) <= 5000 and "<" not in desc and ">" not in desc
    when = long_time(n).replace(tzinfo=None)  # fixed slot per episode: two a day (12:00 + 19:00 IST) from 16 Oct
    master = "ep%02d-master.mp4" % n; thumb = "ep%02d-thumbnail.png" % n; srt = "ep%02d-en.srt" % n
    shutil.copy(R + "Subtitles/" + srt, OUT + srt)
    txt = ("EPISODE %02d\n\nVIDEO FILE: Published-Assets/%s\nTHUMBNAIL: Thumbnails/%s\nCAPTIONS: %s (English)\n\n"
           "TITLE\n%s\n\nDESCRIPTION\n%s\n\nTAGS\n%s\n\nPLAYLIST: %s\n"
           "SCHEDULE: %s IST (Visibility: Schedule -> Public)\n"
           "Audience: No, it's not made for kids | Category: Education | Video language: English\n"
           "Altered or synthetic content: No (narration voice is disclosed in the description; nothing depicts real people or events)\n"
           "End screen: Next episode + Playlist | Cards: none\n\nPINNED COMMENT (post after publish)\n%s\n") % (
        n, master, thumb, srt, title, desc, ", ".join(tags), PLAYLIST_TITLE, when.strftime("%a %d %b %Y, %I:%M %p"), pin)
    open(OUT + "ep%02d-youtube.txt" % n, "w").write(txt)
    rows.append([n, title, when.strftime("%Y-%m-%d %H:%M IST"), master, thumb, srt, len(desc), "QA passed"])
with open(OUT + "schedule.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["episode", "title", "publish_at", "video", "thumbnail", "captions", "desc_chars", "status"]); w.writerows(rows)
print("package:", len(rows), "episodes ->", OUT)
