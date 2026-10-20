import { Easing, interpolate, spring } from "remotion";

export const FPS = 30;
export const W = 1920;
export const H = 1080;

export const C = {
  bg: "#04060D",
  bg2: "#0A1123",
  surface: "#0D1528",
  surface2: "#121C34",
  line: "#1D2A48",
  line2: "#2A3A62",
  blue: "#2D7BFF",
  cyan: "#35E0FF",
  violet: "#7B61FF",
  amber: "#FFB547",
  green: "#3DDC97",
  red: "#FF5D73",
  text: "#EAF1FF",
  muted: "#8A9BBD",
  dim: "#5A6B8E",
};

export const F = {
  hero: "'Unbounded', 'Noto Sans Devanagari', sans-serif",
  head: "'Space Grotesk', 'Noto Sans Devanagari', sans-serif",
  body: "'Inter', 'Noto Sans Devanagari', sans-serif",
  mono: "'JetBrains Mono', 'Noto Sans Devanagari', monospace",
};

export const CL = {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
} as const;

// easeOutExpo-like, speed-ramp in/out, soft sine
export const EXPO = Easing.bezier(0.16, 1, 0.3, 1);
export const RAMP = Easing.bezier(0.83, 0, 0.17, 1);
export const SOFT = Easing.bezier(0.45, 0, 0.55, 1);

export const lerp = (
  f: number,
  a: number,
  b: number,
  x = 0,
  y = 1,
  e: (t: number) => number = (t) => t,
) => interpolate(f, [a, b], [x, y], { ...CL, easing: e });

export const sp = (frame: number, at: number, damping = 15, mass = 1) =>
  spring({ frame: frame - at, fps: FPS, config: { damping, mass } });

export const fit = (text: string, base: number, ref: number, min: number) =>
  Math.max(
    min,
    Math.min(base, base * Math.sqrt(ref / Math.max(ref, text.length))),
  );

export const tone = (t?: string) =>
  t === "warn"
    ? C.amber
    : t === "ok"
      ? C.green
      : t === "err"
        ? C.red
        : t === "violet"
          ? C.violet
          : t === "blue"
            ? C.blue
            : t === "muted"
              ? C.muted
              : C.cyan;

export const pad2 = (n: number) => (n < 10 ? "0" + n : "" + n);

// Series branding (set per render from props.series; defaults keep the Bolna course unchanged)
export const SERIES = { name: "Bolna AI Masterclass", tag: "BOLNA AI" };
export const setSeries = (s?: { name?: string; tag?: string }) => { if (s?.name) SERIES.name = s.name; if (s?.tag) SERIES.tag = s.tag; };
