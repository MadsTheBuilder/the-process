# Scene 10 - THE TALLY - INT. House (Mamta's Room) - Day (shots 61-70, 37 s)
# Hard afternoon sun through the west grille throws a cage of shadow on the floor. Inside the almirah's left
# door: tally marks counting months, stopping at May 12. Papa appears in the doorframe.
import math

from mathutils import Matrix, Quaternion, Vector

from kit import *
from film import *
import cast
import hs
import props
import sets
from sets import H

AX, AY = H["almirah"]
HINGE_L = Vector((AX - 0.6, AY - 0.02))
OPEN_L = -100.0


def door_point(u, z, ang=OPEN_L, out=0.03):
    """a point on the inside face of the left almirah door: u along the leaf (0 hinge .. 0.6 edge)."""
    a = math.radians(ang)
    leaf = Vector((math.cos(a), math.sin(a), 0))
    nrm = Vector((-math.sin(a), math.cos(a), 0))
    return Vector((HINGE_L.x, HINGE_L.y, z)) + leaf * u + nrm * out, nrm


def mamta_room_afternoon(S, st, t, sun=4.5):
    C = sets.mats()
    sets.sun_dir(st["L"]["Sun"], 182, 24)
    S.state(t, Sun=(sun, 5400), WinM=(110, 6200), WinCorr=(25, 6000), WinMo=(20, 6000))
    S.emit(t, C["sky_win"], 4.0)
    S.world(t, (0.42, 0.42, 0.40), 0.03)


def build(S):
    T = S.T
    a = {n: T[n][0] for n in T}
    b = {n: T[n][1] for n in T}
    st = hs.house(S)
    mamta_room_afternoon(S, st, 0)
    S.exposure(0, 0.45)
    haze, _ = fog_box("MRDust", (-4.2, 10.8, 1.6), (7.2, 6.2, 3.1), 0.012, (0.95, 0.9, 0.82), 0.5)
    hs.almirah_keys(st, left=[(0, 0, "const"), (a[62] + 0.4, 0, "bez"), (a[62] + 1.2, -OPEN_L, "const"),
                              (a[67] + 0.2, -OPEN_L, "bez"), (a[67] + 0.9, 50, "const"), (a[70] + 0.3, 50, "bez"), (a[70] + 1.1, 0, "const")],
                    right=[(0, 0, "const"), (a[62] + 0.3, 0, "bez"), (a[62] + 1.0, 95, "const")])
    MA = cast.mamta("fresh")
    PA = cast.papa()
    BED_W = Vector((-2.45, 12.55))
    FRONT = Vector((-4.45, 12.55))
    MA.at(0, -1.55, 8.6, math.pi / 2).walk(a[61] + 2.4, BED_W.x, BED_W.y - 0.6, mode="smooth").stay(b[61], 0.0)
    MA.stay(a[62] + 0.3, 0.0).walk(a[62] + 2.6, FRONT.x, FRONT.y, mode="smooth").stay(b[62], math.pi / 2)
    MA.stay(a[63] + 0.4, math.pi / 2).stay(a[63] + 1.4, math.pi - 0.35, tt=1.0).stay(b[66], math.pi - 0.35)
    MA.stay(a[67] + 0.9).stay(b[67], -math.pi / 2 + 0.6, tt=0.8).stay(b[69], -math.pi / 2 + 0.6).stay(a[70] + 0.3, math.pi - 0.35, tt=0.3).stay(b[70])
    MA.act(0, a[61] + 2.6, armR=("loc", 0.06, -0.28, 0.42), mood=(-0.5, -0.3, 0.0), look=Vector((-1.3, 12.5, 0.6)))
    MA.act(a[61] + 2.2, b[61], fade=0.5, armR=Vector((-1.75, 12.4, 0.82)), armL=Vector((-1.75, 12.8, 0.82)), lean=0.35)
    pile = lambda t, u: ("loc", 0.32, 0.0, 0.62)
    MA.act(a[62], a[62] + 3.0, armL=lambda t, u: ("rel", 0.3, 0.12, -0.15), armR=lambda t, u: ("rel", 0.3, -0.12, -0.15),
           look=Vector((AX, AY, 1.0)))
    MA.act(a[62] + 2.8, b[62], fade=0.4, armL=Vector((AX - 0.15, AY + 0.15, 1.15)), armR=Vector((AX + 0.2, AY + 0.15, 1.15)), lean=0.15)
    tally = door_point(0.3, 1.45)[0]
    MA.act(a[63] + 1.0, b[66], look=tally, mood=lambda t, u: (lerp(-0.4, -1.0, seg(t, a[63] + 1, b[64])), -0.5, 0.0), hp=0.05)
    MA.act(a[65], b[65], armL=lambda t, u: door_point(lerp(0.5, 0.15, u), 1.5 - 0.15 * u, out=0.05)[0])
    MA.act(a[66], b[66], mood=(-1.0, -0.7, 0.08), eyes=lambda t, u: 0.85 - 0.25 * u)
    MA.act(a[67], a[67] + 1.0, armL=door_point(0.5, 1.2, ang=-75, out=0.2)[0], fade=0.25)
    MA.act(a[67] + 0.7, b[69], look=Vector((-1.45, 7.6, 1.5)), mood=talk(a[69] + 0.4, b[69] - 0.4, (-0.7, -0.3)))
    MA.act(a[70], b[70], armL=lambda t, u: door_point(0.45, 1.2, ang=lerp(-50, -5, seg(t, a[70] + 0.3, a[70] + 1.1)), out=0.08)[0], fade=0.2)
    S.on(MA, [61, 62, 63, 66, 67, 69, 70])
    tear(MA, a[66] + 1.6, 2.0, side=0.5)
    # Papa in the doorframe with a prescription
    PA.at(a[67] + 0.5, -1.45, 7.45, math.pi / 2).stay(b[69])
    PA.act(a[67], b[69], armR=("rel", 0.3, -0.05, -0.08), look=lambda t, u: est(MA, t), mood=talk(a[68] + 0.4, b[68] - 0.4, (-0.5, -0.2)))
    S.on(PA, [67, 68, 69])
    rx = props.paper("Prescription")
    hold(rx, PA, "R", a[67], b[69], off=(0.02, 0, 0.02))
    vis(rx, [(a[67], b[69])])
    # suitcase onto the bed, the clothes pile into the almirah
    case = props.suitcase()
    bake_fn(case, 0, a[61] + 2.5, lambda t: (MA.J(t)["hand"]["R"] + Vector((0, 0, -0.64)), Quaternion((0, 0, 1), MA.J(t)["yaw"] + math.pi / 2)), 2)
    bake_fn(case, a[61] + 2.5, S.END, lambda t: (Vector((-1.35, 12.5, 0.56)), Quaternion((0, 1, 0), math.pi / 2)))
    pile = new_obj("ClothesPile", box_mesh("cp", 0.42, 0.34, 0.2), M((0.35, 0.25, 0.30), 0.95))
    bake_fn(pile, 0, a[62], lambda t: (Vector((-1.35, 12.2, 0.73)), Quaternion()))
    bake_fn(pile, a[62], a[62] + 3.0, lambda t: ((MA.J(t)["hand"]["L"] + MA.J(t)["hand"]["R"]) / 2 + Vector((0, 0, -0.08)),
                                                  Quaternion((0, 0, 1), MA.J(t)["yaw"])), 2)
    bake_fn(pile, a[62] + 3.0, S.END, lambda t: (Vector((AX, AY + 0.25, 1.05)), Quaternion()))
    # insert hand brushing the carvings (65)
    hh, hf, hth = props.hand("TallyHand", skin=SKIN["a"], sleeve=(0.22, 0.36, 0.40))
    props.curl(hf, [(0, 0.15)])

    def hand_fn(t):
        u = seg(t, a[65], b[65])
        p, nrm = door_point(lerp(0.52, 0.12, u), lerp(1.58, 1.38, u), out=0.035)
        leaf = Vector((math.cos(math.radians(OPEN_L)), math.sin(math.radians(OPEN_L)), 0))
        # fingers point along -leaf (toward the hinge), palm faces the door (-nrm)
        y = -leaf
        z = nrm
        x = y.cross(z)
        q = Matrix((x, y, z)).transposed().to_quaternion()
        return p - y * 0.09, q
    bake_fn(hh, a[65], b[65], hand_fn)
    vis_tree(hh, [(a[65], b[65])])

    # cameras
    S.shoot(61, lambda t: dict(pos=Vector((-7.45, 8.05, 1.75)), look=Vector((-2.9, 12.4, 0.95)), focus=5.5, fstop=5.6))
    S.shoot(62, lambda t: dict(pos=Vector((-2.2, 10.1, 1.5)), look=head(MA, t) + Vector((0, 0, -0.3)), focus=(head(MA, t) - Vector((-2.2, 10.1, 1.5))).length, fstop=2.8))

    def c63(t):
        return on(MA, b[63], "MCU", 85, yaw=math.pi - 0.35, az=55, third=-0.3, tt=b[63])
    S.shoot(63, c63)

    def c64(t):                                   # macro: slow tilt down the carvings (F, M, A, M-12)
        u = seg(t, a[64], b[64])
        p, nrm = door_point(0.36, lerp(1.72, 1.13, u))
        pos = p + nrm * 0.86 + Vector((0, 0, 0.02))
        return dict(pos=pos, look=p, focus=0.86, fstop=5.6)
    S.shoot(64, c64)

    def c65(t):
        p, nrm = door_point(0.32, 1.47)
        pos = p + nrm * 0.8 + Vector((0.0, 0, 0.12))
        return dict(pos=pos, look=p, focus=0.82, fstop=5.6)
    S.shoot(65, c65)
    S.shoot(66, lambda t: on(MA, a[66] + 1, "CU", 85, yaw=math.pi - 0.35, az=40, tt=a[66]))
    S.shoot(67, lambda t: dict(pos=Vector((-2.6, 11.1, 1.45)), look=Vector((-4.6, 12.75, 1.2)), focus=2.5, fstop=4.0))
    S.shoot(68, lambda t: on(PA, a[68] + 1, "MS", 50, yaw=math.pi / 2, az=8, tt=a[68]))
    S.shoot(69, lambda t: on(MA, a[69] + 0.5, "MCU", 85, yaw=-math.pi / 2 + 0.6, az=10, tt=a[69]))
    S.shoot(70, lambda t: dict(pos=Vector((-3.3, 11.4, 1.35)), look=Vector((AX - 0.35, AY - 0.25, 1.15)), focus=2.2, fstop=4.0))
    W = 5600
    S.light(61, (-2.8, 12.4, 1.0), key=dict(side="L", ang=60, el=25, d=3, w=40, k=W, size=1.5))
    S.light(62, lambda t: head(MA, t), key=dict(side="L", ang=70, el=25, d=2.5, w=40, k=W, size=1.2))
    S.light(63, lambda t: head(MA, t), key=dict(side="R", ang=80, el=18, d=1.8, w=70, k=W, size=0.8), fill=dict(side="L", ang=40, el=10, d=2, w=10, k=W))
    S.light(64, door_point(0.3, 1.4)[0], key=dict(side="L", ang=84, el=14, d=0.7, w=45, k=W, size=0.05), fill=dict(side="R", ang=30, el=10, d=1.0, w=3, k=W))
    S.light(65, door_point(0.3, 1.4)[0], key=dict(side="L", ang=84, el=14, d=0.7, w=45, k=W, size=0.05), fill=dict(side="R", ang=30, el=10, d=1.0, w=3, k=W))
    S.light(66, lambda t: head(MA, t), key=dict(side="R", ang=75, el=18, d=1.8, w=70, k=W, size=0.8), kick=dict(side="L", ang=10, el=5, d=1.2, w=2, k=W))
    S.light(67, lambda t: head(MA, t), key=dict(side="R", ang=60, el=20, d=2.4, w=50, k=W, size=1.0))
    S.light(68, lambda t: head(PA, t), rim=dict(side="L", ang=160, el=20, d=1.6, w=60, k=6000, size=1.0), key=dict(side="R", ang=40, el=20, d=2, w=10, k=W))
    S.light(69, lambda t: head(MA, t), key=dict(side="L", ang=80, el=18, d=1.8, w=60, k=W, size=0.8))
    S.light(70, (AX - 0.3, AY - 0.3, 1.2), key=dict(side="L", ang=80, el=15, d=1.5, w=40, k=W, size=0.3))
