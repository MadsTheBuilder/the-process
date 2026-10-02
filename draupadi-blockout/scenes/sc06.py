# Scene 6 - FLASH: LOCKED IN - INT. House (Mamta's Room) - Day (shots 38-42, 19 s)
# Through the internal bars: ten years earlier, young pregnant Mamta scratches tally marks inside the almirah door
# under a sick green-cold window light. She shuts the door, turns and stares into the lens. Present Mamta recoils.
import math

from mathutils import Quaternion, Vector

from kit import *
from film import *
import cast
import hs
import props
import sets
from sets import H
from scenes.sc05 import corridor_day, carry, WIN_X, BAR_Y


def build(S):
    T = S.T
    st = hs.house(S)
    a38, b38 = T[38]
    a39, b39 = T[39]
    a40, b40 = T[40]
    a41, b41 = T[41]
    a42, b42 = T[42]
    C = sets.mats()
    hs.door_keys(st, [(0, 35, "const")])
    # flash light: the room under a green gel, hard key from the window behind the almirah door
    S.state(0, WinM=(260, 6000, GREEN), WinCorr=(25, 6000), WinMo=0, WinDR1=0, WinDR2=0)
    sets.sun_dir(st["L"]["Sun"], 165, 22)
    S.state(0, Sun=(2.6, 6000, GREEN))
    S.emit(0, C["sky_win"], 2.0)
    S.world(0, (0.25, 0.32, 0.26), 0.03)
    S.exposure(0, 0.3)
    corridor_day(S, st, a41)
    S.state(a41, Sun=0)
    ax, ay = H["almirah"]
    hs.almirah_keys(st, left=[(0, 100, "const"), (a39 + 0.6, 100, "bez"), (a39 + 1.5, 0, "const")],
                    right=[(0, 62, "const")])
    YM = cast.young_mamta("pregnant")
    SPOT = Vector((ax - 0.32, ay - 0.5))
    YM.at(0, SPOT.x, SPOT.y, math.pi - 0.15).stay(a39 + 0.4).stay(a39 + 1.6, math.pi - 0.15)
    YM.stay(a39 + 2.6, -math.pi / 2 - 0.5, tt=1.0).stay(a40 + 0.15).stay(a40 + 0.55, -math.pi / 2 + 0.08, tt=0.35).stay(b40)
    scrape = lambda t, u: Vector((ax - 0.52 + 0.012 * math.sin(t * 18), ay - 0.42 + 0.015 * math.sin(t * 9), 1.35 + 0.02 * math.sin(t * 18)))
    YM.act(0, a39 + 0.5, armR=scrape, armL=("rel", 0.25, 0.05, -0.18), look=Vector((ax - 0.55, ay - 0.4, 1.35)),
           mood=(-0.8, -0.5, 0.1), hp=0.15)
    YM.act(a39 + 0.3, a39 + 1.6, fade=0.3, armR=Vector((ax - 0.62, ay - 0.35, 1.0)), look=Vector((ax - 0.55, ay - 0.2, 1.1)))
    YM.act(a39 + 1.5, b40, armR=("rel", 0.2, -0.05, -0.22), armL=("rel", 0.22, 0.05, -0.2), mood=(-0.9, -0.6, 0.0))
    YM.act(a40 + 0.2, b40, look=Vector((WIN_X, BAR_Y, 1.5)), mood=(-1.0, -0.4, 0.0))
    S.on(YM, [38, 39, 40])
    sw = props.sweater()
    hold(sw, YM, "L", a38, b40, off=(0.02, 0.0, 0.04), step=2)
    nd = props.needle()
    hold(nd, YM, "R", a38, b40, off=(0.0, 0.0, 0.0), step=1)
    for ob in (sw, nd):
        vis_tree(ob, [(a38, b40)])
    # present Mamta at the bars (41) then hurries away east (42)
    MA = cast.mamta("home")
    MA.at(a41, WIN_X + 0.05, 7.22, math.pi / 2).walk(a41 + 0.5, WIN_X + 0.1, 6.9, yaw=math.pi / 2, mode="smooth", gait="stand")
    MA.stay(b41).at(a42, -6.4, 6.85, 0.0).walk(b42, -0.6, 6.7, gait="run")
    MA.act(a41, b41, armL=lambda t, u: Vector((WIN_X + 0.05, BAR_Y - 0.04, 1.42)) if t < a41 + 0.3 else ("rel", 0.18, 0.05, -0.05),
           mood=(-0.2, -0.8, 0.4), lean=-0.12, hp=-0.05, look=Vector((WIN_X - 0.2, 12.0, 1.4)))
    MA.act(a42, b42, armR=("loc", 0.1, -0.28, 0.42), mood=(-0.8, -0.6, 0.2))
    S.on(MA, [41, 42])
    carry(S, MA, a42, b42)
    # foreground bars glued in front of the lens for 40 (her stare through the window)
    cam = S.cam or Cam()
    S.cam = cam
    fg = empty("FGBars", (0, 0, 0))
    for i in range(-4, 5):
        new_obj("fgbar", cyl_mesh("fb", 0.0035, 0.6, 6), C["black"], fg, loc=(i * 0.026 + 0.004, 0, -0.3))
    fg.parent = cam.ob
    fg.location = (0.0, 0.0, -0.22)
    fg.rotation_euler = (math.pi / 2, 0, 0)
    vis_tree(fg, [(a40, b40)])

    # cameras
    POVP = Vector((WIN_X - 0.05, BAR_Y - 0.3, 1.5))
    S.shoot(38, lambda t: dict(pos=POVP, look=Vector((ax - 0.2, ay - 0.5, 1.15)), focus=5.6, fstop=11.0))
    S.shoot(39, lambda t: dict(pos=Vector((ax + 2.6, ay - 1.25, 1.05)), look=Vector((ax - 0.3, ay - 0.45, 0.95)), focus=3.0, fstop=2.8))
    S.shoot(40, lambda t: on(YM, b40, "CU", 85, yaw=-math.pi / 2, az=0, tt=b40))
    S.shoot(41, lambda t: on(MA, a41 + 0.3, "CU", 85, yaw=-math.pi / 2, az=180, tt=a41))
    S.shoot(42, lambda t: dict(pos=Vector((-7.55, 6.95, 1.6)), look=Vector((-1.0, 6.7, 1.15)), focus=4.0, fstop=4.0))
    G = GREEN
    S.light(38, lambda t: head(YM, t), key=dict(side="L", ang=120, el=25, d=2.0, w=120, k=6000, tint=G, size=0.5))
    S.light(39, lambda t: chest(YM, t), key=dict(side="R", ang=75, el=25, d=2.0, w=320, k=6000, tint=G, size=0.6),
            fill=dict(side="L", ang=40, el=10, d=2.5, w=25, k=6000, tint=G))
    S.light(40, lambda t: head(YM, t), key=dict(side="L", ang=8, el=12, d=2.0, w=120, k=6000, tint=G, size=0.8))
    S.light(41, lambda t: head(MA, t), key=dict(side="L", ang=110, el=15, d=1.6, w=50, k=6000, size=0.5))
    S.light(42, (-3.5, 6.8, 1.4), key=dict(side="L", ang=60, el=30, d=3, w=10, k=6000))
