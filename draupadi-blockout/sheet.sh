#!/usr/bin/env bash
# sheet.sh <dir> [cols=4] -> <dir>/sheet.png : tiles t*.png in time order with the time as a label
D="$1"; C="${2:-4}"; cd "$D" || exit 1
args=(); fl=""; N=0
for f in t*.png; do
  lab="${f#t}"; lab="${lab%.png}"
  args+=(-i "$f"); fl+="[$N:v]scale=480:-2,drawtext=fontfile='C\:/Windows/Fonts/arial.ttf':text='$lab':x=6:y=6:fontsize=16:fontcolor=yellow:box=1:boxcolor=black@0.6[v$N];"; N=$((N+1))
done
m=""; for ((k=0;k<N;k++)); do m+="[v$k]"; done
lay=$(python3 -c "c=$C;n=$N;print('|'.join('%d_%d'%((i%c)*480,(i//c)*201) for i in range(n)))")
ffmpeg -y -loglevel error "${args[@]}" -filter_complex "${fl}${m}xstack=inputs=$N:layout=$lay:fill=black" sheet.png && echo "$D/sheet.png"
