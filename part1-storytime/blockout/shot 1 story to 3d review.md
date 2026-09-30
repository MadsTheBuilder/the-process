# Shot 1 story to 3d review

Source: `blockout/red_balloon_p1_compare.mp4` (left = animated storyboard v3, right = Blender blockout), 27 shots, 102.3 s.
Method: 3 frames per shot (start, middle, end) judged against the storyboard panel. Percentages are director's estimates.

**Overall match: about 44%.** Durations and cut points match exactly. Framing, camera axis, cast blocking and set dressing drift.

## Problems that repeat across shots

1. **Cameras sit at right angles to the lane.** Boards use a symmetrical one-point view down the lane (lane runs along +X at y≈0 in scene.py). 1A, 1B, 4C, 5A, 5E look sideways or diagonally. Fixing this recovers about five shots.
2. **Wides have no crowd.** 1A and 4C need a dense, desaturated crowd; only the family and leads carry saturated colour.
3. **Set pieces from the boards are missing.** Ferris-wheel bokeh (2A, 4B), balloon bunch behind seller (5C, 5D), seller's red-white gamchha (5C), Mela Chowki tent and cool lamp (6A), jalebi counter glow (3A).
4. **No warm/cool light split.** Faces are lit evenly in blue. Boards have a 3000K warm key on one cheek, cool fill on the other, background to bokeh. 5D, 5F, 5G backgrounds are still in focus.
5. **Adult occluders too bright and close.** In 3B they should be dark silhouettes at the frame corners.

## Shot by shot

| Shot | Match | What is off and what to change |
|---|---|---|
| 0A | 35% | Board is a map-to-mela zoom locked on the marker. 3D is a dark top-down block grid ending straight down, which doesn't connect to 1A's oblique view. Pitch from ~90° to ~60° by the end; put the map plate on the ground as a texture. |
| 1A | 30% | Board: camera on the lane axis, high, lane converging at centre, stalls both sides. 3D camera at (0..4, −14) looking at (80,0,0) sees the lane from the side. Camera to y≈0, z≈6, look down +X with ~15° pitch, push along the axis. Add crowd. |
| 1B | 35% | Board looks down the lane with two dark occluders at left/right edges, warm stall glow, bulb strings, small ferris wheel. 3D looks 90° across into a stall wall (camera and target x move together). Aim along +X and drift across; one backlit occluder per frame edge; open the roof so the bulbs show. |
| 2A | 40% | Board: four family members facing camera in a clear line at centre-left between two dark occluders. 3D: father hides Dhruv; sister and mother barely readable. Stagger in a line perpendicular to the lens ~0.5 m apart, facing camera; crowd behind and beside only. |
| 2B | 75% | Best match. Order and wardrobe right. Extra bystanders crowd both edges (board is clean) and no warm rim on faces. Clear edge extras; add warm key from camera-left. |
| 2C | 65% | Board: Dhruv left third, three-quarter to the right, sister soft at right. 3D: centred, frontal, sister (orange blur) on the wrong (left) side. Move Dhruv left, turn head ~25° right, sister behind at frame-right, light his left cheek. |
| 3A | 35% | Board: father cropped at left edge, Dhruv pointing up at balloons, mother and sister small in mid-ground at the counter. 3D: mother and Dhruv stacked in foreground, sister missing, no jalebi counter or balloons. Pull camera back ~2.5 m, mother and sister 3 m deep, add glowing counter at left and balloons top right, Dhruv's arm up and right. |
| 3B | 55% | Board: Dhruv centred, eyes moving parents to balloons, dark shoulders at bottom corners. 3D: bright white and orange adult blocks, gaze never moves. Darken adults to ~15% and move to corners, add bokeh bulbs, rotate head left to right over the shot. |
| 3C | 40% | Board: family in left third with heads in frame, Dhruv mid-lane, then an empty child-height gap. 3D: family cropped, large passer-by crosses the centre, gap filled. Camera left and back so all three adults fit in the left third, smaller passer-by, keep centre empty after Dhruv exits. |
| 4A | 30% | Board: father and mother in profile at frame edges, heads visible, empty centre, bokeh crowd. 3D: both heads cropped, counter tray fills centre. Lens ~65mm or pull back 1.5 m, separate the adults, lower the counter out of frame, mother looks past lens. |
| 4B | 45% | Board: mother in left third looking right, big ferris-wheel bokeh, glowing toy stall at right. 3D has neither. Emissive wheel ring behind right side, warm stall glow lower right, gaze up to wheel then down to stall. |
| 4C | 30% | Board: symmetrical wide from 2.4 m, trio at centre, wheel upper left. 3D camera (72,4) looking toward (52,−5) is off-axis and rotated; family lost in crowd. Camera to y≈0, saturated colour on the three leads, mute the crowd. |
| 4D | 50% | Board: father right third in light blue, whole wheel upper left, queue in bright non-blue jackets. 3D: father looks navy and centred (a blue jacket, contradicting the note), wheel only a few beams. Shift him to right third, lighten his shirt, tilt up ~8° or pull back to show the full wheel. |
| 5A | 45% | Board looks down the lane with parents already walking in from the left. 3D looks side-on at the stall wall; parents appear only in the last 0.4 s. Yaw toward the gate for depth, parents at left edge on frame one, show the whole balloon bunch. |
| 5B | 40% | Board: father, mother, seller at similar scale, father's hand low at child height. 3D: seller tiny and far, mother hidden behind father, father's arm straight out horizontal. All three at the same depth ~3.5 m from camera; bend his arm with hand at ~1.05 m. |
| 5C | 50% | Board: seller right of centre in red-white gamchha, balloons soft behind, dark bokeh. 3D: plain cream kurta, stall behind. Add gamchha, balloons behind, darken background. |
| 5D | 45% | Board: seller holds up two fingers at chest height, father's head soft at left edge, balloons top right. 3D: whole arm straight up, bright in-focus stall background. Elbow 90°, two-finger hand at shoulder height, add balloons, darken and blur background. |
| 5E | 25% | Worst in the sequence. Board is a tight three-shot, seller pointing to the gate at left. 3D camera ~16 m away, group is three small figures. Camera to ~5 m, group in right half, empty lane and gate at frame-left, parents turn toward the gate. |
| 5F | 55% | Board: mother left third, father cropped at right edge, soft. 3D: father centred behind her, stalls in focus. Shift father ~0.6 m off-axis so he crops at the edge, raise DOF blur. |
| 5G | 45% | Board: father screen-left, mother screen-right, level, shoulder to shoulder. 3D: swapped and at different depths (mother front-left, father back-right). Swap y values (father ~2.5, mother ~3.1), same x. Add sweat dots. |
| 6A | 40% | Board: trio small in the lane, empty dark road, Mela Chowki tent with cool lamp and mast at the end. 3D: parents and seller large in the foreground, crowd down the lane, no tent. Start pull-back from ~14 m at z≈3.2, thin the crowd, add the blue-lit tent and mast. |
| 6B | 55% | Board: host at left third, dark charcoal-blue set, right half empty for ladder composite. 3D: bright orange desk, physical ladder on the right, stray white rectangle at left, tan wall. Matte charcoal desk, remove physical ladder and white rectangle, add a cool background light on the right. |
| 6C | 55% | Board: host at chest height, ladder inside the right third. 3D: hands and desk visible, ladder against the right edge. Raise camera or push in ~0.6 m to lose hands and desk; move ladder ~0.6 m left. |
| 6D | 65% | Close. Board has a faint ladder echo at frame-right (~35%) and a cool practical; 3D has neither and the head sits slightly left. Add ladder echo and small cool light; nudge host right. |
| 6E | 20% | Board: face-on khaki uniform chest, three stars on the epaulette, blank nameplate. 3D: top surface of a box with two block shapes at a grazing angle, reads as a table. Curved chest panel facing the lens, three extruded stars on the epaulette, black nameplate bar, shoot perpendicular from ~0.9 m with raking light. |
| 6F | 50% | Board: host head ~27%, ladder ~60%, room on the right for tags. 3D: host cropped at left, ladder at right edge. Move host and ladder ~1 m toward centre, keep the right side clear. |
| 6G | 40% | Board: flat graphic, ladder fills the frame, tilt up to the top rung. 3D: small perspective ladder in a room with floor and wall, ending with most of the frame empty. Long lens or orthographic camera on a flat dark background, ladder ~90% of frame height, end tilt with top rung in the upper third. |

## Suggested first fix pass (scene.py)

Re-aim cameras in 1A, 1B, 4C, 5A, 5E onto the lane axis; swap the 5G father/mother positions; then re-render `red_balloon_p1_compare.mp4`.
