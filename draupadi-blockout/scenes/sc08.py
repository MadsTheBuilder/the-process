# Scene 8 - THE CHAIN - INT. House (Mother's Room) - Day (shots 49-58, 36 s)
# Mother lies in the bed in the NE corner (head north). One curtained window (east) - soft, cool, sickroom pale
# on muted blue walls. Her hand on Mamta's wrist becomes, for a cut, a heavy chain.
import math

from mathutils import Matrix, Quaternion, Vector

from kit import *
from film import *
import cast
import hs
import props
import sets
from sets import H

HIP = Vector((6.9, 13.02))
DOOR = Vector((2.5, 7.6))
SIDE = Vector((5.98, 13.0))           # where Mamta stands at the bedside (facing east)


def mother_in_bed(MO, t0, t1, blanket=True):
    MO.at(t0, HIP.x, HIP.y, -math.pi / 2).stay(t1)
    MO.act(t0, t1, fade=0, lie=1.0, bed=0.49, hp=0.42, armL=("rel", -0.02, -0.06, -0.3), armR=("rel", -0.02, 0.06, -0.3),
           eyes=0.75, mood=(-0.2, 0.0, 0.0))
    if blanket:
        b = new_obj("Blanket", box_mesh("bl", 1.34, 1.3, 0.12), sets.mats()["blanket"], loc=(HIP.x, 12.62, 0.49))
        return b


def mo_room_day(S, t, win=170, k=6000):
    C = sets.mats()
    S.state(t, WinMo=(win * 2.3, k), MoBounce=(60, k), WinCorr=(60, 6000), WinDR1=(40, 5600), WinDR2=(40, 5600))
    S.emit(t, C["sky_win"], 3.0)
    S.world(t, (0.35, 0.4, 0.48), 0.03)


def build(S):
    T = S.T
    st = hs.house(S)
    mo_room_day(S, 0)
    S.exposure(0, 0.5)
    a = {n: T[n][0] for n in T}
    b = {n: T[n][1] for n in T}
    MO = cast.mother()
    mother_in_bed(MO, 0, S.END)
    MA = cast.mamta("home")
    PA = cast.papa()
    E = math.pi / 2 * 0
    door_look = Vector((DOOR.x, DOOR.y - 0.3, 1.5))
    # Mother: smile spreads (49), beckons (50), reaches and holds the wrist (51-52), hurt (55), eyes to the door (58)
    MO.act(0, b[49], look=door_look, mood=lambda t, u: (0.2, lerp(0.0, 1.0, seg(t, a[49] + 1.5, b[49] - 0.5)), 0.05))
    beckon = lambda t, u: Vector((6.2, 12.9, 0.95 + 0.06 * math.sin(t * 7)))
    MO.act(a[50], b[50], look=door_look, armR=beckon, mood=(0.3, 0.9, 0.1))
    wrist = lambda t, u: MA.J(t)["wrist"]["R"] + Vector((0, 0, -0.02))
    MO.act(a[51] + 2.6, a[54] + 0.25, fade=0.6, armR=wrist, look=lambda t, u: est(MA, t) + Vector((0, 0, -0.1)), mood=(0.2, 0.7, 0.0))
    MO.act(a[54] + 0.25, b[56], fade=0.25, look=lambda t, u: est(MA, t), mood=(-0.7, -0.4, 0.12),
           armR=lambda t, u: Vector((6.32, 13.0, 0.7)) if t < a[56] + 2.0 else Vector((6.6, 12.8, 0.55)))
    MO.act(a[58], b[58], look=lambda t, u: door_look if (t - a[58]) % 1.6 < 0.9 else est(MA, t), mood=(0.0, 0.3, 0.0))
    # Mamta
    MA.at(0, DOOR.x, DOOR.y - 0.25, math.pi / 2).stay(a[51]).walk(a[51] + 2.6, SIDE.x, SIDE.y, mode="smooth").stay(a[51] + 3.0, 0.0)
    MA.stay(a[54]).walk(a[54] + 0.35, SIDE.x - 0.18, SIDE.y, yaw=0.0, gait="stand").stay(a[56])
    CH = H["mo_chair"]
    MA.walk(a[56] + 1.2, CH.x, CH.y, yaw=0.0, mode="smooth").stay(b[58] - 1.6).walk(b[58], 4.6, 11.2, mode="smooth")
    MA.act(0, a[51] + 3.0, mood=(-0.4, -0.2, 0.0), look=lambda t, u: est(MO, t) + Vector((0, 0.7, -0.9)))
    MA.act(a[51] + 2.4, a[54] + 0.1, fade=0.5, armR=Vector((6.18, 13.0, 0.88)), look=Vector((6.4, 13.3, 0.7)), mood=(-0.6, -0.3, 0.0))
    MA.act(a[54], a[54] + 0.6, fade=0.12, armR=("rel", 0.05, 0.05, -0.2), lean=-0.15, mood=(-0.9, -0.6, 0.2))
    MA.act(a[56] + 1.0, b[58] - 1.6, sit=1.0, seat=0.47, look=lambda t, u: est(MO, t) + Vector((0, 0.7, -0.9)), mood=talk(a[56] + 3.0, b[56] - 0.2, (-0.5, -0.3)))
    MA.act(a[56] + 1.5, a[56] + 3.2, armR=Vector((6.45, 12.95, 0.62)), armL=Vector((6.4, 12.75, 0.62)), lean=0.4)
    MA.act(a[57], b[57], look=Vector((DOOR.x, DOOR.y, 1.5)))
    MA.act(a[58] + 1.4, a[58] + 2.6, hp=lambda t, u: 0.25 * math.sin(u * math.pi * 2) ** 2)
    S.on(MO, list(range(49, 59)), step=2)
    S.on(MA, [49, 51, 54, 56, 57, 58])
    # Papa at the door: sighs, leaves
    PA.at(a[57], DOOR.x + 0.1, DOOR.y - 0.3, math.pi / 2).stay(a[57] + 1.8).walk(b[57] + 0.4, DOOR.x + 1.4, DOOR.y - 0.85, mode="smooth")
    PA.act(a[57], b[57], mood=(-0.8, -0.5, 0.0), look=Vector((6.5, 12.5, 0.8)), bob=lambda t, u: 0.012 * math.sin(u * math.pi) if u < 0.5 else 0.0, bobf=0.0,
           hp=lambda t, u: 0.15 * seg(t, a[57] + 0.8, a[57] + 1.6))
    S.on(PA, [57])

    # inserts 52/53: Mother's frail hand around Mamta's wrist -> a heavy chain
    ROOT = Vector((6.2, 12.98, 0.86))
    arm = new_obj("InsArm", capsule_mesh("ia", 0.34, 0.026), M(SKIN["a"], 0.55), loc=ROOT + Vector((-0.27, 0, 0)), rot=(0, math.pi / 2, 0))
    new_obj("InsSleeve", capsule_mesh("isl", 0.18, 0.034), M((0.22, 0.30, 0.18), 0.9), loc=ROOT + Vector((-0.42, 0, 0)), rot=(0, math.pi / 2, 0))
    ahand, af, ath = props.hand("InsMamtaHand", skin=SKIN["a"])
    ahand.location = ROOT + Vector((0.07, 0, 0))
    ahand.rotation_euler = Matrix(((0, 1, 0), (-1, 0, 0), (0, 0, 1))).to_euler()
    props.curl(af, [(0, 0.35)])
    mh, mf, mth = props.hand("InsMotherHand", skin=SKIN["c"], scale=0.95)
    mh.location = ROOT + Vector((0.02, 0.07, 0.035))
    mh.rotation_euler = Matrix(((1, 0, 0), (0, 0, -1), (0, 1, 0))).to_euler() @ Matrix() if False else (math.radians(-100), 0, math.radians(180))
    props.curl(mf, [(0, 0.75)])
    ch = props.chain()
    ch.location = ROOT + Vector((0.0, 0, 0.0))
    for ob in (arm, ahand):
        vis_tree(ob, [(a[52], b[53])])
    vis(bpy_obj("InsSleeve"), [(a[52], b[53])])
    vis_tree(mh, [(a[52], b[52])])
    vis_tree(ch, [(a[53], b[53])])

    # cameras
    S.shoot(49, lambda t: dict(pos=Vector((DOOR.x - 0.15, DOOR.y - 0.6, 1.5)), look=Vector((6.2, 12.9, 0.8)), focus=6.6, fstop=4.0))
    S.shoot(50, lambda t: dict(pos=Vector((5.35, 12.85, 1.38)), look=head(MO, a[50] + 1) + Vector((0, -0.12, -0.05)), focus=1.85, fstop=2.0))
    S.shoot(51, lambda t: dict(pos=Vector((4.45, 10.9, 1.45)), look=Vector((6.35, 13.05, 0.8)), focus=2.9, fstop=2.8))
    INS = lambda t: dict(pos=ROOT + Vector((-0.15, -0.82, 0.32)), look=ROOT + Vector((0.03, 0.0, 0.0)), focus=0.9, fstop=4.0)
    S.shoot(52, INS)
    S.shoot(53, INS)
    S.shoot(54, lambda t: on(MA, a[54], "MS", 50, yaw=0.0, az=-80, third=0.2, tt=a[54]))
    S.shoot(55, lambda t: dict(pos=Vector((5.55, 13.2, 1.3)), look=head(MO, t) + Vector((0, -0.05, -0.05)), focus=1.5, fstop=2.0))
    S.shoot(56, lambda t: dict(pos=Vector((4.3, 11.0, 1.35)), look=Vector((6.0, 12.8, 0.75)), focus=2.6, fstop=2.8))
    S.shoot(57, lambda t: dict(pos=Vector((5.4, 11.9, 1.45)), look=Vector((DOOR.x + 0.1, DOOR.y - 0.3, 1.3)), focus=5.3, fstop=2.8))
    S.shoot(58, lambda t: dict(pos=Vector((5.6, 13.25, 1.28)), look=head(MO, t) + Vector((0, -0.05, -0.05)), focus=1.5, fstop=2.0))
    # lights: soft curtained window from above the bed, weak catchlights
    W = 6000
    S.light(49, (6.9, 13.6, 0.7), key=dict(side="R", ang=60, el=40, d=2.0, w=45, k=W, size=1.2))
    S.light(50, lambda t: head(MO, t), key=dict(side="R", ang=40, el=55, d=1.5, w=40, k=W, size=1.2), fill=dict(side="L", ang=40, el=20, d=1.6, w=10, k=W))
    S.light(51, lambda t: mid(head(MO, t), head(MA, t)), key=dict(side="R", ang=70, el=30, d=2.0, w=55, k=W, size=1.2))
    S.light(52, ROOT, key=dict(side="R", ang=60, el=40, d=1.0, w=18, k=W, size=0.8), fill=dict(side="L", ang=40, el=20, d=1.0, w=4, k=W))
    S.light(53, ROOT, key=dict(side="R", ang=85, el=15, d=0.8, w=30, k=6500, size=0.08), kick=dict(side="L", ang=60, el=30, d=0.6, w=8, k=7000))
    S.light(54, lambda t: head(MA, t), key=dict(side="R", ang=70, el=25, d=2.0, w=50, k=W, size=1.2))
    S.light(55, lambda t: head(MO, t), key=dict(side="R", ang=40, el=45, d=1.4, w=40, k=W, size=1.0), fill=dict(side="L", ang=40, el=10, d=1.4, w=10, k=W))
    S.light(56, lambda t: head(MA, t), key=dict(side="L", ang=110, el=25, d=2.0, w=45, k=W, size=1.2), fill=dict(side="R", ang=40, el=10, d=2.0, w=8, k=W))
    S.light(57, (DOOR.x, DOOR.y - 0.3, 1.5), rim=dict(side="L", ang=165, el=20, d=1.8, w=50, k=W, size=1.0), key=dict(side="R", ang=40, el=20, d=2, w=6, k=W))
    S.light(58, lambda t: head(MO, t), key=dict(side="R", ang=40, el=45, d=1.4, w=40, k=W, size=1.0), fill=dict(side="L", ang=40, el=10, d=1.4, w=10, k=W))
    S.state(a[53], WinMo=(20, 6000), MoBounce=0)
    mo_room_day(S, b[53])


def bpy_obj(n):
    import bpy
    return bpy.data.objects[n]
