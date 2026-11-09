import React from "react";
import { AbsoluteFill, Audio, Easing, interpolate, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { loadFont } from "@remotion/google-fonts/Poppins";
import { Beat, Browser, Caption, Card, Cta, Flow, Float, Hook, List, Stat, Versus } from "./OmiShort";

const { fontFamily } = loadFont("normal", { weights: ["400", "500", "600", "700", "800"], subsets: ["latin", "devanagari"] });
const INK = "#161616";
const ease = Easing.out(Easing.cubic);

export type LongProps = { id: string; series: string; title: string; accent: string; watermark: string; audio: string; duration: number; beats: Beat[] };
export const longDefaults: LongProps = { id: "demo", series: "DEMO", title: "Demo", accent: "#F2542D", watermark: "omilabs", audio: "", duration: 3, beats: [] };

// ---------- comparison table: columns per tool, rows per criterion, winner tick per row ----------
const Table: React.FC<{ d: any; accent: string }> = ({ d, accent }) => {
  const f = useCurrentFrame();
  const cols: string[] = d.cols || [];
  const rows: { k: string; v: string[]; win?: number }[] = d.rows || [];
  const cw = Math.min(460, 1300 / Math.max(1, cols.length));
  return (
    <Float w={360 + cw * cols.length} tilt={4} style={{ padding: "34px 40px" }}>
      <div style={{ display: "flex", borderBottom: "2px solid #eee", paddingBottom: 18 }}>
        <div style={{ width: 360, fontSize: 26, letterSpacing: 3, color: "#999", fontWeight: 600 }}>{(d.title || "COMPARISON").toUpperCase()}</div>
        {cols.map((c, i) => <div key={i} style={{ width: cw, textAlign: "center", fontSize: 38, fontWeight: 800 }}>{c}</div>)}
      </div>
      {rows.map((r, i) => {
        const p = interpolate(f, [10 + i * 7, 22 + i * 7], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
        return (
          <div key={i} style={{ display: "flex", alignItems: "center", padding: "18px 0", borderBottom: "1px solid #f0f0f0", opacity: p, transform: `translateY(${(1 - p) * 20}px)` }}>
            <div style={{ width: 360, fontSize: 30, color: "#666", fontWeight: 500 }}>{r.k}</div>
            {r.v.map((v, j) => (
              <div key={j} style={{ width: cw, textAlign: "center", fontSize: 30, fontWeight: r.win === j ? 800 : 500, color: r.win === j ? INK : "#555" }}>
                <span style={{ padding: r.win === j ? "6px 16px" : 0, borderRadius: 12, background: r.win === j ? `${accent}1f` : "transparent" }}>{v}{r.win === j ? " ✓" : ""}</span>
              </div>
            ))}
          </div>
        );
      })}
    </Float>
  );
};

// ---------- verdict: who wins for which use case ----------
const Verdict: React.FC<{ d: any; accent: string }> = ({ d, accent }) => {
  const f = useCurrentFrame();
  const items: { who: string; when: string }[] = d.items || [];
  return (
    <div style={{ display: "flex", gap: 40, justifyContent: "center" }}>
      {items.map((it, i) => {
        const p = spring({ frame: f - 6 - i * 10, fps: 30, config: { damping: 14, mass: 0.8 } });
        return (
          <div key={i} style={{ width: 460, transform: `scale(${0.8 + 0.2 * p}) translateY(${(1 - p) * 40}px)`, opacity: Math.min(1, p * 1.5) }}>
            <Float w={460} tilt={5} style={{ padding: 38, display: "flex", flexDirection: "column", gap: 18, minHeight: 330 }}>
              <div style={{ fontSize: 24, letterSpacing: 3, color: accent, fontWeight: 700 }}>🏆 WINNER</div>
              <div style={{ fontSize: 50, fontWeight: 800 }}>{it.who}</div>
              <div style={{ fontSize: 30, color: "#555", lineHeight: 1.35 }}>{it.when}</div>
            </Float>
          </div>
        );
      })}
    </div>
  );
};

// ---------- chapter card ----------
const Chapter: React.FC<{ d: any; accent: string }> = ({ d, accent }) => {
  const f = useCurrentFrame();
  const p = interpolate(f, [0, 18], [0, 1], { extrapolateRight: "clamp", easing: ease });
  const bar = interpolate(f, [8, 30], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  return (
    <div style={{ textAlign: "center", opacity: p, transform: `translateY(${(1 - p) * 30}px)` }}>
      <div style={{ fontSize: 34, letterSpacing: 8, color: accent, fontWeight: 700 }}>{d.num ? `CHAPTER ${d.num}` : "CHAPTER"}</div>
      <div style={{ fontSize: 110, fontWeight: 800, lineHeight: 1.05, marginTop: 14, color: INK }}>{d.title}</div>
      <div style={{ margin: "34px auto 0", width: 520 * bar, height: 10, borderRadius: 5, background: accent }} />
    </div>
  );
};

const LongVisual: React.FC<{ b: Beat; accent: string }> = ({ b, accent }) => {
  switch (b.v) {
    case "hook": return <Hook d={b.d} accent={accent} first={b.start < 0.05} />;
    case "list": return <List d={b.d} accent={accent} />;
    case "stat": return <Stat d={b.d} accent={accent} />;
    case "flow": return <Flow d={b.d} accent={accent} />;
    case "browser": return <Browser d={b.d} accent={accent} />;
    case "versus": return <Versus d={b.d} accent={accent} />;
    case "cta": return <Cta d={b.d} accent={accent} />;
    case "table": return <Table d={b.d} accent={accent} />;
    case "verdict": return <Verdict d={b.d} accent={accent} />;
    case "chapter": return <Chapter d={b.d} accent={accent} />;
    case "duo": return (  // two cards side by side (tool A | tool B)
      <div style={{ display: "flex", gap: 60 }}>
        <Card d={b.d.a} accent={accent} />
        <Card d={b.d.b} accent={b.d.accentB || "#2F6BFF"} />
      </div>);
    default: return <Card d={b.d} accent={accent} />;
  }
};

const LongBeat: React.FC<{ b: Beat; accent: string; len: number }> = ({ b, accent, len }) => {
  const f = useCurrentFrame();
  const out = interpolate(f, [len - 8, len], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const zoom = 1 + 0.03 * interpolate(f, [0, len], [0, 1], { extrapolateRight: "clamp" });   // slow push-in
  return (
    <AbsoluteFill style={{ opacity: out }}>
      <div style={{ position: "absolute", top: 150, height: b.v === "chapter" ? 760 : 640, width: "100%", display: "flex", alignItems: "center", justifyContent: "center", transform: `scale(${zoom})` }}>
        <LongVisual b={b} accent={accent} />
      </div>
      {b.v !== "chapter" && (
        <div style={{ position: "absolute", top: 820, width: "100%", display: "flex", justifyContent: "center" }}>
          <Caption b={b} accent={accent} width={1500} baseSize={44} big={56} />
        </div>
      )}
    </AbsoluteFill>
  );
};

export const OmiLong: React.FC<LongProps> = (props) => {
  const { fps } = useVideoConfig(); const f = useCurrentFrame(); const t = f / fps;
  const idx = Math.max(0, props.beats.findIndex((b) => t >= b.start && t < b.end));
  const chap = [...props.beats.slice(0, idx + 1)].reverse().find((b) => b.v === "chapter");
  return (
    <AbsoluteFill style={{ background: "#EEEEEE", fontFamily }}>
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 35%, #FAFAFA 0%, #EEEEEE 55%, #E2E2E2 100%)" }} />
      <AbsoluteFill style={{ opacity: 0.45, backgroundImage: "radial-gradient(#d2d2d2 1.6px, transparent 1.6px)", backgroundSize: "48px 48px", backgroundPosition: `${(f * 0.3) % 48}px 0px`,
        maskImage: "radial-gradient(ellipse at 50% 45%, black 0%, transparent 70%)", WebkitMaskImage: "radial-gradient(ellipse at 50% 45%, black 0%, transparent 70%)" }} />
      <div style={{ position: "absolute", left: 300 + Math.sin(f / 80) * 120, top: 200 + Math.cos(f / 95) * 60, width: 700, height: 700, borderRadius: 350,
        background: `radial-gradient(circle, ${props.accent}1c 0%, transparent 70%)` }} />
      {props.audio ? <Audio src={staticFile(props.audio)} /> : null}
      {/* header */}
      <div style={{ position: "absolute", top: 44, left: 80, right: 80, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 14, fontWeight: 700, fontSize: 34, color: INK }}>
          <div style={{ width: 42, height: 42, borderRadius: 12, background: props.accent, color: "#fff", display: "grid", placeItems: "center", fontSize: 24 }}>O</div>
          Omilabs
        </div>
        <div style={{ padding: "10px 22px", borderRadius: 999, border: "2px solid #d6d6d6", fontSize: 22, letterSpacing: 3, fontWeight: 600, color: "#555" }}>
          {props.series} · {chap ? (chap.d.title || "").toUpperCase() : "INTRO"}
        </div>
      </div>
      <div style={{ position: "absolute", top: 112, left: 80, right: 80, height: 6, borderRadius: 3, background: "#dcdcdc" }}>
        <div style={{ width: `${Math.min(100, (t / Math.max(0.1, props.duration)) * 100)}%`, height: "100%", borderRadius: 3, background: props.accent }} />
      </div>
      {props.beats.map((b, i) => {
        const from = Math.round(b.start * fps); const len = Math.max(1, Math.round((b.end - b.start) * fps));
        return <Sequence key={i} from={from} durationInFrames={len} layout="none"><LongBeat b={b} accent={props.accent} len={len} /></Sequence>;
      })}
      <div style={{ position: "absolute", bottom: 34, right: 70, fontSize: 34, fontWeight: 700, color: "#C9C9C9" }}>{props.watermark}</div>
      <div style={{ position: "absolute", bottom: 40, left: 80, fontSize: 18, color: "#BDBDBD" }}>AI voice · by Omkar Ghate · not affiliated with the tools shown</div>
    </AbsoluteFill>
  );
};

export const longMetadata = ({ props }: { props: LongProps }) => ({ durationInFrames: Math.max(30, Math.ceil(props.duration * 30)) });

// ---------- thumbnail (1280x720): big text, VS split, honest curiosity hook ----------
export type ThumbProps = { a: string; b?: string; top: string; hook: string; accent: string; colorA?: string; colorB?: string };
export const thumbDefaults: ThumbProps = { a: "ElevenLabs", b: "Bolna", top: "VOICE AI 2026", hook: "INDIA ke liye KAUN?", accent: "#F2542D" };
export const OmiThumb: React.FC<ThumbProps> = ({ a, b, top, hook, accent, colorA = "#111", colorB = "#2F6BFF" }) => (
  <AbsoluteFill style={{ fontFamily, background: "linear-gradient(135deg,#FAFAFA 0%,#E9E9E9 100%)" }}>
    {b ? (
      <>
        <div style={{ position: "absolute", left: 0, top: 0, width: 640, height: 720, background: colorA }} />
        <div style={{ position: "absolute", right: 0, top: 0, width: 640, height: 720, background: colorB }} />
        <div style={{ position: "absolute", left: 0, top: 150, width: 640, textAlign: "center", color: "#fff", fontSize: a.length > 9 ? 92 : 116, fontWeight: 800, letterSpacing: -2 }}>{a}</div>
        <div style={{ position: "absolute", right: 0, top: 150, width: 640, textAlign: "center", color: "#fff", fontSize: b.length > 9 ? 92 : 116, fontWeight: 800, letterSpacing: -2 }}>{b}</div>
        <div style={{ position: "absolute", left: 560, top: 110, width: 160, height: 160, borderRadius: 80, background: accent, color: "#fff", display: "grid", placeItems: "center",
          fontSize: 70, fontWeight: 800, border: "10px solid #fff", boxShadow: "0 20px 50px rgba(0,0,0,.35)" }}>VS</div>
      </>
    ) : (
      <div style={{ position: "absolute", left: 70, top: 120, fontSize: 130, fontWeight: 800, color: "#111", letterSpacing: -3 }}>{a}</div>
    )}
    <div style={{ position: "absolute", left: 50, right: 50, bottom: 70, display: "flex", justifyContent: "center" }}>
      <div style={{ background: "#FFE14D", color: "#111", padding: "18px 40px", borderRadius: 22, fontSize: 84, fontWeight: 800, transform: "rotate(-2deg)",
        boxShadow: "0 16px 40px rgba(0,0,0,.35)", border: "6px solid #111" }}>{hook}</div>
    </div>
    <div style={{ position: "absolute", top: 34, left: 40, background: "#fff", color: "#111", borderRadius: 999, padding: "10px 26px", fontSize: 34, fontWeight: 800,
      boxShadow: "0 8px 20px rgba(0,0,0,.2)" }}>{top}</div>
    <div style={{ position: "absolute", top: 34, right: 40, display: "flex", alignItems: "center", gap: 10, background: "#fff", borderRadius: 999, padding: "8px 22px 8px 10px",
      fontSize: 30, fontWeight: 800, color: "#111", boxShadow: "0 8px 20px rgba(0,0,0,.2)" }}>
      <div style={{ width: 44, height: 44, borderRadius: 12, background: accent, color: "#fff", display: "grid", placeItems: "center", fontSize: 26 }}>O</div>Omilabs
    </div>
  </AbsoluteFill>
);
