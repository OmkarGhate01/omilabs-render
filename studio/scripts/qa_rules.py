"""Omilabs upload rules (YouTube audit, 11 Nov 2026). make_short.py refuses to render a spec that breaks them.
Shorts: problem on frame 0, no outro/subscribe beat (loop), tight pacing, <=40 s.
All: title <=50 chars, thumbnail hook <=4 words that does not repeat the title."""
import re

PROBLEM = re.compile(r"(\?|क्यों|गलत|problem|fix|मत|नहीं|ruk|band|fail|error|slow|wrong|trap|sach|सच|फर्क|vs|kaun|कौन|kya|क्या)", re.I)
CHARS_PER_SEC = 15.0   # Madhur at +8%, Devanagari + English mix


def words(s): return [w for w in re.split(r"\s+", re.sub(r"[^\w\u0900-\u097F ]", " ", s.lower())) if w]


def check(spec):
    errs = []
    long = spec.get("format") == "long"
    beats = spec.get("beats", [])
    title = spec.get("title", "")
    if title and len(title) > 50:
        errs.append("title %d chars > 50: %s" % (len(title), title))
    th = spec.get("thumb")
    if th:
        hw = words(th.get("hook", ""))
        if len(hw) > 4:
            errs.append("thumbnail hook has %d words > 4" % len(hw))
        if title and hw and set(hw) <= set(words(title)):
            errs.append("thumbnail hook repeats the title")
    if not beats:
        return errs + ["no beats"]
    first = beats[0]
    if first.get("v") != "hook":
        errs.append("first beat must be a hook (problem on frame 0)")
    if len(words(first.get("say", ""))) > (22 if long else 16):
        errs.append("first line too long (%d words): get to the problem faster" % len(words(first["say"])))
    if not PROBLEM.search(first.get("say", "") + " " + str(first.get("d", {}))):
        errs.append("first line has no problem/curiosity cue")
    if not long:
        if any(b.get("v") == "cta" for b in beats):
            errs.append("Shorts end without a CTA beat (loop into replay)")
        est = sum(len(b.get("say", "")) for b in beats) / CHARS_PER_SEC + 0.12 * len(beats)
        if est > 40:
            errs.append("estimated %.0f s > 40 s" % est)
        for b in beats:
            if len(b.get("say", "")) / CHARS_PER_SEC > 6.5:
                errs.append("beat %s too long for one visual (>6.5 s): split it" % b.get("tag"))
    return errs
