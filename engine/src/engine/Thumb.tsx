import React from "react";
import { AbsoluteFill } from "remotion";
import { C, F, pad2, SERIES, setSeries } from "./theme";
import { ThumbProps } from "./types";
import { OmMark } from "./fx";
import { Icon } from "./icons";

// 1280x720 thumbnail. Max ~4 words across two lines.
// v3 (CTR audit): one accent colour per module so a feed of thumbnails is not one flat blue,
// bigger headline (smaller icon ring), and a clear "BOLNA AI" tag.
const ACCENTS: Record<string, string> = {
  foundations: "#35E0FF", "agent creation": "#9B7BFF", "graph agents": "#3DF2A0", "speech and models": "#FFB547",
  telephony: "#FF6B8B", "apis and development": "#4DA3FF", "tools and automation": "#3DF2A0", production: "#FFB547", "open source": "#9B7BFF",
};
export const Thumb: React.FC<ThumbProps> = ({ n, l1, l2, icon, module, series }: any) => {
  setSeries(series);
  const A = ACCENTS[module.toLowerCase()] || C.cyan;
  const longest = Math.max(l1.length, l2.length);
  const tier =
    longest <= 6 ? 168 : longest <= 8 ? 146 : longest <= 10 ? 124 : 108;
  // Keep the headline clear of the icon ring (ring starts at x≈795, text at x=64).
  // Unbounded 800 caps average ~0.9em per glyph, spaces ~0.35em.
  const em = (s: string) => s.replace(/ /g, "").length * 0.9 + (s.split(" ").length - 1) * 0.35;
  const size = Math.min(tier, Math.floor(740 / Math.max(em(l1), em(l2), 1)));
  const depth = 10;
  const shadow =
    new Array(depth)
      .fill(0)
      .map(
        (_, i) =>
          `${i * 0.6}px ${i + 1}px 0 rgba(${30 - i * 2},${70 - i * 5},${180 - i * 12},1)`,
      )
      .join(", ") + ", 0 18px 40px rgba(0,0,0,0.7)";
  return (
    <AbsoluteFill
      style={{
        background:
          `radial-gradient(ellipse at 78% 45%, ${A}55 0%, #070B18 50%, #02030A 100%)`,
        overflow: "hidden",
      }}
    >
      <AbsoluteFill
        style={{
          backgroundImage: `linear-gradient(${C.line} 1px, transparent 1px), linear-gradient(90deg, ${C.line} 1px, transparent 1px)`,
          backgroundSize: "64px 64px",
          opacity: 0.35,
          WebkitMaskImage:
            "radial-gradient(ellipse at 70% 50%, black 10%, transparent 70%)",
          maskImage:
            "radial-gradient(ellipse at 70% 50%, black 10%, transparent 70%)",
        }}
      />
      <div
        style={{
          position: "absolute",
          right: 20,
          top: 170,
          width: 430,
          height: 430,
          transform: "scale(0.78)",
        }}
      >
        <svg
          width={430}
          height={430}
          style={{ position: "absolute", left: 0, top: 0 }}
        >
          <circle
            cx={215}
            cy={215}
            r={200}
            fill="none"
            stroke={A}
            strokeOpacity={0.35}
            strokeWidth={2}
            strokeDasharray="60 18 6 18"
          />
          <circle
            cx={215}
            cy={215}
            r={160}
            fill="rgba(255,255,255,0.05)"
            stroke={A}
            strokeWidth={4}
            style={{ filter: `drop-shadow(0 0 28px ${A})` }}
          />
        </svg>
        <div style={{ position: "absolute", left: 95, top: 95 }}>
          <Icon name={icon} size={240} color={A} sw={2.8} />
        </div>
      </div>
      <div
        style={{
          position: "absolute",
          left: 64,
          top: 56,
          display: "flex",
          alignItems: "center",
          gap: 16,
        }}
      >
        <div
          style={{
            fontFamily: F.hero,
            fontWeight: 800,
            fontSize: 44,
            color: C.bg,
            background: A,
            padding: "6px 18px",
            borderRadius: 10,
          }}
        >
          {SERIES.tag} · EP {pad2(n)}
        </div>
        <div
          style={{
            fontFamily: F.mono,
            fontWeight: 700,
            fontSize: 26,
            color: C.muted,
            letterSpacing: 3,
          }}
        >
          {module.toUpperCase()}
        </div>
      </div>
      <div
        style={{
          position: "absolute",
          left: 64,
          top: 120,
          bottom: 160,
          width: 900,
          display: "flex",
          flexDirection: "column",
          justifyContent: "center", // headline centred on the icon ring (y≈335)
        }}
      >
        <div
          style={{
            fontFamily: F.hero,
            fontWeight: 800,
            fontSize: size,
            lineHeight: 1.02,
            color: "#FFFFFF",
            textShadow: shadow,
          }}
        >
          {l1}
        </div>
        <div
          style={{
            fontFamily: F.hero,
            fontWeight: 800,
            fontSize: size,
            lineHeight: 1.06,
            color: A,
            textShadow: shadow,
          }}
        >
          {l2}
        </div>
        {/* CTR audit v4: bright marker bar under the hook line so it reads at 168 px wide in the feed */}
        <div style={{ marginTop: 14, width: Math.min(820, Math.max(260, em(l2) * size * 0.95)), height: 16, borderRadius: 8,
          background: `linear-gradient(90deg, #FFD23F, ${A})`, boxShadow: `0 0 30px ${A}` }} />
      </div>
      <div
        style={{
          position: "absolute",
          left: 64,
          bottom: 50,
          display: "flex",
          alignItems: "center",
          gap: 14,
        }}
      >
        <OmMark size={58} />
        <div
          style={{
            fontFamily: F.mono,
            fontWeight: 700,
            fontSize: 24,
            color: C.text,
            letterSpacing: 4,
          }}
        >
          {SERIES.name.toUpperCase()}
        </div>
      </div>
    </AbsoluteFill>
  );
};
