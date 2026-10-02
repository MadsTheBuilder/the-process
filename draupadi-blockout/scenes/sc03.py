# Scene 3 - HOMECOMING - EXT. House - Day (shots 27-28, 12 s)
# The lane runs south from the house (facade at y=0, ground -1.2). Camera far down the lane looking north:
# the house is a closed grey shape at the end of the frame. A tuk-tuk drops Mamta and pulls away past the lens.
import math

from mathutils import Quaternion, Vector

from kit import *
from film import *
import cast
import hs
import props
import sets

FRAME27 = dict(pos=Vector((-0.55, -39.4, 0.28)), look=Vector((0.1, 0.0, 0.3)))   # reused by scene 4 (shot 29)
MAMTA_ARRIVE = Vector((0.15, -36.45))


def overcast(S, t, sky=3.0):
    sets.sun_dir(bpy_ob("Sky"), 200, 72)
    S.state(t, Sky=(sky, 6500), Sun=0)
    S.world(t, (0.60, 0.64, 0.70), 0.55)
    S.emit(t, sets.mats()["sky_win"], 0.0)


def bpy_ob(name):
    import bpy
    return bpy.data.objects[name]


def build(S):
    T = S.T
    st = hs.house(S)
    overcast(S, 0)
    hs.hide_plates(st)
    S.exposure(0, -0.4)
    hs.door_keys(st, [(0, 70, "const")])
    a27, b27 = T[27]
    a28, b28 = T[28]
    # tuk-tuk: parked facing south, pulls away toward and past the camera
    tk = props.tuktuk()
    tk.rotation_euler.z = -math.pi / 2
    P0 = Vector((1.25, -35.6, -1.2))
    keys_vec(tk, "location", [(0, P0), (a27 + 3.6, P0), (b27, P0 + Vector((0.4, -9.5, 0)))])
    MA = cast.mamta("home")
    PA = cast.papa()
    MA.at(0, MAMTA_ARRIVE.x, MAMTA_ARRIVE.y, 0.15).stay(a27 + 3.2).stay(a27 + 4.6, 0.6).stay(a28 + 1.0, 0.6)
    MA.stay(b28 - 1.2, math.pi / 2, tt=2.4).stay(b28, math.pi / 2)
    MA.act(0, S.END, fade=0, z=-1.2)
    # pull the suitcase out of the back seat, set it down; bag on her shoulder
    MA.act(a27, a27 + 3.4, armR=lambda t, u: Vector((0.95, lerp(-35.95, -36.15, u), lerp(-0.45, -0.75, seg(t, a27 + 1.6, a27 + 3.2)))),
           armL=Vector((0.9, -36.0, -0.5)), lean=0.25, look=Vector((1.0, -35.9, -0.6)), mood=(-0.3, 0.0, 0.0))
    MA.act(a27 + 3.3, S.END, armL=("rel", 0.03, -0.06, -0.03), armR=("loc", 0.08, -0.28, 0.42),
           look=lambda t, u: Vector((1.0, -40.0, -0.2)) if t < b27 else None, mood=(-0.35, -0.1, 0.0))
    MA.act(a28 + 1.5, b28, look=Vector((0.0, 0.0, 0.6)), mood=(-0.6, -0.3, 0.0), hp=-0.04)
    S.on(MA, [27, 28])
    # Papa walks the last stretch and up the steps into the house
    PA.at(a27, 0.5, -10.5, math.pi / 2).walk(a27 + 5.4, 0.15, -3.6, mode="lin").walk(b27 - 0.2, 0.0, -0.1).walk(b27 + 1, 0.0, 1.0)
    PA.act(a27, b28, fade=0, z=hs.on_stairs(PA), armL=("rel", 0.05, 0.05, -0.32))
    S.on(PA, [27])
    # luggage
    case = props.suitcase()
    bag = props.duffel()
    case.rotation_mode = "QUATERNION"

    def case_fn(t):
        j = MA.J(t)
        if t < a27 + 3.3:
            h = j["hand"]["R"]
            return h + Vector((0, 0, -0.62)), Quaternion((0, 0, 1), j["yaw"])
        return j["hand"]["R"] + Vector((0, 0, -0.66)), Quaternion((0, 0, 1), j["yaw"] + math.pi / 2)
    bake_fn(case, a27 + 1.4, b28, case_fn, 2)
    bake_fn(case, 0, a27 + 1.39, lambda t: (Vector((1.0, -35.95, -0.75)), Quaternion((0, 0, 1), 0.0)))

    def bag_fn(t):
        j = MA.J(t)
        return j["sh_c"] + j["tl"] * (MA.sw * 1.15) - j["spine"] * 0.32, basis_quat(j["tf"], j["spine"])
    bake_fn(bag, a27, b28, bag_fn, 2)

    # cameras
    S.shoot(27, lambda t: dict(pos=FRAME27["pos"], look=FRAME27["look"], focus=12.0, fstop=5.6))

    def c28(t):
        u = seg(t, a28, b28)
        c = on(MA, b28, "MS", 85, az=-4, yaw=math.pi / 2, third=0.35)
        return push(c, 0.3 * u)
    S.shoot(28, c28)
    S.light(27, (0.2, -36.4, 0.2), key=dict(side="R", ang=40, el=60, d=4, w=80, k=6500, size=4))
    S.light(28, lambda t: head(MA, t), key=dict(side="R", ang=30, el=60, d=2.5, w=95, k=6500, size=3),
            fill=dict(side="L", ang=60, el=10, d=2.5, w=5, k=6500))
