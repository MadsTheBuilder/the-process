# Scene 20 - THE OMEN - INT. House (Drawing Room / corridor) - Night (shots 147-149, 12 s)
# She tears the medical files out of the cabinet (the cabinet planted in 118) and runs into Mother's room.
# The camera holds the empty doorway; the young Mother steps out and stands there, still, in an impossible light.
import math

from mathutils import Vector

from kit import *
from film import *
import cast
import hs
import props
import sets
from sets import H


def build(S):
    T = S.T
    a = {n: T[n][0] for n in T}
    b = {n: T[n][1] for n in T}
    st = hs.house(S)
    C = sets.mats()
    S.state(0, Lamp=(50, 3200), TubeCorr=(10, 7000), WinMo=(40, 7000), MoBounce=(25, 6500))
    S.emit(0, C["bulb2"], 6.0)
    S.world(0, (0.02, 0.03, 0.05), 0.02)
    S.exposure(0, 1.4)
    MA = cast.mamta("night")
    CAB = H["cabinet"]
    MD = H["mo_door"]
    MA.at(0, CAB.x - 0.1, CAB.y - 0.62, math.pi / 2).stay(b[147] - 0.4).walk(a[148] + 1.4, 0.5, 6.7, gait="run").walk(a[148] + 2.4, MD.x, MD.y + 0.6, gait="run")
    MA.act(0, b[147], armL=lambda t, u: Vector((CAB.x - 0.3 + 0.2 * math.sin(t * 9), CAB.y - 0.1, 0.6 + 0.1 * math.sin(t * 7))),
           armR=lambda t, u: Vector((CAB.x + 0.2 + 0.15 * math.sin(t * 8 + 1), CAB.y - 0.1, 0.55)), lean=0.5, crouch=0.18,
           look=Vector((CAB.x, CAB.y, 0.55)), mood=(-0.9, -0.7, 0.3))
    MA.act(b[147] - 0.5, b[148], armR=("rel", 0.2, 0.0, -0.1), mood=(-0.9, -0.7, 0.2))
    S.on(MA, [147, 148])
    fol = props.folder()
    hold(fol, MA, "R", b[147] - 0.8, b[148], off=(0, 0, 0.02))
    vis(fol, [(b[147] - 0.8, b[148])])
    YMO = cast.mother(young=True)
    YMO.at(a[149], MD.x, MD.y + 0.7, -math.pi / 2).walk(a[149] + 1.6, MD.x, MD.y - 0.15, mode="smooth").stay(b[149])
    YMO.act(a[149], b[149], mood=(0.0, 0.0, 0.0), look=Vector((0.2, 6.25, 1.6)), eyes=0.9)
    S.on(YMO, [149])
    ghost = lamp("GhostLight", "AREA", (MD.x, MD.y + 1.6, 1.4), 0, kelvin(5600), size=1.2, shadow=False)
    ghost.rotation_euler = (math.radians(-90), 0, 0)
    S.state(0, GhostLight=0)
    S.state(a[149], GhostLight=(180, 5600), WinMo=(120, 6500))
    S.shoot(147, lambda t: dict(pos=Vector((CAB.x - 1.4, CAB.y - 2.0, 1.45)), look=Vector((CAB.x, CAB.y - 0.3, 0.75)), focus=2.3, fstop=2.8))
    DOORCAM = dict(pos=Vector((0.2, 6.25, 1.6)), look=Vector((MD.x, MD.y, 1.2)), focus=2.6, fstop=4.0)
    S.shoot(148, lambda t: DOORCAM)
    S.shoot(149, lambda t: DOORCAM)
    S.light(147, (CAB.x, CAB.y - 0.4, 0.8), key=dict(side="R", ang=50, el=35, d=1.5, w=40, k=3200, size=0.15))
    S.light(148, (MD.x, MD.y, 1.3), key=dict(side="R", ang=170, el=10, d=2, w=0))
    S.light(149, lambda t: head(YMO, t), key=dict(side="R", ang=20, el=10, d=1.5, w=15, k=5600, size=1.0))
