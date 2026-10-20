import React from "react";
import { AbsoluteFill, random, useCurrentFrame } from "remotion";
import { C, H, RAMP, W } from "./theme";
import { Tr } from "./types";

// Exit types where the outgoing segment must sit above the incoming one.
export const OUT_ON_TOP = ["zoom", "split"];

const bell = (p: number) => Math.sin(Math.PI * Math.min(1, Math.max(0, p)));

// Wraps one segment and applies its entry / exit transition styles.
export const TWrap: React.FC<{
  id: string;
  len: number;
  tin: Tr | null;
  tout: Tr | null;
  children: React.ReactNode;
}> = ({ id, len, tin, tout, children }) => {
  const f = useCurrentFrame();
  let side: "in" | "out" | null = null;
  let t: Tr | null = null;
  let p = 0;
  if (tin && f < tin.d) {
    side = "in";
    t = tin;
    p = f / tin.d;
  } else if (tout && f >= len - tout.d) {
    side = "out";
    t = tout;
    p = (f - (len - tout.d)) / tout.d;
  }
  if (!side || !t) return <AbsoluteFill>{children}</AbsoluteFill>;
  const e = RAMP(Math.min(1, Math.max(0, p)));
  const dir = t.dir || 1;
  const fid = id + "-" + side;
  let st: React.CSSProperties = {};
  let defs: React.ReactNode = null;

  switch (t.type) {
    case "whip": {
      const b = 46 * bell(p);
      defs = (
        <filter id={fid} x="-30%" y="0" width="160%" height="100%">
          <feGaussianBlur stdDeviation={`${b} 0`} />
        </filter>
      );
      const x = side === "out" ? -dir * e * W * 0.9 : dir * (1 - e) * W * 0.9;
      st = {
        transform: `translateX(${x}px) skewX(${-dir * 6 * bell(p)}deg)`,
        filter: `url(#${fid})`,
      };
      break;
    }
    case "push": {
      const x = side === "out" ? -dir * e * W : dir * (1 - e) * W;
      st = { transform: `translateX(${x}px) scale(${1 - 0.12 * bell(p)})` };
      break;
    }
    case "zoom": {
      st =
        side === "out"
          ? {
              transform: `scale(${1 + 1.7 * e})`,
              opacity: 1 - Math.pow(e, 1.4),
              filter: `blur(${14 * e}px)`,
            }
          : {
              transform: `scale(${0.58 + 0.42 * e})`,
              opacity: Math.min(1, e * 1.7),
              filter: `blur(${10 * (1 - e)}px)`,
            };
      break;
    }
    case "glitch": {
      const k = Math.floor(f);
      const dx = (random(fid + "d" + k) - 0.5) * 60 * bell(p);
      defs = (
        <filter id={fid} x="-5%" y="0" width="110%" height="100%">
          <feColorMatrix
            in="SourceGraphic"
            type="matrix"
            values="1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0"
            result="r"
          />
          <feOffset in="r" dx={dx} dy="0" result="r2" />
          <feColorMatrix
            in="SourceGraphic"
            type="matrix"
            values="0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 1 0"
            result="g"
          />
          <feColorMatrix
            in="SourceGraphic"
            type="matrix"
            values="0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0"
            result="b"
          />
          <feOffset in="b" dx={-dx} dy="0" result="b2" />
          <feBlend in="r2" in2="g" mode="screen" result="rg" />
          <feBlend in="rg" in2="b2" mode="screen" />
        </filter>
      );
      const visible = side === "out" ? p < 0.5 : p >= 0.5;
      const jx = (random(fid + "j" + k) - 0.5) * 50 * bell(p);
      st = {
        opacity: visible ? 1 : 0,
        filter: `url(#${fid})`,
        transform: `translateX(${jx}px) skewX(${(random(fid + "s" + k) - 0.5) * 8 * bell(p)}deg)`,
      };
      break;
    }
    case "iris": {
      if (side === "in") {
        const r = 2300 * e;
        st = { clipPath: `circle(${r}px at ${W / 2}px ${H / 2}px)` };
      } else {
        st = {
          transform: `scale(${1 - 0.08 * e})`,
          filter: `brightness(${1 - 0.55 * e})`,
        };
      }
      break;
    }
    case "wipe": {
      if (side === "in") {
        const x0 = -460 + (W + 920) * e;
        st = {
          clipPath: `polygon(0px 0px, ${x0}px 0px, ${x0 - 460}px ${H}px, 0px ${H}px)`,
        };
      } else {
        st = {
          transform: `translateX(${-90 * e}px)`,
          filter: `brightness(${1 - 0.4 * e})`,
        };
      }
      break;
    }
    case "shutter": {
      st = { opacity: side === "out" ? (p < 0.5 ? 1 : 0) : p >= 0.5 ? 1 : 0 };
      break;
    }
    case "cube": {
      const a = side === "out" ? -dir * 90 * e : dir * 90 * (1 - e);
      st = {
        transform: `perspective(2600px) rotateY(${a}deg)`,
        transformOrigin:
          side === "out"
            ? dir > 0
              ? "100% 50%"
              : "0% 50%"
            : dir > 0
              ? "0% 50%"
              : "100% 50%",
        filter: `brightness(${1 - (Math.abs(a) / 90) * 0.6})`,
      };
      break;
    }
    case "flash": {
      st =
        side === "out"
          ? { opacity: 1 - e, transform: `scale(${1 + 0.06 * e})` }
          : { opacity: e, transform: `scale(${1.06 - 0.06 * e})` };
      break;
    }
    case "split": {
      if (side === "out") {
        const y = e * 620;
        return (
          <AbsoluteFill>
            <AbsoluteFill
              style={{
                clipPath: "inset(0 0 50% 0)",
                transform: `translateY(${-y}px)`,
              }}
            >
              {children}
            </AbsoluteFill>
            <AbsoluteFill
              style={{
                clipPath: "inset(50% 0 0 0)",
                transform: `translateY(${y}px)`,
              }}
            >
              {children}
            </AbsoluteFill>
          </AbsoluteFill>
        );
      }
      st = {
        transform: `scale(${0.9 + 0.1 * e})`,
        opacity: Math.min(1, 0.4 + e),
      };
      break;
    }
    default:
      st = { opacity: side === "out" ? 1 - e : e };
  }
  return (
    <AbsoluteFill style={st}>
      {defs && (
        <svg width="0" height="0" style={{ position: "absolute" }}>
          <defs>{defs}</defs>
        </svg>
      )}
      {children}
    </AbsoluteFill>
  );
};

// Drawn once over the cut point, above both segments.
export const TransitionOverlay: React.FC<{ t: Tr; seed: string }> = ({
  t,
  seed,
}) => {
  const f = useCurrentFrame();
  const p = Math.min(1, Math.max(0, f / t.d));
  const b = bell(p);
  const dir = t.dir || 1;
  if (t.type === "whip" || t.type === "push") {
    const k = t.type === "whip" ? 1 : 0.45;
    return (
      <AbsoluteFill style={{ pointerEvents: "none", opacity: b * k }}>
        {new Array(18).fill(0).map((_, i) => {
          const y = random(seed + "y" + i) * H;
          const w = 300 + random(seed + "w" + i) * 900;
          const x =
            (dir > 0 ? 1 : -1) *
              ((random(seed + "x" + i) * 2 - 1) * 400 - (p - 0.5) * 2600) +
            W / 2 -
            w / 2;
          return (
            <div
              key={i}
              style={{
                position: "absolute",
                left: x,
                top: y,
                width: w,
                height: 1 + random(seed + "h" + i) * 3,
                background: `linear-gradient(90deg, transparent, ${i % 3 === 0 ? C.cyan : "#FFFFFF"}, transparent)`,
                opacity: 0.25 + random(seed + "o" + i) * 0.5,
              }}
            />
          );
        })}
      </AbsoluteFill>
    );
  }
  if (t.type === "zoom") {
    return (
      <AbsoluteFill style={{ pointerEvents: "none", opacity: b * 0.7 }}>
        {new Array(30).fill(0).map((_, i) => {
          const a = (i / 30) * 360 + random(seed + "a" + i) * 8;
          const len = 300 + random(seed + "l" + i) * 500;
          return (
            <div
              key={i}
              style={{
                position: "absolute",
                left: W / 2,
                top: H / 2,
                width: len,
                height: 2,
                transformOrigin: "0 50%",
                transform: `rotate(${a}deg) translateX(${120 + p * 900}px)`,
                background: `linear-gradient(90deg, transparent, ${i % 2 ? C.cyan : "#FFFFFF"})`,
                opacity: 0.5,
              }}
            />
          );
        })}
        <AbsoluteFill
          style={{
            background: `radial-gradient(circle at 50% 50%, rgba(255,255,255,${0.35 * b}), transparent 35%)`,
          }}
        />
      </AbsoluteFill>
    );
  }
  if (t.type === "glitch") {
    const k = Math.floor(f);
    return (
      <AbsoluteFill style={{ pointerEvents: "none" }}>
        {new Array(12).fill(0).map((_, i) => (
          <div
            key={i}
            style={{
              position: "absolute",
              left: random(seed + k + "x" + i) * W * 0.7,
              top: random(seed + k + "y" + i) * H,
              width: 200 + random(seed + k + "w" + i) * 900,
              height: 4 + random(seed + k + "h" + i) * 50,
              background: [C.cyan, C.blue, C.violet, "#FFFFFF"][i % 4],
              opacity: 0.55 * b,
              mixBlendMode: "screen",
            }}
          />
        ))}
        <AbsoluteFill
          style={{
            backgroundImage:
              "repeating-linear-gradient(0deg, rgba(255,255,255,0.07) 0px, rgba(255,255,255,0.07) 1px, transparent 2px, transparent 4px)",
            opacity: b,
          }}
        />
        {Math.abs(p - 0.5) < 0.06 && (
          <AbsoluteFill style={{ background: "rgba(255,255,255,0.18)" }} />
        )}
      </AbsoluteFill>
    );
  }
  if (t.type === "iris") {
    const r = 2300 * RAMP(p);
    return (
      <svg
        width={W}
        height={H}
        style={{ position: "absolute", left: 0, top: 0, pointerEvents: "none" }}
      >
        <circle
          cx={W / 2}
          cy={H / 2}
          r={r}
          fill="none"
          stroke={C.cyan}
          strokeWidth={6}
          strokeOpacity={1 - p}
        />
        <circle
          cx={W / 2}
          cy={H / 2}
          r={r * 0.92}
          fill="none"
          stroke="#FFFFFF"
          strokeWidth={2}
          strokeOpacity={(1 - p) * 0.6}
        />
      </svg>
    );
  }
  if (t.type === "wipe") {
    const x0 = -460 + (W + 920) * RAMP(p);
    return (
      <AbsoluteFill style={{ pointerEvents: "none" }}>
        <div
          style={{
            position: "absolute",
            top: -100,
            left: x0 - 520,
            width: 140,
            height: H + 200,
            transform: "skewX(-23deg)",
            transformOrigin: "100% 0",
            background: `linear-gradient(90deg, transparent, ${C.blue}, ${C.cyan}, #FFFFFF)`,
            opacity: b,
            boxShadow: `0 0 80px ${C.cyan}`,
          }}
        />
      </AbsoluteFill>
    );
  }
  if (t.type === "shutter") {
    const n = 9;
    return (
      <AbsoluteFill style={{ pointerEvents: "none" }}>
        {new Array(n).fill(0).map((_, i) => {
          const st = i * 0.035;
          const grow = Math.min(1, Math.max(0, (p - st) / 0.32));
          const shrink = Math.min(1, Math.max(0, (p - 0.5 - st) / 0.32));
          const sc = p < 0.5 ? RAMP(grow) : 1 - RAMP(shrink);
          return (
            <div
              key={i}
              style={{
                position: "absolute",
                left: (i * W) / n - 1,
                top: 0,
                width: W / n + 2,
                height: H,
                transform: `scaleY(${sc})`,
                transformOrigin: p < 0.5 ? "50% 0%" : "50% 100%",
                background:
                  i % 2
                    ? `linear-gradient(180deg, ${C.surface2}, ${C.bg})`
                    : `linear-gradient(180deg, ${C.bg2}, ${C.surface})`,
                borderRight: `2px solid ${C.cyan}55`,
              }}
            />
          );
        })}
      </AbsoluteFill>
    );
  }
  if (t.type === "flash") {
    return (
      <AbsoluteFill
        style={{
          pointerEvents: "none",
          opacity: b,
          background: `radial-gradient(ellipse 70% 60% at ${30 + p * 40}% 40%, rgba(255,214,150,0.55), transparent 70%), radial-gradient(ellipse 60% 50% at ${70 - p * 40}% 70%, rgba(53,224,255,0.45), transparent 70%)`,
          mixBlendMode: "screen",
        }}
      >
        <AbsoluteFill style={{ background: `rgba(255,255,255,${0.22 * b})` }} />
      </AbsoluteFill>
    );
  }
  if (t.type === "split") {
    return (
      <AbsoluteFill style={{ pointerEvents: "none" }}>
        <div
          style={{
            position: "absolute",
            left: 0,
            top: H / 2 - 2,
            width: W,
            height: 4,
            background: `linear-gradient(90deg, transparent, ${C.cyan}, #FFFFFF, ${C.cyan}, transparent)`,
            transform: `scaleX(${Math.min(1, p * 4)})`,
            opacity: p < 0.6 ? 1 : 1 - (p - 0.6) / 0.4,
            boxShadow: `0 0 40px ${C.cyan}`,
          }}
        />
      </AbsoluteFill>
    );
  }
  if (t.type === "cube") {
    return (
      <AbsoluteFill
        style={{
          pointerEvents: "none",
          background: `linear-gradient(${dir > 0 ? 90 : 270}deg, transparent 40%, rgba(53,224,255,${0.12 * b}) 50%, transparent 60%)`,
        }}
      />
    );
  }
  return null;
};
