# Scene 19 - THE FIGHT - INT. House (Drawing Room) - Late Evening (shots 131-146, 68 s)
# One hard green-cool tubelight on the north wall, one dim warm table lamp by Papa's sofa. She speaks from the
# main doorframe on her way out; he answers from the sofa. Two islands of light and the dark gulf between them.
import math

from mathutils import Quaternion, Vector

from kit import *
from film import *
import cast
import hs
import props
import sets
from sets import H

DOOR_IN = Vector((0.05, 0.95))


def dr_tube(S, st, t):
    C = sets.mats()
    S.state(t, TubeDR=(320, 4300, (0.8, 1.0, 0.82)), Lamp=(70, 3200), WinDR1=(15, 8000), WinDR2=(15, 8000), TubeCorr=(14, 7000), WinMo=(30, 6500))
    S.emit(t, C["tube2"], 9.0)
    S.emit(t, C["bulb2"], 6.0)
    S.world(t, (0.03, 0.04, 0.07), 0.03)


def build(S):
    T = S.T
    a = {n: T[n][0] for n in T}
    b = {n: T[n][1] for n in T}
    E = S.END
    st = hs.house(S)
    dr_tube(S, st, 0)
    S.exposure(0, 1.35)
    hs.door_keys(st, [(0, 0, "const"), (a[132] - 0.6, 0, "bez"), (a[132] + 0.2, 88, "const")])
    MA = cast.mamta("night")
    PA = cast.papa()
    SOFA = H["sofa"]
    PSEAT = Vector((SOFA.x - 0.05, SOFA.y - 0.3))
    PSTAND = Vector((3.35, 2.15))
    TOP = math.atan2(PSEAT.y - DOOR_IN.y, PSEAT.x - DOOR_IN.x)        # her yaw toward him
    MA.at(0, -0.3, 6.3, -math.pi / 2).walk(b[131] - 0.4, 0.2, 1.4, mode="smooth").walk(a[132] + 1.6, DOOR_IN.x, DOOR_IN.y, mode="smooth")
    MA.stay(a[132] + 2.6, -math.pi / 2 + 0.3).stay(a[134] + 0.4, TOP, tt=0.5).stay(a[145] + 0.3, TOP).stay(a[145] + 0.9, math.pi / 2, tt=0.5)
    MA.walk(a[146] + 1.2, -0.2, 5.6, gait="run").walk(b[146], 1.8, 7.0, gait="run")
    PA.at(0, PSEAT.x, PSEAT.y, math.pi + 0.2).stay(a[141] + 0.5).walk(a[141] + 2.2, PSTAND.x, PSTAND.y, yaw=math.pi + 0.25, mode="smooth", gait="stand")
    PA.stay(a[145] + 0.3).stay(a[145] + 0.9, math.pi / 2 + 0.3, tt=0.5).walk(a[146] + 1.0, 0.9, 5.4, gait="run").walk(b[146], 2.4, 6.9, gait="run")
    # Mamta: wrapping the dupatta, then the exchange
    MA.act(0, b[131], armL=lambda t, u: (lambda j: j["sh_c"] - j["tl"] * 0.12 + j["tf"] * 0.1)(MA.J(t)),
           armR=lambda t, u: (lambda j: j["sh_c"] + j["tl"] * 0.15 + j["tf"] * 0.08 + Vector((0, 0, -0.1)))(MA.J(t)), mood=(-0.4, -0.2, 0.0))
    lines = [(a[132] + 0.6, b[132] - 0.3), (a[134] + 0.2, b[134] - 0.3), (a[136] + 0.2, b[136] - 0.2), (a[138] + 0.2, b[138] - 0.2),
             (a[140] + 0.4, b[140] - 1.2), (a[142] + 0.3, b[142] - 0.4), (a[144] + 0.3, b[144] - 0.5)]
    def ma_mouth(t, u):
        o = 0.0
        for t0, t1 in lines:
            o = max(o, talk(t0, t1, amt=0.38 if t > a[142] else 0.3)(t, u)[2])
        brow = -0.5 if t < a[134] else (-0.9 if t > a[142] else -0.7)
        return (brow, -0.5 if t > a[134] else -0.1, o)
    MA.act(a[132], a[145], mood=ma_mouth, look=lambda t, u: est(PA, t) if t > a[132] + 2.5 else None,
           lean=lambda t, u: 0.1 * seg(t, a[144], a[144] + 4), shake=lambda t, u: 0.5 if t > a[144] + 5 else 0.0)
    MA.act(a[144] + 6.0, a[145], armR=lambda t, u: ("rel", 0.3, -0.1, -0.05 + 0.1 * math.sin(t * 3)))
    MA.act(a[145], b[146], look=Vector((0.5, 8.0, 1.6)), mood=(-0.6, -0.9, 0.3))
    # Papa: papers on the sofa, then up into the tube's hard top light
    plines = [(a[133] + 0.3, b[133] - 0.4), (a[135] + 0.2, b[135] - 0.2), (a[137] + 0.2, b[137] - 0.2), (a[139] + 0.2, b[139] - 0.2),
              (a[141] + 1.2, b[141] - 0.4), (a[143] + 0.3, b[143] - 0.4)]
    def pa_mouth(t, u):
        o = 0.0
        for t0, t1 in plines:
            o = max(o, talk(t0, t1, amt=0.3)(t, u)[2])
        return (-0.4 if t < a[139] else -0.8, -0.2, o)
    PA.act(0, a[141] + 0.9, sit=1.0, seat=0.44, _hold0=True)
    PA.act(0, b[133], hp=0.5, look=Vector((3.3, 2.4, 0.46)), armR=lambda t, u: Vector((3.4, 2.3 + 0.2 * math.sin(t * 0.9), 0.5)),
           armL=lambda t, u: Vector((3.35, 2.6, 0.48)))
    PA.act(a[134], a[145], mood=pa_mouth, look=lambda t, u: est(MA, t), lean=lambda t, u: 0.18 if a[139] < t < b[139] else 0.0)
    PA.act(a[145], b[146], look=Vector((0.5, 8.0, 1.6)), mood=(-0.6, -0.9, 0.3))
    S.on(MA, list(range(131, 147)))
    S.on(PA, list(range(131, 147)))
    for k in range(5):
        pp = new_obj("paper", box_mesh("pp", 0.21, 0.297, 0.002), M((0.82, 0.8, 0.74), 0.9), loc=(3.0 + 0.12 * k, 2.2 + 0.15 * (k % 3), 0.452 + 0.002 * k))
        pp.rotation_euler.z = 0.3 * k
    # cameras
    S.shoot(131, lambda t: dict(pos=Vector((-3.4, 1.0, 1.55)), look=mid(est(MA, t), Vector((PSEAT.x, PSEAT.y, 1.3))) + Vector((0, 0, -0.35)), focus=4.0, fstop=4.0))
    S.shoot(132, lambda t: on(MA, b[132], "MS", 50, yaw=math.pi / 2, az=8, tt=b[132]))
    PY = math.pi + 0.2
    S.shoot(133, lambda t: on(PA, t, "MCU", 85, yaw=PY, az=-20, tt=a[133]))
    mcuM = lambda n: (lambda t: on(MA, t, "CU", 85, yaw=TOP, az=-8, third=-0.3, tt=a[n]))
    mcuP = lambda n: (lambda t: on(PA, t, "MCU", 85, yaw=math.pi + 0.2, az=10, third=0.3, tt=a[n]))
    for n in (134, 136, 138, 142):
        S.shoot(n, mcuM(n))
    for n in (135, 137, 139, 143):
        S.shoot(n, mcuP(n))
    S.shoot(140, lambda t: dict(pos=Vector((-4.5, 3.3, 1.6)), look=Vector((2.0, 1.6, 1.0)), focus=5.0, fstop=4.0))
    S.shoot(141, lambda t: on(PA, b[141], "MCU", 85, yaw=math.pi + 0.25, az=12, el=-8, tt=b[141]))
    S.shoot(144, lambda t: push(on(MA, t, "CU", 85, yaw=TOP, az=-8, third=-0.2, tt=a[144]), 0.25 * seg(t, a[144], b[144])))
    S.shoot(145, lambda t: dict(pos=Vector((-1.6, 0.9, 1.5)), look=Vector((1.8, 1.4, 1.35)), focus=3.5, fstop=4.0))
    S.shoot(146, lambda t: dict(pos=Vector((6.8, 6.85, 1.5)), look=Vector((0.5, 6.7, 1.3)), focus=4.0, fstop=2.8))
    # lights: Mamta in the cold tube key (hard top-side), Papa in the warm lamp (underlight), ratios per the sheet
    G = (0.8, 1.0, 0.82)
    S.light(131, lambda t: head(MA, t), key=dict(side="L", ang=30, el=60, d=2.5, w=60, k=4300, tint=G, size=0.3))
    S.light(132, lambda t: head(MA, t), rim=dict(side="L", ang=160, el=40, d=1.6, w=30, k=4300, tint=G), key=dict(side="R", ang=60, el=55, d=2, w=25, k=4300, tint=G))
    S.light(133, lambda t: head(PA, t), key=dict(side="L", ang=40, el=-20, d=1.2, w=30, k=3200, size=0.4), fill=dict(side="R", ang=20, el=70, d=1.5, w=12, k=4300, tint=G))
    for n in (134, 136, 138):
        S.light(n, lambda t: head(MA, t), key=dict(side="L", ang=45, el=60, d=1.4, w=60, k=4300, tint=G, size=0.2), fill=dict(side="R", ang=40, el=10, d=1.5, w=5, k=4300))
    for n in (135, 137):
        S.light(n, lambda t: head(PA, t), key=dict(side="L", ang=40, el=-15, d=1.2, w=35, k=3200, size=0.4), fill=dict(side="R", ang=40, el=10, d=1.5, w=6, k=3200))
    S.light(139, lambda t: head(PA, t), key=dict(side="R", ang=30, el=60, d=1.4, w=50, k=4300, tint=G, size=0.2), fill=dict(side="L", ang=40, el=-15, d=1.2, w=20, k=3200))
    S.light(140, (1.5, 2.0, 1.2), key=dict(side="L", ang=30, el=60, d=4, w=60, k=4300, tint=G, size=0.5))
    S.light(141, lambda t: head(PA, t), key=dict(side="L", ang=10, el=75, d=1.3, w=70, k=4300, tint=G, size=0.2))
    S.light(142, lambda t: head(MA, t), key=dict(side="L", ang=60, el=60, d=1.3, w=70, k=4300, tint=G, size=0.15))
    S.light(143, lambda t: head(PA, t), key=dict(side="L", ang=20, el=65, d=1.3, w=55, k=4300, tint=G, size=0.2), rim=dict(side="R", ang=150, el=0, d=1.2, w=15, k=3200))
    S.light(144, lambda t: head(MA, t), key=dict(side="L", ang=25, el=40, d=1.3, w=70, k=4300, tint=G, size=0.3), kick=dict(side="R", ang=20, el=5, d=1.0, w=3, k=4300))
    S.light(145, lambda t: mid(head(MA, t), head(PA, t)), key=dict(side="L", ang=40, el=60, d=3, w=90, k=4300, tint=G, size=0.4))
    S.light(146, (1.0, 6.8, 1.4), key=dict(side="R", ang=150, el=20, d=3, w=80, k=6000, size=1.0), fill=dict(side="L", ang=30, el=20, d=3, w=20, k=6000))
