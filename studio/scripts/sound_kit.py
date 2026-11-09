# Procedural, license-free sound kit for Omilabs Shorts (no samples, no downloads):
# a soft lo-fi music bed per series + SFX (whoosh, pop, click, ding). Pure numpy -> 44.1 kHz WAV.
import os, wave
import numpy as np

SR = 44100
rng = np.random.default_rng(7)


def save(path, x):
    x = np.clip(x, -1, 1)
    pcm = (x * 32767).astype(np.int16)
    if pcm.ndim == 1:
        pcm = np.stack([pcm, pcm], 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())


def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR); y = np.empty_like(x); s = 0.0
    for i, v in enumerate(x):
        s = (1 - a) * v + a * s; y[i] = s
    return y


def lp_fast(x, cutoff, passes=2):
    # cheap low-pass: moving average approximating a one-pole (vectorised)
    k = max(1, int(SR / (cutoff * 2.2)))
    ker = np.ones(k) / k
    for _ in range(passes):
        x = np.convolve(x, ker, mode="same")
    return x


def note(f):
    return 440.0 * 2 ** ((f - 69) / 12)


# series moods: (root midi, chord progression in semitones from root, bpm)
MOODS = {
    "MUSE AI": (57, [[0, 3, 7, 10], [-4, 0, 3, 7], [-7, -3, 0, 5], [-2, 2, 5, 9]], 92),      # A minor-ish, warm
    "KLING 4.0": (55, [[0, 4, 7, 11], [-3, 0, 4, 7], [5, 9, 12, 16], [2, 5, 9, 12]], 100),    # G major 7, bright
    "CLAUDE MOTION": (60, [[0, 4, 7, 11], [5, 9, 12, 16], [-3, 0, 4, 7], [7, 11, 14, 17]], 96),  # C maj7, airy
    "ELEVENLABS V4": (52, [[0, 3, 7, 10], [5, 8, 12, 15], [-2, 2, 5, 9], [3, 7, 10, 14]], 88),  # E minor, smooth
}


def music(series, seconds=48):
    root, prog, bpm = MOODS.get(series, MOODS["CLAUDE MOTION"])
    n = int(seconds * SR); t = np.arange(n) / SR; out = np.zeros(n)
    beat = 60 / bpm; bar = 4 * beat
    # pad: each chord 1 bar, soft sines + slight detune, slow swell
    for i in range(int(seconds / bar) + 1):
        ch = prog[i % len(prog)]; s0 = int(i * bar * SR); s1 = min(n, int((i + 1) * bar * SR) + int(0.3 * SR))
        if s0 >= n: break
        tt = np.arange(s1 - s0) / SR
        env = np.minimum(1, tt / 0.6) * np.minimum(1, (tt[-1] - tt + 1e-3) / 0.4)
        for semi in ch:
            f = note(root + semi)
            out[s0:s1] += 0.05 * env * (np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 1.003 * tt) + 0.15 * np.sin(4 * np.pi * f * tt))
        # pluck arpeggio, 8th notes, one octave up
        for k in range(8):
            ps = s0 + int(k * beat / 2 * SR)
            if ps >= n: break
            L = min(int(0.45 * SR), n - ps); pt = np.arange(L) / SR
            f = note(root + 12 + ch[[0, 2, 1, 3, 2, 1, 3, 2][k]])
            out[ps:ps + L] += 0.045 * np.exp(-pt * 7) * (np.sin(2 * np.pi * f * pt) + 0.3 * np.sin(4 * np.pi * f * pt))
    # drums: soft kick on 1 and 3, closed hat on off-beats
    nb = int(seconds / beat)
    for b in range(nb):
        s = int(b * beat * SR)
        if b % 2 == 0:
            L = int(0.3 * SR); kt = np.arange(L) / SR
            f = 110 * np.exp(-kt * 18) + 45
            out[s:s + L] += 0.35 * np.exp(-kt * 9) * np.sin(2 * np.pi * np.cumsum(f) / SR)
        hs = s + int(beat / 2 * SR); L = int(0.05 * SR)
        if hs + L < n:
            nz = rng.standard_normal(L); nz = nz - lp_fast(nz, 6000, 1)
            out[hs:hs + L] += 0.05 * np.exp(-np.arange(L) / SR * 60) * nz
    out = lp_fast(out, 9000, 1)
    out /= np.max(np.abs(out)) + 1e-9
    fade = int(1.5 * SR); out[-fade:] *= np.linspace(1, 0, fade)
    return 0.8 * out


def whoosh():
    L = int(0.42 * SR); t = np.arange(L) / SR
    nz = rng.standard_normal(L)
    env = np.sin(np.pi * np.clip(t / 0.42, 0, 1)) ** 2
    lo = lp_fast(nz, 2500, 2); hi = nz - lp_fast(nz, 700, 1)
    mix = (1 - t / 0.42) * lo + (t / 0.42) * hi * 0.6
    x = env * mix; return 0.9 * x / (np.max(np.abs(x)) + 1e-9)


def pop():
    L = int(0.09 * SR); t = np.arange(L) / SR
    f = 300 + 700 * np.exp(-t * 45)
    x = np.exp(-t * 38) * np.sin(2 * np.pi * np.cumsum(f) / SR)
    return 0.9 * x / np.max(np.abs(x))


def click():
    L = int(0.03 * SR); t = np.arange(L) / SR
    x = np.exp(-t * 220) * (0.6 * rng.standard_normal(L) + np.sin(2 * np.pi * 2200 * t))
    return 0.8 * x / np.max(np.abs(x))


def ding():
    L = int(1.1 * SR); t = np.arange(L) / SR
    x = np.exp(-t * 4) * (np.sin(2 * np.pi * 1318.5 * t) + 0.6 * np.sin(2 * np.pi * 1760 * t) + 0.25 * np.sin(2 * np.pi * 2637 * t))
    return 0.8 * x / np.max(np.abs(x))


def ensure(root):
    d = os.path.join(root, "assets", "sound"); os.makedirs(d, exist_ok=True)
    for name, fn in (("whoosh", whoosh), ("pop", pop), ("click", click), ("ding", ding)):
        p = os.path.join(d, name + ".wav")
        if not os.path.exists(p):
            save(p, fn())
    for s in MOODS:
        p = os.path.join(d, "music-" + s.lower().replace(" ", "-").replace(".", "") + ".wav")
        if not os.path.exists(p):
            save(p, music(s))
    return d


def music_long(root, series, seconds):
    d = os.path.join(root, "assets", "sound"); os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "music-%s-%ds.wav" % (series.lower().replace(" ", "-").replace(".", ""), int(seconds)))
    if not os.path.exists(p):
        save(p, music(series, seconds))
    return p


def music_path(root, series):
    return os.path.join(root, "assets", "sound", "music-" + series.lower().replace(" ", "-").replace(".", "") + ".wav")


if __name__ == "__main__":
    import sys
    print(ensure(sys.argv[1] if len(sys.argv) > 1 else "."))
