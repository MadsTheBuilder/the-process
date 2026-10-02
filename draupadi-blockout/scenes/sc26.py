# Scene 26 - BLUE WALLS - INT. House (Mother's Room) - Night (shots 184-186, 16 s)
# The first calm image of the house: moonlight on the blue walls. The toppled steel jug and glass (planted in 110)
# have spilled water that throws rippling caustics on the walls - and across her face, turning into the river.
import math

from mathutils import Quaternion, Vector

from kit import *
from film import *
import cast
import hs
import props
import sets
from sets import H
from scenes.sc08 import mother_in_bed

CH = H["mo_chair"]
SIDE_T = H["mo_side"]


def build(S):
    T = S.T
    a = {n: T[n][0] for n in T}
    b = {n: T[n][1] for n in T}
    E = S.END
    st = hs.house(S)
    C = sets.mats()
    sets.sun_dir(st["L"]["Moon"], 8, 22)
    S.state(0, Moon=(1.6, 7200), WinMo=(150, 7500), MoBounce=(20, 7000))
    S.emit(0, C["sky_win"], 0.5)
    S.world(0, (0.02, 0.03, 0.07), 0.03)
    S.exposure(0, 1.0)
    caustics(C["wall_mother"], 0, E, strength=0.05, scale=3.0, name="CW")
    MO = cast.mother()
    mother_in_bed(MO, 0, E)
    MO.act(0, E, eyes=0.1, hp=0.4)
    MA = cast.mamta("night")
    MA.at(0, CH.x, CH.y, 0.15).stay(E)
    MA.act(0, E, fade=0, sit=1.0, seat=0.47, look=Vector((7.95, 11.5, 1.6)), mood=(-0.3, 0.0, 0.0), eyes=0.9,
           armL=("rel", 0.2, 0.05, -0.33), armR=("rel", 0.2, -0.05, -0.33))
    S.on(MO, [184, 185, 186], step=6)
    S.on(MA, [184, 185, 186], step=3)
    caustics(M(SKIN["a"], 0.7), a[186], b[186], strength=0.1, scale=8.0, name="CF")
    # the spill: jug and glass on their sides, a sheet of water on the floor
    jug, gl = st["P"]["jug"], st["P"]["glass"]
    jug.location = (SIDE_T.x - 0.2, SIDE_T.y - 0.35, 0.07)
    jug.rotation_euler = (math.pi / 2, 0, 0.7)
    gl.location = (SIDE_T.x - 0.55, SIDE_T.y - 0.6, 0.035)
    gl.rotation_euler = (math.pi / 2, 0, -0.4)
    puddle = new_obj("Puddle", sphere_mesh("pd", 0.55, 20, 6, (1.3, 0.8, 0.004)), M((0.02, 0.03, 0.04), 0.02), loc=(SIDE_T.x - 0.45, SIDE_T.y - 0.5, 0.004))
    caustics(puddle.data.materials[0], 0, E, strength=0.12, scale=9.0, name="CP")
    S.shoot(184, lambda t: dict(pos=Vector((5.0, 8.25, 1.6)), look=Vector((6.3, 12.6, 0.8)), focus=4.6, fstop=5.6))
    S.shoot(185, lambda t: dict(pos=Vector((SIDE_T.x - 1.1, SIDE_T.y - 1.4, 1.45)), look=Vector((SIDE_T.x - 0.4, SIDE_T.y - 0.45, 0.1)), focus=1.8, fstop=4.0))
    S.shoot(186, lambda t: push(on(MA, t, "CU", 85, yaw=0.15, az=18, tt=a[186]), 0.18 * seg(t, a[186], b[186])))
    S.light(184, (6.2, 12.5, 0.8), key=dict(side="R", ang=60, el=30, d=3, w=20, k=7500, size=2))
    S.light(185, (SIDE_T.x - 0.4, SIDE_T.y - 0.45, 0.1), kick=dict(side="R", ang=60, el=40, d=1.2, w=30, k=7500))
    S.light(186, lambda t: head(MA, t), key=dict(side="R", ang=50, el=15, d=1.6, w=25, k=7500, size=1.0))
