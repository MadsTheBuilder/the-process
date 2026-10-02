# mela.py - the Mirzapur mela at night, built once at real scale (metres).
# Layout (x east, y north):
#   main lane  y -5.5..5.5, x -62..62        stall rows A y=+-7 (face the lane), B y=+-11 (face outward), C y=+-21 (face lane 2)
#   lane 2     y +-(12.5..19.5)               cross lanes at x=-26 (through the wheel), 14, 36
#   ferris wheel (-26, 32), jhoola (34, 32), balloon vendor pole (16, 2.9), white van (21.5, -3.6), gate x=62
import math
import random

import bpy
from mathutils import Vector

from kit import ANIM, Builder, F, M, V, box_mesh, empty, link, new_obj, sphere_mesh, cyl_mesh, to_mesh, ease, bsdf

WHEEL = Vector((-26, 32, 14.5))
JHOOLA = Vector((34, 32, 0))
POLE = Vector((16.0, 2.9, 0))
VAN = Vector((21.5, -3.6, 0))
GATE_X = 62.0
CROSS = (-26.0, 14.0, 36.0)
STALL_COLORS = ["teal", "mustard", "blue", "green", "cream", "plum"]
TARP = {"teal": (0.07, 0.28, 0.28), "mustard": (0.5, 0.36, 0.08), "blue": (0.09, 0.15, 0.34),
        "green": (0.14, 0.28, 0.16), "cream": (0.5, 0.45, 0.32), "plum": (0.24, 0.1, 0.24)}


def sky(zenith=(0.012, 0.02, 0.06), horizon=(0.10, 0.16, 0.28), strength=2.2):
    w = bpy.data.worlds.new("World")
    w.use_nodes = True
    nt = w.node_tree
    for n in list(nt.nodes):
        if n.type not in ("OUTPUT_WORLD",):
            nt.nodes.remove(n)
    out = next(n for n in nt.nodes if n.type == "OUTPUT_WORLD")
    bg = nt.nodes.new("ShaderNodeBackground")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    mr = nt.nodes.new("ShaderNodeMapRange")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    nt.links.new(tc.outputs["Generated"], sep.inputs["Vector"])
    nt.links.new(sep.outputs["Z"], mr.inputs["Value"])
    mr.inputs["From Min"].default_value = 0.0
    mr.inputs["From Max"].default_value = 0.8
    nt.links.new(mr.outputs["Result"], ramp.inputs["Fac"])
    ramp.color_ramp.elements[0].color = (*horizon, 1)
    ramp.color_ramp.elements[1].color = (*zenith, 1)
    nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = strength
    nt.links.new(bg.outputs["Background"], out.inputs["Surface"])
    bpy.context.scene.world = w
    return w, bg


def build_mela(T, seed=3):
    rnd = random.Random(seed)
    env = {}
    ms = {
        "ground": M((0.085, 0.07, 0.055), 1.0), "lane": M((0.12, 0.10, 0.075), 1.0),
        "wood": M((0.07, 0.05, 0.04), 0.9), "dark": M((0.04, 0.04, 0.05), 0.8),
        "steel": M((0.22, 0.24, 0.28), 0.5, 0.6), "goods": M((0.45, 0.38, 0.28), 0.9),
        "goods2": M((0.2, 0.3, 0.4), 0.9), "goods3": M((0.5, 0.45, 0.2), 0.9),
        "white": M((0.7, 0.7, 0.68), 0.5), "van": M((0.78, 0.78, 0.76), 0.35),
        "glass": M((0.03, 0.05, 0.07), 0.1), "pole": M((0.15, 0.15, 0.17), 0.6, 0.5),
        "lamp": M((1, 0.55, 0.2), 0.5, emit=(1.0, 0.5, 0.15), strength=14),
        "fw": M((1, 0.7, 0.3), 0.5, emit=(1.0, 0.62, 0.22), strength=18),
        "fc": M((0.5, 0.9, 1), 0.5, emit=(0.4, 0.85, 1.0), strength=14),
        "fg": M((0.7, 1, 0.6), 0.5, emit=(0.6, 1.0, 0.5), strength=12),
        "ww": M((1, 0.95, 0.8), 0.5, emit=(1.0, 0.92, 0.7), strength=16),
        "string": M((0.7, 0.7, 0.7), 0.9),
        "wl0": M((1, 0.7, 0.3), 0.5, emit=(1.0, 0.62, 0.22), strength=18),
        "wl1": M((0.5, 0.9, 1), 0.5, emit=(0.4, 0.85, 1.0), strength=14),
        "wl2": M((0.7, 1, 0.6), 0.5, emit=(0.6, 1.0, 0.5), strength=12),
        "cart": M((0.55, 0.45, 0.2), 0.8), "cartglow": M((1, 0.5, 0.15), 0.5, emit=(1.0, 0.45, 0.1), strength=7),
        "seat": M((0.35, 0.3, 0.12), 0.7), "cabin": M((0.35, 0.4, 0.5), 0.6),
        "cabinglow": M((1, 0.85, 0.5), 0.5, emit=(1.0, 0.8, 0.4), strength=6),
        "banner": M((0.5, 0.3, 0.08), 0.8), "smoke": M((0.55, 0.55, 0.55), 1.0, alpha=0.1),
    }
    for k, c in TARP.items():
        ms["t_" + k] = M(c, 0.95)
    B = Builder()
    # ---------------- ground
    g = new_obj("Ground", box_mesh("g", 6000, 6000, 0.2, False), ms["ground"], loc=(0, 0, -0.1))
    B.box("lane", (0, 0, 0.01), (124, 11, 0.02))
    B.box("lane", (-26, 16, 0.01), (7, 60, 0.02))
    B.box("lane", (14, 16, 0.01), (5, 60, 0.02))
    B.box("lane", (36, 16, 0.01), (5, 60, 0.02))
    B.box("lane", (0, 16, 0.01), (124, 7, 0.02))
    B.box("lane", (0, -16, 0.01), (124, 7, 0.02))
    B.box("lane", (-26, -16, 0.01), (7, 12, 0.02))
    # ---------------- stalls
    def stall(x, yc, face, col):
        """face = -1/+1: direction (in y) the open front looks. Stall footprint 5 x 3 centred on (x, yc)."""
        fy = yc + face * 1.5
        by = yc - face * 1.5
        k = "t_" + col
        B.box("wood", (x, by, 1.3), (5.0, 0.12, 2.6))                       # back wall
        B.box("wood", (x - 2.45, yc, 1.2), (0.12, 3.0, 2.4))                # side walls
        B.box("wood", (x + 2.45, yc, 1.2), (0.12, 3.0, 2.4))
        B.box(k, (x, yc, 2.62), (5.3, 3.4, 0.1), rx=face * 0.0)             # canopy
        B.box(k, (x, fy + face * 0.15, 2.4), (5.3, 0.06, 0.35))             # valance
        B.box("wood", (x, fy - face * 0.4, 0.5), (4.8, 0.7, 1.0))           # counter
        for i in range(rnd.randint(3, 6)):                                   # goods
            gk = rnd.choice(["goods", "goods2", "goods3"])
            B.box(gk, (x - 2 + i * 0.8 + rnd.uniform(-.2, .2), fy - face * 0.4, 1.12), (0.5, 0.4, rnd.uniform(0.2, 0.5)))
        for i in range(12):                                                  # shelf goods
            B.box(rnd.choice(["goods", "goods2", "goods3"]), (x - 2.1 + i * 0.38, by + face * 0.3, 1.2 + rnd.choice([0, 0.5, 1.0])),
                  (0.3, 0.3, 0.3))
        # fairy lights along the valance
        for i in range(12):
            B.box(rnd.choice(["fw", "fw", "ww", "fc", "fg"]), (x - 2.5 + i * 0.46, fy + face * 0.2, 2.2 + 0.05 * math.sin(i * 1.3)), (0.09, 0.09, 0.09))

    for row_y, face in ((7.0, -1), (11.0, 1), (21.0, -1)):
        for sgn in (1, -1):
            yc = sgn * row_y
            fc = -sgn * 1 if row_y != 11.0 else sgn
            if row_y == 11.0:
                fc = sgn          # faces outward
            elif row_y == 7.0:
                fc = -sgn         # faces the main lane
            else:
                fc = -sgn         # faces lane 2
            for i in range(20):
                x = -57 + 6 * i
                if any(abs(x - c) < 4.2 for c in CROSS):
                    continue
                stall(x, yc, fc, STALL_COLORS[(i + int(row_y)) % 6])
    # ---------------- lamps (emissive heads) and string lights across the lane
    for x in range(-56, 60, 10):
        for sg in (1, -1):
            B.cyl("pole", (x, sg * 5.0, 0), (x, sg * 5.0, 6.0), 0.05, 6)
            B.box("lamp", (x, sg * 5.0, 6.1), (0.5, 0.5, 0.2))
    for x in range(-58, 62, 8):
        for i in range(24):
            u = i / 23
            B.box(rnd.choice(["fw", "ww", "fc", "fg", "fw"]), (x, -5.3 + 10.6 * u, 4.6 - 0.9 * math.sin(math.pi * u)), (0.09, 0.09, 0.09))
        B.cyl("string", (x, -5.3, 4.6), (x, 5.3, 4.6), 0.01, 4)
    # ---------------- gate
    for sg in (1, -1):
        B.box("steel", (GATE_X, sg * 5.5, 3.0), (1.0, 1.0, 6.0))
        B.box("banner", (GATE_X, sg * 5.5, 3.0), (1.1, 1.1, 0.5))
    B.box("steel", (GATE_X, 0, 6.2), (1.0, 12.0, 0.8))
    B.box("banner", (GATE_X - 0.55, 0, 6.2), (0.1, 9.0, 0.55))
    for i in range(40):
        B.box(rnd.choice(["fw", "ww", "fc"]), (GATE_X - 0.6, -5.8 + i * 0.3, 5.7), (0.1, 0.1, 0.1))
    B.box("dark", (GATE_X + 1.5, 0, 0.8), (0.4, 40, 1.6))                     # outer fence
    # ---------------- jhoola tower (static part)
    jx, jy = JHOOLA.x, JHOOLA.y
    B.cyl("steel", (jx, jy, 0), (jx, jy, 9), 0.55, 10)
    B.cyl("steel", (jx - 4, jy - 4, 0), (jx, jy, 8), 0.12, 6)
    B.cyl("steel", (jx + 4, jy - 4, 0), (jx, jy, 8), 0.12, 6)
    B.cyl("steel", (jx, jy + 5, 0), (jx, jy, 8), 0.12, 6)
    # ---------------- ferris wheel static legs
    wx, wy, wz = WHEEL
    for sy in (-1.7, 1.7):
        for sx in (-7.5, 7.5):
            B.cyl("steel", (wx + sx, wy + sy * 1.7, 0), (wx, wy + sy * 0.55, wz), 0.28, 8)
    B.box("steel", (wx, wy, 0.15), (18, 7, 0.3))
    # ---------------- toy stall extra: hanging toys (pastel, no red)
    for i in range(14):
        B.sph("goods2" if i % 2 else "goods3", (-3.0 - 2 + i * 0.35, 8.1, 2.0 - 0.2 * (i % 3)), 0.12)
    # ---------------- food carts
    for cx in (25.0, 28.5, 32.0):
        B.box("cart", (cx, -5.0, 0.55), (1.8, 0.95, 0.9))
        B.box("cartglow", (cx, -5.0, 1.05), (1.5, 0.7, 0.08))
        B.cyl("pole", (cx, -5.0, 0.9), (cx, -5.0, 2.4), 0.03, 5)
        B.cyl("t_mustard", (cx, -5.0, 2.4), (cx, -5.0, 2.55), 1.4, 10, r2=0.1)
    # ---------------- white van (parked at lane edge, length along x)
    vx, vy = VAN.x, VAN.y
    B.box("van", (vx, vy, 1.1), (5.2, 1.95, 1.6))
    B.box("van", (vx + 2.2, vy, 0.75), (1.4, 1.95, 0.9))
    B.box("glass", (vx + 2.45, vy, 1.45), (0.8, 1.8, 0.7))
    B.box("dark", (vx, vy, 0.28), (5.2, 1.9, 0.28))
    for wxo in (-1.6, 1.8):
        for sg in (1, -1):
            B.cyl("dark", (vx + wxo, vy + sg * 0.95, 0.38), (vx + wxo, vy + sg * 0.78, 0.38), 0.38, 10)
    # ---------------- balloon vendor pole + bunch
    px, py = POLE.x, POLE.y
    B.cyl("pole", (px, py, 0), (px, py, 3.35), 0.03, 6)
    B.cyl("pole", (px - 0.5, py, 1.3), (px + 0.5, py, 1.3), 0.02, 4)
    B.box("wood", (px, py, 0.05), (0.6, 0.6, 0.1))
    objs = B.build(ms, "Mela")
    # ---------------- balloons (separate objects so the hero can be keyed)
    cols = [(0.62, 0.62, 0.58), (0.62, 0.56, 0.3), (0.3, 0.4, 0.55), (0.28, 0.46, 0.32), (0.45, 0.38, 0.55), (0.6, 0.45, 0.45)]
    bmesh_ = sphere_mesh("balloon", 0.15, 10, 8, (1, 1, 1.18))
    placed = []
    bs = Builder()
    for i in range(46):
        for _try in range(30):
            a, h = rnd.uniform(0, 6.28), rnd.uniform(1.55, 3.25)
            rad = 0.18 + 0.5 * (1 - abs(h - 2.3) / 1.1) * rnd.random()
            p = Vector((px + rad * math.cos(a), py + rad * math.sin(a), h))
            if all((p - q).length > 0.27 for q in placed):
                placed.append(p)
                break
        else:
            continue
        o = new_obj("bal%d" % i, bmesh_, M(cols[i % 6], 0.35))
        o.location = p
        bs.cyl("string", p - Vector((0, 0, 0.18)), (px, py, 1.4 + rnd.uniform(0, 0.4)), 0.004, 3)
    # hero red balloon (front/west side of the bunch, where Dhruv sees it)
    hero_pos = Vector((px - 0.42, py - 0.3, 2.9))
    red = M((0.8, 0.012, 0.01), 0.3, emit=(0.8, 0.012, 0.01), strength=0.6)
    hero = new_obj("HeroBalloon", bmesh_, red)
    hero.location = hero_pos
    bs.cyl("string", hero_pos - Vector((0, 0, 0.18)), (px, py, 1.6), 0.004, 3)
    env["hero_pos"] = hero_pos
    env["hero"] = hero
    env["red_mat"] = red
    # a couple more reds low in the bunch (planted, not dominant)
    extra_red = []
    for p in (Vector((px + 0.35, py + 0.25, 1.75)), Vector((px - 0.1, py + 0.5, 2.1))):
        o = new_obj("redExtra", bmesh_, red)
        o.location = p
        extra_red.append(o)
    ms2 = {"string": ms["string"]}
    bs.build(ms2, "BalStrings")
    # foreground bunch B (second hawker, for the track-in shot)
    bB = Vector((8.3, -0.6, 0))
    bs2 = Builder()
    bs2.cyl("pole", bB, bB + Vector((0, 0, 2.9)), 0.03, 6)
    for i in range(22):
        a, h = rnd.uniform(0, 6.28), rnd.uniform(1.5, 2.9)
        p = Vector((bB.x + (0.15 + 0.35 * rnd.random()) * math.cos(a), bB.y + (0.15 + 0.35 * rnd.random()) * math.sin(a), h))
        o = new_obj("balB%d" % i, bmesh_, M(cols[i % 6], 0.35))
        o.location = p
        bs2.cyl("string", p - Vector((0, 0, 0.18)), (bB.x, bB.y, 1.3), 0.004, 3)
    bs2.build({"string": ms["string"], "pole": ms["pole"]}, "BalB")
    # ---------------- ferris wheel (rotating structure + counter-rotated gondolas)
    R = 12.0
    wb = Builder()
    N = 16
    for ring in (-0.9, 0.9):
        for i in range(48):
            a0, a1 = 2 * math.pi * i / 48, 2 * math.pi * (i + 1) / 48
            wb.cyl("steel", (R * math.cos(a0), ring, R * math.sin(a0)), (R * math.cos(a1), ring, R * math.sin(a1)), 0.1, 5)
        for i in range(N):
            a = 2 * math.pi * i / N
            wb.cyl("steel", (0, ring * 0.6, 0), (R * math.cos(a), ring, R * math.sin(a)), 0.045, 4)
    for i in range(N):
        a = 2 * math.pi * i / N
        wb.cyl("steel", (R * math.cos(a), -0.9, R * math.sin(a)), (R * math.cos(a), 0.9, R * math.sin(a)), 0.07, 4)
    wb.cyl("steel", (0, -1.2, 0), (0, 1.2, 0), 0.5, 10)
    keys = ["wl0", "wl1", "wl2"]
    for i in range(96):
        a = 2 * math.pi * i / 96
        for ring in (-0.9, 0.9):
            wb.box(keys[i % 3], (R * math.cos(a), ring, R * math.sin(a)), (0.16, 0.16, 0.16))
    wobj = wb.build(ms, "WheelRot")
    wh = empty("Wheel_hub", WHEEL)
    for o in wobj.values():
        o.parent = wh
    om = 0.12
    wh.rotation_mode = "XYZ"
    ANIM.put(wh, "rotation_euler", 1, 1, 0.0, "lin")
    ANIM.put(wh, "rotation_euler", 1, F(T), -om * T, "lin")
    # gondolas
    gm = {"cab": ms["cabin"], "glow": ms["cabinglow"]}
    for i in range(N):
        gb = Builder()
        gb.box("cab", (0, 0, 0), (1.5, 1.2, 1.3))
        gb.box("glow", (0.0, 0.0, 0.1), (1.54, 1.0, 0.5))
        gb.cyl("cab", (0, 0, 0.65), (0, 0, 1.0), 0.04, 4)
        go = list(gb.build(gm, "Gond").values())
        g0 = empty("gond%d" % i)
        for o in go:
            o.parent = g0
        a0 = 2 * math.pi * i / N
        for f in range(1, int(F(T)) + 6, 6):
            t = (f - 1) / 24
            a = a0 - om * t
            pv = WHEEL + Vector((R * math.cos(a), 0, R * math.sin(a)))
            ANIM.put(g0, "location", 0, f, pv.x)
            ANIM.put(g0, "location", 1, f, pv.y)
            ANIM.put(g0, "location", 2, f, pv.z - 1.0)
    # LED blinking (3 groups on their own materials, constant keys)
    for gi, (m, base) in enumerate(((ms["wl0"], 18), (ms["wl1"], 14), (ms["wl2"], 12))):
        node = m.node_tree.nodes["Principled BSDF"]
        idx = list(node.inputs).index(node.inputs["Emission Strength"])
        path = 'nodes["Principled BSDF"].inputs[%d].default_value' % idx
        k = 0
        t = 0.0
        while t < T:
            ANIM.put(m.node_tree, path, 0, F(t), base if (k + gi) % 3 else 0.3, "const")
            t += 0.4
            k += 1
    # ---------------- jhoola (rotating top with swinging seats)
    jb = Builder()
    for i in range(8):
        a = 2 * math.pi * i / 8
        jb.cyl("steel", (0, 0, 0), (4.6 * math.cos(a), 4.6 * math.sin(a), -0.3), 0.07, 5)
        sx, sy = 4.6 * math.cos(a) + 0.9 * math.cos(a), 4.6 * math.sin(a) + 0.9 * math.sin(a)
        jb.cyl("string", (4.6 * math.cos(a), 4.6 * math.sin(a), -0.3), (sx, sy, -3.0), 0.025, 4)
        jb.box("seat", (sx, sy, -3.2), (0.7, 0.7, 0.2), rz=a)
        jb.box("fw", (4.6 * math.cos(a), 4.6 * math.sin(a), -0.2), (0.14, 0.14, 0.14))
    jb.cyl("steel", (0, 0, -0.5), (0, 0, 0.3), 0.7, 10)
    jobj = jb.build(ms, "JhoolaTop")
    jh = empty("Jhoola_top", (jx, jy, 9.0))
    for o in jobj.values():
        o.parent = jh
    ANIM.put(jh, "rotation_euler", 2, 1, 0.0, "lin")
    ANIM.put(jh, "rotation_euler", 2, F(T), 1.0 * T, "lin")
    # ---------------- food-cart smoke
    sb = Builder()
    for cx in (25.0, 28.5, 32.0):
        for i in range(6):
            sb.sph("smoke", (cx + rnd.uniform(-.3, .3), -5.0 + rnd.uniform(-.3, .3), 1.4 + i * 0.45), 0.35 + 0.1 * i, 8, 6)
    sb.build({"smoke": ms["smoke"]}, "Smoke")
    env["ms"] = ms
    env["balloon_mesh"] = bmesh_
    return env


def add_lights(T):
    """Blue-hour fill + sodium point lights along the lane. Shadows off except for the few that matter."""
    sun = bpy.data.lights.new("Moon", "SUN")
    sun.energy = 0.35
    sun.color = (0.45, 0.6, 1.0)
    so = bpy.data.objects.new("Moon", sun)
    link(so)
    so.rotation_euler = (math.radians(55), math.radians(10), math.radians(-30))
    out = []
    for x in range(-56, 60, 8):
        d = bpy.data.lights.new("Sod%d" % x, "POINT")
        d.energy = 1000
        d.color = (1.0, 0.58, 0.25)
        d.shadow_soft_size = 0.3
        d.use_shadow = False
        ob = bpy.data.objects.new("Sod%d" % x, d)
        link(ob)
        ob.location = (x, 0.0, 5.8)
        out.append(ob)
    for x in range(-52, 60, 14):
        for yy in (16, -16):
            d = bpy.data.lights.new("Sod2_%d_%d" % (x, yy), "POINT")
            d.energy = 700
            d.color = (1.0, 0.62, 0.3)
            d.use_shadow = False
            ob = bpy.data.objects.new("Sod2", d)
            link(ob)
            ob.location = (x, yy, 5.0)
            out.append(ob)
    # wheel plaza + jhoola plaza glow
    for pos, col, e in (((-26, 24, 6), (0.5, 0.8, 1.0), 2500), ((34, 24, 6), (1.0, 0.7, 0.4), 1800)):
        d = bpy.data.lights.new("Plaza", "POINT")
        d.energy, d.color, d.use_shadow = e, col, False
        ob = bpy.data.objects.new("Plaza", d)
        link(ob)
        ob.location = pos
    return out
