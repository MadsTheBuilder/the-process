# Scene 23 - WHAT SHE SEES - INT. House (Drawing Room) - Night (shots 165-166, 9 s)
# She rolls her suitcase across the moonlit drawing room toward the open main door. Her feet stop. What she sees
# is withheld (revealed in 167): the warm porch light finds her face.
import math

from mathutils import Quaternion, Vector

from kit import *
from film import *
import cast
import hs
import props
import sets


def dr_moon(S, st, t, porch=True):
    C = sets.mats()
    sets.sun_dir(st["L"]["Moon"], -70, 28)
    S.state(t, Moon=(0.9, 7500), WinDR1=(35, 8000), WinDR2=(35, 8000), Porch=(180 if porch else 0, 3200), DoorDay=(30 if porch else 0, 3200))
    S.emit(t, C["porch"], 25.0 if porch else 0.0)
    S.emit(t, C["sky_win"], 0.4)
    S.world(t, (0.02, 0.03, 0.06), 0.03)


def build(S):
    T = S.T
    a = {n: T[n][0] for n in T}
    b = {n: T[n][1] for n in T}
    st = hs.house(S)
    dr_moon(S, st, 0)
    S.exposure(0, 1.2)
    hs.door_keys(st, [(0, 85, "const")])
    MA = cast.mamta("night")
    MA.at(0, -0.4, 6.0, -math.pi / 2).walk(b[165] + 0.3, 0.1, 2.2).walk(a[166] + 1.2, 0.15, 1.9, mode="smooth").stay(b[166])
    MA.act(0, b[165], armL=lambda t, u: (lambda j: j["head_c"] + j["hf"] * 0.1 + j["tl"] * 0.03)(MA.J(t)) if (t % 2.2) < 0.9 else ("rel", 0.05, 0.05, -0.3),
           armR=("loc", -0.25, -0.3, 0.38), mood=(-0.9, -0.6, 0.1))
    MA.act(a[166], b[166], armR=("loc", -0.25, -0.3, 0.38), look=lambda t, u: Vector((0.0, -1.2, 1.4)) if t < a[166] + 2.6 else Vector((0.0, -1.0, 0.5)),
           mood=(-0.8, -0.6, 0.0))
    S.on(MA, [165, 166])
    tear(MA, a[166] + 2.8, 1.8, 0.45)
    case = props.suitcase()

    def roll(t):
        j = MA.J(t)
        h = j["hand"]["R"]
        return h + Vector((0, 0, -0.62)) - fvec(j["yaw"]) * 0.25, Quaternion((0, 0, 1), j["yaw"] + math.pi / 2) @ Quaternion((1, 0, 0), 0.35)
    bake_fn(case, 0, b[166], roll, 2)

    def c165(t):                                  # gimbal lead: backs toward the door ahead of her
        h = est(MA, t)
        pos = h + Vector((0.3, -2.4, -0.05))
        return dict(pos=pos, look=h + Vector((0, 0, -0.3)), focus=2.4, fstop=2.8)
    S.shoot(165, c165)
    S.shoot(166, lambda t: on(MA, t, "CU", 85, yaw=-math.pi / 2, az=-6, tt=a[166]))
    S.light(165, lambda t: head(MA, t), key=dict(side="R", ang=60, el=40, d=2.5, w=15, k=7500, size=1.0))
    S.light(166, lambda t: head(MA, t), key=dict(side="L", ang=10, el=8, d=2.0, w=35, k=3200, size=0.5), rim=dict(side="R", ang=150, el=30, d=2, w=10, k=7500))
