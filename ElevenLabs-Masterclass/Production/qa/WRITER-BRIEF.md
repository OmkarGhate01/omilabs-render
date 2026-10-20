# Spec-writer brief: ElevenLabs Masterclass (Omilabs channel, creator Omkar Ghate)

Goal: write docs-grounded episode specs + Shorts specs for an English YouTube course that should outperform our Bolna AI series.

## Inputs
- Curriculum (episode number, module, working title): /home/claude/ElevenLabs-Masterclass/Production/curriculum.py
- Research packet per episode (official ElevenLabs docs, full markdown): /home/claude/ElevenLabs-Masterclass/Research/packets/epNN.md. Doc page slugs are in /home/claude/ElevenLabs-Masterclass/Research/epmap.py; a slug "eleven-agents/quickstart" means https://elevenlabs.io/docs/eleven-agents/quickstart
- FORMAT REFERENCE (copy the structure exactly): /home/claude/Bolna-AI-Masterclass/Production/specs/ep20.py and ep05.py, ep12.py (long episodes); /home/claude/Bolna-AI-Masterclass/Production/shorts/batch01.py (Shorts). Valid scene types and fields are enforced by lint() in /home/claude/ElevenLabs-Masterclass/Production/build.py (read it); Short beat visuals (v=...) are in /home/claude/ElevenLabs-Masterclass/Production/shorts_build.py and /home/claude/Bolna-AI-Masterclass/Video-Projects/omilabs-remotion/src/engine/Short.tsx.
- Icons available: /home/claude/Bolna-AI-Masterclass/Video-Projects/omilabs-remotion/src/engine/icons.tsx (use only names defined there).

## Outputs
- /home/claude/ElevenLabs-Masterclass/Production/specs/epNN.py  (EP = dict(...)), one per assigned episode.
  - `sources` = the doc slugs used (from epmap.py). Scene `src` = slug.
  - Title: keep the curriculum title unless a clearer search phrase fits; must contain "ElevenLabs" (or "ElevenAgents"/"ElevenCreative" with ElevenLabs in kws).
  - 8–13 scenes, ~7–11 min of narration, first scene hook, last scene recap. One idea per scene; vary scene types (cards, steps, compare, code, table, timeline, graph, pipeline, checklist, callout, chips, terminal, bars, stat, sequence).
  - seo: 3 titles, kw, 6 kws, intent, desc (2–4 sentences), 11 tags (include "elevenlabs", "omilabs", "omkar ghate"), pinned (a question that invites comments), shorts (3 ideas).
- /home/claude/ElevenLabs-Masterclass/Production/shorts/batchNN.py (batch number given to you): SHORTS list with exactly 2 Shorts per assigned episode, ids given to you, in the batch01.py format. CTA line: "Save this, and watch the full lesson in episode %d." Titles end WITHOUT a series suffix (the publisher adds it). Hook ≤ 8 words with a pain point or question. 5–7 beats, 15–40 s spoken, every beat ≤ 6.5 s spoken. Mood words matter: green for good outcomes, red for bad ones.

## Hard rules
1. Facts only from the packet: every model name, number, limit, price, UI label, parameter, file format, language count must appear in the packet text. Never invent endpoints, models, pricing, or capabilities. If the docs don't say it, don't say it. Prices change: say "check the pricing page" instead of quoting unless the packet states it.
2. Episodes are documented walkthroughs, not live demos. Never say "as you can see on my screen", never claim we tested it.
3. Code scenes: only code that appears in (or is a direct trim of) the packet; keep API key in an env var `ELEVENLABS_API_KEY`.
4. No fake urgency, no "guaranteed viral", no affiliation claims (Omilabs is independent; not affiliated with ElevenLabs).
5. Spoken lines must sound natural read aloud by a TTS voice: short sentences, no markdown, spell numbers the way they should be spoken where ambiguous, use the "||" spoken variant for anything with symbols/URLs.
6. Run `cd /home/claude/ElevenLabs-Masterclass/Production && python3 check.py NN` for every episode. Lint must be OK. Grounding: fix every unverified token that is a real fact; tokens that are plain English words are fine — list any you kept in your final report.
7. Shorts: only facts that also appear in that episode's spec.
8. Do not render, do not run TTS, do not touch files outside your assigned outputs.

## Report back (short)
Episodes written, lint status, kept grounding tokens per episode, and any doc gaps.
