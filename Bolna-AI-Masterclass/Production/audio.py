"""Original music bed + sound design, synthesized from scratch (no samples)."""
import numpy as np
from scipy.signal import butter, sosfilt, resample_poly

SR = 48000


def lp(x, fc, o=2):
    return sosfilt(butter(o, fc, fs=SR, output="sos"), x)


def hp(x, fc, o=2):
    return sosfilt(butter(o, fc, btype="high", fs=SR, output="sos"), x)


def bp(x, lo, hi):
    return sosfilt(butter(2, [lo, hi], btype="band", fs=SR, output="sos"), x)


mtof = lambda m: 440.0 * 2 ** ((m - 69) / 12.0)

PROGS = {
    "a": [(0, "m"), (-4, "M"), (3, "M"), (-2, "M")],  # i VI III VII
    "b": [(0, "m"), (-2, "M"), (-4, "M"), (-2, "M")],  # i VII VI VII
    "c": [(0, "m"), (5, "m"), (-4, "M"), (-2, "M")],  # i iv VI VII
}
MUSIC = {
    1: (90, 50, "a"), 2: (94, 45, "b"), 3: (88, 52, "c"), 4: (96, 48, "a"),
    5: (92, 43, "b"), 6: (98, 47, "c"), 7: (92, 49, "a"), 8: (86, 46, "b"),
}


def chord(root, q):
    third = 3 if q == "m" else 4
    return [root, root + 7, root + 12, root + 12 + third, root + 19]


class Track:
    def __init__(self, n):
        self.L = np.zeros(n, np.float32)
        self.R = np.zeros(n, np.float32)
        self.n = n

    def add(self, x, at, g=1.0, pan=0.5):
        s = int(at * SR)
        if s >= self.n or s + len(x) <= 0:
            return
        if s < 0:
            x = x[-s:]
            s = 0
        x = x[: self.n - s].astype(np.float32)
        self.L[s : s + len(x)] += x * g * (1 - pan) * 2 * 0.7071
        self.R[s : s + len(x)] += x * g * pan * 2 * 0.7071

    def st(self):
        return np.stack([self.L, self.R], 1)


def music(dur, module, sections, seed=1):
    """sections: list of (t0, t1, name) with name in hook/title/content/end."""
    bpm, key, pk = MUSIC.get(module, MUSIC[1])
    prog = PROGS[pk]
    rng = np.random.default_rng(seed)
    n = int(dur * SR)
    beat = 60.0 / bpm
    bar = beat * 4
    chord_len = bar * 2
    pad, arp, bass, kick, hat = Track(n), Track(n), Track(n), Track(n), Track(n)

    def sec_at(t):
        for a, b, nm in sections:
            if a <= t < b:
                return nm
        return "content"

    G = {  # layer gains per section
        "hook": dict(pad=1.0, arp=0.9, bass=0.55, kick=0.0, hat=0.5),
        "title": dict(pad=1.0, arp=1.0, bass=1.0, kick=1.0, hat=0.9),
        "content": dict(pad=0.85, arp=0.6, bass=0.6, kick=0.5, hat=0.35),
        "end": dict(pad=1.0, arp=1.0, bass=0.9, kick=0.9, hat=0.8),
    }
    k = 0
    t = 0.0
    while t < dur:
        root, q = prog[k % len(prog)]
        notes = chord(key + root, q)
        L = min(chord_len + 1.6, dur - t + 0.01)
        tt = np.arange(int(L * SR)) / SR
        env = np.minimum(tt / 1.6, 1) * np.minimum(np.maximum(L - tt, 0) / 1.4, 1)
        wob = 1 + 0.12 * np.sin(2 * np.pi * 0.09 * tt + k)
        for i, m in enumerate(notes):
            for det, pan in ((-0.0045, 0.3), (0.0045, 0.7)):
                fr = mtof(m) * (1 + det)
                w = np.sin(2 * np.pi * fr * tt + i) + 0.3 * np.sin(2 * np.pi * 2 * fr * tt) + 0.12 * np.sin(2 * np.pi * 3 * fr * tt)
                pad.add(w * env * wob * (0.042 if i else 0.06), t, G[sec_at(t)]["pad"], pan)
        # 8th-note arp + bass, kick on 1 & 3, hats on off-beats
        steps = int(chord_len / (beat / 2))
        for j in range(steps):
            ts = t + j * beat / 2
            if ts >= dur:
                break
            g = G[sec_at(ts)]
            m = notes[1:][[0, 1, 2, 3, 2, 1, 3, 2][j % 8]] + 12
            x = np.arange(int(0.55 * SR)) / SR
            pl = (np.sin(2 * np.pi * mtof(m) * x) + 0.25 * np.sin(4 * np.pi * mtof(m) * x)) * np.exp(-x * 7.5) * 0.04
            arp.add(pl * (1 if j % 4 == 0 else 0.65), ts, g["arp"], 0.5 + 0.32 * np.sin(j * 1.3))
            if j % 2 == 0 or j % 8 == 7:
                xb = np.arange(int(0.3 * SR)) / SR
                fb = mtof(key + root - 12)
                bw = np.sign(np.sin(2 * np.pi * fb * xb)) * 0.5 + np.sin(2 * np.pi * fb * xb)
                bass.add(bw * np.exp(-xb * 8) * 0.05, ts, g["bass"], 0.5)
            if j % 4 == 0:
                xk = np.arange(int(0.35 * SR)) / SR
                kk = np.sin(2 * np.pi * (45 + 75 * np.exp(-xk * 30)) * xk) * np.exp(-xk * 9) * 0.32
                kick.add(kk, ts, g["kick"], 0.5)
            if j % 2 == 1:
                xh = rng.standard_normal(int(0.05 * SR))
                hat.add(xh * np.exp(-np.arange(len(xh)) / SR * 90) * 0.035, ts, g["hat"], 0.62)
        t += chord_len
        k += 1
    mix = lp(pad.st().T, 2600).T + lp(arp.st().T, 4200).T + lp(bass.st().T, 700).T + kick.st() + hp(hat.st().T, 6000).T
    return mix


# ---------------- SFX ----------------
class Sfx:
    def __init__(self, dur, seed=7):
        self.t = Track(int(dur * SR))
        self.rng = np.random.default_rng(seed)

    def noise(self, d):
        return self.rng.standard_normal(int(d * SR))

    def whoosh(self, at, d=0.7, g=1.0, rise=False):
        x = np.arange(int(d * SR)) / SR
        n = self.noise(d)
        env = np.sin(np.pi * x / d) ** 2
        if rise:
            env = (x / d) ** 2.2
        lo = bp(n, 300, 1200)
        hi = bp(n, 1500, 6000)
        mixk = (x / d) if not rise else (x / d) ** 0.5
        y = (lo * (1 - mixk) + hi * mixk) * env * 0.5
        self.t.add(y, at - d / 2 if not rise else at - d, g, 0.5)

    def impact(self, at, g=1.0):
        x = np.arange(int(1.4 * SR)) / SR
        y = np.sin(2 * np.pi * (44 + 60 * np.exp(-x * 14)) * x) * np.exp(-x * 3.4) * 0.7
        y += lp(self.noise(1.4), 900) * np.exp(-x * 10) * 0.25
        self.t.add(y, at, g, 0.5)

    def riser(self, at, d=1.6, g=1.0):
        x = np.arange(int(d * SR)) / SR
        y = hp(self.noise(d), 1500) * (x / d) ** 2.6 * 0.14 + np.sin(2 * np.pi * (180 + 520 * (x / d) ** 2) * x) * (x / d) ** 2 * 0.06
        self.t.add(y, at - d, g, 0.5)

    def glitch(self, at, d=0.42, g=1.0):
        n = int(d * SR)
        y = np.zeros(n)
        pos = 0
        while pos < n:
            L = int(self.rng.uniform(0.012, 0.05) * SR)
            kind = self.rng.integers(0, 3)
            x = np.arange(min(L, n - pos)) / SR
            if kind == 0:
                seg = np.sign(np.sin(2 * np.pi * self.rng.uniform(200, 1800) * x)) * 0.18
            elif kind == 1:
                seg = np.round(self.rng.standard_normal(len(x)) * 3) / 3 * 0.16
            else:
                seg = np.zeros(len(x))
            y[pos : pos + len(x)] = seg
            pos += L
        self.t.add(hp(y, 200), at - d / 2, g, 0.35 + self.rng.random() * 0.3)

    def shimmer(self, at, d=0.9, g=1.0):
        x = np.arange(int(d * SR)) / SR
        y = sum(np.sin(2 * np.pi * f * x + p) for f, p in ((2093, 0), (2637, 1), (3136, 2), (4186, 3))) * np.exp(-x * 4.5) * 0.03
        y *= np.minimum(x / 0.03, 1)
        self.t.add(y, at, g, 0.5)

    def tick(self, at, g=1.0):
        x = np.arange(int(0.08 * SR)) / SR
        y = (np.sin(2 * np.pi * 1850 * x) + 0.5 * np.sin(2 * np.pi * 2900 * x)) * np.exp(-x * 75) * 0.09
        self.t.add(y, at, g, 0.35 + self.rng.random() * 0.3)

    def blip(self, at, fr=1320, g=1.0):
        x = np.arange(int(0.22 * SR)) / SR
        self.t.add(np.sin(2 * np.pi * fr * x) * np.exp(-x * 16) * 0.11, at, g, 0.5)

    def alert(self, at, g=1.0):
        x = np.arange(int(0.5 * SR)) / SR
        y = (np.sin(2 * np.pi * 660 * x) * (x < 0.2) + np.sin(2 * np.pi * 440 * x) * (x >= 0.25)) * np.exp(-(x % 0.25) * 8) * 0.11
        self.t.add(y, at, g, 0.5)

    def typing(self, at, d, g=1.0):
        t = at
        while t < at + d:
            x = np.arange(int(0.03 * SR)) / SR
            y = bp(self.noise(0.03), 2000, 6000) * np.exp(-x * 160) * 0.12
            self.t.add(y, t, g * self.rng.uniform(0.6, 1.0), 0.4 + self.rng.random() * 0.2)
            t += self.rng.uniform(0.045, 0.11)

    def roll(self, at, d, g=1.0):
        t = at
        k = 0
        while t < at + d:
            self.blip(t, 900 + k * 25, g * 0.35)
            t += 0.05 + 0.0025 * k
            k += 1

    def clicks(self, at, d, n=9, g=1.0):
        for i in range(n):
            self.tick(at + i * d / n, g * 0.8)

    def transition(self, kind, at):
        if kind in ("whip", "push"):
            self.whoosh(at, 0.6 if kind == "whip" else 0.75)
        elif kind == "zoom":
            self.whoosh(at, 0.7, rise=True)
            self.impact(at, 0.55)
        elif kind == "glitch":
            self.glitch(at)
        elif kind == "iris":
            self.shimmer(at - 0.2)
            self.impact(at, 0.35)
        elif kind in ("wipe", "split"):
            self.whoosh(at, 0.65)
            self.tick(at + 0.05, 0.8)
        elif kind == "shutter":
            self.clicks(at - 0.35, 0.7)
            self.whoosh(at, 0.5, g=0.6)
        elif kind == "cube":
            self.whoosh(at, 0.8)
            self.impact(at + 0.05, 0.3)
        elif kind == "flash":
            self.shimmer(at - 0.25, 1.1)
            self.whoosh(at, 0.6, g=0.5)


def master(narr24k, dur, module, sections, boundaries, events, seed):
    n = int(dur * SR)
    nar = resample_poly(narr24k, 2, 1).astype(np.float32)
    nar = np.pad(nar, (0, max(0, n - len(nar))))[:n]
    mus = music(dur, module, sections, seed)[:n]
    if len(mus) < n:
        mus = np.pad(mus, ((0, n - len(mus)), (0, 0)))
    env = lp(np.abs(nar), 4) / 0.11
    duck = 1 - 0.66 * np.clip(env, 0, 1)
    tt = np.arange(n) / SR
    base = np.full(n, 0.5, np.float32)
    for a, b, nm in sections:
        if nm in ("title", "end"):
            base[int(a * SR) : int(b * SR)] = 1.0
        elif nm == "hook":
            base[int(a * SR) : int(b * SR)] = 0.7
    base = lp(base, 1.2)
    fade = np.minimum(tt / 2.0, 1) * np.minimum((dur - tt) / 2.5, 1)
    mus = mus * (base * duck * fade)[:, None] * 0.9
    sx = Sfx(dur, seed + 11)
    for kind, at in boundaries:
        sx.transition(kind, at)
    for kind, at, arg in events:
        if kind == "tick":
            sx.tick(at)
        elif kind == "blip":
            sx.blip(at)
        elif kind == "alert":
            sx.alert(at)
        elif kind == "type":
            sx.typing(at, arg)
        elif kind == "roll":
            sx.roll(at, arg)
        elif kind == "impact":
            sx.impact(at, arg or 1.0)
        elif kind == "riser":
            sx.riser(at, arg or 1.6)
        elif kind == "shimmer":
            sx.shimmer(at)
        elif kind == "glitch":
            sx.glitch(at)
    sfx = sx.t.st() * 0.85
    mix = np.stack([nar, nar], 1) * 0.95 + mus + sfx
    pk = np.max(np.abs(mix))
    if pk > 0.95:
        mix = mix / pk * 0.95
    return mix.astype(np.float32), mus, sfx
