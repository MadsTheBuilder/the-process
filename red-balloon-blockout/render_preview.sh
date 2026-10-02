#!/usr/bin/env bash
# render_preview.sh [percent=50] : build scene01.blend, render all frames (EEVEE), burn captions -> scene01_preview.mp4
cd "$(dirname "$0")"; PCT="${1:-50}"
./blender.sh -P scene01.py -- "$(pwd -W)/scene01.blend" 2>&1 | grep -iE "error|Traceback"
rm -rf scene01_frames; mkdir scene01_frames
./blender.sh scene01.blend --python-expr "import bpy;s=bpy.context.scene;s.render.resolution_percentage=$PCT;s.eevee.taa_render_samples=6;s.render.filepath=r'$(pwd -W)/scene01_frames/f_';s.render.image_settings.file_format='PNG'" -a 2>&1 | grep -iE "error|Traceback"
python burn.py "$(pwd -W)/scene01_frames" "$(pwd -W)/scene01_preview.mp4" || /c/Users/madhu/AppData/Local/Microsoft/WindowsApps/python burn.py "$(pwd -W)/scene01_frames" "$(pwd -W)/scene01_preview.mp4"
