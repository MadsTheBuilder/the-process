# Scene 12 - CORE MEMORY: THE SHEETS - EXT. Hospital backyard - Day (shots 76-84, 43 s)
# Rows of white sheets on lines (along x, lines at y 204 + 2.3k). Hard sun BEHIND the sheets (from the north),
# blown two stops, warm 4500K: the only bright memory. Dev's face stays hidden behind sheets, backs and blur.
import math
import random

import bpy
from mathutils import Quaternion, Vector

from kit import *
from film import *
import cast
import props
import sets
from sets import LINES_Y

LANES = [(LINES_Y[i] + LINES_Y[i + 1]) / 2 for i in range(len(LINES_Y) - 1)]    # walkable lanes between lines


def build(S):
    T = S.T
    E = S.END
    a = {n: T[n][0] for n in T}
    b = {n: T[n][1] for n in T}
    st = sets.build_yard(E)
    L = st["L"]
    sm = sets.sheet_mat()
    sm.use_transparent_shadow = True
    sets.sun_dir(L["Y_Sun"], 95, 34)
    sets.sun_dir(L["Y_Sky"], 260, 70)
    S.state(0, Y_Sun=(9.0, 4500), Y_Sky=(0.6, 6000), Y_Bounce=(500, 5000))
    S.world(0, (0.85, 0.8, 0.7), 0.45)
    S.emit(0, sm, 0.0)
    S.exposure(0, -0.95)
    # hero sheets (the ones touched in the story) replace the random sheets around them
    HERO = {"over_dev": None}
    def clear(x0, x1, y):
        for s_ in st["P"]["sheets"]:
            if abs(s_.location.y - y) < 0.01 and x0 < s_.location.x < x1:
                s_.hide_render = s_.hide_viewport = True
    X80, X82, X83 = 199.0, 207.0, 202.5
    clear(X83 - 1.6, X83 + 1.6, LINES_Y[3])
    hero83 = sets.sheet_obj("HeroSheet83", 1.7, 2.0, (X83, LINES_Y[3], 2.45), sm, 3.0)
    keys_vec(hero83, "location", [(0, hero83.location), (a[83] + 1.6, hero83.location), (a[83] + 2.6, hero83.location + Vector((1.15, 0, 0.0)))])
    YM = cast.young_mamta("dev")
    DV = cast.dev("coat")
    PM = cast.mamta("home", name="MamtaNow")
    lane = LANES
    # 76: they run through the rows (Dev chasing), crossing lines through the sheets
    YM.at(a[76], 191.5, lane[2] + 0.2, 0.0).walk(b[76], 199.4, lane[2] + 0.1, gait="run")
    DV.at(a[76], 189.2, lane[2] - 0.2, 0.0).walk(b[76], 198.4, lane[2] - 0.05, gait="run")
    # 77: he catches her arm and pulls her close
    P77 = Vector((200.2, lane[2]))
    YM.at(a[77], P77.x + 0.15, P77.y + 0.75, -math.pi / 2).walk(a[77] + 1.6, P77.x + 0.05, P77.y + 0.3, yaw=-math.pi / 2, mode="smooth", gait="stand").stay(b[78] - 2.2, -math.pi / 2)
    DV.at(a[77], P77.x, P77.y - 0.35, math.pi / 2).stay(b[78] - 2.0)
    YM.walk(b[78], P77.x + 3.4, P77.y + 0.2, yaw=0.0, gait="run")
    DV.stay(b[78], math.pi / 2)
    YM.act(a[76], b[76], mood=(0.3, 1.0, 0.45), look=lambda t, u: est(DV, t))
    DV.act(a[76], b[76], mood=(0.2, 1.0, 0.4), look=lambda t, u: est(YM, t))
    DV.act(a[77], a[77] + 2.2, armR=lambda t, u: YM.J(t)["wrist"]["L"] if False else est(YM, t) + Vector((-0.1, -0.15, -0.55)))
    YM.act(a[77], b[77], look=lambda t, u: est(DV, t), mood=(0.4, 0.9, 0.1), lean=lambda t, u: 0.15 * seg(t, a[77] + 0.5, a[77] + 2))
    DV.act(a[77], b[78], look=lambda t, u: est(YM, t), mood=(0.2, 0.8, 0.05), armL=lambda t, u: est(YM, t) + Vector((0.0, 0.18, -0.45)))
    # 78: she throws a sheet over his face, giggles and runs
    t_throw = a[78] + 1.0
    YM.act(a[78], t_throw + 0.6, armL=lambda t, u: est(DV, t) + Vector((0, 0, 0.1)), armR=lambda t, u: est(DV, t) + Vector((0, -0.2, 0.1)),
           mood=(0.3, 1.0, 0.5))
    YM.act(t_throw + 0.6, b[78], mood=(0.4, 1.0, 0.5), look=lambda t, u: est(DV, t))
    shroud = new_obj("Shroud", sphere_mesh("sh", 0.34, 14, 10, (0.9, 0.9, 1.6)), sm)
    bake_fn(shroud, t_throw, b[78], lambda t: (DV.J(t)["head_c"] + Vector((0, 0, -0.32 * seg(t, t_throw, t_throw + 0.5))), None), 1, rot=False)
    vis(shroud, [(t_throw, b[78])])
    DV.act(t_throw, b[78], armL=lambda t, u: (lambda j: j["head_c"] + j["tf"] * 0.15)(DV.J(t)), armR=("rel", 0.3, -0.1, 0.05))
    # 79: hide and seek - both cross lanes behind the sheets while the camera tracks along lane 0
    YM.at(a[79], 196.0, lane[2], -1.2).walk(a[79] + 2.4, 197.5, lane[1], gait="run").walk(a[79] + 3.2, 198.4, lane[1] + 0.1).stay(b[79], 0.5)
    DV.at(a[79], 193.0, lane[3], 0.0).walk(a[79] + 2.5, 195.8, lane[3]).walk(b[79], 198.2, lane[2], gait="walk")
    YM.act(a[79], b[79], mood=(0.4, 1.0, 0.3), look=lambda t, u: est(DV, t))
    DV.act(a[79], b[79], look=lambda t, u: est(YM, t) + Vector((2 * math.sin(t), 0, 0)))
    # 80: Dev's silhouette behind a sheet, searching
    DV.at(a[80], X80, lane[2] + 0.35, -math.pi / 2).stay(a[80] + 1.0).stay(a[80] + 2.2, -math.pi / 2 + 0.7, tt=0.8).stay(b[80], -math.pi / 2 - 0.5, tt=1.2)
    DV.act(a[80], b[80], hy=lambda t, u: 0.5 * math.sin(t * 1.4))
    # 81-82: they find each other, hold close, lean in; the kiss behind a fluttering sheet
    C81 = Vector((X82, lane[3]))
    YM.at(a[81], C81.x, C81.y + 0.3, -math.pi / 2).stay(b[81])
    DV.at(a[81], C81.x, C81.y - 0.3, math.pi / 2).stay(b[81])
    YM.at(a[82], C81.x + 0.3, C81.y, math.pi).stay(b[82])
    DV.at(a[82], C81.x - 0.3, C81.y, 0.0).stay(b[82])
    YM.act(a[81], b[82], look=lambda t, u: est(DV, t) + Vector((0, 0, -0.03)), mood=(0.3, 0.7, 0.0), armL=lambda t, u: est(DV, t) + Vector((0.12, 0.12, -0.35)),
           armR=lambda t, u: est(DV, t) + Vector((0.12, -0.12, -0.35)), lean=lambda t, u: 0.1 + 0.14 * seg(t, a[81] + 1, b[82] - 3),
           eyes=lambda t, u: 1.0 if t < a[82] + 1.5 else 0.15)
    DV.act(a[81], b[82], look=lambda t, u: est(YM, t) + Vector((0, 0, 0.05)), mood=(0.2, 0.7, 0.0), armL=lambda t, u: est(YM, t) + Vector((-0.1, -0.15, -0.45)),
           armR=lambda t, u: est(YM, t) + Vector((-0.1, 0.15, -0.45)), lean=lambda t, u: 0.1 + 0.16 * seg(t, a[81] + 1, b[82] - 3), hp=0.12)
    S.on(YM, [76, 77, 78, 79, 81, 82])
    S.on(DV, [76, 77, 78, 79, 80, 81, 82])
    # 83: present Mamta inside the memory pulls the sheet aside - no one there (84)
    PM.at(a[83], X83 - 0.35, lane[2] + 0.2, math.pi / 2).stay(b[84])
    PM.act(a[83], b[84], mood=lambda t, u: (0.2, lerp(0.8, -0.4, seg(t, a[83] + 2.6, b[83])), 0.0), look=Vector((X83, LINES_Y[3] + 2, 1.5)),
           armR=lambda t, u: Vector((X83 - 0.45 + 1.15 * seg(t, a[83] + 1.6, a[83] + 2.6), LINES_Y[3] - 0.05, 1.55)) if t < a[83] + 2.8 else None)
    S.on(PM, [83, 84])

    # cameras
    def c76(t):                                    # steadicam running alongside one lane behind
        u = seg(t, a[76], b[76])
        pos = Vector((lerp(187.0, 195.6, u), lane[2] + 0.35, 1.35))
        tgt = mid(est(YM, t), est(DV, t))
        return dict(pos=pos, look=tgt + Vector((0, 0, -0.3)), focus=(tgt - pos).length, fstop=2.8)
    S.shoot(76, c76)
    S.shoot(77, lambda t: dict(pos=Vector((P77.x + 3.4, P77.y + 0.1, 1.45)), look=mid(est(YM, t), est(DV, t)) + Vector((0, 0, -0.3)), focus=3.4, fstop=2.8))
    S.shoot(78, lambda t: dict(pos=Vector((P77.x + 1.95, P77.y + 0.25, 1.5)), look=est(YM, t) + Vector((0, -0.15, -0.1)), focus=1.95, fstop=2.8))

    def c79(t):                                    # tracking along lane 0, looking north across the rows
        u = seg(t, a[79], b[79])
        pos = Vector((lerp(193.5, 199.0, u), lane[0], 1.45))
        return dict(pos=pos, look=pos + Vector((0.9, 3.5, -0.05)), focus=4.0, fstop=4.0)
    S.shoot(79, c79)
    S.shoot(80, lambda t: dict(pos=Vector((X80 + 0.2, lane[1] + 0.5, 1.55)), look=Vector((X80, lane[2] + 0.35, 1.5)), focus=2.75, fstop=2.0))

    def c81(t):
        u = seg(t, a[81], b[81])
        c = dict(pos=Vector((C81.x + 2.9, C81.y + 0.05, 1.55)), look=Vector((C81.x, C81.y, 1.5)), focus=2.9, fstop=2.0)
        return push(c, 0.22 * u)
    S.shoot(81, c81)
    S.shoot(82, lambda t: dict(pos=Vector((C81.x, C81.y - 2.0, 1.55)), look=Vector((C81.x, C81.y, 1.55)), focus=2.0, fstop=2.0))
    S.shoot(83, lambda t: dict(pos=Vector((X83 + 2.6, lane[2] + 0.55, 1.55)), look=head(PM, t) + Vector((0, 0, -0.12)), focus=2.95, fstop=2.0))
    S.shoot(84, lambda t: dict(pos=eyes(PM, a[84]) + Vector((0.05, 0, 0)), look=Vector((X83 + 0.3, LINES_Y[3] + 4, 1.4)), focus=3.0, fstop=2.8))
    # lights: big white bounce for faces, sun as rim; 83-84 the bounce is pulled and it goes cooler
    S.light(76, lambda t: mid(head(YM, t), head(DV, t)), fill=dict(side="L", ang=20, el=10, d=3, w=80, k=4800, size=3))
    S.light(77, lambda t: mid(head(YM, t), head(DV, t)), fill=dict(side="R", ang=25, el=10, d=2.5, w=120, k=4800, size=3))
    S.light(78, lambda t: head(YM, t), fill=dict(side="R", ang=25, el=10, d=2.5, w=100, k=4800, size=3))
    S.light(81, lambda t: mid(head(YM, t), head(DV, t)), fill=dict(side="L", ang=20, el=10, d=2.2, w=120, k=4800, size=3))
    S.light(83, lambda t: head(PM, t), fill=dict(side="L", ang=30, el=10, d=2.2, w=15, k=6200, size=2))
    S.state(a[83], Y_Bounce=(120, 6000), Y_Sun=(7.0, 5000))
    S.state(a[84], Y_Sun=(4.0, 5600), Y_Bounce=(60, 6000))
    S.emit(a[76], sm, 0.35)
    S.emit(a[84], sm, 0.0)
