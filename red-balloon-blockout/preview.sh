#!/usr/bin/env bash
# preview.sh — fast EEVEE preview of a blockout: frames -> MP4 -> contact sheet of chosen seconds.
#   scripts/preview.sh scene.blend [percent=33] [seconds for the sheet, e.g. "0 1 2.5 4 ..."]
# Writes <name>_preview.mp4 and <name>_sheet.png next to the .blend. ~1 min for 500 frames at 33%.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
BLEND="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
PCT="${2:-33}"
SECS="${3:-}"
STEM="${BLEND%.blend}"
FR="${STEM}_frames"
rm -rf "$FR"; mkdir -p "$FR"
OUTP="$FR/f_"
command -v cygpath >/dev/null && OUTP="$(cygpath -m "$FR")/f_"   # Blender needs an absolute native path
"$HERE/blender.sh" "$BLEND" --python-expr "import bpy;s=bpy.context.scene;s.render.resolution_percentage=$PCT;s.eevee.taa_render_samples=4;s.render.filepath=r'$OUTP';s.render.image_settings.file_format='PNG'" -a \
  2>&1 | grep -iE 'error|traceback' || true
FPS=$("$HERE/blender.sh" "$BLEND" --python-expr "import bpy;print('FPS=%d'%bpy.context.scene.render.fps)" 2>/dev/null | sed -n 's/^FPS=//p')
FPS="${FPS:-24}"
ffmpeg -y -loglevel error -framerate "$FPS" -i "$FR/f_%04d.png" -c:v libx264 -pix_fmt yuv420p \
  -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" "${STEM}_preview.mp4"
if [ -z "$SECS" ]; then   # default: 16 evenly spaced frames
  N=$(ls "$FR" | wc -l); SECS=$(python -c "print(' '.join(str(round(i*($N-1)/15/$FPS,2)) for i in range(16)))")
fi
SEL=$(python -c "import sys;print('+'.join('eq(n\\\\,%d)'%round(float(s)*$FPS) for s in sys.argv[1:]))" $SECS)
COUNT=$(echo $SECS | wc -w); COLS=$(( COUNT > 8 ? 8 : COUNT )); ROWS=$(( (COUNT + 7) / 8 ))
ffmpeg -y -loglevel error -i "${STEM}_preview.mp4" -vf "select='$SEL',scale=240:-1,tile=${COLS}x${ROWS}" \
  -frames:v 1 "${STEM}_sheet.png"
echo "preview: ${STEM}_preview.mp4"
echo "sheet:   ${STEM}_sheet.png  (seconds: $SECS)"
