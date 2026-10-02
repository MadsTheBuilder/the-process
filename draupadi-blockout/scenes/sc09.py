# Scene 9 - DISTANCE - INT. House (Drawing Room/Corridor) - Day (shots 59-60, 8 s)
# From the dark corridor, across the drawing room on a long lens: Papa in a window pool, wiping tears.
# Mamta, soft in the foreground, does not cross the light between them. She turns to her room instead.
import math

from mathutils import Vector

from kit import *
from film import *
import cast
import hs
import sets
from scenes.sc07 import dr_day


def build(S):
    T = S.T
    st = hs.house(S)
    dr_day(S, st, 0, lamp_w=25)
    S.state(0, WinDR1=(260, 5600), WinDR2=(90, 5600), WinCorr=(12, 6000))
    S.exposure(0, 0.2)
    haze, _ = fog_box("DRDust", (0, 3, 1.6), (9.8, 5.8, 3.1), 0.018, (0.92, 0.88, 0.8), 0.45)
    a59, b59 = T[59]
    a60, b60 = T[60]
    PA = cast.papa()
    MA = cast.mamta("home")
    PP = Vector((-2.95, 1.05))
    PA.at(0, PP.x, PP.y, math.radians(-75)).stay(S.END)
    PA.act(0, S.END, armR=lambda t, u: (lambda j: j["head_c"] + j["hf"] * 0.07 + j["tl"] * -0.03 + Vector((0, 0, 0.0)))(PA.J(t))
           if (t % 3.0) < 1.6 else ("rel", 0.1, -0.08, -0.25), hp=0.3, mood=(-0.9, -0.6, 0.05), shake=0.5)
    MA.at(0, -0.55, 6.6, -math.pi / 2 - 0.25).stay(a60 + 0.6).stay(a60 + 1.4, math.pi, tt=0.8).walk(b60 + 0.5, -2.0, 6.95, mode="smooth")
    MA.act(0, a60 + 0.6, look=lambda t, u: est(PA, t), mood=(-0.8, -0.5, 0.0))
    S.on(PA, [59], step=2)
    S.on(MA, [59, 60])
    S.shoot(59, lambda t: dict(pos=Vector((0.32, 7.5, 1.55)), look=Vector((PP.x + 0.15, PP.y, 1.3)), focus=6.9, fstop=2.8))
    S.shoot(60, lambda t: on(MA, a60 + 1.5, "MS", 35, yaw=math.pi, az=35, tt=a60 + 1.5))
    S.light(59, (PP.x, PP.y, 1.5), key=dict(side="L", ang=60, el=30, d=2, w=60, k=5600, size=1.2))
    S.light(60, lambda t: head(MA, t), key=dict(side="R", ang=100, el=20, d=2, w=10, k=6000))
