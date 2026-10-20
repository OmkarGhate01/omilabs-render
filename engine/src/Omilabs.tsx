import "@fontsource/space-grotesk/500.css";
import "@fontsource/space-grotesk/700.css";
import "@fontsource/inter/400.css";
import "@fontsource/inter/600.css";
import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
  Easing,
} from "remotion";

export const C = {
  bg: "#070B14",
  surface: "#0F1726",
  line: "#1E2A44",
  blue: "#2D7BFF",
  cyan: "#35E0FF",
  amber: "#FFB547",
  text: "#EAF1FF",
  muted: "#8A9BBD",
};
const HEAD = "'Space Grotesk', sans-serif";
const BODY = "'Inter', sans-serif";
const clamp = {
  extrapolateLeft: "clamp" as const,
  extrapolateRight: "clamp" as const,
};

// Shared dark backdrop: grid plus one blue glow.
export const Backdrop: React.FC<{ glowX?: number; glowY?: number }> = ({
  glowX = 70,
  glowY = 45,
}) => {
  const frame = useCurrentFrame();
  const drift = (frame * 0.25) % 80;
  return (
    <AbsoluteFill style={{ backgroundColor: C.bg }}>
      <AbsoluteFill
        style={{
          backgroundImage: `linear-gradient(${C.line} 1px, transparent 1px), linear-gradient(90deg, ${C.line} 1px, transparent 1px)`,
          backgroundSize: "80px 80px",
          backgroundPosition: `${drift}px ${drift}px`,
          opacity: 0.35,
        }}
      />
      <AbsoluteFill
        style={{
          background: `radial-gradient(circle at ${glowX}% ${glowY}%, rgba(45,123,255,0.38), transparent 45%)`,
        }}
      />
      <AbsoluteFill
        style={{
          background: `radial-gradient(circle at 50% 50%, transparent 55%, ${C.bg} 100%)`,
        }}
      />
    </AbsoluteFill>
  );
};

// Logo mark: ring drawn on, with a three-bar waveform inside.
export const OmilabsMark: React.FC<{ size: number; progress?: number }> = ({
  size,
  progress = 1,
}) => {
  const frame = useCurrentFrame();
  const r = 42;
  const circ = 2 * Math.PI * r;
  const bars = [0.45, 1, 0.65];
  return (
    <svg width={size} height={size} viewBox="0 0 100 100">
      <defs>
        <linearGradient id="omi" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor={C.cyan} />
          <stop offset="1" stopColor={C.blue} />
        </linearGradient>
      </defs>
      <circle
        cx="50"
        cy="50"
        r={r}
        fill="none"
        stroke="url(#omi)"
        strokeWidth="7"
        strokeLinecap="round"
        strokeDasharray={circ}
        strokeDashoffset={circ * (1 - progress * 0.86)}
        transform="rotate(-60 50 50)"
      />
      {bars.map((b, i) => {
        const wobble = 1 + 0.18 * Math.sin(frame / 5 + i * 1.7);
        const h = 34 * b * wobble * progress;
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

// 1. Intro sting (5s)
export const IntroSting: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const draw = interpolate(frame, [5, 45], [0, 1], {
    ...clamp,
    easing: Easing.out(Easing.cubic),
  });
  const pop = spring({ frame: frame - 5, fps, config: { damping: 14 } });
  const word = "OMILABS".split("");
  const out = interpolate(frame, [130, 150], [1, 0], clamp);
  return (
    <AbsoluteFill style={{ opacity: out }}>
      <Backdrop glowX={50} glowY={45} />
      <AbsoluteFill
        style={{ alignItems: "center", justifyContent: "center", gap: 36 }}
      >
        <div style={{ transform: `scale(${0.8 + pop * 0.2})` }}>
          <OmilabsMark size={260} progress={draw} />
        </div>
        <div style={{ display: "flex", gap: 14 }}>
          {word.map((ch, i) => {
            const s = spring({
              frame: frame - 40 - i * 3,
              fps,
              config: { damping: 16 },
            });
            return (
              <span
                key={i}
                style={{
                  fontFamily: HEAD,
                  fontWeight: 700,
                  fontSize: 120,
                  letterSpacing: 10,
                  color: C.text,
                  opacity: s,
                  transform: `translateY(${(1 - s) * 40}px)`,
                }}
              >
                {ch}
              </span>
            );
          })}
        </div>
        <div
          style={{
            fontFamily: BODY,
            fontSize: 34,
            color: C.muted,
            letterSpacing: 2,
            opacity: interpolate(frame, [75, 95], [0, 1], clamp),
          }}
        >
          Practical AI engineering by Omkar Ghate
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// 2. Episode title card (4s)
export const EpisodeTitle: React.FC<{
  episode: string;
  line1: string;
  line2: string;
  series: string;
}> = ({ episode, line1, line2, series }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const reveal = (delay: number) =>
    spring({ frame: frame - delay, fps, config: { damping: 18 } });
  const bar = interpolate(frame, [8, 40], [0, 1], {
    ...clamp,
    easing: Easing.out(Easing.cubic),
  });
  return (
    <AbsoluteFill>
      <Backdrop glowX={78} glowY={40} />
      <AbsoluteFill style={{ padding: "0 140px", justifyContent: "center" }}>
        <div
          style={{
            display: "inline-flex",
            alignSelf: "flex-start",
            fontFamily: HEAD,
            fontWeight: 700,
            fontSize: 34,
            color: C.bg,
            background: C.cyan,
            padding: "10px 24px",
            borderRadius: 10,
            letterSpacing: 3,
            opacity: reveal(4),
          }}
        >
          {episode}
        </div>
        {[line1, line2].map((l, i) => (
          <div key={i} style={{ overflow: "hidden", marginTop: i ? 0 : 36 }}>
            <div
              style={{
                fontFamily: HEAD,
                fontWeight: 700,
                fontSize: 150,
                lineHeight: 1.06,
                color: i ? C.cyan : C.text,
                transform: `translateY(${(1 - reveal(12 + i * 8)) * 170}px)`,
              }}
            >
              {l}
            </div>
          </div>
        ))}
        <div
          style={{
            height: 6,
            width: 520 * bar,
            background: `linear-gradient(90deg, ${C.blue}, ${C.cyan})`,
            borderRadius: 3,
            marginTop: 44,
          }}
        />
        <div
          style={{
            fontFamily: BODY,
            fontWeight: 600,
            fontSize: 38,
            color: C.muted,
            marginTop: 30,
            opacity: reveal(34),
          }}
        >
          {series}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// 3. Listen / Think / Speak loop (10s)
const STEPS = [
  { k: "LISTEN", s: "Speech-to-text", d: "Caller audio becomes text" },
  { k: "THINK", s: "Language model", d: "Reads the text, writes a reply" },
  { k: "SPEAK", s: "Text-to-speech", d: "Reply becomes audio" },
];
export const PipelineLoop: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const start = 40;
  const per = 55;
  const t = Math.max(0, frame - start);
  const active = Math.floor(t / per) % 3;
  const within = (t % per) / per;
  const begun = frame >= start;
  return (
    <AbsoluteFill>
      <Backdrop glowX={50} glowY={55} />
      <AbsoluteFill style={{ alignItems: "center", paddingTop: 110 }}>
        <div
          style={{
            fontFamily: HEAD,
            fontWeight: 700,
            fontSize: 76,
            color: C.text,
            opacity: interpolate(frame, [0, 18], [0, 1], clamp),
          }}
        >
          Every turn of the call
        </div>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            marginTop: 120,
          }}
        >
          {STEPS.map((st, i) => {
            const enter = spring({
              frame: frame - 10 - i * 8,
              fps,
              config: { damping: 16 },
            });
            const on = begun && active === i;
            const glow = on ? 0.5 + 0.5 * Math.sin(within * Math.PI) : 0;
            return (
              <React.Fragment key={st.k}>
                <div
                  style={{
                    width: 440,
                    height: 400,
                    borderRadius: 28,
                    background: C.surface,
                    border: `3px solid ${on ? C.cyan : C.line}`,
                    boxShadow: `0 0 ${90 * glow}px rgba(53,224,255,${0.55 * glow})`,
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "flex-start",
                    padding: "64px 44px 0",
                    opacity: enter,
                    transform: `translateY(${(1 - enter) * 60}px) scale(${1 + 0.04 * glow})`,
                  }}
                >
                  <div
                    style={{
                      fontFamily: BODY,
                      fontWeight: 600,
                      fontSize: 30,
                      color: C.muted,
                    }}
                  >
                    0{i + 1}
                  </div>
                  <div
                    style={{
                      fontFamily: HEAD,
                      fontWeight: 700,
                      fontSize: 92,
                      color: on ? C.cyan : C.text,
                      marginTop: 6,
                    }}
                  >
                    {st.k}
                  </div>
                  <div
                    style={{
                      fontFamily: BODY,
                      fontWeight: 600,
                      fontSize: 36,
                      color: C.text,
                      marginTop: 14,
                    }}
                  >
                    {st.s}
                  </div>
                  <div
                    style={{
                      fontFamily: BODY,
                      fontSize: 30,
                      color: C.muted,
                      marginTop: 10,
                    }}
                  >
                    {st.d}
                  </div>
                </div>
                {i < 2 && (
                  <div
                    style={{
                      width: 110,
                      height: 6,
                      background: C.line,
                      position: "relative",
                      opacity: enter,
                    }}
                  >
                    <div
                      style={{
                        position: "absolute",
                        top: -7,
                        left:
                          begun && active === i
                            ? interpolate(within, [0.55, 1], [0, 90], clamp)
                            : 0,
                        width: 20,
                        height: 20,
                        borderRadius: 10,
                        background: C.cyan,
                        opacity: begun && active === i && within > 0.55 ? 1 : 0,
                      }}
                    />
                  </div>
                )}
              </React.Fragment>
            );
          })}
        </div>
        <div
          style={{
            fontFamily: BODY,
            fontSize: 34,
            color: C.muted,
            marginTop: 90,
            opacity: interpolate(frame, [60, 80], [0, 1], clamp),
          }}
        >
          Caller speaks, the agent replies, and the loop repeats
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// 4. Lower third (4s, transparent-friendly: no backdrop)
export const LowerThird: React.FC<{ name: string; role: string }> = ({
  name,
  role,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const inn = spring({ frame: frame - 5, fps, config: { damping: 18 } });
  const out = interpolate(
    frame,
    [durationInFrames - 18, durationInFrames - 4],
    [1, 0],
    clamp,
  );
  return (
    <AbsoluteFill style={{ justifyContent: "flex-end", padding: 100 }}>
      <div
        style={{
          display: "flex",
          alignSelf: "flex-start",
          opacity: out,
          transform: `translateX(${(1 - inn) * -80}px)`,
        }}
      >
        <div style={{ width: 10, background: C.cyan, borderRadius: 5 }} />
        <div
          style={{
            background: "rgba(15,23,38,0.94)",
            border: `2px solid ${C.line}`,
            borderLeft: "none",
            padding: "22px 40px",
            borderRadius: "0 16px 16px 0",
            opacity: inn,
          }}
        >
          <div
            style={{
              fontFamily: HEAD,
              fontWeight: 700,
              fontSize: 54,
              color: C.text,
            }}
          >
            {name}
          </div>
          <div style={{ fontFamily: BODY, fontSize: 30, color: C.muted }}>
            {role}
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 5. Thumbnail still (1280x720)
export const Thumbnail: React.FC<{
  episode: string;
  line1: string;
  line2: string;
}> = ({ episode, line1, line2 }) => {
  return (
    <AbsoluteFill>
      <Backdrop glowX={76} glowY={50} />
      <AbsoluteFill
        style={{
          flexDirection: "row",
          alignItems: "center",
          padding: "0 64px",
        }}
      >
        <div style={{ flex: 1 }}>
          <div
            style={{
              display: "inline-block",
              fontFamily: HEAD,
              fontWeight: 700,
              fontSize: 34,
              color: C.bg,
              background: C.cyan,
              padding: "8px 20px",
              borderRadius: 8,
              letterSpacing: 2,
            }}
          >
            {episode}
          </div>
          <div
            style={{
              fontFamily: HEAD,
              fontWeight: 700,
              fontSize: 128,
              lineHeight: 1,
              color: C.text,
              marginTop: 26,
            }}
          >
            {line1}
          </div>
          <div
            style={{
              fontFamily: HEAD,
              fontWeight: 700,
              fontSize: 128,
              lineHeight: 1.05,
              color: C.cyan,
            }}
          >
            {line2}
          </div>
        </div>
        <div
          style={{
            width: 360,
            display: "flex",
            flexDirection: "column",
            gap: 20,
          }}
        >
          {STEPS.map((st, i) => (
            <div
              key={st.k}
              style={{
                background: C.surface,
                border: `3px solid ${i === 1 ? C.cyan : C.line}`,
                boxShadow: i === 1 ? "0 0 50px rgba(53,224,255,0.45)" : "none",
                borderRadius: 18,
                padding: "22px 30px",
                fontFamily: HEAD,
                fontWeight: 700,
                fontSize: 58,
                color: i === 1 ? C.cyan : C.text,
              }}
            >
              {st.k}
            </div>
          ))}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
