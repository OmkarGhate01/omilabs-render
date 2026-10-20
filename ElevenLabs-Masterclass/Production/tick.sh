#!/bin/bash
# ElevenLabs render keepalive: restart render queue / builds if the box slept.
cd /home/claude/ElevenLabs-Masterclass/Production
ps -eo args | grep -q "^python3 pipeline.py queue" || (nohup python3 pipeline.py queue >> queue.out 2>&1 &)
ps -eo args | grep -q "^python3 shorts_pipeline.py queue" || (nohup python3 shorts_pipeline.py queue >> shorts_queue.out 2>&1 &)
if ! grep -q ALLBUILT build_all.log 2>/dev/null && ! ps -eo args | grep -q "^python3 build.py"; then
  nohup bash -c 'for n in $(seq 1 33); do [ -f build/ep$(printf %02d $n)/props.json ] && continue; python3 build.py $n >> build_all.log 2>&1 && python3 pipeline.py ready $n >> build_all.log 2>&1; done; echo ALLBUILT >> build_all.log' >/dev/null 2>&1 &
fi
if ! grep -q SHORTSBUILT shorts_build_all.log 2>/dev/null && ! ps -eo args | grep -q "^python3 shorts_build.py"; then
  nohup bash -c 'for b in 2 3 4; do python3 shorts_build.py $b >> shorts_build_all.log 2>&1; done; echo SHORTSBUILT >> shorts_build_all.log' >/dev/null 2>&1 &
fi
ps -eo args | grep -q "^/bin/bash /home/claude/push_media.sh" || (nohup bash -c 'xargs -a /tmp/claude-0/media-list.txt /home/claude/push_media.sh' >> /tmp/claude-0/push_media.log 2>&1 &)
bash /home/claude/Bolna-AI-Masterclass/Production/keepalive.sh
echo "eps built: $(ls build/ep*/props.json 2>/dev/null | wc -l)/33  masters: $(ls ../Published-Assets/ep*-master.mp4 2>/dev/null | wc -l)/33  shorts: $(ls ../Published-Assets/shorts/*.mp4 2>/dev/null | wc -l)/67  bolna media pushed: $(grep -c '^ok' /tmp/claude-0/push_media.log)"
# Push finished ElevenLabs renders to GitHub as media/el-<file> (names prefixed so they never clash with Bolna files)
mkdir -p /tmp/claude-0/el-media
for f in /home/claude/ElevenLabs-Masterclass/Published-Assets/ep[0-9][0-9]-master.mp4 /home/claude/ElevenLabs-Masterclass/Published-Assets/shorts/e[0-9][0-9][0-9].mp4; do
  [ -f "$f" ] || continue; ln -sf "$f" /tmp/claude-0/el-media/el-$(basename "$f")
done
ps -eo args | grep -q "^/bin/bash /home/claude/push_media.sh" || (nohup bash -c 'ls /tmp/claude-0/el-media/*.mp4 2>/dev/null | xargs -r /home/claude/push_media.sh' >> /tmp/claude-0/push_media_el.log 2>&1 &)
# Back up all source/progress to GitHub (workspace/)
(bash /home/claude/Bolna-AI-Masterclass/Production/oss_package.sh >> /tmp/claude-0/oss_package.log 2>&1; cd /home/claude/ElevenLabs-Masterclass/Production && python3 el_package.py >> /tmp/claude-0/el_package.log 2>&1; /home/claude/sync_git.sh >> /tmp/claude-0/sync_git.log 2>&1) &
# Bolna Open Source bonus (ep54-56 + s101-s106): build -> ready (Bolna render queue picks them up)
if ! grep -q OSSBUILT /home/claude/Bolna-AI-Masterclass/Production/oss_build.log 2>/dev/null && ! ps -eo args | grep -q "^bash -c cd /home/claude/Bolna-AI-Masterclass/Production; for n in 54"; then
  nohup bash -c 'cd /home/claude/Bolna-AI-Masterclass/Production; for n in 54 55 56; do [ -f build/ep$n/READY ] || [ -f build/ep$n/RENDERED ] || { python3 build.py $n >> oss_build.log 2>&1 && python3 pipeline.py ready $n >> oss_build.log 2>&1; }; done; python3 shorts_build.py 11 >> oss_build.log 2>&1; echo OSSBUILT >> oss_build.log' >/dev/null 2>&1 &
fi
