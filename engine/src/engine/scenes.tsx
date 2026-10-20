import React from "react";
import { AbsoluteFill, interpolate, random, useCurrentFrame } from "remotion";
import { noise2D } from "@remotion/noise";
import {
  C,
  CL,
  EXPO,
  F,
  FPS,
  H,
  RAMP,
  W,
  fit,
  lerp,
  pad2,
  sp,
  tone,
} from "./theme";
import { SERIES } from "./theme";
import { EpisodeProps, SceneData } from "./types";
import {
  Backdrop,
  Brackets,
  Chip,
  Grain,
  Headline,
  Kicker,
  LightLeak,
  OmMark,
  Panel,
  Pop,
  ScrambleFx,
  SplitFx,
} from "./fx";
import { Icon } from "./icons";

export type SP = {
  s: SceneData;
  from: number;
  len: number;
  idx: number;
  tin: number;
  ep: EpisodeProps;
};

// ---------- helpers ----------
const cueMap = (s: SceneData, from: number) => {
  const map: Record<string, number> = {};
  for (const l of s.lines) {
    if (l.cue && map[l.cue] === undefined)
      map[l.cue] = Math.round(l.start * FPS) - from;
  }
  const first = s.lines.length ? Math.round(s.lines[0].start * FPS) - from : 0;
  return {
    stg: Number(s.stagger || 9),
    has: (k: string) => map[k] !== undefined,
    at: (k: string, fb: number) => (map[k] !== undefined ? map[k] : fb),
    first,
  };
};

// item i reveals on its own cue, else staggered from an "all" cue, else at the fallback frame
const rv = (cu: ReturnType<typeof cueMap>, i: number, fb: number) =>
  cu.has(String(i + 1))
    ? cu.at(String(i + 1), 0)
    : cu.has("all")
      ? cu.at("all", 0) + i * cu.stg
      : fb;

const activeIdx = (f: number, times: number[], has: boolean[], end: number) => {
  let a = -1;
  for (let i = 0; i < times.length; i++) if (has[i] && f >= times[i]) a = i;
  if (a < 0) return -1;
  let stop = end;
  for (let j = a + 1; j < times.length; j++) {
    if (has[j]) {
      stop = times[j];
      break;
    }
  }
  return f < stop ? a : -1;
};

const FXS = ["split", "words", "glitch", "outline", "scramble", "extrude"];
const autoFx = (idx: number, title: string) => {
  let fx = FXS[idx % FXS.length];
  if (fx === "scramble" && title.length > 26) fx = "words";
  if ((fx === "extrude" || fx === "outline") && title.length > 30) fx = "split";
  return fx;
};

const Shell: React.FC<{
  len: number;
  bg?: string;
  hue?: string;
  center?: boolean;
  grain?: boolean;
  children: React.ReactNode;
}> = ({ len, bg = "grid", hue, center = false, grain = false, children }) => {
  const f = useCurrentFrame();
  const z = lerp(f, 0, len, 1, 1.04);
  const dx = noise2D("cx", f * 0.004, 0) * 9;
  const dy = noise2D("cy", 0, f * 0.004) * 6;
  const tilt = lerp(f, 0, 34, 6, 0, EXPO);
  return (
    <AbsoluteFill style={{ overflow: "hidden", backgroundColor: C.bg }}>
      <Backdrop variant={bg} hue={hue} />
      <AbsoluteFill style={{ perspective: 2200 }}>
        <AbsoluteFill
          style={{
            transform: `translate(${dx}px, ${dy}px) scale(${z}) rotateX(${tilt}deg)`,
            padding: "150px 130px 178px",
            display: "flex",
            flexDirection: "column",
            justifyContent: center ? "center" : "flex-start",
            alignItems: center ? "center" : "stretch",
          }}
        >
          {children}
        </AbsoluteFill>
      </AbsoluteFill>
      {grain && <Grain opacity={0.06} />}
    </AbsoluteFill>
  );
};

const Header: React.FC<{
  s: SceneData;
  at: number;
  idx: number;
  align?: "left" | "center";
  big?: boolean;
}> = ({ s, at, idx, align = "left", big = false }) => {
  const title = s.title || "";
  const fx = s.fx || autoFx(idx, title);
  const hero = fx === "split" || fx === "extrude" || fx === "outline";
  const base = hero ? (big ? 104 : 66) : big ? 118 : 84;
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: 20,
        alignItems: align === "center" ? "center" : "flex-start",
        textAlign: align,
      }}
    >
      <Kicker
        text={s.kicker || s.label}
        at={at}
        index={pad2(idx)}
        align={align}
      />
      {title && (
        <Headline
          text={title}
          fx={fx}
          at={at + 6}
          size={fit(title, base, hero ? 22 : 28, base * 0.66)}
          accent={s.accent || []}
          align={align}
          font={hero ? F.hero : F.head}
          weight={hero ? 800 : 700}
        />
      )}
    </div>
  );
};

const Note: React.FC<{ text: string; color?: string; size?: number }> = ({
  text,
  color = C.amber,
  size = 32,
}) => (
  <div
    style={{
      display: "inline-flex",
      alignItems: "center",
      gap: 16,
      background: "rgba(14,22,40,0.94)",
      border: `2px solid ${color}`,
      borderRadius: 18,
      padding: "16px 28px",
      boxShadow: `0 0 40px ${color}33`,
    }}
  >
    <Icon
      name={color === C.amber ? "alert" : color === C.green ? "check" : "bulb"}
      size={size * 1.3}
      color={color}
    />
    <span
      style={{
        fontFamily: F.body,
        fontWeight: 600,
        fontSize: size,
        color: C.text,
        lineHeight: 1.3,
      }}
    >
      {text}
    </span>
  </div>
);

const BigMotif: React.FC<{
  icon: string;
  x?: number;
  y?: number;
  size?: number;
  o?: number;
}> = ({ icon, x = 1180, y = 120, size = 860, o = 0.06 }) => {
  const f = useCurrentFrame();
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        opacity: o,
        transform: `rotate(${f * 0.05}deg) scale(${1 + 0.03 * Math.sin(f / 40)})`,
      }}
    >
      <Icon name={icon} size={size} color={C.cyan} sw={1} />
    </div>
  );
};

// ---------- HOOK ----------
export const Hook: React.FC<SP> = ({ s, from, len, ep }) => {
  const f = useCurrentFrame();
  const cu = cueMap(s, from);
  const beats = (s.beats || []) as {
    t: string;
    fx?: string;
    sub?: string;
    icon?: string;
    tone?: string;
    accent?: string[];
  }[];
  const times = beats.map((_, i) => rv(cu, i, i === 0 ? cu.first : 99999));
  let cur = 0;
  times.forEach((t, i) => {
    if (f >= t - 2) cur = i;
  });
  const b = beats[cur] || { t: "" };
  const t0 = times[cur];
  const nextT = cur + 1 < times.length ? times[cur + 1] : len + 999;
  const out = lerp(f, nextT - 7, nextT - 1, 0, 1, EXPO);
  const fxs = ["glitch", "split", "extrude", "scramble", "words"];
  let fx = b.fx || fxs[cur % fxs.length];
  if (fx === "scramble" && b.t.length > 24) fx = "split";
  const size = fit(b.t, 150, 14, 80);
  return (
    <Shell len={len} bg="floor" hue="violet" grain center>
      <BigMotif icon={ep.icon} />
      <LightLeak strength={0.6} />
      <div
        style={{
          transform: `scale(${1 + out * 0.18})`,
          opacity: 1 - out,
          filter: out > 0 ? `blur(${out * 14}px)` : undefined,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 34,
          textAlign: "center",
          maxWidth: 1600,
        }}
      >
        {b.icon && (
          <Pop at={t0}>
            <Icon
              name={b.icon}
              size={150}
              color={tone(b.tone)}
              draw={lerp(f, t0, t0 + 24, 0, 1, EXPO)}
            />
          </Pop>
        )}
        <Headline
          text={b.t}
          fx={fx}
          at={t0 + 2}
          size={size}
          accent={b.accent || []}
          align="center"
          font={F.hero}
          weight={800}
          color={b.tone ? tone(b.tone) : C.text}
        />
        {b.sub && (
          <Pop at={t0 + 16}>
            <div
              style={{
                fontFamily: F.body,
                fontSize: 40,
                color: C.muted,
                maxWidth: 1300,
                lineHeight: 1.35,
              }}
            >
              {b.sub}
            </div>
          </Pop>
        )}
      </div>
    </Shell>
  );
};

// ---------- TITLE CARD (sting + episode title) ----------
export const TitleCard: React.FC<{ ep: EpisodeProps; len: number }> = ({
  ep,
  len,
}) => {
  const f = useCurrentFrame();
  const sting = 40;
  const draw = lerp(f, 2, 30, 0, 1, EXPO);
  const markOut = lerp(f, sting - 6, sting + 8, 0, 1, RAMP);
  const num = pad2(ep.n);
  const burst = new Array(36).fill(0).map((_, i) => {
    const a = random("ba" + i) * Math.PI * 2;
    const d = lerp(f, 4, 40, 0, 1, EXPO) * (300 + random("bd" + i) * 600);
    return {
      x: W / 2 + Math.cos(a) * d,
      y: H / 2 - 40 + Math.sin(a) * d,
      o: 1 - lerp(f, 10, 44, 0, 1),
      r: 2 + random("br" + i) * 4,
    };
  });
  const isoRot = interpolate(f, [sting, len], [-30, -18], CL);
  return (
    <AbsoluteFill style={{ backgroundColor: C.bg, overflow: "hidden" }}>
      <Backdrop variant="floor" hue="violet" />
      <LightLeak strength={1} />
      {/* phase 1: logo sting */}
      {f < sting + 10 && (
        <AbsoluteFill
          style={{
            alignItems: "center",
            justifyContent: "center",
            gap: 30,
            transform: `scale(${1 + markOut * 2.4})`,
            opacity: 1 - markOut,
            filter: markOut > 0 ? `blur(${markOut * 10}px)` : undefined,
          }}
        >
          <svg
            width={W}
            height={H}
            style={{ position: "absolute", left: 0, top: 0 }}
          >
            {burst.map((p, i) => (
              <circle
                key={i}
                cx={p.x}
                cy={p.y}
                r={p.r}
                fill={i % 3 ? C.cyan : C.text}
                opacity={Math.max(0, p.o)}
              />
            ))}
          </svg>
          <div style={{ transform: `scale(${0.7 + 0.3 * sp(f, 2, 12)})` }}>
            <OmMark size={230} draw={draw} />
          </div>
          <ScrambleFx
            text="OMILABS"
            at={10}
            size={84}
            font={F.hero}
            weight={800}
            ls={14}
          />
        </AbsoluteFill>
      )}
      {/* phase 2: episode title */}
      {f >= sting - 4 && (
        <AbsoluteFill>
          <div
            style={{
              position: "absolute",
              right: -40,
              top: 230,
              perspective: 1600,
              opacity: lerp(f, sting, sting + 14) * 0.85,
            }}
          >
            <div
              style={{
                transformStyle: "preserve-3d",
                transform: `rotateX(18deg) rotateY(${isoRot}deg)`,
                position: "relative",
                fontFamily: F.hero,
                fontWeight: 800,
                fontSize: 500,
                lineHeight: 1,
              }}
            >
              {new Array(14).fill(0).map((_, i) => (
                <div
                  key={i}
                  style={{
                    position: i === 0 ? "relative" : "absolute",
                    left: 0,
                    top: 0,
                    transform: `translateZ(${-i * 7}px)`,
                    color:
                      i === 0
                        ? "transparent"
                        : interpolate(i, [1, 13], [0.32, 0.04]) > 0
                          ? `rgba(45,123,255,${interpolate(i, [1, 13], [0.32, 0.04])})`
                          : "transparent",
                    WebkitTextStroke: i === 0 ? `3px ${C.cyan}` : undefined,
                  }}
                >
                  {num}
                </div>
              ))}
            </div>
          </div>
          <AbsoluteFill
            style={{ padding: "0 140px", justifyContent: "center" }}
          >
            <Kicker text={`Episode ${num} · ${ep.module}`} at={sting} />
            <div style={{ marginTop: 30, maxWidth: 1060 }}>
              <SplitFx
                text={ep.short}
                at={sting + 6}
                size={fit(ep.short, 104, 12, 66)}
                font={F.hero}
                weight={800}
                accent={[]}
              />
            </div>
            <div
              style={{
                height: 6,
                width: 560 * lerp(f, sting + 18, sting + 46, 0, 1, EXPO),
                background: `linear-gradient(90deg, ${C.blue}, ${C.cyan})`,
                borderRadius: 3,
                marginTop: 40,
                boxShadow: `0 0 30px ${C.cyan}`,
              }}
            />
            <Pop at={sting + 24}>
              <div
                style={{
                  fontFamily: F.body,
                  fontWeight: 600,
                  fontSize: 36,
                  color: C.muted,
                  marginTop: 26,
                }}
              >
                {SERIES.name} · Created by Omkar Ghate
              </div>
            </Pop>
          </AbsoluteFill>
        </AbsoluteFill>
      )}
      <Grain opacity={0.08} />
    </AbsoluteFill>
  );
};

// ---------- STATEMENT ----------
export const Statement: React.FC<SP> = ({ s, from, len, idx, tin }) => {
  const f = useCurrentFrame();
  const cu = cueMap(s, from);
  const at = Math.round(tin * 0.5);
  const chips = (s.chips || []) as (string | { t: string; tone?: string })[];
  return (
    <Shell len={len} bg={s.bg || "floor"} center>
      {s.visual === "rings" && (
        <BigMotif
          icon={s.icon || "target"}
          x={560}
          y={110}
          size={800}
          o={0.05}
        />
      )}
      <Header s={s} at={at} idx={idx} align="center" big />
      {s.sub && (
        <Pop at={cu.at("sub", at + 28)}>
          <div
            style={{
              fontFamily: F.body,
              fontSize: 40,
              color: C.muted,
              maxWidth: 1400,
              marginTop: 34,
              lineHeight: 1.38,
              textAlign: "center",
            }}
          >
            {s.sub}
          </div>
        </Pop>
      )}
      {chips.length > 0 && (
        <div
          style={{
            display: "flex",
            gap: 18,
            flexWrap: "wrap",
            justifyContent: "center",
            marginTop: 46,
            maxWidth: 1600,
          }}
        >
          {chips.map((c, i) => {
            const t = typeof c === "string" ? c : c.t;
            const tn = typeof c === "string" ? undefined : c.tone;
            const a = rv(cu, i, at + 36 + i * 6);
            const on = cu.has(String(i + 1)) && f >= a && f < a + 45;
            return (
              <Pop key={i} at={a}>
                <Chip size={36} color={tone(tn)} solid={on}>
                  {t}
                </Chip>
              </Pop>
            );
          })}
        </div>
      )}
    </Shell>
  );
};

// ---------- CARDS ----------
export const Cards: React.FC<SP> = ({ s, from, len, idx, tin }) => {
  const f = useCurrentFrame();
  const cu = cueMap(s, from);
  const at = Math.round(tin * 0.5);
  const items = (s.items || []) as {
    h: string;
    d?: string;
    tag?: string;
    icon?: string;
    tone?: string;
  }[];
  const n = items.length;
  const cols =
    n === 4
      ? items.every((it) => (it.d || "").length <= 54)
        ? 4
        : 2
      : Math.min(n, 3);
  const has = items.map((_, i) => cu.has(String(i + 1)));
  const rev = items.map((_, i) => rv(cu, i, at + 22 + i * 7));
  const callT = s.callout ? cu.at("c", at + 60) : -1;
  const act = activeIdx(f, rev, has, s.callout && cu.has("c") ? callT : len);
  const small = cols >= 4 || (cols === 2 && n === 4);
  return (
    <Shell len={len} bg={s.bg || "grid"}>
      <Header s={s} at={at} idx={idx} />
      <div
        style={{
          display: "grid",
          gridTemplateColumns: `repeat(${cols}, 1fr)`,
          gap: 26,
          marginTop: 30,
          flex: 1,
          alignContent: "center",
        }}
      >
        {items.map((it, i) => {
          const col = tone(it.tone);
          return (
            <Pop key={i} at={rev[i]} flip dy={70}>
              <Panel
                active={act === i}
                color={col}
                style={{ minHeight: small ? 250 : 320 }}
              >
                <div
                  style={{
                    display: "flex",
                    alignItems: "flex-start",
                    gap: 20,
                    flexDirection: "column",
                  }}
                >
                  {it.icon && (
                    <Icon
                      name={it.icon}
                      size={small ? 66 : 80}
                      color={col}
                      draw={lerp(f, rev[i] + 4, rev[i] + 28, 0, 1, EXPO)}
                    />
                  )}
                  <div
                    style={{
                      fontFamily: F.head,
                      fontWeight: 700,
                      fontSize: small ? 42 : 50,
                      color: act === i ? col : C.text,
                      lineHeight: 1.08,
                    }}
                  >
                    {it.h}
                  </div>
                </div>
                {it.tag && (
                  <div style={{ marginTop: 14 }}>
                    <Chip size={22} color={col} solid={act === i}>
                      {it.tag}
                    </Chip>
                  </div>
                )}
                {it.d && (
                  <div
                    style={{
                      fontFamily: F.body,
                      fontSize: small ? 27 : 30,
                      color: C.muted,
                      marginTop: 14,
                      lineHeight: 1.36,
                    }}
                  >
                    {it.d}
                  </div>
                )}
              </Panel>
            </Pop>
          );
        })}
      </div>
      {s.callout && f >= callT - 2 && (
        <Pop at={callT} style={{ marginTop: 30, alignSelf: "center" }}>
          <Note text={s.callout.t} color={tone(s.callout.tone || "warn")} />
        </Pop>
      )}
    </Shell>
  );
};

// ---------- PIPELINE ----------
export const Pipeline: React.FC<SP> = ({ s, from, len, idx, tin }) => {
  const f = useCurrentFrame();
  const cu = cueMap(s, from);
  const at = Math.round(tin * 0.5);
  const nodes = (s.nodes || []) as {
    h: string;
    s?: string;
    d?: string;
    icon?: string;
    tone?: string;
  }[];
  const n = nodes.length;
  const has = nodes.map((_, i) => cu.has(String(i + 1)));
  const rev = nodes.map((_, i) => rv(cu, i, at + 20 + i * 8));
  const loopT = s.loop ? cu.at("c", rev[n - 1] + 40) : 99999;
  const mT = s.merge ? cu.at("m", 99999) : 99999;
  const act = activeIdx(f, rev, has, Math.min(loopT, mT, len));
  const allOn = f >= rev[n - 1] + 10;
  const m = lerp(f, mT, mT + 30, 0, 1, RAMP);
  const conn = 84;
  const nodeW = (W - 260 - conn * (n - 1)) / n;
  const big = n <= 3;
  return (
    <Shell len={len} bg={s.bg || "dots"}>
      <Header s={s} at={at} idx={idx} />
      <div
        style={{
          position: "relative",
          flex: 1,
          display: "flex",
          alignItems: "center",
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "stretch",
            opacity: 1 - m * 0.95,
          }}
        >
          {nodes.map((nd, i) => {
            const col = tone(nd.tone);
            const on =
              act === i ||
              (allOn &&
                act < 0 &&
                f >= loopT &&
                Math.floor((f - loopT) / 16) % n === i);
            const shift = ((n - 1) / 2 - i) * (nodeW + conn) * m;
            return (
              <React.Fragment key={i}>
                <Pop
                  at={rev[i]}
                  flip
                  dy={60}
                  style={{ width: nodeW, transform: undefined }}
                >
                  <div
                    style={{
                      transform: `translateX(${shift}px)`,
                      height: "100%",
                    }}
                  >
                    <Panel
                      active={on}
                      color={col}
                      style={{
                        height: big ? 360 : 340,
                        padding: big ? "28px 32px" : "22px 22px",
                      }}
                    >
                      <div
                        style={{
                          display: "flex",
                          justifyContent: "space-between",
                          alignItems: "center",
                        }}
                      >
                        <span
                          style={{
                            fontFamily: F.mono,
                            fontWeight: 700,
                            fontSize: 24,
                            color: C.muted,
                          }}
                        >
                          {pad2(i + 1)}
                        </span>
                        {nd.icon && (
                          <Icon
                            name={nd.icon}
                            size={big ? 62 : 50}
                            color={col}
                            draw={lerp(f, rev[i] + 4, rev[i] + 26, 0, 1, EXPO)}
                          />
                        )}
                      </div>
                      <div
                        style={{
                          fontFamily: big ? F.hero : F.head,
                          fontWeight: big ? 800 : 700,
                          fontSize: big
                            ? fit(nd.h, 64, 7, 40)
                            : fit(nd.h, 42, 8, 28),
                          color: on ? col : C.text,
                          marginTop: 14,
                          lineHeight: 1.05,
                        }}
                      >
                        {nd.h}
                      </div>
                      {nd.s && (
                        <div
                          style={{
                            fontFamily: F.head,
                            fontWeight: 700,
                            fontSize: big ? 34 : 25,
                            color: C.text,
                            marginTop: 12,
                          }}
                        >
                          {nd.s}
                        </div>
                      )}
                      {nd.d && (
                        <div
                          style={{
                            fontFamily: F.body,
                            fontSize: big ? 28 : 22,
                            color: C.muted,
                            marginTop: 10,
                            lineHeight: 1.32,
                          }}
                        >
                          {nd.d}
                        </div>
                      )}
                    </Panel>
                  </div>
                </Pop>
                {i < n - 1 && (
                  <div
                    style={{
                      width: conn,
                      alignSelf: "center",
                      position: "relative",
                      height: 8,
                      opacity: lerp(f, rev[i + 1] - 6, rev[i + 1] + 6),
                    }}
                  >
                    <div
                      style={{
                        position: "absolute",
                        inset: 0,
                        background: C.line2,
                        borderRadius: 4,
                      }}
                    />
                    {[0, 1, 2].map((k) => {
                      const ph = ((f + k * 10) % 30) / 30;
                      const live = act === i || act === i + 1 || f >= loopT;
                      return (
                        <div
                          key={k}
                          style={{
                            position: "absolute",
                            top: -6,
                            left: ph * (conn - 20),
                            width: 20,
                            height: 20,
                            borderRadius: 10,
                            background: C.cyan,
                            boxShadow: `0 0 18px ${C.cyan}`,
                            opacity: live ? Math.sin(ph * Math.PI) : 0,
                          }}
                        />
                      );
                    })}
                  </div>
                )}
              </React.Fragment>
            );
          })}
        </div>
        {s.merge && m > 0 && (
          <div
            style={{
              position: "absolute",
              left: 0,
              right: 0,
              display: "flex",
              justifyContent: "center",
            }}
          >
            <div
              style={{
                transform: `scale(${0.7 + 0.3 * m})`,
                opacity: m,
                width: 900,
              }}
            >
              <Panel
                active
                color={C.violet}
                style={{ textAlign: "center", padding: "40px 50px" }}
              >
                <div
                  style={{
                    fontFamily: F.mono,
                    fontWeight: 700,
                    fontSize: 24,
                    color: C.muted,
                  }}
                >
                  {s.merge.k || "ONE MODEL"}
                </div>
                <div
                  style={{
                    fontFamily: F.hero,
                    fontWeight: 800,
                    fontSize: 64,
                    color: C.violet,
                    marginTop: 10,
                  }}
                >
                  {s.merge.h}
                </div>
                {s.merge.d && (
                  <div
                    style={{
                      fontFamily: F.body,
                      fontSize: 32,
                      color: C.muted,
                      marginTop: 14,
                    }}
                  >
                    {s.merge.d}
                  </div>
                )}
              </Panel>
            </div>
          </div>
        )}
      </div>
      {s.loop && f >= loopT && (
        <Pop at={loopT} style={{ alignSelf: "center" }}>
          <Chip solid size={34}>
            {s.loop}
          </Chip>
        </Pop>
      )}
    </Shell>
  );
};

// ---------- TIMELINE ----------
export const Timeline: React.FC<SP> = ({ s, from, len, idx, tin }) => {
  const f = useCurrentFrame();
  const cu = cueMap(s, from);
  const at = Math.round(tin * 0.5);
  const steps = (s.steps || []) as { k: string; d?: string; tone?: string }[];
  const n = steps.length;
  const rev = steps.map((_, i) => rv(cu, i, at + 20 + i * 10));
  let cur = -1;
  rev.forEach((t, i) => {
    if (f >= t) cur = i;
  });
  const fillTo = interpolate(
    sp(f, cur >= 0 ? rev[cur] : 0, 20),
    [0, 1],
    [Math.max(0, cur - 1), Math.max(0, cur)],
  );
  const notes = (s.notes || []) as { t: string; tone?: string }[];
  const span = W - 260;
  const stepW = span / n;
  return (
    <Shell len={len} bg={s.bg || "grid"}>
      <Header s={s} at={at} idx={idx} />
      <div style={{ position: "relative", marginTop: 70, height: 250 }}>
        <div
          style={{
            position: "absolute",
            left: stepW / 2,
            right: stepW / 2,
            top: 38,
            height: 8,
            background: C.line,
            borderRadius: 4,
          }}
        />
        <div
          style={{
            position: "absolute",
            left: stepW / 2,
            top: 38,
            height: 8,
            width:
              n > 1 ? (span - stepW) * (cur < 0 ? 0 : fillTo / (n - 1)) : 0,
            background: `linear-gradient(90deg, ${C.blue}, ${C.cyan})`,
            borderRadius: 4,
            boxShadow: `0 0 20px ${C.cyan}88`,
          }}
        />
        <div style={{ display: "flex" }}>
          {steps.map((st, i) => {
            const on = cur === i;
            const done = cur > i;
            const col = tone(st.tone);
            const pulse = on ? 1 + 0.1 * Math.sin(f / 4) : 1;
            return (
              <Pop
                key={i}
                at={rev[i] - (cu.has(String(i + 1)) ? 0 : 0)}
                style={{ width: stepW, textAlign: "center" }}
              >
                <div
                  style={{
                    width: 84,
                    height: 84,
                    borderRadius: 42,
                    margin: "0 auto",
                    background: on || done ? col : C.surface,
                    border: `4px solid ${on || done ? col : C.line2}`,
                    boxShadow: on ? `0 0 60px ${col}` : "none",
                    transform: `scale(${pulse})`,
                    fontFamily: F.hero,
                    fontWeight: 800,
                    fontSize: 32,
                    lineHeight: "76px",
                    color: on || done ? C.bg : C.muted,
                  }}
                >
                  {i + 1}
                </div>
                <div
                  style={{
                    fontFamily: F.mono,
                    fontWeight: 700,
                    fontSize: n > 6 ? 22 : 26,
                    color: on ? col : done ? C.text : C.muted,
                    marginTop: 22,
                    padding: "0 6px",
                    lineHeight: 1.25,
                  }}
                >
                  {st.k}
                </div>
                {st.d && (
                  <div
                    style={{
                      fontFamily: F.body,
                      fontSize: n > 6 ? 21 : 24,
                      color: C.muted,
                      marginTop: 8,
                      padding: "0 8px",
                      lineHeight: 1.3,
                    }}
                  >
                    {st.d}
                  </div>
                )}
              </Pop>
            );
          })}
        </div>
      </div>
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: 20,
          justifyContent: "center",
          marginTop: 34,
        }}
      >
        {notes.map((nt, i) => {
          const a = cu.at("n" + (i + 1), 99999);
          return f >= a - 2 ? (
            <Pop key={i} at={a}>
              <Note text={nt.t} color={tone(nt.tone || "warn")} size={30} />
            </Pop>
          ) : null;
        })}
      </div>
    </Shell>
  );
};

// ---------- STEPS (documented UI path, not a screenshot) ----------
export const Steps: React.FC<SP> = ({ s, from, len, idx, tin }) => {
  const f = useCurrentFrame();
  const cu = cueMap(s, from);
  const at = Math.round(tin * 0.5);
  const steps = (s.steps || []) as { h: string; path?: string[]; d?: string }[];
  const n = steps.length;
  const has = steps.map((_, i) => cu.has(String(i + 1)));
  const rev = steps.map((_, i) => rv(cu, i, at + 22 + i * 8));
  const act = activeIdx(f, rev, has, len);
  // Fit the list into the safe area (above the caption band): estimate the
  // stacked height, switch to two columns when one column would need heavy
  // shrinking, then scale every size by k so nothing reaches the captions.
  const AVAIL = 556;
  const est = (cols: number, k: number) => {
    const colW = cols === 1 ? 1660 : 818;
    const inner = colW - 146;
    const hs = steps.map((st) => {
      const tf = 40 * k;
      const pf = 23 * k;
      const df = 26 * k;
      let h = 44 * k + Math.ceil((st.h.length * tf * 0.55) / inner) * tf * 1.12;
      if (st.path && st.path.length) {
        const pw =
          st.path.reduce((a, p) => a + p.length * pf * 0.62 + 34 * k, 0) +
          (st.path.length - 1) * 36 * k;
        h += 10 * k + Math.ceil(pw / inner) * (pf * 1.25 + 16 * k + 12 * k);
      }
      if (st.d) h += 8 * k + Math.ceil((st.d.length * df * 0.52) / inner) * df * 1.3;
      return h;
    });
    const half = Math.ceil(n / 2);
    const groups = cols === 1 ? [hs] : [hs.slice(0, half), hs.slice(half)];
    return Math.max(
      ...groups.map((g) => g.reduce((a, b) => a + b, 0) + (g.length - 1) * 18 * k),
    );
  };
  const fitK = (cols: number) => {
    let k = 1;
    for (let it = 0; it < 8; it++) {
      const h = est(cols, k);
      if (h <= AVAIL) break;
      k *= Math.max(0.85, AVAIL / h);
    }
    return Math.max(0.62, k);
  };
  const k1 = fitK(1);
  const cols = k1 >= 0.86 || n < 3 ? 1 : 2;
  const k = cols === 1 ? k1 : Math.min(1, fitK(2));
  const half = Math.ceil(n / 2);
  return (
    <Shell len={len} bg={s.bg || "grid"}>
      <Header s={s} at={at} idx={idx} />
      <div
        style={{
          display: "grid",
          gridTemplateColumns: cols === 1 ? "1fr" : "1fr 1fr",
          gridTemplateRows: cols === 1 ? undefined : `repeat(${half}, auto)`,
          gridAutoFlow: cols === 1 ? "row" : "column",
          columnGap: 24,
          rowGap: 18 * k,
          marginTop: 34 * k,
          alignContent: "start",
        }}
      >
        {steps.map((st, i) => {
          const on = act === i;
          const done = has[i] && f >= rev[i] && !on;
          return (
            <Pop key={i} at={rev[i]} dx={-80} dy={0}>
              <Panel
                active={on}
                style={{ padding: `${22 * k}px ${30 * k}px`, height: cols === 2 ? "100%" : undefined }}
              >
                <div style={{ display: "flex", alignItems: "center", gap: 26 * k }}>
                  <div
                    style={{
                      width: 60 * k,
                      height: 60 * k,
                      borderRadius: 30 * k,
                      flexShrink: 0,
                      background: on ? C.cyan : done ? C.blue : C.surface2,
                      color: on || done ? C.bg : C.muted,
                      fontFamily: F.hero,
                      fontWeight: 800,
                      fontSize: 26 * k,
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      boxShadow: on ? `0 0 24px ${C.cyan}88` : "none",
                    }}
                  >
                    {i + 1}
                  </div>
                  <div style={{ flex: 1 }}>
                    <div
                      style={{
                        fontFamily: F.head,
                        fontWeight: 700,
                        fontSize: 40 * k,
                        color: on ? C.cyan : C.text,
                        lineHeight: 1.12,
                      }}
                    >
                      {st.h}
                    </div>
                    {st.path && st.path.length > 0 && (
                      <div
                        style={{
                          display: "flex",
                          alignItems: "center",
                          gap: 12 * k,
                          rowGap: 8 * k,
                          marginTop: 10 * k,
                          flexWrap: "wrap",
                        }}
                      >
                        {st.path.map((pth, j) => {
                          const tj = rev[i] + 10 + j * 14;
                          const lit = on && f >= tj;
                          const click = on && f >= tj && f < tj + 10;
                          return (
                            <React.Fragment key={j}>
                              {j > 0 && (
                                <span
                                  style={{
                                    fontFamily: F.mono,
                                    fontSize: 26 * k,
                                    color: C.dim,
                                  }}
                                >
                                  ›
                                </span>
                              )}
                              <div style={{ position: "relative" }}>
                                <div
                                  style={{
                                    fontFamily: F.mono,
                                    fontWeight: 700,
                                    fontSize: 23 * k,
                                    color: lit ? C.bg : C.text,
                                    background: lit
                                      ? C.cyan
                                      : "rgba(18,28,52,0.9)",
                                    border: `2px solid ${lit ? C.cyan : C.line2}`,
                                    borderRadius: 10 * k,
                                    padding: `${5 * k}px ${14 * k}px`,
                                  }}
                                >
                                  {pth}
                                </div>
                                {click && (
                                  <div
                                    style={{
                                      position: "absolute",
                                      right: -10,
                                      bottom: -10,
                                      width: 34,
                                      height: 34,
                                      borderRadius: 17,
                                      border: `3px solid ${C.cyan}`,
                                      transform: `scale(${0.4 + (f - tj) / 8})`,
                                      opacity: 1 - (f - tj) / 10,
                                    }}
                                  />
                                )}
                              </div>
                            </React.Fragment>
                          );
                        })}
                      </div>
                    )}
                    {st.d && (
                      <div
                        style={{
                          fontFamily: F.body,
                          fontSize: 26 * k,
                          color: on ? "#C9D6F2" : C.muted,
                          marginTop: 8 * k,
                          lineHeight: 1.3,
                        }}
                      >
                        {st.d}
                      </div>
                    )}
                  </div>
                </div>
              </Panel>
            </Pop>
          );
        })}
      </div>
    </Shell>
  );
};

// ---------- CODE ----------
const TOK =
  /(^\s*#.*$|\s#\s.*$|\/\/\s.*$)|("(?:[^"\\]|\\.)*"(?=\s*:))|("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')|(\$\{?\w+\}?|\{\{\w+\}\})|(https?:\/\/[^\s"']+)|(\s--?[A-Za-z][\w-]*)|\b(\d+(?:\.\d+)?)\b|\b(curl|const|let|await|async|import|from|def|return|if|else|true|false|null|None|True|False|export|function|POST|GET|PATCH|PUT|DELETE|print|for|in|of|new|json)\b/g;
const TOKC = [
  C.dim,
  C.cyan,
  "#8FE3B0",
  C.amber,
  "#8FE3B0",
  "#7FA8FF",
  C.amber,
  "#B79CFF",
];
const tokenize = (line: string) => {
  const out: { t: string; c: string }[] = [];
  const re = new RegExp(TOK.source, "g");
  let last = 0;
  let m: RegExpExecArray | null;
  while ((m = re.exec(line)) !== null) {
    if (m[0].length === 0) {
      re.lastIndex++;
      continue;
    }
    if (m.index > last) out.push({ t: line.slice(last, m.index), c: C.text });
    let g = 0;
    for (let k = 1; k < m.length; k++) {
      if (m[k] !== undefined) {
        g = k - 1;
        break;
      }
    }
    out.push({ t: m[0], c: TOKC[g] });
    last = m.index + m[0].length;
  }
  if (last < line.length) out.push({ t: line.slice(last), c: C.text });
  return out;
};

// markdown/plain text: only highlight {{variables}}
const tokenizeMd = (line: string) => {
  const out: { t: string; c: string }[] = [];
  const re = /\{\{\w+\}\}/g;
  let last = 0;
  let m: RegExpExecArray | null;
  while ((m = re.exec(line)) !== null) {
    if (m.index > last) out.push({ t: line.slice(last, m.index), c: C.text });
    out.push({ t: m[0], c: C.amber });
    last = m.index + m[0].length;
  }
  if (last < line.length) out.push({ t: line.slice(last), c: C.text });
  return out;
};

const Window: React.FC<{
  label: string;
  children: React.ReactNode;
  style?: React.CSSProperties;
  dark?: boolean;
}> = ({ label, children, style, dark }) => (
  <div
    style={{
      background: dark ? "rgba(3,5,10,0.96)" : "rgba(8,12,24,0.96)",
      border: `2px solid ${C.line2}`,
      borderRadius: 18,
      overflow: "hidden",
      boxShadow: "0 30px 80px rgba(0,0,0,0.55)",
      ...style,
    }}
  >
    <div
      style={{
        height: 52,
        display: "flex",
        alignItems: "center",
        gap: 10,
        padding: "0 20px",
        background: "rgba(20,30,54,0.9)",
        borderBottom: `2px solid ${C.line}`,
      }}
    >
      {[C.line2, C.line2, C.line2].map((c, i) => (
        <div
          key={i}
          style={{ width: 14, height: 14, borderRadius: 7, background: c }}
        />
      ))}
      <div
        style={{
          marginLeft: 16,
          fontFamily: F.mono,
          fontSize: 22,
          color: C.muted,
        }}
      >
        {label}
      </div>
    </div>
    {children}
  </div>
);

export const Code: React.FC<SP> = ({ s, from, len, idx, tin }) => {
  const f = useCurrentFrame();
  const cu = cueMap(s, from);
  const at = Math.round(tin * 0.5);
  const lines = String(s.code || "").split("\n");
  const hl = (s.hl || []) as { l: number[]; note?: string; tone?: string }[];
  const has = hl.map((_, i) => cu.has(String(i + 1)));
  const rev = hl.map((_, i) => rv(cu, i, 99999));
  const act = activeIdx(f, rev, has, len);
  const total = lines.reduce((a, l) => a + l.length + 1, 0);
  const t0 = at + (s.title ? 18 : 10);
  const rate = Math.max(2.5, total / 50);
  const shown = Math.max(0, (f - t0) * rate);
  const lh = 37;
  const vis = s.title ? 13 : 16;
  const tops = hl.map((h) =>
    Math.max(0, Math.min(lines.length - vis, h.l[0] - 3)),
  );
  let top = 0;
  if (lines.length > vis) {
    top = 0;
    for (let i = 0; i < hl.length; i++) {
      if (has[i] && f >= rev[i])
        top = interpolate(
          sp(f, rev[i], 20),
          [0, 1],
          [i > 0 ? tops[i - 1] : 0, tops[i]],
        );
    }
  }
  const notes = hl
    .map((h, i) => ({ ...h, i }))
    .filter((h) => h.note && has[h.i] && f >= rev[h.i] - 2);
  let acc = 0;
  return (
    <Shell len={len} bg={s.bg || "dots"}>
      <Header s={s} at={at} idx={idx} />
      <div
        style={{
          display: "flex",
          gap: 30,
          marginTop: 30,
          alignItems: "flex-start",
        }}
      >
        <Pop at={at + 8} dy={60} style={{ flex: 1 }}>
          <Window label={s.file || "request"}>
            <div
              style={{
                height: vis * lh + 28,
                overflow: "hidden",
                position: "relative",
              }}
            >
              <div
                style={{
                  transform: `translateY(${-top * lh}px)`,
                  padding: "14px 0",
                }}
              >
                {lines.map((ln, li) => {
                  const startC = acc;
                  acc += ln.length + 1;
                  const n = Math.max(0, Math.min(ln.length, shown - startC));
                  const inHl =
                    act >= 0 &&
                    li + 1 >= hl[act].l[0] &&
                    li + 1 <= hl[act].l[1];
                  const dim = act >= 0 && !inHl;
                  const col = act >= 0 ? tone(hl[act].tone) : C.cyan;
                  const toks =
                    s.lang === "md" && ln.trim().startsWith("#")
                      ? [{ t: ln.slice(0, n), c: C.cyan }]
                      : s.lang === "md"
                        ? [{ t: ln.slice(0, n), c: C.text }].flatMap((x) =>
                            tokenizeMd(x.t),
                          )
                        : tokenize(ln.slice(0, n));
                  return (
                    <div
                      key={li}
                      style={{
                        display: "flex",
                        height: lh,
                        alignItems: "center",
                        background: inHl ? `${col}1A` : "transparent",
                        borderLeft: `4px solid ${inHl ? col : "transparent"}`,
                        opacity: dim ? 0.32 : 1,
                      }}
                    >
                      <span
                        style={{
                          width: 62,
                          textAlign: "right",
                          paddingRight: 18,
                          fontFamily: F.mono,
                          fontSize: 20,
                          color: C.dim,
                        }}
                      >
                        {li + 1}
                      </span>
                      <span
                        style={{
                          fontFamily: F.mono,
                          fontSize: 24,
                          whiteSpace: "pre",
                        }}
                      >
                        {toks.map((tk, k) => (
                          <span key={k} style={{ color: tk.c }}>
                            {tk.t}
                          </span>
                        ))}
                        {n < ln.length && n > 0 && shown < total && (
                          <span style={{ background: C.cyan, color: C.cyan }}>
                            ▌
                          </span>
                        )}
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>
          </Window>
        </Pop>
        {hl.some((h) => h.note) && (
          <div
            style={{
              width: 470,
              display: "flex",
              flexDirection: "column",
              gap: 16,
            }}
          >
            {notes.map((h) => (
              <Pop key={h.i} at={rev[h.i]} dx={60} dy={0}>
                <Panel
                  active={act === h.i}
                  color={tone(h.tone)}
                  style={{ padding: "18px 24px" }}
                >
                  <div
                    style={{
                      fontFamily: F.mono,
                      fontWeight: 700,
                      fontSize: 20,
                      color: tone(h.tone),
                    }}
                  >
                    {h.l[0] === h.l[1]
                      ? `LINE ${h.l[0]}`
                      : `LINES ${h.l[0]}–${h.l[1]}`}
                  </div>
                  <div
                    style={{
                      fontFamily: F.body,
                      fontSize: 26,
                      color: C.text,
                      marginTop: 6,
                      lineHeight: 1.32,
                    }}
                  >
                    {h.note}
                  </div>
                </Panel>
              </Pop>
            ))}
          </div>
        )}
      </div>
    </Shell>
  );
};

// ---------- TERMINAL ----------
export const Terminal: React.FC<SP> = ({ s, from, len, idx, tin }) => {
  const f = useCurrentFrame();
  const cu = cueMap(s, from);
  const at = Math.round(tin * 0.5);
  const cmds = (s.cmds || []) as { c: string; out?: string[] }[];
  const rows: { t: string; kind: "cmd" | "out"; caret: boolean }[] = [];
  cmds.forEach((cm, i) => {
    const t = rv(cu, i, at + 16 + i * 60);
    if (f < t) return;
    const typed = Math.min(cm.c.length, Math.floor((f - t) * 1.7));
    rows.push({
      t: cm.c.slice(0, typed),
      kind: "cmd",
      caret: typed < cm.c.length,
    });
    const done = t + cm.c.length / 1.7 + 6;
    (cm.out || []).forEach((o, j) => {
      if (f >= done + j * 4) rows.push({ t: o, kind: "out", caret: false });
    });
  });
  const vis = 13;
  const top = Math.max(0, rows.length - vis);
  return (
    <Shell len={len} bg={s.bg || "dots"}>
      <Header s={s} at={at} idx={idx} />
      <Pop at={at + 8} dy={60} style={{ marginTop: 30 }}>
        <Window label={s.file || "terminal"} dark>
          <div
            style={{
              height: vis * 40 + 30,
              padding: "16px 30px",
              overflow: "hidden",
            }}
          >
            {rows.slice(top).map((r, i) => (
              <div
                key={i}
                style={{
                  fontFamily: F.mono,
                  fontSize: 25,
                  height: 40,
                  whiteSpace: "pre",
                  color: r.kind === "cmd" ? C.text : C.muted,
                }}
              >
                {r.kind === "cmd" && <span style={{ color: C.cyan }}>❯ </span>}
                {r.t}
                {r.caret && Math.floor(f / 8) % 2 === 0 && (
                  <span style={{ color: C.cyan }}>▌</span>
                )}
              </div>
            ))}
          </div>
        </Window>
      </Pop>
    </Shell>
  );
};

// ---------- COMPARE ----------
export const Compare: React.FC<SP> = ({ s, from, len, idx, tin }) => {
  const f = useCurrentFrame();
  const cu = cueMap(s, from);
  const at = Math.round(tin * 0.5);
  const rows = (s.rows || []) as { l: string; r: string }[];
  const rev = rows.map((_, i) => rv(cu, i, at + 26 + i * 8));
  const rrev = rows.map((_, i) =>
    cu.has("r" + (i + 1))
      ? cu.at("r" + (i + 1), 0)
      : cu.has("r")
        ? cu.at("r", 0) + i * cu.stg
        : rev[i] + 6,
  );
  const side = (key: "l" | "r") => {
    const hd = key === "l" ? s.left : s.right;
    const col = tone(hd.tone || (key === "l" ? "muted" : "cyan"));
    return (
      <Pop at={at + 12} dx={key === "l" ? -80 : 80} dy={0} style={{ flex: 1 }}>
        <Panel active={key === "r"} color={col} style={{ height: "100%" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
            {hd.icon && <Icon name={hd.icon} size={54} color={col} />}
            <div
              style={{
                fontFamily: F.hero,
                fontWeight: 800,
                fontSize: 40,
                color: col,
              }}
            >
              {hd.h}
            </div>
          </div>
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              gap: 18,
              marginTop: 26,
            }}
          >
            {rows.map((r, i) => (
              <Pop
                key={i}
                at={key === "r" ? rrev[i] : rev[i]}
                dx={key === "l" ? -30 : 30}
                dy={0}
              >
                <div
                  style={{ display: "flex", gap: 16, alignItems: "flex-start" }}
                >
                  <div
                    style={{
                      width: 12,
                      height: 12,
                      borderRadius: 6,
                      background: col,
                      marginTop: 13,
                      flexShrink: 0,
                    }}
                  />
                  <div
                    style={{
                      fontFamily: F.body,
                      fontSize: 30,
                      color: C.text,
                      lineHeight: 1.32,
                    }}
                  >
                    {r[key]}
                  </div>
                </div>
              </Pop>
            ))}
          </div>
        </Panel>
      </Pop>
    );
  };
  const vs = sp(f, at + 18, 10);
  return (
    <Shell len={len} bg={s.bg || "grid"}>
      <Header s={s} at={at} idx={idx} />
      <div
        style={{
          display: "flex",
          gap: 40,
          marginTop: 40,
          flex: 1,
          position: "relative",
        }}
      >
        {side("l")}
        {side("r")}
        <div
          style={{
            position: "absolute",
            left: "50%",
            top: "42%",
            transform: `translate(-50%, -50%) scale(${vs}) rotate(${(1 - vs) * 90}deg)`,
            width: 92,
            height: 92,
            borderRadius: 46,
            background: C.bg,
            border: `3px solid ${C.cyan}`,
            fontFamily: F.hero,
            fontWeight: 800,
            fontSize: 30,
            color: C.cyan,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            boxShadow: `0 0 40px ${C.cyan}77`,
          }}
        >
          VS
        </div>
      </div>
    </Shell>
  );
};

// ---------- STAT ----------
export const Stat: React.FC<SP> = ({ s, from, len, idx, tin }) => {
  const f = useCurrentFrame();
  const cu = cueMap(s, from);
  const at = Math.round(tin * 0.5);
  const t = cu.at("s", at + 20);
  const p = lerp(f, t, t + 42, 0, 1, EXPO);
  const val = Number(s.value || 0);
  const dec = Number(s.decimals || 0);
  const shown = (val * p).toFixed(dec);
  const numLen = val.toFixed(dec).length + 0.42 * String(s.unit || "").length;
  const numSize = Math.max(110, Math.min(250, (250 * 4.2) / Math.max(4.2, numLen)));
  const ct = cu.at("c", t + 50);
  const r = 362;
  const circ = 2 * Math.PI * r;
  return (
    <Shell len={len} bg={s.bg || "rings"} center>
      <svg
        width={900}
        height={900}
        style={{ position: "absolute", left: W / 2 - 450, top: H / 2 - 490 }}
      >
        <circle
          cx={450}
          cy={450}
          r={r}
          fill="none"
          stroke={C.line}
          strokeWidth={10}
        />
        <circle
          cx={450}
          cy={450}
          r={r}
          fill="none"
          stroke={C.cyan}
          strokeWidth={10}
          strokeLinecap="round"
          strokeDasharray={circ}
          strokeDashoffset={circ * (1 - p * Number(s.gauge || 0.78))}
          transform="rotate(-90 450 450)"
          style={{ filter: `drop-shadow(0 0 14px ${C.cyan})` }}
        />
      </svg>
      <Kicker
        text={s.kicker || s.label}
        at={at}
        index={pad2(idx)}
        align="center"
      />
      {s.prefix && (
        <div
          style={{
            fontFamily: F.mono,
            fontWeight: 700,
            fontSize: 36,
            color: C.muted,
            letterSpacing: 6,
            marginTop: 30,
            opacity: lerp(f, t - 6, t + 6),
          }}
        >
          {s.prefix}
        </div>
      )}
      <div
        style={{
          fontFamily: F.hero,
          fontWeight: 800,
          fontSize: numSize,
          lineHeight: 1,
          color: C.cyan,
          textShadow: `0 0 70px ${C.blue}`,
          opacity: lerp(f, t - 6, t + 4),
        }}
      >
        {shown}
        {s.unit && (
          <span style={{ fontSize: Math.round(numSize * 0.42), color: C.text }}> {s.unit}</span>
        )}
      </div>
      {s.title && (
        <Pop at={t + 20}>
          <div
            style={{
              fontFamily: F.head,
              fontWeight: 700,
              fontSize: 50,
              color: C.text,
              marginTop: 26,
              textAlign: "center",
            }}
          >
            {s.title}
          </div>
        </Pop>
      )}
      {s.caveat && f >= ct - 2 && (
        <Pop at={ct} style={{ marginTop: 28 }}>
          <Chip color={C.amber} size={30}>
            {s.caveat}
          </Chip>
        </Pop>
      )}
    </Shell>
  );
};

// ---------- CHECKLIST ----------
export const Checklist: React.FC<SP> = ({ s, from, len, idx, tin }) => {
  const f = useCurrentFrame();
  const cu = cueMap(s, from);
  const at = Math.round(tin * 0.5);
  const items = (s.items || []) as (string | { t: string; tone?: string })[];
  const two = items.length > 5;
  return (
    <Shell len={len} bg={s.bg || "grid"}>
      <Header s={s} at={at} idx={idx} />
      <div
        style={{
          display: "grid",
          gridTemplateColumns: two ? "1fr 1fr" : "1fr",
          gap: two ? "18px 40px" : 20,
          marginTop: 40,
        }}
      >
        {items.map((it, i) => {
          const txt = typeof it === "string" ? it : it.t;
          const col = tone(
            typeof it === "string" ? undefined : it.tone || "ok",
          );
          const a = rv(cu, i, at + 24 + i * 7);
          const p = lerp(f, a + 4, a + 18, 0, 1, EXPO);
          return (
            <Pop key={i} at={a} dx={-60} dy={0}>
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 24,
                  background: "rgba(14,22,40,0.75)",
                  border: `2px solid ${p > 0.5 ? col + "88" : C.line}`,
                  borderRadius: 18,
                  padding: "16px 26px",
                }}
              >
                <Icon
                  name="check"
                  size={two ? 50 : 60}
                  color={col}
                  draw={p}
                  sw={3}
                />
                <div
                  style={{
                    fontFamily: F.head,
                    fontWeight: 700,
                    fontSize: two ? 34 : 42,
                    color: C.text,
                    lineHeight: 1.15,
                  }}
                >
                  {txt}
                </div>
              </div>
            </Pop>
          );
        })}
      </div>
    </Shell>
  );
};

// ---------- CALLOUT ----------
export const CalloutScene: React.FC<SP> = ({ s, from, len, idx, tin }) => {
  const f = useCurrentFrame();
  const cu = cueMap(s, from);
  const at = Math.round(tin * 0.5);
  const col = tone(s.tone || "warn");
  const icon =
    s.icon ||
    (s.tone === "ok"
      ? "check"
      : s.tone === "tip" || s.tone === "cyan"
        ? "bulb"
        : "alert");
  const bt = cu.at("1", at + 26);
  const ct = cu.at("2", bt + 30);
  return (
    <Shell len={len} bg={s.bg || "floor"} center>
      <Pop at={at + 4} dy={80} flip>
        <div
          style={{
            position: "relative",
            width: 1440,
            padding: "56px 70px",
            borderRadius: 30,
            background:
              "linear-gradient(160deg, rgba(22,32,58,0.96), rgba(8,12,24,0.96))",
            border: `3px solid ${col}`,
            boxShadow: `0 0 90px ${col}44`,
          }}
        >
          <Brackets color={col} inset={16} len={34} />
          <div style={{ display: "flex", gap: 40, alignItems: "flex-start" }}>
            <Icon
              name={icon}
              size={130}
              color={col}
              draw={lerp(f, at + 8, at + 34, 0, 1, EXPO)}
              sw={2.6}
            />
            <div style={{ flex: 1 }}>
              <Kicker
                text={s.kicker || s.label}
                at={at + 4}
                index={pad2(idx)}
                color={col}
              />
              <div style={{ marginTop: 18 }}>
                <Headline
                  text={s.title || ""}
                  fx={s.fx || (s.tone === "warn" ? "glitch" : "split")}
                  at={at + 10}
                  size={fit(s.title || "", 66, 24, 46)}
                  font={F.hero}
                  weight={800}
                  accent={s.accent || []}
                />
              </div>
              {s.body && (
                <Pop at={bt}>
                  <div
                    style={{
                      fontFamily: F.body,
                      fontSize: 36,
                      color: C.muted,
                      marginTop: 22,
                      lineHeight: 1.4,
                    }}
                  >
                    {s.body}
                  </div>
                </Pop>
              )}
              {s.code && f >= ct - 2 && (
                <Pop at={ct} style={{ marginTop: 24 }}>
                  <div
                    style={{
                      display: "inline-block",
                      fontFamily: F.mono,
                      fontWeight: 700,
                      fontSize: 32,
                      color: col,
                      background: "rgba(3,5,10,0.9)",
                      border: `2px solid ${col}66`,
                      borderRadius: 12,
                      padding: "12px 22px",
                    }}
                  >
                    {s.code}
                  </div>
                </Pop>
              )}
            </div>
          </div>
        </div>
      </Pop>
    </Shell>
  );
};

// ---------- GRAPH ----------
export const Graph: React.FC<SP> = ({ s, from, len, idx, tin }) => {
  const f = useCurrentFrame();
  const cu = cueMap(s, from);
  const at = Math.round(tin * 0.5);
  const nodes = (s.nodes || []) as {
    id: string;
    h: string;
    x: number;
    y: number;
    tone?: string;
    icon?: string;
  }[];
  const edges = (s.edges || []) as [string, string, string?][];
  const top = s.title ? 360 : 290;
  const hgt = H - top - 210;
  const pos: Record<
    string,
    { x: number; y: number; t: number; tone?: string }
  > = {};
  nodes.forEach((nd, i) => {
    pos[nd.id] = {
      x: 130 + 120 + (nd.x / 100) * (W - 260 - 240),
      y: top + 40 + (nd.y / 100) * (hgt - 80),
      t: cu.has(nd.id)
        ? cu.at(nd.id, 0)
        : cu.has("all")
          ? cu.at("all", 0) + i * cu.stg
          : at + 24 + i * 8,
      tone: nd.tone,
    };
  });
  const bez = (a: { x: number; y: number }, b: { x: number; y: number }) => {
    const mx = (a.x + b.x) / 2;
    return {
      d: `M${a.x} ${a.y} C${mx} ${a.y}, ${mx} ${b.y}, ${b.x} ${b.y}`,
      c1: { x: mx, y: a.y },
      c2: { x: mx, y: b.y },
    };
  };
  const pt = (
    a: { x: number; y: number },
    b: { x: number; y: number },
    t: number,
  ) => {
    const { c1, c2 } = bez(a, b);
    const u = 1 - t;
    return {
      x:
        u * u * u * a.x +
        3 * u * u * t * c1.x +
        3 * u * t * t * c2.x +
        t * t * t * b.x,
      y:
        u * u * u * a.y +
        3 * u * u * t * c1.y +
        3 * u * t * t * c2.y +
        t * t * t * b.y,
    };
  };
  const path = (s.path || []) as string[];
  const goT = cu.at("go", Math.max(...nodes.map((nd) => pos[nd.id].t)) + 20);
  let packet: { x: number; y: number } | null = null;
  let litNode = "";
  if (path.length > 1 && f >= goT) {
    const segs = path.length - 1;
    const per = 22;
    const k = Math.floor((f - goT) / per) % (segs + 1);
    if (k < segs) {
      const t = ((f - goT) % per) / per;
      const a = pos[path[k]];
      const b = pos[path[k + 1]];
      if (a && b) packet = pt(a, b, EXPO(t));
      litNode = path[k + 1];
    } else litNode = path[segs];
  }
  return (
    <Shell len={len} bg={s.bg || "dots"}>
      <Header s={s} at={at} idx={idx} />
      <svg
        width={W}
        height={H}
        style={{ position: "absolute", left: 0, top: 0 }}
      >
        {edges.map(([a, b, lab], i) => {
          const A = pos[a];
          const B = pos[b];
          if (!A || !B) return null;
          const t0 = Math.max(A.t, B.t);
          const p = lerp(f, t0, t0 + 16, 0, 1, EXPO);
          const { d } = bez(A, B);
          const mid = pt(A, B, 0.5);
          return (
            <g key={i}>
              <path
                d={d}
                fill="none"
                stroke={C.line2}
                strokeWidth={4}
                pathLength={1}
                strokeDasharray={1}
                strokeDashoffset={1 - p}
              />
              <path
                d={d}
                fill="none"
                stroke={C.cyan}
                strokeWidth={2}
                strokeOpacity={0.5}
                pathLength={1}
                strokeDasharray="0.02 0.03"
                strokeDashoffset={-f * 0.004}
                style={{ opacity: p }}
              />
              {lab && p > 0.6 && (
                <g transform={`translate(${mid.x}, ${mid.y})`}>
                  <rect
                    x={-lab.length * 7.5 - 14}
                    y={-18}
                    width={lab.length * 15 + 28}
                    height={36}
                    rx={18}
                    fill={C.bg}
                    stroke={C.line2}
                    strokeWidth={2}
                  />
                  <text
                    x={0}
                    y={7}
                    textAnchor="middle"
                    fill={C.muted}
                    style={{ fontFamily: F.mono, fontSize: 20 }}
                  >
                    {lab}
                  </text>
                </g>
              )}
            </g>
          );
        })}
        {packet && (
          <circle
            cx={packet.x}
            cy={packet.y}
            r={11}
            fill={C.cyan}
            style={{ filter: `drop-shadow(0 0 12px ${C.cyan})` }}
          />
        )}
      </svg>
      {nodes.map((nd) => {
        const P = pos[nd.id];
        const s2 = sp(f, P.t, 13);
        const col = tone(nd.tone);
        const lit =
          litNode === nd.id || (cu.has(nd.id) && f >= P.t && f < P.t + 40);
        return (
          <div
            key={nd.id}
            style={{
              position: "absolute",
              left: P.x,
              top: P.y,
              transform: `translate(-50%, -50%) scale(${s2})`,
              opacity: Math.min(1, s2 * 1.5),
              display: "flex",
              alignItems: "center",
              gap: 16,
              padding: "19px 30px",
              borderRadius: 20,
              background: lit
                ? `linear-gradient(135deg, ${col}22, rgba(12,19,36,0.97) 70%)`
                : "rgba(12,19,36,0.97)",
              border: `3px solid ${lit ? col : C.line2}`,
              boxShadow: lit
                ? `0 0 46px ${col}88, inset 0 0 18px ${col}33`
                : "0 10px 30px rgba(0,0,0,0.4)",
              whiteSpace: "nowrap",
            }}
          >
            {nd.icon && <Icon name={nd.icon} size={46} color={col} />}
            <span
              style={{
                fontFamily: F.head,
                fontWeight: 700,
                fontSize: 34,
                color: lit ? col : C.text,
              }}
            >
              {nd.h}
            </span>
          </div>
        );
      })}
    </Shell>
  );
};

// ---------- CHIPS (grouped lists) ----------
export const Chips: React.FC<SP> = ({ s, from, len, idx, tin }) => {
  const f = useCurrentFrame();
  const cu = cueMap(s, from);
  const at = Math.round(tin * 0.5);
  const groups = (s.groups || []) as {
    h: string;
    items: string[];
    icon?: string;
    tone?: string;
  }[];
  const has = groups.map((_, i) => cu.has(String(i + 1)));
  const rev = groups.map((_, i) => rv(cu, i, at + 24 + i * 12));
  const act = activeIdx(f, rev, has, len);
  const maxItems = Math.max(...groups.map((g) => g.items.length));
  const cs0 = maxItems <= 2 ? 40 : maxItems <= 4 ? 32 : maxItems <= 6 ? 28 : 25;
  const ng = groups.length;
  const longest = Math.max(...groups.flatMap((g) => g.items.map((x) => x.length)));
  const nc = ng;
  const colW = (1660 - 26 * (nc - 1)) / nc - 76;
  const cs = Math.max(17, Math.min(cs0, Math.floor(colW / (longest * 0.6 + 1.7))));
  return (
    <Shell len={len} bg={s.bg || "grid"}>
      <Header s={s} at={at} idx={idx} />
      <div
        style={{
          display: "grid",
          gridTemplateColumns: `repeat(${nc}, minmax(0, 1fr))`,
          gap: 26,
          marginTop: 30,
          flex: 1,
          alignContent: "center",
        }}
      >
        {groups.map((g, i) => {
          const col = tone(g.tone);
          return (
            <Pop key={i} at={rev[i]} flip dy={60}>
              <Panel active={act === i} color={col} style={{ minHeight: nc < ng ? 0 : 330 }}>
                <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
                  {g.icon && (
                    <Icon
                      name={g.icon}
                      size={ng >= 4 ? 50 : 62}
                      color={col}
                      draw={lerp(f, rev[i], rev[i] + 22, 0, 1, EXPO)}
                    />
                  )}
                  <div
                    style={{
                      fontFamily: F.head,
                      fontWeight: 700,
                      fontSize: ng >= 4 ? 34 : 42,
                      lineHeight: 1.1,
                      color: act === i ? col : C.text,
                    }}
                  >
                    {g.h}
                  </div>
                </div>
                <div
                  style={{
                    display: "flex",
                    flexWrap: "wrap",
                    gap: 12,
                    marginTop: 22,
                  }}
                >
                  {g.items.map((it, j) => (
                    <Pop key={j} at={rev[i] + 8 + j * 3} dy={20}>
                      <Chip size={cs}>{it}</Chip>
                    </Pop>
                  ))}
                </div>
              </Panel>
            </Pop>
          );
        })}
      </div>
    </Shell>
  );
};

// ---------- BARS (illustrative) ----------
export const Bars: React.FC<SP> = ({ s, from, len, idx, tin }) => {
  const f = useCurrentFrame();
  const cu = cueMap(s, from);
  const at = Math.round(tin * 0.5);
  const bars = (s.bars || []) as {
    h: string;
    d?: string;
    v: number;
    tone?: string;
  }[];
  const nt = cu.at("c", at + 40 + bars.length * 20);
  return (
    <Shell len={len} bg={s.bg || "grid"}>
      <Header s={s} at={at} idx={idx} />
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: 28,
          marginTop: 50,
        }}
      >
        {bars.map((b, i) => {
          const a = rv(cu, i, at + 24 + i * 12);
          const w = lerp(f, a, a + 28, 0, b.v, EXPO);
          const col = tone(b.tone);
          return (
            <Pop key={i} at={a} dx={-40} dy={0}>
              <div style={{ display: "flex", alignItems: "center", gap: 30 }}>
                <div style={{ width: 420 }}>
                  <div
                    style={{
                      fontFamily: F.head,
                      fontWeight: 700,
                      fontSize: 40,
                      color: C.text,
                    }}
                  >
                    {b.h}
                  </div>
                  {b.d && (
                    <div
                      style={{
                        fontFamily: F.body,
                        fontSize: 25,
                        color: C.muted,
                        marginTop: 4,
                      }}
                    >
                      {b.d}
                    </div>
                  )}
                </div>
                <div
                  style={{
                    flex: 1,
                    height: 40,
                    background: C.surface,
                    borderRadius: 20,
                    border: `2px solid ${C.line}`,
                    overflow: "hidden",
                  }}
                >
                  <div
                    style={{
                      width: `${w}%`,
                      height: "100%",
                      background: `linear-gradient(90deg, ${col}AA, ${col})`,
                      borderRadius: 20,
                      boxShadow: `0 0 30px ${col}66`,
                    }}
                  />
                </div>
              </div>
            </Pop>
          );
        })}
      </div>
      {s.note && f >= nt - 2 && (
        <Pop at={nt} style={{ marginTop: 34, alignSelf: "flex-start" }}>
          <Note text={s.note} color={C.amber} size={28} />
        </Pop>
      )}
    </Shell>
  );
};

// ---------- TABLE ----------
export const Table: React.FC<SP> = ({ s, from, len, idx, tin }) => {
  const f = useCurrentFrame();
  const cu = cueMap(s, from);
  const at = Math.round(tin * 0.5);
  const cols = (s.cols || []) as string[];
  const rows = (s.rows || []) as string[][];
  const mono = (s.mono || [0]) as number[];
  const has = rows.map((_, i) => cu.has(String(i + 1)));
  const rev = rows.map((_, i) => rv(cu, i, at + 22 + i * 6));
  const act = activeIdx(f, rev, has, len);
  const widths = cols.map((c, j) =>
    Math.max(c.length, ...rows.map((r) => (r[j] || "").length)),
  );
  const sum = widths.reduce((a, b) => a + b, 0);
  const n = rows.length;
  const rh = n <= 3 ? 108 : n === 4 ? 94 : n === 5 ? 84 : n === 6 ? 74 : 64;
  const fsB = n <= 3 ? 34 : n === 4 ? 32 : n === 5 ? 30 : n === 6 ? 28 : 27;
  const shine = ((f - at) % 90) / 90;
  return (
    <Shell len={len} bg={s.bg || "grid"}>
      <Header s={s} at={at} idx={idx} />
      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          paddingBottom: 24,
        }}
      >
      <Pop at={at + 10} dy={50} style={{ marginTop: 24 }}>
        <div
          style={{
            border: `2px solid ${C.line2}`,
            borderRadius: 20,
            overflow: "hidden",
            background: "rgba(8,12,24,0.92)",
            boxShadow: `0 30px 80px rgba(0,0,0,0.45), 0 0 0 1px rgba(53,224,255,0.06)`,
          }}
        >
          <div
            style={{
              display: "flex",
              background:
                "linear-gradient(90deg, rgba(45,123,255,0.22), rgba(20,30,54,0.95) 60%)",
              height: n <= 4 ? 66 : 58,
              alignItems: "center",
              borderBottom: `2px solid ${C.blue}55`,
            }}
          >
            {cols.map((c, j) => (
              <div
                key={j}
                style={{
                  flex: widths[j] / sum,
                  padding: "0 28px",
                  fontFamily: F.mono,
                  fontWeight: 700,
                  fontSize: 22,
                  color: C.cyan,
                  letterSpacing: 2,
                }}
              >
                {c.toUpperCase()}
              </div>
            ))}
          </div>
          {rows.map((r, i) => {
            const on = act === i;
            const vis = lerp(f, rev[i], rev[i] + 8);
            return (
              <div
                key={i}
                style={{
                  display: "flex",
                  height: rh,
                  alignItems: "center",
                  borderTop: `1px solid ${C.line}`,
                  background: on
                    ? `linear-gradient(90deg, rgba(53,224,255,0.04) ${shine * 100 - 30}%, rgba(53,224,255,0.16) ${shine * 100}%, rgba(53,224,255,0.04) ${shine * 100 + 30}%), rgba(53,224,255,0.08)`
                    : i % 2
                      ? "rgba(255,255,255,0.015)"
                      : "transparent",
                  boxShadow: on ? `inset 6px 0 0 ${C.cyan}` : "none",
                  opacity: vis,
                  transform: `translateX(${(1 - vis) * -40}px)`,
                }}
              >
                {r.map((cell, j) => (
                  <div
                    key={j}
                    style={{
                      flex: widths[j] / sum,
                      padding: "0 28px",
                      lineHeight: 1.15,
                      fontFamily: mono.indexOf(j) >= 0 ? F.mono : F.body,
                      fontWeight: mono.indexOf(j) >= 0 ? 700 : j === 0 ? 600 : 400,
                      fontSize: mono.indexOf(j) >= 0 ? fsB - 3 : fsB,
                      color:
                        on && j === 0 ? C.cyan : j === 0 ? C.text : on ? "#C9D6F2" : C.muted,
                    }}
                  >
                    {cell}
                  </div>
                ))}
              </div>
            );
          })}
        </div>
      </Pop>
      </div>
    </Shell>
  );
};

// ---------- SEQUENCE DIAGRAM ----------
export const SequenceScene: React.FC<SP> = ({ s, from, len, idx, tin }) => {
  const f = useCurrentFrame();
  const cu = cueMap(s, from);
  const at = Math.round(tin * 0.5);
  const actors = (s.actors || []) as { h: string; icon?: string }[];
  const msgs = (s.msgs || []) as {
    a: number;
    b: number;
    t: string;
    tone?: string;
  }[];
  const n = actors.length;
  const top = s.title ? 350 : 290;
  const ax = (i: number) => 130 + ((i + 0.5) * (W - 260)) / n;
  const rowH = Math.min(92, (H - top - 300) / Math.max(1, msgs.length));
  return (
    <Shell len={len} bg={s.bg || "grid"}>
      <Header s={s} at={at} idx={idx} />
      <svg
        width={W}
        height={H}
        style={{ position: "absolute", left: 0, top: 0 }}
      >
        <defs>
          <marker
            id="ah"
            viewBox="0 0 10 10"
            refX="8"
            refY="5"
            markerWidth="7"
            markerHeight="7"
            orient="auto-start-reverse"
          >
            <path d="M0 0L10 5L0 10z" fill={C.cyan} />
          </marker>
        </defs>
        {actors.map((_, i) => (
          <line
            key={i}
            x1={ax(i)}
            y1={top + 80}
            x2={ax(i)}
            y2={H - 190}
            stroke={C.line2}
            strokeWidth={3}
            strokeDasharray="10 10"
            opacity={lerp(f, at + 14, at + 30)}
          />
        ))}
        {msgs.map((m, i) => {
          const t = rv(cu, i, at + 30 + i * 18);
          const p = lerp(f, t, t + 16, 0, 1, EXPO);
          const y = top + 130 + i * rowH;
          const x1 = ax(m.a);
          const x2 = ax(m.b);
          const col = tone(m.tone);
          if (p <= 0) return null;
          if (m.a === m.b) {
            return (
              <g key={i} opacity={p}>
                <path
                  d={`M${x1} ${y - 14} h70 v28 h-62`}
                  fill="none"
                  stroke={col}
                  strokeWidth={3}
                  markerEnd="url(#ah)"
                />
                <text
                  x={x1 + 86}
                  y={y + 8}
                  fill={C.text}
                  style={{ fontFamily: F.body, fontSize: 25 }}
                >
                  {m.t}
                </text>
              </g>
            );
          }
          const xe = x1 + (x2 - x1) * p;
          return (
            <g key={i}>
              <line
                x1={x1}
                y1={y}
                x2={xe}
                y2={y}
                stroke={col}
                strokeWidth={3.5}
                markerEnd="url(#ah)"
                style={{ filter: `drop-shadow(0 0 6px ${col})` }}
              />
              <text
                x={(x1 + x2) / 2}
                y={y - 14}
                textAnchor="middle"
                fill={C.text}
                opacity={p}
                style={{ fontFamily: F.body, fontWeight: 600, fontSize: 25 }}
              >
                {m.t}
              </text>
            </g>
          );
        })}
      </svg>
      {actors.map((a, i) => (
        <div
          key={i}
          style={{
            position: "absolute",
            left: ax(i),
            top: top,
            transform: "translateX(-50%)",
          }}
        >
          <Pop at={at + 10 + i * 5}>
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: 12,
                padding: "14px 26px",
                borderRadius: 16,
                background: "rgba(14,22,40,0.96)",
                border: `2px solid ${C.cyan}`,
                whiteSpace: "nowrap",
              }}
            >
              {a.icon && <Icon name={a.icon} size={36} color={C.cyan} />}
              <span
                style={{
                  fontFamily: F.head,
                  fontWeight: 700,
                  fontSize: 30,
                  color: C.text,
                }}
              >
                {a.h}
              </span>
            </div>
          </Pop>
        </div>
      ))}
    </Shell>
  );
};

// ---------- RECAP + END CARD ----------
export const Recap: React.FC<SP> = ({ s, from, len, idx, tin, ep }) => {
  const f = useCurrentFrame();
  const cu = cueMap(s, from);
  const at = Math.round(tin * 0.5);
  const items = (s.items || []) as string[];
  const nx = cu.at("next", len - 140);
  const bye = cu.at("bye", nx + 90);
  const end = f >= nx - 6;
  const fade = lerp(f, len - 26, len - 2, 1, 0);
  return (
    <Shell len={len} bg={end ? "floor" : "grid"} grain={end} center={end}>
      <AbsoluteFill
        style={{
          opacity: fade,
          padding: "150px 130px 178px",
          display: "flex",
          flexDirection: "column",
          justifyContent: end ? "center" : "flex-start",
          alignItems: end ? "center" : "stretch",
        }}
      >
        {!end ? (
          <>
            <Kicker text={s.kicker || "Recap"} at={at} index={pad2(idx)} />
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                gap: 16,
                marginTop: 36,
              }}
            >
              {items.map((it, i) => {
                const a = rv(cu, i, at + 16 + i * 8);
                return (
                  <Pop key={i} at={a} dx={-70} dy={0}>
                    <div
                      style={{ display: "flex", alignItems: "center", gap: 24 }}
                    >
                      <Icon
                        name="check"
                        size={58}
                        color={C.cyan}
                        draw={lerp(f, a + 4, a + 18, 0, 1, EXPO)}
                        sw={3}
                      />
                      <div
                        style={{
                          fontFamily: F.head,
                          fontWeight: 500,
                          fontSize: items.length > 5 ? 46 : 52,
                          color: C.text,
                        }}
                      >
                        {it}
                      </div>
                    </div>
                  </Pop>
                );
              })}
            </div>
          </>
        ) : (
          <>
            <Pop at={nx}>
              <Chip solid size={34}>
                {ep.next
                  ? `NEXT · EPISODE ${pad2(ep.next.n)}`
                  : "SERIES COMPLETE"}
              </Chip>
            </Pop>
            <div style={{ marginTop: 34, maxWidth: 1500 }}>
              <SplitFx
                text={ep.next ? ep.next.title : "Thanks for learning with us"}
                at={nx + 10}
                size={fit(
                  ep.next ? ep.next.title : "Thanks for learning",
                  100,
                  20,
                  64,
                )}
                align="center"
                accent={[]}
              />
            </div>
            <Pop
              at={bye}
              style={{
                display: "flex",
                alignItems: "center",
                gap: 26,
                marginTop: 60,
              }}
            >
              <OmMark size={110} draw={lerp(f, bye, bye + 24, 0, 1, EXPO)} />
              <div>
                <div
                  style={{
                    fontFamily: F.hero,
                    fontWeight: 800,
                    fontSize: 52,
                    color: C.text,
                    letterSpacing: 8,
                  }}
                >
                  OMILABS
                </div>
                <div
                  style={{ fontFamily: F.body, fontSize: 32, color: C.muted }}
                >
                  Created by Omkar Ghate
                </div>
              </div>
            </Pop>
          </>
        )}
      </AbsoluteFill>
    </Shell>
  );
};

export const SCENES: Record<string, React.FC<SP>> = {
  hook: Hook,
  statement: Statement,
  cards: Cards,
  pipeline: Pipeline,
  timeline: Timeline,
  steps: Steps,
  code: Code,
  terminal: Terminal,
  compare: Compare,
  stat: Stat,
  checklist: Checklist,
  callout: CalloutScene,
  graph: Graph,
  chips: Chips,
  bars: Bars,
  table: Table,
  sequence: SequenceScene,
  recap: Recap,
};
