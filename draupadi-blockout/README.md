# DRAUPADI SE DRAUPADI TAK — Blender blockout (213 shots, 28 scenes, 15.6 min)

Built from `Test_script_Shot_Breakdown_v2_lit.xlsx` (shots, lenses, moves, angles, lighting, audio, durations)
and the reference boards in `Desktop/test references` (sets, rooms, costume colours, the river and sheets moods).

## Run
| Command | What it does |
|---|---|
| `./blender.sh -P build.py -- <n> <abs>/out/scNN.blend` | build one scene file |
| `./qs.sh <n> 30 t1 t2 ...` | build + render stills at those seconds + contact sheet (`out/stNN/sheet.png`) |
| `./render.sh <n> [pct] [samples]` | build, render every frame, grade + caption → `out/scNN.mp4` |
| `./film.sh [first] [last]` | render the range and join → `out/DRAUPADI_blockout_animatic.mp4` |

Always use `blender.sh` (isolated user folder) for headless runs.

## Files
- `shots.json` — the breakdown, parsed from the xlsx (timing source for every scene).
- `kit.py` — mannequin rig (walk, sit, lie face-up / face-down, look, two-bone arms, face: brows/mouth/eyelids), bulk keyframe writer.
- `film.py` — scene context: shot times, lens-aware framing (`on`, `frame`, `ots`, `push`), per-shot key/fill/rim rig, light states, props on hands, tears, caustics, the lens-blocked check.
- `sets.py` — all locations at real scale: house (drawing room, corridor, Mamta's room, Mother's room, kitchen, front steps, lane), school (classroom, veranda, staff room), street, hospital backyard with sheets, dream river.
- `cast.py` — every character look (Mamta 35 / 22, Papa, Mother, Dev, Jagdish, kids, extras).
- `props.py`, `hs.py` — props, vehicles, house helpers (doors, almirah, mirror flaps, fairy lights, mirror probes).
- `scenes/scNN.py` — one file per scene: blocking, cameras, light per shot. Edit numbers there and rebuild.
- `burn.py` — per-shot colour grade + burned-in captions (shot / mag / move / lens / angle + verbatim audio).

## Decisions the sheet did not make (change in the scene file)
- One house for every house scene, so "same framing" callbacks are literal: 27↔29 (lane), 43↔116 (drawing-room corner), 61↔150 (Mamta's room), 105→112, 184↔208 (Mother's room).
- Classroom windows on the west wall (camera-left from the back row). Reverse angles keep the sheet's key side (a gaffer's cheat).
- Mirror shots (93, 95–101) are shot into a real raytraced mirror; the reflection is the image.
- Dev's face stays hidden (sheets, backs, distance) until 191.
- 127: Dev falls face-down so his face stays away from camera.
- 32: the bags fall at the foot of the steps (she has walked up the lane between 28 and 32).
- 153/159: the baby is a wrapped bundle, never a face.
- 212: the flower sits in a crack in Mother's east wall, lit by its own sunbeam.

## Conflicts / notes for the director
- Sheet 76 says white sheets; the reference board is saturated yellow. Kept **white** (the sheet's motif: white = Dev = loss).
- 4 "window key camera-left" on the girls' reverse angle: physically the window is camera-right there; the rig follows the sheet.
- 59: "LS" on a 135 mm across the drawing room only gives a waist-up of Papa (room is 6 m deep).
- 149 "WS" in a 1.6 m corridor: at 35 mm the widest possible is roughly a full figure.
- 150's bare bulb is in the room centre, not above the bed, so it reads in the wide.
- The red sweater stays red (script says blue in Sc21) as the sheet decided.
