"""Print the grounded source material (episode scene narration) for each short idea."""
import runpy, re, sys
def toks(s): return set(re.findall(r"[a-z0-9]+", s.lower())) - {"the","a","to","in","of","and","your","you","it","for","with","on","is","what","how","why"}
for e in [int(x) for x in sys.argv[1:]]:
    EP = runpy.run_path("specs/ep%02d.py" % e)["EP"]
    for idea in EP["seo"]["shorts"][:2]:
        best = max(EP["scenes"][1:-1], key=lambda s: len(toks(idea) & toks(" ".join([s.get("title",""), s.get("label","")] + s["lines"]))))
        lines = " ".join(re.sub(r"^@\S+\s*", "", l).split(" || ")[0] for l in best["lines"])
        print("EP%02d | %s | scene: %s (%s)\n  %s\n" % (e, idea, best.get("title", best["label"]), best["type"], lines[:700]))
