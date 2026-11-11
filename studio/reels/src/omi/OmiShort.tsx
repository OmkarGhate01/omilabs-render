import React from "react";
import {
  AbsoluteFill, Audio, Easing, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig, Sequence,
} from "remotion";
import { loadFont } from "@remotion/google-fonts/Poppins";

const { fontFamily } = loadFont("normal", { weights: ["400", "500", "600", "700", "800"], subsets: ["latin", "devanagari"] });

export type Word = { t: string; s: number; e: number; hl?: boolean; chip?: boolean };
export type Beat = { tag: string; v: string; d: any; start: number; end: number; words: Word[] };
export type OmiProps = { id: string; series: string; accent: string; watermark: string; audio: string; duration: number; beats: Beat[] };

export const omiDefaults: OmiProps = { id: "demo", series: "DEMO", accent: "#F2542D", watermark: "omilabs", audio: "", duration: 3, beats: [] };

const INK = "#161616";
const MUTED = "#8A8A8A";
const BG = "#EEEEEE";
const ease = Easing.out(Easing.cubic);

const useIn = (delay = 0, damping = 200) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig();
  return spring({ frame: f - delay, fps, config: { damping, mass: 0.9 } });
};

// ---------- floating card shell (3D tilt + soft shadow, like the reference) ----------
export const Float: React.FC<{ children: React.ReactNode; delay?: number; w?: number; dark?: boolean; tilt?: number; style?: React.CSSProperties; instant?: boolean }> =
  ({ children, delay = 0, w = 760, dark, tilt = 6, style, instant }) => {
    const f = useCurrentFrame(); const p0 = useIn(delay); const p = instant ? Math.max(p0, 0.75 + 0.25 * p0) : p0;
    const bob = Math.sin((f - delay) / 28) * 6;
    return (
      <div style={{ perspective: 1600 }}>
        <div style={{
          width: w, borderRadius: 34, padding: 40, boxSizing: "border-box",
          background: dark ? "linear-gradient(160deg,#1d1f2b,#0d0e14)" : "#FFFFFF",
          color: dark ? "#fff" : INK,
          boxShadow: "0 40px 80px rgba(0,0,0,.16), 0 8px 20px rgba(0,0,0,.08)",
          transform: `translateY(${(1 - p) * 70 + bob}px) scale(${0.9 + 0.1 * p}) rotateX(${tilt * (1 - p) + 2}deg) rotateY(${-tilt * (1 - p)}deg)`,
          opacity: p, ...style,
        }}>{children}</div>
      </div>
    );
  };

// ---------- icons ----------
export const Icon: React.FC<{ name: string; color: string; size?: number }> = ({ name, color, size = 56 }) => {
  const p: Record<string, React.ReactNode> = {
    mail: <><rect x="3" y="5" width="18" height="14" rx="2" /><path d="M3 7l9 6 9-6" /></>,
    wallet: <><rect x="3" y="6" width="18" height="13" rx="2" /><path d="M16 12h3M3 9h18" /></>,
    check: <path d="M5 12l5 5 9-10" />,
    x: <path d="M6 6l12 12M18 6L6 18" />,
    lock: <><rect x="5" y="11" width="14" height="9" rx="2" /><path d="M8 11V8a4 4 0 018 0v3" /></>,
    users: <><circle cx="9" cy="8" r="3" /><path d="M3 20c0-3 3-5 6-5s6 2 6 5M16 5a3 3 0 010 6M18 15c2 .5 3 2.5 3 5" /></>,
    video: <><rect x="3" y="6" width="13" height="12" rx="2" /><path d="M16 10l5-3v10l-5-3" /></>,
    cpu: <><rect x="6" y="6" width="12" height="12" rx="2" /><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4" /></>,
    gift: <><rect x="3" y="9" width="18" height="12" rx="1" /><path d="M12 9v12M3 13h18M12 9c-2-4-6-4-6-1s6 1 6 1 6 2 6-1-4-3-6 1" /></>,
    star: <path d="M12 3l2.7 5.6 6.3.9-4.5 4.4 1 6.2L12 17l-5.6 3 1-6.2L3 9.5l6.3-.9z" />,
    bookmark: <path d="M6 3h12v18l-6-4-6 4z" />,
    mobile: <><rect x="7" y="2" width="10" height="20" rx="2" /><path d="M11 18h2" /></>,
    globe: <><circle cx="12" cy="12" r="9" /><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18" /></>,
    bolt: <path d="M13 2L4 14h7l-1 8 9-12h-7z" />,
    chat: <path d="M4 5h16v11H9l-5 4z" />,
    chart: <><path d="M4 20V10M10 20V4M16 20v-7M22 20H2" /></>,
    code: <path d="M8 7l-5 5 5 5M16 7l5 5-5 5M14 4l-4 16" />,
    image: <><rect x="3" y="4" width="18" height="16" rx="2" /><circle cx="9" cy="10" r="2" /><path d="M21 17l-5-5-9 8" /></>,
    key: <><circle cx="8" cy="15" r="4" /><path d="M11 12l9-9M17 6l3 3" /></>,
    book: <path d="M4 4h7a3 3 0 013 3v13a2 2 0 00-2-2H4zM20 4h-5a3 3 0 00-3 3" />,
    edit: <path d="M4 20h4L20 8l-4-4L4 16zM14 6l4 4" />,
    warning: <><path d="M12 3l10 18H2z" /><path d="M12 10v5M12 18v.5" /></>,
    clock: <><circle cx="12" cy="12" r="9" /><path d="M12 7v5l3 2" /></>,
    wave: <path d="M2 12h2M6 8v8M10 4v16M14 7v10M18 10v4M22 12h0" />,
  };
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={2.2} strokeLinecap="round" strokeLinejoin="round">
      {p[name] ?? p.star}
    </svg>
  );
};

// ---------- visuals ----------
export const Hook: React.FC<{ d: any; accent: string; first?: boolean }> = ({ d, accent, first }) => {
  const f = useCurrentFrame();
  const num = parseFloat(String(d.stat).replace(/,/g, ""));
  const isNum = /^[\d.]+/.test(String(d.stat)) && !isNaN(num);
  // first beat: the number is already there on frame 0 (no "0" in the thumbnail frame / swipe moment)
  const n = first ? num : interpolate(f, [6, 34], [0, isNum ? num : 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  const unit = isNum ? String(d.stat).replace(/^[\d.,]+\s*/, "") : "";
  return (
    <Float dark w={640} tilt={10} instant={first}>
      {d.problem ? (
        // v3 rule: the problem is readable on frame 0 (no fade-in), 2–6 words
        <div style={{ marginBottom: 26, fontSize: 64, fontWeight: 800, lineHeight: 1.08, color: "#fff" }}>
          {d.problem}<span style={{ color: accent }}>?</span>
        </div>
      ) : null}
      <div style={{ display: "flex", alignItems: "center", gap: 18 }}>
        <div style={{ width: 64, height: 64, borderRadius: 18, background: accent, display: "grid", placeItems: "center", fontWeight: 800, fontSize: 34 }}>M</div>
        <div style={{ fontSize: 54, fontWeight: 700 }}>{d.brand}</div>
      </div>
      <div style={{ marginTop: 22, display: "inline-block", padding: "8px 18px", borderRadius: 999, border: `2px solid ${accent}`, color: accent, fontSize: 24, fontWeight: 700, letterSpacing: 3 }}>{d.pill}</div>
      <div style={{ marginTop: 34, borderRadius: 24, padding: "26px 30px", background: "rgba(255,255,255,.06)", border: "1px solid rgba(255,255,255,.12)" }}>
        <div style={{ fontSize: 22, letterSpacing: 3, opacity: 0.6, fontWeight: 600 }}>{(d.sub || "").toUpperCase()}</div>
        <div style={{ fontSize: 96, fontWeight: 800, lineHeight: 1.05 }}>{isNum ? (num % 1 ? n.toFixed(1) : Math.round(n)) : d.stat}{unit ? <span style={{ fontSize: 48, opacity: 0.7 }}> {unit}</span> : null}</div>
      </div>
    </Float>
  );
};

export const Browser: React.FC<{ d: any; accent: string }> = ({ d, accent }) => {
  const f = useCurrentFrame();
  const cx = interpolate(f, [18, 42], [560, 330], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  const cy = interpolate(f, [18, 42], [430, 300], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  const click = interpolate(f, [44, 50, 58], [1, 0.92, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const ring = interpolate(f, [46, 66], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <Float w={820} style={{ padding: 0, overflow: "hidden", position: "relative" }}>
      <div style={{ display: "flex", alignItems: "center", gap: 12, padding: "22px 26px", background: "#F4F4F4", borderBottom: "1px solid #e4e4e4" }}>
        {["#FF5F57", "#FEBC2E", "#28C840"].map((c) => <div key={c} style={{ width: 18, height: 18, borderRadius: 9, background: c }} />)}
        <div style={{ marginLeft: 18, flex: 1, background: "#fff", borderRadius: 12, padding: "10px 20px", fontSize: 28, color: "#444", fontWeight: 500 }}>🔒 {d.url}</div>
      </div>
      <div style={{ height: 420, position: "relative", display: "grid", placeItems: "center" }}>
        <div style={{ position: "absolute", top: 50, left: 50, fontSize: 40, fontWeight: 800 }}>{d.url}</div>
        <div style={{ position: "absolute", top: 110, left: 50, width: 420, height: 18, borderRadius: 9, background: "#ececec" }} />
        <div style={{ position: "absolute", top: 142, left: 50, width: 300, height: 18, borderRadius: 9, background: "#ececec" }} />
        <div style={{ position: "absolute", top: 250, left: 50, transform: `scale(${click})`, padding: "22px 44px", borderRadius: 18, background: accent, color: "#fff", fontWeight: 700, fontSize: 36, boxShadow: `0 0 0 ${ring * 26}px ${accent}${Math.round((1 - ring) * 90).toString(16).padStart(2, "0")}` }}>{d.button}</div>
        <svg style={{ position: "absolute", left: cx, top: cy }} width="48" height="48" viewBox="0 0 24 24"><path d="M4 2l16 9-7 2-3 7z" fill="#111" stroke="#fff" strokeWidth="1.2" /></svg>
      </div>
    </Float>
  );
};

export const Card: React.FC<{ d: any; accent: string }> = ({ d, accent }) => {
  const f = useCurrentFrame();
  return (
    <Float w={800}>
      <div style={{ display: "flex", alignItems: "center", gap: 22, marginBottom: 26 }}>
        <div style={{ width: 92, height: 92, borderRadius: 26, background: `${accent}18`, display: "grid", placeItems: "center" }}><Icon name={d.icon} color={accent} /></div>
        <div style={{ fontSize: 50, fontWeight: 700 }}>{d.title}</div>
      </div>
      {(d.rows || []).map((r: string[], i: number) => {
        const p = interpolate(f, [14 + i * 9, 26 + i * 9], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
        return (
          <div key={i} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "24px 6px", borderTop: "1px solid #eee", opacity: p, transform: `translateX(${(1 - p) * 40}px)` }}>
            <span style={{ fontSize: 34, color: MUTED, fontWeight: 500 }}>{r[0]}</span>
            <span style={{ fontSize: 38, fontWeight: 700, color: i === (d.hl ?? -1) ? accent : INK }}>{r[1]}</span>
          </div>
        );
      })}
    </Float>
  );
};

export const Versus: React.FC<{ d: any; accent: string }> = ({ d }) => {
  const f = useCurrentFrame();
  const strike = interpolate(f, [26, 40], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  const row = (txt: string, good: boolean, delay: number) => (
    <Float w={820} delay={delay} tilt={4} style={{ padding: "30px 34px" }}>
      <div style={{ display: "flex", alignItems: "center", gap: 24 }}>
        <div style={{ width: 66, height: 66, flex: "none", borderRadius: 33, background: good ? "#1DB954" : "#1a1a1a", display: "grid", placeItems: "center" }}>
          <Icon name={good ? "check" : "x"} color="#fff" size={38} />
        </div>
        <div style={{ position: "relative", fontSize: 36, fontWeight: good ? 700 : 500, color: good ? INK : MUTED, lineHeight: 1.3 }}>
          {txt}
          {!good && <div style={{ position: "absolute", left: 0, top: "52%", height: 4, width: `${strike * 100}%`, background: "#E5484D", borderRadius: 2 }} />}
        </div>
      </div>
    </Float>
  );
  return <div style={{ display: "flex", flexDirection: "column", gap: 34, alignItems: "center" }}>{row(d.bad, false, 0)}{row(d.good, true, 16)}</div>;
};

export const List: React.FC<{ d: any; accent: string }> = ({ d, accent }) => {
  const f = useCurrentFrame();
  return (
    <Float w={800}>
      {(d.items || []).map((it: string, i: number) => {
        const p = interpolate(f, [8 + i * 8, 20 + i * 8], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
        return (
          <div key={i} style={{ display: "flex", alignItems: "center", gap: 24, padding: "20px 4px", borderTop: i ? "1px solid #eee" : "none", opacity: p, transform: `translateX(${(1 - p) * 50}px)` }}>
            <div style={{ width: 54, height: 54, flex: "none", borderRadius: 27, background: accent, color: "#fff", display: "grid", placeItems: "center", fontWeight: 800, fontSize: 28, transform: `scale(${0.6 + 0.4 * p})` }}>{i + 1}</div>
            <div style={{ fontSize: 40, fontWeight: 600 }}>{it}</div>
          </div>
        );
      })}
    </Float>
  );
};

export const Stat: React.FC<{ d: any; accent: string }> = ({ d, accent }) => {
  const f = useCurrentFrame();
  const ring = interpolate(f, [6, 40], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  const R = 190, C = 2 * Math.PI * R;
  const pop = spring({ frame: f - 10, fps: 30, config: { damping: 12, mass: 0.7 } });
  return (
    <Float w={620} style={{ display: "flex", flexDirection: "column", alignItems: "center", padding: 46 }}>
      <div style={{ position: "relative", width: 440, height: 440 }}>
        <svg width={440} height={440} style={{ position: "absolute", inset: 0, transform: "rotate(-90deg)" }}>
          <circle cx={220} cy={220} r={R} stroke="#eee" strokeWidth={22} fill="none" />
          <circle cx={220} cy={220} r={R} stroke={accent} strokeWidth={22} fill="none" strokeLinecap="round" strokeDasharray={C} strokeDashoffset={C * (1 - 0.82 * ring)} />
        </svg>
        <div style={{ position: "absolute", inset: 0, display: "grid", placeItems: "center", fontSize: String(d.value).length > 5 ? 84 : 120, fontWeight: 800, transform: `scale(${0.7 + 0.3 * pop})` }}>{d.value}</div>
      </div>
      <div style={{ marginTop: 24, fontSize: 36, fontWeight: 600, color: "#444", textAlign: "center" }}>{d.label}</div>
    </Float>
  );
};

export const Flow: React.FC<{ d: any; accent: string }> = ({ d, accent }) => {
  const f = useCurrentFrame(); const nodes: string[] = d.nodes || [];
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
      {nodes.map((n, i) => {
        const p = interpolate(f, [6 + i * 12, 18 + i * 12], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
        const line = interpolate(f, [16 + i * 12, 26 + i * 12], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
        const last = i === nodes.length - 1;
        return (
          <React.Fragment key={i}>
            <div style={{ opacity: p, transform: `scale(${0.85 + 0.15 * p})`, padding: "26px 46px", minWidth: 520, textAlign: "center", borderRadius: 26,
              background: last ? accent : "#fff", color: last ? "#fff" : INK, fontSize: 40, fontWeight: 700, boxShadow: "0 24px 50px rgba(0,0,0,.12)" }}>{n}</div>
            {!last && <div style={{ width: 6, height: 54 * line, background: accent, borderRadius: 3, margin: "6px 0", opacity: 0.8 }} />}
            {!last && line < 1 && <div style={{ height: 54 * (1 - line) + 12 }} />}
          </React.Fragment>
        );
      })}
    </div>
  );
};

export const Cta: React.FC<{ d: any; accent: string }> = ({ d, accent }) => {
  const f = useCurrentFrame(); const p = useIn(18, 14);
  const ls = interpolate(f, [0, 22], [24, 2], { extrapolateRight: "clamp", easing: ease });
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 46 }}>
      <Float w={560} tilt={8} style={{ display: "flex", flexDirection: "column", alignItems: "center", padding: 46 }}>
        <Icon name="bookmark" color={accent} size={120} />
        <div style={{ fontSize: 70, fontWeight: 800, letterSpacing: ls, marginTop: 14 }}>{d.title}</div>
      </Float>
      <div style={{ transform: `scale(${0.8 + 0.2 * p})`, opacity: p, display: "flex", gap: 20 }}>
        <div style={{ padding: "18px 34px", borderRadius: 999, background: "#FF0000", color: "#fff", fontWeight: 700, fontSize: 32 }}>▶ Subscribe</div>
        <div style={{ padding: "18px 34px", borderRadius: 999, background: INK, color: "#fff", fontWeight: 700, fontSize: 32 }}>Follow {d.follow}</div>
      </div>
    </div>
  );
};

const Visual: React.FC<{ b: Beat; accent: string }> = ({ b, accent }) => {
  switch (b.v) {
    case "hook": return <Hook d={b.d} accent={accent} first={b.start < 0.05} />;
    case "list": return <List d={b.d} accent={accent} />;
    case "stat": return <Stat d={b.d} accent={accent} />;
    case "flow": return <Flow d={b.d} accent={accent} />;
    case "browser": return <Browser d={b.d} accent={accent} />;
    case "card": return <Card d={b.d} accent={accent} />;
    case "versus": return <Versus d={b.d} accent={accent} />;
    case "cta": return <Cta d={b.d} accent={accent} />;
    default: return <Card d={{ title: b.tag, rows: [] }} accent={accent} />;
  }
};

// ---------- kinetic caption: words appear as spoken; key words bold & bigger; one accent chip ----------
export const Caption: React.FC<{ b: Beat; accent: string; width?: number; baseSize?: number; big?: number }> = ({ b, accent, width = 900, baseSize = 50, big = 66 }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig();
  const t = b.start + f / fps;
  return (
    <div style={{ width, display: "flex", flexWrap: "wrap", justifyContent: "center", alignItems: "baseline", columnGap: 16, rowGap: 6, lineHeight: 1.25 }}>
      {b.words.map((w, i) => {
        const p = interpolate(t, [w.s - 0.05, w.s + 0.12], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
        const size = w.hl || w.chip ? big : baseSize;
        const base: React.CSSProperties = {
          fontSize: size, fontWeight: w.hl || w.chip ? 800 : 500, color: w.hl ? INK : "#5c5c5c",
          opacity: p, transform: `translateY(${(1 - p) * 18}px)`, display: "inline-block",
        };
        if (w.chip) {
          const c = interpolate(t, [w.s, w.s + 0.25], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
          return (
            <span key={i} style={{ ...base, position: "relative", color: c > 0.5 ? "#fff" : INK, padding: "0 14px" }}>
              <span style={{ position: "absolute", inset: "6% 0", borderRadius: 14, background: accent, transformOrigin: "left", transform: `scaleX(${c})`, zIndex: -1 }} />
              {w.t}
            </span>
          );
        }
        return <span key={i} style={base}>{w.t}</span>;
      })}
    </div>
  );
};

const Header: React.FC<{ series: string; tag: string; i: number; n: number; accent: string; watermark: string }> = ({ series, tag, i, n, accent, watermark }) => (
  <div style={{ position: "absolute", top: 236, left: 70, right: 70, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
    <div style={{ display: "flex", alignItems: "center", gap: 14, fontWeight: 700, fontSize: 34, color: INK }}>
      <div style={{ width: 40, height: 40, borderRadius: 12, background: accent, color: "#fff", display: "grid", placeItems: "center", fontSize: 24 }}>O</div>
      {watermark.charAt(0).toUpperCase() + watermark.slice(1)}
    </div>
    <div style={{ padding: "10px 20px", borderRadius: 999, border: "2px solid #d6d6d6", fontSize: 22, letterSpacing: 3, fontWeight: 600, color: "#555" }}>
      {series} · {tag} · {String(i + 1).padStart(2, "0")}/{String(n).padStart(2, "0")}
    </div>
  </div>
);

export const BG_FILL = BG;
export const INK_C = INK;
export const OmiShort: React.FC<OmiProps> = (props) => {
  const { fps } = useVideoConfig(); const f = useCurrentFrame();
  const t = f / fps;
  const idx = Math.max(0, props.beats.findIndex((b) => t >= b.start && t < b.end));
  const cur = props.beats[idx];
  return (
    <AbsoluteFill style={{ background: BG, fontFamily }}>
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 30%, #FAFAFA 0%, #EEEEEE 55%, #E4E4E4 100%)" }} />
      <AbsoluteFill style={{ opacity: 0.5, backgroundImage: "radial-gradient(#d4d4d4 1.6px, transparent 1.6px)", backgroundSize: "44px 44px", backgroundPosition: `0px ${(f * 0.4) % 44}px`,
        maskImage: "radial-gradient(ellipse at 50% 40%, black 0%, transparent 70%)", WebkitMaskImage: "radial-gradient(ellipse at 50% 40%, black 0%, transparent 70%)" }} />
      <div style={{ position: "absolute", left: 140 + Math.sin(f / 70) * 60, top: 420 + Math.cos(f / 90) * 40, width: 520, height: 520, borderRadius: 260,
        background: `radial-gradient(circle, ${props.accent}22 0%, transparent 70%)`, filter: "blur(10px)" }} />
      {props.audio ? <Audio src={staticFile(props.audio)} /> : null}
      {cur && <Header series={props.series} tag={cur.tag} i={idx} n={props.beats.length} accent={props.accent} watermark={props.watermark} />}
      {props.beats.map((b, i) => {
        const from = Math.round(b.start * fps); const len = Math.max(1, Math.round((b.end - b.start) * fps));
        return (
          <Sequence key={i} from={from} durationInFrames={len} layout="none">
            <BeatView b={b} accent={props.accent} len={len} />
          </Sequence>
        );
      })}
      {/* progress bar */}
      <div style={{ position: "absolute", top: 300, left: 70, right: 70, height: 6, borderRadius: 3, background: "#dcdcdc" }}>
        <div style={{ width: `${Math.min(100, (t / Math.max(0.1, props.duration)) * 100)}%`, height: "100%", borderRadius: 3, background: props.accent }} />
      </div>
      {/* watermark */}
      <div style={{ position: "absolute", bottom: 300, width: "100%", textAlign: "center", fontSize: 40, fontWeight: 700, color: "#C9C9C9", letterSpacing: 1 }}>
        {props.watermark}
      </div>
      <div style={{ position: "absolute", bottom: 262, width: "100%", textAlign: "center", fontSize: 20, fontWeight: 500, color: "#BDBDBD", letterSpacing: 1 }}>
        AI voice · by Omkar Ghate
      </div>
    </AbsoluteFill>
  );
};

const BeatView: React.FC<{ b: Beat; accent: string; len: number }> = ({ b, accent, len }) => {
  const f = useCurrentFrame();
  const out = interpolate(f, [len - 8, len], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ opacity: out, transform: `translateY(${(1 - out) * -30}px)` }}>
      <div style={{ position: "absolute", top: 340, height: 720, width: "100%", display: "flex", alignItems: "center", justifyContent: "center" }}>
        <Visual b={b} accent={accent} />
      </div>
      <div style={{ position: "absolute", top: 1120, width: "100%", display: "flex", justifyContent: "center" }}>
        <Caption b={b} accent={accent} />
      </div>
    </AbsoluteFill>
  );
};

export const omiMetadata = ({ props }: { props: OmiProps }) => ({
  durationInFrames: Math.max(30, Math.ceil(props.duration * 30)),
});
