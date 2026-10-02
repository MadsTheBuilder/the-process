#!/usr/bin/env bash
# run.sh <outdir> t1 t2 ... : rebuild scene01.blend then render stills at the given seconds + sheet
cd "$(dirname "$0")"; O="$1"; shift
./blender.sh -P scene01.py -- "$(pwd -W)/scene01.blend" 2>&1 | grep -iE "error|Traceback|crowd" 
rm -rf "$O"; ./blender.sh scene01.blend -P stills.py -- "$(pwd -W)/$O" "$@" 2>&1 | grep -iE "error|Traceback"
./sheet.sh "$O" ${COLS:-3}
