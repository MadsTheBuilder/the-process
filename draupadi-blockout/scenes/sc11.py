# Scene 11 - WHITE COATS - EXT. Small Town - Day (shots 71-75, 19 s)
# A grey street (runs east-west at y=200). Mamta walks east, folding the prescription. A flood of medical students
# in white coats parts around her from every side; her view whips; she freezes, drowned in white.
import math
import random

from mathutils import Quaternion, Vector

from kit import *
from film import *
import cast
import props
import sets

Y0 = 200.0


def build(S):
    T = S.T
    E = S.END
    a = {n: T[n][0] for n in T}
    b = {n: T[n][1] for n in T}
    st = sets.build_street(E)
    L = st["L"]
    sets.sun_dir(L["T_Sky"], 210, 70)
    sets.sun_dir(L["T_Sun"], 200, 60)
    S.state(0, T_Sky=(3.2, 6500), T_Sun=(0.6, 6500))
    S.world(0, (0.62, 0.66, 0.72), 0.7)
    S.exposure(0, -0.55)
    MA = cast.mamta("home")
    STOP = Vector((-6.6, Y0 - 0.4))
    MA.at(0, -13.6, Y0 - 0.5, 0.0).walk(b[72], -7.2, Y0 - 0.45).walk(a[73] + 1.2, STOP.x, STOP.y, mode="smooth").stay(E, 0.0)
    fold = lambda t, u: ("rel", 0.24, -0.04 + 0.03 * math.sin(t * 5), -0.18)
    MA.act(0, a[72], armL=fold, armR=lambda t, u: ("rel", 0.24, 0.04 - 0.03 * math.sin(t * 5), -0.18), hp=0.35, mood=(-0.4, -0.2, 0.0))
    MA.act(a[72], b[72], armR=lambda t, u: (lambda j: j["sh_c"] + j["tl"] * 0.2 - j["spine"] * 0.36 + j["tf"] * 0.05)(MA.J(t)),
           hp=0.4, mood=(-0.4, -0.2, 0.0))
    MA.act(a[73], E, look=lambda t, u: est(MA, t) + Vector((math.cos(t * 1.7) * 3, math.sin(t * 1.3) * 3, 0)) if t < a[75] else
           est(MA, t) + Vector((3, 0, 0)), mood=lambda t, u: (-0.9, -0.6, 0.15 if t < a[75] else 0.0), shake=0.3)
    S.on(MA, list(range(71, 76)))
    rx = props.paper("Prescription")
    hold(rx, MA, "L", 0, a[72] + 1.2, off=(0.02, 0, 0.0))
    vis(rx, [(0, a[72] + 1.2)])
    hb = new_obj("Handbag", box_mesh("hb", 0.28, 0.1, 0.24, False), M((0.30, 0.20, 0.12), 0.7))
    bake_fn(hb, 0, E, lambda t: (MA.J(t)["sh_c"] + MA.J(t)["tl"] * (MA.sw * 1.2) - MA.J(t)["spine"] * 0.33,
                                  basis_quat(MA.J(t)["tf"], MA.J(t)["spine"])), 2)
    # street life: pedestrians and vendors (before the coats arrive)
    rnd = random.Random(21)
    for i in range(10):
        e = cast.extra("Ped%d" % i, 300 + i)
        x0 = rnd.uniform(-30, 10)
        y = Y0 + rnd.choice((-3.4, -2.8, 2.6, 3.3, 1.8))
        d = rnd.choice((-1, 1))
        e.at(0, x0, y, 0 if d > 0 else math.pi).walk(E, x0 + d * E * rnd.uniform(0.8, 1.2), y)
        e.act(0, E, look=None)
        S.on(e, list(range(71, 76)), step=2)
    for i, x in enumerate((-20, -2, 16)):
        v = cast.extra("Vendor%d" % i, 330 + i)
        v.at(0, x + 0.3, Y0 - 4.0, math.pi / 2).stay(E)
        S.on(v, list(range(71, 76)), step=6)
    # the white coats: 28 students flowing past her both ways, parting around her
    WHITE = (0.92, 0.92, 0.90)
    t_arrive = a[73] + 0.4
    for i in range(28):
        e = cast.extra("Coat%d" % i, 400 + i, top=WHITE, coat=True)
        d = 1 if i % 2 else -1
        lane = rnd.choice((-1.9, -1.3, -0.85, 0.65, 1.1, 1.6, 2.2))
        sp = rnd.uniform(1.15, 1.55)
        tc = t_arrive + rnd.uniform(0.0, E - t_arrive - 1.0)           # when they pass her
        x_pass = STOP.x
        x0 = x_pass - d * sp * (tc - a[71] + 0.5)
        x1 = x_pass + d * sp * (E - tc + 0.5)
        y = STOP.y + lane
        e.at(a[71], x0, y, 0 if d > 0 else math.pi).walk(E, x1, y)
        e.act(0, E, look=None, mood=(0.0, 0.5, 0.15 * (i % 3)), armL=("rel", 0.2, 0.05, -0.15) if i % 4 == 0 else None)
        S.on(e, [73, 74, 75], step=1)
    # cameras
    def c71(t):                                    # gimbal lead: backs away down the street ahead of her
        h = head(MA, t)
        pos = h + Vector((10.0, 0.6, 0.0))
        return dict(pos=pos, look=h + Vector((0, 0, -0.55)), focus=10.0, fstop=4.0)
    S.shoot(71, c71)

    def c72(t):
        j = MA.J(t)
        p = j["sh_c"] + j["tl"] * 0.2 - j["spine"] * 0.36
        pos = p + Vector((0.9, -0.55, 0.3))
        return dict(pos=pos, look=p, focus=(p - pos).length, fstop=2.8)
    S.shoot(72, c72)
    S.shoot(73, lambda t: on(MA, t, "MS", 50, yaw=0.0, az=-20, tt=a[73] + 1.5))

    def c74(t):                                    # POV: whips left, right, forward, back
        e = eyes(MA, t) + Vector((0.05, 0, 0))
        k = [(a[74], 0.0), (a[74] + 0.6, 0.0), (a[74] + 0.85, 85.0), (a[74] + 1.6, 85.0), (a[74] + 1.9, -80.0),
             (a[74] + 2.6, -80.0), (a[74] + 2.9, 10.0), (a[74] + 3.3, 10.0), (a[74] + 3.65, 178.0), (b[74], 178.0)]
        ang = k[0][1]
        for (t0, v0), (t1, v1) in zip(k, k[1:]):
            if t0 <= t <= t1:
                ang = lerp(v0, v1, seg(t, t0, t1))
        y = math.radians(ang)
        return dict(pos=e, look=e + Vector((math.cos(y), math.sin(y), -0.08)) * 3, focus=2.0, fstop=4.0)
    S.shoot(74, c74)
    S.shoot(75, lambda t: on(MA, t, "CU", 85, yaw=0.0, az=0, tt=a[75]))
    S.light(71, lambda t: head(MA, t), key=dict(side="R", ang=30, el=60, d=3, w=60, k=6500, size=3))
    S.light(72, lambda t: head(MA, t), key=dict(side="R", ang=30, el=60, d=3, w=40, k=6500, size=3))
    S.light(73, lambda t: head(MA, t), key=dict(side="L", ang=30, el=55, d=3, w=50, k=6500, size=3))
    S.light(75, lambda t: head(MA, t), key=dict(side="L", ang=30, el=50, d=2, w=25, k=6500, size=2))
