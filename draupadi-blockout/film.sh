#!/usr/bin/env bash
# film.sh [first=1] [last=28] : render every scene (render.sh) and join them into out/DRAUPADI_blockout_animatic.mp4
cd "$(dirname "$0")"
A="${1:-1}"; B="${2:-28}"
for n in $(seq "$A" "$B"); do ./render.sh "$n" 40 12 2>&1 | tail -1; done
ls out/sc??.mp4 | sed "s/^/file '/; s/$/'/" > out/list.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i out/list.txt -c copy out/DRAUPADI_blockout_animatic.mp4 && echo "film: out/DRAUPADI_blockout_animatic.mp4"
