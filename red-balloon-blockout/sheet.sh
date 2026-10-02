#!/usr/bin/env bash
# sheet.sh outdir cols  -> outdir/sheet.png (tiles t*.png in time order; no labels)
D="$1"; C="${2:-3}"; cd "$D"
args=(); N=0; fl=""
for f in t*.png; do args+=(-i "$f"); fl+="[$N:v]scale=640:-1[v$N];"; N=$((N+1)); done
m=""; for ((k=0;k<N;k++)); do m+="[v$k]"; done
lay=$(python -c "c=$C;n=$N;print('|'.join('%d_%d'%((i%c)*640,(i//c)*360) for i in range(n)))")
ffmpeg -y -loglevel error "${args[@]}" -filter_complex "${fl}${m}xstack=inputs=$N:layout=$lay" sheet.png
