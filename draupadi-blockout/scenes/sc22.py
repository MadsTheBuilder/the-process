# Scene 22 - BREAKDOWN - INT. House (Mamta's Room) - Night (shots 162-164, 14 s)
# Only corridor spill and a cold window moonlight. She collapses, then in anger slams the almirah open (the tally
# marks in frame) and packs in jump cuts, weeping.
import math

from mathutils import Quaternion, Vector

from kit import *
from film import *
import cast
import hs
import props
import sets
from sets import H


def mamta_room_night(S, st, t, moon=1.2):
    C = sets.mats()
    sets.sun_dir(st["L"]["Moon"], 185, 20)
    S.state(t, Moon=(moon, 7500), TubeCorr=(35, 6500), WinM=(25, 8000))
    S.emit(t, C["tube"], 5.0)
    S.emit(t, C["sky_win"], 0.3)
    S.world(t, (0.02, 0.03, 0.06), 0.02)


def build(S):
    T = S.T
    a = {n: T[n][0] for n in T}
    b = {n: T[n][1] for n in T}
    st = hs.house(S)
    mamta_room_night(S, st, 0)
    S.exposure(0, 1.3)
    AX, AY = H["almirah"]
    hs.almirah_keys(st, left=[(0, 0, "const"), (a[163] + 0.8, 0, "bez"), (a[163] + 1.1, 110, "const")],
                    right=[(0, 0, "const"), (a[163] + 0.8, 0, "bez"), (a[163] + 1.15, 100, "const")])
    MA = cast.mamta("night")
    MA.at(0, -1.45, 7.7, math.pi / 2).walk(a[162] + 2.0, -2.6, 10.3, mode="smooth").stay(b[162], math.pi / 2 + 0.4)
    MA.at(a[163], -3.4, 11.4, math.pi / 2).walk(a[163] + 0.9, AX + 0.15, AY - 0.75, mode="smooth").stay(b[163])
    # jump cuts: three positions between the almirah and the suitcase on the bed
    js = [(-3.0, 12.5, 0.0), (-2.3, 12.4, 0.0), (-2.4, 12.1, 0.3)]
    for k, (x, y, yaw) in enumerate(js):
        t0 = a[164] + k * 2.0
        MA.at(t0, x, y, yaw).stay(t0 + 2.0)
    MA.act(a[162] + 1.6, b[162], fade=0.6, sit=1.0, seat=0.0, ffwd=0.4, lean=0.5, hp=0.6, shake=1.2, mood=(-1.0, -0.8, 0.3),
           armL=lambda t, u: (lambda j: j["head_c"] + j["hf"] * 0.1 + j["tl"] * 0.06)(MA.J(t)), armR=lambda t, u: (lambda j: j["head_c"] + j["hf"] * 0.1 - j["tl"] * 0.06)(MA.J(t)))
    MA.act(0, a[162] + 1.8, mood=(-1.0, -0.8, 0.4), shake=0.8, lean=0.15, armR=("rel", 0.2, -0.15, 0.0))
    MA.act(a[163] + 0.5, a[163] + 1.2, fade=0.15, armL=Vector((AX - 0.5, AY - 0.1, 1.2)), armR=Vector((AX + 0.5, AY - 0.1, 1.2)), mood=(-1.0, -0.9, 0.5))
    MA.act(a[163] + 1.2, b[163], look=Vector((AX - 0.55, AY - 0.4, 1.4)), mood=(-1.0, -0.8, 0.2), shake=0.6)
    for k in range(3):
        t0 = a[164] + k * 2.0
        tgt = Vector((-1.3, 12.5, 0.75)) if k % 2 == 0 else Vector((AX, AY + 0.1, 1.1))
        MA.act(t0, t0 + 2.0, fade=0.1, armL=tgt + Vector((0, 0.15, 0)), armR=tgt + Vector((0, -0.15, 0)), lean=0.35, look=tgt, mood=(-1.0, -0.9, 0.4), shake=0.9)
    S.on(MA, [162, 163, 164])
    tear(MA, a[162] + 2.0, 2.5, 0.5)
    tear(MA, a[164] + 0.5, 2.0, -0.5, name="tear2")
    case = props.suitcase()
    case.location = (-1.3, 12.45, 0.56)
    case.rotation_euler = (0, math.pi / 2, 0)
    vis_tree(case, [(a[164], b[164])])
    pile = new_obj("ClothesThrow", box_mesh("ct", 0.35, 0.3, 0.12), M((0.3, 0.22, 0.28), 0.95))
    bake_fn(pile, a[164], b[164], lambda t: ((MA.J(t)["hand"]["L"] + MA.J(t)["hand"]["R"]) / 2, None), 1, rot=False)
    vis(pile, [(a[164], b[164])])
    S.shoot(162, lambda t: dict(pos=Vector((-4.6, 9.0, 1.5)), look=est(MA, t) + Vector((0, 0, -0.55)), focus=2.5, fstop=2.8))
    S.shoot(163, lambda t: dict(pos=Vector((-2.4, 10.8, 1.5)), look=Vector((AX - 0.2, AY - 0.4, 1.2)), focus=3.0, fstop=4.0))
    jc = [Vector((-4.2, 10.4, 1.55)), Vector((-3.6, 10.0, 1.3)), Vector((-4.6, 11.2, 1.7))]
    S.shoot(164, lambda t: dict(pos=jc[min(2, int((t - a[164]) / 2.0))], look=est(MA, t) + Vector((0, 0, -0.4)), focus=2.4, fstop=2.8))
    S.light(162, lambda t: head(MA, t), key=dict(side="R", ang=100, el=25, d=2.0, w=60, k=7500, size=0.6))
    S.light(163, lambda t: head(MA, t), key=dict(side="L", ang=80, el=20, d=2.0, w=35, k=7500, size=0.1))
    S.light(164, lambda t: head(MA, t), key=dict(side="R", ang=100, el=20, d=2.0, w=25, k=6500, size=0.4))
    # the corridor spill flickers as she moves through it (164)
    for k in range(10):
        t = a[164] + k * 0.6
        S.state(t, TubeCorr=(35 if k % 2 == 0 else 12, 6500))
