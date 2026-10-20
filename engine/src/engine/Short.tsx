// Vertical Short (1080x1920, 30fps). Reference look: black canvas, one accent glow,
// glassmorphic cards, a single bold keyword per beat at the top, fast beat changes,
// karaoke captions. All content stays inside the Shorts safe zone
// (x 70..930 clear of the right-side action rail, y 260..1500 clear of the title/description overlay).
import React from "react";
import { AbsoluteFill, interpolate, random, useCurrentFrame } from "remotion";
import { noise2D } from "@remotion/noise";
import { C, CL, EXPO, F, lerp, sp, SERIES, setSeries } from "./theme";
import { Icon } from "./icons";
import { OmMark } from "./fx";
import { Crowd, ChartPanel, Person } from "./glossy";

export const SW = 1080;
export const SH = 1920;
const SAFE_L = 70;
const SAFE_R = 930; // right rail (like/comment/share) starts ~950

type Beat = { k: string; v: string; d: any; start: number; end: number };
type Word = { w: string; start: number; end: number };
export type ShortProps = {
  id: string;
  ep: number;
  accent: string;
  durationInFrames: number;
  beats: Beat[];
  words: Word[];
};

const ACC: Record<string, string> = { cyan: C.cyan, green: C.green, amber: C.amber, violet: C.violet };
const glass: React.CSSProperties = {
  background: "linear-gradient(180deg, rgba(255,255,255,0.16) 0%, rgba(255,255,255,0.05) 18%, rgba(255,255,255,0.02) 100%)",
  border: "1.5px solid rgba(255,255,255,0.14)",
  borderRadius: 34,
  boxShadow: "0 30px 80px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.12)",
};
const fr = (s: number) => Math.round(s * 30);

// ---------------- mood (reference: green wash = good/up, red wash = bad/down) ----------------
const RED = "#FF3B5C", GREEN = "#2EE87A";
const NEG = /\b(wrong|fail|fails|failed|slow|empty|broke|broken|trap|never|stuck|lost|lose|late|spam|kill|kills|mistake|error|bug|drop|dropped|robotic|choppy|bad|worse|misread|missing|blocked)\b/i;
const POS = /\b(fix|fixed|rule|best|fast|faster|works|right|save|instantly|free|zero|smooth|clean|better|win|easy|exactly|always|correct|safe|live|done|answered|booked)\b/i;
const moodOf = (b: Beat, words: Word[], a: string) => {
  if (b.v === "hook") return a;
  if (b.v === "cta") return GREEN;
  const said = words.filter((w) => w.start >= b.start - 0.05 && w.start < b.end).map((w) => w.w).join(" ");
  const n = (said.match(new RegExp(NEG.source, "gi")) || []).length, p = (said.match(new RegExp(POS.source, "gi")) || []).length;
  return n > p ? RED : p > n ? GREEN : a;
};

// ---------------- background ----------------
const Bg: React.FC<{ a: string; beat: number }> = ({ a, beat }) => {
  const f = useCurrentFrame();
  const gx = 50 + noise2D("sx", f * 0.004, beat) * 22;
  const gy = 42 + noise2D("sy", beat, f * 0.004) * 14;
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <AbsoluteFill style={{ background: `radial-gradient(circle at ${gx}% ${gy}%, ${a}33 0%, ${a}10 28%, transparent 58%)` }} />
      {/* top spotlight cone + soft full-frame wash in the mood colour */}
      <AbsoluteFill style={{ background: `radial-gradient(ellipse 70% 38% at 50% 0%, ${a}aa 0%, ${a}44 45%, transparent 100%)` }} />
      <AbsoluteFill style={{ background: `linear-gradient(180deg, ${a}33 0%, transparent 60%)` }} />
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 45%, transparent 45%, rgba(0,0,0,0.85) 100%)" }} />
      <svg width={SW} height={SH} style={{ position: "absolute" }}>
        {new Array(26).fill(0).map((_, i) => {
          const x = random("px" + i) * SW;
          const y = (random("py" + i) * SH - f * (0.4 + random("pv" + i) * 0.9) + SH * 4) % SH;
          return <circle key={i} cx={x} cy={y} r={1 + random("pr" + i) * 2.2} fill={i % 4 ? "#fff" : a} opacity={0.12 + random("po" + i) * 0.25} />;
        })}
      </svg>
    </AbsoluteFill>
  );
};

// ---------------- keyword (top, like the reference) ----------------
export const Keyword: React.FC<{ text: string; at: number; a: string }> = ({ text, at, a }) => {
  const f = useCurrentFrame();
  const s = sp(f, at, 16);
  const size = Math.min(76, Math.floor(1500 / Math.max(6, text.length)));
  return (
    <div style={{ position: "absolute", top: 300, left: SAFE_L, width: SAFE_R - SAFE_L, textAlign: "center",
      fontFamily: F.head, fontWeight: 600, fontSize: size, color: "#fff", letterSpacing: 1,
      opacity: s, transform: `translateY(${(1 - s) * 30}px)`, filter: `blur(${(1 - s) * 8}px)`,
      textShadow: `0 0 34px ${a}66` }}>
      {text}
    </div>
  );
};

// ---------------- live word (reference: the spoken word, small, top centre) ----------------
const LiveWord: React.FC<{ words: Word[] }> = ({ words }) => {
  const f = useCurrentFrame();
  const t = f / 30;
  const i = words.findIndex((w, k) => t >= w.start - 0.04 && t < (words[k + 1] ? words[k + 1].start - 0.04 : w.end + 0.35));
  if (i < 0) return null;
  const w = words[i];
  const s = sp(f, Math.round((w.start - 0.04) * 30), 22);
  return (
    <div style={{ position: "absolute", top: 290, left: SAFE_L, width: SAFE_R - SAFE_L, textAlign: "center", fontFamily: F.body, fontWeight: 500,
      fontSize: 62, color: "#fff", opacity: 0.35 + 0.65 * s, transform: `translateY(${(1 - s) * 10}px)`, textShadow: "0 2px 24px rgba(0,0,0,0.9)" }}>
      {w.w.replace(/[.,!?;:]+$/, "").toLowerCase()}
    </div>
  );
};

// ---------------- sparkle (reference: a star flare travelling along the motion) ----------------
const Sparkle: React.FC<{ at: number; end: number; a: string }> = ({ at, end, a }) => {
  const f = useCurrentFrame();
  const p = interpolate(f, [at + 6, end], [0, 1], CL);
  if (p <= 0 || p >= 1) return null;
  const x = 160 + p * 760, y = 1330 - Math.sin(p * Math.PI) * 90;
  const r = 34 + Math.sin(f * 0.5) * 6;
  return (
    <svg width={SW} height={SH} style={{ position: "absolute", left: 0, top: 0, pointerEvents: "none" }}>
      <defs><radialGradient id="spk"><stop offset="0" stopColor="#fff" /><stop offset="0.35" stopColor={a} stopOpacity="0.7" /><stop offset="1" stopColor={a} stopOpacity="0" /></radialGradient></defs>
      <circle cx={x} cy={y} r={r * 1.6} fill="url(#spk)" opacity={0.55} />
      <path d={`M${x - r} ${y}L${x} ${y - 3}L${x + r} ${y}L${x} ${y + 3}Z M${x} ${y - r * 0.7}L${x + 3} ${y}L${x} ${y + r * 0.7}L${x - 3} ${y}Z`} fill="#fff" />
    </svg>
  );
};

// ---------------- visuals ----------------
const pop = (f: number, at: number) => {
  const s = sp(f, at, 14);
  return { opacity: Math.min(1, s * 1.4), transform: `translateY(${(1 - s) * 60}px) scale(${0.92 + 0.08 * s})` };
};

const Hook: React.FC<{ d: any; at: number; a: string }> = ({ d, at, a }) => {
  const f = useCurrentFrame();
  // re-flow into short lines (<=12 chars) so the hook can be big; hot words keep the accent
  const hotIdx = d.hot ?? d.lines.length - 1;
  const ws: { w: string; hot: boolean }[] = [];
  (d.lines as string[]).forEach((l, i) => l.split(" ").forEach((w) => ws.push({ w, hot: i === hotIdx })));
  const rows: { w: string; hot: boolean }[][] = [];
  ws.forEach((x) => {
    const r = rows[rows.length - 1];
    if (r && r.map((y) => y.w).join(" ").length + 1 + x.w.length <= 12 && r[0].hot === x.hot) r.push(x);
    else rows.push([x]);
  });
  const lines = rows.map((r) => r.map((y) => y.w).join(" "));
  const longest = Math.max(...lines.map((l) => l.length));
  const size = Math.min(150, Math.floor((SAFE_R - SAFE_L) / (Math.max(longest, 1) * 0.8)));
  return (
    <div style={{ width: SAFE_R - SAFE_L, textAlign: "center" }}>
      {lines.map((l, i) => {
        const s = sp(f, at + i * (at < 0 ? 1 : 5), 13); // first beat: every line visible by frame ~4
        const hot = rows[i][0].hot;
        return (
          <div key={i} style={{ fontFamily: F.hero, fontWeight: 800, fontSize: size, lineHeight: 1.08,
            color: hot ? a : "#fff", opacity: s, transform: `translateY(${(1 - s) * 70}px)`,
            textShadow: hot ? `0 0 50px ${a}aa` : "0 10px 40px rgba(0,0,0,0.8)" }}>{l}</div>
        );
      })}
    </div>
  );
};

const Stat: React.FC<{ d: any; at: number; a: string }> = ({ d, at, a }) => {
  const f = useCurrentFrame();
  const down = a === RED;
  const dec = d.dec ?? 0;
  const from = down ? d.value * 1.9 : 0;
  const v = interpolate(f, [at, at + 40], [from, d.value], { ...CL, easing: EXPO });
  const num = (d.text ?? (d.pre || "") + v.toFixed(dec)) + (d.unit || "");
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
      <ChartPanel at={at} c={a} down={down} num={num} label={d.label} h={420} w={720} />
      <div style={{ position: "relative", width: 760, height: 270, marginTop: 0, transform: "scale(0.82)", transformOrigin: "top center" }}>
        <Crowd at={at + 8} c={down ? a : "#c9d2df"} up={!down} w={760} />
      </div>
    </div>
  );
};

const Card: React.FC<{ d: any; at: number; a: string }> = ({ d, at, a }) => {
  const f = useCurrentFrame();
  return (
    <div style={{ ...glass, width: SAFE_R - SAFE_L - 40, padding: "46px 50px", ...pop(f, at) }}>
      <div style={{ display: "flex", alignItems: "center", gap: 22, marginBottom: 30 }}>
        {d.icon && <Icon name={d.icon} size={64} color={a} sw={2.2} />}
        <div style={{ fontFamily: F.head, fontWeight: 700, fontSize: 52, color: "#fff" }}>{d.title}</div>
      </div>
      {(d.rows || []).map((r: [string, string], i: number) => {
        const s = sp(f, at + 10 + i * 7, 15);
        return (
          <div key={i} style={{ display: "flex", justifyContent: "space-between", gap: 24, padding: "22px 0",
            borderTop: "1px solid rgba(255,255,255,0.08)", opacity: s, transform: `translateX(${(1 - s) * 40}px)` }}>
            <span style={{ fontFamily: F.body, fontSize: 38, color: C.muted }}>{r[0]}</span>
            <span style={{ fontFamily: F.mono, fontWeight: 700, fontSize: 38, color: i === (d.hl ?? -1) ? a : "#fff", textAlign: "right" }}>{r[1]}</span>
          </div>
        );
      })}
    </div>
  );
};

const Chat: React.FC<{ d: any; at: number; a: string }> = ({ d, at, a }) => {
  const f = useCurrentFrame();
  return (
    <div style={{ width: SAFE_R - SAFE_L - 20, display: "flex", flexDirection: "column", gap: 34 }}>
      <svg width={SAFE_R - SAFE_L - 20} height={300} style={{ opacity: sp(f, at, 16) }}>
        {["#9B7BFF", "#4DA3FF", "#2EE87A", "#fff", "#FF3B5C"].map((c, i) => {
          const x = 250 + i * 90, y = 50 + Math.sin(f * 0.12 + i) * 10;
          return <g key={i}><circle cx={x} cy={y} r={30} fill={c} opacity={0.18} /><circle cx={x} cy={y} r={13} fill={c} style={{ filter: `drop-shadow(0 0 10px ${c})` }} /></g>;
        })}
        <Person x={(SAFE_R - SAFE_L - 20) / 2} y={150} s={1.5} c={a} face />
      </svg>
      {(d.msgs as [string, string][]).map(([who, t], i) => {
        const me = who === "agent";
        const s = sp(f, at + i * 16, 14);
        return (
          <div key={i} style={{ display: "flex", justifyContent: me ? "flex-start" : "flex-end", gap: 18, alignItems: "flex-end",
            opacity: s, transform: `translateY(${(1 - s) * 40}px)` }}>
            {me && <div style={{ width: 70, height: 70, borderRadius: 35, flexShrink: 0, background: `radial-gradient(circle at 35% 35%, #fff, ${a} 45%, #0b2a3a)`, boxShadow: `0 0 30px ${a}88` }} />}
            <div style={{ ...glass, borderRadius: 30, maxWidth: 640, padding: "28px 34px", fontFamily: F.body, fontSize: 40, lineHeight: 1.3, color: "#fff",
              border: me ? `1.5px solid ${a}88` : glass.border, boxShadow: me ? `0 0 40px ${a}33` : glass.boxShadow }}>{t}</div>
          </div>
        );
      })}
    </div>
  );
};

const Flow: React.FC<{ d: any; at: number; a: string }> = ({ d, at, a }) => {
  const f = useCurrentFrame();
  const nodes: string[] = d.nodes;
  const gap = 210;
  const h = (nodes.length - 1) * gap;
  const head = interpolate(f, [at + 10, at + 10 + 22 * (nodes.length - 1)], [0, h], CL);
  return (
    <div style={{ position: "relative", width: 640, height: h + 130 }}>
      <svg width={640} height={h + 130} style={{ position: "absolute", left: 0, top: 0 }}>
        <line x1={320} y1={65} x2={320} y2={65 + h} stroke="rgba(255,255,255,0.12)" strokeWidth={4} />
        <line x1={320} y1={65} x2={320} y2={65 + head} stroke={a} strokeWidth={5} style={{ filter: `drop-shadow(0 0 10px ${a})` }} />
        <circle cx={320} cy={65 + head} r={13} fill="#fff" style={{ filter: `drop-shadow(0 0 16px ${a})` }} />
      </svg>
      {nodes.map((t, i) => {
        const s = sp(f, at + i * 12, 14);
        const lit = head >= i * gap - 1;
        return (
          <div key={i} style={{ position: "absolute", left: 0, top: i * gap, width: 640, height: 130, display: "flex", alignItems: "center", justifyContent: "center",
            ...glass, background: "linear-gradient(160deg, #182033, #0b111d)", borderRadius: 30, border: lit ? `2px solid ${a}` : glass.border, boxShadow: lit ? `0 0 40px ${a}44` : glass.boxShadow,
            fontFamily: F.head, fontWeight: 700, fontSize: Math.min(50, Math.floor(1100 / Math.max(10, t.length))), color: lit ? "#fff" : C.muted,
            opacity: s, transform: `scale(${0.9 + 0.1 * s})` }}>{t}</div>
        );
      })}
    </div>
  );
};

const Orb: React.FC<{ d: any; at: number; a: string }> = ({ d, at, a }) => {
  const f = useCurrentFrame();
  const s = sp(f, at, 12);
  const pulse = 1 + 0.04 * Math.sin((f - at) / 5);
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 50 }}>
      <div style={{ position: "relative", width: 520, height: 520, transform: `scale(${s * pulse})` }}>
        {[0, 1, 2].map((i) => {
          const t = ((f - at) / 45 + i / 3) % 1;
          return <div key={i} style={{ position: "absolute", inset: 260 - (150 + t * 110), borderRadius: "50%", border: `3px solid ${a}`, opacity: (1 - t) * 0.5 }} />;
        })}
        <div style={{ position: "absolute", inset: 110, borderRadius: "50%",
          background: `conic-gradient(from ${(f - at) * 3}deg, ${a}, #ffffff, ${a}88, #0a1a2a, ${a})`,
          boxShadow: `0 0 120px ${a}aa, inset 0 0 60px rgba(0,0,0,0.5)` }} />
      </div>
      {d.label && <div style={{ ...glass, borderRadius: 999, padding: "18px 44px", fontFamily: F.head, fontWeight: 600, fontSize: 42, color: "#fff", opacity: s }}>{d.label}</div>}
    </div>
  );
};

const Code: React.FC<{ d: any; at: number; a: string }> = ({ d, at, a }) => {
  const f = useCurrentFrame();
  const lines: string[] = d.lines;
  return (
    <div style={{ ...glass, borderRadius: 26, width: SAFE_R - SAFE_L - 20, padding: "30px 36px", ...pop(f, at) }}>
      <div style={{ display: "flex", gap: 12, marginBottom: 24 }}>
        {[C.red, C.amber, C.green].map((c, i) => <div key={i} style={{ width: 18, height: 18, borderRadius: 9, background: c, opacity: 0.8 }} />)}
        {d.file && <div style={{ fontFamily: F.mono, fontSize: 26, color: C.muted, marginLeft: 12 }}>{d.file}</div>}
      </div>
      {lines.map((l, i) => {
        const s = lerp(f, at + 8 + i * 5, at + 16 + i * 5);
        return <div key={i} style={{ fontFamily: F.mono, fontSize: 34, lineHeight: 1.55, color: i === d.hl ? a : "#E6EEFF", opacity: s, whiteSpace: "pre" }}>{l}</div>;
      })}
    </div>
  );
};

const Versus: React.FC<{ d: any; at: number; a: string }> = ({ d, at, a }) => {
  const f = useCurrentFrame();
  const row = (ok: boolean, t: string, i: number) => {
    const s = sp(f, at + i * 14, 14);
    return (
      <div style={{ ...glass, width: SAFE_R - SAFE_L - 40, padding: "38px 44px", display: "flex", alignItems: "center", gap: 30,
        border: `2px solid ${ok ? a : C.red}88`, boxShadow: `0 0 40px ${ok ? a : C.red}22`, opacity: s, transform: `translateX(${(1 - s) * (ok ? 60 : -60)}px)` }}>
        <div style={{ width: 86, height: 86, borderRadius: 43, flexShrink: 0, display: "flex", alignItems: "center", justifyContent: "center",
          background: ok ? a : C.red, color: "#000", fontFamily: F.hero, fontWeight: 800, fontSize: 50 }}>{ok ? "✓" : "✕"}</div>
        <div style={{ fontFamily: F.head, fontWeight: 600, fontSize: 44, lineHeight: 1.25, color: "#fff" }}>{t}</div>
      </div>
    );
  };
  return <div style={{ display: "flex", flexDirection: "column", gap: 40 }}>{row(false, d.bad, 0)}{row(true, d.good, 1)}</div>;
};

const List: React.FC<{ d: any; at: number; a: string }> = ({ d, at, a }) => {
  const f = useCurrentFrame();
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 30, width: SAFE_R - SAFE_L - 40 }}>
      {(d.items as string[]).map((t, i) => {
        const s = sp(f, at + i * 12, 14);
        return (
          <div key={i} style={{ ...glass, padding: "32px 40px", display: "flex", alignItems: "center", gap: 28, opacity: s, transform: `translateY(${(1 - s) * 40}px)` }}>
            <div style={{ fontFamily: F.hero, fontWeight: 800, fontSize: 46, color: a, width: 60 }}>{i + 1}</div>
            <div style={{ fontFamily: F.head, fontWeight: 600, fontSize: 44, color: "#fff", lineHeight: 1.2 }}>{t}</div>
          </div>
        );
      })}
    </div>
  );
};

const Cta: React.FC<{ d: any; at: number; a: string; ep: number }> = ({ d, at, a, ep }) => {
  const f = useCurrentFrame();
  const s = sp(f, at, 13);
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 40, opacity: s, transform: `scale(${0.9 + 0.1 * s})` }}>
      <div style={{ width: 170, height: 170, borderRadius: 40, display: "flex", alignItems: "center", justifyContent: "center", ...glass, border: `2px solid ${a}`, boxShadow: `0 0 60px ${a}55` }}>
        <svg width={86} height={100} viewBox="0 0 24 28"><path d="M3 2h18v24l-9-6-9 6z" fill="none" stroke={a} strokeWidth={2.2} strokeLinejoin="round" /></svg>
      </div>
      <div style={{ fontFamily: F.body, fontWeight: 600, fontSize: 70, color: "#fff", textAlign: "center", lineHeight: 1.1,
        letterSpacing: interpolate(f - at, [0, 24], [26, 3], CL) }}>Save this post</div>
      <div style={{ fontFamily: F.body, fontWeight: 500, fontSize: 44, color: "#cfd8e6", textAlign: "center", letterSpacing: 2,
        clipPath: `inset(0 ${100 - interpolate(f - at, [10, 40], [0, 100], CL)}% 0 0)` }}>your future self will thank you.</div>
      <div style={{ ...glass, borderRadius: 999, padding: "20px 44px", fontFamily: F.head, fontWeight: 600, fontSize: 40, color: "#fff" }}>
        Full lesson: <span style={{ color: a }}>Episode {ep}</span>
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: 16, marginTop: 10 }}>
        <OmMark size={54} />
        <div style={{ fontFamily: F.mono, fontWeight: 700, fontSize: 30, letterSpacing: 4, color: C.muted }}>{SERIES.name.toUpperCase()}</div>
      </div>
    </div>
  );
};

const V: Record<string, React.FC<any>> = { hook: Hook, stat: Stat, card: Card, chat: Chat, flow: Flow, orb: Orb, code: Code, versus: Versus, list: List, cta: Cta };

// ---------------- captions ----------------
export const Captions: React.FC<{ words: Word[]; a: string }> = ({ words, a }) => {
  const f = useCurrentFrame();
  const t = f / 30;
  // chunks of up to 3 words, broken at punctuation
  const chunks: Word[][] = [];
  let cur: Word[] = [];
  words.forEach((w) => {
    cur.push(w);
    if (cur.length === 3 || /[.,!?;:]$/.test(w.w)) { chunks.push(cur); cur = []; }
  });
  if (cur.length) chunks.push(cur);
  const ch = chunks.find((c, i) => t >= c[0].start - 0.05 && t < (chunks[i + 1] ? chunks[i + 1][0].start - 0.05 : c[c.length - 1].end + 0.4));
  if (!ch) return null;
  const s = sp(f, fr(ch[0].start) - 2, 18);
  const chars = ch.reduce((n, w) => n + w.w.length, 0);
  const size = chars > 22 ? 54 : chars > 17 ? 60 : 68; // keeps every chunk to two lines above the overlay
  return (
    <div style={{ position: "absolute", top: 1330, left: SAFE_L, width: SAFE_R - SAFE_L, display: "flex", justifyContent: "center", flexWrap: "wrap", columnGap: 22,
      transform: `scale(${0.9 + 0.1 * s})`, opacity: s }}>
      {ch.map((w, i) => {
        const on = t >= w.start - 0.03;
        return (
          <span key={i} style={{ fontFamily: F.hero, fontWeight: 800, fontSize: size, color: on ? (t < w.end + 0.05 ? a : "#fff") : "rgba(255,255,255,0.45)",
            textShadow: "0 6px 24px rgba(0,0,0,0.95), 0 0 2px #000" }}>{w.w.toUpperCase()}</span>
        );
      })}
    </div>
  );
};

// ---------------- composition ----------------
export const Short: React.FC<ShortProps> = ({ beats, words, accent, ep, series }: any) => {
  setSeries(series);
  const f = useCurrentFrame();
  const a = ACC[accent] || C.cyan;
  const bi = Math.max(0, beats.findIndex((b: any) => f >= fr(b.start) && f < fr(b.end)));
  const b = beats[bi] || beats[beats.length - 1];
  // first beat starts its entrance 8 frames "early" so frame 0 already shows the hook (feed preview)
  const at = bi === 0 ? fr(b.start) - 8 : fr(b.start);
  const Comp = V[b.v] || Hook;
  const m = moodOf(b, words, a);
  const push = 1 + interpolate(f, [at, fr(b.end)], [0, 0.05], CL); // slow camera push-in
  // quick in/out: zoom-blur on every beat change (reference cuts every 2-4 s)
  const inT = bi === 0 ? 0 : interpolate(f, [at, at + 8], [1, 0], CL);
  const outT = interpolate(f, [fr(b.end) - 6, fr(b.end)], [0, 1], CL);
  const blur = (inT + outT) * 14;
  const scale = 1 + inT * 0.08 - outT * 0.06;
  const flash = interpolate(f - at, [0, 3, 9], [0.0, bi === 0 ? 0 : 0.18, 0], CL);
  return (
    <AbsoluteFill style={{ background: "#000", overflow: "hidden" }}>
      <Bg a={m} beat={bi} />
      {b.v !== "hook" && b.v !== "cta" && <LiveWord words={words} />}
      <AbsoluteFill style={{ display: "flex", alignItems: "center", justifyContent: "center", paddingTop: b.v === "hook" ? 0 : 250, paddingBottom: 330,
        paddingLeft: SAFE_L, paddingRight: SW - SAFE_R, filter: blur > 0.3 ? `blur(${blur}px)` : undefined, transform: `scale(${scale * push * (["hook", "chat", "code"].includes(b.v) ? 1 : 1.15)})`, opacity: 1 - outT * 0.7 }}>
        <Comp key={"v" + bi} d={b.d} at={at} a={m} ep={ep} />
      </AbsoluteFill>
      {b.v !== "hook" && <div style={{ position: "absolute", left: 140, width: 800, top: 1260, height: 120, borderRadius: "50%",
        background: `radial-gradient(ellipse at 50% 50%, ${m}55 0%, transparent 70%)`, filter: "blur(10px)" }} />}
      {["card", "orb", "flow"].includes(b.v) && <Sparkle key={"s" + bi} at={at} end={fr(b.end)} a={m} />}
      <AbsoluteFill style={{ background: "#fff", opacity: flash, mixBlendMode: "overlay" }} />
      <div style={{ position: "absolute", left: 0, top: 0, height: 8, width: `${(f / Math.max(1, fr(beats[beats.length - 1].end))) * 100}%`, background: m, boxShadow: `0 0 16px ${m}`, opacity: 0.9 }} />
    </AbsoluteFill>
  );
};

export const shortSample: ShortProps = {
  id: "s001", ep: 19, accent: "cyan", durationInFrames: 30 * 12,
  beats: [
    { k: "", v: "hook", d: { lines: ["Your voice agent", "feels slow?"] }, start: 0, end: 2.6 },
    { k: "latency", v: "stat", d: { value: 800, unit: " ms", label: "the pause callers notice", ring: 0.6 }, start: 2.6, end: 5.4 },
    { k: "the pipeline", v: "flow", d: { nodes: ["Transcriber", "LLM", "Voice"] }, start: 5.4, end: 8.6 },
    { k: "", v: "cta", d: { title: "Save this" }, start: 8.6, end: 12 },
  ],
  words: [],
};
