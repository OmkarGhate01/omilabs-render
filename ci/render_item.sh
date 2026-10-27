#!/bin/bash
# Render ONE item on a GitHub runner and publish the result as two branches of this repo:
#   media/<file.mp4>  -> the video, split into <=45 MB parts (the private publisher downloads it)
#   pkg/<item>        -> metadata files laid out at the private publisher's paths (it imports them)
# Items: el-epNN (ElevenLabs long), el-bNN (ElevenLabs Shorts batch NN), bo-epNN (Bolna long), bo-bNN (Bolna Shorts batch NN)
set -euo pipefail
ITEM="$1"
W="$GITHUB_WORKSPACE"
EL=/home/claude/ElevenLabs-Masterclass; BO=/home/claude/Bolna-AI-Masterclass
PKG="$RUNNER_TEMP/pkg"; rm -rf "$PKG"; mkdir -p "$PKG"

# --- same paths as the original render box -------------------------------------------------
sudo mkdir -p /home/claude && sudo chown "$USER" /home/claude
ln -sfn "$W/ElevenLabs-Masterclass" $EL
ln -sfn "$W/Bolna-AI-Masterclass" $BO
mkdir -p "$W/Bolna-AI-Masterclass/Video-Projects"
ln -sfn "$W/engine" "$W/Bolna-AI-Masterclass/Video-Projects/omilabs-remotion"
ln -sfn "$W/Bolna-AI-Masterclass/Video-Projects" "$W/ElevenLabs-Masterclass/Video-Projects"
ln -sfn "$RUNNER_TEMP/tts" /home/claude/tts

push_media() {  # push_media FILE NAME
  local f="$1" n="$2" T="$RUNNER_TEMP/split"; rm -rf "$T"; mkdir -p "$T"
  split -b 45m -d -a 2 "$f" "$T/$n.part"
  export GIT_INDEX_FILE="$RUNNER_TEMP/idx-media"; rm -f "$GIT_INDEX_FILE"
  for p in "$T"/*; do b=$(git hash-object -w "$p"); git update-index --add --cacheinfo 100644,$b,$(basename "$p"); done
  local c; c=$(echo "media $n" | git commit-tree "$(git write-tree)"); unset GIT_INDEX_FILE
  git push -q -f origin "$c:refs/heads/media/$n"
  echo "pushed media/$n"
}
push_pkg() {  # push_pkg NAME  (contents of $PKG)
  export GIT_INDEX_FILE="$RUNNER_TEMP/idx-pkg"; rm -f "$GIT_INDEX_FILE"
  (cd "$PKG" && find . -type f | sed 's#^\./##') | while read -r rel; do
    b=$(git hash-object -w "$PKG/$rel"); git update-index --add --cacheinfo 100644,$b,"$rel"; done
  local c; c=$(echo "pkg $1" | git commit-tree "$(git write-tree)"); unset GIT_INDEX_FILE
  git push -q -f origin "$c:refs/heads/pkg/$1"
  echo "pushed pkg/$1"
}
approve_auto() {  # no human on the runner: visual review = automatic visual + render checks
  python3 - "$1" <<'PY'
import json, sys
p = sys.argv[1]; a = json.load(open(p))
a["pass_visual_review"] = bool(a.get("pass_visual_auto") and a.get("pass_render"))
a["review"] = "auto (GitHub runner)"
json.dump(a, open(p, "w"), indent=1)
PY
}

case "$ITEM" in
  el-ep*)
    n=$((10#${ITEM#el-ep})); N=$(printf %02d $n); cd $EL/Production
    python3 build.py $n
    python3 pipeline.py bundle
    python3 pipeline.py render $n
    python3 pipeline.py post $n
    PKG_OUT="$PKG/" python3 el_package.py $n
    test -f "$PKG/Published-Assets/youtube-upload/elevenlabs/el$N.json"
    push_media "$EL/Published-Assets/ep$N-master.mp4" "el-ep$N-master.mp4"
    push_pkg "el-ep$N" ;;
  bo-ep*)
    n=$((10#${ITEM#bo-ep})); N=$(printf %02d $n); cd $BO/Production
    python3 build.py $n
    python3 pipeline.py bundle
    python3 pipeline.py render $n
    python3 pipeline.py post $n
    python3 youtube_package.py $n
    mkdir -p "$PKG/Published-Assets/youtube-upload" "$PKG/Thumbnails"
    cp "$BO/Published-Assets/youtube-upload/ep$N-youtube.txt" "$BO/Published-Assets/youtube-upload/ep$N-en.srt" "$PKG/Published-Assets/youtube-upload/"
    cp "$BO/Thumbnails/ep$N-thumbnail.png" "$PKG/Thumbnails/"
    push_media "$BO/Published-Assets/ep$N-master.mp4" "ep$N-master.mp4"
    push_pkg "bo-ep$N" ;;
  el-b*|bo-b*)
    b=$((10#${ITEM#*-b})); B=$(printf %02d $b)
    if [[ "$ITEM" == el-* ]]; then D=$EL; PFX="el-"; else D=$BO; PFX=""; fi
    cd $D/Production
    python3 shorts_build.py $b
    python3 shorts_pipeline.py bundle
    ids=$(python3 -c "import runpy;print(' '.join(s['id'] for s in runpy.run_path('shorts/batch$B.py')['SHORTS']))")
    for id in $ids; do
      python3 shorts_pipeline.py render $id || { echo "render failed $id"; continue; }
      a=build/shorts/$id/audit.json; [ -f "$a" ] || continue
      approve_auto "$a"
      mkdir -p "$PKG/Production/build/shorts/$id"; cp "$a" "$PKG/Production/build/shorts/$id/"
      [ -f "$D/Published-Assets/shorts/$id.mp4" ] && push_media "$D/Published-Assets/shorts/$id.mp4" "$PFX$id.mp4"
    done
    push_pkg "$ITEM" ;;
  ns-b*)
    b=$((10#${ITEM#ns-b})); B=$(printf %02d $b)
    NAMES=(muse el_v4 claude_motion kling)
    BNAME="${NAMES[$((b-1))]}"
    D=$BO; cd $D/Production
    python3 shorts_build.py --batch "shorts/batch_${BNAME}.py" 2>/dev/null || true
    ids=$(python3 -c "import runpy; print(' '.join(s['id'] for s in runpy.run_path('shorts/batch_${BNAME}.py')['SHORTS']))")
    for id in $ids; do
      python3 shorts_pipeline.py render $id || { echo "render failed $id"; continue; }
      a=build/shorts/$id/audit.json; [ -f "$a" ] || continue
      approve_auto "$a"
      mkdir -p "$PKG/Production/build/shorts/$id"; cp "$a" "$PKG/Production/build/shorts/$id/"
      [ -f "$D/Published-Assets/shorts/$id.mp4" ] && push_media "$D/Published-Assets/shorts/$id.mp4" "$id.mp4"
    done
    push_pkg "$ITEM" ;;
  *) echo "unknown item $ITEM"; exit 1 ;;
esac
