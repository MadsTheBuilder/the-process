# Scene 4 - FLASH: BIDAAI - EXT. House - Night / Day (shots 29-33, 22 s)
# 29 is the exact frame of 27 at night: fairy-light strings, decorated car, relatives, the bride at the door.
# 31 rice thrown back over her head in slow motion. 32-33 back to the grey day: bags in the dust, she goes in.
import math
import random

from mathutils import Quaternion, Vector

from kit import *
from film import *
import cast
import hs
import props
import sets
from sets import step_z
from scenes.sc03 import FRAME27, overcast


def build(S):
    T = S.T
    E = S.END
    C = sets.mats()
    st = hs.house(S)
    a29, b29 = T[29]
    a30, b30 = T[30]
    a31, b31 = T[31]
    a32, b32 = T[32]
    a33, b33 = T[33]
    NIGHT = (0, b31)
    # ---------------------------------------------------------------- night: wedding
    S.world(0, (0.02, 0.035, 0.10), 0.9)
    hs.hide_plates(st)
    sets.sun_dir(st["L"]["Moon"], 60, 55)
    S.state(0, Moon=(0.35, 7500), Porch=(220, 3000), DRBulb=(260, 2900), Lamp=(60, 2900))
    S.emit(0, C["porch"], 25.0)
    S.emit(0, C["fairy"], 14.0)
    S.emit(0, C["bulb2"], 8.0)
    S.exposure(0, -0.2)
    hs.door_keys(st, [(0, 85, "const")])
    hs.fairy_strings(C["fairy"])
    car, cfairy = props.wedding_car()
    car.location = (0.9, -12.5, -1.2)
    car.rotation_euler.z = -math.pi / 2
    S.emit(0, cfairy, 10.0)
    fl = lamp("CarGlow", "POINT", (0.9, -12.5, 0.6), 0, kelvin(2400), size=0.5)
    canopy = lamp("FairyFill", "AREA", (0, -6, 4.5), 0, kelvin(2500), size=8)
    S.state(0, CarGlow=(140, 2400), FairyFill=(420, 2500))
    lane = lamp("LaneStrings", "AREA", (0, -24, 4.0), 0, kelvin(2500), size=(7, 30))
    S.state(0, LaneStrings=(900, 2500))
    S.state(b31, LaneStrings=0)
    # ---------------------------------------------------------------- day again (32-33)
    overcast(S, b31, 3.0)
    S.state(b31, Moon=0, Porch=0, DRBulb=0, Lamp=0, CarGlow=0, FairyFill=0)
    S.emit(b31, C["porch"], 0.0)
    S.emit(b31, C["fairy"], 0.0)
    S.emit(b31, C["bulb2"], 0.0)
    S.emit(b31, cfairy, 0.0)
    S.exposure(b31, -0.45)
    import bpy
    fairy_ob = bpy.data.objects["FAIRY_fairy"]
    vis(fairy_ob, [NIGHT])
    vis_tree(car, [NIGHT])

    # ---------------------------------------------------------------- cast (night)
    BR = cast.young_mamta("bride", name="Bride")
    YP = cast.papa(young=True)
    YM = cast.mother(young=True)
    BR.at(0, 0.0, -0.75, -math.pi / 2).stay(b30).at(a31, 0.0, -1.3, -math.pi / 2).stay(b31)
    YP.at(0, 0.75, -0.6, -math.pi / 2 + 0.5).stay(b31)
    YM.at(0, -0.72, -0.62, -math.pi / 2 - 0.5).stay(b31)
    BR.act(0, b31, hp=0.18, mood=(0.0, 0.0, 0.0), armL=("rel", 0.2, -0.08, -0.3), armR=("rel", 0.2, 0.08, -0.3),
           look=Vector((0.0, -12.0, 0.4)))
    # 31: rice thrown back over the head, slow motion (60 fps -> 2.5x stretched)
    throw = lambda t, u: ("rel", lerp(0.25, -0.05, seg(t, a31 + 0.6, a31 + 2.4)), 0.0, lerp(-0.05, 0.42, seg(t, a31 + 0.4, a31 + 2.2)))
    BR.act(a31, b31, fade=0.3, armL=throw, armR=throw, hp=lambda t, u: lerp(0.1, -0.2, seg(t, a31 + 0.6, a31 + 2.4)), look=None)
    YM.act(0, b31, armR=lambda t, u: (lambda j: j["head_c"] + j["hf"] * 0.08 + Vector((0, 0, -0.04)))(YM.J(t)),
           mood=(-0.9, -0.6, 0.15), shake=0.6, hp=0.25, look=lambda t, u: est(BR, t))
    YP.act(0, b31, mood=(-0.7, -0.5, 0.0), look=lambda t, u: est(BR, t), armL=("rel", 0.1, 0.08, -0.28))
    rel = []
    rnd = random.Random(9)
    spots = [(-1.9, -1.0), (1.9, -1.1), (-1.6, -2.4), (1.7, -2.6), (-2.6, -4.6), (2.4, -4.4), (-1.2, -5.6), (1.0, -6.4),
             (-2.9, -7.6), (3.1, -8.4), (-0.8, -9.6)]
    fest = [(0.55, 0.18, 0.08), (0.45, 0.3, 0.05), (0.20, 0.10, 0.30), (0.62, 0.42, 0.10), (0.15, 0.30, 0.25), (0.50, 0.08, 0.20)]
    for i, (x, y) in enumerate(spots):
        woman = i % 2 == 0
        r = cast.extra("Rel%d" % i, 40 + i, top=fest[i % len(fest)], skirt=woman, dup=fest[(i + 2) % len(fest)])
        yaw = math.atan2(-0.8 - y, 0.0 - x)
        r.at(0, x, y, yaw).stay(b31)
        r.act(0, b31, fade=0, z=step_z(y), look=lambda t, u, br=BR: est(BR, t), mood=(-0.8, -0.5, 0.0),
              shake=0.4 if woman else 0.0)
        if woman and i % 4 == 0:
            r.act(0, b31, armR=lambda t, u, rr=r: (lambda j: j["head_c"] + j["hf"] * 0.08 + Vector((0, 0, -0.05)))(rr.J(t)))
        S.on(r, [29, 30, 31], step=4)
        rel.append(r)
    S.on(BR, [29, 30, 31])
    S.on(YP, [29, 30, 31], step=2)
    S.on(YM, [29, 30, 31], step=2)
    # rice: grains thrown back toward the house, ballistic with time stretched (slow motion)
    grain = props.rice_grain()
    rm = M((0.95, 0.93, 0.85), 0.25, emit=(1, 0.95, 0.8), strength=2.5)
    t_rel = a31 + 1.9
    for k in range(160):
        g = new_obj("rice", grain, rm)
        v = Vector((rnd.uniform(-0.9, 0.9), rnd.uniform(1.0, 2.8), rnd.uniform(0.8, 3.0)))
        spin_ = rnd.uniform(-8, 8)

        def gp(t, v=v, k=k, sp=spin_):
            tt = max(0.0, (t - t_rel)) * 0.4
            hp_ = BR.J(min(t, t_rel))["hand"]["L" if k % 2 else "R"]
            p = hp_ + v * tt + Vector((0, 0, -4.9 * tt * tt))
            return p, Quaternion((1, 0, 0), sp * tt)
        bake_fn(g, a31, b31, gp, 2)
        vis(g, [(t_rel - 0.05, b31)])
    # ---------------------------------------------------------------- cast (day): bags in the dust, she goes in
    MA = cast.mamta("home")
    BAGP = Vector((0.35, -4.2, -1.2))
    MA.at(a32, -0.55, -4.75, math.radians(50)).stay(b32)
    MA.walk(a33 + 1.6, 0.0, -3.8, mode="smooth").walk(a33 + 4.0, 0.0, -0.4).walk(b33, 0.0, 1.1)
    MA.act(a32, E, fade=0, z=hs.on_stairs(MA))
    MA.act(a32 + 0.8, a33 + 1.2, fade=0.7, lean=0.75, crouch=0.25, armR=lambda t, u: BAGP + Vector((0.0, 0.05, lerp(0.35, 0.2, u))),
           look=BAGP, mood=(-0.6, -0.3, 0.0))
    MA.act(a33 + 1.0, b33, armR=("loc", 0.06, -0.28, 0.42), look=Vector((0, 2, 1.4)), mood=(-0.6, -0.3, 0.0))
    S.on(MA, [32, 33])
    case = props.suitcase()
    bag = props.duffel()
    bake_fn(case, a32, a33 + 1.1, lambda t: (BAGP + Vector((0.05, 0.1, 0.13)), Quaternion((0, 1, 0), math.pi / 2)))
    bake_fn(case, a33 + 1.1, b33, lambda t: (MA.J(t)["hand"]["R"] + Vector((0, 0, -0.64)), Quaternion((0, 0, 1), MA.J(t)["yaw"] + math.pi / 2)), 2)
    bake_fn(bag, a32, b33, lambda t: (BAGP + Vector((-0.45, 0.2, 0.1)), Quaternion((0, 0, 1), 0.6)) if t < a33 + 1.0 else
            (MA.J(t)["sh_c"] + MA.J(t)["tl"] * (MA.sw * 1.15) - MA.J(t)["spine"] * 0.32, basis_quat(MA.J(t)["tf"], MA.J(t)["spine"])), 2)
    for ob in (case, bag):
        vis_tree(ob, [(a32, b33)])
    # rice grains left near the steps in daylight
    for k in range(9):
        g = new_obj("riceday", grain, M((0.9, 0.88, 0.8), 0.4), loc=(BAGP.x + rnd.uniform(-0.5, 0.4), BAGP.y + rnd.uniform(0.0, 0.6), -1.195))
        vis(g, [(a32, b33)])

    # ---------------------------------------------------------------- cameras
    S.shoot(29, lambda t: dict(pos=FRAME27["pos"], look=FRAME27["look"], focus=12.0, fstop=5.6))
    S.shoot(30, lambda t: on(BR, t, "MCU", 85, az=-6, third=0.4, tt=a30))

    def c31(t):                                     # low, in front of her: hands over the head, rice into the lights
        j = BR.J(a31 + 2.0)
        mid_ = (j["hand"]["L"] + j["hand"]["R"]) / 2
        pos = mid_ + Vector((0.25, -2.6, -0.75))
        return dict(pos=pos, look=mid_ + Vector((0, 0.35, 0.12)), focus=(mid_ - pos).length + 0.2, fstop=2.8)
    S.shoot(31, c31)
    S.shoot(32, lambda t: dict(pos=BAGP + Vector((0.7, 0.35, 1.55)), look=BAGP + Vector((-0.15, 0.25, 0.0)), focus=1.75, fstop=4.0))
    S.shoot(33, lambda t: dict(pos=Vector((-1.4, -11.0, 0.35)), look=Vector((0.0, -1.5, 0.15)), focus=9.5, fstop=5.6))
    # ---------------------------------------------------------------- lights
    S.light(29, (0, -2, 0.5), key=dict(side="R", ang=20, el=35, d=6, w=150, k=2700, size=3))
    S.light(30, lambda t: head(BR, t), key=dict(side="L", ang=35, el=55, d=1.6, w=55, k=2700, size=0.4),
            rim=dict(side="R", ang=160, el=30, d=1.5, w=25, k=2600))
    S.light(31, lambda t: BR.J(a31 + 2)["hand"]["R"], rim=dict(side="L", ang=170, el=30, d=1.5, w=110, k=2600, size=0.4),
            key=dict(side="R", ang=40, el=10, d=1.6, w=10, k=2700))
    S.light(32, BAGP, key=dict(side="R", ang=30, el=70, d=3, w=60, k=6500, size=3))
    S.light(33, (0, -2, 0.3), key=dict(side="R", ang=30, el=60, d=4, w=80, k=6500, size=4))
