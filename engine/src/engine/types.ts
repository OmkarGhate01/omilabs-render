/* eslint-disable @typescript-eslint/no-explicit-any */
export type Line = {
  t: string;
  cue: string | null;
  start: number;
  end: number;
};

export type SceneData = {
  type: string;
  label: string;
  kicker?: string;
  title?: string;
  accent?: string[];
  src?: string;
  fx?: string;
  bg?: string;
  start: number;
  end: number;
  lines: Line[];
  [k: string]: any;
};

export type Tr = { type: string; d: number; dir: number };

export type Segment = {
  kind: "scene" | "title";
  scene: number; // index into scenes, -1 for title
  from: number; // visual start frame (boundary)
  to: number; // visual end frame (next boundary)
  tin: Tr | null; // transition into this segment
  tout: Tr | null; // transition out of this segment
};

export type EpisodeProps = {
  n: number;
  title: string;
  short: string;
  module: string;
  moduleN: number;
  icon: string;
  next: { n: number; title: string } | null;
  durationInFrames: number;
  scenes: SceneData[];
  segments: Segment[];
};

export type ThumbProps = {
  n: number;
  l1: string;
  l2: string;
  icon: string;
  module: string;
};
