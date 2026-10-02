# Scene 1 - THE PARABLE - INT. Classroom - Day (shots 1-16, 88 s)
# Mamta stands at the front of the centre aisle, back against the teacher's table, facing the class (south).
# Windows on the west wall = camera-left from the back row. Door on the east wall, front corner.
import math
import random

from mathutils import Quaternion, Vector

from kit import *
from film import *
import cast
import sets
from sets import S as SC, DESK_X, DESK_Y, desk_seat

GRADE = {"default": "cold"}


def build(S):
    T = S.T
    E = S.END
    C = sets.mats()
    set_ = sets.build_school(E)
    L = set_["L"]
    vol, _ = fog_box("ClassHaze", (104.5, 6.0, 1.8), (8.8, 11.8, 3.5), 0.006, (0.9, 0.9, 0.85))

    # ------------------------------------------------------------------ world / base light (soft north light)
    S.world(0, (0.55, 0.62, 0.72), 0.25)
    sets.sun_dir(L["S_Sky"], 180, 60)
    S.state(0, S_Sky=0, **{"S_Win%d" % i: (380, 5800) for i in range(3)},
            S_Yard=(450, 6000), S_ArchS=(800, 6000), S_ArchN=(800, 6000), S_DoorSpill=(0, 6000))
    S.emit(0, C["sky_win"], 6.0)
    S.exposure(0, -0.5)

    # ------------------------------------------------------------------ cast
    MA = cast.mamta("school")
    MP = Vector((104.5, 9.85))
    SOUTH = -math.pi / 2
    MA.at(0, MP.x, MP.y, SOUTH).stay(83.6)
    MA.walk(85.0, 106.4, 10.0, mode="smooth").walk(87.2, 108.7, 10.45).walk(88.0, 109.6, 10.6)
    tm = lambda t0, t1, b=(0.1, 0.25): talk(t0, t1, b)
    MA.act(0, 30, lean=-0.06, look=lambda t, u: Vector((104.5 + 2.5 * math.sin(t * 0.21), 4.0, 0.9)), mood=tm(22, 30),
          armL=("rel", 0.24, 0.04, -0.22), armR=("rel", 0.24, -0.1, -0.2))
    # shot 6: chuckle, crouch, grip an invisible plant, yank it out
    a6, b6 = T[6]
    grip = lambda t, u: ("loc", 0.42, 0.0, lerp(0.42, 0.95, seg(t, a6 + 2.6, a6 + 3.3)))
    MA.act(a6, b6, fade=0.4, crouch=lambda t, u: 0.13 * (1 - seg(t, a6 + 2.7, a6 + 3.6)),
          lean=lambda t, u: 0.38 * (1 - seg(t, a6 + 2.7, a6 + 3.7)) - 0.08 * seg(t, a6 + 3.4, a6 + 4.0),
          armL=grip, armR=grip, mood=lambda t, u: (0.2, 1.0, 0.25 + 0.2 * abs(math.sin(t * 7))), bob=0.006, bobf=2.4,
          look=lambda t, u: Vector((104.5, 8.5, 0.6 + 0.9 * seg(t, a6 + 2.7, a6 + 3.6))))
    # 7: warming to it
    a7, b7 = T[7]
    MA.act(a7, T[8][0] + 0.15, mood=tm(a7, b7, (0.15, 0.4)), armL=("rel", 0.24, 0.04, -0.22),
          armR=lambda t, u: ("rel", 0.14, -0.12, -0.24 + 0.07 * math.sin(t * 2)), lean=0.04,
          look=lambda t, u: Vector((104.5 + 2.0 * math.sin(t * 0.3), 5.0, 0.9)))
    # 8-9: the knock; she turns to the door, answers without asking who
    a8, b8 = T[8]
    a9, b9 = T[9]
    PEON_P = Vector((109.35, 10.55))
    MA.act(a8 + 0.1, b9, look=Vector((109.3, 10.55, 1.5)), twist=lambda t, u: 0.5 * seg(t, a8 + 0.1, a8 + 0.8),
          mood=lambda t, u: (-0.25 if t > a9 else -0.1, 0.0, talk(a9 + 0.4, b9 - 0.5)(t, u)[2]), armL=("rel", 0.24, 0.04, -0.22))
    # 10: back to the story, leaning in
    a10, b10 = T[10]
    MA.act(a10, b10, lean=lambda t, u: 0.18 * seg(t, a10, a10 + 3), mood=tm(a10 + 0.3, b10 - 0.3, (0.1, 0.45)),
          armL=("rel", 0.26, 0.04, -0.2), armR=lambda t, u: ("rel", 0.16, -0.1, -0.2 + 0.08 * math.sin(t * 1.7)),
          look=lambda t, u: Vector((104.5 + 2.5 * math.sin(t * 0.25), 5.0, 0.95)))
    # 11: listening faces; she is offscreen (keeps a gentle pose)
    a11, b11 = T[11]
    MA.act(a11, b11, lean=0.12, armL=("rel", 0.26, 0.04, -0.2), look=Vector((104, 5, 0.9)))
    # 12: hope - the moral
    a12, b12 = T[12]
    MA.act(a12, b12, mood=lambda t, u: (0.35, 0.95, talk(a12 + 0.8, b12 - 0.6)(t, u)[2]), hp=-0.06, lean=0.08,
          armL=("rel", 0.26, 0.04, -0.2), armR=("rel", 0.2, -0.08, -0.12), look=Vector((104.5, 5.0, 1.0)))
    # 13-14: the question; she looks down at the boy, the smile drains
    KQ = desk_seat(1, 5, 1)                          # the boy who asks (front row, centre-left)
    a13, b13 = T[13]
    a14, b14 = T[14]
    MA.act(a13, b14, look=Vector((KQ.x, KQ.y, 1.0)), armL=("rel", 0.26, 0.04, -0.2),
          mood=lambda t, u: (lerp(0.3, -0.35, seg(t, a14 + 0.5, b14 - 1.0)), lerp(0.9, -0.35, seg(t, a14 + 0.5, b14 - 1.5)), 0.03))
    # 16: gathers the book, heads for the door
    a16, b16 = T[16]
    MA.act(a16, a16 + 1.5, armR=Vector((104.3, 10.5, 0.8)), lean=0.35, look=Vector((104.3, 10.5, 0.78)), mood=(-0.3, -0.1, 0.0))
    MA.act(a16 + 1.4, b16, look=Vector((109.5, 10.6, 1.5)), armL=("rel", 0.2, 0.08, -0.12), armR=("rel", 0.18, -0.05, -0.12),
          mood=(-0.3, 0.0, 0.0))
    S.on(MA, [n for n in range(4, 17) if n not in (11, 15)])

    # book: in her left hand, on the table during shot 6, then gathered against her chest
    bk = empty("Book", (0, 0, 0))
    new_obj("pgL", box_mesh("pg", 0.15, 0.22, 0.012, False), M_paper(), bk, loc=(0.0, -0.075, 0), rot=(0.2, 0, 0))
    new_obj("pgR", box_mesh("pg2", 0.15, 0.22, 0.012, False), M_paper(), bk, loc=(0.0, 0.075, 0), rot=(-0.2, 0, 0))
    new_obj("cov", box_mesh("cv", 0.155, 0.31, 0.008, False), M((0.3, 0.12, 0.08), 0.7), bk, loc=(0, 0, -0.008))
    hold(bk, MA, "L", 0, a6, off=(0.0, 0.0, 0.03), step=2)
    bake_fn(bk, a6, a7, lambda t: (Vector((104.1, 10.55, 0.81)), Quaternion((0, 0, 1), 0.4)))
    hold(bk, MA, "L", a7, a16 + 1.2, off=(0.0, 0.0, 0.03), step=2)
    hold(bk, MA, "L", a16 + 1.2, b16, off=(0.0, 0.0, 0.05), step=2)

    # ------------------------------------------------------------------ peon at the door (shots 8-9)
    PE = cast.peon()
    PE.at(a8, PEON_P.x + 0.4, PEON_P.y, math.pi).walk(a8 + 0.9, PEON_P.x, PEON_P.y, yaw=math.pi).stay(b9)
    PE.act(a8, b9, armR=("rel", 0.28, -0.05, -0.12), armL=("rel", 0.25, 0.08, -0.14),
           mood=talk(a8 + 1.6, a8 + 3.4), look=lambda t, u: head(MA, t))
    S.on(PE, [8, 9])
    fold = new_obj("Folders", box_mesh("fd", 0.24, 0.32, 0.06, False), M((0.55, 0.45, 0.3), 0.8))
    hold(fold, PE, "R", a8, b9, off=(0.0, 0.05, 0.0), step=2)
    vis(fold, [(a8, b9)])
    # classroom door opened by the peon
    door = set_["P"]["cls_door"]
    keys(door, "rotation_euler", 2, [(0, math.radians(12))])                   # open all day (90 = shut)

    # ------------------------------------------------------------------ the class: 48 kids seated in 6 rows
    rnd = random.Random(1)
    kids = []
    GIRL_A, GIRL_B = None, None
    for ri in range(6):
        for ci in range(4):
            for k in range(2):
                p = desk_seat(ci, ri, k)
                kd = cast.kid(len(kids), 7)
                if (ci, ri, k) == (0, 3, 0):
                    kd = cast.kid(len(kids), 7, girl=True, name="GirlA")
                    GIRL_A = kd
                elif (ci, ri, k) == (0, 3, 1):
                    kd = cast.kid(len(kids), 7, girl=True, name="GirlB")
                    GIRL_B = kd
                kd.at(0, p.x, p.y, math.pi / 2).stay(E)
                ph = rnd.uniform(0, 6)
                kd.act(0, E, fade=0, sit=1.0, seat=0.38, _hold0=True,
                       look=(lambda pp, ph_: (lambda t, u: head(MA, t) + Vector((0.4 * math.sin(t * 0.37 + ph_), 0, 0))))(p, ph),
                       mood=(0.15, 0.35 + 0.3 * rnd.random(), 0.0), hp=0.05)
                kd.kq = (ci, ri, k)
                kids.append(kd)
    # the girls: candy play (shot 4)
    a4, b4 = T[4]
    GIRL_B.act(a4, b4, fade=0.3, look=lambda t, u: head(GIRL_A, t),
               armL=lambda t, u: (GIRL_A.J(t)["hand"]["R"] + Vector((0.03, 0, 0))) if (a4 + 1.0 < t < a4 + 2.4 or a4 + 3.8 < t < a4 + 5.0) else ("rel", 0.25, 0.05, -0.15),
               mood=lambda t, u: (0.2, 1.0, 0.35 * abs(math.sin(t * 9))), twist=-0.35, bob=0.01, bobf=3.0)
    GIRL_A.act(a4, b4, fade=0.3, look=lambda t, u: est_seated(GIRL_B, t),
               armR=lambda t, u: ("rel", 0.16, lerp(-0.12, 0.22, seg(t, a4 + 1.4, a4 + 2.0)) if t < a4 + 3.5 else lerp(0.22, -0.12, seg(t, a4 + 4.2, a4 + 4.8)),
                                  -0.12 + 0.2 * seg(t, a4 + 1.2, a4 + 1.8)),
               mood=lambda t, u: (0.2, 1.0, 0.3 * abs(math.sin(t * 8 + 1))), twist=0.3, bob=0.01, bobf=2.6)
    # stir at the bell: a few kids half rise, everyone turns
    a15 = T[15][0]
    for kd in kids:
        if rnd.random() < 0.4:
            kd.act(a15 + 2.5 + rnd.uniform(0, 1.5), E, fade=0.8, sit=0.0, look=Vector((109, 10.5, 1.2)))
        else:
            kd.act(a15 + 2.0, E, fade=0.5, look=lambda t, u: head(MA, t), mood=(0, 0.6, 0.2))
    kq = next(k for k in kids if k.kq == (1, 5, 1))
    kq.act(T[13][0], T[13][1], mood=talk(T[13][0] + 0.3, T[13][1] - 0.5))
    for kd in kids:
        shots_on = [4, 5, 6, 7, 10, 11, 12, 13, 14, 16]
        if kd is kq:
            shots_on.remove(13)
        if kd.kq[0] == 0 and kd.kq[1] in (4, 5):          # cleared for the girls' two-shot
            shots_on.remove(4)
        S.on(kd, shots_on, step=1 if kd in (GIRL_A, GIRL_B) else 12)

    # ------------------------------------------------------------------ tabletop props: sand tray + insect (1), hands + candy (2-3)
    TRAY = Vector((100.62, 5.92, 0.705))
    new_obj("Tray", box_mesh("tr", 0.30, 0.20, 0.02), M((0.18, 0.12, 0.07), 0.8), loc=TRAY)
    sand = new_obj("Sand", box_mesh("sd", 0.28, 0.18, 0.012), M((0.62, 0.52, 0.36), 1.0), loc=TRAY + Vector((0, 0, 0.012)))
    rnd2 = random.Random(5)
    pts = [Vector((TRAY.x - 0.12, TRAY.y - 0.06, TRAY.z + 0.026))]
    ang = 0.4
    for i in range(140):
        ang += rnd2.uniform(-0.55, 0.55) + 0.06 * math.sin(i * 0.3)
        q = pts[-1] + Vector((math.cos(ang), math.sin(ang), 0)) * 0.0016
        q.x = min(max(q.x, TRAY.x - 0.13), TRAY.x + 0.13)
        q.y = min(max(q.y, TRAY.y - 0.08), TRAY.y + 0.08)
        pts.append(q)
    bug = new_obj("Insect", sphere_mesh("ins", 0.004, 8, 6, (1.6, 0.9, 0.6)), M((0.04, 0.03, 0.02), 0.4))
    a1, b1 = T[1]

    def bugpos(t):
        u = min(max((t - a1) / (b1 - a1), 0), 1) * (len(pts) - 2)
        i = int(u)
        p = pts[i].lerp(pts[i + 1], u - i)
        d = pts[i + 1] - pts[i]
        return p, Quaternion((0, 0, 1), math.atan2(d.y, d.x))
    bake_fn(bug, a1, b1, bugpos)
    vis(bug, [(a1, b1)])
    trail_m = M((0.22, 0.17, 0.11), 1.0)
    for i in range(0, len(pts) - 1, 2):
        d_ = new_obj("trail", sphere_mesh("tdot", 0.0014, 4, 3, (1.4, 1.4, 0.3)), trail_m, loc=pts[i] - Vector((0, 0, 0.002)))
        tt = a1 + (b1 - a1) * i / (len(pts) - 2)
        vis(d_, [(tt, b1)])
    # girl's hands on her desk (top-down), palm lines, fist that opens to a candy
    HP = Vector((100.86, 5.86, 0.705))
    skin = M(SKIN["b"], 0.55)
    sleeve = M((0.86, 0.86, 0.84), 0.9)
    lines_m = M((0.16, 0.08, 0.05), 0.8)
    a2, b2 = T[2]
    a3, b3 = T[3]
    palm = empty("PalmL", HP + Vector((-0.07, 0, 0.015)))
    new_obj("palm", box_mesh("pm", 0.065, 0.075, 0.016, False), skin, palm)
    for i, dx in enumerate((-0.024, -0.008, 0.008, 0.024)):
        f_ = new_obj("fing", capsule_mesh("fg", 0.05 - abs(dx) * 0.4, 0.007), skin, palm, loc=(dx, 0.035, 0.0), rot=(-math.pi / 2, 0, 0))
    new_obj("thumb", capsule_mesh("th", 0.04, 0.0085), skin, palm, loc=(0.03, -0.01, 0.0), rot=(-math.pi / 2, 0, -0.9))
    for (dx, dy, w, rz) in ((-0.004, 0.012, 0.05, 0.25), (0.0, 0.0, 0.055, -0.15), (-0.01, -0.016, 0.04, 1.1)):
        new_obj("pline", box_mesh("pl", w, 0.0012, 0.001, False), lines_m, palm, loc=(dx, dy, 0.0085), rot=(0, 0, rz))
    new_obj("forearmL", capsule_mesh("fa", 0.2, 0.022), skin, palm, loc=(0, -0.04, 0), rot=(math.pi / 2, 0, 0))
    new_obj("sleeveL", capsule_mesh("sl", 0.12, 0.03), sleeve, palm, loc=(0, -0.2, 0), rot=(math.pi / 2, 0, 0))
    fist = empty("FistR", HP + Vector((0.07, -0.005, 0.022)))
    knuck = new_obj("fistball", sphere_mesh("fb", 0.03, 12, 8, (1.0, 1.15, 0.8)), skin, fist)
    new_obj("forearmR", capsule_mesh("fa", 0.2, 0.022), skin, fist, loc=(0, -0.03, -0.004), rot=(math.pi / 2, 0, 0))
    new_obj("sleeveR", capsule_mesh("sl", 0.12, 0.03), sleeve, fist, loc=(0, -0.19, -0.004), rot=(math.pi / 2, 0, 0))
    fingers = []
    for i, dx in enumerate((-0.021, -0.007, 0.007, 0.021)):
        hinge = empty("knuck%d" % i, (0, 0, 0), fist)
        hinge.location = (dx, 0.022, 0.004)
        new_obj("ofing", capsule_mesh("ofg", 0.046, 0.0068), skin, hinge, rot=(-math.pi / 2, 0, 0))
        fingers.append(hinge)
    candy = new_obj("Candy", sphere_mesh("cd", 0.011, 10, 6, (1.7, 1, 0.9)), M((0.85, 0.25, 0.35), 0.15, 0.8))
    for sgn in (-1, 1):
        new_obj("twist", sphere_mesh("tw", 0.007, 6, 4, (1.2, 0.5, 0.3)), M((0.9, 0.7, 0.2), 0.1, 1.0), candy, loc=(sgn * 0.022, 0, 0))
    t_open = a3 + 0.4
    for h_ in fingers:
        h_.rotation_mode = "XYZ"
        keys(h_, "rotation_euler", 0, [(0, -2.6), (t_open, -2.6), (t_open + 0.9, -0.05)])
    keys(knuck, "scale", 2, [(0, 1.0), (t_open, 1.0), (t_open + 0.9, 0.45)])
    keys(knuck, "scale", 1, [(0, 1.0), (t_open, 1.0), (t_open + 0.9, 0.7)])
    # the hand lifts and dangles the candy to the right (toward the friend)
    keys_vec(fist, "location", [(0, fist.location), (t_open + 1.1, fist.location),
                                (b3, fist.location + Vector((0.035, 0.01, 0.05)))])

    def candy_at(t):
        base = fist.location.copy()
        if t > t_open + 1.1:
            base = base.lerp(fist.location + Vector((0.035, 0.01, 0.05)), seg(t, t_open + 1.1, b3))
            sw = math.sin((t - t_open) * 7.5) * 0.02
            return base + Vector((0.02 + sw, 0.04, -0.035 + 0.01 * abs(sw) / 0.02)), Quaternion((0, 0, 1), sw * 10)
        return base + Vector((0, 0.022, 0.012)), Quaternion((0, 0, 1), 0.3)
    bake_fn(candy, a2, b3, candy_at)
    for ob in (palm, fist, candy):
        vis_tree(ob, [(a2, b3)])

    # ------------------------------------------------------------------ bell (shot 15) shakes
    arm = set_["P"]["bell_arm"]
    a15, b15 = T[15]
    arm.rotation_mode = "XYZ"
    for f_ in range(int(F(a15)), int(F(b15)) + 1):
        ANIM.put(arm, "rotation_euler", 0, f_, 0.35 * (1 if f_ % 2 else -1))

    # ------------------------------------------------------------------ cameras
    yawM = SOUTH

    def c1(t):                                      # top-down macro on sand, frame-up = north
        p = TRAY + Vector((0.0, 0.0, 0.03))
        return dict(pos=p + Vector((0, -0.0004, 0.86)), look=p, lens=100, focus=0.86, fstop=4.0)
    S.shoot(1, c1)

    def c2(t):
        p = HP + Vector((0.0, 0.0, 0.02))
        return dict(pos=p + Vector((0, -0.0004, 0.86)), look=p, lens=100, focus=0.86, fstop=4.0)
    S.shoot(2, c2)
    S.shoot(3, c2)

    def c4(t):                                     # two girls, from two rows ahead at child height (rows cleared)
        g = mid(head(GIRL_A, t), head(GIRL_B, t))
        pos = Vector((101.22, 6.85, 0.93))
        return dict(pos=pos, look=g + Vector((0, 0, -0.12)), focus=(g - pos).length, fstop=2.8)
    S.shoot(4, c4)

    def c5(t):                                     # back row, slow push toward Mamta
        u = seg(t, T[5][0], T[5][1])
        pos = Vector((104.5, 0.55, 1.55)).lerp(Vector((104.5, 2.0, 1.5)), u)
        return dict(pos=pos, look=Vector((104.5, 9.85, 1.25)), focus=(9.85 - pos.y), fstop=5.6)
    S.shoot(5, c5)

    def c6(t):
        return frame(chest(MA, a6 + 0.5) + Vector((0, 0, -0.15)), yawM, 50, "MS", h=1.55, az=8, up=0.0, fstop=4.0)
    S.shoot(6, c6)

    def mcu(t, az=14):
        return frame(eyes(MA, t), yawM, 85, "MCU", az=az, up=-0.06, third=-0.6, fstop=2.0)
    S.shoot(7, lambda t: mcu(t))
    S.shoot(8, lambda t: ots(MA, PE, t, 50, side=-1, back=0.65, out_=0.3, dz=0.02) if t > a8 + 0.9 else
            ots(MA, PE, a8 + 0.9, 50, side=-1, back=0.65, out_=0.3, dz=0.02))
    S.shoot(9, lambda t: frame(eyes(MA, t), yawM, 85, "MCU", az=34, up=-0.06, third=-0.5))
    S.shoot(10, lambda t: push(mcu(t), 0.22 * seg(t, a10, b10)))

    def c11(t):                                    # pan across rapt faces, child's eye level
        u = seg(t, a11, b11)
        pos = Vector((104.5, 9.15, 0.92))
        yaw = math.radians(lerp(-150, -30, u))
        return dict(pos=pos, look=pos + Vector((math.cos(yaw), math.sin(yaw), -0.03)) * 3, focus=2.6, fstop=4.0)
    S.shoot(11, c11)
    S.shoot(12, lambda t: frame(eyes(MA, t), yawM, 85, "CU", az=10, up=-0.03, third=-0.4))

    def c13(t):                                    # POV of the boy: desk height, looking up at her
        pos = Vector((KQ.x + 0.05, KQ.y + 0.05, 1.0))
        e = eyes(MA, t)
        return dict(pos=pos, look=e + Vector((0, 0, -0.2)), focus=(e - pos).length, fstop=2.8)
    S.shoot(13, c13)
    S.shoot(14, lambda t: push(frame(eyes(MA, t), yawM, 85, "ECU", h=0.24, az=4, up=-0.01), 0.12 * seg(t, a14, b14)))

    def c15(t):
        bp = SC["bell"]
        pos = Vector((110.6, 12.4, 1.15))
        return dict(pos=pos, look=Vector((bp.x + 0.08, bp.y, bp.z - 0.02)), focus=(Vector(bp) - pos).length, fstop=2.8)
    S.shoot(15, c15)
    S.shoot(16, lambda t: dict(pos=Vector((103.1, 7.0, 1.45)), look=Vector((105.3, 10.0, 1.15)), focus=3.5, fstop=4.0))

    # ------------------------------------------------------------------ per-shot light (from the Lighting column)
    W = 5600
    eyeM = lambda t: eyes(MA, t)
    S.light(1, TRAY, key=dict(side="L", ang=88, el=7, d=1.2, w=60, k=W, size=0.8), fill=dict(side="R", ang=60, el=40, w=4, k=6500))
    S.light(2, HP, key=dict(side="L", ang=88, el=8, d=1.2, w=60, k=W, size=0.8), fill=dict(side="R", ang=60, el=40, w=3, k=6500))
    S.light(3, HP, key=dict(side="L", ang=85, el=10, d=1.2, w=60, k=W, size=0.8), fill=dict(side="R", ang=60, el=40, w=3, k=6500),
            kick=dict(side="R", ang=30, el=35, d=0.8, w=4, k=5000))
    S.light(4, lambda t: mid(head(GIRL_A, t), head(GIRL_B, t)), key=dict(side="L", ang=45, el=25, d=2.5, w=110, k=W, size=1.6),
            fill=dict(side="R", ang=20, el=-15, d=2.0, w=30, k=W, size=2.0))
    S.light(5, (104.5, 7, 1.3), key=dict(side="L", ang=75, el=35, d=5, w=400, k=W, size=3), fill=dict(side="R", ang=40, el=30, d=6, w=60, k=6000))
    S.light(6, eyeM, key=dict(side="L", ang=45, el=25, d=2.4, w=150, k=W, size=1.6), fill=dict(side="R", ang=50, el=10, d=2.2, w=38, k=W, size=1.6))
    S.light(7, eyeM, key=dict(side="L", ang=45, el=22, d=2.0, w=110, k=W, size=1.4), fill=dict(side="R", ang=50, el=8, d=2.0, w=27, k=W, size=1.6))
    S.light(8, lambda t: head(PE, a8 + 1), key=dict(side="R", ang=160, el=15, d=1.6, w=180, k=6000, size=1.5),
            fill=dict(side="L", ang=60, el=20, d=2.0, w=10, k=W))
    S.light(9, eyeM, key=dict(side="L", ang=55, el=22, d=2.0, w=100, k=W, size=1.4), fill=dict(side="R", ang=50, el=8, d=2.0, w=18, k=W))
    S.light(10, eyeM, key=dict(side="L", ang=30, el=18, d=2.0, w=110, k=W, size=1.4), fill=dict(side="R", ang=50, el=8, d=2.0, w=27, k=W))
    S.light(11, (104.5, 6.0, 0.95), key=dict(side="L", ang=60, el=25, d=3, w=200, k=W, size=2.5), fill=dict(side="R", ang=20, el=-25, d=2.5, w=60, k=W, size=3))
    S.light(12, eyeM, key=dict(side="L", ang=40, el=20, d=1.9, w=170, k=4300, size=1.4), fill=dict(side="R", ang=50, el=8, d=2.0, w=55, k=4300),
            kick=dict(side="L", ang=20, el=10, d=1.4, w=6, k=4300))
    S.light(13, eyeM, key=dict(side="L", ang=60, el=20, d=2.0, w=60, k=W), rim=dict(side="L", ang=150, el=25, d=2.0, w=140, k=6000, size=1.2))
    S.light(14, eyeM, key=dict(side="L", ang=40, el=20, d=1.9, w=150, k=4600, size=1.4), fill=dict(side="R", ang=50, el=8, d=2.0, w=50, k=4600))
    ramp(S.rig["fill"].data, "energy", 0, a14 + 0.5, b14 - 0.5, 50, 6)          # the cutter takes the bounce away
    S.light(15, (SC["bell"].x + 0.08, SC["bell"].y, SC["bell"].z), key=dict(side="R", ang=50, el=20, d=1.5, w=40, k=6000, size=1.5),
            kick=dict(side="L", ang=70, el=40, d=0.8, w=20, k=6500))
    S.light(16, eyeM, key=dict(side="L", ang=45, el=25, d=2.5, w=120, k=W, size=1.6), fill=dict(side="R", ang=50, el=10, d=2.4, w=30, k=6000))
    S.state(a8, S_DoorSpill=(260, 6200))
    S.state(b9, S_DoorSpill=(0, 6200))


_PAPER = {}


def M_paper():
    if "m" not in _PAPER:
        _PAPER["m"] = M((0.82, 0.8, 0.72), 0.9)
    return _PAPER["m"]
