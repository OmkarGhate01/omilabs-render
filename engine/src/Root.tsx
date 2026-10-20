import {
  CalculateMetadataFunction,
  Composition,
  Folder,
  Still,
} from "remotion";
import { Episode } from "./engine/Episode";
import { Thumb } from "./engine/Thumb";
import { Short, ShortProps, shortSample } from "./engine/Short";
import { EpisodeProps, ThumbProps } from "./engine/types";
import sample from "./engine/sample.json";
import {
  EpisodeTitle,
  IntroSting,
  LowerThird,
  PipelineLoop,
  Thumbnail,
} from "./Omilabs";

const calc: CalculateMetadataFunction<EpisodeProps> = ({ props }) => ({
  durationInFrames: props.durationInFrames,
});

const calcShort: CalculateMetadataFunction<ShortProps> = ({ props }) => ({
  durationInFrames: props.durationInFrames,
});

const thumbDefaults: ThumbProps = {
  n: 1,
  l1: "WHAT IS",
  l2: "BOLNA AI?",
  icon: "wave",
  module: "Foundations",
};

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="Episode"
        component={Episode}
        durationInFrames={300}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={sample as unknown as EpisodeProps}
        calculateMetadata={calc}
      />
      <Composition
        id="Short"
        component={Short}
        durationInFrames={360}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={shortSample}
        calculateMetadata={calcShort}
      />
      <Still
        id="Thumb"
        component={Thumb}
        width={1280}
        height={720}
        defaultProps={thumbDefaults}
      />
      <Folder name="Legacy">
        <Composition
          id="IntroSting"
          component={IntroSting}
          durationInFrames={150}
          fps={30}
          width={1920}
          height={1080}
        />
        <Composition
          id="Ep01Title"
          component={EpisodeTitle}
          durationInFrames={120}
          fps={30}
          width={1920}
          height={1080}
          defaultProps={{
            episode: "EP 01",
            line1: "What Is",
            line2: "Bolna AI?",
            series: "Bolna AI Masterclass  ·  Omkar Ghate",
          }}
        />
        <Composition
          id="PipelineLoop"
          component={PipelineLoop}
          durationInFrames={300}
          fps={30}
          width={1920}
          height={1080}
        />
        <Composition
          id="LowerThird"
          component={LowerThird}
          durationInFrames={120}
          fps={30}
          width={1920}
          height={1080}
          defaultProps={{
            name: "Omkar Ghate",
            role: "Agentic AI Architect  ·  Omilabs",
          }}
        />
        <Still
          id="Ep01Thumbnail"
          component={Thumbnail}
          width={1280}
          height={720}
          defaultProps={{
            episode: "EP 01",
            line1: "WHAT IS",
            line2: "BOLNA AI?",
          }}
        />
      </Folder>
    </>
  );
};
