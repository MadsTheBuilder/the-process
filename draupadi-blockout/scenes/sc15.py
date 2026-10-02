# Scene 15 - CORE MEMORY: THE BRIDE - INT. House (Mamta's Room) - Night / Afternoon (shots 95-104, 40 s)
# On the 'dhakk' the light flips to hard night tungsten: a bare bulb overhead + bulbs round the mirror. In the
# three-panel mirror: three brides with dead eyes, hands closing in from every side to dress her for the wager.
import math

from mathutils import Quaternion, Vector

from kit import *
from film import *
import cast
import hs
import props
import sets
from sets import H
from scenes.sc14 import mamta_room_soft, STOOL

MIRROR = Vector((-0.67, 9.0, 1.2))


def build(S):
    T = S.T
    a = {n: T[n][0] for n in T}
    b = {n: T[n][1] for n in T}
    st = hs.house(S)
    C = sets.mats()
    hs.mirror_probes(st)
    import bpy
    bpy.context.scene.eevee.use_raytracing = True
    hs.hide_plates(st, [(0, b[101])])
    hs.flaps(st, [(0, 1.0, "const")])
    vm, vkey = hs.vanity_bulbs(0, b[101])
    NIGHT_END = b[101]
    # night tungsten
    S.state(0, BulbM=(110, 2700), VanityKey=(140, 2700), Sun=0, WinM=0, WinCorr=0, WinMo=0)
    S.emit(0, C["bulb"], 40.0)
    S.emit(0, vm, 30.0)
    S.emit(0, C["sky_win"], 0.0)
    S.world(0, (0.02, 0.02, 0.03), 0.02)
    S.exposure(0, 0.3)
    # afternoon again (102-104)
    mamta_room_soft(S, st, NIGHT_END)
    S.state(NIGHT_END, VanityKey=0)
    S.emit(NIGHT_END, vm, 0.0)
    S.exposure(NIGHT_END, 0.45)

    BR = cast.young_mamta("bride_bare", name="Bride")
    AUNT = cast.extra("Aunt", 77, top=(0.40, 0.25, 0.05), skirt=True, dup=(0.55, 0.35, 0.05), H=1.58)
    YMO = cast.mother(young=True)
    COUS = cast.extra("Cousin", 78, top=(0.55, 0.15, 0.30), skirt=True, dup=(0.6, 0.4, 0.5), H=1.55)
    BR.at(0, STOOL.x, STOOL.y, 0.0).stay(NIGHT_END)
    BR.act(0, NIGHT_END, fade=0, sit=1.0, seat=0.44, eyes=0.85, mood=(0.0, 0.0, 0.0), look=MIRROR + Vector((0, 0, 0.05)),
           armL=("rel", 0.25, -0.02, -0.38), armR=("rel", 0.25, 0.02, -0.38))
    # 97: glances down, brushes her hand over the stomach
    BR.act(a[97], b[97], hp=0.6, look=None, armR=lambda t, u: (lambda j: j["hip_c"] + j["tf"] * 0.16 + j["tl"] * (0.06 * math.sin(t * 1.6)) + Vector((0, 0, 0.12)))(BR.J(t)))
    BR.act(a[98], b[98], eyes=0.75, mood=(-0.5, -0.2, 0.0))
    BR.act(a[100], NIGHT_END, eyes=0.7, mood=(-0.6, -0.3, 0.0))
    HEADP = lambda t: est_seated(BR, t, 0.44)
    AUNT.at(0, STOOL.x + 0.15, STOOL.y - 0.62, math.pi / 2).stay(NIGHT_END)
    YMO.at(0, STOOL.x + 0.12, STOOL.y + 0.62, -math.pi / 2).stay(NIGHT_END)
    COUS.at(0, STOOL.x - 0.62, STOOL.y + 0.05, 0.0).stay(NIGHT_END)
    ear = lambda t, u: HEADP(t) + Vector((0.02, -0.09, -0.02))
    nose = lambda t, u: HEADP(t) + Vector((0.11, 0.0, -0.03))
    bun = lambda t, u: HEADP(t) + Vector((-0.1, 0.0, 0.06))
    AUNT.act(a[96], b[96], armL=ear, look=lambda t, u: HEADP(t), mood=(0.0, 0.2, 0.0))
    YMO.act(a[96], b[96], armR=nose, look=lambda t, u: HEADP(t), mood=(-0.2, 0.0, 0.0))
    COUS.act(a[96], b[96], armL=bun, armR=lambda t, u: bun(t, u) + Vector((0, 0.05, 0.03 * math.sin(t * 9))), look=lambda t, u: HEADP(t))
    COUS.act(a[99], b[99], armL=lambda t, u: HEADP(t) + Vector((-0.05, 0.12, 0.12)), armR=lambda t, u: HEADP(t) + Vector((-0.05, -0.12, 0.12)), look=lambda t, u: HEADP(t))
    YMO.act(a[101], b[101], armR=lambda t, u: HEADP(t) + Vector((0.1, 0.06, lerp(0.15, -0.05, seg(t, a[101] + 0.6, a[101] + 2.6)))),
            armL=lambda t, u: HEADP(t) + Vector((0.1, -0.06, lerp(0.15, -0.05, seg(t, a[101] + 0.6, a[101] + 2.6)))), look=lambda t, u: HEADP(t), mood=(-0.4, -0.2, 0.0))
    for x in (BR,):
        S.on(x, [95, 96, 97, 98, 99, 100, 101])
    for x in (AUNT, YMO, COUS):
        S.on(x, [95, 96, 97, 98, 99, 100, 101], step=2)
    tear(BR, a[100] + 0.4, 2.2, side=0.45)
    # the red dupatta: placed on her head (99), pulled down over her face (101)
    veil = new_obj("RedDupatta", sphere_mesh("rd", BR.hr * 1.22, 16, 10, (1, 1, 0.95)), M((0.62, 0.03, 0.05), 0.9, alpha=0.93))
    drape = props.dupatta_veil()

    def veil_fn(t):
        j = BR.J(t)
        down = 0.0 if t < a[99] + 1.2 else 0.0
        drop = (1 - seg(t, a[99] + 0.4, a[99] + 1.4)) * 0.25
        return j["head_c"] + j["hu"] * (BR.hr * 0.25 + drop) - j["hf"] * BR.hr * 0.12, None
    bake_fn(veil, a[99], NIGHT_END, veil_fn, 1, rot=False)
    vis(veil, [(a[99], NIGHT_END)])

    def drape_fn(t):
        j = BR.J(t)
        k = seg(t, a[101] + 0.6, a[101] + 2.6)
        p = j["head_c"] + j["hf"] * BR.hr * 1.15 + j["hu"] * lerp(BR.hr * 1.9, -BR.hr * 2.0, k)
        return p, basis_quat(j["tl"], j["hu"])
    bake_fn(drape, a[101], NIGHT_END, drape_fn)
    vis(drape, [(a[101] + 0.3, NIGHT_END)])
    # present day: Papa at the door with a plate (102-104)
    MA = cast.mamta("fresh")
    PA = cast.papa()
    MA.at(a[102], STOOL.x, STOOL.y, 0.0).stay(a[102] + 0.5).stay(a[102] + 1.0, -math.pi / 2 - 0.2, tt=0.4).stay(a[104] + 1.0)
    MA.walk(b[104], -1.5, 7.9, mode="smooth")
    MA.act(a[102], a[104] + 1.2, sit=1.0, seat=0.44, look=Vector((-1.45, 7.6, 1.5)), mood=lambda t, u: (-0.5, -0.2, 0.0), _hold0=True)
    MA.act(a[104] + 0.4, a[104] + 1.4, hp=lambda t, u: 0.2 * math.sin(u * math.pi))
    MA.act(a[104] + 2.0, b[104], armR=lambda t, u: est(PA, t) + Vector((0.2, 0.3, -0.5)), armL=lambda t, u: est(PA, t) + Vector((-0.15, 0.3, -0.5)))
    PA.at(a[102], -1.45, 7.45, math.pi / 2).stay(b[103]).walk(a[104] + 2.0, -1.45, 7.95, mode="smooth").stay(b[104], math.pi / 2 + 0.4)
    PA.act(a[102], b[104], armR=("rel", 0.3, 0.05, -0.12), armL=("rel", 0.3, 0.12, -0.12), look=lambda t, u: est(MA, t),
           mood=lambda t, u: (-0.3, -0.1, talk(a[102] + 0.3, a[102] + 1.8)(t, u)[2] + talk(a[103] + 0.4, b[103] - 0.4)(t, u)[2]), hp=0.1)
    S.on(MA, [102, 103, 104])
    S.on(PA, [102, 103, 104])
    th = props.thaali()
    bake_fn(th, a[102], b[104], lambda t: ((PA.J(t)["hand"]["L"] + PA.J(t)["hand"]["R"]) / 2 + Vector((0, 0, 0.02)) if t < a[104] + 2.6 else
                                           (MA.J(t)["hand"]["L"] + MA.J(t)["hand"]["R"]) / 2 + Vector((0, 0, 0.02)), None), 2, rot=False)

    # cameras: into the mirror (the reflection is the image) or tight from the mirror side
    def into_mirror(dist_cam, side=0.0, dz=0.2, look_dz=0.0):
        def f(t):
            pos = Vector((STOOL.x - dist_cam, STOOL.y + side, 1.25 + dz))
            e = eyes(BR, t)
            virt = Vector((2 * MIRROR.x - e.x, e.y, e.z + look_dz - 0.05))      # her image behind the glass
            return dict(pos=pos, look=virt, focus=(virt - pos).length, fstop=2.8)
        return f
    S.shoot(95, into_mirror(1.15, 0.38, 0.22))
    S.shoot(96, into_mirror(0.55, 0.3, 0.16, 0.06))
    S.shoot(97, lambda t: dict(pos=Vector((-0.92, 9.18, 1.62)), look=Vector((-1.25, 9.0, 0.62)), focus=1.1, fstop=2.8))
    S.shoot(98, into_mirror(0.35, 0.22, 0.12, 0.08))
    S.shoot(99, into_mirror(0.85, 0.32, 0.2, 0.08))
    S.shoot(100, lambda t: dict(pos=Vector((-0.88, 9.17, 1.27)), look=eyes(BR, a[100] + 1) + Vector((0, 0.03, -0.05)), focus=0.52, fstop=4.0))
    S.shoot(101, into_mirror(0.3, 0.2, 0.12, 0.08))
    S.shoot(102, lambda t: dict(pos=Vector((-3.6, 9.4, 1.45)), look=Vector((-1.6, 8.3, 1.2)), focus=2.4, fstop=2.8))
    S.shoot(103, lambda t: on(PA, t, "MCU", 85, yaw=math.pi / 2, az=10, tt=a[103]))
    S.shoot(104, lambda t: dict(pos=Vector((-3.8, 9.6, 1.45)), look=mid(head(MA, t), head(PA, t)) + Vector((0, 0, -0.35)), focus=2.6, fstop=2.8))
    S.light(95, lambda t: head(BR, t), key=dict(side="R", ang=25, el=20, d=1.0, w=25, k=2700, size=0.3))
    S.light(96, lambda t: head(BR, t), key=dict(side="R", ang=25, el=55, d=1.2, w=30, k=2700, size=0.2))
    S.light(97, lambda t: head(BR, t), key=dict(side="R", ang=20, el=75, d=1.4, w=25, k=2700, size=0.1))
    S.light(98, lambda t: head(BR, t), key=dict(side="R", ang=20, el=20, d=1.0, w=22, k=2700, size=0.3))
    S.light(99, lambda t: head(BR, t), rim=dict(side="L", ang=150, el=60, d=1.0, w=40, k=2700, size=0.1))
    S.light(100, lambda t: head(BR, t), key=dict(side="R", ang=15, el=10, d=0.8, w=18, k=2700, size=0.1))
    S.light(101, lambda t: head(BR, t), rim=dict(side="L", ang=160, el=60, d=1.0, w=50, k=2700, size=0.1))
    S.light(102, lambda t: head(PA, t), rim=dict(side="R", ang=165, el=20, d=1.6, w=40, k=6000, size=1.0), key=dict(side="L", ang=40, el=15, d=2, w=15, k=4800))
    S.light(103, lambda t: head(PA, t), key=dict(side="L", ang=40, el=18, d=1.8, w=35, k=4800, size=1.2), fill=dict(side="R", ang=40, el=10, d=1.8, w=10, k=4800))
    S.light(104, lambda t: mid(head(MA, t), head(PA, t)), key=dict(side="L", ang=50, el=20, d=2.4, w=40, k=4800, size=1.4))
