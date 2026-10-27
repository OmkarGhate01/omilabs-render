"""
new_series.py — Muse AI, ElevenLabs v4, Claude Motion, Kling 4.0
All Shorts-only. 4 series × 10 Shorts = 40 total.
Schedule: after Bolna + EL finish. 4 consecutive days at 10/day.

Series keys:
  Muse AI:         mu001..mu010  → video: Published-Assets/shorts/mu001.mp4 etc.
  ElevenLabs v4:   ev001..ev010  → video: Published-Assets/shorts/ev001.mp4
  Claude Motion:   cm001..cm010  → video: Published-Assets/shorts/cm001.mp4
  Kling 4.0:       kl001..kl010  → video: Published-Assets/shorts/kl001.mp4
"""

import os
import sys
import runpy
import datetime

# ── paths ──────────────────────────────────────────────────────────────────
R   = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
sys.path.insert(0, R + "Production")
import youtube_upload as Y

SOUT  = R + "Published-Assets/shorts/"          # rendered Short mp4s
SB    = R + "Production/build/shorts/"           # audit.json files
BATCH = R + "Production/shorts/"

IST   = datetime.timezone(datetime.timedelta(hours=5, minutes=30))

# YouTube SLOTS (same as Bolna) — 8 Short slots/day
SLOTS = [(8, 0), (10, 0), (11, 30), (13, 30), (15, 0), (17, 0), (18, 30), (21, 0)]

GATES = ("pass_audio", "pass_render", "pass_visual_auto", "pass_visual_review")

# Manual audio gate overrides (e.g. slight beat overage accepted)
ACCEPT_AUDIO = set()

# ── affiliate / voice constants ─────────────────────────────────────────────
AFFIL    = "https://try.elevenlabs.io/c9bnghlu9434"
EL_VOICE = ("https://elevenlabs.io/app/voice-lab/share/"
             "0ca97729faff22ee3841f4eb985cd7e58e4a7687ba6d4afde460babdf249999d/8WqHCYyrnUqoK70Px5EJ")
AFF_LINE = "ElevenLabs affiliate link (I may earn a commission at no extra cost to you): " + AFFIL
DISCLOSE = "(AI-generated voice | Created by Omkar Ghate, Omilabs)"

# ── load all 4 batch specs ──────────────────────────────────────────────────
def _load_batch(fname):
    return runpy.run_path(BATCH + fname)["SHORTS"]

def specs():
    out = []
    for f in ("batch_muse.py", "batch_el_v4.py", "batch_claude_motion.py", "batch_kling.py"):
        try:
            out += _load_batch(f)
        except FileNotFoundError:
            pass
    return out


# ── series metadata ─────────────────────────────────────────────────────────
_META = {
    "muse": dict(
        label="Muse AI",
        hashtags="#Shorts #MuseAI #AIVideo #VideoHosting",
        docs_url="https://muse.ai",
        desc_suffix="Created by Omkar Ghate (Omilabs). Independent educational content; not affiliated with or endorsed by Muse AI. %s" % DISCLOSE,
        tag_suffix=["muse ai tutorial", "muse ai", "ai video", "omilabs", "shorts"],
        brand_in_title="Muse AI",
        aff_line=None,
    ),
    "el_v4": dict(
        label="ElevenLabs v4",
        hashtags="#Shorts #ElevenLabs #AIVoice #ElevenLabsV4",
        docs_url="https://elevenlabs.io/docs",
        desc_suffix=("My ElevenLabs voice (use it in your videos): %s\n%s\n\n"
                     "Built from official ElevenLabs documentation: https://elevenlabs.io/docs\n"
                     "Created by Omkar Ghate (Omilabs). Independent educational content; not affiliated with ElevenLabs. %s"
                     % (EL_VOICE, AFF_LINE, DISCLOSE)),
        tag_suffix=["elevenlabs v4", "elevenlabs tutorial", "ai voice", "omilabs", "shorts"],
        brand_in_title="ElevenLabs",
        aff_line=AFF_LINE,
    ),
    "claude_motion": dict(
        label="Claude Motion",
        hashtags="#Shorts #ClaudeMotion #AnthropicAI #AIAnimation",
        docs_url="https://claude.ai",
        desc_suffix="Created by Omkar Ghate (Omilabs). Independent educational content; not affiliated with or endorsed by Anthropic. %s" % DISCLOSE,
        tag_suffix=["claude motion", "claude ai", "ai animation", "omilabs", "shorts"],
        brand_in_title="Claude",
        aff_line=None,
    ),
    "kling": dict(
        label="Kling 4.0",
        hashtags="#Shorts #Kling #KlingAI #AIVideo",
        docs_url="https://klingai.com",
        desc_suffix="Created by Omkar Ghate (Omilabs). Independent educational content; not affiliated with or endorsed by Kling AI. %s" % DISCLOSE,
        tag_suffix=["kling 4.0", "kling ai", "ai video generator", "omilabs", "shorts"],
        brand_in_title="Kling",
        aff_line=None,
    ),
}

def _meta(series):
    return _META.get(series, _META["muse"])


# ── title / desc / tags ─────────────────────────────────────────────────────
def short_title(s):
    m = _meta(s["series"])
    t = s["title"]
    brand = m["brand_in_title"]
    if brand.lower() not in t.lower() and len(t) + len(brand) + 3 <= 70:
        t += " | " + brand
    return t[:95]


def short_desc(s):
    m = _meta(s["series"])
    hook = s["beats"][0]["say"]
    d = ("%s | %s tutorial: %s.\n\n%s\n\n%s"
         % (hook, m["label"], s["topic"], m["desc_suffix"], m["hashtags"]))
    return d.replace("<", "").replace(">", "")


def tags_trim(tags):
    out, n = [], 0
    for t in tags:
        if t.lower() not in [x.lower() for x in out] and n + len(t) + 3 <= 480:
            out.append(t); n += len(t) + 3
    return out


def short_tags(s):
    m = _meta(s["series"])
    return tags_trim(s["tags"] + m["tag_suffix"])


# ── schedule: append 4 consecutive days after EL finishes ──────────────────
def extend_schedule(st, out, _planned, next_slot, LSLOTS, SLOTS_unused, floor):
    """
    Appends new-series Short slots AFTER the last ElevenLabs Short already in `out`.
    Mutates `out` in place, returns it.
    """
    # find last EL Short slot in out (keys like "e001"..."e067")
    el_short_keys = [k for k in out if k.startswith("e") and k[1:].isdigit()]
    last_el = max((out[k] for k in el_short_keys), default=None) if el_short_keys else None

    # also check Bolna Shorts last slot
    bo_short_keys = [k for k in out if k.startswith("s") and k[1:].isdigit()]
    last_bo = max((out[k] for k in bo_short_keys), default=None) if bo_short_keys else None

    # start from whichever finishes last
    candidates = [t for t in [last_el, last_bo, floor] if t is not None]
    start = max(candidates) + datetime.timedelta(minutes=1) if candidates else floor

    prev = None
    for s in specs():
        sid = s["id"]
        p = _planned(st, sid)
        if p:
            out[sid] = p
            prev = p
            continue
        t = next_slot(max(start, prev + datetime.timedelta(minutes=1)) if prev else start, SLOTS)
        out[sid] = prev = t

    return out


# ── items for plan() ────────────────────────────────────────────────────────
def items(st, W):
    res = []
    for s in specs():
        sid = s["id"]
        a = Y.jload(SB + sid + "/audit.json", {})
        bad = [g for g in GATES if not a.get(g) and not (g == "pass_audio" and sid in ACCEPT_AUDIO)]
        video = SOUT + sid + ".mp4"
        have = Y.have(video)
        res.append(dict(
            key=sid,
            kind="short",
            series=s["series"],
            n=int(sid[2:]),        # numeric part after 2-char prefix
            spec=s,
            when=W.get(sid),
            done=bool(st.get(sid, {}).get("video")),
            ready=have and not bad,
            video=video,
            why=("audit: " + ",".join(bad)) if bad else ("" if have else "not rendered"),
        ))
    return res


# ── upload helpers (called from youtube_publisher.upload_short) ─────────────
def handles(series):
    """Return True if this module handles this series key."""
    return series in _META


def get_title_desc_tags(s, st, W):
    return short_title(s), short_desc(s), short_tags(s)
