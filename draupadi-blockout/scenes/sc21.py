# Scene 21 - CORE MEMORY: THE BIRTH - INT. House (Mamta's Room) - Night (shots 150-161, 48 s)
# Shot 61's frame at night: a single bare bulb overhead, hard, no fill; the nurse and doctor throw shadows on
# the walls. The birth is implied - faces and hands only. The baby is never seen. The red sweater was for him.
import math

from mathutils import Matrix, Quaternion, Vector

from kit import *
from film import *
import cast
import hs
import props
import sets
from sets import H

BED = H["m_bed"]
HIPB = Vector((BED.x, BED.y + 0.05))
CORNER = Vector((-1.25, 8.55))          # where the nurse cleans the baby (by the door)


def build(S):
    T = S.T
    a = {n: T[n][0] for n in T}
    b = {n: T[n][1] for n in T}
    E = S.END
    st = hs.house(S)
    C = sets.mats()
    S.state(0, BulbM=(130, 2700), TubeCorr=(40, 6500))
    S.emit(0, C["bulb"], 50.0)
    S.emit(0, C["tube"], 6.0)
    S.world(0, (0.01, 0.01, 0.015), 0.01)
    S.exposure(0, 1.0)
    # the bulb swings when the nurse knocks it (160)
    bulb = st["P"]["bulb_m"]
    bl = st["L"]["BulbM"]
    B0 = bulb.location.copy()
    for f in range(int(F(a[160])), int(F(b[161])) + 1):
        t = (f - 1) / FPS
        k = math.exp(-(t - a[160]) * 0.25)
        off = Vector((0.35 * k * math.sin((t - a[160]) * 3.1), 0.12 * k * math.sin((t - a[160]) * 2.3), 0))
        for i in range(3):
            ANIM.put(bulb, "location", i, f, (B0 + off)[i])
            ANIM.put(bl, "location", i, f, (B0 + off + Vector((0, 0, -0.1)))[i])
    YMb = cast.young_mamta("birth", name="YMbirth")
    YMa = cast.young_mamta("after", name="YMafter")
    NU = cast.nurse()
    DR = cast.doctor()
    YMO = cast.mother(young=True)
    FACELESS = Actor("Faceless", 1.72, (0.02, 0.02, 0.02), (0.02, 0.02, 0.02), silhouette=True, sleeve=2.0)
    # young Mamta lying on the bed, head north on the pillow
    for X, t0, t1 in ((YMb, 0, b[151]), (YMa, a[152], E)):
        X.at(t0, HIPB.x, HIPB.y, -math.pi / 2).stay(t1)
        X.act(t0, t1, fade=0, lie=1.0, bed=0.53, hp=0.35, armL=("rel", 0.05, 0.12, -0.25), armR=("rel", 0.05, -0.12, -0.25))
    YMb.act(0, b[151], mood=lambda t, u: (-1.0, -0.8, 0.45 + 0.4 * abs(math.sin(t * 2.2))), shake=0.8, hy=lambda t, u: 0.3 * math.sin(t * 1.3),
            armL=Vector((BED.x + 0.75, BED.y + 0.6, 0.8)), armR=Vector((BED.x - 0.75, BED.y + 0.5, 0.8)))
    YMa.act(a[152], b[152], mood=(-0.3, 0.1, 0.25), eyes=0.6, look=Vector((CORNER.x, CORNER.y, 1.0)))
    YMa.act(a[153], b[153], look=Vector((CORNER.x, CORNER.y, 1.0)), mood=(0.0, 0.2, 0.0))
    YMa.act(a[154], b[154], mood=(0.4, 0.8, 0.0), hp=0.15, look=lambda t, u: Vector((CORNER.x, CORNER.y, 1.0)))
    YMa.act(a[155], b[156], armL=lambda t, u: est(NU, t) + Vector((0.2, 0.25, -0.35)), armR=lambda t, u: est(NU, t) + Vector((0.2, 0.05, -0.35)),
            look=lambda t, u: est(NU, t), mood=(0.2, 0.5, 0.05), shake=lambda t, u: 0.5 if t > a[156] else 0.0)
    YMa.act(a[157], b[159], look=Vector((-1.45, 7.6, 1.4)), mood=lambda t, u: (lerp(0.0, -1.0, seg(t, a[158], a[158] + 1.5)), lerp(0.4, -0.6, seg(t, a[158], a[158] + 1.5)), 0.0))
    YMa.act(a[160], b[160], fade=0.3, lie=0.55, bed=0.53, mood=lambda t, u: (-1.0, -0.9, 0.5 + 0.4 * abs(math.sin(t * 7))), shake=1.5,
            armR=lambda t, u: Vector((-1.45, 7.6, 1.2)), look=Vector((-1.45, 7.6, 1.3)))
    YMa.act(a[161], b[161], armR=("rel", 0.35, -0.05, 0.05), mood=(-1.0, -0.9, 0.3))
    # nurse and doctor
    NU.at(0, BED.x - 0.95, BED.y - 0.3, 0.0).stay(b[151]).at(a[152], CORNER.x, CORNER.y, -0.8).stay(b[154])
    NU.walk(a[155] + 1.0, BED.x - 0.9, BED.y - 0.6, mode="smooth").stay(b[156], 0.2)
    NU.walk(b[157], -1.45, 7.55, mode="smooth").at(a[159], -1.45, 6.95, -math.pi / 2).stay(a[159] + 2.2).walk(b[159], -1.0, 6.9, mode="smooth")
    NU.at(a[160], BED.x - 0.85, BED.y - 0.2, 0.0).stay(b[160])
    DR.at(0, BED.x - 0.2, BED.y - 1.3, math.pi / 2).stay(b[151]).at(a[160], BED.x - 0.4, BED.y - 1.25, math.pi / 2 - 0.4).stay(b[160])
    NU.act(0, b[151], armR=Vector((BED.x - 0.2, BED.y + 0.1, 0.75)), armL=Vector((BED.x - 0.2, BED.y + 0.5, 0.8)), lean=0.3, look=Vector((BED.x, BED.y + 0.6, 0.7)))
    DR.act(0, b[151], lean=0.35, armR=Vector((BED.x - 0.1, BED.y - 0.7, 0.7)), armL=Vector((BED.x + 0.2, BED.y - 0.7, 0.7)), look=Vector((BED.x, BED.y - 0.6, 0.6)))
    babyhold = lambda t, u: ("rel", 0.3, -0.1, -0.15)
    NU.act(a[152], b[157], armL=("rel", 0.3, 0.1, -0.15), armR=babyhold, lean=0.25, look=lambda t, u: Vector((CORNER.x - 0.35, CORNER.y - 0.25, 0.85)))
    NU.act(a[159], b[159], armL=lambda t, u: est(YMO, t) + Vector((0, 0.3, -0.5)) if t < a[159] + 2.0 else ("rel", 0.1, 0.1, -0.3), armR=babyhold)
    pin = lambda t, u: Vector((BED.x - 0.15, BED.y + 0.35, 0.78))
    NU.act(a[160], b[160], armL=pin, armR=lambda t, u: Vector((BED.x - 0.05, BED.y + 0.6, 0.85)), lean=0.6)
    DR.act(a[160], b[160], armL=Vector((BED.x - 0.1, BED.y - 0.2, 0.75)), armR=Vector((BED.x + 0.15, BED.y - 0.3, 0.75)), lean=0.5)
    # through the curtain: the nurse gives the baby to Mother, who walks away and hands him to someone faceless
    YMO.at(a[159], -1.55, 6.55, math.pi / 2).stay(a[159] + 2.3).walk(b[159], -4.6, 6.7, yaw=math.pi, mode="smooth")
    YMO.act(a[159], b[159], armL=("rel", 0.3, 0.1, -0.15), armR=("rel", 0.3, -0.1, -0.15), mood=(-0.5, -0.4, 0.0))
    FACELESS.at(a[159], -5.4, 6.75, 0.0).stay(b[159])
    FACELESS.act(a[159] + 4.0, b[159], armL=("rel", 0.35, 0.05, -0.15), armR=("rel", 0.35, -0.05, -0.15))
    S.on(YMb, [150, 151])
    S.on(YMa, list(range(152, 162)))
    S.on(NU, [150, 151, 152, 153, 155, 156, 157, 159, 160])
    S.on(DR, [150, 151, 160])
    S.on(YMO, [159])
    S.on(FACELESS, [159])
    # the baby: a wrapped bundle (face never shown), carried by the nurse then Mother
    bundle = new_obj("Baby", capsule_mesh("bb", 0.42, 0.1), M((0.85, 0.83, 0.78), 0.95))
    def baby(t):
        if t < a[159] + 2.2:
            who = NU
        elif t < a[159] + 4.4:
            who = YMO
        else:
            who = FACELESS
        j = who.J(t)
        p = (j["hand"]["L"] + j["hand"]["R"]) / 2 + Vector((0, 0, 0.03))
        return p, basis_quat(j["tl"], j["tf"])
    bake_fn(bundle, a[152], b[159], baby, 1)
    vis(bundle, [(a[152], b[157] + 0.4), (a[159], b[159])])
    # the red sweater in her hands (155-156) and in her fist (161)
    sw = props.sweater()
    hold(sw, YMa, "L", a[155], b[156], off=(0.05, 0.0, 0.06))
    vis_tree(sw, [(a[155], b[156])])
    fistR, ff, fth = props.hand("SweaterFist", skin=SKIN["a"], sleeve=(0.30, 0.06, 0.10))
    red = M((0.50, 0.02, 0.03), 0.95)
    knit = new_obj("FistKnit", sphere_mesh("fk", 0.07, 12, 8, (1.4, 0.9, 0.5)), red, loc=(0, 0, 0))
    FP = Vector((-2.0, 12.2, 0.75))
    fistR.location = FP
    fistR.rotation_euler = (math.radians(15), 0, math.radians(-90))
    props.curl(ff, [(a[161], 0.35), (a[161] + 1.6, 0.85), (a[161] + 2.6, 0.95), (a[161] + 3.2, 0.2)])
    keys_vec(knit, "location", [(a[161], FP + Vector((-0.09, 0.0, -0.01))), (a[161] + 3.2, FP + Vector((-0.09, 0.0, -0.01))),
                                (b[161], FP + Vector((-0.12, 0.0, -0.75)))])
    for ob in (fistR, knit):
        vis_tree(ob, [(a[161], b[161])])
    # the door curtain flutters (159): stronger wave
    cur = st["P"]["door_curtain"]
    cur.modifiers["wave"].height = 0.08

    # cameras
    S.shoot(150, lambda t: dict(pos=Vector((-7.45, 8.05, 1.75)), look=Vector((-2.3, 12.2, 1.0)), focus=5.6, fstop=5.6))
    def face_cam(X, tt, side=-0.6, d=1.9):
        def f(t):
            j = X.J(tt)
            dirv = (j["hf"] * 0.8 + Vector((side, 0, 0))).normalized()
            return dict(pos=j["head_c"] + dirv * d, look=head(X, t), focus=d, fstop=2.0)
        return f
    S.shoot(151, face_cam(YMb, a[151]))
    S.shoot(152, face_cam(YMa, a[152]))

    def c153(t):                                  # POV from the bed: rack from the bedpost to the nurse's corner
        pos = head(YMa, a[153]) + Vector((-0.1, -0.4, 0.32))
        k = seg(t, a[153] + 0.8, a[153] + 2.4)
        return dict(pos=pos, look=Vector((CORNER.x, CORNER.y, 1.0)), focus=lerp(1.2, (Vector((CORNER.x, CORNER.y, 1.0)) - pos).length, k), fstop=1.8)
    S.shoot(153, c153)
    S.shoot(154, face_cam(YMa, a[154], -0.4))
    S.shoot(155, lambda t: dict(pos=Vector((-3.4, 11.0, 1.5)), look=Vector((-1.7, 12.6, 0.85)), focus=2.4, fstop=2.8))
    S.shoot(156, lambda t: dict(pos=YMa.J(a[156])["hand"]["L"] + Vector((-0.65, -0.25, 0.5)), look=YMa.J(t)["hand"]["L"], focus=0.9, fstop=2.8))
    S.shoot(157, lambda t: dict(pos=Vector((-3.9, 10.6, 1.5)), look=est(NU, t) + Vector((0, 0, -0.4)), focus=3.0, fstop=4.0))
    S.shoot(158, face_cam(YMa, a[158], -0.7))
    S.shoot(159, lambda t: dict(pos=head(YMa, a[159]) + Vector((-0.1, -0.35, 0.25)), look=Vector((-1.6, 6.8, 1.25)), focus=6.0, fstop=2.8))
    S.shoot(160, lambda t: dict(pos=Vector((-2.15, 11.2, 2.35)), look=head(YMa, t) + Vector((0, -0.3, -0.1)), focus=1.9, fstop=2.8))
    S.shoot(161, lambda t: dict(pos=FP + Vector((-0.55, -0.62, 0.12)), look=FP + Vector((-0.08, 0, -0.05)), focus=0.84, fstop=2.8))
    # hard top light only, no fill
    S.light(151, lambda t: head(YMb, t), kick=dict(side="L", ang=40, el=70, d=1.2, w=20, k=2700))
    S.light(152, lambda t: head(YMa, t), kick=dict(side="L", ang=40, el=70, d=1.2, w=15, k=2700))
    S.light(154, lambda t: head(YMa, t), kick=dict(side="L", ang=20, el=60, d=1.2, w=25, k=2700))
    S.light(156, lambda t: YMa.J(t)["hand"]["L"], key=dict(side="L", ang=40, el=70, d=1.0, w=30, k=2700, size=0.1))
    S.light(153, (CORNER.x, CORNER.y, 1.1), key=dict(side="R", ang=60, el=60, d=1.5, w=40, k=2700, size=0.1))
    S.light(155, lambda t: est(NU, t), key=dict(side="L", ang=40, el=65, d=1.6, w=40, k=2700, size=0.1))
    S.light(157, lambda t: est(NU, t), key=dict(side="L", ang=40, el=65, d=1.6, w=40, k=2700, size=0.1))
    S.light(161, FP, kick=dict(side="L", ang=40, el=75, d=0.8, w=20, k=2700))
