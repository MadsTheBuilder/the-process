# Scene 27 - THE RIVER - EXT. River Dream Space - Night -> Sunrise (shots 187-207, 100 s)
# Infinite still water, heavy fog, a moon backlight. Mamta alone in a small boat drifting east along a shore
# 12 m to the north. Figures appear on the shore and let her go: Dev, the child (heard), Jagdish (unties the
# rope), her parents (ask forgiveness). She leaves them to God and floats on into the first warm light.
import math

import bpy
from mathutils import Quaternion, Vector

from kit import *
from film import *
import cast
import props
import sets
from sets import RIV

BY = RIV.y + 10.0                     # the boat's line (y)
SHORE_Y = RIV.y + 23.0                # where people stand on the bank
SHORE_Z = 0.2
POST = Vector((2.0, RIV.y + 22.4, 0.9))


def build(S):
    T = S.T
    a = {n: T[n][0] for n in T}
    b = {n: T[n][1] for n in T}
    E = S.END
    st = sets.build_river(E)
    L = st["L"]
    P = st["P"]
    C = sets.mats()
    sun_dir = sets.sun_dir
    sun_dir(L["R_Moon"], 92, 16)
    sun_dir(L["R_Sky"], 270, 60)
    sun_dir(L["R_Rise"], 2, 3)
    S.state(0, R_Moon=(1.4, 7500), R_Sky=(0.12, 8000), R_Rise=0, R_Lantern=0)
    S.world(0, (0.05, 0.08, 0.16), 0.5)
    S.exposure(0, 0.6)
    fog = P["fog_node"]
    ftree = P["fog"].data.materials[0].node_tree
    dpath = 'nodes["%s"].inputs["Density"].default_value' % fog.name
    cpath = 'nodes["%s"].inputs["Color"].default_value' % fog.name
    for t, d in ((0, 0.035), (a[199] - 0.5, 0.035), (a[199] + 3.0, 0.016), (a[204], 0.02), (a[207], 0.02), (E, 0.012)):
        ANIM.put(ftree, dpath, 0, F(t), d)
    # sunrise: the first warm light of the film
    SR = a[207]
    S.state(SR, R_Moon=(0.3, 7500), R_Rise=(3.5, 3000), R_Sky=(0.3, 5000))
    for t, col in ((SR, (0.75, 0.82, 0.95)), (SR + 4, (1.0, 0.72, 0.45)), (E, (1.0, 0.7, 0.42))):
        for i, c in enumerate(col):
            ANIM.put(ftree, cpath, i, F(t), c)
    for t, (col, s) in ((SR, ((0.05, 0.08, 0.16), 0.5)), (SR + 4, ((0.55, 0.32, 0.2), 0.9)), (E, ((0.7, 0.42, 0.25), 1.1))):
        for i, c in enumerate(col):
            ANIM.put(bpy.context.scene.world.node_tree, 'nodes["Background"].inputs[0].default_value', i, F(t), c)
        ANIM.put(bpy.context.scene.world.node_tree, 'nodes["Background"].inputs[1].default_value', 0, F(t), s)
    sunball = new_obj("SunDisc", sphere_mesh("sd", 14, 24, 16), M((1, 0.6, 0.3), 1.0, emit=(1.0, 0.55, 0.25), strength=0.0), loc=(520, RIV.y - 30, 6))
    sm = sunball.data.materials[0]
    ANIM.put(sm.node_tree, 'nodes["Principled BSDF"].inputs["Emission Strength"].default_value', 0, 1, 0.0, "const")
    ANIM.put(sm.node_tree, 'nodes["Principled BSDF"].inputs["Emission Strength"].default_value', 0, F(SR), 0.0)
    ANIM.put(sm.node_tree, 'nodes["Principled BSDF"].inputs["Emission Strength"].default_value', 0, F(E), 25.0)
    keys_vec(sunball, "location", [(0, Vector((520, RIV.y - 30, -10))), (SR, Vector((520, RIV.y - 30, -10))), (E, Vector((520, RIV.y - 30, 10)))])

    # ------------------------------------------------------------- the boat's drift
    stops = [(0, -9.5), (a[196], 2.6), (a[196] + 1.2, 3.0), (a[201], 3.0), (a[204], 5.6), (a[207], 7.4), (E, 15.0)]

    def bx(t):
        for (t0, x0), (t1, x1) in zip(stops, stops[1:]):
            if t0 <= t <= t1:
                u = (t - t0) / (t1 - t0)
                return lerp(x0, x1, u if not (t0 == a[196]) else seg(t, t0, t1))
        return stops[-1][1]

    def by(t):
        return BY - (seg(t, a[207], E) * 6.0)

    boat = P["boat"]
    boat.rotation_mode = "XYZ"
    for f in range(1, int(F(E)) + 1, 2):
        t = (f - 1) / FPS
        for i, v in enumerate((bx(t), by(t), 0.06 * math.sin(t * 0.9))):
            ANIM.put(boat, "location", i, f, v)
        ANIM.put(boat, "rotation_euler", 0, f, 0.025 * math.sin(t * 0.7))
        ANIM.put(boat, "rotation_euler", 2, f, -0.25 * seg(t, a[207], E))
    # ------------------------------------------------------------- Mamta in the boat (seated on the middle thwart)
    MA = cast.mamta("boat")
    N, E_, S_ = math.pi / 2, 0.0, -math.pi / 2
    beats = [(0, 0.35), (a[188], 0.6), (a[188] + 2.0, 1.2), (a[190], N), (a[192] + 2.0, N + 0.9), (a[194], 0.3), (a[194] + 2.0, 1.4),
             (a[195] + 1.5, S_ + 0.4), (a[196], S_ + 0.3), (a[197], math.pi - 0.2), (a[199], N - 0.2), (a[203], 0.2),
             (a[204], N - 0.3), (a[207], 0.0)]

    def yaw_at(t):
        y = beats[0][1]
        for t0, v in beats:
            if t >= t0:
                y = v
        return y
    MA.at(0, bx(0) + 0.3, by(0), yaw_at(0))
    t = 0.5
    while t <= E + 0.01:
        MA.walk(t, bx(t) + 0.3, by(t), yaw=yaw_at(t), gait="stand", tt=1.4)
        t += 0.5
    MA.act(0, E, fade=0, sit=1.0, seat=0.40, footz=0.05, ffwd=0.42, _hold0=True)
    MA.act(0, E, z=lambda t, u: 0.06 * math.sin(t * 0.9))
    MA.act(a[188], b[188], look=lambda t, u: est(MA, t) + Vector((math.cos(t * 0.8) * 6, 6, 0)), mood=(-0.3, -0.1, 0.0))
    MA.act(a[189], b[192], look=lambda t, u: est(DV, t), mood=lambda t, u: (0.2 if t > a[191] else -0.3, 0.3 if t > a[191] else 0.0,
                                                                            talk(a[192] + 0.5, b[192] - 0.6)(t, u)[2]),
           eyes=lambda t, u: 0.5 if a[190] < t < a[190] + 1.2 else 1.0)
    MA.act(a[194], b[194], look=lambda t, u: est(MA, t) + Vector((6 * math.sin(t * 1.4), 6 * math.cos(t * 0.9), 0)), mood=(-0.8, -0.5, 0.1))
    MA.act(a[195], b[195], mood=lambda t, u: (-0.2, lerp(-0.3, 0.45, u), 0.0))
    MA.act(a[196] + 0.3, b[196], lean=0.65, crouch=0.0, armL=lambda t, u: est(MA, t) + Vector((-0.2 + 0.25 * math.sin(t * 3), -0.75, -1.5)),
           armR=lambda t, u: est(MA, t) + Vector((0.3 + 0.25 * math.sin(t * 3 + 1), -0.75, -1.5)), mood=(-0.5, -0.3, 0.05))
    ROPE_END = lambda t: Vector((bx(t) - 2.1, by(t), 0.55))
    MA.act(a[197], b[198], armL=lambda t, u: ROPE_END(t) + Vector((0.5 + 0.12 * math.sin(t * 4), 0.05, 0.2)),
           armR=lambda t, u: ROPE_END(t) + Vector((0.75 + 0.12 * math.sin(t * 4), -0.05, 0.25)), lean=0.25, mood=(-0.6, -0.4, 0.1))
    MA.act(a[199], b[202], look=lambda t, u: est(JG, t), mood=lambda t, u: (0.0, 0.35 if t > a[201] else 0.0, 0.0))
    MA.act(a[203], b[203], look=lambda t, u: est(MA, t) + Vector((6, 2, 4)), hp=-0.25)
    MA.act(a[204], b[206], look=lambda t, u: mid(est(MO, t), est(PA, t)), mood=lambda t, u: (0.0, 0.0, talk(a[206] + 0.8, b[206] - 1.0, amt=0.12)(t, u)[2]))
    MA.act(a[207], E, look=lambda t, u: est(MA, t) + Vector((10, -2, 0.5)))
    # ------------------------------------------------------------- the shore: Dev, Jagdish, the parents
    DV = cast.dev("river")
    JG = cast.jagdish("sherwani")
    MO = cast.mother()
    PA = cast.papa()
    DVX = -1.2
    DV.at(0, DVX, SHORE_Y, S_).stay(a[193]).walk(b[193], DVX - 0.5, SHORE_Y + 9.0, yaw=S_, gait="stand")
    DV.act(0, E, z=SHORE_Z, mood=(0.3, 0.7, 0.0), look=lambda t, u: est(MA, t), armR=lambda t, u: est(MA, t) if t > a[191] else None)
    JG.at(a[199], POST.x + 0.9, SHORE_Y + 0.8, S_).stay(a[200]).walk(a[200] + 1.6, POST.x + 0.35, POST.y + 0.35, mode="smooth").stay(b[201])
    JG.walk(a[202] + 0.4, POST.x + 0.6, SHORE_Y + 1.0, mode="smooth").walk(b[202], POST.x + 0.8, SHORE_Y + 10.0, gait="stand")
    JG.act(a[199], E, z=SHORE_Z, look=lambda t, u: est(MA, t), mood=(0.0, 0.35, 0.0))
    JG.act(a[200] + 1.4, a[201] + 0.6, crouch=0.2, lean=0.5, armL=POST + Vector((0.1, 0.05, -0.15)), armR=POST + Vector((0.1, -0.05, -0.2)), look=POST)
    MO.at(a[203], 7.4, SHORE_Y + 0.2, S_).stay(E)
    PA.at(a[203], 8.4, SHORE_Y + 0.2, S_).stay(E)
    namaste = lambda X: (lambda t, u: (lambda j: j["sh_c"] + j["tf"] * 0.22 - j["spine"] * 0.18)(X.J(t)))
    for X in (MO, PA):
        X.act(a[203], E, z=SHORE_Z + 0.2, armL=namaste(X), armR=namaste(X), look=lambda t, u: est(MA, t), mood=(-0.9, -0.6, 0.0), shake=0.4)
    MO.act(a[205], b[205], mood=lambda t, u: (-1.0, -0.6, talk(a[205] + 0.4, b[205] - 0.5)(t, u)[2]))
    S.on(MA, list(range(187, 208)))
    S.on(DV, [189, 191, 192, 193])
    S.on(JG, [199, 200, 201, 202])
    S.on(MO, [204, 205, 206, 207], step=2)
    S.on(PA, [204, 205, 206, 207], step=2)
    tear(MA, a[201] + 1.0, 2.5, 0.45)
    tear(JG, a[201] + 1.4, 2.4, -0.45, name="tearJ")
    # the rope: boat stern to the post while tied; slack and dragging after Jagdish unties it
    rope = P["rope"]
    rope.rotation_mode = "QUATERNION"

    def rope_fn(t):
        s = ROPE_END(t)
        e = POST if t < a[201] + 0.4 else s + Vector((-1.2, 1.5, -0.55))
        d = e - s
        return s, Vector((0, 0, 1)).rotation_difference(d.normalized())
    bake_fn(rope, a[196], E, rope_fn, 2)
    for f in (int(F(a[196])), int(F(a[201] + 0.4)), int(F(E))):
        t = (f - 1) / FPS
        s = ROPE_END(t)
        e = POST if t < a[201] + 0.4 else s + Vector((-1.2, 1.5, -0.55))
        ANIM.put(rope, "scale", 2, f, (e - s).length, "const")
    vis(rope, [(a[196], E)])
    # ------------------------------------------------------------- cameras
    def c187(t):                                 # crane up from the water's surface to a high wide
        u = seg(t, a[187], b[187])
        bp = Vector((bx(t), by(t), 0.4))
        pos = bp + Vector((lerp(-5.0, -16.0, u), lerp(-6.0, -22.0, u), lerp(0.6, 14.0, u)))
        return dict(pos=pos, look=bp + Vector((lerp(1.5, 3.0, u), lerp(2.0, 6.0, u), 0.0)), focus=(bp - pos).length, fstop=8.0)
    S.shoot(187, c187)
    S.shoot(188, lambda t: on(MA, t, "MS", 50, yaw=0.6, az=-15, tt=a[188] + 1))
    S.shoot(189, lambda t: dict(pos=eyes(MA, a[189]) + Vector((0.2, 0.0, 0.0)), look=est(DV, t) + Vector((0, 0, -0.5)), focus=13.5, fstop=4.0))
    S.shoot(190, lambda t: on(MA, t, "CU", 85, yaw=N, az=-35, tt=a[190]))
    S.shoot(191, lambda t: on(DV, t, "MS", 85, yaw=S_, az=-10, tt=a[191]))

    def c192(t):                                 # boat-mounted: rides the bow, looking back at her
        bp = Vector((bx(t), by(t), 0.0))
        pos = bp + Vector((2.6, -0.5, 1.2))
        return dict(pos=pos, look=est(MA, t) + Vector((0, 0, -0.35)), focus=2.6, fstop=2.8)
    S.shoot(192, c192)
    S.shoot(193, lambda t: dict(pos=eyes(MA, a[193]) + Vector((0.2, 0, 0)), look=Vector((DVX, SHORE_Y + 2, 1.3)), focus=14.0, fstop=4.0))
    S.shoot(194, lambda t: on(MA, t, "CU", 85, yaw=0.3, az=-25, tt=a[194]))
    S.shoot(195, lambda t: push(on(MA, t, "MCU", 85, yaw=S_ + 0.4, az=-20, tt=b[195]), 0.2 * seg(t, a[195], b[195])))
    S.shoot(196, lambda t: dict(pos=Vector((bx(t) + 3.0, by(t) - 6.5, 1.2)), look=Vector((bx(t), by(t), 0.6)), focus=7.1, fstop=4.0))
    S.shoot(197, lambda t: dict(pos=ROPE_END(t) + Vector((-0.4, -1.4, 0.45)), look=ROPE_END(t) + Vector((-0.6, 0.6, -0.05)), focus=1.6, fstop=2.8))
    S.shoot(198, lambda t: on(MA, t, "MS", 50, yaw=math.pi - 0.2, az=-30, tt=a[198]))
    S.shoot(199, lambda t: dict(pos=eyes(MA, a[199]) + Vector((0.2, 0, 0)), look=est(JG, t) + Vector((0, 0, -0.6)), focus=13.0, fstop=4.0))
    S.shoot(200, lambda t: dict(pos=POST + Vector((1.2, -3.0, 0.4)), look=POST + Vector((0.3, 0.2, 0.0)), focus=3.2, fstop=2.8))
    S.shoot(201, lambda t: dict(pos=Vector((bx(t) + 24.0, by(t) + 3.0, 1.8)), look=Vector((bx(t) + 0.5, (by(t) + SHORE_Y) / 2, 0.9)), focus=24.0, fstop=8.0))
    S.shoot(202, lambda t: dict(pos=eyes(MA, a[202]) + Vector((0.2, 0, 0)), look=est(JG, t) + Vector((0, 0, -0.5)), focus=14.0, fstop=4.0))
    S.shoot(203, lambda t: on(MA, t, "MS", 50, yaw=0.2, az=-20, tt=a[203]))
    S.shoot(204, lambda t: dict(pos=Vector((bx(t) - 1.0, by(t) + 1.0, 1.4)), look=Vector((7.9, SHORE_Y, 1.2)), focus=13.0, fstop=4.0))
    S.shoot(205, lambda t: on(MO, t, "MS", 85, yaw=S_, az=8, tt=a[205]))
    S.shoot(206, lambda t: on(MA, t, "MCU", 85, yaw=N - 0.3, az=-6, tt=a[206]))

    def c207(t):                                 # drone pull back from behind her, toward the rising sun
        u = seg(t, a[207], E)
        bp = Vector((bx(t), by(t), 0.5))
        pos = bp + Vector((lerp(-3.5, -40.0, u), lerp(0.6, 6.0, u), lerp(1.6, 18.0, u)))
        return dict(pos=pos, look=bp + Vector((lerp(6, 40, u), 0, lerp(0.5, 2.0, u))), focus=(bp - pos).length, fstop=8.0)
    S.shoot(207, c207)
    # ------------------------------------------------------------- lights: soft cool fill, moon rims; warm at the end
    cool = dict(side="L", ang=35, el=15, d=2.5, w=18, k=7500, size=2.0)
    for n in (188, 190, 194, 195, 198, 203, 206):
        S.light(n, lambda t: head(MA, t), fill=cool, rim=dict(side="R", ang=155, el=20, d=2.0, w=30, k=7500))
    S.light(195, lambda t: head(MA, t), fill=dict(side="L", ang=35, el=15, d=2.0, w=25, k=5000, size=2.0), rim=dict(side="R", ang=155, el=20, d=2.0, w=30, k=7500))
    S.light(191, lambda t: head(DV, t), fill=dict(side="L", ang=20, el=15, d=3, w=40, k=7000, size=2.5))
    S.light(205, lambda t: head(MO, t), fill=dict(side="L", ang=20, el=15, d=3, w=40, k=7000, size=2.5))
    S.light(200, lambda t: head(JG, t), rim=dict(side="R", ang=160, el=20, d=2.0, w=40, k=7500), fill=dict(side="L", ang=40, el=20, d=2.5, w=12, k=7000))
    S.light(197, ROPE_END(a[197]), kick=dict(side="R", ang=120, el=30, d=1.2, w=12, k=7500))
