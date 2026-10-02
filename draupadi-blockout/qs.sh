#!/usr/bin/env bash
# qs.sh <scene no> <pct> t1 t2 ... : build the scene and render a stills sheet (quick check)
cd "$(dirname "$0")"
N=$(printf "%02d" "$1"); P="$2"; shift 2
./blender.sh -P build.py -- "$((10#$N))" "$(pwd -W)/out/sc$N.blend" 2>&1 | grep -iE "error|traceback|line [0-9]|WARN" 
rm -rf "out/st$N"; ./blender.sh "out/sc$N.blend" -P stills.py -- "$(pwd -W)/out/st$N" "$P" "$@" 2>&1 | grep -iE "error|traceback"
./sheet.sh "out/st$N" "${COLS:-4}"
