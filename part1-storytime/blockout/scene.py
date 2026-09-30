# scene.py — Operation Red Balloon, Part 1: 3D blockout of animatic v3 (27 shots, 102.3s, 25 fps).
# Build (isolated user dir, never the plain blender binary):
#   ~/.claude/skills/create-3d-scene/scripts/blender.sh -P scene.py -- <abs>/red_balloon_p1.blend
#
# One camera, cut per shot. Everything is baked per frame from SHOTS (camera) and stage() (cast),
# so edit those and re-run. Shot data mirrors the SHOTS table in ../index.html.
#
# World (metres): the mela lane runs along +X from the gate (x=10) to the clock tower (x=150),
# lane is y in [-4, 4], stalls line both sides. Figures face +X at yaw 0 (their left = +Y).
# Narrator set lives far away at NARR (y=400) inside a closed room.
import math
import os
import random
import sys

import bmesh
import bpy
from mathutils import Matrix, Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scene_kit import seg, lerp, vlerp, look_quat, mat, add_box, join, empty, light, collection, move_to, markers, set_interpolation  # noqa: E402

OUT = sys.argv[sys.argv.index("--") + 1]
FPS, DUR = 25, 102.3
NF = int(round(DUR * FPS))

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.fps = FPS
scene.frame_start, scene.frame_end = 1, NF
scene.render.resolution_x, scene.render.resolution_y = 1920, 1080
scene.render.engine = "BLENDER_EEVEE"
scene.eevee.taa_render_samples = 16
random.seed(7)

# ---------------------------------------------------------------- key places
CX = 40.8                          # jalebi counter stall (+Y side)
SELLER = Vector((76.3, 2.85, 0))   # balloon seller's spot
FERRIS = Vector((58, -15, 9.5))    # jhoola, behind the junction gap on the -Y side
GATE_X = 10.0                      # mela gate / lane entrance; the Mela Chowki sits beside it
CHOWKI = Vector((15, -6.6, 0))
TOWER = Vector((150, 0, 0))
NARR = Vector((0, 400, 0))         # narrator set origin
HOST = NARR + Vector((-0.9, 0.15, 0))
LADDER = NARR + Vector((1.35, 1.9, 0))
UNIFORM = NARR + Vector((2.9, 0.6, 0))

# ---------------------------------------------------------------- materials
M = {k: mat(k, *v) for k, v in {
    "ground": ((0.33, 0.27, 0.2),), "lane": ((0.5, 0.42, 0.32),), "city": ((0.55, 0.5, 0.42),),
    "roof": ((0.4, 0.36, 0.32),), "river": ((0.1, 0.16, 0.22), 0.2),
    "skin": ((0.5, 0.32, 0.22),), "hair": ((0.03, 0.03, 0.03),),
    "father_top": ((0.62, 0.76, 0.95),), "father_bot": ((0.06, 0.08, 0.22),),
    "sari": ((0.9, 0.85, 0.72),), "sari_border": ((0.62, 0.2, 0.08),),
    "dhruv_top": ((0.04, 0.12, 0.62),), "jeans": ((0.25, 0.38, 0.6),), "white": ((0.95, 0.95, 0.95),),
    "sister_top": ((0.95, 0.38, 0.08),),
    "kurta": ((0.88, 0.85, 0.76),), "lungi": ((0.12, 0.2, 0.42),), "gamchha": ((0.75, 0.25, 0.25),),
    "jhola": ((0.35, 0.22, 0.12),), "host": ((0.09, 0.09, 0.11),), "host_shirt": ((0.7, 0.72, 0.75),),
    "steel": ((0.6, 0.6, 0.62), 0.3, 0.8), "wood": ((0.25, 0.15, 0.08),), "pan": ((0.05, 0.05, 0.05), 0.3, 0.7),
    "jalebi": ((1.0, 0.55, 0.05), 0.4, 0, (1.0, 0.5, 0.05), 0.4),
    "cream": ((0.85, 0.8, 0.68),), "gate_red": ((0.55, 0.08, 0.05),), "khaki": ((0.55, 0.47, 0.3),),
    "navy": ((0.05, 0.06, 0.12),), "gold": ((0.9, 0.7, 0.2), 0.3, 1.0, (1.0, 0.75, 0.3), 0.3),
    "rust": ((0.7, 0.2, 0.06), 0.5, 0, (0.8, 0.22, 0.05), 1.5), "rung": ((0.62, 0.52, 0.36),),
    "room": ((0.13, 0.12, 0.1), 0.8), "clock": ((1, 0.95, 0.8), 0.5, 0, (1, 0.9, 0.7), 3.0),
    "bulb": ((1, 0.8, 0.5), 0.5, 0, (1.0, 0.62, 0.3), 25.0),
    "stall_bulb": ((1, 0.8, 0.5), 0.5, 0, (1.0, 0.62, 0.3), 40.0),
    "cool_lamp": ((0.6, 0.8, 1), 0.5, 0, (0.45, 0.65, 1.0), 30.0),
}.items()}
TARPS = [mat(f"tarp_{i}", c) for i, c in enumerate([(0.08, 0.25, 0.65), (0.7, 0.12, 0.08), (0.85, 0.6, 0.08), (0.1, 0.45, 0.25), (0.85, 0.82, 0.75)])]
GOODS = [mat(f"goods_{i}", c) for i, c in enumerate([(0.9, 0.2, 0.3), (0.2, 0.6, 0.9), (0.95, 0.8, 0.1), (0.3, 0.8, 0.3), (0.9, 0.5, 0.1), (0.6, 0.3, 0.8)])]
BALLOON = [mat(f"balloon_{i}", c, 0.3) for i, c in enumerate([(0.85, 0.02, 0.02), (0.05, 0.2, 0.9), (0.98, 0.8, 0.02), (0.1, 0.7, 0.15), (0.98, 0.45, 0.02), (0.95, 0.3, 0.6)])]
CROWD = [mat(f"crowd_{i}", c) for i, c in enumerate([(0.32, 0.34, 0.42), (0.45, 0.36, 0.3), (0.28, 0.33, 0.28), (0.5, 0.45, 0.4), (0.38, 0.28, 0.32), (0.22, 0.24, 0.3)])]
KIDS = [mat(f"kid_{i}", c) for i, c in enumerate([(0.8, 0.1, 0.1), (0.95, 0.8, 0.1), (0.2, 0.65, 0.2), (0.95, 0.4, 0.6), (0.95, 0.5, 0.1), (0.45, 0.08, 0.15)])]

C_SET, C_CAST, C_CROWD, C_NARR, C_LIGHT = (collection(n) for n in ("Set_Mela", "Cast", "Crowd", "Set_Narrator", "Lights"))


def ops_add(fn, coll, material, name, **kw):
    fn(**kw)
    ob = bpy.context.active_object
    ob.name = name
    ob.data.materials.append(material)
    move_to(ob, coll)
    return ob


def box(name, loc, size, material, coll, rot=(0, 0, 0)):
    return add_box(name, loc, size, material, rot=rot, coll=coll)


def sphere(name, loc, r, material, coll):
    return ops_add(bpy.ops.mesh.primitive_uv_sphere_add, coll, material, name, segments=16, ring_count=8, radius=r, location=loc)


def cyl(name, loc, r1, r2, depth, material, coll, rot=(0, 0, 0)):
    return ops_add(bpy.ops.mesh.primitive_cone_add, coll, material, name, vertices=16, radius1=r1, radius2=r2, depth=depth, location=loc, rotation=rot)


# ---------------------------------------------------------------- fast baked keys
IP = {"CONSTANT": "CONSTANT", "LINEAR": "LINEAR"}


def fk(idb, path, idx, values, interp="CONSTANT"):
    """values: one per frame (frame 1..NF). Consecutive repeats are dropped; CONSTANT keeps them exact."""
    ad = idb.animation_data or idb.animation_data_create()
    if ad.action is None:
        ad.action = bpy.data.actions.new(f"{idb.name}_act")
    fc = ad.action.fcurve_ensure_for_datablock(idb, path, index=idx)
    pts = [(i + 1, v) for i, v in enumerate(values) if i == 0 or v != values[i - 1] or i == len(values) - 1]
    fc.keyframe_points.add(len(pts))
    fc.keyframe_points.foreach_set("co", [c for p in pts for c in p])
    for k in fc.keyframe_points:
        k.interpolation = interp
    fc.update()


def fk_vec(idb, path, vecs, interp="CONSTANT"):
    for i in range(len(vecs[0])):
        fk(idb, path, i, [round(v[i], 5) for v in vecs], interp)


# ---------------------------------------------------------------- figures
def figure(name, H, top, bottom, kind="adult", coll=C_CAST, rig=True, stripes=False):
    """Box-and-sphere person, feet at origin, facing +X. Returns (root, {'L': arm, 'R': arm}) or a joined mesh if rig=False."""
    hr = H * (0.078 if kind == "kid" else 0.062)
    hip = H * 0.48
    sh = H - 2 * hr - H * 0.035
    tw, tb = H * 0.11, H * (0.22 if kind == "kid" else 0.2)
    aw, al = H * 0.05, H * 0.36
    hz = sh + H * 0.035 + hr
    p = []
    if kind == "sari":
        p.append(cyl("skirt", (0, 0, hip / 2 + 0.02), tb * 0.7, tb * 0.48, hip + 0.04, bottom, coll))
        p.append(cyl("border", (0, 0, 0.05), tb * 0.72, tb * 0.7, 0.09, M["sari_border"], coll))
        p.append(box("pallu", (0.01, 0.0, (hip + sh) / 2), (tw * 1.08, 0.08, sh - hip), M["sari_border"], coll, rot=(math.radians(35), 0, 0)))
    elif kind == "kurta":
        p.append(box("lungi", (0, 0, hip / 2), (tw * 1.1, tb * 0.95, hip), bottom, coll))
        p.append(box("kurta_low", (0, 0, hip * 0.8), (tw * 1.08, tb * 1.03, hip * 0.45), top, coll))
    else:
        for s in (1, -1):
            p.append(box("leg", (0, s * tb * 0.26, hip / 2), (tw * 0.8, tb * 0.42, hip), bottom, coll))
    p.append(box("torso", (0, 0, (hip + sh) / 2), (tw, tb, sh - hip + 0.03), top, coll))
    if stripes:
        p.append(box("zip", (tw / 2 + 0.003, 0, (hip + sh) / 2), (0.01, 0.02, sh - hip), M["white"], coll))
    p.append(box("neck", (0, 0, sh + H * 0.02), (H * 0.04, H * 0.05, H * 0.05), M["skin"], coll))
    p.append(sphere("head", (0, 0, hz), hr, M["skin"], coll))
    p.append(sphere("hair", (-hr * 0.28, 0, hz + hr * 0.22), hr * 1.02, M["hair"], coll))
    p.append(box("nose", (hr * 0.95, 0, hz - hr * 0.1), (hr * 0.35, hr * 0.28, hr * 0.35), M["skin"], coll))
    arms = {}
    for s, lab in ((1, "L"), (-1, "R")):
        pivot = Vector((0, s * (tb / 2 + aw / 2 + 0.006), sh - 0.03))
        ap = [box("arm", pivot - Vector((0, 0, al / 2)), (aw, aw, al), top, coll),
              sphere("hand", pivot - Vector((0, 0, al + aw * 0.4)), aw * 0.7, M["skin"], coll)]
        if stripes:
            ap.append(box("stripe", pivot + Vector((0, s * aw / 2, -al / 2)), (0.012, 0.01, al), M["white"], coll))
        arm = join(ap, f"{name}_arm{lab}")
        if rig:
            scene.cursor.location = pivot
            bpy.ops.object.select_all(action="DESELECT")
            arm.select_set(True)
            bpy.context.view_layer.objects.active = arm
            bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
            arms[lab] = arm
        else:
            p.append(arm)
    body = join(p, f"{name}_body")
    if not rig:
        return body
    root = empty(name, coll=coll)
    for ob in [body, *arms.values()]:
        ob.parent = root
    return root, arms


def balloon_bunch(name, base, coll, n=14, spread=0.35, height=2.55):
    parts = [box("stick", base + Vector((0, 0, (height - base.z) / 2 - 0.1)), (0.02, 0.02, height - base.z - 0.2), M["wood"], coll)]
    for i in range(n):
        a = random.uniform(0, math.tau)
        rr = random.uniform(0, spread)
        parts.append(sphere("b", base + Vector((rr * math.cos(a), rr * math.sin(a), height - base.z + random.uniform(-0.3, 0.35))),
                            random.uniform(0.13, 0.18), BALLOON[i % len(BALLOON)], coll))
    return join(parts, name)


# ---------------------------------------------------------------- the mela set
def build_city():
    """Map/rooftop context in one mesh: city blocks round the mela, a river north, open ground elsewhere."""
    me = bpy.data.meshes.new("City")
    bm = bmesh.new()
    for x in range(-260, 420, 16):
        for y in range(-300, 300, 16):
            if -14 < y < 14 and 0 < x < 162:           # the mela strip
                continue
            if -20 < x < 30 and -40 < y < 0:          # keep 1A's rooftop view clear
                continue
            if (x - FERRIS.x) ** 2 + (y - FERRIS.y) ** 2 < 14 ** 2 or 200 < y < 250:
                continue
            w, d, h = random.uniform(8, 14), random.uniform(8, 14), random.choice([4, 5, 6, 7, 8, 10, 12, 15])
            bmesh.ops.create_cube(bm, size=1, matrix=Matrix.Translation((x + 8, y + 8, h / 2)) @ Matrix.Diagonal((w, d, h, 1)))
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("City", me)
    C_SET.objects.link(ob)
    me.materials.append(M["city"])
    box("Ground", (80, 0, -0.05), (1400, 1400, 0.1), M["ground"], C_SET)
    box("River", (80, 225, 0.01), (1400, 50, 0.02), M["river"], C_SET)
    box("Lane", (80, 0, 0.005), (142, 8.4, 0.01), M["lane"], C_SET)
    box("Rooftop_1A", (-1, -15.5, 2.9), (10, 7, 5.8), M["roof"], C_SET)   # the rooftop 1A is shot from


def stall(x, side, tarp, counter_mat=None, lit=True):
    y0 = side * 4.2
    parts = [box("counter", (x, y0 + side * 0.3, 0.45), (3.2, 0.55, 0.9), counter_mat or M["wood"], C_SET),
             box("back", (x, side * 7.0, 1.2), (3.3, 0.1, 2.4), random.choice(CROWD), C_SET),
             box("roof", (x, side * 5.6, 2.75), (3.5, 3.2, 0.05), tarp, C_SET, rot=(side * math.radians(-8), 0, 0)),
             box("bulb", (x, side * 4.5, 2.45), (0.12, 0.12, 0.12), M["stall_bulb"], C_SET)]
    for dx in (-1.6, 1.6):
        parts.append(box("post", (x + dx, y0, 1.35), (0.07, 0.07, 2.7), M["wood"], C_SET))
    for i in range(4):
        parts.append(box("goods", (x - 1.2 + i * 0.8, y0 + side * 0.35, 0.9 + 0.12), (0.5, 0.35, 0.25), random.choice(GOODS), C_SET))
    ob = join(parts, f"Stall_{'L' if side > 0 else 'R'}_{x:.1f}")
    if lit:
        pl = bpy.data.objects.new(f"Practical_{ob.name}", PRACTICAL)
        C_LIGHT.objects.link(pl)
        pl.location = (x, side * 5.2, 2.3)
    return ob


PRACTICAL = bpy.data.lights.new("Practical_3000K", "POINT")   # one datablock shared by every stall light
PRACTICAL.energy, PRACTICAL.color, PRACTICAL.shadow_soft_size = 90, (1.0, 0.64, 0.36), 0.3
PRACTICAL.use_shadow = False

build_city()
STALL_XS = [12 + 3.6 * k for k in range(36)]
for i, x in enumerate(STALL_XS):
    for side in (1, -1):
        if side == -1 and 50 < x < 66:       # junction gap toward the ferris wheel
            continue
        if side == 1 and abs(x - CX) < 0.1:
            continue
        stall(x, side, TARPS[(i + (side > 0)) % len(TARPS)])

# jalebi counter (the family's stall, board 01B)
stall(CX, 1, TARPS[1], counter_mat=M["steel"])
cyl("Jalebi_Pan", (CX - 0.6, 4.55, 0.95), 0.4, 0.35, 0.1, M["pan"], C_SET)
for i in range(6):
    cyl("Jalebi", (CX + 0.3 + (i % 3) * 0.35, 4.45 + (i // 3) * 0.3, 0.93), 0.13, 0.13, 0.04, M["jalebi"], C_SET)

# bulb strings across the lane
for x in range(13, 140, 7):
    for s in (1, -1):
        box("Pole", (x, s * 4.1, 2.4), (0.08, 0.08, 4.8), M["wood"], C_SET)
    bulbs = [box("b", (x, lerp(-4.1, 4.1, i / 10), 4.6 - 0.5 * math.sin(math.pi * i / 10)), (0.09, 0.09, 0.12), M["bulb"], C_SET) for i in range(11)]
    join(bulbs, f"BulbString_{x}")

# balloon cluster tied to the string near the counter (peeks top-right in 3A)
balloon_bunch("Balloons_String", Vector((CX + 2.7, 1.6, 1.6)), C_SET, n=7, spread=0.2, height=2.15)

# ferris wheel (jhoola)
hub = empty("Ferris_Hub", FERRIS, coll=C_SET)
hub.rotation_euler = (math.radians(90), 0, math.radians(30))
wheel = [ops_add(bpy.ops.mesh.primitive_torus_add, C_SET, M["steel"], "rim", major_radius=8, minor_radius=0.12, location=(0, 0, 0))]
for i in range(8):
    wheel.append(box("spoke", (0, 0, 0), (16, 0.08, 0.08), M["steel"], C_SET, rot=(0, 0, i * math.pi / 8)))
for i in range(24):
    a = i * math.tau / 24
    wheel.append(box("rimbulb", (8 * math.cos(a), 8 * math.sin(a), 0), (0.25, 0.25, 0.25), M["bulb"], C_SET))
for i in range(8):
    a = i * math.tau / 8
    wheel.append(box("cabin", (8 * math.cos(a), 8 * math.sin(a) - 0.7, 0), (0.9, 0.9, 0.9), TARPS[i % 5], C_SET))
wheel_ob = join(wheel, "Ferris_Wheel")
wheel_ob.parent = hub
for s in (1, -1):
    for f in (1, -1):
        leg = box("Ferris_Leg", (0, 0, 0), (0.25, 0.25, 11), M["steel"], C_SET, rot=(0, s * math.radians(18), 0))
        leg.location = FERRIS + Vector((f * 0.9, 0, -4.75)) + Vector((s * 1.7, 0, 0))
        leg.rotation_euler.z = math.radians(30)
box("Jhoola_Rail", (59, -10.8, 0.5), (6.5, 0.06, 1.0), M["steel"], C_SET)

# clock tower, gate, Mela Chowki
box("ClockTower", TOWER + Vector((0, 0, 12)), (6, 6, 24), M["cream"], C_SET)
box("ClockTower_Top", TOWER + Vector((0, 0, 25)), (7, 7, 2), M["cream"], C_SET)
cyl("ClockTower_Spire", TOWER + Vector((0, 0, 28)), 2.5, 0.2, 4, M["cream"], C_SET)
box("Clock_Face", TOWER + Vector((-3.05, 0, 21)), (0.1, 3, 3), M["clock"], C_SET)
for s in (1, -1):
    box("Gate_Pillar", (GATE_X, s * 5, 3), (1, 1, 6), M["gate_red"], C_SET)
box("Gate_Beam", (GATE_X, 0, 6.4), (1, 11, 1.2), M["gate_red"], C_SET)
box("Chowki_Tent", CHOWKI + Vector((0, 0, 1.25)), (4, 3, 2.5), M["khaki"], C_SET)
box("Chowki_Roof", CHOWKI + Vector((0, 0, 2.7)), (4.4, 3.4, 0.3), M["cream"], C_SET)
box("Chowki_Mast", CHOWKI + Vector((2.3, -1.5, 4.5)), (0.1, 0.1, 9), M["steel"], C_SET)
box("Chowki_Lamp", CHOWKI + Vector((0, 1.6, 2.4)), (0.3, 0.1, 0.3), M["cool_lamp"], C_SET)
chowki_light = light("Chowki_Light", "POINT", CHOWKI + Vector((0, 2.0, 2.4)), 400, coll=C_LIGHT, color=(0.5, 0.7, 1.0), use_shadow=False)

# ---------------------------------------------------------------- the narrator set
for nm, loc, size in (("Floor", (0, 0.5, 0), (10, 7, 0.05)), ("Wall_Back", (0, 2.4, 2.75), (10, 0.1, 5.5)),
                      ("Wall_L", (-5, 0.5, 2.75), (0.1, 7, 5.5)), ("Wall_R", (5, 0.5, 2.75), (0.1, 7, 5.5)),
                      ("Ceiling", (0, 0.5, 5.5), (10, 7, 0.1))):
    box(f"Narr_{nm}", NARR + Vector(loc), size, M["room"], C_NARR)
box("Narr_Desk", HOST + Vector((0, -0.55, 0.38)), (1.4, 0.6, 0.76), M["wood"], C_NARR)
box("Narr_Practical", NARR + Vector((-2.7, 2.1, 1.7)), (0.3, 0.3, 0.7), M["cool_lamp"], C_NARR)
narr_practical = light("Narr_Practical_Light", "POINT", NARR + Vector((-2.7, 1.8, 1.7)), 60, coll=C_LIGHT, color=(0.5, 0.7, 1.0))
for s in (1, -1):
    box("Ladder_Rail", LADDER + Vector((s * 0.3, 0, 2.3)), (0.06, 0.06, 4.6), M["rung"], C_NARR)
for i in range(9):
    box("Ladder_Rung_TOP" if i == 8 else "Ladder_Rung", LADDER + Vector((0, 0, 0.4 + i * 0.5)), (0.6, 0.05, 0.06), M["rust"] if i == 8 else M["rung"], C_NARR)
box("Uniform_Pole", UNIFORM + Vector((0, 0, 0.45)), (0.05, 0.05, 0.9), M["steel"], C_NARR)
box("Uniform_Torso", UNIFORM + Vector((0, 0, 1.16)), (0.44, 0.24, 0.62), M["khaki"], C_NARR)
box("Uniform_Belt", UNIFORM + Vector((0, 0, 0.9)), (0.45, 0.25, 0.05), M["wood"], C_NARR)
for s in (1, -1):
    box("Uniform_Epaulette", UNIFORM + Vector((s * 0.16, 0, 1.48)), (0.13, 0.07, 0.02), M["navy"], C_NARR)
    for j in range(2):
        box("Uniform_Star", UNIFORM + Vector((s * (0.12 + 0.06 * j), 0, 1.5)), (0.03, 0.03, 0.015), M["gold"], C_NARR)
    box("Uniform_Badge", UNIFORM + Vector((s * 0.11, -0.125, 1.28)), (0.06, 0.01, 0.06), M["gold"], C_NARR)

# ---------------------------------------------------------------- cast
CAST = {}
CAST["father"] = figure("Father", 1.75, M["father_top"], M["father_bot"])
CAST["mother"] = figure("Mother", 1.6, M["sari_border"], M["sari"], kind="sari")
CAST["dhruv"] = figure("Dhruv", 1.25, M["dhruv_top"], M["jeans"], kind="kid", stripes=True)
CAST["sister"] = figure("Sister", 1.38, M["sister_top"], M["jeans"], kind="kid")
CAST["seller"] = figure("Seller", 1.72, M["kurta"], M["lungi"], kind="kurta")
CAST["host"] = figure("Host", 1.78, M["host"], M["host"])
CAST["passer"] = figure("Passerby_3C", 1.7, CROWD[1], CROWD[5])
CAST["occ1"] = figure("Occluder_1B_a", 1.72, CROWD[0], CROWD[5])
CAST["occ2"] = figure("Occluder_1B_b", 1.6, CROWD[4], CROWD[2])
for i in range(6):
    CAST[f"kid{i}"] = figure(f"QueueKid_{i}", random.uniform(1.05, 1.3), KIDS[i], CROWD[5], kind="kid")
sroot = CAST["seller"][0]
for part in (balloon_bunch("Seller_Balloons", Vector((0.25, 0.3, 1.15)), C_CAST, n=16),
             box("Seller_Jhola", (-0.02, -0.24, 0.95), (0.12, 0.3, 0.34), M["jhola"], C_CAST),
             box("Seller_Gamchha", (0.07, 0.1, 1.22), (0.03, 0.1, 0.5), M["gamchha"], C_CAST)):
    part.parent = sroot
box("Host_Shirt", (0.057, 0, 1.38), (0.01, 0.1, 0.22), M["host_shirt"], C_CAST).parent = CAST["host"][0]

# ---------------------------------------------------------------- cast staging (per shot)
FAM_COUNTER = {"father": (CX - 0.8, 3.35, 90), "dhruv": (CX - 0.45, 2.85, 60), "mother": (CX + 0.45, 3.4, 90), "sister": (CX + 1.15, 3.3, 90)}
F5, M5 = Vector((73.6, 1.6, 0)), Vector((73.2, 2.5, 0))     # parents at the seller
TO_SELLER_F = math.degrees(math.atan2(SELLER.y - F5.y, SELLER.x - F5.x))
TO_SELLER_M = math.degrees(math.atan2(SELLER.y - M5.y, SELLER.x - M5.x))
HIDE = (0, -500)
POINT, SHOW_HEIGHT, TUG, TWO_FINGERS, EAT, HOLD = (-95, 0), (-60, 0), (-45, 25), (-160, 10), (-120, 25), (-55, 0)


def S(x, y, yaw, L=(0, 0), R=(0, 0), vis=True):
    return {"pos": (x, y), "yaw": yaw, "L": L, "R": R, "vis": vis}


def walk(p0, p1, u):
    p = vlerp(p0, p1, u)
    return p.x, p.y, math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0]))


def stage(sid, tau, dur):
    """Cast placements for shot `sid` at tau seconds into it. Anyone not named keeps their previous state."""
    u = tau / dur
    if sid == "s0a":
        return {"father": S(31.0, 0.4, -150), "dhruv": S(31.4, 0.9, -150), "sister": S(31.9, 1.3, -150), "mother": S(32.3, 1.7, -150),
                "seller": S(SELLER.x, SELLER.y, 200, L=HOLD), "host": S(HOST.x, HOST.y, -90),
                "passer": S(*HIDE, 0, vis=False), "occ1": S(22.9, -1.35, 0), "occ2": S(24.7, -0.9, 180),
                **{f"kid{i}": S(57.9 + i * 0.6, -10.25, 0) for i in range(6)}}
    if sid == "s1b":   # two foreground occluders drift across the lens
        return {"occ1": S(22.4 + 1.2 * u, -1.35, 0), "occ2": S(25.2 - 0.9 * u, -0.9, 180)}
    if sid == "s2a":
        return {"occ1": S(*HIDE, 0, vis=False), "occ2": S(*HIDE, 0, vis=False)}
    if sid == "s2b":   # four-shot walking +X toward the retreating camera
        x = 29 + 1.0 * tau
        return {"father": S(x, -0.75, 0), "dhruv": S(x + 0.15, -0.25, 0), "sister": S(x + 0.1, 0.25, 0), "mother": S(x, 0.75, 0)}
    if sid == "s2c":
        return {"dhruv": S(33.0, 0.5, 180), "sister": S(34.3, 1.2, 190), "father": S(34.2, -0.7, 180), "mother": S(34.6, 1.9, 180)}
    if sid == "s3a":   # at the counter: Dhruv tugs the sleeve and points; mother and sister eat
        st = {k: S(*v) for k, v in FAM_COUNTER.items()}
        st["dhruv"] = S(*FAM_COUNTER["dhruv"], L=TUG, R=POINT if u > 0.35 else (0, 0))
        st["mother"] = S(*FAM_COUNTER["mother"], R=EAT)
        st["sister"] = S(*FAM_COUNTER["sister"], L=EAT)
        return st
    if sid == "s3b":   # parents cheated in tight so they crop at both frame edges
        return {"dhruv": S(CX - 0.45, 2.85, -90), "father": S(CX - 0.95, 3.25, 90), "mother": S(CX + 0.05, 3.3, 90)}
    if sid == "s3c":   # Dhruv slips out frame-right; a passer-by crosses the near foreground
        st = {k: S(*v) for k, v in FAM_COUNTER.items() if k != "dhruv"}
        a, b, c = Vector((CX - 0.45, 2.85, 0)), Vector((CX + 2.7, 0.3, 0)), Vector((CX + 7.2, -3.8, 0))
        if tau < 0.3:
            st["dhruv"] = S(*FAM_COUNTER["dhruv"])
        elif tau < 3.0:
            v = seg(tau, 0.3, 3.0)
            st["dhruv"] = S(*walk(a, b, v * 2) if v < 0.5 else walk(b, c, v * 2 - 1))
        else:
            st["dhruv"] = S(*HIDE, 0, vis=False)
        st["passer"] = S(*walk(Vector((CX - 2.6, -3.6, 0)), Vector((CX - 2.2, 2.4, 0)), seg(tau, 1.0, 2.8))) if 1.0 <= tau <= 2.8 else S(*HIDE, 0, vis=False)
        return st
    if sid == "s4a":
        return {"dhruv": S(*HIDE, 0, vis=False), "father": S(CX - 1.15, 3.1, -60), "mother": S(CX + 0.85, 3.2, -110), "sister": S(CX + 1.6, 3.2, -90)}
    if sid == "s4b":   # eye-line jhoola -> stall
        return {"mother": S(CX + 4.0, 2.2, lerp(140, 80, seg(tau, 1.2, 2.2)))}
    if sid == "s4c":   # split up: father to the jhoola, mother to the stalls, sister back to the counter
        return {"father": S(*walk(Vector((56.5, 0.3, 0)), Vector((57.5, -4.5, 0)), seg(tau, 0.2, 2.4))),
                "mother": S(*walk(Vector((56.2, 0.9, 0)), Vector((55.0, 3.8, 0)), seg(tau, 0.3, 2.4))),
                "sister": S(*walk(Vector((57.0, -0.2, 0)), Vector((53.5, 0.8, 0)), seg(tau, 0.4, 2.4)))}
    if sid == "s4d":
        return {"father": S(57.6, -7.6, -80), "mother": S(*HIDE, 0, vis=False), "sister": S(*HIDE, 0, vis=False)}
    if sid == "s5a":   # parents walk in from frame-left
        v = seg(tau, 0.0, 3.2)
        fx, fy, _ = walk(Vector((68.6, 1.3, 0)), F5, v)
        mx, my, _ = walk(Vector((68.2, 2.1, 0)), M5, v)
        return {"father": S(fx, fy, lerp(3, TO_SELLER_F, seg(tau, 2.6, 3.4))), "mother": S(mx, my, lerp(4, TO_SELLER_M, seg(tau, 2.6, 3.4)))}
    if sid == "s5b":
        return {"father": S(F5.x, F5.y, TO_SELLER_F, R=SHOW_HEIGHT if tau > 0.6 else (0, 0)), "mother": S(M5.x, M5.y, TO_SELLER_M)}
    if sid == "s5c":
        return {"father": S(F5.x, F5.y, TO_SELLER_F)}
    if sid == "s5d":
        return {"seller": S(SELLER.x, SELLER.y, 200, L=HOLD, R=TWO_FINGERS if tau > 0.5 else (0, 0))}
    if sid == "s5e":   # he points past them to the gate; they turn to look
        turn = seg(tau, 1.6, 2.4)
        return {"seller": S(SELLER.x, SELLER.y, 200, L=HOLD, R=(-95, -25) if tau > 0.8 else (0, 0)),
                "father": S(F5.x, F5.y, lerp(TO_SELLER_F, 175, turn)), "mother": S(M5.x, M5.y, lerp(TO_SELLER_M, 170, turn))}
    if sid in ("s5f", "s5g"):   # father cheated behind her so he sits soft at frame-right
        return {"seller": S(SELLER.x, SELLER.y, 200, L=HOLD), "mother": S(M5.x, M5.y, 8), "father": S(72.3, 3.15, 5)}
    if sid == "s6a":
        return {"father": S(F5.x, F5.y, TO_SELLER_F), "mother": S(M5.x, M5.y, TO_SELLER_M)}
    return {}


# ---------------------------------------------------------------- camera (one entry per shot, like index.html)
def _right(d):
    d = Vector((d.x, d.y, 0)).normalized()
    return Vector((d.y, -d.x, 0))


def C(x, y, z):
    return Vector((x, y, z))


def cam_5c(u):
    head = SELLER + Vector((0, 0, 1.6))
    pos = C(73.95, 1.35, 1.58)
    return pos, head - _right(head - pos) * 0.2, 85


def cam_5d(u):
    tgt = SELLER + Vector((0, 0, 1.42))
    d = (tgt - F5).normalized()
    pos = F5 - Vector((d.x, d.y, 0)) * 0.95 + _right(d) * 0.4 + Vector((0, 0, 1.58))
    return pos, tgt, 50


# (id, start, dur, key side, fn(u) -> (pos, look_at, lens_mm))  u = 0..1 through the shot
SHOTS = [
    ("s0a", 0.0, 3.5, "none", lambda u: (C(75, 0, 900 * (70 / 900) ** u), C(75.5, 0, 0), 24)),
    ("s1a", 3.5, 3.0, "none", lambda u: (vlerp((0, -14, 6.4), (4, -12.6, 6.2), u), C(80, 0, 0), 24)),
    ("s1b", 6.5, 3.4, "L", lambda u: (C(lerp(22.2, 24.2, u), -2.6, 1.55), C(lerp(22.2, 24.2, u), 5, 1.4), 35)),
    ("s2a", 9.9, 2.4, "L", lambda u: (C(25.2, -3.6, 1.55) + _right(C(7, 5, 0)) * lerp(-0.4, 0.4, u), C(32.2, 1.4, 1.2) + _right(C(7, 5, 0)) * (0.9 + lerp(-0.4, 0.4, u)), 35)),
    ("s2b", 12.3, 2.8, "L", lambda u: (C(29 + 2.8 * u + 5.2, 0, 1.4), C(29 + 2.8 * u, 0, 1.15), 50)),
    ("s2c", 15.1, 3.0, "L", lambda u: (vlerp((30.8, 0.45, 1.05), (31.1, 0.46, 1.05), u), C(33.0, 0.5, 1.12), 85)),
    ("s3a", 18.1, 4.4, "L", lambda u: (C(CX - 3.5, 1.9, 1.05), C(CX - 0.2, 3.0, 0.95), 50)),
    ("s3b", 22.5, 2.2, "L", lambda u: (C(CX - 0.4, 0.95, 1.05), C(CX - 0.45, 2.85, 1.08), 85)),
    ("s3c", 24.7, 3.4, "L", lambda u: (C(CX - 4.5, -1.0, 1.05), C(CX + 4.7, 2.2, 0.95), 35)),
    ("s4a", 28.1, 3.6, "L", lambda u: (C(CX - 0.15, lerp(-2.0, -1.7, seg(u * 3.6, 0, 1.4)), 1.5), C(CX - 0.15, 3.0, 1.25), 85)),
    ("s4b", 31.7, 3.6, "L", lambda u: (C(CX + 2.65, 3.9, 1.5), C(CX + 4.0, 2.2, 1.47), 85)),
    ("s4c", 35.3, 2.4, "L", lambda u: (C(72, 4, 2.4), C(52, -5, 1.5), 24)),
    ("s4d", 37.7, 2.4, "L", lambda u: (C(56.3, -5.3, 1.6), C(58.8, -10.2, 1.25), 50)),
    ("s5a", 40.1, 3.6, "L", lambda u: (C(72.5, -3.2, 1.5), C(74.6, 2.6, 1.3), 35)),
    ("s5b", 43.7, 3.6, "L", lambda u: (C(73.9, -1.7, 1.5), C(75.0, 2.3, 1.3), 35)),
    ("s5c", 47.3, 3.8, "L", cam_5c),
    ("s5d", 51.1, 3.4, "L", cam_5d),
    ("s5e", 54.5, 5.0, "L", lambda u: (C(86, -2.8, 1.5), C(70, 0.8, 1.3), 35)),
    ("s5f", 59.5, 3.8, "L", lambda u: (C(75.9, 1.3, 1.5), C(73.2, 2.6, 1.45) + _right(C(-2.7, 1.3, 0)) * 0.25, 85)),
    ("s5g", 63.3, 4.0, "L", lambda u: (vlerp((75.9, 1.3, 1.5), (75.5, 1.5, 1.5), u), C(72.8, 2.85, 1.45), 85)),
    ("s6a", 67.3, 3.4, "none", lambda u: (vlerp((80, 1.2, 3.0), (84, 0.8, 3.2), seg(u, 0, 1)), C(40, 0, 1.0), 24)),
    ("s6b", 70.7, 3.8, "L", lambda u: (NARR + C(0.4, -4.6, 1.55), NARR + C(0.4, 0, 1.3), 35)),
    ("s6c", 74.5, 3.6, "L", lambda u: (NARR + vlerp((0.2, -3.8, 1.55), (0.1, -3.4, 1.55), u), NARR + C(0.1, 0, 1.4), 50)),
    ("s6d", 78.1, 7.0, "L", lambda u: (NARR + vlerp((-0.6, -2.4, 1.58), (-0.65, -2.2, 1.58), u), NARR + C(-0.78, 0, 1.52), 85)),
    ("s6e", 85.1, 4.2, "rake", lambda u: (UNIFORM + C(lerp(-0.35, 0.05, u), -0.85, 1.6), UNIFORM + C(lerp(-0.33, 0.07, u), 0, 1.45), 100)),
    ("s6f", 89.3, 6.0, "L", lambda u: (NARR + C(0.2, -3.8, 1.55), NARR + C(0.2, 0, 1.35), 50)),
    ("s6g", 95.3, 7.0, "flat", lambda u: (LADDER + C(0, -3.4, 1.0), LADDER + C(0, 0, lerp(0.8, 4.4, seg(u, 0, 0.7))), 35)),
]
assert abs(SHOTS[-1][1] + SHOTS[-1][2] - DUR) < 1e-6
for a, b in zip(SHOTS, SHOTS[1:]):
    assert abs(a[1] + a[2] - b[1]) < 1e-6, (a[0], b[0])


def shot_at(t):
    for sh in reversed(SHOTS):
        if t >= sh[1] - 1e-9:
            return sh
    return SHOTS[0]


# ---------------------------------------------------------------- lights and world
key = light("KEY_3000K", "AREA", (0, 0, 0), 0, coll=C_LIGHT, color=(1.0, 0.68, 0.42), size=1.5)
fill = light("FILL_6500K", "AREA", (0, 0, 0), 0, coll=C_LIGHT, color=(0.72, 0.82, 1.0), size=3.0)
for l in (key, fill):
    l.rotation_mode = "QUATERNION"

w = bpy.data.worlds.new("World")
w.use_nodes = True
bg = next(n for n in w.node_tree.nodes if n.type == "BACKGROUND")
scene.world = w


def world_state(t):
    """(sky rgb, strength, practical W, key W, fill W). Dusk -> night at 5A; 5G sinks; narrator set is a dark room."""
    if t < 40.1:
        return (0.12, 0.2, 0.45), 0.55, 140, 180, 45
    if t < 63.3:
        return (0.04, 0.06, 0.16), 0.6, 90, 180, 45
    if t < 67.3:
        u = seg(t, 63.3, 67.3)
        return (0.04, 0.06, 0.16), lerp(0.6, 0.15, u), lerp(90, 25, u), 180, lerp(45, 10, u)
    if t < 70.7:
        return (0.04, 0.06, 0.16), 0.5, 90, 0, 0
    return (0.04, 0.05, 0.08), 0.02, 90, 160, 40


# ---------------------------------------------------------------- crowd
CROWD_T = [figure(f"crowd_tpl_{i}", random.uniform(1.5, 1.82), CROWD[i], CROWD[(i + 3) % 6], coll=C_CROWD, rig=False) for i in range(6)]
crowd = []
for i in range(170):
    ob = bpy.data.objects.new(f"Crowd_{i:02d}", CROWD_T[i % 6].data)
    C_CROWD.objects.link(ob)
    crowd.append((ob, random.uniform(14, 140), random.uniform(-3.4, 3.4), random.uniform(3, 8), random.uniform(0.07, 0.14), random.uniform(0, math.tau)))
for tpl in CROWD_T:
    tpl.hide_render = tpl.hide_viewport = True
    tpl.location = HIDE + (0,)


def seg_dist(p, a, b):
    ab, ap = b - a, p - a
    L = ab.length_squared
    u = 0 if L == 0 else max(0, min(1, ap.dot(ab) / L))
    return (a + ab * u - p).length


# ---------------------------------------------------------------- bake everything per frame
cam_d = bpy.data.cameras.new("Film_Cam")
cam_d.sensor_width, cam_d.sensor_fit = 36, "AUTO"
cam_d.clip_start, cam_d.clip_end = 0.05, 3000
cam_d.dof.use_dof, cam_d.dof.aperture_fstop = True, 2.8
cam = bpy.data.objects.new("Film_Cam", cam_d)
scene.collection.objects.link(cam)
scene.camera = cam
cam.rotation_mode = "QUATERNION"

rec = {"cam_loc": [], "cam_rot": [], "lens": [], "focus": [], "key_loc": [], "key_rot": [], "fill_loc": [], "fill_rot": [],
       "key_e": [], "fill_e": [], "prac": [], "sky": [], "sky_s": []}
cast_rec = {k: {"loc": [], "rot": [], "L": [], "R": [], "vis": []} for k in CAST}
crowd_rec = [{"loc": [], "rot": [], "vis": []} for _ in crowd]
prev_q = prev_kq = prev_fq = None

for f in range(1, NF + 1):
    t = (f - 1) / FPS
    sid, t0, dur, side, fn = shot_at(t)
    u = min(max((t - t0) / dur, 0), 1)
    pos, tgt, lens = fn(u)
    pos, tgt = Vector(pos), Vector(tgt)
    prev_q = look_quat(pos, tgt, prev_q)
    rec["cam_loc"].append(tuple(pos))
    rec["cam_rot"].append(tuple(prev_q))
    rec["lens"].append(lens)
    rec["focus"].append((tgt - pos).length)

    # key/fill: key 45° toward screen-left of the lens, fill on the other side and lower (about 4:1)
    back = Vector(((pos - tgt).x, (pos - tgt).y, 0)).normalized()
    left = -_right(tgt - pos)
    kdir = (back * 0.2 + left).normalized() if side == "rake" else (back + left).normalized()
    kpos = tgt + kdir * 2.8 + Vector((0, 0, 1.1))
    fpos = tgt + (back - left).normalized() * 3.5 + Vector((0, 0, 0.3))
    prev_kq = look_quat(kpos, tgt, prev_kq)
    prev_fq = look_quat(fpos, tgt, prev_fq)
    rec["key_loc"].append(tuple(kpos))
    rec["key_rot"].append(tuple(prev_kq))
    rec["fill_loc"].append(tuple(fpos))
    rec["fill_rot"].append(tuple(prev_fq))
    sky, sky_s, prac, ke, fe = world_state(t)
    if side in ("none", "flat"):
        ke, fe = (0, 0) if side == "none" else (60, 60)
    rec["key_e"].append(round(ke, 2))
    rec["fill_e"].append(round(fe, 2))
    rec["prac"].append(round(prac, 2))
    rec["sky"].append((*sky, 1))
    rec["sky_s"].append(round(sky_s, 3))

    state = {}
    for sh in SHOTS:
        if sh[1] > t + 1e-9:
            break
        state.update(stage(sh[0], min(t - sh[1], sh[2]), sh[2]))
    for k, st in state.items():
        r = cast_rec[k]
        x, y = st["pos"]
        r["loc"].append((x, y, 0))
        r["rot"].append((0, 0, math.radians(st["yaw"])))
        r["L"].append((0, math.radians(st["L"][0]), math.radians(st["L"][1])))
        r["R"].append((0, math.radians(st["R"][0]), -math.radians(st["R"][1])))
        r["vis"].append(not st["vis"])

    # crowd loiters along the lane; hidden when blocking the lens, overlapping the cast, or in the thinned witness lane
    cast_pts = [Vector((*s["pos"], 0)) for k, s in state.items() if s["vis"]]
    cam2, tgt2 = Vector((pos.x, pos.y, 0)), Vector((tgt.x, tgt.y, 0))
    guard = sid not in ("s0a", "s1a", "s1b", "s6a")
    for (ob, x0, y0, amp, w_, ph), r in zip(crowd, crowd_rec):
        x = x0 + amp * math.sin(w_ * t + ph)
        vx = amp * w_ * math.cos(w_ * t + ph)
        p = Vector((x, y0, 0))
        hide = any((p - c).length < 0.7 for c in cast_pts)
        hide |= guard and seg_dist(p, cam2, tgt2 + (tgt2 - cam2).normalized() * 0.5) < 0.8
        hide |= (cam2 - p).length < 1.2
        hide |= t >= 40.1 and abs(x - SELLER.x) < 9 and t < 70.7
        r["loc"].append((x, y0, 0))
        r["rot"].append((0, 0, 0 if vx >= 0 else math.pi))
        r["vis"].append(hide)

fk_vec(cam, "location", rec["cam_loc"])
fk_vec(cam, "rotation_quaternion", rec["cam_rot"])
fk(cam_d, "lens", 0, rec["lens"])
fk(cam_d, "dof.focus_distance", 0, [round(v, 3) for v in rec["focus"]])
for ob, loc, rot in ((key, "key_loc", "key_rot"), (fill, "fill_loc", "fill_rot")):
    fk_vec(ob, "location", rec[loc])
    fk_vec(ob, "rotation_quaternion", rec[rot])
fk(key.data, "energy", 0, rec["key_e"])
fk(fill.data, "energy", 0, rec["fill_e"])
fk(PRACTICAL, "energy", 0, rec["prac"])
fk_vec(w.node_tree, f'nodes["{bg.name}"].inputs[0].default_value', rec["sky"])
fk(w.node_tree, f'nodes["{bg.name}"].inputs[1].default_value', 0, rec["sky_s"])
for k, (root, arms) in CAST.items():
    r = cast_rec[k]
    fk_vec(root, "location", r["loc"])
    fk_vec(root, "rotation_euler", r["rot"])
    fk_vec(arms["L"], "rotation_euler", r["L"])
    fk_vec(arms["R"], "rotation_euler", r["R"])
    for ob in [root, *root.children]:
        fk(ob, "hide_render", 0, r["vis"])
        fk(ob, "hide_viewport", 0, r["vis"])
for (ob, *_), r in zip(crowd, crowd_rec):
    fk_vec(ob, "location", [tuple(round(c, 3) for c in v) for v in r["loc"]], "CONSTANT")
    fk_vec(ob, "rotation_euler", r["rot"])
    fk(ob, "hide_render", 0, r["vis"])
    fk(ob, "hide_viewport", 0, r["vis"])

# the ferris wheel turns slowly the whole film
hub.keyframe_insert("rotation_euler", index=1, frame=1)
hub.rotation_euler.y = math.radians(40)
hub.keyframe_insert("rotation_euler", index=1, frame=NF)
set_interpolation([hub], "LINEAR")

markers([(sh[0][1:].upper(), sh[1]) for sh in SHOTS])
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("SAVED", OUT, "frames", NF)
