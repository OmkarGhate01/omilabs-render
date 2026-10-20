"""Package rendered ElevenLabs items into the GitHub publisher repo (run by tick.sh after renders).
Long: Published-Assets/youtube-upload/elevenlabs/elNN.json + Thumbnails/el-epNN-thumbnail.png
Shorts: Production/shorts/el_batchNN.py + Production/build/shorts/eNNN/audit.json
Media itself goes up via push_media.sh as media/el-*.mp4 (see tick.sh)."""
import os, json, shutil, glob, re
from publish_check import meta
R = "/home/claude/ElevenLabs-Masterclass/"
G = os.environ.get("PKG_OUT", "/home/claude/omilabs-publisher/")
os.makedirs(G + "Published-Assets/youtube-upload/elevenlabs", exist_ok=True)
os.makedirs(G + "Thumbnails", exist_ok=True)
# SEO audit 21 Oct: titles <= 70 chars, keyword first; "ElevenLabs" in the first description line.
TITLES = {
    11: "ElevenLabs Professional Voice Cloning: Clone Your Own Voice",
    13: "Share Your Voice on ElevenLabs and Earn: Voice Library Payouts",
    17: "ElevenLabs Agent Conversation Flow: Turn-Taking and Interruptions",
    18: "ElevenLabs Agent Voice Settings: Speed, Expressive Mode, Pronunciation",
    20: "ElevenLabs Agent Tools Explained: Client, Webhook, Code, MCP",
    22: "ElevenLabs System Tools: End Call, Transfer and Language Detection",
    25: "ElevenLabs Voice Agent SDKs: React, JavaScript and Python",
    28: "Test Your ElevenLabs Voice Agent: Testing and Simulated Chats",
    29: "ElevenLabs Conversation Analysis: Success Evaluation + Data",
    30: "What Does an ElevenLabs Voice Agent Cost? Pricing and Limits",
    32: "ElevenLabs API for Developers: Streaming, Latency, Speech to Text",
}
done = []
import sys
ONLY = [int(a) for a in sys.argv[1:]]
for n in (ONLY or range(1, 34)):
    m = R + "Published-Assets/ep%02d-master.mp4" % n
    th = R + "Thumbnails/ep%02d-thumbnail.png" % n
    seo = R + "SEO/episode-%02d-seo.md" % n
    if not (os.path.exists(m) and os.path.exists(th) and os.path.exists(seo)):
        continue
    title, desc, tags, pin = meta(n)
    assert "{{" not in desc and len(desc) <= 5000 and len(title) <= 100, "ep%02d package check failed" % n
    desc = desc.replace("<", "").replace(">", "")
    title = TITLES.get(n, title)
    assert len(title) <= 70, (n, len(title))
    if "elevenlabs" not in "\n".join(desc.split("\n")[:2]).lower():
        desc = "ElevenLabs tutorial: %s.\n\n%s" % (title, desc)
    json.dump(dict(title=title, desc=desc, tags=tags, pinned=pin), open(G + "Published-Assets/youtube-upload/elevenlabs/el%02d.json" % n, "w"), indent=1)
    shutil.copy(th, G + "Thumbnails/el-ep%02d-thumbnail.png" % n)
    done.append(n)
for p in ([] if ONLY else glob.glob(R + "Production/shorts/batch*.py")):
    shutil.copy(p, G + "Production/shorts/el_" + os.path.basename(p))
for p in ([] if ONLY else glob.glob(R + "Production/build/shorts/e*/audit.json")):
    sid = p.split("/")[-2]
    os.makedirs(G + "Production/build/shorts/" + sid, exist_ok=True)
    shutil.copy(p, G + "Production/build/shorts/%s/audit.json" % sid)
print("packaged long:", done)
