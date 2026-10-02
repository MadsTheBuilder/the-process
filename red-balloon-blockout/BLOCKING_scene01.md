# Operation Red Balloon, Scene 1 "MELA": blocking sheet (shots 1-19, 102 s)

This is the choreography the shot breakdown did not contain. Everything here is what the Blender file plays back.
Built only from the shot breakdown + script. No reference images, no visual storyboard PDF were used.
Edit the numbers in `scene01.py`, run `./blender.sh -P scene01.py -- <abs path>/scene01.blend`.

Axes: x east, y north, z up. Yaw 0 = facing east. The main lane runs east-west; the gate is at the east end (x = 62).

## The place (all at real scale)
| Thing | Where |
|---|---|
| Main lane | y -5.5 to 5.5, x -62 to 62. Stall rows either side, lanes 2 further out. Cross lanes at x = -26, 14, 36 |
| Ferris wheel | (-26, 32), 24 m wheel, 16 gondolas, rotates slowly, LED lights blink in 3 groups |
| Jhoola (chair swing) | (34, 32), rotating top with 8 swinging seats |
| Balloon vendor pole | (16, 2.9): 46 muted balloons + ONE hero red balloon on the west side. 2 more reds low in the bunch |
| Toy stall | row A, x = -3. Bargaining stall: row A, x = 3 |
| White van | (21.5, -3.6), parked at the lane edge |
| Food carts | (25, 28.5, 32; y = -5) with glowing tops and steam |
| Crowd | about 970 walkers drifting along the lanes; 14 carry a red balloon. Pruned so nobody walks through the cast |

Light: blue hour. Sodium point lights every 8 m along the lane, fairy-light strings, ferris-wheel LEDs. Red appears only on balloons.

## Cast (articulated mannequins: walk cycle, two-bone arms/legs, face with brows and mouth)
Father 1.72 m, Mother 1.58 m (dupatta), Uncle, Cousin (girl), **Dhruv 1.25 m** (blue jacket, safety pin on the zip), Balloon seller (moustache, gamchha), stall keeper, thin man in black cap and second man (both pure silhouettes, face never visible).

## Shot by shot
| # | Time | Camera | What happens (who moves where) | Feel |
|---|---|---|---|---|
| 1 | 0-5 | 24 mm drone, from (-72,-78,64) pushing in to (-30,-34,38), tilting down | Wheel turning, lanes glowing, crowd drifting. Establishes scale | Cold dusk, warm pockets of light |
| 2 | 5-9 | 135 mm static on a raised platform (-26, 64, 7) looking down the cross lane | Crowd compressed behind the wheel's gondolas and spokes. Red balloons planted in the crowd, steam from carts | Claustrophobic |
| 3 | 9-14 | 35 mm gimbal, orbits 160 deg from behind to front of the group | Gupta family walks east along the lane at 1.1 m/s: father, Dhruv holding his finger, mother, cousin skipping, uncle eating. All laughing | Warm, last normal moment |
| 4 | 14-17 | 50 mm static at child height (0.95 m) in front of Dhruv | Family stopped. Dhruv holds father's hand, glances up at father, then looks off toward the balloons. Pin visible on the zip | Innocent, a little wistful |
| 5 | 17-20 | 85 mm from Dhruv's eye (1.08 m), f/1.4 | POV across the crowd to the vendor pole. Focus racks from foreground crowd (4.5 m) to balloons (20 m). A light warms the hero red balloon at 18.7 s | Longing |
| 6 | 20-25 | 50 mm handheld, 2.4 m south of the stall | Parents bargain at the stall, backs to us, faces out of frame. Dhruv faces us, tugs mother's dupatta with one hand, points at the balloons with the other, pleading | Unreachable parents |
| 7 | 25-28 | 100 mm macro, 0.5 m from father's hand | Father's index finger; Dhruv's small fist slides down it and slips off the tip, drifts away. Empty finger held for the last beat | Inciting moment, quiet |
| 8 | 28-32 | 85 mm from 8 m west, f/2 focused on Dhruv | Parents (left, soft) keep bargaining. Dhruv walks east along the lane; 8 people cross between him and the camera until the crowd closes over him | Dread |
| 9 | 32-36 | 50 mm from SE of mother, rack focus | Crowd rushes past (speed-ramped), snaps to normal at 33.4 s with the focus rack. Mother turns, smile fades, looks down at the empty spot beside her | Realisation |
| 10 | 36-41 | 24 mm drone straight down (40 m up) | Father, mother, uncle, cousin run out from one point in four directions like a crack. White rings under them so they read from above | Panic, geography lost in the crowd |
| 11 | 41-45 | 25 mm handheld, three inserts with whip pans (110 deg in 0.2 s) | Father at the jhoola, mother at the toy stall, uncle at the food carts, each cupping hands to call "Dhruv!" | Frantic |
| 12 | 45-49 | 35 mm slow track in from (5.2,0.4) to (7.6,0.9) | Parents hurry east toward the vendor. A second bunch of balloons frames the foreground. Vendor half hidden behind his bunch | Foreshadow |
| 13 | 49-52 | 50 mm handheld over the vendor's shoulder | Father, bent over and breathless, asks his question; mother behind him afraid. Vendor listens | Urgent |
| 14 | 52-57 | 85 mm, slightly low, from the north-west, f/2.2 | Vendor answers too fast, glances at the gate, points east with his arm, mouth moving rapidly. Neutral, no tell | Quietly wrong |
| 15 | 57-62 | 35 mm handheld from behind, desaturated veil + dim lights | RECREATION: two black silhouettes walk up to Dhruv at the pole, thin one with the cap crouches and gives him a red balloon, they lead him to the white van. Backs only | "Told" version, washed out |
| 16 | 62-68 | 100 mm ECU pushing in 1.35 m to 1.0 m | Father's face; brows knit, mouth trembling, sweat drops run down. Mother's hand grips his arm at the frame edge | The words land |
| 17 | 68-77 | 24 mm crane: ground level up to 170 m, then through 3 map cards (up to 22 km) | Parents frozen below, mother's hand over mouth, vendor still at the pole. Then the VFX map zoom (placeholder cards: MELA GROUND, MIRZAPUR, UTTAR PRADESH, UP POLICE HQ) | Fall away from the family |
| 18 | 77-95 | 100 mm macro slider on 5 props, then 35 mm for the ladder | Three stars on a shoulder patch, Ashoka emblem, belt buckle, name plate "RAVI", badge, then a 10-rung rank ladder (Constable to DGP) builds and "SHO? IO? CO?" pops. Rim-lit on black | Authority, procedural |
| 19 | 95-102 | 50 mm static, low | One red balloon rises out of black frame; title pops in: OPERATION / RED (red) / BALLOON | Title hit |

## Things I decided that the sheet did not say (change these if wrong)
- Shot 6 camera is placed so Dhruv's face is visible and the parents' faces are cut by the frame top (the sheet note).
- Shots 3, 4, 6, 7 happen at two spots: the lane (x -10 to -4) and the bargaining stall (x 3). The family moves between them across the cuts.
- The vendor's bunch has exactly one hero red balloon; the two extra reds in the bunch are lower and smaller. Red appears nowhere else, only on balloons.
- Shot 15 grade is done with a translucent grey veil in front of the lens plus dimmer lights, since the preview has no colour grading.
- Shot 17 and 18 graphics are placeholders: flat cards and bars. The real VFX map and rank ladder replace them.
- Only the lens numbers come from the sheet. Camera positions, paths and timings are mine.
- No audio. Captions in the preview MP4 show the shot number, lens/move and the VO line from the sheet.

## Known rough edges
- People are low-poly mannequins: no fingers, no cloth. Gestures are readable, not fine acting.
- Foot sliding when characters turn in place.
- Crowd walkers glide (no leg cycle); only the cast and 14 featured extras have walk cycles.
- Shot 7 uses separate prop hands, not the mannequins.
