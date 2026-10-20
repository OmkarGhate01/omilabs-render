// Glossy 3D-look figures (reference style): spheres + shoulder busts with specular highlights and rim light.
import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { CL, sp } from "./theme";

let gid = 0;
// One glossy person bust. (x,y) = head centre, s = scale (1 = head radius 40).
export const Person: React.FC<{ x: number; y: number; s?: number; c: string; up?: boolean; face?: boolean; dim?: number }> = ({ x, y, s = 1, c, up, face, dim = 1 }) => {
  const id = "gp" + gid++;
  const r = 40 * s;
  return (
    <g opacity={dim}>
      <defs>
        <radialGradient id={id + "h"} cx="35%" cy="30%" r="75%"><stop offset="0" stopColor="#fff" /><stop offset="0.35" stopColor={c} stopOpacity="0.95" /><stop offset="1" stopColor="#05070c" /></radialGradient>
        <linearGradient id={id + "b"} x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#fff" stopOpacity="0.85" /><stop offset="0.25" stopColor={c} stopOpacity="0.8" /><stop offset="1" stopColor="#05070c" /></linearGradient>
      </defs>
      {up && (
        <g stroke={`url(#${id}b)`} strokeWidth={14 * s} strokeLinecap="round" fill="none">
          <path d={`M${x - 1.3 * r} ${y + 1.6 * r} L${x - 1.9 * r} ${y - 0.4 * r}`} />
          <path d={`M${x + 1.3 * r} ${y + 1.6 * r} L${x + 1.9 * r} ${y - 0.4 * r}`} />
        </g>
      )}
      <path d={`M${x - 1.7 * r} ${y + 3.1 * r} Q${x - 1.7 * r} ${y + 1.25 * r} ${x} ${y + 1.25 * r} Q${x + 1.7 * r} ${y + 1.25 * r} ${x + 1.7 * r} ${y + 3.1 * r} Z`} fill={`url(#${id}b)`} />
      <circle cx={x} cy={y} r={r} fill={`url(#${id}h)`} />
      <ellipse cx={x - r * 0.3} cy={y - r * 0.42} rx={r * 0.28} ry={r * 0.16} fill="#fff" opacity={0.8} />
      {face && (
        <g fill="#0a0d14">
          <circle cx={x - r * 0.3} cy={y + r * 0.05} r={r * 0.09} />
          <circle cx={x + r * 0.3} cy={y + r * 0.05} r={r * 0.09} />
          <path d={`M${x - r * 0.22} ${y + r * 0.42} Q${x} ${y + r * 0.5} ${x + r * 0.22} ${y + r * 0.42}`} stroke="#0a0d14" strokeWidth={r * 0.06} fill="none" strokeLinecap="round" />
        </g>
      )}
    </g>
  );
};

// A reacting crowd strip (3 rows). Positive mood: arms up and bouncing; negative: sparse, slumped.
export const Crowd: React.FC<{ at: number; c: string; up: boolean; y?: number; w?: number }> = ({ at, c, up, y = 0, w = 1080 }) => {
  const f = useCurrentFrame();
  const s = sp(f, at, 18);
  const rows = [
    { n: 6, yy: 0, sc: 0.62, d: 0.55 },
    { n: 7, yy: 70, sc: 0.75, d: 0.75 },
    { n: 6, yy: 150, sc: 0.9, d: 1 },
  ];
  return (
    <svg width={w} height={420} style={{ position: "absolute", left: 0, top: y, opacity: s }}>
      {rows.map((r, ri) =>
        new Array(r.n).fill(0).map((_, i) => {
          if (!up && (i + ri) % 2) return null;
          const x = 110 + ((w - 220) / (r.n - 1)) * i + (ri % 2 ? 35 : 0);
          const bob = up ? Math.abs(Math.sin((f + i * 7 + ri * 11) * 0.18)) * 14 : 0;
          return <Person key={ri + "-" + i} x={x} y={60 + r.yy - bob + (1 - s) * 40} s={r.sc} c={c} up={up} dim={r.d} />;
        }),
      )}
    </svg>
  );
};

// Glass chart panel: ticker number + self-drawing line with glowing head (reference "prices climb / drop").
export const ChartPanel: React.FC<{ at: number; c: string; down: boolean; num: string; label?: string; w?: number; h?: number }> = ({ at, c, down, num, label, w = 760, h = 520 }) => {
  const f = useCurrentFrame();
  const p = interpolate(f, [at + 4, at + 46], [0, 1], CL);
  const pts = new Array(41).fill(0).map((_, i) => {
    const t = i / 40;
    const base = down ? 0.25 + 0.6 * Math.pow(t, 1.6) : 0.85 - 0.62 * (1 / (1 + Math.exp(-(t - 0.55) * 9)));
    return [40 + t * (w - 80), 150 + base * (h - 210) + Math.sin(t * 19) * 6] as [number, number];
  });
  const n = Math.max(2, Math.round(p * 40) + 1);
  const shown = pts.slice(0, n);
  const [hx, hy] = shown[shown.length - 1];
  const d = shown.map((q, i) => (i ? "L" : "M") + q[0].toFixed(1) + " " + q[1].toFixed(1)).join(" ");
  return (
    <div style={{ position: "relative", width: w, height: h, borderRadius: 40, overflow: "hidden",
      background: `linear-gradient(180deg, ${c}38 0%, rgba(255,255,255,0.04) 40%, rgba(255,255,255,0.02) 100%)`,
      border: "1.5px solid rgba(255,255,255,0.16)", boxShadow: `0 40px 90px rgba(0,0,0,0.7), 0 0 80px ${c}30, inset 0 1px 0 rgba(255,255,255,0.25)` }}>
      <div style={{ position: "absolute", left: 40, top: 34, fontFamily: "Inter, sans-serif", fontWeight: 700, fontSize: 84, color: "#fff", textShadow: `0 0 30px ${c}` }}>{num}</div>
      {label && <div style={{ position: "absolute", left: 44, top: 132, fontFamily: "Inter, sans-serif", fontWeight: 500, fontSize: 30, color: "#b9c4d6" }}>{label}</div>}
      <svg width={w} height={h} style={{ position: "absolute", left: 0, top: 0 }}>
        <defs><linearGradient id="cpf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor={c} stopOpacity="0.45" /><stop offset="1" stopColor={c} stopOpacity="0" /></linearGradient></defs>
        <path d={`${d} L${hx} ${h} L40 ${h} Z`} fill="url(#cpf)" />
        <path d={d} stroke={c} strokeWidth={6} fill="none" strokeLinejoin="round" style={{ filter: `drop-shadow(0 0 12px ${c})` }} />
        <circle cx={hx} cy={hy} r={26} fill={c} opacity={0.35} />
        <circle cx={hx} cy={hy} r={11} fill="#fff" />
        <path d={`M${hx - 44} ${hy}L${hx} ${hy - 4}L${hx + 44} ${hy}L${hx} ${hy + 4}Z M${hx} ${hy - 30}L${hx + 4} ${hy}L${hx} ${hy + 30}L${hx - 4} ${hy}Z`} fill="#fff" />
      </svg>
    </div>
  );
};
