import "@fontsource/unbounded/700.css";
import "@fontsource/unbounded/800.css";
import "@fontsource/space-grotesk/500.css";
import "@fontsource/space-grotesk/700.css";
import "@fontsource/inter/400.css";
import "@fontsource/inter/600.css";
import "@fontsource/jetbrains-mono/400.css";
import "@fontsource/jetbrains-mono/700.css";
import "@fontsource/noto-sans-devanagari/400.css";
import "@fontsource/noto-sans-devanagari/600.css";
import "@fontsource/noto-sans-devanagari/700.css";
import React from "react";
import {
  AbsoluteFill,
  Img,
  interpolate,
  interpolateColors,
  random,
  staticFile,
  useCurrentFrame,
} from "remotion";
import { noise2D } from "@remotion/noise";
import { C, CL, EXPO, F, H, W, lerp, sp } from "./theme";

// ================= BACKDROPS =================
const Base: React.FC = () => (
  <AbsoluteFill
    style={{
      background:
        "radial-gradient(ellipse at 50% 38%, #0C1633 0%, #060914 58%, #020308 100%)",
    }}
  />
);

const Glows: React.FC<{ hue?: string }> = ({ hue = "cyan" }) => {
  const f = useCurrentFrame();
  const x1 = 70 + noise2D("g1", f * 0.004, 0) * 14;
  const y1 = 38 + noise2D("g2", f * 0.004, 1) * 12;
  const x2 = 24 + noise2D("g3", f * 0.003, 2) * 14;
  const y2 = 74 + noise2D("g4", f * 0.003, 3) * 10;
  const second =
    hue === "violet"
      ? "rgba(123,97,255,0.22)"
      : hue === "amber"
        ? "rgba(255,181,71,0.13)"
        : "rgba(53,224,255,0.15)";
  // Perf: each glow is painted only inside its visible circle (same maths as the old
  // full-screen radial-gradient, verified PSNR > 100 dB), ~2x less pixel work.
  return (
    <AbsoluteFill>
      <GlowSpot px={x2} py={y2} color={second} stop={0.4} />
      <GlowSpot px={x1} py={y1} color="rgba(45,123,255,0.30)" stop={0.42} />
    </AbsoluteFill>
  );
};

// A "circle at x% y%" gradient sized farthest-corner, fading to transparent at `stop`.
const GlowSpot: React.FC<{ px: number; py: number; color: string; stop: number }> = ({ px, py, color, stop }) => {
  const cx = (px / 100) * W;
  const cy = (py / 100) * H;
  const far = Math.max(Math.hypot(cx, cy), Math.hypot(W - cx, cy), Math.hypot(cx, H - cy), Math.hypot(W - cx, H - cy));
  const R = far * stop;
  const x0 = Math.max(0, Math.floor(cx - R));
  const y0 = Math.max(0, Math.floor(cy - R));
  const x1 = Math.min(W, Math.ceil(cx + R));
  const y1 = Math.min(H, Math.ceil(cy + R));
  return (
    <div
      style={{
        position: "absolute",
        left: x0,
        top: y0,
        width: x1 - x0,
        height: y1 - y0,
        background: `radial-gradient(circle ${R}px at ${cx - x0}px ${cy - y0}px, ${color}, transparent ${R}px)`,
      }}
    />
  );
};

export const Plexus: React.FC<{
  n?: number;
  seed?: string;
  opacity?: number;
}> = ({ n = 26, seed = "px", opacity = 1 }) => {
  const f = useCurrentFrame();
  const span = W + 240;
  const pts = new Array(n).fill(0).map((_, i) => {
    const z = 0.3 + random(seed + "z" + i) * 0.7;
    const bx = random(seed + "x" + i) * span;
    const by = random(seed + "y" + i) * H;
    const x =
      bx + noise2D(seed + "a" + i, f * 0.0035, 0) * 150 * z + f * 0.35 * z;
    const y = by + noise2D(seed + "b" + i, 0, f * 0.0035) * 110 * z;
    return { x: (((x % span) + span) % span) - 120, y, z };
  });
  const lines: React.ReactNode[] = [];
  for (let i = 0; i < n; i++) {
    for (let j = i + 1; j < n; j++) {
      const dx = pts[i].x - pts[j].x;
      const dy = pts[i].y - pts[j].y;
      const d = Math.sqrt(dx * dx + dy * dy);
      if (d < 250) {
        lines.push(
          <line
            key={i + "-" + j}
            x1={pts[i].x}
            y1={pts[i].y}
            x2={pts[j].x}
            y2={pts[j].y}
            stroke={C.cyan}
            strokeOpacity={(1 - d / 250) * 0.24 * Math.min(pts[i].z, pts[j].z)}
            strokeWidth={1.1}
          />,
        );
      }
    }
  }
  return (
    <svg
      width={W}
      height={H}
      style={{ position: "absolute", left: 0, top: 0, opacity }}
    >
      {lines}
      {pts.map((p, i) => (
        <circle
          key={i}
          cx={p.x}
          cy={p.y}
          r={1.4 + p.z * 2.6}
          fill={i % 5 === 0 ? C.cyan : C.text}
          fillOpacity={0.18 + 0.5 * p.z}
        />
      ))}
    </svg>
  );
};

const Floor: React.FC = () => {
  const f = useCurrentFrame();
  const hz = 640;
  const vx = W / 2;
  const rows = 15;
  const phase = (f * 0.011) % 1;
  const hl: React.ReactNode[] = [];
  for (let k = 0; k < rows; k++) {
    const t = (k + phase) / rows;
    const y = hz + (H - hz) * Math.pow(t, 2.3);
    hl.push(
      <line
        key={"h" + k}
        x1={0}
        y1={y}
        x2={W}
        y2={y}
        stroke={C.blue}
        strokeOpacity={0.05 + 0.4 * t}
        strokeWidth={0.8 + t * 1.8}
      />,
    );
  }
  const vl: React.ReactNode[] = [];
  for (let k = -18; k <= 18; k++) {
    vl.push(
      <line
        key={"v" + k}
        x1={vx + k * 12}
        y1={hz}
        x2={vx + k * 200}
        y2={H + 40}
        stroke={C.blue}
        strokeOpacity={0.24}
        strokeWidth={1.1}
      />,
    );
  }
  return (
    <AbsoluteFill>
      <AbsoluteFill
        style={{
          WebkitMaskImage: `linear-gradient(180deg, transparent ${hz}px, black ${hz + 260}px)`,
          maskImage: `linear-gradient(180deg, transparent ${hz}px, black ${hz + 260}px)`,
        }}
      >
        <svg width={W} height={H}>
          {vl}
          {hl}
        </svg>
      </AbsoluteFill>
      <AbsoluteFill
        style={{
          background: `linear-gradient(180deg, transparent ${hz - 70}px, rgba(45,123,255,0.22) ${hz}px, transparent ${hz + 50}px)`,
        }}
      />
    </AbsoluteFill>
  );
};

// Perf: the grid is drawn as 1px SVG rects instead of repeating CSS gradients
// (same pixels, verified SSIM 0.9999 / PSNR ~70 dB), ~16% faster per frame.
const GridLayer: React.FC<{ step: number; ox: number; oy: number; opacity: number }> = ({ step, ox, oy, opacity }) => {
  const x0 = ox % step;
  const y0 = oy % step;
  const rects: React.ReactNode[] = [];
  for (let x = x0 - step; x < W; x += step) rects.push(<rect key={"x" + x} x={x} y={0} width={1} height={H} />);
  for (let y = y0 - step; y < H; y += step) rects.push(<rect key={"y" + y} x={0} y={y} width={W} height={1} />);
  return (
    <svg width={W} height={H} style={{ position: "absolute", left: 0, top: 0, opacity }}>
      <g fill={C.line}>{rects}</g>
    </svg>
  );
};

const Grid: React.FC = () => {
  const f = useCurrentFrame();
  const d1 = (f * 0.3) % 120;
  const d2 = (f * 0.12) % 40;
  return (
    <>
      <GridLayer step={120} ox={d1} oy={d1 * 0.5} opacity={0.32} />
      <GridLayer step={40} ox={d2} oy={d2} opacity={0.1} />
    </>
  );
};

const Dots: React.FC = () => {
  const f = useCurrentFrame();
  const mx = 50 + noise2D("dm", f * 0.004, 0) * 30;
  const my = 50 + noise2D("dn", 0, f * 0.004) * 25;
  return (
    <AbsoluteFill
      style={{
        backgroundImage:
          "radial-gradient(circle, rgba(138,155,189,0.35) 1.6px, transparent 2.2px)",
        backgroundSize: "34px 34px",
        WebkitMaskImage: `radial-gradient(circle at ${mx}% ${my}%, black 0%, transparent 55%)`,
        maskImage: `radial-gradient(circle at ${mx}% ${my}%, black 0%, transparent 55%)`,
        opacity: 0.6,
      }}
    />
  );
};

const Rings: React.FC<{ cx?: number; cy?: number }> = ({
  cx = 1460,
  cy = 560,
}) => {
  const f = useCurrentFrame();
  const rs = [110, 190, 285, 400, 540, 700];
  return (
    <svg width={W} height={H} style={{ position: "absolute", left: 0, top: 0 }}>
      {rs.map((r, i) => (
        <circle
          key={i}
          cx={cx}
          cy={cy}
          r={r}
          fill="none"
          stroke={i % 2 ? C.cyan : C.blue}
          strokeOpacity={0.09 + 0.05 * (i % 2)}
          strokeWidth={i === 2 ? 2.2 : 1.2}
          strokeDasharray={i % 2 ? "3 14" : "70 22 8 22"}
          transform={`rotate(${(i % 2 ? -1 : 1) * f * (0.12 + 0.05 * i)} ${cx} ${cy})`}
        />
      ))}
      {new Array(60).fill(0).map((_, k) => {
        const a = (k / 60) * Math.PI * 2 + f * 0.002;
        const r1 = 330;
        const r2 = k % 5 === 0 ? 352 : 342;
        return (
          <line
            key={"t" + k}
            x1={cx + Math.cos(a) * r1}
            y1={cy + Math.sin(a) * r1}
            x2={cx + Math.cos(a) * r2}
            y2={cy + Math.sin(a) * r2}
            stroke={C.cyan}
            strokeOpacity={0.18}
            strokeWidth={1.2}
          />
        );
      })}
    </svg>
  );
};

export const Backdrop: React.FC<{ variant?: string; hue?: string }> = ({
  variant = "grid",
  hue,
}) => (
  <AbsoluteFill>
    <Base />
    {variant === "floor" && <Floor />}
    {variant === "grid" && <Grid />}
    {variant === "dots" && <Dots />}
    {variant === "rings" && <Rings />}
    <Glows hue={hue} />
    <Plexus seed={"px" + variant} n={variant === "dots" ? 14 : 24} />
  </AbsoluteFill>
);

export const Grain: React.FC<{ opacity?: number }> = ({ opacity = 0.07 }) => {
  const f = useCurrentFrame();
  const k = Math.floor(f / 2);
  const ox = Math.floor(random("gx" + k) * 180);
  const oy = Math.floor(random("gy" + k) * 100);
  const fx = random("gf" + k) > 0.5 ? -1 : 1;
  const fy = random("gg" + k) > 0.5 ? -1 : 1;
  return (
    <AbsoluteFill
      style={{
        opacity,
        mixBlendMode: "overlay",
        pointerEvents: "none",
        overflow: "hidden",
      }}
    >
      <Img
        src={staticFile("grain.png")}
        style={{
          position: "absolute",
          left: -ox,
          top: -oy,
          width: W + 200,
          height: H + 120,
          transform: `scale(${fx}, ${fy})`,
        }}
      />
    </AbsoluteFill>
  );
};

export const Vignette: React.FC = () => (
  <AbsoluteFill
    style={{
      background:
        "radial-gradient(ellipse at 50% 50%, transparent 56%, rgba(0,0,0,0.5) 100%)",
      pointerEvents: "none",
    }}
  />
);

export const LightLeak: React.FC<{ strength?: number }> = ({
  strength = 1,
}) => {
  const f = useCurrentFrame();
  const x = 20 + ((f * 0.6) % 80);
  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(ellipse 60% 45% at ${x}% 20%, rgba(255,181,71,${0.16 * strength}), transparent 70%), radial-gradient(ellipse 50% 40% at ${100 - x}% 85%, rgba(53,224,255,${0.14 * strength}), transparent 70%)`,
        mixBlendMode: "screen",
        pointerEvents: "none",
      }}
    />
  );
};

// ================= TYPOGRAPHY =================
type TP = {
  text: string;
  at: number;
  size: number;
  color?: string;
  accent?: string[];
  font?: string;
  weight?: number;
  align?: "left" | "center";
  lh?: number;
  ls?: number;
};

const clean = (w: string) => w.replace(/[^A-Za-z0-9-]/g, "");
const isAccent = (w: string, accent: string[]) =>
  accent.length > 0 && accent.map(clean).indexOf(clean(w)) >= 0;

const flexText = (p: TP, gap = 0.26): React.CSSProperties => ({
  display: "flex",
  flexWrap: "wrap",
  justifyContent: p.align === "center" ? "center" : "flex-start",
  columnGap: p.size * gap,
  fontFamily: p.font || F.head,
  fontWeight: p.weight || 700,
  fontSize: p.size,
  lineHeight: p.lh || 1.08,
  letterSpacing: p.ls || 0,
});

// Widow control: the last two words always share a line, so a wrapped headline never
// ends on a single orphan word. Single-line text lays out exactly as before.
const keepLast2 = (items: React.ReactNode[], gapPx: number): React.ReactNode[] =>
  items.length < 3
    ? items
    : [
        ...items.slice(0, -2),
        <span key="last2" style={{ display: "inline-flex", columnGap: gapPx }}>
          {items.slice(-2)}
        </span>,
      ];

export const Plain: React.FC<TP> = (p) => (
  <div style={flexText(p)}>
    {keepLast2(
      p.text.split(" ").map((w, i) => (
        <span
          key={i}
          style={{
            color: isAccent(w, p.accent || []) ? C.cyan : p.color || C.text,
          }}
        >
          {w}
        </span>
      )),
      p.size * 0.26,
    )}
  </div>
);

export const WordsFx: React.FC<TP> = (p) => {
  const f = useCurrentFrame();
  const accent = p.accent || [];
  return (
    <div style={flexText(p)}>
      {keepLast2(p.text.split(" ").map((w, i) => {
        const at = p.at + i * 2.4;
        const s = sp(f, at, 18);
        const acc = isAccent(w, accent);
        const u = lerp(f, at + 10, at + 24, 0, 1, EXPO);
        return (
          <span
            key={i}
            style={{
              overflow: "hidden",
              display: "inline-block",
              paddingBottom: p.size * 0.1,
              position: "relative",
            }}
          >
            <span
              style={{
                display: "inline-block",
                color: acc ? C.cyan : p.color || C.text,
                transform: `translateY(${(1 - s) * p.size * 1.2}px) rotate(${(1 - s) * 7}deg)`,
              }}
            >
              {w}
            </span>
            {acc && (
              <span
                style={{
                  position: "absolute",
                  left: 0,
                  bottom: p.size * 0.03,
                  height: Math.max(4, p.size * 0.06),
                  width: "100%",
                  background: `linear-gradient(90deg, ${C.cyan}, ${C.blue})`,
                  transform: `scaleX(${u})`,
                  transformOrigin: "left",
                  borderRadius: 4,
                }}
              />
            )}
          </span>
        );
      }), p.size * 0.26)}
    </div>
  );
};

export const SplitFx: React.FC<TP> = (p) => {
  const f = useCurrentFrame();
  const accent = p.accent || [];
  let ci = 0;
  return (
    <div
      style={{
        ...flexText(
          { ...p, font: p.font || F.hero, weight: p.weight || 800 },
          0.3,
        ),
        perspective: 900,
      }}
    >
      {keepLast2(p.text.split(" ").map((w, wi) => {
        const acc = isAccent(w, accent);
        return (
          <span
            key={wi}
            style={{ display: "inline-flex", whiteSpace: "nowrap" }}
          >
            {w.split("").map((ch, k) => {
              const idx = ci++;
              const s = sp(f, p.at + idx * 1.05, 13);
              return (
                <span
                  key={k}
                  style={{
                    display: "inline-block",
                    color: acc ? C.cyan : p.color || C.text,
                    opacity: Math.min(1, s * 1.6),
                    transform: `translateY(${(1 - s) * p.size * 0.55}px) rotateX(${(1 - s) * -100}deg)`,
                    transformOrigin: "50% 100%",
                    textShadow: acc
                      ? `0 0 ${p.size * 0.45}px rgba(53,224,255,0.35)`
                      : "none",
                  }}
                >
                  {ch}
                </span>
              );
            })}
          </span>
        );
      }), p.size * 0.3)}
    </div>
  );
};

const GLYPHS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789<>/#%&*+=";
export const ScrambleFx: React.FC<TP & { speed?: number }> = (p) => {
  const f = useCurrentFrame();
  const accent = p.accent || [];
  const speed = p.speed || 0.9;
  let ci = 0;
  return (
    <div style={flexText(p)}>
      {keepLast2(p.text.split(" ").map((w, wi) => {
        const acc = isAccent(w, accent);
        return (
          <span key={wi} style={{ whiteSpace: "nowrap" }}>
            {w.split("").map((ch, k) => {
              const idx = ci++;
              const show = p.at + idx * 0.45;
              const done = p.at + 7 + idx * speed;
              if (f < show) {
                return (
                  <span key={k} style={{ opacity: 0 }}>
                    {ch}
                  </span>
                );
              }
              const scr = f < done;
              const g = scr
                ? GLYPHS[
                    Math.floor(
                      random("s" + idx + "-" + Math.floor(f / 2)) *
                        GLYPHS.length,
                    )
                  ]
                : ch;
              return (
                <span
                  key={k}
                  style={{
                    color: scr || acc ? C.cyan : p.color || C.text,
                    opacity: scr ? 0.7 : 1,
                  }}
                >
                  {g}
                </span>
              );
            })}
          </span>
        );
      }), p.size * 0.26)}
    </div>
  );
};

export const GlitchFx: React.FC<TP> = (p) => {
  const f = useCurrentFrame();
  const t = f - p.at;
  if (t < 0)
    return (
      <div style={{ opacity: 0 }}>
        <Plain {...p} />
      </div>
    );
  const active = t < 16;
  const micro = t > 40 && f % 113 < 3;
  const k = Math.floor(f / 2);
  const amp = active ? 1 - t / 16 : micro ? 0.35 : 0;
  const dx = (random("gx" + k) - 0.5) * 34 * amp;
  const dy = (random("gy" + k) - 0.5) * 8 * amp;
  const cut = random("gc" + k) * 70;
  const cutH = 8 + random("gh" + k) * 22;
  const flicker = active && t < 8 && t % 3 === 1 ? 0.25 : 1;
  return (
    <div style={{ position: "relative", opacity: flicker }}>
      {amp > 0 && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            transform: `translate(${dx}px, ${dy}px)`,
            opacity: 0.85,
          }}
        >
          <Plain {...p} color={C.cyan} accent={[]} />
        </div>
      )}
      {amp > 0 && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            transform: `translate(${-dx}px, ${-dy}px)`,
            opacity: 0.75,
          }}
        >
          <Plain {...p} color={C.red} accent={[]} />
        </div>
      )}
      <div style={{ position: "relative" }}>
        <Plain {...p} />
      </div>
      {amp > 0 && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            transform: `translateX(${dx * 2.2}px)`,
            clipPath: `inset(${cut}% 0 ${Math.max(0, 100 - cut - cutH)}% 0)`,
          }}
        >
          <Plain {...p} color={C.text} />
        </div>
      )}
    </div>
  );
};

export const ExtrudeFx: React.FC<TP & { depth?: number }> = (p) => {
  const f = useCurrentFrame();
  const s = sp(f, p.at, 16);
  const depth = p.depth || 12;
  const rx = interpolate(s, [0, 1], [42, 9]);
  const ry = interpolate(f - p.at, [0, 360], [-16, 8], CL);
  const shadow =
    new Array(depth)
      .fill(0)
      .map(
        (_, i) =>
          `0 ${i + 1}px 0 ${interpolateColors(i / depth, [0, 1], ["#2E5BD1", "#0A1430"])}`,
      )
      .join(", ") + `, 0 ${depth + 10}px ${p.size * 0.35}px rgba(0,0,0,0.65)`;
  const sweep = lerp(f, p.at + 8, p.at + 50, -30, 140);
  const st: React.CSSProperties = {
    fontFamily: p.font || F.hero,
    fontWeight: p.weight || 800,
    fontSize: p.size,
    lineHeight: p.lh || 1.06,
    textAlign: p.align || "left",
    textWrap: "balance", // no orphan word when a hero line wraps
  };
  return (
    <div style={{ perspective: 1400, opacity: Math.min(1, s * 1.5) }}>
      <div
        style={{
          position: "relative",
          transform: `rotateX(${rx}deg) rotateY(${ry}deg) translateY(${(1 - s) * 90}px)`,
        }}
      >
        <div style={{ ...st, color: "#3B6CF0", textShadow: shadow }}>
          {p.text}
        </div>
        <div
          style={{
            ...st,
            position: "absolute",
            inset: 0,
            backgroundImage: `linear-gradient(100deg, ${C.text} ${sweep - 14}%, #FFFFFF ${sweep}%, ${C.cyan} ${sweep + 6}%, ${C.text} ${sweep + 20}%)`,
            WebkitBackgroundClip: "text",
            backgroundClip: "text",
            color: "transparent",
          }}
        >
          {p.text}
        </div>
      </div>
    </div>
  );
};

export const OutlineFx: React.FC<TP> = (p) => {
  const f = useCurrentFrame();
  const o = lerp(f, p.at, p.at + 10);
  const fill = lerp(f, p.at + 10, p.at + 42, 0, 100, EXPO);
  const st: React.CSSProperties = {
    fontFamily: p.font || F.hero,
    fontWeight: p.weight || 800,
    fontSize: p.size,
    lineHeight: p.lh || 1.06,
    textAlign: p.align || "left",
    textWrap: "balance", // no orphan word when a hero line wraps
  };
  return (
    <div
      style={{
        position: "relative",
        opacity: o,
        transform: `translateY(${(1 - o) * 30}px)`,
      }}
    >
      <div
        style={{
          ...st,
          color: "transparent",
          WebkitTextStroke: `2px ${C.cyan}`,
        }}
      >
        {p.text}
      </div>
      <div
        style={{
          ...st,
          position: "absolute",
          inset: 0,
          color: C.text,
          clipPath: `inset(0 ${100 - fill}% 0 0)`,
        }}
      >
        {p.text}
      </div>
    </div>
  );
};

export const Headline: React.FC<TP & { fx?: string }> = ({
  fx = "words",
  ...p
}) => {
  if (fx === "split") return <SplitFx {...p} />;
  if (fx === "scramble") return <ScrambleFx {...p} />;
  if (fx === "glitch") return <GlitchFx {...p} />;
  if (fx === "extrude") return <ExtrudeFx {...p} />;
  if (fx === "outline") return <OutlineFx {...p} />;
  return <WordsFx {...p} />;
};

export const Kicker: React.FC<{
  text: string;
  at: number;
  index?: string;
  color?: string;
  align?: "left" | "center";
}> = ({ text, at, index, color = C.cyan, align = "left" }) => {
  const f = useCurrentFrame();
  const bar = lerp(f, at, at + 14, 0, 1, EXPO);
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        gap: 16,
        justifyContent: align === "center" ? "center" : "flex-start",
      }}
    >
      {index && (
        <span
          style={{
            fontFamily: F.mono,
            fontWeight: 700,
            fontSize: 24,
            color: C.bg,
            background: color,
            padding: "3px 10px",
            borderRadius: 6,
            opacity: bar,
          }}
        >
          {index}
        </span>
      )}
      <div
        style={{
          width: 64 * bar,
          height: 3,
          background: color,
          borderRadius: 2,
        }}
      />
      <ScrambleFx
        text={text.toUpperCase()}
        at={at + 4}
        size={25}
        font={F.mono}
        weight={700}
        color={color}
        speed={0.55}
        ls={2}
      />
    </div>
  );
};

// ================= UI PRIMITIVES =================
export const Pop: React.FC<{
  at: number;
  dy?: number;
  dx?: number;
  flip?: boolean;
  style?: React.CSSProperties;
  children: React.ReactNode;
}> = ({ at, dy = 40, dx = 0, flip = false, style, children }) => {
  const f = useCurrentFrame();
  const s = sp(f, at, 15);
  return (
    <div
      style={{
        opacity: Math.min(1, s * 1.6),
        transform: `perspective(1200px) translate(${(1 - s) * dx}px, ${(1 - s) * dy}px)${flip ? ` rotateX(${(1 - s) * -65}deg)` : ""} scale(${0.92 + 0.08 * s})`,
        transformOrigin: "50% 100%",
        ...style,
      }}
    >
      {children}
    </div>
  );
};

export const Brackets: React.FC<{
  color?: string;
  inset?: number;
  len?: number;
}> = ({ color = C.cyan, inset = 10, len = 22 }) => {
  const b = (
    pos: React.CSSProperties,
    bt: string,
    bl: string,
  ): React.CSSProperties => ({
    position: "absolute",
    width: len,
    height: len,
    borderTop: bt,
    borderLeft: bl,
    ...pos,
  });
  const s = `3px solid ${color}`;
  return (
    <>
      <div style={b({ left: inset, top: inset }, s, s)} />
      <div
        style={{
          ...b({ right: inset, top: inset }, s, "none"),
          borderRight: s,
        }}
      />
      <div
        style={{
          ...b({ left: inset, bottom: inset }, "none", s),
          borderBottom: s,
        }}
      />
      <div
        style={{
          ...b({ right: inset, bottom: inset }, "none", "none"),
          borderRight: s,
          borderBottom: s,
        }}
      />
    </>
  );
};

export const Panel: React.FC<{
  active?: boolean;
  color?: string;
  style?: React.CSSProperties;
  children: React.ReactNode;
}> = ({ active = false, color = C.cyan, style, children }) => {
  const f = useCurrentFrame();
  const pulse = active ? 0.7 + 0.3 * Math.sin(f / 6) : 0;
  const scan = (f * 7) % 700;
  return (
    <div
      style={{
        position: "relative",
        background:
          "linear-gradient(160deg, rgba(20,31,58,0.94), rgba(8,13,27,0.94))",
        border: `2px solid ${active ? color : C.line}`,
        borderRadius: 22,
        padding: "28px 32px",
        boxShadow: active
          ? `0 0 ${56 * pulse}px ${color}55, inset 0 0 28px ${color}12`
          : "0 18px 44px rgba(0,0,0,0.35)",
        overflow: "hidden",
        ...style,
      }}
    >
      {active && (
        <div
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            top: scan - 120,
            height: 120,
            background: `linear-gradient(180deg, transparent, ${color}16, transparent)`,
          }}
        />
      )}
      {active && <Brackets color={color} />}
      <div style={{ position: "relative" }}>{children}</div>
    </div>
  );
};

export const Chip: React.FC<{
  children: React.ReactNode;
  color?: string;
  solid?: boolean;
  size?: number;
  mono?: boolean;
}> = ({ children, color = C.cyan, solid = false, size = 30, mono = false }) => (
  <div
    style={{
      display: "inline-block",
      fontFamily: mono ? F.mono : F.body,
      fontWeight: 600,
      fontSize: size,
      color: solid ? C.bg : C.text,
      background: solid ? color : "rgba(14,22,40,0.92)",
      border: `2px solid ${solid ? color : C.line2}`,
      borderRadius: 999,
      padding: `${size * 0.34}px ${size * 0.78}px`,
      whiteSpace: "nowrap",
    }}
  >
    {children}
  </div>
);

export const OmMark: React.FC<{ size: number; draw?: number }> = ({
  size,
  draw = 1,
}) => {
  const f = useCurrentFrame();
  const r = 42;
  const circ = 2 * Math.PI * r;
  const bars = [0.45, 1, 0.65];
  return (
    <svg width={size} height={size} viewBox="0 0 100 100">
      <defs>
        <linearGradient id="omg" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor={C.cyan} />
          <stop offset="1" stopColor={C.blue} />
        </linearGradient>
      </defs>
      <circle
        cx="50"
        cy="50"
        r={r}
        fill="none"
        stroke="url(#omg)"
        strokeWidth="7"
        strokeLinecap="round"
        strokeDasharray={circ}
        strokeDashoffset={circ * (1 - draw * 0.86)}
        transform="rotate(-60 50 50)"
      />
      {bars.map((b, i) => {
        const h = 34 * b * (1 + 0.18 * Math.sin(f / 5 + i * 1.7)) * draw;
        return (
          <rect
            key={i}
            x={34 + i * 13}
            y={50 - h / 2}
            width="7"
            height={h}
            rx="3.5"
            fill={C.text}
          />
        );
      })}
    </svg>
  );
};
