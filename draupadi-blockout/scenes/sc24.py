# Scene 24 - THE LATHI - EXT. House (Stairs) - Night (shots 167-180, 63 s)
# The front steps at night: warm doorway light behind, cool moonlight from the sky, crickets. Jagdish sits two steps
# below Mamta (the old order). The earthen gamla with its struggling plant: "the lathi, or the hands?"
import math

from mathutils import Quaternion, Vector

from kit import *
from film import *
import cast
import hs
import props
import sets
from sets import STEP_R, STEP_T, step_z

S_ = -math.pi / 2


def step_top(k):
    return -STEP_R * (k + 1)


def step_y(k):
    return -1.45 - STEP_T * k - STEP_T / 2


GAMLA = Vector((1.85, -2.6, -0.62))


def build(S):
    T = S.T
    a = {n: T[n][0] for n in T}
    b = {n: T[n][1] for n in T}
    E = S.END
    st = hs.house(S)
    C = sets.mats()
    hs.hide_plates(st)
    sets.sun_dir(st["L"]["Moon"], -60, 35)
    S.state(0, Moon=(0.25, 7000), Porch=(170, 3200), DRBulb=(260, 3000), Lamp=(60, 3000))
    S.emit(0, C["porch"], 22.0)
    S.emit(0, C["bulb2"], 6.0)
    S.world(0, (0.03, 0.05, 0.12), 0.12)
    S.exposure(0, 0.55)
    hs.door_keys(st, [(0, 22, "const"), (a[180] + 0.3, 22, "bez"), (a[180] + 1.0, 85, "const")])
    S.state(a[180] + 0.4, DRBulb=(420, 3000))
    MA = cast.mamta("night")
    JG = cast.jagdish()
    PA = cast.papa()
    DOC = cast.doctor()
    MP = Vector((-0.38, step_y(0) + 0.05))
    JP = Vector((0.42, step_y(2) + 0.05))
    MA.at(0, MP.x, MP.y, S_).stay(a[180] + 2.6).walk(a[180] + 3.4, -0.75, MP.y - 0.1, gait="stand").stay(a[180] + 5.0)
    MA.walk(b[180], -0.2, 0.6, mode="smooth")
    JG.at(0, JP.x, JP.y, S_).stay(a[180] + 2.6).walk(a[180] + 3.4, 0.95, JP.y, gait="stand").stay(b[180])
    seat_M = dict(sit=1.0, seat=0.0, footz=step_top(2) - step_top(0), ffwd=0.62)
    seat_J = dict(sit=1.0, seat=0.0, footz=step_top(4) - step_top(2), ffwd=0.62)
    MA.act(0, a[180] + 2.3, z=step_top(0), _hold0=True, **seat_M)
    JG.act(0, a[180] + 2.3, z=step_top(2), _hold0=True, **seat_J)
    MA.act(a[180] + 2.2, E, z=hs.on_stairs(MA))
    JG.act(a[180] + 2.2, E, z=hs.on_stairs(JG))
    # the conversation: who looks where, who speaks
    lines_M = {168: (0.3, 2.6), 170: (0.3, 2.6), 172: (0.6, 4.6), 174: (0.2, 1.6), 177: (0.8, 2.6)}
    lines_J = {169: (0.4, 4.6), 173: (0.3, 3.6), 175: (0.4, 6.6), 176: (0.0, 3.6), 178: (0.5, 5.6)}

    def mouth(lines, base):
        def f(t, u):
            o = 0.0
            for n, (s0, s1) in lines.items():
                o = max(o, talk(a[n] + s0, a[n] + s1)(t, u)[2])
            return (base[0](t), base[1](t), o)
        return f
    m_brow = lambda t: -0.6 if t < a[177] else -0.2
    m_smile = lambda t: 0.6 if a[177] < t < b[177] else (-0.4 if t < a[177] else 0.0)
    MA.act(0, a[180], mood=mouth(lines_M, (m_brow, m_smile)), armL=("rel", 0.2, 0.0, -0.32), armR=("rel", 0.2, 0.0, -0.32),
           look=lambda t, u: est(JG, t) + Vector((0, 0, -0.45)) if (a[172] < t < b[173] or t > a[177]) else Vector((0.0, -12.0, 0.6)),
           hp=lambda t, u: 0.12 if t > a[179] else 0.0)
    j_smile = lambda t: 0.55 if a[171] < t < b[171] or t > a[178] else 0.1
    JG.act(0, a[180], mood=mouth(lines_J, (lambda t: -0.2, j_smile)), armL=("rel", 0.2, 0.0, -0.3),
           look=lambda t, u: (Vector((6.0, -6.0, 0.0)) if t < a[171] else est(MA, t) + Vector((0, 0, -0.35))) if not (a[175] + 2.4 < t < b[176]) else GAMLA)
    JG.act(a[175] + 2.0, b[176] + 0.2, armR=lambda t, u: GAMLA + Vector((-0.45, 0.1, 0.45)), twist=-0.35)
    MA.act(a[179], b[179], hp=0.25, look=Vector((0.0, -10.0, 0.0)), mood=(-0.7, -0.3, 0.0), eyes=0.7)
    # 180: the door opens; Papa and the doctor come out; the doctor goes down between them
    PA.at(a[180] + 0.6, 0.15, 0.9, S_).walk(a[180] + 1.8, 0.15, -0.6, mode="smooth").stay(a[180] + 3.6).stay(a[180] + 4.2, math.pi / 2, tt=0.5)
    PA.walk(b[180], 0.1, 1.4, mode="smooth")
    DOC.at(a[180] + 0.6, -0.2, 1.1, S_).walk(a[180] + 2.0, -0.1, -0.7, mode="smooth").walk(b[180], 0.15, -6.5)
    DOC.act(a[180], b[180], z=hs.on_stairs(DOC), armR=("rel", 0.15, -0.15, -0.28))
    PA.act(a[180], b[180], mood=(-0.9, -0.6, 0.0), hp=0.2)
    MA.act(a[180] + 2.2, b[180], look=lambda t, u: est(PA, t))
    JG.act(a[180] + 2.2, b[180], look=lambda t, u: est(DOC, t))
    S.on(MA, list(range(167, 181)))
    S.on(JG, list(range(167, 181)))
    S.on(PA, [180])
    S.on(DOC, [180])
    bag = new_obj("DocBag", box_mesh("db", 0.38, 0.16, 0.24), M((0.08, 0.05, 0.03), 0.6))
    bake_fn(bag, a[180], b[180], lambda t: (DOC.J(t)["hand"]["R"] + Vector((0, 0, -0.26)), Quaternion((0, 0, 1), DOC.J(t)["yaw"])), 2)

    # cameras
    WIDE = dict(pos=Vector((0.35, -9.3, -0.1)), look=Vector((0.0, -1.6, 0.05)), focus=7.6, fstop=4.0)
    S.shoot(167, lambda t: WIDE)
    S.shoot(180, lambda t: WIDE)
    S.shoot(168, lambda t: on(MA, t, "MCU", 85, yaw=S_, az=-18, el=10, tt=a[168]))
    S.shoot(169, lambda t: on(JG, t, "MCU", 85, yaw=S_, az=22, el=-8, tt=a[169]))
    S.shoot(170, lambda t: on(MA, t, "CU", 85, yaw=S_, az=-18, el=10, tt=a[170]))
    S.shoot(171, lambda t: on(JG, t, "CU", 85, yaw=S_ + 0.6, az=10, el=-8, tt=a[171]))
    S.shoot(172, lambda t: on(MA, t, "MCU", 85, yaw=S_, az=-25, el=10, tt=a[172]))
    S.shoot(173, lambda t: on(JG, t, "MCU", 85, yaw=S_ + 0.6, az=10, el=-8, tt=a[173]))
    S.shoot(174, lambda t: on(MA, t, "CU", 85, yaw=S_, az=-25, el=10, tt=a[174]))
    TWO = lambda t: dict(pos=Vector((2.3, -5.6, 0.35)), look=mid(est(MA, t), est(JG, t)) + Vector((0, 0, -1.05)), focus=4.2, fstop=2.8)
    S.shoot(175, TWO)
    S.shoot(176, lambda t: dict(pos=GAMLA + Vector((-0.55, -0.75, 0.75)), look=GAMLA + Vector((0, 0, -0.05)), focus=1.15, fstop=2.8))
    S.shoot(177, lambda t: on(MA, t, "CU", 85, yaw=S_, az=-25, el=10, tt=a[177]))
    S.shoot(178, lambda t: push(on(JG, t, "MCU", 85, yaw=S_ + 0.6, az=10, tt=a[178]), 0.18 * seg(t, a[178], b[178])))
    S.shoot(179, TWO)
    # lights: warm door rim behind, soft moon fill in front; the first kind light at night
    rimM = dict(side="L", ang=160, el=30, d=1.6, w=45, k=3200, size=0.5)
    fillC = dict(side="R", ang=35, el=25, d=2.2, w=14, k=6500, size=1.5)
    for n in (168, 170, 172, 174, 177):
        S.light(n, lambda t: head(MA, t), rim=rimM, fill=fillC, key=dict(side="L", ang=70, el=15, d=1.8, w=10 if n < 177 else 20, k=3200, size=0.6))
    for n in (169, 171, 173, 178):
        S.light(n, lambda t: head(JG, t), key=dict(side="R", ang=30, el=20, d=1.8, w=35, k=3200, size=0.8), fill=dict(side="L", ang=40, el=20, d=2, w=10, k=6500))
    S.light(175, lambda t: mid(head(MA, t), head(JG, t)), rim=dict(side="L", ang=150, el=30, d=2, w=40, k=3200), fill=fillC)
    S.light(179, lambda t: mid(head(MA, t), head(JG, t)), rim=dict(side="L", ang=150, el=30, d=2, w=40, k=3200), fill=fillC)
    S.light(176, GAMLA, key=dict(side="L", ang=70, el=12, d=1.0, w=18, k=3000, size=0.3))
