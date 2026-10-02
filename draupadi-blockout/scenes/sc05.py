# Scene 5 - THE SCRAPING - INT. House (Corridor) - Day (shots 34-37, 15 s)
# She comes through the drawing room into the corridor (y 6.8) heading west. The internal barred window at
# x -5.3..-3.7 (north wall) looks into her old room. Low key, green-grey: the house holds its breath.
import math

from mathutils import Matrix, Quaternion, Vector

from kit import *
from film import *
import cast
import hs
import props
import sets
from sets import H

WIN_X = -4.4
BAR_Y = 7.6


def corridor_day(S, st, t):
    C = sets.mats()
    S.state(t, WinCorr=(110, 6000), WinDR1=(45, 6000), WinDR2=(45, 6000), WinM=(70, 6000), WinMo=(40, 6000), DoorDay=(25, 6200))
    S.emit(t, C["sky_win"], 3.5)
    S.world(t, (0.4, 0.45, 0.42), 0.04)


def carry(S, MA, t0, t1, bags=None):
    """suitcase in the right hand, duffel on the left shoulder."""
    case, bag = bags or (props.suitcase(), props.duffel())
    bake_fn(case, t0, t1, lambda t: (MA.J(t)["hand"]["R"] + Vector((0, 0, -0.64)),
                                      Quaternion((0, 0, 1), MA.J(t)["yaw"] + math.pi / 2)), 2)
    bake_fn(bag, t0, t1, lambda t: (MA.J(t)["sh_c"] + MA.J(t)["tl"] * (MA.sw * 1.15) - MA.J(t)["spine"] * 0.32,
                                     basis_quat(MA.J(t)["tf"], MA.J(t)["spine"])), 2)
    return case, bag


def build(S):
    T = S.T
    E = S.END
    st = hs.house(S)
    corridor_day(S, st, 0)
    S.exposure(0, 0.35)
    hs.door_keys(st, [(0, 35, "const")])
    a34, b34 = T[34]
    a35, b35 = T[35]
    a36, b36 = T[36]
    a37, b37 = T[37]
    W = math.pi
    MA = cast.mamta("home")
    MA.at(a34, 0.3, 3.6, math.pi / 2).walk(a34 + 2.4, -0.25, 6.6, mode="lin").walk(b34, -3.0, 6.75, yaw=W)
    MA.walk(a35 + 0.8, -3.45, 6.78, yaw=W, mode="smooth").stay(b35, W)
    MA.walk(a36 + 1.6, WIN_X + 0.05, 7.22, yaw=math.pi / 2, mode="smooth").stay(b37, math.pi / 2)
    MA.act(a34, a36 + 1.0, armR=("loc", 0.06, -0.28, 0.42), mood=(-0.4, -0.2, 0.0))
    MA.act(a35 + 0.6, b35, look=Vector((WIN_X, 9.5, 1.5)), mood=(-0.6, -0.4, 0.05), hy=0.2)
    MA.act(a36 + 1.4, b37, armL=lambda t, u: Vector((WIN_X + 0.05, BAR_Y - 0.04, lerp(1.15, 1.42, seg(t, a36 + 1.6, a36 + 3.4)))),
           look=Vector((WIN_X - 0.1, 11.0, 1.4)), mood=(-0.7, -0.5, 0.08), lean=0.05)
    S.on(MA, [34, 35, 36])
    case, bag = carry(S, MA, a34, a36 + 1.0)
    bake_fn(case, a36 + 1.0, b37, lambda t: (Vector((WIN_X + 0.5, 7.0, 0.0)), Quaternion((0, 0, 1), 0.3)))
    bake_fn(bag, a36 + 1.0, b37, lambda t: (Vector((WIN_X + 0.6, 6.7, 0.15)), Quaternion((0, 1, 0), 1.3)))
    # 37: an insert hand closing around a rusted bar (the internal grille bars sit every ~0.145 m)
    hr, fing, th = props.hand("GripHand", sleeve=(0.22, 0.30, 0.18), skin=SKIN["a"])
    bar_x = -4.375
    hr.location = (bar_x + 0.1, BAR_Y - 0.035, 1.4)
    hr.rotation_euler = Matrix(((0, -1, 0), (0, 0, -1), (1, 0, 0))).to_euler()   # fingers west, palm facing the bar
    props.curl(fing, [(a37, 0.05), (a37 + 0.8, 0.05), (a37 + 2.2, 0.85)])
    vis_tree(hr, [(a37, b37)])
    # a hard spot inside her room throws bar shadows across her arm and chest (shots 36-37)
    bar = lamp("BarKey", "SPOT", (WIN_X - 0.6, 10.6, 2.1), 0, kelvin(5600), size=0.03, spot=28)
    aim(bar, (WIN_X, 7.1, 1.3))
    S.state(0, BarKey=0)
    S.state(a36, BarKey=(900, 5600))

    # cameras
    def c34(t):                                    # gimbal follow, behind her
        h = head(MA, t)
        j = MA.J(t)
        back = -fvec(j["yaw"])
        pos = h + back * 2.3 + Vector((0, 0, -0.15)) + lvec(j["yaw"]) * 0.25
        return dict(pos=pos, look=h + Vector((0, 0, -0.25)), focus=2.35)
    S.shoot(34, c34)
    S.shoot(35, lambda t: on(MA, t, "CU", 85, yaw=W, az=-8, tt=a35 + 0.3))
    S.shoot(36, lambda t: on(MA, b36, "MS", 50, yaw=math.pi / 2, az=-88, third=-0.3))
    S.shoot(37, lambda t: dict(pos=Vector((bar_x - 0.45, BAR_Y - 0.78, 1.52)), look=Vector((bar_x + 0.03, BAR_Y - 0.03, 1.4)), focus=0.92, fstop=5.6))
    S.light(34, lambda t: head(MA, t), key=dict(side="R", ang=80, el=20, d=3, w=45, k=6000, size=1.2), fill=dict(side="L", ang=150, el=30, d=3, w=20, k=6000))
    S.light(35, lambda t: head(MA, t), key=dict(side="R", ang=95, el=15, d=1.6, w=55, k=6000, size=0.6))
    S.light(36, lambda t: head(MA, t), fill=dict(side="L", ang=50, el=10, d=2, w=4, k=6000))
    S.light(37, (bar_x, BAR_Y, 1.4), kick=dict(side="L", ang=80, el=20, d=0.8, w=6, k=5600))
