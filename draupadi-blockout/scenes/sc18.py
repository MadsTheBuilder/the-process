# Scene 18 - CORE MEMORY: THE INTERVIEW - INT./EXT. House - Evening (shots 113-130, 73 s)
# She wakes to an empty bed and follows warm light into the drawing room of ten years ago (Shot 43's frame):
# her parents choosing a groom from photographs. Through the window, young Mamta and Dev walk home.
# She runs out, screams at them; they never hear her. The door; the voices; Dev thrown out; the lathi.
import math

import bpy
from mathutils import Quaternion, Vector

from kit import *
from film import *
import cast
import hs
import props
import sets
from sets import H, step_z
from scenes.sc08 import mother_in_bed

CH = H["mo_chair"]


def build(S):
    T = S.T
    a = {n: T[n][0] for n in T}
    b = {n: T[n][1] for n in T}
    E = S.END
    st = hs.house(S)
    C = sets.mats()
    L = st["L"]
    INSIDE0, INSIDE1 = a[116], b[120]        # the warm memory interior
    OUT0, OUT1 = a[121], b[128]              # dusk outside
    # --- 113-115: blue dusk in Mother's room, warm spill from the drawing room ahead
    S.world(0, (0.08, 0.1, 0.18), 0.05)
    S.state(0, WinMo=(70, 7500), DRBulb=(260, 3000), Lamp=(70, 3000), TubeCorr=(10, 7500), WinCorr=(25, 7500))
    S.emit(0, C["sky_win"], 0.6)
    S.emit(0, C["bulb2"], 8.0)
    S.exposure(0, 0.7)
    # --- 116-121: the drawing room as a warm memory; dusk outside the windows
    S.state(INSIDE0, DRBulb=(380, 3000), Lamp=(90, 2900), WinDR1=(50, 2400), WinDR2=(50, 2400))
    S.exposure(INSIDE0, 0.4)
    # --- 121-128: outside, blue dusk + a red-orange last light low in the west; the doorway glows warm
    sets.sun_dir(L["Sun"], 165, 3)
    sets.sun_dir(L["Sky"], 200, 70)
    S.state(OUT0, Sun=(4.0, 1900), Sky=(0.5, 9000), Porch=(0, 3000))
    S.world(OUT0, (0.12, 0.16, 0.32), 0.7)
    S.exposure(OUT0, 0.2)
    # --- 129-130: back to Mother's room, dark blue night
    S.state(a[129], Sun=0, Sky=0, DRBulb=0, Lamp=0, WinDR1=0, WinDR2=0, WinMo=(35, 8000), TubeCorr=0, WinCorr=(10, 8000))
    S.emit(a[129], C["bulb2"], 0.0)
    S.emit(a[129], C["sky_win"], 0.25)
    S.world(a[129], (0.05, 0.07, 0.14), 0.04)
    S.exposure(a[129], 0.9)
    hs.hide_plates(st, [(OUT0, OUT1)])
    for k in ("net0", "net1"):
        vis(st["P"][k], [(a[121], b[121])], inverse=True)
    hs.door_keys(st, [(0, 0, "const"), (a[122] + 0.3, 0, "bez"), (a[122] + 0.6, 85, "const"),
                      (a[124] + 2.6, 85, "bez"), (a[124] + 3.4, 4, "const"), (a[127] + 0.2, 4, "bez"), (a[127] + 0.45, 88, "const"), (b[128], 88, "const")])

    MA = cast.mamta("fresh")
    YM = cast.young_mamta("dev")
    DV = cast.dev("shirt")
    YP = cast.papa(young=True)
    YMO = cast.mother(young=True)
    MO = cast.mother()
    mother_in_bed(MO, a[129], E)
    MO.act(a[129], E, eyes=0.1)
    # ---------------------------------------------------------------- Mamta
    MA.at(0, CH.x, CH.y, 0.15).stay(a[115] + 0.3)
    MA.walk(a[115] + 1.4, 4.4, 10.0, gait="run").walk(a[115] + 2.4, 2.5, 7.9, gait="run").walk(a[115] + 3.4, 0.6, 6.8, gait="run").walk(b[115], -0.25, 6.6)
    MA.at(a[116], -0.3, 6.2, -math.pi / 2).stay(b[121])
    MA.at(a[122], 0.0, 0.2, -math.pi / 2).walk(a[122] + 1.0, 0.0, -1.3, gait="run").walk(b[122], 0.4, -3.9, gait="run")
    MA.walk(b[123], 0.9, -5.2, gait="run")
    MA.at(a[124], 0.75, -1.0, math.pi / 2).stay(b[126])
    MA.at(a[127], 1.25, -0.95, math.radians(150)).stay(b[128])
    MA.at(a[129], CH.x, CH.y, 0.15).stay(a[130] + 1.0).walk(b[130] + 0.5, 4.4, 10.0, mode="smooth")
    MA.act(0, a[113] + 0.01, fade=0, sit=1.0, seat=0.47, hp=0.4, eyes=0.1, _hold0=True)
    MA.act(a[113], b[114] + 0.4, sit=1.0, seat=0.47, eyes=lambda t, u: 0.45 if t < b[113] else 1.0, look=Vector((6.7, 13.2, 0.6)), _hold0=True)
    MA.act(a[115], b[115], mood=(-0.8, -0.6, 0.15), lean=0.1)
    MA.act(a[116], b[121], look=lambda t, u: est(YP, t) if t < a[120] + 1.0 else Vector((-3.1, 0.0, 1.4)), mood=(-0.9, -0.4, 0.05),
           armL=Vector((-1.0, 6.05, 1.3)))
    MA.act(a[122], b[123], mood=lambda t, u: (-1.0, -0.7, 0.3 + 0.4 * abs(math.sin(t * 8))), lean=0.2,
           look=lambda t, u: est(YM, t), armR=lambda t, u: est(YM, t) + Vector((0.3, 0, -0.3)) if t > a[123] + 2 else None)
    MA.act(a[124], b[124], z=0.0, look=Vector((0, 0.5, 1.5)), mood=(-1.0, -0.7, 0.1), lean=0.05)
    MA.act(a[125], b[126], z=0.0, look=Vector((0, 0.1, 1.55)), mood=(-1.0, -0.8, 0.2), bob=0.006, bobf=1.9)
    MA.act(a[127], b[128], z=0.0, look=lambda t, u: est(DV, t) + Vector((0, 0, -1.2)), mood=(-0.9, -0.9, 0.5), lean=-0.1)
    MA.act(a[122], b[123], z=hs.on_stairs(MA))
    MA.act(a[129], a[130] + 1.2, sit=1.0, seat=0.47, look=Vector((6.7, 13.2, 0.6)), mood=(-0.7, -0.5, 0.2), _hold0=True)
    S.on(MA, [113, 115, 116, 120, 122, 123, 124, 125, 126, 127, 129, 130])
    # ---------------------------------------------------------------- the memory: parents choose a groom
    SOFA = H["sofa"]
    YP.at(a[116], SOFA.x - 0.05, SOFA.y - 0.3, math.pi).stay(b[120])
    YP.act(a[116], b[120], sit=1.0, seat=0.44, _hold0=True, hp=0.55, look=Vector((3.15, 2.55, 0.45)),
           armR=lambda t, u: Vector((3.3, 2.4 + 0.15 * math.sin(t * 0.8), 0.5)), mood=lambda t, u: (-0.3, 0.0, talk(a[117] + 0.3, b[117] - 0.2)(t, u)[2] + talk(a[119] + 0.5, b[119] - 0.4)(t, u)[2]))
    YP.act(a[119], b[119], hp=0.1, look=lambda t, u: est(YMO, t))
    CAB = H["cabinet"]
    YMO.at(a[116], CAB.x, CAB.y - 0.6, math.pi / 2).stay(a[118] + 1.2).walk(a[118] + 3.0, 2.15, 3.3, mode="smooth").walk(a[118] + 3.6, 1.75, 4.0, yaw=0.0, gait="stand")
    YMO.stay(b[120], 0.0)
    YMO.act(a[118], a[118] + 1.4, armL=Vector((CAB.x - 0.2, CAB.y - 0.1, 0.7)), armR=Vector((CAB.x + 0.1, CAB.y - 0.1, 0.7)), lean=0.4, crouch=0.15)
    YMO.act(a[118] + 3.4, b[120], sit=1.0, seat=0.5, look=lambda t, u: est(YP, t), mood=talk(a[118] + 3.6, b[118] - 0.2, (-0.2, 0.1)))
    S.on(YP, [116, 117, 118, 119, 120], step=2)
    S.on(YMO, [116, 118, 119, 120], step=2)
    photos = props.photos_on_table(Vector((3.15, 2.55, 0.455)), 7)
    alb = props.album()
    bake_fn(alb, a[116], a[118] + 1.4, lambda t: (Vector((CAB.x, CAB.y, 0.55)), None), 12, rot=False)
    bake_fn(alb, a[118] + 1.4, a[118] + 3.0, lambda t: ((YMO.J(t)["hand"]["L"] + YMO.J(t)["hand"]["R"]) / 2, None), 2, rot=False)
    bake_fn(alb, a[118] + 3.0, b[120], lambda t: (Vector((3.0, 3.0, 0.45)), None), 12, rot=False)
    for ob in (photos, alb):
        vis_tree(ob, [(INSIDE0, b[120])])
    # ---------------------------------------------------------------- young Mamta and Dev come home
    YM.at(a[121], -1.1, -24.0, math.pi / 2).walk(b[123], -0.35, -5.6).walk(a[124] + 1.0, -0.3, -3.6).walk(a[124] + 2.6, -0.15, -1.2).walk(a[124] + 3.4, -0.1, 0.9)
    DV.at(a[121], -0.2, -24.2, math.pi / 2).walk(b[123], 0.45, -5.8).walk(a[124] + 1.0, 0.4, -3.6).walk(a[124] + 2.6, 0.25, -1.2).walk(a[124] + 3.4, 0.2, 0.8)
    for x, o in ((YM, DV), (DV, YM)):
        x.act(a[121], b[124], z=hs.on_stairs(x), look=lambda t, u, o=o: est(o, t) if (t % 4) < 2 else est(o, t) + Vector((0, 8, 0)), mood=(0.2, 0.8, 0.15))
    YM.act(a[121], a[124] + 2.4, armR=lambda t, u: DV.J(t)["hand"]["L"] if False else est(DV, t) + Vector((-0.35, -0.05, -0.85)))
    # ---------------------------------------------------------------- 127: Dev thrown out; father with the lathi; mother drags Mamta in
    DV.at(a[127], 0.0, 0.8, -math.pi / 2).walk(a[127] + 0.8, 0.0, -0.3, gait="run").walk(a[127] + 1.6, 0.05, -1.1, gait="stand")
    DV.stay(b[128])
    DV.act(a[127] + 0.7, b[128], fade=0.7, lie=-1.0, bed=0.0, z=0.0, armL=("rel", 0.4, 0.15, 0.1), armR=("rel", 0.4, -0.15, 0.1))
    YP.at(a[127] + 0.3, 0.0, 2.2, -math.pi / 2).walk(a[127] + 1.6, 0.05, 0.25, gait="run").stay(b[128])
    YP.act(a[127], b[128], mood=(-1.0, -0.8, 0.5), look=lambda t, u: est(DV, t) + Vector((0, 0, -1.3)),
           armR=lambda t, u: ("rel", 0.12, -0.1, lerp(0.1, 0.45, seg(t, a[127] + 1.4, a[127] + 2.2))), lean=0.1)
    YMO.at(a[127], -0.2, 1.4, math.pi / 2).walk(b[127], -0.8, 4.5, mode="smooth")
    YM.at(a[127], -0.3, 1.0, -math.pi / 2).walk(b[127], -0.9, 4.0, yaw=-math.pi / 2, gait="stand")
    YMO.act(a[127], b[127], armR=lambda t, u: est(YM, t) + Vector((0.15, -0.1, -0.6)), look=lambda t, u: est(YM, t))
    YM.act(a[127], b[127], armL=lambda t, u: est(DV, t) + Vector((0, 0, -0.6)), mood=(-1.0, -0.8, 0.6), lean=0.3, look=lambda t, u: est(DV, t))
    S.on(YM, [121, 123, 124, 127])
    S.on(DV, [121, 123, 124, 127])
    S.on(YP, [127, 128])
    S.on(YMO, [127], step=2)
    S.on(MO, [129, 130], step=4)
    lt = props.lathi()
    hold(lt, YP, "R", a[127], b[128], off=(0.0, 0.0, -0.4))
    vis(lt, [(a[127], b[128])])

    # ---------------------------------------------------------------- cameras
    S.shoot(113, lambda t: on(MA, a[113] + 1, "CU", 85, yaw=0.15, az=-50, tt=a[113]))
    S.shoot(114, lambda t: dict(pos=Vector((5.2, 11.7, 1.25)), look=Vector((6.9, 13.0, 0.5)), focus=2.0, fstop=2.8))

    def c115(t):
        h = est(MA, t)
        j = MA.pos_yaw(t)
        pos = h - fvec(j[2]) * 1.9 + Vector((0, 0, -0.1))
        return dict(pos=pos, look=h + fvec(j[2]) * 2 + Vector((0, 0, -0.3)), focus=1.9, fstop=2.8)
    S.shoot(115, c115)
    S.shoot(116, lambda t: dict(pos=Vector((-4.55, 5.55, 2.35)), look=Vector((1.6, 1.7, 0.75)), focus=5.0, fstop=5.6))
    S.shoot(117, lambda t: dict(pos=Vector((3.15, 2.55, 1.3)), look=Vector((3.15, 2.5501, 0.45)), focus=0.85, fstop=4.0))
    S.shoot(118, lambda t: dict(pos=Vector((0.4, 2.4, 1.4)), look=est(YMO, t) + Vector((0, 0, -0.45)), focus=3.0, fstop=2.8))
    S.shoot(119, lambda t: on(YP, t, "MCU", 85, yaw=math.pi, az=15, tt=a[119]))
    S.shoot(120, lambda t: on(MA, t, "CU", 85, yaw=-math.pi / 2, az=-15, tt=a[120]))
    S.shoot(121, lambda t: dict(pos=Vector((-3.05, 0.45, 1.5)), look=mid(est(YM, t), est(DV, t)) + Vector((0, 0, -1.0)), focus=18.0, fstop=4.0))
    S.shoot(122, lambda t: dict(pos=Vector((1.5, -6.6, 0.45)), look=est(MA, t) + Vector((0, 0, -0.45)), focus=5.0, fstop=4.0))

    def c123(t):                                  # tracking alongside them (east side), moving north
        m = mid(est(YM, t), est(DV, t), est(MA, t))
        pos = Vector((2.4, m.y - 1.2, 0.3))
        return dict(pos=pos, look=Vector((m.x, m.y, m.z - 1.55)), focus=(Vector((m.x, m.y, 0.3)) - pos).length, fstop=2.8)
    S.shoot(123, c123)
    S.shoot(124, lambda t: dict(pos=Vector((1.9, -4.6, 0.75)), look=Vector((0.3, 0.0, 1.0)), focus=4.5, fstop=4.0))
    S.shoot(125, lambda t: push(on(MA, t, "CU", 85, yaw=math.pi / 2, az=-75, tt=a[125]), 0.2 * seg(t, a[125], b[125])))
    S.shoot(126, lambda t: dict(pos=eyes(MA, t) + Vector((0.42, 0.28, 0.0)), look=eyes(MA, t), focus=0.5, fstop=4.0))
    S.shoot(127, lambda t: dict(pos=Vector((-0.9, -7.2, 0.15)), look=Vector((0.0, 0.2, 0.85)), focus=7.3, fstop=4.0))
    S.shoot(128, lambda t: dict(pos=YP.J(a[128] + 0.5)["hand"]["R"] + Vector((0.25, -0.75, -0.35)), look=YP.J(t)["hand"]["R"], focus=0.85, fstop=2.8))
    S.shoot(129, lambda t: on(MA, t, "CU", 85, yaw=0.15, az=-50, tt=a[129]))
    S.shoot(130, lambda t: dict(pos=Vector((5.2, 9.6, 1.4)), look=Vector((6.0, 12.6, 0.8)), focus=3.1, fstop=2.8))
    # ---------------------------------------------------------------- lights
    S.light(113, lambda t: head(MA, t), key=dict(side="R", ang=80, el=20, d=1.6, w=20, k=7500, size=1.0))
    S.light(114, (6.9, 13.0, 0.5), key=dict(side="R", ang=60, el=40, d=2, w=10, k=8000, size=1.0))
    S.light(115, lambda t: head(MA, t), key=dict(side="L", ang=20, el=10, d=3, w=40, k=3000, size=1.0), rim=dict(side="R", ang=160, el=20, d=2, w=20, k=7500))
    S.light(116, (2.5, 2.5, 1.0), key=dict(side="L", ang=40, el=40, d=3, w=60, k=3000, size=2.0), rim=dict(side="R", ang=150, el=20, d=2, w=20, k=7500))
    S.light(117, (3.15, 2.55, 0.45), key=dict(side="L", ang=40, el=60, d=1.2, w=20, k=3000, size=0.8))
    S.light(118, lambda t: head(YMO, t), key=dict(side="L", ang=40, el=40, d=1.6, w=40, k=3000, size=0.8))
    S.light(119, lambda t: head(YP, t), key=dict(side="L", ang=20, el=-25, d=1.2, w=40, k=3000, size=0.4))
    S.light(120, lambda t: head(MA, t), key=dict(side="L", ang=80, el=10, d=1.4, w=30, k=3000, size=0.6), fill=dict(side="R", ang=80, el=10, d=1.4, w=25, k=8000))
    S.light(121, mid(Vector((0, -15, 0)), Vector((0, -15, 0))), rim=dict(side="R", ang=170, el=5, d=6, w=0))
    S.light(122, lambda t: head(MA, t), key=dict(side="L", ang=60, el=20, d=3, w=40, k=9000, size=2))
    S.light(123, lambda t: head(MA, t), key=dict(side="L", ang=60, el=20, d=3, w=50, k=9000, size=2))
    S.light(124, (0, -0.5, 1.2), key=dict(side="L", ang=30, el=20, d=3, w=10, k=9000, size=2))
    S.light(125, lambda t: head(MA, t), key=dict(side="R", ang=60, el=0, d=0.9, w=12, k=2900, size=0.03))
    S.light(126, lambda t: head(MA, t), key=dict(side="R", ang=60, el=0, d=0.9, w=12, k=2900, size=0.02))
    S.light(127, (0, -0.5, 1.0), rim=dict(side="L", ang=175, el=10, d=2.5, w=0))
    S.light(128, lambda t: YP.J(t)["hand"]["R"], key=dict(side="L", ang=150, el=10, d=1.0, w=30, k=2900, size=0.05))
    S.light(129, lambda t: head(MA, t), key=dict(side="R", ang=80, el=20, d=1.6, w=15, k=8000, size=0.6))
    S.light(130, lambda t: head(MO, t), key=dict(side="R", ang=60, el=40, d=1.6, w=15, k=8000, size=1.0))
    S.state(a[127], DRBulb=(500, 3000))
