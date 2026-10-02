# Scene 7 - THE UNCHANGED ROOM - INT. House (Drawing Room) - Day (shots 43-48, 28 s)
# Nothing has changed in ten years. Net-curtain daylight from the south windows, one warm lamp in the SE corner,
# dust hanging in the air. She turns where she stands; the room turns the other way around her.
import math

from mathutils import Quaternion, Vector

from kit import *
from film import *
import cast
import hs
import props
import sets
from sets import H
from scenes.sc05 import carry

MID = Vector((0.35, 2.85))


def dr_day(S, st, t, lamp_w=45):
    C = sets.mats()
    S.state(t, WinDR1=(400, 5600), WinDR2=(400, 5600), WinCorr=(30, 6000), Lamp=(lamp_w, 3000), WinMo=(30, 6000), WinM=(30, 6000))
    S.emit(t, C["sky_win"], 3.5)
    S.emit(t, C["bulb2"], 6.0)
    S.world(t, (0.4, 0.42, 0.4), 0.03)


def build(S):
    T = S.T
    st = hs.house(S)
    dr_day(S, st, 0)
    S.exposure(0, 0.45)
    hs.door_keys(st, [(0, 35, "const")])
    haze, _ = fog_box("DRDust", (0, 3, 1.6), (9.8, 5.8, 3.1), 0.018, (0.92, 0.88, 0.8), 0.45)
    a43, b43 = T[43]
    a44, b44 = T[44]
    a45, b45 = T[45]
    a46, b46 = T[46]
    a47, b47 = T[47]
    a48, b48 = T[48]
    MA = cast.mamta("home")
    S0 = -math.pi / 2
    MA.at(a43, -0.3, 6.6, S0).walk(a43 + 3.6, MID.x, MID.y, mode="smooth").stay(b43, S0 + 0.3)
    # 44: a slow full turn to her left; the camera arcs the other way
    MA.stay(a44 + 0.2, S0 + 0.3)
    for k in range(1, 7):
        MA.stay(a44 + 0.2 + k * 0.95, S0 + 0.3 + math.radians(50) * k, tt=0.95)
    MA.stay(b47, S0 + 0.3 + math.radians(300), tt=0.9)
    MA.stay(a48 + 1.4).walk(b48, -0.3, 6.4, mode="smooth")
    MA.act(a43, a48 + 1.0, armR=("loc", 0.06, -0.28, 0.42), mood=(-0.5, -0.3, 0.0))
    MA.act(a44, b44, hp=-0.08, look=lambda t, u: est(MA, t) + fvec(MA.pos_yaw(t)[2] + 0.35) * 3 + Vector((0, 0, 0.3)), mood=(-0.6, -0.3, 0.05))
    MA.act(a47, b47, mood=lambda t, u: (lerp(-0.4, -1.0, seg(t, a47, b47 - 1.2)), -0.5, 0.0), eyes=lambda t, u: 1.0 if t < b47 - 0.7 else 0.4,
           look=Vector((4.5, 1.0, 1.0)))
    MA.act(a48, b48, look=Vector((0.0, 7.0, 1.4)), mood=(-0.7, -0.5, 0.0))
    S.on(MA, [43, 44, 47, 48])
    case, bag = carry(S, MA, a43, a48 + 1.0)
    bake_fn(case, a48 + 1.0, b48, lambda t: (Vector((MID.x + 0.3, MID.y - 0.15, 0.0)), Quaternion((0, 1, 0), math.pi / 2)))
    bake_fn(bag, a48 + 1.0, b48, lambda t: (Vector((MID.x - 0.1, MID.y - 0.35, 0.12)), Quaternion((0, 1, 0), 1.2)))

    # cameras
    S.shoot(43, lambda t: dict(pos=Vector((-4.55, 5.55, 2.35)), look=Vector((1.6, 1.7, 0.75)), focus=5.0, fstop=5.6))

    def c44(t):                                    # arc: 260 deg clockwise round her at MCU distance
        u = seg(t, a44, b44)
        c = head(MA, t) + Vector((0, 0, -0.07))
        ang = math.radians(-60 - 260 * u)
        d = dist_for("MCU", 35)
        pos = c + Vector((math.cos(ang), math.sin(ang), 0)) * d + Vector((0, 0, -0.02))
        return dict(pos=pos, look=c, focus=d, fstop=2.8)
    S.shoot(44, c44)

    def c45(t):                                    # slide along the framed photos above the sofa
        u = seg(t, a45, b45)
        y = lerp(1.05, 3.1, u)
        return dict(pos=Vector((4.22, y, 1.78)), look=Vector((4.9, y + 0.25, 1.8)), focus=0.72, fstop=2.8)
    S.shoot(45, c45)

    def c46(t):
        u = seg(t, a46, b46)
        return push(dict(pos=Vector((2.35, 1.85, 0.95)), look=Vector((4.3, 2.6, 0.42)), focus=2.2, fstop=2.8), 0.3 * u)
    S.shoot(46, c46)
    S.shoot(47, lambda t: on(MA, t, "CU", 85, yaw=MA.pos_yaw(a47)[2], az=10, tt=a47))
    S.shoot(48, lambda t: dict(pos=Vector((1.3, 0.55, 1.45)), look=Vector((0.0, 4.2, 1.1)), focus=2.8, fstop=4.0))
    S.light(43, (MID.x, MID.y, 1.0), key=dict(side="R", ang=60, el=30, d=4, w=60, k=5600, size=2))
    S.light(44, lambda t: head(MA, t), key=dict(side="R", ang=45, el=20, d=1.8, w=40, k=5600, size=1.2))
    S.light(45, (4.88, 2.1, 1.8), key=dict(side="R", ang=60, el=20, d=1.5, w=45, k=5600, size=1.0), fill=dict(side="L", ang=30, el=10, d=1.5, w=10, k=3000))
    S.light(46, (4.3, 2.55, 0.45), key=dict(side="R", ang=80, el=15, d=2, w=70, k=5600, size=1.2), fill=dict(side="L", ang=30, el=20, d=2, w=12, k=3000))
    S.light(47, lambda t: head(MA, t), key=dict(side="R", ang=80, el=15, d=1.8, w=50, k=5600, size=1.0),
            kick=dict(side="L", ang=20, el=5, d=1.5, w=2, k=3000))
    S.light(48, (MID.x, MID.y + 1, 1.2), key=dict(side="R", ang=60, el=30, d=3, w=40, k=5600, size=2))
