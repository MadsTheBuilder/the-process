# Scene 13 - PRETENDING - INT. House (Drawing Room) - Afternoon (shots 85-91, 28 s)
# She bursts in and locks herself in the house she fled. Curtains half drawn: one hard sun slash across the floor,
# the rest low key. Warm kitchen spill (the father as cook) from the east door.
import math

from mathutils import Quaternion, Vector

from kit import *
from film import *
import cast
import hs
import props
import sets
from sets import H


def dr_afternoon(S, st, t):
    C = sets.mats()
    sets.sun_dir(st["L"]["Sun"], 245, 24)
    S.state(t, Sun=(5.0, 5000), WinDR1=(70, 5600), WinDR2=(50, 5600), Kitchen=(160, 3200), WinCorr=(15, 6000), Lamp=0)
    S.emit(t, C["sky_win"], 2.5)
    S.world(t, (0.4, 0.38, 0.34), 0.03)


def build(S):
    T = S.T
    a = {n: T[n][0] for n in T}
    b = {n: T[n][1] for n in T}
    st = hs.house(S)
    dr_afternoon(S, st, 0)
    S.exposure(0, 0.45)
    # half-drawn curtains: dark panels over most of each south window, leaving a slit for the sun slash
    cm = M((0.25, 0.18, 0.12), 0.95)
    for x in (-3.1, 3.1):
        new_obj("CurtainL", box_mesh("cl", 0.62, 0.03, 1.5), cm, loc=(x - 0.42, 0.32, 0.85))
        new_obj("CurtainR", box_mesh("cr", 0.5, 0.03, 1.5), cm, loc=(x + 0.48, 0.32, 0.85))
    for k in ("net0", "net1"):
        st["P"][k].hide_render = st["P"][k].hide_viewport = True
    haze, _ = fog_box("DRDust", (0, 3, 1.6), (9.8, 5.8, 3.1), 0.012, (0.92, 0.88, 0.8), 0.45)
    # the door bursts open, she shuts it from inside
    hs.door_keys(st, [(0, 0, "const"), (a[85] + 0.2, 0, "bez"), (a[85] + 0.7, 80, "bez"), (a[85] + 1.6, 80, "bez"), (a[85] + 2.3, 0, "const")])
    MA = cast.mamta("home")
    PA = cast.papa()
    IN = Vector((0.05, 0.48))
    MA.at(a[85], 0.0, -0.9, math.pi / 2).walk(a[85] + 1.2, 0.15, 0.95, gait="run").stay(a[85] + 1.5).stay(a[85] + 2.0, -math.pi / 2, tt=0.4)
    MA.walk(a[85] + 2.4, IN.x, IN.y, yaw=-math.pi / 2, mode="smooth", gait="stand").stay(b[86])
    MA.stay(a[87] + 1.6).stay(a[87] + 2.8, math.pi / 2, tt=1.1).stay(b[88])
    MA.walk(a[89] + 2.6, 0.75, 1.75, yaw=math.radians(40), mode="smooth").stay(b[91], math.radians(40))
    MA.act(a[85] + 1.6, a[87] + 1.7, armL=Vector((-0.3, 0.2, 1.05)), armR=Vector((0.32, 0.2, 1.1)), lean=0.12, hp=0.1,
           mood=lambda t, u: (-0.9, -0.5, 0.25 + 0.15 * abs(math.sin(t * 6))), bob=0.012, bobf=1.6, eyes=lambda t, u: 0.15 if t > a[86] + 0.3 else 1.0)
    MA.act(a[87] + 0.6, a[87] + 1.4, eyes=lambda t, u: 1.0, mood=(-0.9, -0.5, 0.1))
    MA.act(a[87] + 1.6, b[91], mood=lambda t, u: (-0.2, lerp(-0.3, 0.25, seg(t, a[87] + 1.6, a[87] + 3)), talk(a[89] + 0.4, a[89] + 1.0)(t, u)[2]),
           look=lambda t, u: est(PA, t), armR=("loc", 0.06, -0.28, 0.42))
    MA.act(a[89] + 0.5, a[90] + 2.5, armL=lambda t, u: ("rel", 0.18, 0.05, -0.2) if t < a[89] + 2.4 else est(PA, t) + Vector((-0.25, -0.15, -0.55)))
    S.on(MA, [85, 86, 87, 88, 89, 90, 91])
    # Papa comes out of the kitchen with a stained ladle
    PP = Vector((1.55, 2.85))
    PA.at(a[87], 3.9, 4.5, math.radians(-135)).walk(a[88] + 0.8, PP.x, PP.y, mode="smooth").stay(b[91], math.radians(-140))
    PA.act(a[87], b[91], armR=("rel", 0.22, -0.08, -0.05), look=lambda t, u: est(MA, t) + Vector((0, 0, -0.03)),
           mood=lambda t, u: (0.0, 0.3, talk(a[88] + 0.6, a[88] + 2.6)(t, u)[2] + talk(a[91] + 0.4, b[91] - 0.4)(t, u)[2]))
    PA.act(a[90] + 0.8, b[91], armL=lambda t, u: est(MA, t) + Vector((0.35, 0.3, -0.55)) if t < a[90] + 3.0 else ("rel", 0.2, 0.05, -0.15))
    PA.act(a[91], b[91], mood=lambda t, u: (0.3, 0.6, talk(a[91] + 0.4, b[91] - 0.4)(t, u)[2]))
    S.on(PA, [87, 88, 89, 90, 91])
    ld = props.ladle()
    hold(ld, PA, "R", a[87], b[91], off=(0.0, 0.0, -0.02))
    pb = props.poly_bag()
    bake_fn(pb, a[89] + 1.0, a[90] + 2.6, lambda t: (MA.J(t)["hand"]["L"] + Vector((0, 0, -0.08)), None), 2, rot=False)
    bake_fn(pb, a[90] + 2.6, b[91], lambda t: (PA.J(t)["hand"]["L"] + Vector((0, 0, -0.08)), None), 2, rot=False)
    vis(pb, [(a[89] + 1.0, b[91])])
    # sweat beads on her forehead (90)
    sw = M((0.85, 0.9, 1.0), 0.02, emit=(0.6, 0.7, 0.8), strength=0.8)
    for k, side in enumerate((-0.35, 0.1, 0.4)):
        d_ = new_obj("sweat%d" % k, sphere_mesh("sw", 0.004, 6, 4), sw)
        bake_fn(d_, a[90], b[90], lambda t, side=side: ((lambda j: j["head_c"] + j["hf"] * MA.hr * 0.82 + j["hu"] * MA.hr * 0.5
                                                         + j["hf"].cross(j["hu"]) * side * MA.hr)(MA.J(t)), None), 2, rot=False)
        vis(d_, [(a[90], b[90])])

    # cameras
    S.shoot(85, lambda t: dict(pos=Vector((0.55, 2.9, 1.45)), look=Vector((0.05, 0.3, 1.25)), focus=2.6, fstop=2.8))
    S.shoot(86, lambda t: dict(pos=Vector((1.85, 0.62, 1.48)), look=head(MA, t) + Vector((0, 0, -0.02)), focus=1.85, fstop=2.0))
    S.shoot(87, lambda t: on(MA, b[87], "MCU", 85, yaw=math.pi / 2, az=8, tt=b[87]))
    S.shoot(88, lambda t: dict(pos=Vector((-0.45, 0.8, 1.5)), look=head(PA, a[88] + 1.2) + Vector((0, 0, -0.35)), focus=2.5, fstop=2.8))
    S.shoot(89, lambda t: dict(pos=Vector((-1.6, 2.4, 1.45)), look=mid(head(MA, t), head(PA, t)) + Vector((0, 0, -0.3)), focus=2.4, fstop=2.8))
    S.shoot(90, lambda t: ots(PA, MA, t, 85, mag="CU", side=1))
    S.shoot(91, lambda t: on(PA, t, "MCU", 85, yaw=math.radians(-140), az=10, tt=a[91]))
    S.light(85, (0.0, 0.4, 1.3), key=dict(side="R", ang=60, el=20, d=2, w=15, k=5000, size=0.4))
    S.light(86, lambda t: head(MA, t), key=dict(side="R", ang=45, el=12, d=1.4, w=30, k=5000, size=0.05))
    S.light(87, lambda t: head(MA, t), key=dict(side="L", ang=45, el=15, d=1.8, w=40, k=4300, size=1.0))
    S.light(88, lambda t: head(PA, t), rim=dict(side="R", ang=160, el=25, d=1.6, w=55, k=3200, size=0.8), key=dict(side="L", ang=30, el=15, d=2, w=10, k=4000))
    S.light(89, lambda t: head(MA, t), key=dict(side="R", ang=50, el=20, d=2, w=35, k=3600, size=1.0))
    S.light(90, lambda t: head(MA, t), key=dict(side="R", ang=40, el=18, d=1.6, w=45, k=3600, size=0.8), kick=dict(side="L", ang=30, el=35, d=1.0, w=6, k=4500))
    S.light(91, lambda t: head(PA, t), key=dict(side="L", ang=40, el=18, d=1.6, w=45, k=3400, size=1.0), fill=dict(side="R", ang=40, el=10, d=1.8, w=15, k=3400))
