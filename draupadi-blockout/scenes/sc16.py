# Scene 16 - FEEDING - INT. House (Mother's Room) - Afternoon (shots 105-111, 28 s)
# Duty without care: Mamta on the chair, spooning food mechanically, locked off in profile. The steel jug and glass
# (planted here) pay off when the glass falls in Scene 19 and the water spills in Scene 26.
import math

from mathutils import Quaternion, Vector

from kit import *
from film import *
import cast
import hs
import props
import sets
from sets import H
from scenes.sc08 import mother_in_bed, HIP, mo_room_day

CHAIR = H["mo_chair"]
SIDE_T = H["mo_side"]


def mouth_of(MO, t):
    j = MO.J(t)
    return j["head_c"] + j["hf"] * MO.hr * 0.95 - j["hu"] * MO.hr * 0.45


def build(S):
    T = S.T
    a = {n: T[n][0] for n in T}
    b = {n: T[n][1] for n in T}
    st = hs.house(S)
    mo_room_day(S, 0, win=150, k=5500)
    S.exposure(0, 0.5)
    MO = cast.mother()
    mother_in_bed(MO, 0, S.END)
    MO.act(0, S.END, hp=0.62, eyes=0.8)
    MA = cast.mamta("fresh")
    PLATE = Vector((CHAIR.x + 0.32, CHAIR.y, 0.66))
    MA.at(0, CHAIR.x, CHAIR.y, 0.15).stay(a[108] + 0.5).stay(b[108], 0.15)
    MA.walk(a[110] + 0.3, 7.15, 10.85, mode="smooth").stay(a[110] + 0.6, math.radians(40)).stay(a[111] + 0.4)
    MA.walk(a[111] + 1.6, 6.45, 12.1, yaw=math.radians(60), mode="smooth").stay(a[111] + 4.0).walk(b[111] + 0.6, 4.6, 10.6, mode="smooth")
    MA.act(0, a[108] + 1.4, sit=1.0, seat=0.47, _hold0=True)
    MA.act(0, b[107], look=lambda t, u: est(MO, t) + Vector((0, 0.72, -0.85)), mood=(-0.1, -0.2, 0.0), eyes=0.8)
    spoon = lambda t, u: (PLATE + Vector((0.02, 0, 0.08))).lerp(mouth_of(MO, t) + Vector((-0.06, 0, 0)), 0.5 - 0.5 * math.cos(t * 1.9))
    MA.act(0, b[106], armR=spoon, armL=PLATE + Vector((-0.02, 0.08, 0.02)))
    MA.act(a[110] + 0.4, b[110], armR=lambda t, u: Vector((SIDE_T.x - 0.08, SIDE_T.y + 0.05, 0.95)), armL=lambda t, u: Vector((SIDE_T.x + 0.1, SIDE_T.y - 0.08, 0.72)),
           look=Vector((SIDE_T.x, SIDE_T.y, 0.65)), lean=0.3)
    MA.act(a[111] + 1.0, a[111] + 4.0, armR=lambda t, u: mouth_of(MO, t) + Vector((-0.05, 0, -0.02)), look=lambda t, u: est(MO, t) + Vector((0, 0.72, -0.85)))
    MO.act(0, b[106], mood=lambda t, u: (0.0, 0.0, 0.15 * max(0, math.sin(t * 1.9 - 0.4))), look=lambda t, u: est(MA, t))
    MO.act(a[107], b[107], armR=lambda t, u: Vector((6.35, 12.85, 0.85 + 0.04 * math.sin(t * 6))), hy=lambda t, u: 0.2 * math.sin(t * 5))
    MO.act(a[109], b[109], mood=talk(a[109] + 0.5, b[109] - 0.6, (-0.4, -0.2), 0.18, 4), look=lambda t, u: est(MA, t), armR=Vector((6.3, 12.6, 0.8)))
    MO.act(a[111] + 1.6, a[111] + 3.8, mood=(0, 0, 0.12), hp=0.85)
    S.on(MO, list(range(105, 112)), step=2)
    S.on(MA, list(range(105, 112)))
    th = props.thaali()
    bake_fn(th, 0, a[108] + 0.4, lambda t: (PLATE, None), 6, rot=False)
    bake_fn(th, a[108] + 0.4, S.END, lambda t: (Vector((CHAIR.x - 0.05, CHAIR.y, 0.47)), None), 6, rot=False)
    sp = new_obj("Spoon", cyl_mesh("sp", 0.006, 0.14, 6), M((0.75, 0.76, 0.78), 0.15, 1.0))
    hold(sp, MA, "R", 0, b[106], off=(0.0, 0.0, 0.02))
    vis(sp, [(0, b[106])])
    # the steel jug pours into the glass, then the glass goes to her mouth and back
    jug, gl = st["P"]["jug"], st["P"]["glass"]
    J0, G0 = jug.location.copy(), gl.location.copy()
    jug.rotation_mode = "XYZ"
    keys_vec(jug, "location", [(0, J0), (a[110] + 0.5, J0), (a[110] + 1.0, J0 + Vector((0.08, -0.05, 0.22))), (b[110] - 0.2, J0 + Vector((0.08, -0.05, 0.22))), (b[110] + 0.1, J0)])
    keys(jug, "rotation_euler", 0, [(0, 0.0), (a[110] + 0.9, 0.0), (a[110] + 1.4, 1.2), (b[110] - 0.4, 1.2), (b[110], 0.0)])
    bake_fn(gl, a[111] + 0.6, a[111] + 4.2, lambda t: (MA.J(t)["hand"]["R"] + Vector((0, 0, -0.04)), None), 2, rot=False)
    stream = new_obj("Pour", cyl_mesh("pr", 0.006, 0.2, 6), M((0.8, 0.85, 0.9), 0.05, alpha=0.6), loc=G0 + Vector((0, 0, 0.1)))
    vis(stream, [(a[110] + 1.4, b[110] - 0.4)])

    # cameras: profile two-shot, locked off
    S.shoot(105, lambda t: dict(pos=Vector((6.35, 9.35, 1.45)), look=Vector((6.25, 12.95, 0.8)), focus=3.4, fstop=2.8))
    S.shoot(106, lambda t: on(MA, a[106] + 1, "CU", 85, yaw=0.15, az=-55, tt=a[106]))
    S.shoot(107, lambda t: dict(pos=Vector((5.55, 13.25, 1.3)), look=head(MO, t) + Vector((0, -0.05, -0.05)), focus=1.5, fstop=2.0))
    S.shoot(108, lambda t: dict(pos=Vector((6.25, 10.0, 1.3)), look=Vector((5.7, 12.4, 1.0)), focus=2.5, fstop=2.8))
    S.shoot(109, lambda t: dict(pos=Vector((5.55, 13.25, 1.3)), look=head(MO, t) + Vector((0, -0.05, -0.05)), focus=1.5, fstop=2.0))
    S.shoot(110, lambda t: dict(pos=Vector((7.78, 10.3, 1.25)), look=Vector((SIDE_T.x - 0.05, SIDE_T.y, 0.7)), focus=0.98, fstop=4.0))
    S.shoot(111, lambda t: dict(pos=Vector((5.3, 10.3, 1.4)), look=Vector((6.6, 12.6, 0.9)), focus=2.6, fstop=2.8))
    W = 5500
    S.light(105, lambda t: head(MO, t), rim=dict(side="R", ang=150, el=25, d=2.0, w=40, k=W, size=1.0))
    S.light(106, lambda t: head(MA, t), key=dict(side="L", ang=100, el=15, d=1.6, w=30, k=W, size=0.8))
    S.light(107, lambda t: head(MO, t), key=dict(side="R", ang=30, el=40, d=1.4, w=40, k=W, size=1.0))
    S.light(108, lambda t: head(MA, t), key=dict(side="R", ang=70, el=20, d=2.0, w=25, k=W, size=1.0))
    S.light(109, lambda t: head(MO, t), key=dict(side="R", ang=30, el=40, d=1.4, w=40, k=W, size=1.0))
    S.light(110, (SIDE_T.x, SIDE_T.y, 0.66), key=dict(side="R", ang=60, el=40, d=1.0, w=20, k=W, size=0.6))
    S.light(111, lambda t: head(MO, t), key=dict(side="R", ang=60, el=30, d=2.0, w=35, k=W, size=1.0))
