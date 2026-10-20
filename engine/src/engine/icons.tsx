import React from "react";
import { C } from "./theme";

// Original line icons drawn for this project (48x48 grid).
type P = {
  fill: string;
  stroke: string;
  strokeWidth: number;
  strokeLinecap: "round";
  strokeLinejoin: "round";
  pathLength: number;
  strokeDasharray: number;
  strokeDashoffset: number;
};

const I: Record<string, (p: P) => React.ReactNode> = {
  phone: (p) => (
    <path
      {...p}
      d="M14 7h6l3 9-4.5 3.5a24 24 0 0 0 10 10L32 25l9 3v6a5 5 0 0 1-5 5C20 39 9 28 9 12a5 5 0 0 1 5-5z"
    />
  ),
  chat: (p) => (
    <>
      <path
        {...p}
        d="M8 9h22a4 4 0 0 1 4 4v10a4 4 0 0 1-4 4H18l-7 6v-6H8a4 4 0 0 1-4-4V13a4 4 0 0 1 4-4z"
      />
      <path
        {...p}
        d="M38 17h2a4 4 0 0 1 4 4v10a4 4 0 0 1-4 4h-1v6l-7-6h-8a4 4 0 0 1-3-1.5"
      />
    </>
  ),
  message: (p) => (
    <>
      <path
        {...p}
        d="M8 9h32a4 4 0 0 1 4 4v16a4 4 0 0 1-4 4H22l-9 7v-7H8a4 4 0 0 1-4-4V13a4 4 0 0 1 4-4z"
      />
      <path {...p} d="M15 21h1M24 21h1M33 21h1" />
    </>
  ),
  graph: (p) => (
    <>
      <circle {...p} cx="11" cy="12" r="5" />
      <circle {...p} cx="37" cy="12" r="5" />
      <circle {...p} cx="24" cy="37" r="5" />
      <path {...p} d="M16 12h16M14 16l7.5 16.5M34 16l-7.5 16.5" />
    </>
  ),
  keypad: (p) => (
    <>
      {[0, 1, 2].map((r) =>
        [0, 1, 2].map((c) => (
          <rect
            key={r * 3 + c}
            {...p}
            x={7 + c * 13}
            y={5 + r * 13}
            width="8"
            height="8"
            rx="2"
          />
        )),
      )}
      <rect {...p} x="20" y="44" width="8" height="1" rx="0.5" />
    </>
  ),
  wave: (p) => (
    <path
      {...p}
      d="M6 24v0M11 19v10M16 12v24M21 17v14M26 6v36M31 15v18M36 20v8M41 23v2"
    />
  ),
  cpu: (p) => (
    <>
      <rect {...p} x="13" y="13" width="22" height="22" rx="4" />
      <rect {...p} x="19" y="19" width="10" height="10" rx="2" />
      <path
        {...p}
        d="M19 6v7M29 6v7M19 35v7M29 35v7M6 19h7M6 29h7M35 19h7M35 29h7"
      />
    </>
  ),
  spark: (p) => (
    <path
      {...p}
      d="M24 4c2 10 6 14 16 16-10 2-14 6-16 16-2-10-6-14-16-16 10-2 14-6 16-16zM39 33c.8 3.5 2 4.7 5 5.5-3 .8-4.2 2-5 5.5-.8-3.5-2-4.7-5-5.5 3-.8 4.2-2 5-5.5z"
    />
  ),
  speaker: (p) => (
    <>
      <path {...p} d="M7 18h8l11-9v30l-11-9H7z" />
      <path {...p} d="M32 18a8 8 0 0 1 0 12M37 12a16 16 0 0 1 0 24" />
    </>
  ),
  mic: (p) => (
    <>
      <rect {...p} x="18" y="5" width="12" height="23" rx="6" />
      <path {...p} d="M11 22a13 13 0 0 0 26 0M24 35v8M17 43h14" />
    </>
  ),
  code: (p) => (
    <path {...p} d="M16 13L6 24l10 11M32 13l10 11-10 11M28 8l-8 32" />
  ),
  terminal: (p) => (
    <>
      <rect {...p} x="4" y="8" width="40" height="32" rx="4" />
      <path {...p} d="M12 19l6 5-6 5M22 30h12" />
    </>
  ),
  browser: (p) => (
    <>
      <rect {...p} x="4" y="8" width="40" height="32" rx="4" />
      <path {...p} d="M4 17h40M10 12.5h1M15 12.5h1M20 12.5h1" />
    </>
  ),
  plug: (p) => (
    <path {...p} d="M18 5v9M30 5v9M12 14h24v7a12 12 0 0 1-24 0zM24 33v10" />
  ),
  webhook: (p) => (
    <>
      <rect {...p} x="26" y="8" width="18" height="32" rx="3" />
      <path {...p} d="M31 16h8M31 22h8M3 24h17M14 18l6 6-6 6" />
    </>
  ),
  db: (p) => (
    <>
      <ellipse {...p} cx="24" cy="11" rx="15" ry="5" />
      <path
        {...p}
        d="M9 11v26c0 3 7 5 15 5s15-2 15-5V11M9 24c0 3 7 5 15 5s15-2 15-5"
      />
    </>
  ),
  sheet: (p) => (
    <>
      <rect {...p} x="6" y="7" width="36" height="34" rx="3" />
      <path {...p} d="M6 18h36M6 29h36M18 7v34M30 7v34" />
    </>
  ),
  calendar: (p) => (
    <>
      <rect {...p} x="6" y="9" width="36" height="33" rx="4" />
      <path
        {...p}
        d="M6 19h36M16 5v8M32 5v8M14 27h4M22 27h4M30 27h4M14 34h4M22 34h4"
      />
    </>
  ),
  book: (p) => (
    <path
      {...p}
      d="M24 11c-5-4-11-5-18-3v30c7-2 13-1 18 3 5-4 11-5 18-3V8c-7-2-13-1-18 3zM24 11v30"
    />
  ),
  globe: (p) => (
    <>
      <circle {...p} cx="24" cy="24" r="18" />
      <ellipse {...p} cx="24" cy="24" rx="7" ry="18" />
      <path {...p} d="M6 24h36M9 15h30M9 33h30" />
    </>
  ),
  clock: (p) => (
    <>
      <circle {...p} cx="24" cy="24" r="18" />
      <path {...p} d="M24 13v11l8 5" />
    </>
  ),
  shield: (p) => (
    <>
      <path {...p} d="M24 5l16 6v11c0 10-7 17-16 21-9-4-16-11-16-21V11z" />
      <path {...p} d="M17 24l5 5 9-10" />
    </>
  ),
  lock: (p) => (
    <>
      <rect {...p} x="9" y="21" width="30" height="21" rx="4" />
      <path {...p} d="M15 21v-6a9 9 0 0 1 18 0v6M24 29v6" />
    </>
  ),
  key: (p) => (
    <>
      <circle {...p} cx="15" cy="33" r="8" />
      <path {...p} d="M21 27L41 7M35 13l5 5M30 18l4 4" />
    </>
  ),
  coin: (p) => (
    <>
      <ellipse {...p} cx="24" cy="12" rx="15" ry="6" />
      <path
        {...p}
        d="M9 12v8c0 3.3 6.7 6 15 6s15-2.7 15-6v-8M9 20v8c0 3.3 6.7 6 15 6s15-2.7 15-6v-8M9 28v8c0 3.3 6.7 6 15 6s15-2.7 15-6v-8"
      />
    </>
  ),
  wallet: (p) => (
    <>
      <path
        {...p}
        d="M8 12h28a4 4 0 0 1 4 4v22a4 4 0 0 1-4 4H8a4 4 0 0 1-4-4V12l26-6v6"
      />
      <path {...p} d="M30 25h10v8H30a4 4 0 0 1 0-8z" />
    </>
  ),
  user: (p) => (
    <>
      <circle {...p} cx="24" cy="16" r="8" />
      <path {...p} d="M8 42c2-9 9-14 16-14s14 5 16 14" />
    </>
  ),
  users: (p) => (
    <>
      <circle {...p} cx="18" cy="17" r="7" />
      <path
        {...p}
        d="M4 41c2-8 7-12 14-12s12 4 14 12M31 11a7 7 0 0 1 0 13M36 29c4 2 7 6 8 12"
      />
    </>
  ),
  bolt: (p) => <path {...p} d="M27 4L10 28h12l-2 16 18-26H26z" />,
  flow: (p) => (
    <>
      <rect {...p} x="4" y="6" width="15" height="11" rx="3" />
      <rect {...p} x="29" y="19" width="15" height="11" rx="3" />
      <rect {...p} x="4" y="32" width="15" height="11" rx="3" />
      <path {...p} d="M19 11h5v14h5M19 37h5V25" />
    </>
  ),
  check: (p) => (
    <>
      <circle {...p} cx="24" cy="24" r="18" />
      <path {...p} d="M15 24l6 6 12-13" />
    </>
  ),
  alert: (p) => (
    <>
      <path {...p} d="M24 6l20 35H4z" />
      <path {...p} d="M24 18v11M24 35v.5" />
    </>
  ),
  gear: (p) => (
    <>
      <circle {...p} cx="24" cy="24" r="7" />
      <path
        {...p}
        d="M24 4v6M24 38v6M4 24h6M38 24h6M9.9 9.9l4.2 4.2M33.9 33.9l4.2 4.2M9.9 38.1l4.2-4.2M33.9 14.1l4.2-4.2"
      />
      <circle {...p} cx="24" cy="24" r="14" />
    </>
  ),
  list: (p) => (
    <path {...p} d="M17 12h25M17 24h25M17 36h25M7 12h1M7 24h1M7 36h1" />
  ),
  robot: (p) => (
    <>
      <rect {...p} x="9" y="15" width="30" height="24" rx="7" />
      <path {...p} d="M24 8v7M18 26v1M30 26v1M18 33h12M4 25v6M44 25v6" />
      <circle {...p} cx="24" cy="6" r="2" />
    </>
  ),
  cloud: (p) => (
    <path
      {...p}
      d="M14 37h23a9 9 0 0 0 1-18 12 12 0 0 0-23-3 10 10 0 0 0-1 21z"
    />
  ),
  chart: (p) => (
    <>
      <path {...p} d="M6 6v36h36" />
      <path {...p} d="M14 33V23M22 33V14M30 33v-7M38 33V10" />
    </>
  ),
  mail: (p) => (
    <>
      <rect {...p} x="5" y="10" width="38" height="28" rx="4" />
      <path {...p} d="M6 12l18 14 18-14" />
    </>
  ),
  search: (p) => (
    <>
      <circle {...p} cx="20" cy="20" r="12" />
      <path {...p} d="M29 29l12 12" />
    </>
  ),
  layers: (p) => (
    <path {...p} d="M24 6l18 9-18 9-18-9zM6 24l18 9 18-9M6 33l18 9 18-9" />
  ),
  rocket: (p) => (
    <>
      <path {...p} d="M24 4c9 7 11 18 6 28H18C13 22 15 11 24 4z" />
      <circle {...p} cx="24" cy="18" r="4" />
      <path {...p} d="M18 26l-7 5 3 8 5-7M30 26l7 5-3 8-5-7M21 38l3 6 3-6" />
    </>
  ),
  transfer: (p) => <path {...p} d="M7 15h33l-7-7M41 33H8l7 7" />,
  inbound: (p) => <path {...p} d="M24 4v24M15 19l9 9 9-9M7 30v12h34V30" />,
  outbound: (p) => <path {...p} d="M24 30V6M15 15l9-9 9 9M7 30v12h34V30" />,
  retry: (p) => (
    <>
      <path {...p} d="M40 24a16 16 0 1 1-5-11.5" />
      <path {...p} d="M37 5v9h-9" />
    </>
  ),
  trunk: (p) => (
    <>
      <path {...p} d="M4 15h40M4 24h40M4 33h40" />
      <circle {...p} cx="14" cy="15" r="3" />
      <circle {...p} cx="30" cy="24" r="3" />
      <circle {...p} cx="20" cy="33" r="3" />
    </>
  ),
  batch: (p) => (
    <>
      <rect {...p} x="12" y="4" width="30" height="22" rx="3" />
      <path {...p} d="M8 10v20h28M4 16v26h28" />
    </>
  ),
  doc: (p) => (
    <>
      <path {...p} d="M11 4h18l10 10v30H11z" />
      <path {...p} d="M29 4v10h10M17 23h16M17 30h16M17 37h10" />
    </>
  ),
  target: (p) => (
    <>
      <circle {...p} cx="24" cy="24" r="18" />
      <circle {...p} cx="24" cy="24" r="11" />
      <circle {...p} cx="24" cy="24" r="4" />
    </>
  ),
  play: (p) => (
    <>
      <circle {...p} cx="24" cy="24" r="18" />
      <path {...p} d="M20 16l12 8-12 8z" />
    </>
  ),
  link: (p) => (
    <path
      {...p}
      d="M20 28l8-8M17 22l-5 5a6 6 0 0 0 9 9l5-5M31 26l5-5a6 6 0 0 0-9-9l-5 5"
    />
  ),
  filter: (p) => <path {...p} d="M5 8h38L28 26v14l-8 4V26z" />,
  bulb: (p) => (
    <>
      <path {...p} d="M17 33c0-4-6-7-6-15a13 13 0 0 1 26 0c0 8-6 11-6 15z" />
      <path {...p} d="M18 38h12M20 43h8" />
    </>
  ),
  dot: (p) => <circle {...p} cx="24" cy="24" r="8" />,
};

export const ICON_NAMES = Object.keys(I);

export const Icon: React.FC<{
  name?: string;
  size?: number;
  color?: string;
  draw?: number;
  sw?: number;
}> = ({ name = "dot", size = 64, color = C.cyan, draw = 1, sw = 2.4 }) => {
  const p: P = {
    fill: "none",
    stroke: color,
    strokeWidth: sw,
    strokeLinecap: "round",
    strokeLinejoin: "round",
    pathLength: 1,
    strokeDasharray: 1,
    strokeDashoffset: 1 - draw,
  };
  const fn = I[name] || I.dot;
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 48 48"
      style={{ overflow: "visible" }}
    >
      {fn(p)}
    </svg>
  );
};
