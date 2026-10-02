# Scene 25 - NOTHING MORE - INT. House (Drawing Room) - Night (shots 181-183, 15 s)
# A single bare overhead bulb. She follows Papa across the room; he stops with his back to her - for once his
# face is toward us and broken. He walks out of frame; she stands alone in the bulb's pool.
import math

from mathutils import Vector

from kit import *
from film import *
import cast
import hs
import sets


def build(S):
    T = S.T
    a = {n: T[n][0] for n in T}
    b = {n: T[n][1] for n in T}
    st = hs.house(S)
    C = sets.mats()
    bulb = new_obj("DRBareBulb", sphere_mesh("db", 0.05, 10, 8), C["bulb"], loc=(0.3, 3.0, 2.65))
    new_obj("DRBareBulbWire", cyl_mesh("dbw", 0.006, 0.5, 4), C["black"], bulb, loc=(0, 0, 0.04))
    S.state(0, DRBulb=(200, 2900), TubeCorr=(10, 7000))
    S.emit(0, C["bulb"], 45.0)
    S.world(0, (0.01, 0.01, 0.02), 0.01)
    S.exposure(0, 1.1)
    MA = cast.mamta("night")
    PA = cast.papa()
    PA.at(0, 0.6, 2.0, math.pi / 2).walk(b[181] - 0.2, 0.2, 4.4, mode="smooth").stay(b[182]).walk(a[183] + 2.0, -0.6, 6.6, mode="smooth")
    MA.at(0, 0.5, 0.7, math.pi / 2).walk(b[181], 0.3, 2.9, mode="smooth").stay(b[183])
    MA.act(0, b[181], mood=talk(a[181] + 0.6, a[181] + 3.0, (-0.6, -0.3)), look=lambda t, u: est(PA, t))
    MA.act(a[182], b[183], look=lambda t, u: est(PA, t) if t < a[183] + 1.5 else Vector((0.3, 6.0, 1.5)), mood=(-1.0, -0.8, 0.05),
           eyes=lambda t, u: 1.0 if t < a[183] + 3 else 0.8)
    PA.act(a[182], b[182], mood=lambda t, u: (-1.0, -0.8, talk(a[182] + 0.6, a[182] + 2.4)(t, u)[2]), hp=0.25, shake=0.6)
    S.on(MA, [181, 182, 183])
    S.on(PA, [181, 182, 183])
    tear(PA, a[182] + 1.4, 2.4, -0.45)
    tear(MA, a[183] + 2.4, 2.5, 0.45)

    def c181(t):                                  # gimbal follow behind Papa, Mamta trailing
        h = est(PA, t)
        pos = h + Vector((0.4, -2.6, 0.1))
        return dict(pos=pos, look=h + Vector((0, 0, -0.3)), focus=2.6, fstop=2.8)
    S.shoot(181, c181)
    S.shoot(182, lambda t: dict(pos=est(PA, b[181]) + Vector((0.1, 3.05, -0.02)), look=est(PA, t) + Vector((0, 0, -0.08)), focus=3.1, fstop=2.0))
    S.shoot(183, lambda t: dict(pos=Vector((0.3, 5.75, 1.6)), look=est(MA, b[183]) + Vector((0, 0, -0.45)), focus=3.3, fstop=2.8))
    S.light(181, lambda t: head(PA, t), key=dict(side="L", ang=20, el=75, d=1.5, w=20, k=2900, size=0.1))
    S.light(182, lambda t: head(PA, t), key=dict(side="R", ang=15, el=15, d=1.4, w=30, k=6000, size=1.0))
    S.light(183, lambda t: head(MA, t), key=dict(side="L", ang=10, el=80, d=1.0, w=30, k=2900, size=0.1))
