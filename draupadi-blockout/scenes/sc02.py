# Scene 2 - THE SUMMONS - INT. Outside Staff Room - Day (shots 17-26, 41 s)
# The veranda corridor runs north-south (x ~110.3). Classroom door at y 10.55, staff-room door at y 17.5 (west side).
# Hard morning sun from the east-south-east cuts through the columns: pools of light and shadow on the floor.
import math

from mathutils import Quaternion, Vector

from kit import *
from film import *
import cast
import sets
from sets import S as SC


def books_at_chest(a, side_sep=0.0):
    def fn(t):
        j = a.J(t)
        p = (j["hand"]["L"] + j["hand"]["R"]) / 2 + j["tf"] * 0.03
        q = basis_quat(j["tl"], j["spine"])
        return p, q
    return fn


def build(S):
    T = S.T
    E = S.END
    C = sets.mats()
    set_ = sets.build_school(E)
    L = set_["L"]
    S.world(0, (0.55, 0.6, 0.68), 0.22)
    sets.sun_dir(L["S_Sun"], -22, 28)
    S.state(0, S_Sun=(5.5, 5800), S_Sky=0, S_Yard=(350, 6200), S_ArchS=(1400, 6000), S_ArchN=(900, 6000),
            S_StaffWin=(420, 5600), **{"S_Win%d" % i: (150, 5800) for i in range(3)})
    S.emit(0, C["sky_win"], 7.0)
    S.exposure(0, -0.55)
    haze, _ = fog_box("CorrHaze", (110.6, 14, 1.7), (3.6, 56, 3.4), 0.01, (0.9, 0.9, 0.88))

    MA = cast.mamta("school")
    PA = cast.papa()
    X0 = 110.25
    a17, b17 = T[17]
    a18, b18 = T[18]
    a19, b19 = T[19]
    a20, b20 = T[20]
    a21, b21 = T[21]
    a22, b22 = T[22]
    a23, b23 = T[23]
    a24, b24 = T[24]
    a25, b25 = T[25]
    a26, b26 = T[26]
    N, Sd = math.pi / 2, -math.pi / 2
    STOP = Vector((109.95, 16.75))               # her feet stop on the edge of the light at the threshold
    # walk up the corridor to the staff room
    MA.at(a17, X0, 10.9, N).walk(b17, X0 - 0.1, 16.1, yaw=N).walk(a18 + 1.0, STOP.x, STOP.y, yaw=math.radians(120), mode="smooth")
    MA.stay(b19, math.radians(150))
    # 20: turns away, leans on the wall beside the door (back to the wall, facing east), then walks off south
    WALL = Vector((109.38, 16.25))
    MA.walk(a20 + 1.2, WALL.x, WALL.y, yaw=0.0, mode="smooth", gait="walk").stay(a20 + 4.3, 0.0)
    MA.walk(b20, X0, 15.2, yaw=Sd, mode="smooth").walk(b21, X0, 12.4, yaw=Sd).walk(a22 + 0.3, X0, 12.05, yaw=Sd, mode="smooth")
    MA.stay(a22 + 0.8, Sd).stay(b22 - 0.3, N, tt=1.6).stay(b26, N)
    # Papa: seated in the staff room, back to the door (19); at the door when he calls (21); walks to her (23)
    SEAT = SC["staff_seat"]
    PA.at(0, SEAT.x, SEAT.y, math.pi).stay(b19)
    PA.at(b20, 109.7, 17.45, Sd).stay(a23).walk(b23 - 0.4, X0, 13.15, yaw=Sd, mode="smooth").stay(b26, Sd)
    PA.act(0, b19 + 0.01, fade=0, sit=1.0, seat=0.45, hp=0.25, armL=("rel", 0.3, 0.05, -0.12), armR=("rel", 0.3, -0.05, -0.12))
    books = lambda t, u: None
    MA.act(a17, a24 + 0.6, armL=("rel", 0.17, -0.1, -0.13), armR=("rel", 0.17, 0.1, -0.13), mood=(-0.15, 0.1, 0.0),
           look=lambda t, u: Vector((109.6, 17.5, 1.3)) if t < a19 else None)
    MA.act(a18 + 0.6, b19, look=Vector((106.0, 17.4, 1.1)), mood=(-0.6, -0.4, 0.05), hp=0.05)
    MA.act(a20 + 1.1, a20 + 4.4, fade=0.5, roll=0.06, hp=0.22, eyes=lambda t, u: 0.3 if 0.3 < u < 0.7 else 1.0,
           mood=(-0.7, -0.5, 0.15), lean=-0.05, bob=0.01, bobf=0.35)
    MA.act(a20 + 4.2, b21, mood=(-0.6, -0.4, 0.0), hp=0.1)
    MA.act(a21 + 1.6, b22, mood=(-0.8, -0.5, 0.05), eyes=lambda t, u: 1.0)
    MA.act(a23, b23, look=lambda t, u: est(PA, t), mood=(-0.8, -0.6, 0.05))
    # 24: she bends and touches his feet
    feet = lambda t, u: Vector((X0, 13.0, 0.08))
    MA.act(a24 + 0.9, b24 - 0.2, fade=0.7, lean=1.25, crouch=0.24, armL=feet, armR=feet, look=Vector((X0, 13.1, 0.0)), hp=0.5)
    MA.act(b24 - 0.4, b26, fade=0.4, look=lambda t, u: head(PA, t), mood=lambda t, u: (-0.9, -0.6, talk(a25 + 0.3, b25 - 0.2)(t, u)[2] + 0.05),
           armL=("rel", 0.12, -0.03, -0.25), armR=("rel", 0.12, 0.03, -0.25))
    PA.act(b20, b21, mood=talk(a21 + 0.6, a21 + 1.6, (-0.7, -0.3)), look=lambda t, u: est(MA, t), armR=("rel", 0.18, -0.12, -0.05))
    PA.act(a23, b26, look=lambda t, u: est(MA, t) if t < a24 + 0.8 or t > b24 - 0.4 else Vector((X0, 12.6, 0.6)),
           mood=lambda t, u: (-0.9, -0.5, talk(a24 + 0.2, a24 + 0.9)(t, u)[2] + talk(a26 + 0.2, b26 - 0.4)(t, u)[2]),
           hp=lambda t, u: 0.25 if a24 + 0.8 < t < b24 - 0.4 else 0.0,
           armR=lambda t, u: ("rel", 0.12, -0.04, -0.15 + 0.25 * seg(t, a24 + 1.6, a24 + 2.2)) if a24 < t < b24 else ("rel", 0.05, -0.05, -0.3))
    S.on(MA, list(range(17, 27)))
    S.on(PA, [19, 23, 24, 25, 26])
    PA.bake(b20, b21)
    # her books, held against the chest
    bk = new_obj("Books", box_mesh("bks", 0.25, 0.06, 0.32, False), M((0.22, 0.18, 0.28), 0.8))
    bake_fn(bk, a17, a24 + 0.7, books_at_chest(MA), 1)
    vis(bk, [(a17, a24 + 0.7)])
    sd_ = set_["P"]["staff_door"]
    keys(sd_, "rotation_euler", 2, [(0, math.radians(-75))])

    # ------------------------------------------------------------------ cameras
    def c17(t):                                    # gimbal lead: backs up ahead of her
        h = chest(MA, t)
        pos = h + Vector((0.35, 2.4, 0.25))
        return dict(pos=pos, look=h + Vector((0, 0, 0.12)), focus=(h - pos).length, fstop=2.8)
    S.shoot(17, c17)
    S.shoot(18, lambda t: dict(pos=Vector((111.05, 17.3, 0.22)), look=Vector((STOP.x, STOP.y, 0.06)), focus=1.25, fstop=2.8))
    S.shoot(19, lambda t: dict(pos=Vector((110.05, 17.35, 1.5)), look=Vector((106.3, 17.45, 1.05)), focus=3.9, fstop=2.8))
    S.shoot(20, lambda t: frame(chest(MA, a20 + 2.5) + Vector((0, 0, 0.05)), 0.0, 50, "MS", az=-88, up=0.05, third=0.5))
    S.shoot(21, lambda t: dict(pos=Vector((X0 + 0.25, 17.9, 1.55)), look=Vector((X0, 6.0, 1.15)), focus=4.5, fstop=4.0))
    S.shoot(22, lambda t: frame(eyes(MA, b22), N, 85, "MCU", az=0.0, up=-0.06, third=0.4))

    def c23(t):
        pos = Vector((X0 + 0.75, 10.6, 1.5))
        p = head(PA, t)
        return dict(pos=pos, look=p + Vector((0, 0, -0.18)), focus=(p - pos).length)
    S.shoot(23, c23)
    S.shoot(24, lambda t: dict(pos=Vector((111.15, 8.4, 1.25)), look=Vector((X0, 12.7, 1.0)), focus=4.3))
    S.shoot(25, lambda t: ots(PA, MA, t, 85, side=1, out_=0.3))
    S.shoot(26, lambda t: ots(MA, PA, t, 85, side=-1, out_=0.3))

    # ------------------------------------------------------------------ lights per shot
    W = 6000
    S.light(17, lambda t: head(MA, t), key=dict(side="R", ang=70, el=20, d=3, w=40, k=W, size=2))
    S.light(18, (STOP.x, STOP.y, 0.05), kick=dict(side="R", ang=80, el=12, d=1.5, w=0))
    S.light(19, (106.2, 17.4, 1.1), rim=dict(side="L", ang=165, el=20, d=1.6, w=60, k=5600, size=1.0))
    S.light(20, lambda t: head(MA, t), key=dict(side="R", ang=120, el=15, d=1.8, w=45, k=W, size=0.6))
    S.light(21, lambda t: head(MA, t), key=dict(side="L", ang=150, el=20, d=3, w=0))
    S.light(22, lambda t: head(MA, t), key=dict(side="R", ang=70, el=15, d=2.0, w=90, k=W, size=1.2),
            fill=dict(side="L", ang=50, el=10, d=2.0, w=12, k=W))
    S.light(23, lambda t: head(PA, b23), key=dict(side="R", ang=35, el=25, d=2.2, w=110, k=5600, size=1.4),
            fill=dict(side="L", ang=50, el=10, d=2.2, w=28, k=5600))
    S.light(24, lambda t: mid(head(MA, t), head(PA, t)), key=dict(side="L", ang=20, el=70, d=2.5, w=120, k=5600, size=2.0),
            fill=dict(side="R", ang=40, el=10, d=2.5, w=35, k=5600))
    S.light(25, lambda t: head(MA, t), key=dict(side="R", ang=50, el=18, d=1.8, w=110, k=5600, size=1.2),
            fill=dict(side="L", ang=40, el=8, d=2.0, w=22, k=5600))
    S.light(26, lambda t: head(PA, t), key=dict(side="L", ang=35, el=18, d=1.8, w=70, k=6200, size=1.6),
            fill=dict(side="R", ang=40, el=8, d=2.0, w=20, k=6200))
    # threshold slash: a hard narrow spot across the floor at the staff door (shot 18)
    sl = lamp("ThresholdSlash", "SPOT", (112.6, 14.2, 3.4), 0, kelvin(5800), size=0.02, spot=7)
    aim(sl, (STOP.x, STOP.y + 0.35, 0.0))
    S.state(0, ThresholdSlash=0)
    S.state(a18, ThresholdSlash=(2600, 5800))
    S.state(b18, ThresholdSlash=0)
