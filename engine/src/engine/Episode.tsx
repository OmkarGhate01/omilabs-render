import { setSeries, SERIES } from "./theme";
import React, { useEffect, useState } from "react";
import {
  AbsoluteFill,
  Sequence,
  continueRender,
  delayRender,
  interpolate,
  useCurrentFrame,
} from "remotion";
import { C, CL, EXPO, F, FPS, lerp, pad2, sp } from "./theme";
import { EpisodeProps, Line } from "./types";
import { OUT_ON_TOP, TWrap, TransitionOverlay } from "./transitions";
import { SCENES, TitleCard } from "./scenes";
import { OmMark, ScrambleFx, Vignette } from "./fx";

const FONTS = [
  "800 80px Unbounded",
  "700 80px Unbounded",
  "700 80px 'Space Grotesk'",
  "500 80px 'Space Grotesk'",
  "400 40px Inter",
  "600 40px Inter",
  "400 40px 'JetBrains Mono'",
  "700 40px 'JetBrains Mono'",
  "400 40px 'Noto Sans Devanagari'",
  "600 40px 'Noto Sans Devanagari'",
];

const segAt = (ep: EpisodeProps, f: number) => {
  let j = 0;
  ep.segments.forEach((sg, i) => {
    if (f >= sg.from) j = i;
  });
  return j;
};

const HUD: React.FC<{ ep: EpisodeProps }> = ({ ep }) => {
  const f = useCurrentFrame();
  const j = segAt(ep, f);
  const sg = ep.segments[j];
  const firstContent = ep.segments.length > 2 ? ep.segments[2].from : 0;
  const show = lerp(f, firstContent, firstContent + 20);
  if (show <= 0 || sg.kind === "title" || sg.scene <= 0) return null;
  const sc = ep.scenes[sg.scene];
  const total = ep.scenes.length - 1;
  const secs = Math.floor(f / FPS);
  const tc = `${pad2(Math.floor(secs / 60))}:${pad2(secs % 60)}`;
  const content = ep.segments.filter((x) => x.kind === "scene" && x.scene > 0);
  return (
    <AbsoluteFill style={{ opacity: show, pointerEvents: "none" }}>
      <div
        style={{
          position: "absolute",
          top: 40,
          left: 130,
          right: 130,
          display: "flex",
          alignItems: "center",
          gap: 22,
        }}
      >
        <OmMark size={44} />
        <div
          style={{
            fontFamily: F.mono,
            fontWeight: 700,
            fontSize: 22,
            color: C.cyan,
            letterSpacing: 2,
          }}
        >
          {pad2(sg.scene)}/{pad2(total)}
        </div>
        <div style={{ width: 430, overflow: "hidden", whiteSpace: "nowrap" }}>
          <ScrambleFx
            key={j}
            text={sc.label.toUpperCase()}
            at={sg.from + 4}
            size={22}
            font={F.mono}
            weight={700}
            color={C.muted}
            speed={0.5}
            ls={2}
          />
        </div>
        <div style={{ flex: 1, display: "flex", gap: 6 }}>
          {content.map((x, i) => {
            const p = interpolate(f, [x.from, x.to], [0, 100], CL);
            return (
              <div
                key={i}
                style={{
                  flex: x.to - x.from,
                  height: 5,
                  background: C.line,
                  borderRadius: 3,
                  overflow: "hidden",
                }}
              >
                <div
                  style={{ width: `${p}%`, height: "100%", background: C.cyan }}
                />
              </div>
            );
          })}
        </div>
        <div
          style={{
            fontFamily: F.mono,
            fontWeight: 700,
            fontSize: 22,
            color: C.muted,
            letterSpacing: 2,
          }}
        >
          EP {pad2(ep.n)} · {tc}
        </div>
      </div>
      {sc.src && (
        <div
          style={{
            position: "absolute",
            left: 130,
            bottom: 22,
            fontFamily: F.mono,
            fontSize: 19,
            color: C.dim,
            letterSpacing: 1,
          }}
        >
          <span style={{ color: C.cyan }}>SRC ▸</span> {SERIES.tag === "ELEVENLABS" ? "elevenlabs.io/docs/" + sc.src : String(sc.src).startsWith("oss:") ? "github.com/bolna-ai/bolna" : "bolna.ai/docs/" + sc.src}
        </div>
      )}
      <div
        style={{
          position: "absolute",
          right: 130,
          bottom: 22,
          fontFamily: F.mono,
          fontSize: 19,
          color: C.dim,
          letterSpacing: 2,
        }}
      >
        DOCS-CHECKED · OMILABS
      </div>
      {[
        { left: 24, top: 24, bt: true, bl: true },
        { right: 24, top: 24, bt: true, br: true },
        { left: 24, bottom: 24, bb: true, bl: true },
        { right: 24, bottom: 24, bb: true, br: true },
      ].map((c, i) => (
        <div
          key={i}
          style={{
            position: "absolute",
            left: c.left,
            right: c.right,
            top: c.top,
            bottom: c.bottom,
            width: 26,
            height: 26,
            borderTop: c.bt ? `2px solid ${C.line2}` : undefined,
            borderBottom: c.bb ? `2px solid ${C.line2}` : undefined,
            borderLeft: c.bl ? `2px solid ${C.line2}` : undefined,
            borderRight: c.br ? `2px solid ${C.line2}` : undefined,
          }}
        />
      ))}
    </AbsoluteFill>
  );
};

const Captions: React.FC<{ ep: EpisodeProps }> = ({ ep }) => {
  const f = useCurrentFrame();
  const t = f / FPS;
  let cur: Line | null = null;
  for (const sc of ep.scenes) {
    for (const l of sc.lines) {
      if (t >= l.start - 0.05 && t < l.end + 0.2) cur = l;
    }
  }
  if (!cur) return null;
  const words = cur.t.split(" ");
  const total = cur.t.length;
  const p = interpolate(t, [cur.start, cur.end], [0, 1], CL);
  const chunks: { w: string; a: number; b: number }[][] = [];
  let acc = 0;
  words.forEach((w, i) => {
    const a = acc / total;
    acc += w.length + 1;
    if (i % 7 === 0) chunks.push([]);
    chunks[chunks.length - 1].push({ w, a, b: acc / total });
  });
  let chunk = chunks[0];
  for (const ch of chunks) if (p >= ch[0].a) chunk = ch;
  return (
    <AbsoluteFill
      style={{
        justifyContent: "flex-end",
        alignItems: "center",
        paddingBottom: 66,
        pointerEvents: "none",
      }}
    >
      <div
        style={{
          display: "flex",
          gap: 13,
          background: "rgba(4,6,13,0.84)",
          border: `2px solid ${C.line}`,
          borderRadius: 18,
          padding: "13px 30px",
          maxWidth: 1560,
          flexWrap: "wrap",
          justifyContent: "center",
        }}
      >
        {chunk.map((it, i) => {
          const said = p >= it.a;
          const now = p >= it.a && p < it.b;
          return (
            <span
              key={i}
              style={{
                fontFamily: F.body,
                fontWeight: 600,
                fontSize: 40,
                color: now ? C.cyan : said ? C.text : C.muted,
                transform: `translateY(${now ? -3 : 0}px)`,
                display: "inline-block",
              }}
            >
              {it.w}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

const LowerThird: React.FC<{ ep: EpisodeProps }> = ({ ep }) => {
  const f = useCurrentFrame();
  if (ep.segments.length < 3) return null;
  const st = ep.segments[2].from + 24;
  const en = st + 120;
  if (f < st || f > en) return null;
  const inn = sp(f, st, 18);
  const out = lerp(f, en - 14, en, 1, 0);
  return (
    <div
      style={{
        position: "absolute",
        left: 130,
        top: 800,
        display: "flex",
        opacity: out,
        transform: `translateX(${(1 - inn) * -90}px)`,
      }}
    >
      <div style={{ width: 8, background: C.cyan, borderRadius: 4 }} />
      <div
        style={{
          background: "rgba(10,16,32,0.94)",
          border: `2px solid ${C.line2}`,
          borderLeft: "none",
          padding: "16px 34px",
          borderRadius: "0 14px 14px 0",
          opacity: inn,
        }}
      >
        <div
          style={{
            fontFamily: F.head,
            fontWeight: 700,
            fontSize: 44,
            color: C.text,
          }}
        >
          Omkar Ghate
        </div>
        <div style={{ fontFamily: F.body, fontSize: 26, color: C.muted }}>
          Agentic AI Architect · Omilabs
        </div>
      </div>
    </div>
  );
};

// v3 look (ElevenLabs series): top spotlight that shifts colour per scene + travelling sparkle, blended over everything.
const V3Light: React.FC<{ ep: any }> = ({ ep }) => {
  const f = useCurrentFrame();
  const seg = ep.segments.find((g: any) => f >= g.from && f < g.to) || ep.segments[0];
  const pal = ["#7B61FF", "#35E0FF", "#2EE87A", "#FFB547"];
  const c = pal[(seg.scene ?? 0) % pal.length];
  const p = (f - seg.from) / Math.max(1, seg.to - seg.from);
  const x = 200 + p * 1520, y = 1000 - Math.sin(p * Math.PI) * 60;
  return (
    <AbsoluteFill style={{ pointerEvents: "none", zIndex: 900 }}>
      <AbsoluteFill style={{ background: `radial-gradient(ellipse 55% 45% at 50% -8%, ${c}55 0%, ${c}18 45%, transparent 100%)`, mixBlendMode: "screen" }} />
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 50%, transparent 55%, rgba(0,0,0,0.55) 100%)" }} />
      <svg width={1920} height={1080} style={{ position: "absolute", left: 0, top: 0, mixBlendMode: "screen", opacity: p > 0.04 && p < 0.96 ? 0.8 : 0 }}>
        <circle cx={x} cy={y} r={40} fill={c} opacity={0.25} />
        <path d={`M${x - 34} ${y}L${x} ${y - 3}L${x + 34} ${y}L${x} ${y + 3}Z M${x} ${y - 24}L${x + 3} ${y}L${x} ${y + 24}L${x - 3} ${y}Z`} fill="#fff" />
      </svg>
    </AbsoluteFill>
  );
};

export const Episode: React.FC<EpisodeProps> = (ep) => {
  setSeries((ep as any).series);
  const f = useCurrentFrame();
  const [handle] = useState(() => delayRender("fonts"));
  useEffect(() => {
    Promise.all(FONTS.map((x) => document.fonts.load(x)))
      .then(() => continueRender(handle))
      .catch(() => continueRender(handle));
  }, [handle]);
  const segs = ep.segments;
  return (
    <AbsoluteFill style={{ backgroundColor: C.bg }}>
      {segs.map((sg, j) => {
        const hin = sg.tin ? Math.floor(sg.tin.d / 2) : 0;
        const from = sg.from - hin;
        const end = sg.tout
          ? sg.to + (sg.tout.d - Math.floor(sg.tout.d / 2))
          : sg.to;
        const dur = Math.max(1, end - from);
        const exiting =
          sg.tout &&
          f >= end - sg.tout.d &&
          OUT_ON_TOP.indexOf(sg.tout.type) >= 0;
        const Comp =
          sg.kind === "scene"
            ? SCENES[ep.scenes[sg.scene].type] || SCENES.statement
            : null;
        return (
          <Sequence
            key={j}
            from={from}
            durationInFrames={dur}
            style={{ zIndex: exiting ? 500 : 10 + j }}
          >
            <TWrap id={"sg" + j} len={dur} tin={sg.tin} tout={sg.tout}>
              {Comp ? (
                <Comp
                  s={ep.scenes[sg.scene]}
                  from={from}
                  len={dur}
                  idx={sg.scene}
                  tin={sg.tin ? sg.tin.d : 0}
                  ep={ep}
                />
              ) : (
                <TitleCard ep={ep} len={dur} />
              )}
            </TWrap>
          </Sequence>
        );
      })}
      {segs.map((sg, j) =>
        sg.tin ? (
          <Sequence
            key={"ov" + j}
            from={sg.from - Math.floor(sg.tin.d / 2)}
            durationInFrames={sg.tin.d}
            style={{ zIndex: 900 }}
          >
            <TransitionOverlay t={sg.tin} seed={"t" + j} />
          </Sequence>
        ) : null,
      )}
      <AbsoluteFill style={{ zIndex: 950 }}>
        <Vignette />
        <HUD ep={ep} />
        <LowerThird ep={ep} />
        <Captions ep={ep} />
      </AbsoluteFill>
      {f < 2 && (
        <AbsoluteFill
          style={{
            zIndex: 999,
            opacity: interpolate(f, [0, 2], [1, 0], { ...CL, easing: EXPO }),
            backgroundColor: C.bg,
          }}
        />
      )}
      {(ep as any).style === "v3" && <V3Light ep={ep} />}
    </AbsoluteFill>
  );
};
