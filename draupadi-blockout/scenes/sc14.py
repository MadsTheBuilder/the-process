# Scene 14 - THE MIRROR - INT. House (Mamta's Room) - Afternoon (shots 92-94, 11 s)
# Fresh clothes, damp hair. The three-panel mirror on the dressing table (east wall, facing west) is shut like a
# door; its flaps stick, then spring open on a hard 'dhakk' - the cut into memory.
import math

from mathutils import Quaternion, Vector

from kit import *
from film import *
import cast
import hs
import props
import sets
from sets import H

STOOL = Vector((-1.45, 9.0))


def mamta_room_soft(S, st, t):
    C = sets.mats()
    sets.sun_dir(st["L"]["Sun"], 186, 16)
    S.state(t, Sun=(1.6, 4800), WinM=(170, 5200), WinCorr=(20, 6000), WinMo=(15, 6000), BulbM=0)
    S.emit(t, C["sky_win"], 3.0)
    S.emit(t, C["bulb"], 0.0)
    S.world(t, (0.42, 0.4, 0.36), 0.03)


def build(S):
    T = S.T
    a = {n: T[n][0] for n in T}
    b = {n: T[n][1] for n in T}
    st = hs.house(S)
    mamta_room_soft(S, st, 0)
    S.exposure(0, 0.45)
    hs.mirror_probes(st)
    import bpy
    bpy.context.scene.eevee.use_raytracing = True
    hs.flaps(st, [(0, 0.0, "const"), (a[93] + 1.2, 0.0, "bez"), (a[93] + 1.5, 0.08, "bez"), (a[93] + 1.8, 0.0, "bez"),
                  (a[93] + 2.4, 0.0, "bez"), (a[93] + 2.7, 0.1, "bez"), (a[93] + 3.0, 0.02, "const"),
                  (a[94] + 0.35, 0.02, "bez"), (a[94] + 0.6, 1.08, "bez"), (a[94] + 0.85, 0.97, "bez"), (a[94] + 1.1, 1.0, "const")])
    MA = cast.mamta("fresh")
    AX, AY = H["almirah"]
    MA.at(0, AX + 0.2, AY - 0.75, math.pi / 2).stay(a[92] + 2.2).walk(a[92] + 4.6, STOOL.x - 0.15, STOOL.y - 0.2, mode="smooth")
    MA.walk(a[93] + 0.8, STOOL.x, STOOL.y, yaw=0.0, mode="smooth", gait="stand").stay(b[94], 0.0)
    MA.act(0, a[92] + 2.2, armL=lambda t, u: (lambda j: j["head_c"] + j["hf"] * 0.1 + j["tl"] * 0.05 + Vector((0, 0, -0.02 + 0.04 * math.sin(t * 6))))(MA.J(t)),
           armR=lambda t, u: (lambda j: j["head_c"] + j["hf"] * 0.1 - j["tl"] * 0.05)(MA.J(t)), hp=0.12, eyes=0.3, mood=(-0.2, 0.0, 0.0))
    MA.act(a[92] + 2.0, b[94], look=Vector((-0.7, 9.0, 1.3)), mood=(-0.4, -0.2, 0.0))
    MA.act(a[93] + 0.5, b[94], sit=1.0, seat=0.44)
    tug = lambda side: (lambda t, u: Vector((-0.78, 9.0 + side * 0.55, 1.2)) + Vector((-0.04 * abs(math.sin(t * 7)), 0, 0)))
    MA.act(a[93] + 1.0, a[94] + 0.6, fade=0.3, armL=tug(-1), armR=tug(1), lean=0.15, mood=(-0.6, -0.3, 0.1))
    MA.act(a[94] + 0.5, b[94], fade=0.15, armL=Vector((-1.0, 8.35, 1.25)), armR=Vector((-1.0, 9.65, 1.25)), lean=-0.05, mood=(-0.8, -0.4, 0.3))
    S.on(MA, [92, 93, 94])
    tw = props.towel()
    hold(tw, MA, "L", 0, a[92] + 4.0, off=(0.0, 0.0, 0.0))
    bake_fn(tw, a[92] + 4.0, b[94], lambda t: (Vector((-1.05, 9.65, 0.82)), Quaternion((1, 0, 0), math.pi / 2)))
    S.shoot(92, lambda t: dict(pos=Vector((-2.4, 10.4, 1.5)), look=head(MA, t) + Vector((0, 0, -0.3)), focus=(head(MA, t) - Vector((-2.4, 10.4, 1.5))).length, fstop=2.8))
    # 93: over her shoulder into the mirror - her reflection is the subject
    S.shoot(93, lambda t: dict(pos=Vector((-2.85, 9.55, 1.42)), look=Vector((-0.67, 9.0, 1.2)), focus=2.25 + 0.8, fstop=2.8))
    S.shoot(94, lambda t: dict(pos=Vector((-1.05, 8.15, 1.3)), look=Vector((-0.72, 8.75, 1.22)), focus=0.7, fstop=2.8))
    S.light(92, lambda t: head(MA, t), key=dict(side="L", ang=60, el=20, d=2.4, w=40, k=4800, size=1.2))
    S.light(93, lambda t: head(MA, t), key=dict(side="R", ang=50, el=15, d=1.8, w=25, k=4800, size=1.0), rim=dict(side="L", ang=150, el=25, d=1.6, w=35, k=4800))
    S.light(94, (-0.72, 8.75, 1.2), key=dict(side="R", ang=50, el=20, d=1.2, w=60, k=5000, size=0.6), kick=dict(side="L", ang=70, el=20, d=1.2, w=60, k=5000))
    # the flare: a hard flick of window light off the glass as it swings
    S.state(a[94] + 0.5, Sun=(6.0, 4800))
    S.state(a[94] + 0.9, Sun=(1.6, 4800))
