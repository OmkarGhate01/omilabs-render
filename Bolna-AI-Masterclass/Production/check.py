"""Spec gate without audio: python3 check.py 5 [6 ...] -> lint errors + grounding report."""
import sys, build
from common import load_spec
for a in sys.argv[1:]:
    n = int(a); ep = load_spec(n)
    e = build.lint(ep)
    print("ep%02d lint:" % n, "OK" if not e else e)
    build.grounding(n, ep, ep["scenes"])
