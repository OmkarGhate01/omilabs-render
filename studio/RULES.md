# Omilabs production rules: v3 (from the YouTube audit, 11 Nov 2026)

`scripts/qa_rules.py` checks these automatically. `make_short.py` refuses to render a spec that fails, unless the spec has `rules: "v2"` (videos made before these rules).

## Channel
- **Language:** Hinglish only for all new videos (Omkar, 11 Nov). The old English Bolna and ElevenLabs videos stay up as they are.
- **Promise:** "AI tools ki problem → fix, Hinglish mein". Every script serves this promise.
- **Cadence:** the current schedule stays as it is (Omkar, 11 Nov). New videos are made for quality, not volume.

## vidIQ / YouTube Analytics facts (14 Oct–11 Nov 2026)
- Of 7,406 Shorts views, only 1,745 were engaged views (24%). About 3 in 4 viewers swipe away at the start, so frame 0 matters most.
- Search brings the most views (4,252, 56%), ahead of the Shorts feed (3,200). Titles need the English search keyword even when the video is in Hinglish.
- Views by country: India 2,616, US 1,210, Pakistan 173.
- Playlist viewers watch 55% of a video for an average of 172 s, the best of any source. Every description links to its playlist.
- In 28 days: 8 subscribers gained, 0 shares. Long videos gained 0 subscribers with an average view duration of 24.5%.

## Shorts (≤40 s)
1. **Frame 0:** a big `d.problem` headline of 2–6 words is visible from the very first frame, with no fade-in. The problem is also both on screen and in the first spoken words. The first beat is a `hook` beat of at most 16 words, and it has a problem or curiosity cue ("?", kyon, galat, fix, kaun, sach).
2. **Broad framing:** the hook is a problem any builder relates to ("AI call bina bataye fail ho rahi hai?"), not jargon ("Disconnected ≠ Completed"). The jargon goes in the explanation.
3. **Template:** 0–2 s problem / 2–10 s why / 10–30 s fix / last line loops back to the hook.
4. **No outro:** no "save / like / subscribe" beat. The last line hands off to the first frame so the Short replays.
5. **Pacing:** each beat is ≤6.5 s, with a new visual every 2–4 s. Pauses between beats are 0.10 s, the tail is 0.35 s, and TTS silence is trimmed from both ends of every line.
6. **Series:** keep the header series label consistent, e.g. "AI FIX #12". Viewers who recognise a series subscribe.

## Long videos (target 6–8 min)
1. Open on the hook (≤22 words) that names the stakes. No intro, no greeting, no logo sting.
2. Use chapter beats every 60–90 s. The description gets timestamps automatically.
3. The CTA comes at the end only, with one line and the channel promise.

## Packaging (all videos)
- **Title:** ≤50 characters. Write it in Roman script and put the English search keyword in it (`search_kw`). Lead with the result or the curiosity, avoid internal jargon, and keep the keyword early.
- **Thumbnail hook:** ≤4 words, high contrast, and complementary to the title. It must not repeat the title's words.
- **Facts:** only from official docs. No fake urgency.

## Manual steps (Omkar, in YouTube Studio; the API can't do these)
- **Related video:** on every top Short, set the "Related video" to its long video.
- **Pinned comment:** pin one question as a comment on each new video, and reply to comments in the first hour.
