#!/usr/bin/env bash
# blender.sh — run Blender headless in an ISOLATED user dir, so factory resets inside scene scripts
# can't disable (and delete the Python wheels of) the user's installed extensions.
#   scripts/blender.sh -P scene.py -- out.blend
#   scripts/blender.sh file.blend --python-expr "..." -a
set -euo pipefail
B="${BLENDER:-}"
if [ -z "$B" ]; then
  for c in "/c/Program Files/Blender Foundation/Blender 5.1/blender.exe" \
           "/Applications/Blender.app/Contents/MacOS/Blender" "$(command -v blender || true)"; do
    [ -n "$c" ] && [ -x "$c" ] && B="$c" && break
  done
fi
[ -z "$B" ] && { echo "Blender not found; set BLENDER=/path/to/blender" >&2; exit 1; }
ISO="${TMPDIR:-${TEMP:-/tmp}}/create-3d-scene-blender-iso"
mkdir -p "$ISO"
command -v cygpath >/dev/null && ISO="$(cygpath -w "$ISO")"
BLENDER_USER_RESOURCES="$ISO" exec "$B" -b "$@"
