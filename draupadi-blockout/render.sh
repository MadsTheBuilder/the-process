#!/usr/bin/env bash
# render.sh <scene no> [percent=40] [samples=6] : build out/scNN.blend, render every frame (EEVEE), grade + caption -> out/scNN.mp4
set -e
cd "$(dirname "$0")"
N=$(printf "%02d" "$1"); PCT="${2:-40}"; SMP="${3:-6}"
W="$(pwd -W)"
./blender.sh -P build.py -- "$1" "$W/out/sc$N.blend" 2>&1 | grep -iE "error|traceback" && exit 1
rm -rf "out/f$N"; mkdir -p "out/f$N"
./blender.sh "out/sc$N.blend" --python-expr "import bpy;s=bpy.context.scene;s.render.resolution_percentage=$PCT;s.eevee.taa_render_samples=$SMP;s.render.filepath=r'$W/out/f$N/f_';s.render.image_settings.file_format='JPEG';s.render.image_settings.quality=90" -a 2>&1 | grep -iE "error|traceback" || true
python3 burn.py "$1" "$W/out/f$N" "$W/out/sc$N.mp4"
