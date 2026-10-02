# scene01.py - SCENE 1 "MELA" (shots 1-19, 102 s) blockout. Run:  ./blender.sh -P scene01.py -- <abs>/scene01.blend
# Everything is data: actor waypoints/gestures below, one camera function per shot, light states per shot.
# Axes: x east, y north, z up. Actor yaw 0 = facing +x, 90deg = facing +y. Times are seconds on the film timeline.
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from mathutils import Vector

from kit import *
import mela
from mela import POLE, VAN, WHEEL

OUT = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else os.path.abspath("scene01.blend")
T_END = 102.0
SH = {1: (0, 5), 2: (5, 9), 3: (9, 14), 4: (14, 17), 5: (17, 20), 6: (20, 25), 7: (25, 28), 8: (28, 32), 9: (32, 36),
      10: (36, 41), 11: (41, 45), 12: (45, 49), 13: (49, 52), 14: (52, 57), 15: (57, 62), 16: (62, 68), 17: (68, 77),
      18: (77, 95), 19: (95, 102)}
LENS = {1: 24, 2: 135, 3: 35, 4: 50, 5: 85, 6: 50, 7: 100, 8: 85, 9: 50, 10: 24, 11: 25, 12: 35, 13: 50, 14: 85,
        15: 35, 16: 100, 17: 24, 18: 100, 19: 50}
INFO = {1: "ELS | Drone push in + slow tilt down | 24mm | High/top down", 2: "LS | Static | 135mm | Eye level",
        3: "MLS | Gimbal follow from behind, arcs to frontal | 35mm | Eye level",
        4: "MCU | Static | 50mm | Child's eye level (low)", 5: "CU | Static, rack focus crowd to balloons | 85mm | Low (Dhruv POV)",
        6: "MS | Handheld | 50mm | Eye level", 7: "ECU | Static, slow motion | 100mm macro | Eye level",
        8: "LS | Static | 85mm | Eye level", 9: "MS | Static, rack focus (speed ramp) | 50mm | Eye level",
        10: "ELS | Drone static top down | 24mm | Top down", 11: "MCU | Handheld, whip pans between cuts | 25mm | Eye level",
        12: "LS | Slow track in | 35mm | Eye level", 13: "MCU | Handheld | 50mm | Eye level (OTS seller)",
        14: "MCU | Static | 85mm | Slightly low", 15: "MS | Handheld (recreation, 'told' grade) | 35mm | Eye level",
        16: "ECU | Static, slow push in | 100mm | Eye level", 17: "ELS | Crane up into VFX map zoom | 24mm | High to top down",
        18: "ECU | Slow slider moves, macro montage + rank ladder | 100mm macro | Various",
        19: "LS | Static, balloon rises out of frame (TITLE) | 50mm | Low"}

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.fps = 24
scene.frame_start, scene.frame_end = 1, int(T_END * 24)
scene.render.resolution_x, scene.render.resolution_y = 1920, 1080
scene.render.engine = "BLENDER_EEVEE"
scene.eevee.taa_render_samples = 16
scene.view_settings.view_transform = "Standard"
scene.view_settings.exposure = -0.6

# ====================================================================== world
mela.sky()
env = mela.build_mela(T_END)
sod = mela.add_lights(T_END)
cam = Cam()
cam.d.dof.use_dof = True
rnd = random.Random(11)


# ====================================================================== helpers
def lamp(name, kind, loc, energy, color=(1, 1, 1), shadow=False, size=0.3):
    d = bpy.data.lights.new(name, kind)
    d.energy, d.color, d.use_shadow = energy, color, shadow
    if kind in ("POINT", "SPOT"):
        d.shadow_soft_size = size
    elif kind == "AREA":
        d.size = size
    ob = bpy.data.objects.new(name, d)
    link(ob)
    ob.location = loc
    return ob


def lamp_windows(ob, wins, e):
    """energy e during each (t0,t1) window, 0 otherwise (constant keys)."""
    ANIM.put(ob.data, "energy", 0, 1, 0.0, "const")
    for a, b in wins:
        ANIM.put(ob.data, "energy", 0, int(F(a)), e, "const")
        ANIM.put(ob.data, "energy", 0, int(F(b)), 0.0, "const")


def vis(ob, wins):
    """render/viewport visibility during windows (constant keys)."""
    for p in ("hide_render", "hide_viewport"):
        ANIM.put(ob, p, 0, 1, 1, "const")
        for a, b in wins:
            ANIM.put(ob, p, 0, int(F(a)), 0, "const")
            ANIM.put(ob, p, 0, int(F(b)), 1, "const")


def text3d(body, size, mat, loc, rot=(math.pi / 2, 0, 0), extrude=0.0, align="CENTER"):
    c = bpy.data.curves.new("txt", "FONT")
    c.body, c.size, c.align_x, c.align_y, c.extrude = body, size, align, "CENTER", extrude
    ob = bpy.data.objects.new("txt", c)
    ob.data.materials.append(mat)
    link(ob)
    ob.location, ob.rotation_euler = loc, rot
    return ob


def pop(ob, t, dur=0.35, final=(1, 1, 1)):
    """hidden until t, then scales up with ease (keys on scale)."""
    for i in range(3):
        ANIM.put(ob, "scale", i, 1, 1e-4, "const")
        ANIM.put(ob, "scale", i, int(F(t)), 1e-4, "const")
    for k in range(1, 9):
        u = k / 8
        for i in range(3):
            ANIM.put(ob, "scale", i, int(F(t + dur * u)) + 0, 1e-4 + (final[i] - 1e-4) * ease(u))


COLS = dict(father=(0.72, 0.70, 0.62), mother=(0.62, 0.46, 0.14), uncle=(0.2, 0.34, 0.25), girl=(0.45, 0.36, 0.58),
            dhruv=(0.40, 0.52, 0.72), vendor=(0.42, 0.34, 0.22), dark=(0.10, 0.10, 0.12))


def extra(name, seed, H=None):
    r = random.Random(seed)
    H = H or r.uniform(1.55, 1.85)
    return Actor(name, H, r.choice(CROWD_COLORS), (0.1 + r.random() * 0.1, 0.1, 0.12 + r.random() * 0.1),
                 skin=r.choice("abcd"), build=r.uniform(0.9, 1.12), headwear=r.choice([None, None, "cap"]),
                 hw_col=r.choice(CROWD_COLORS))


def mouth(a, sd):
    sg = 1 if sd == "L" else -1
    return lambda t, u: (lambda j: j["head_c"] + j["tf"] * 0.1 * a.H + j["tl"] * 0.045 * a.H * sg + V(0, 0, -0.05 * a.H))(a.J(t))


def head_of(a, dz=0.0):
    return lambda t, u=0: a.J(t)["head_c"] + V(0, 0, dz)


def est(a, k=0.93):
    """estimated head position of another actor (no skeleton lookup, so no circular dependency)."""
    return lambda t, u=0: (lambda p: V(p[0], p[1], a.H * k))(a.pos_yaw(t))


def scan(a, amp=0.9, rate=0.9, far=6.0, ph=0.0):
    """look target sweeping left-right of the actor's heading (calling out / searching)."""
    def f(t, u):
        x, y, yaw = a.pos_yaw(t)[:3]
        return V(x, y, 0.93 * a.H) + fvec(yaw + amp * math.sin(t * rate * 2 * math.pi + ph)) * far
    return f


# ====================================================================== actors
FATHER = Actor("Father", 1.72, COLS["father"], (0.10, 0.10, 0.13), skin="b", hair=(0.03, 0.03, 0.03), sleeve=1.0)
MOTHER = Actor("Mother", 1.58, COLS["mother"], (0.15, 0.12, 0.10), skin="a", flags=("bun", "dupatta"), sleeve=1.0, build=0.95)
UNCLE = Actor("Uncle", 1.70, COLS["uncle"], (0.12, 0.11, 0.10), skin="c", build=1.08, sleeve=1.0)
GIRL = Actor("Cousin", 1.30, COLS["girl"], (0.35, 0.30, 0.40), skin="a", head_k=1.15, flags=("bun",), sleeve=1.0, build=0.9)
DHRUV = Actor("Dhruv", 1.25, COLS["dhruv"], (0.16, 0.16, 0.20), skin="b", head_k=1.25, flags=("pin",), sleeve=2.0, build=0.9)
VENDOR = Actor("Vendor", 1.66, COLS["vendor"], (0.22, 0.20, 0.17), skin="d", build=0.85, flags=("moustache", "scarf"), sleeve=1.0)
KEEPER = Actor("Keeper", 1.65, (0.4, 0.38, 0.3), (0.15, 0.13, 0.12), skin="c", flags=("moustache",), sleeve=1.0)
THIN = Actor("ThinMan", 1.82, (0, 0, 0), (0, 0, 0), build=0.82, headwear="cap", silhouette=True, sleeve=2.0)
MAN2 = Actor("Man2", 1.74, (0, 0, 0), (0, 0, 0), build=1.12, silhouette=True, sleeve=2.0)
SH_FAM = (FATHER, MOTHER, UNCLE, GIRL, DHRUV)

# ---- shared geometry
FY = math.radians(24.8)      # father yaw toward vendor in 12-17
VEN_P = (16.2, 3.5)
VEN_YAW = math.atan2(2.3 - 3.5, 13.6 - 16.2)
MOM_STALL = (2.3, 4.95)
DH_STALL = (3.2, 4.75)
FA_STALL = (4.1, 4.95)
N = math.pi / 2

# ---- S3/S4: family walks the lane (formation moves with G, heading +x)
g0, g1 = -10.0, -4.5
form = {"f": (0, -0.35), "d": (0, 0.15), "m": (0.1, 0.7), "c": (-0.1, 1.2), "u": (-1.3, 0.2)}
gy = -2.0
for a, k in ((FATHER, "f"), (DHRUV, "d"), (MOTHER, "m"), (GIRL, "c"), (UNCLE, "u")):
    fx, fyy = form[k]
    a.at(9, g0 + fx, gy + fyy, 0.0).walk(14, g1 + fx, gy + fyy, yaw=0.0).stay(17, 0.0)
# ---- S6-S9: the stall (20-36)
FATHER.at(20, *FA_STALL, N).stay(36)
MOTHER.at(20, *MOM_STALL, N).stay(33.5).stay(36, math.radians(-25), tt=1.2)
UNCLE.at(20, 5.3, 4.5, N).stay(36)
GIRL.at(20, 0.9, 4.3, N).stay(36)
KEEPER.at(20, 3.0, 6.9, -N).stay(36)
DHRUV.at(20, *DH_STALL, math.radians(-75)).stay(28)
DHRUV.walk(29.3, 4.7, 3.5, mode="smooth").walk(31.6, 9.0, 3.0).walk(32.0, 9.6, 2.95)
# ---- S10: the scatter (36-41), running
FATHER.at(36, *FA_STALL, N).walk(38.6, 12.5, 5.0, gait="run").walk(41, 14.0, 13.0, gait="run")
MOTHER.at(36, *MOM_STALL, 0.0).walk(41, -12.0, 4.0, gait="run")
UNCLE.at(36, 5.3, 4.5, N).walk(41, 18.0, -4.5, gait="run")
GIRL.at(36, 0.9, 4.3, N).walk(41, -6.0, -4.8, gait="run")
# ---- S11: callers at three places
FATHER.at(41, 33.4, 26.6, -N).stay(45)
MOTHER.at(42.3, -3.0, 4.6, -N).stay(45)
UNCLE.at(43.6, 28.5, -3.2, N).stay(45)
# ---- S12-S14 parents reach the vendor, S16-S17 hold
FATHER.at(45, 10.0, 0.8, 0.0).walk(48.3, 13.6, 2.3, gait="walk").stay(49.0, FY).stay(77, FY)
MOTHER.at(45, 9.2, 0.4, 0.0).walk(48.3, 13.83, 1.80, gait="walk").stay(49.2, FY).stay(77, FY)
VENDOR.at(17, *VEN_P, 3.5).stay(45).at(45, *VEN_P, VEN_YAW).stay(77)
# ---- S15 recreation
THIN.at(57, 12.6, -0.1, 0.0).walk(59.4, 16.4, 0.5, mode="smooth").stay(60.3, math.radians(-40)).walk(62, 19.7, -1.7, mode="smooth")
MAN2.at(57, 12.2, 0.8, 0.0).walk(59.4, 16.4, 1.35, mode="smooth").stay(60.3, math.radians(-40)).walk(62, 19.9, -1.1, mode="smooth")
DHRUV.at(57, 17.6, 0.7, math.pi).stay(60.2, math.pi).walk(62, 20.3, -1.45, yaw=math.radians(-40), mode="smooth")

# ---- extras with real walk cycles (S8 swallow, S9 speed-ramp crowd)
X = []
for i, (x, y0, y1, t0, t1) in enumerate([(6.0, -2.5, 6.0, 27.0, 31.4), (7.2, 7.0, -1.5, 27.5, 31.0), (8.0, -3.5, 5.5, 28.0, 31.6),
                                          (8.8, 6.5, 0.0, 28.0, 31.8), (9.8, -1.0, 6.5, 29.0, 32.0), (10.6, 5.5, 0.5, 28.5, 32.0),
                                          (7.0, 0.0, 6.0, 28.5, 32.0), (11.4, -2.0, 5.0, 29.5, 32.0)]):
    e = extra("X%d" % i, 100 + i)
    e.at(t0 - 0.01, x, y0, math.atan2(y1 - y0, 0.001)).walk(t1, x + 0.4, y1)
    X.append(e)
Y = []
for i in range(6):
    e = extra("Y%d" % i, 200 + i)
    y = 3.7 + (i % 3) * 0.22
    e.at(31.9 + i * 0.12, 8.5 + (i % 2), y, math.pi).walk(33.4, 3.2 + (i % 2), y, gait="run").walk(35.9, 0.0, y - 0.3 + (i % 3) * 0.2)
    Y.append(e)

# ---- gestures
# S3 laugh/eat
mv_happy = (-0.2, 0.9, 0.25)
FATHER.act(9, 14, armL=("loc", 0.05, 0.16, 0.50), look=est(DHRUV), mood=mv_happy, bob=0.004, bobf=1.8)
FATHER.act(14, 17, armL=("loc", 0.05, 0.16, 0.50), look=V(-1, 0, 1.2), mood=(0, 0.6, 0.0))
DHRUV.act(9, 17, armR=lambda t, u: FATHER.J(t)["hand"]["L"], mood=(0.0, 0.9, 0.3))
DHRUV.act(9.4, 11.5, look=est(FATHER), mood=(-0.1, 1.0, 0.4))
DHRUV.act(14.2, 15.4, look=est(FATHER), mood=(-0.2, 0.6, 0.2))
DHRUV.act(15.4, 17, look=V(16, 2.9, 2.5), mood=(-0.5, 0.2, 0.0))
MOTHER.act(9, 14, mood=(-0.2, 1.0, 0.45), bobf=2.0, bob=0.003, hp=-0.12, look=est(GIRL))
MOTHER.act(14, 17, mood=(0, 0.7, 0.1), look=V(-5, 3, 1.3))
GIRL.act(9, 14, bob=0.03, bobf=2.1, mood=(0, 1.0, 0.5))
GIRL.act(14, 17, mood=(0, 0.7, 0.2))
for a, b in ((9.4, 10.3), (11.6, 12.5)):
    UNCLE.act(a, b, armR=mouth(UNCLE, "R"), mood=(0, 0.5, 0.6), fade=0.2)
UNCLE.act(9, 17, look=V(0, 8, 1.4), mood=(0, 0.5, 0.0))
# S6 tug / bargain
tail = lambda t, u: MOTHER.J(t)["torso_M"] @ V(0, -MOTHER.sw * 1.02, MOTHER.torsoL * 0.85 - 0.3 * MOTHER.H) + V(0.05 * math.sin(t * 11), 0, 0.045 * math.sin(t * 11))
DHRUV.act(20, 24.3, armR=tail, look=est(MOTHER), mood=lambda t, u: (-0.9, -0.5, 0.5 + 0.4 * math.sin(t * 7)))
DHRUV.act(20.5, 22.4, armL=V(18, 2.0, 1.4))
DHRUV.act(22.4, 24.6, armL=lambda t, u: FATHER.J(t)["hand"]["L"])
DHRUV.act(24.6, 28, armL=lambda t, u: FATHER.J(t)["hand"]["L"], look=V(16, 3, 2.5), mood=(-0.7, -0.6, 0.0))
MOTHER.act(20, 32, look=est(KEEPER), armR=lambda t, u: ("loc", 0.38, -0.12, 0.62 + 0.07 * math.sin(t * 5)),
           mood=(0.2, 0.0, 0.5), lean=0.08)
FATHER.act(20, 32, look=est(KEEPER), armR=lambda t, u: ("loc", 0.35, -0.2, 0.62 + 0.06 * math.sin(t * 4.2)),
           mood=(0.3, 0.0, 0.4), armL=lambda t, u: ("loc", 0.05, 0.16, 0.50) if t < 28.4 else ("loc", 0.15, 0.2, 0.40))
KEEPER.act(20, 36, armR=lambda t, u: V(2.4, 5.9, 1.2 + 0.1 * math.sin(t * 6)), look=est(MOTHER), mood=(0, 0.2, 0.5))
UNCLE.act(20, 36, look=V(3, 8, 1.4))
GIRL.act(20, 36, look=V(14, 2, 2.5))
# S8 Dhruv leaves, parents unaware
DHRUV.act(28, 32, look=V(16, 2.9, 2.4), armR=("loc", 0.3, -0.1, 0.35), mood=(0, 0.3, 0.0))
# S9 mother turns and looks down at the empty spot (turn is in the waypoints: stay(...) with yaw)
MOTHER.acts = [x for x in MOTHER.acts if not (x[0] == 20 and x[1] == 32)]
MOTHER.act(20, 33.4, look=est(KEEPER), armR=lambda t, u: ("loc", 0.38, -0.12, 0.62 + 0.07 * math.sin(t * 5)),
           mood=(0.2, 0.0, 0.5), lean=0.08)
MOTHER.act(33.6, 36, look=lambda t, u: V(3.3, 4.6, 0.6) if t > 34.4 else V(4.4, 3.1, 1.4),
           mood=lambda t, u: (-0.9 * u, 0.7 - 1.5 * min(1, u * 1.6), 0.15), lean=0.12,
           armR=("rel", 0.0, -0.05, -0.33), armL=("loc", 0.05, 0.4, 0.4))
FATHER.act(32, 36, look=est(KEEPER), mood=(0.3, 0.0, 0.4))
# S10 scatter: calling while running
for a in (FATHER, MOTHER, UNCLE, GIRL):
    a.act(36.4, 41, look=scan(a, 0.7, 0.8), mood=(-0.6, -0.4, 0.8))
# S11 calling out
for a, (t0, t1) in ((FATHER, (41, 42.3)), (MOTHER, (42.3, 43.6)), (UNCLE, (43.6, 45.0))):
    a.act(t0, t1, fade=0.15, armL=mouth(a, "L"), armR=mouth(a, "R"), look=scan(a, 0.6, 0.9, 8, a.H), lean=-0.1,
          mood=lambda t, u: (-0.8, -0.5, 0.5 + 0.5 * abs(math.sin(t * 8))))
# S12 hurrying
FATHER.act(45, 48.4, mood=(-0.6, -0.5, 0.35), lean=0.08, look=V(16, 3, 1.7), bob=0.012, bobf=2.0)
MOTHER.act(45, 48.4, mood=(-0.6, -0.4, 0.1), lean=0.06, look=V(16, 3, 1.7))
VENDOR.act(17, 20, armR=("loc", 0.3, -0.2, 1.05), look=V(-4, -2, 1.3), mood=(0, 0.6, 0.5))
VENDOR.act(45, 48.4, armR=lambda t, u: ("loc", 0.2, -0.2, 0.9 + 0.12 * math.sin(t * 4)), look=V(10, 1, 1.5), mood=(0, 0.5, 0.5))
# S13 father: breathless question; vendor listens
FATHER.act(48.8, 52, lean=0.48, crouch=0.06, bob=0.012, bobf=1.3, look=est(VENDOR), mood=(-0.9, -0.5, 0.7),
           armL=lambda t, u: (lambda j: j["hip_c"] + j["tf"] * 0.12 + j["tl"] * 0.14 + V(0, 0, -0.2))(FATHER.J(t)),
           armR=lambda t, u: ("loc", 0.2, -0.15, 0.55 + 0.1 * math.sin(t * 3)))
MOTHER.act(48.8, 52, look=est(VENDOR), mood=(-0.9, -0.5, 0.0), armL=lambda t, u: ("loc", 0.15, 0.3, 0.7))
VENDOR.act(49, 52, look=est(FATHER), mood=(0, 0.1, 0.2))
# S14 vendor answers fast and points at the gate
VENDOR.act(52, 54.2, look=V(14, 5, 1.5), mood=lambda t, u: (0, 0.3, 0.6 * abs(math.sin(t * 9))), armL=("loc", 0.3, 0.25, 0.55))
VENDOR.act(54.2, 55.4, look=V(60, 3.5, 1.7), armR=V(60, 3.5, 1.5), mood=lambda t, u: (0, 0.2, 0.5 * abs(math.sin(t * 9))))
VENDOR.act(55.4, 57, look=V(14, 5, 1.5), mood=(0, 0.3, 0.0))
# S15: thin man gives the red balloon to Dhruv (silhouettes)
THIN.act(59.0, 60.3, crouch=0.14, lean=0.3, armR=("rel", 0.5, -0.1, -0.25))
THIN.act(60.4, 62, armL=("rel", 0.4, 0.15, -0.25))
MAN2.act(58.5, 62, armR=lambda t, u: ("loc", 0.15, -0.3, 0.7))
DHRUV.act(57, 62, mood=(-0.1, 0.2, 0.0), look=lambda t, u: est(THIN)(t, u) if t < 60.3 else V(21, -2, 1.1), armR=lambda t, u: THIN.J(t)["hand"]["R"] if t < 60.1 else ("rel", 0.1, -0.1, -0.1))
# S16 the words land
FATHER.act(62, 68, look=V(16.2, 3.5, 1.6), mood=lambda t, u: (-0.9, -0.8, 0.12 + 0.1 * math.sin(t * 2.2)), lean=0.0, bob=0.004, bobf=0.9)
MOTHER.act(62, 68, look=est(FATHER), mood=(-1.0, -0.8, 0.0),
           armL=lambda t, u: (lambda j: j["arms"]["R"][0] * 0.55 + j["arms"]["R"][1] * 0.45 + j["tl"] * -0.035 + V(0, 0, 0.0))(FATHER.J(t)))
VENDOR.act(62, 77, look=est(FATHER), mood=(0, 0.1, 0.0))
# S17 frozen parents
FATHER.act(68, 77, look=V(16.2, 3.5, 1.6), mood=(-0.9, -0.8, 0.1))
MOTHER.act(68, 77, armL=lambda t, u: mouth(MOTHER, "L")(t, u), look=V(16.2, 3.5, 1.6), mood=(-1.0, -0.9, 0.0))
# stall keeper / extras small acts
for e in X:
    e.act(26, 33, look=V(14, 3, 1.5))
for e in Y:
    e.act(31, 36, mood=(0, 0.1, 0.1))

# ---- bake windows (hide elsewhere)
FATHER_W = [(9, 16.95), (20, 42.3), (45, 57), (62, 77)]
MOTHER_W = [(9, 16.95), (20, 43.6), (45, 57), (62, 77)]
UNCLE_W = [(9, 16.95), (20, 45)]
GIRL_W = [(9, 16.95), (20, 41)]
DHRUV_W = [(9, 16.95), (20, 24.99), (28, 32.3), (57, 62)]
for a, wl in ((FATHER, FATHER_W), (MOTHER, MOTHER_W), (UNCLE, UNCLE_W), (GIRL, GIRL_W), (DHRUV, DHRUV_W)):
    for w in wl:
        a.bake(*w)
VENDOR.bake(17, 19.95)
VENDOR.bake(45, 77)
KEEPER.bake(20, 36)
THIN.bake(57, 62)
MAN2.bake(57, 62)
for e in X:
    e.bake(26, 32.2)
for e in Y:
    e.bake(31.8, 36)
for a in SH_FAM + (VENDOR, KEEPER, THIN, MAN2) + tuple(X) + tuple(Y):
    a.finalize(T_END)

# ====================================================================== props
# S7 macro hands (father's index finger, Dhruv's small fist slips off)
P7 = Vector((3.83, 4.95, 0.86))
skin_f, skin_d = M(SKIN["b"], 0.6), M(SKIN["b"], 0.6)
hand_f = empty("S7_fatherhand", P7)
new_obj("palm", box_mesh("palm", 0.085, 0.03, 0.095, False), skin_f, hand_f, loc=(0, 0, 0))
new_obj("idx", capsule_mesh("idx", 0.085, 0.0095), skin_f, hand_f, loc=(0, -0.03, 0.0), rot=(math.pi, 0, 0))
for i, dx in enumerate((-0.026, 0.0, 0.026, 0.045)):
    new_obj("fing%d" % i, capsule_mesh("fg", 0.045, 0.008), skin_f, hand_f, loc=(dx - 0.0, 0.02, 0.0), rot=(math.pi, 0, 0))
new_obj("sleeve", box_mesh("sl", 0.11, 0.07, 0.25), M((0.72, 0.70, 0.62), 0.9), hand_f, loc=(0, 0, 0.0), rot=(0, 0, 0))
kid = empty("S7_kidhand", P7 + Vector((0, -0.03, -0.06)))
new_obj("fist", sphere_mesh("fist", 0.034, 10, 8), skin_d, kid)
new_obj("kthumb", capsule_mesh("kth", 0.04, 0.009), skin_d, kid, loc=(0.0, -0.02, 0.0), rot=(math.pi / 2, 0, 0))
new_obj("ksleeve", capsule_mesh("ks", 0.18, 0.03), M(COLS["dhruv"], 0.9), kid, loc=(0, 0.02, 0.0), rot=(-math.radians(70), 0, 0))
for ob in (hand_f, kid):
    for ch in ob.children:
        vis(ch, [(25, 28)])
vis(hand_f, [(25, 28)])
vis(kid, [(25, 28)])
slip = [(25.0, (0.0, -0.03, -0.07)), (26.0, (0.0, -0.03, -0.075)), (26.9, (0.0, -0.032, -0.095)), (27.4, (-0.01, -0.04, -0.14)), (28.0, (-0.05, -0.06, -0.24))]
for t, o in slip:
    for i in range(3):
        ANIM.put(kid, "location", i, int(F(t)), P7[i] + o[i])
for ob in (hand_f,):
    ANIM.put(ob, "rotation_euler", 0, int(F(25)), 0.0)
    ANIM.put(ob, "rotation_euler", 0, int(F(28)), -0.08)

# S15 red balloon B, string
bal_mesh = env["balloon_mesh"]
balB = new_obj("RedBalloonB", bal_mesh, env["red_mat"])
strB = new_obj("RedBalloonB_str", capsule_mesh("str", 0.34, 0.004), M((0.8, 0.8, 0.8), 0.9))
strB.rotation_mode = "QUATERNION"
prevq = None
for f in range(int(F(57.3)), int(F(62)) + 1):
    t = (f - 1) / FPS
    hand = (THIN if t < 60.1 else DHRUV).J(t)["hand"]["R" if t < 60.1 else "R"]
    hp = hand + V(0.0, 0.0, 0.03)
    top = hp + V(0.03 * math.sin(t * 3), 0.02 * math.cos(t * 2.3), 0.38)
    for i in range(3):
        ANIM.put(balB, "location", i, f, (top + V(0, 0, 0.17))[i])
        ANIM.put(strB, "location", i, f, hp[i])
    q = seg_quat(hp, top, prevq)
    prevq = q
    for i, v in enumerate((q.w, q.x, q.y, q.z)):
        ANIM.put(strB, "rotation_quaternion", i, f, v)
vis(balB, [(57.3, 62)])
vis(strB, [(57.3, 62)])

# S16 sweat drops on the father's face
drop_m = M((0.8, 0.85, 0.9), 0.05, emit=(0.6, 0.7, 0.8), strength=0.4)
for k, (side, t0) in enumerate(((0.45, 62.5), (-0.5, 63.6), (0.2, 64.8), (-0.3, 66.0), (0.55, 66.9))):
    d = new_obj("sweat%d" % k, sphere_mesh("sw", 0.006, 6, 4, (1, 1, 1.4)), drop_m)
    fh = FATHER.hr
    for f in range(int(F(t0)), int(F(t0 + 1.6)) + 1, 2):
        t = (f - 1) / FPS
        u = (f - F(t0)) / (1.6 * FPS)
        j = FATHER.J(t)
        p = j["head_c"] + j["hf"] * fh * 0.93 + j["tl"] * side * fh * 0.7 + V(0, 0, fh * (0.75 - 1.4 * u * u))
        for i in range(3):
            ANIM.put(d, "location", i, f, p[i])
    vis(d, [(t0, t0 + 1.6)])

# S15 told-grade veil: a translucent grey plane glued to the camera
veil = new_obj("Veil", box_mesh("veil", 0.7, 0.42, 0.001, False), M((0.55, 0.57, 0.6), 1.0, alpha=0.3), cam.ob, loc=(0, 0, -0.3))
vis(veil, [(57, 62)])

# ====================================================================== special sets
# --- S17 map zoom cards (high above the mela)
def card(z, w, h, label, hl_w, hl_h, hl_label, gold=False):
    before = set(bpy.data.objects)
    _card(z, w, h, label, hl_w, hl_h, hl_label, gold)
    for o in set(bpy.data.objects) - before:
        vis(o, [(72.7, 77.1)])


def _card(z, w, h, label, hl_w, hl_h, hl_label, gold=False):
    cm = M((0.02, 0.05, 0.09), 1.0)
    new_obj("card", box_mesh("c", w, h, 2, False), cm, loc=(13.6, 1.9, z))
    ln = M((0.1, 0.6, 0.75), 0.5, emit=(0.1, 0.7, 0.9), strength=2.0)
    b = Builder()
    for i in range(-5, 6):
        b.box("g", (13.6 + i * w / 11, 1.9, z + 2.01), (w * 0.002, h, 0.02))
        b.box("g", (13.6, 1.9 + i * h / 11, z + 2.01), (w, h * 0.002, 0.02))
    b.box("g", (13.6, 1.9 + h / 2, z + 2.02), (w, h * 0.006, 0.03))
    b.box("g", (13.6, 1.9 - h / 2, z + 2.02), (w, h * 0.006, 0.03))
    b.box("g", (13.6 + w / 2, 1.9, z + 2.02), (w * 0.006, h, 0.03))
    b.box("g", (13.6 - w / 2, 1.9, z + 2.02), (w * 0.006, h, 0.03))
    b.build({"g": ln}, "grid")
    gm = M((0.9, 0.65, 0.1), 0.5, emit=(1.0, 0.7, 0.1), strength=4) if gold else ln
    hb = Builder()
    for sx, sy, ex, ey in ((-1, -1, 1, -1), (1, -1, 1, 1), (1, 1, -1, 1), (-1, 1, -1, -1)):
        hb.cyl("h", (13.6 + sx * hl_w / 2, 1.9 + sy * hl_h / 2, z + 2.1), (13.6 + ex * hl_w / 2, 1.9 + ey * hl_h / 2, z + 2.1), hl_w * 0.012, 4)
    hb.build({"h": gm}, "hl")
    tm = M((0.9, 0.95, 1.0), 0.5, emit=(0.9, 0.95, 1.0), strength=3)
    text3d(label, w * 0.07, tm, (13.6 - w * 0.4, 1.9 + h * 0.4, z + 2.2), rot=(0, 0, 0), align="LEFT")
    text3d(hl_label, hl_w * 0.13, gm, (13.6, 1.9 + hl_h * 0.62, z + 2.2), rot=(0, 0, 0))


card(180, 700, 440, "MIRZAPUR", 170, 110, "MELA GROUND")
card(1800, 14000, 8800, "UTTAR PRADESH", 3400, 2200, "MIRZAPUR")
card(15000, 120000, 72000, "LUCKNOW HQ", 18000, 11000, "UP POLICE HQ", gold=True)

# --- S18 macro uniform montage + rank ladder (black void far north)
V18 = Vector((0, 2000, 30))
black = M((0.0, 0.0, 0.0), 1.0)
new_obj("Void18", box_mesh("v", 400, 2, 200, False), black, loc=(V18.x, V18.y + 6, -20))
khaki, gold, brass, steel = M((0.42, 0.37, 0.22), 0.9), M((0.9, 0.7, 0.2), 0.3, 1.0), M((0.75, 0.55, 0.2), 0.3, 1.0), M((0.7, 0.72, 0.75), 0.25, 1.0)
beltm, platem, white = M((0.03, 0.03, 0.03), 0.5), M((0.02, 0.02, 0.025), 0.4), M((0.9, 0.9, 0.9), 0.4, emit=(1, 1, 1), strength=0.8)


def star_mesh(ro, ri, th):
    import bmesh
    bm = bmesh.new()
    pts = [(math.sin(i * math.pi / 5) * (ro if i % 2 == 0 else ri), math.cos(i * math.pi / 5) * (ro if i % 2 == 0 else ri)) for i in range(10)]
    ctr = bm.verts.new((0, 0, th))
    vt = [bm.verts.new((x, y, th)) for x, y in pts]
    for i in range(10):
        bm.faces.new((ctr, vt[i], vt[(i + 1) % 10]))
    ext = bmesh.ops.extrude_face_region(bm, geom=list(bm.faces))
    for v in [e for e in ext["geom"] if isinstance(e, bmesh.types.BMVert)]:
        v.co.z -= th
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return to_mesh("star", bm)


def item(i):
    return V18 + Vector((i * 1.5, 0, 0))


# 1 shoulder epaulette with three stars
p = item(0)
new_obj("epa", box_mesh("e", 0.12, 0.06, 0.012), khaki, loc=(p.x, p.y, p.z - 0.006), rot=(math.pi / 2, 0, 0))
new_obj("epa_b", box_mesh("e2", 0.12, 0.06, 0.004), M((0.05, 0.05, 0.05), 0.8), loc=(p.x, p.y - 0.006, p.z - 0.001), rot=(math.pi / 2, 0, 0))
for k in range(3):
    new_obj("star", star_mesh(0.0085, 0.0035, 0.004), gold, loc=(p.x - 0.03 + k * 0.03, p.y - 0.012, p.z + 0.0), rot=(math.pi / 2, 0, 0))
# 2 Ashoka emblem
p = item(1)
new_obj("ash_b", cyl_mesh("ab", 0.032, 0.008, 24), steel, loc=(p.x, p.y, p.z - 0.03), rot=(math.pi / 2, 0, 0))
for k in range(3):
    a = k * 2.0944
    new_obj("lion", sphere_mesh("l", 0.011, 8, 6, (1, 1, 1.4)), steel, loc=(p.x + 0.013 * math.cos(a), p.y - 0.012, p.z + 0.012 + 0.013 * math.sin(a) * 0))
new_obj("abacus", cyl_mesh("ab2", 0.026, 0.004, 24), steel, loc=(p.x, p.y - 0.009, p.z - 0.012), rot=(math.pi / 2, 0, 0))
new_obj("wheel", cyl_mesh("wh", 0.011, 0.004, 24), gold, loc=(p.x, p.y - 0.013, p.z - 0.012), rot=(math.pi / 2, 0, 0))
# 3 belt buckle
p = item(2)
new_obj("belt", box_mesh("bl", 0.22, 0.045, 0.006), beltm, loc=(p.x, p.y, p.z), rot=(math.pi / 2, 0, 0))
new_obj("buckle", box_mesh("bk", 0.06, 0.05, 0.008), brass, loc=(p.x, p.y - 0.005, p.z), rot=(math.pi / 2, 0, 0))
new_obj("buckle_in", cyl_mesh("bi", 0.015, 0.006, 24), steel, loc=(p.x, p.y - 0.012, p.z), rot=(math.pi / 2, 0, 0))
# 4 name plate
p = item(3)
new_obj("plate", box_mesh("pl", 0.1, 0.022, 0.004), platem, loc=(p.x, p.y, p.z), rot=(math.pi / 2, 0, 0))
text3d("RAVI", 0.014, white, (p.x, p.y - 0.0055, p.z), extrude=0.0006)
# 5 badge
p = item(4)
new_obj("badge", sphere_mesh("bd", 0.04, 16, 10, (1, 0.12, 1.2)), gold, loc=(p.x, p.y, p.z))
new_obj("badge_in", sphere_mesh("bd2", 0.028, 14, 8, (1, 0.12, 1.1)), M((0.05, 0.1, 0.35), 0.5), loc=(p.x, p.y - 0.004, p.z))
new_obj("badge_star", star_mesh(0.015, 0.006, 0.004), steel, loc=(p.x, p.y - 0.008, p.z + 0.004), rot=(math.pi / 2, 0, 0))
for i in range(5):
    pi_ = item(i)
    lamp("k18_%d" % i, "AREA", (pi_.x - 0.18, pi_.y - 0.35, pi_.z + 0.2), 3.0, (0.85, 0.92, 1.0), size=0.2)
    lamp("r18_%d" % i, "SPOT", (pi_.x + 0.25, pi_.y + 0.35, pi_.z + 0.12), 6.0, (1.0, 0.86, 0.72), size=0.05)
# ladder
LAD = V18 + Vector((24, 0, 0))
ranks = ["CONSTABLE", "HEAD CONSTABLE", "ASI", "SUB-INSPECTOR", "INSPECTOR", "DSP", "SP", "DIG", "ADG", "DGP"]
barm = M((0.1, 0.5, 0.65), 0.5, emit=(0.1, 0.5, 0.7), strength=1.5)
txtm = M((0.95, 0.97, 1.0), 0.5, emit=(0.95, 0.97, 1.0), strength=3)
for i, rk in enumerate(ranks):
    w = 2.4 + i * 0.35
    holder = empty("rank%d" % i, (LAD.x, LAD.y, LAD.z - 1.9 + i * 0.42))
    new_obj("bar", box_mesh("rb", w, 0.1, 0.34, False), barm, holder, loc=(0, 0, -0.17))
    text3d(rk, 0.2, txtm, (0, -0.07, 0.0)).parent = holder
    pop(holder, 90.4 + i * 0.4, 0.25)
for k, (q, tq) in enumerate((("SHO?", 92.4), ("IO?", 93.2), ("CO?", 94.0))):
    o = text3d(q, 0.7, M((0.9, 0.7, 0.15), 0.5, emit=(1.0, 0.75, 0.1), strength=5), (LAD.x + 5.0, LAD.y, LAD.z + 1.4 - k * 1.0))
    pop(o, tq, 0.3)
lamp("ladder_key", "AREA", (LAD.x, LAD.y - 6, LAD.z + 1), 120, (0.8, 0.9, 1.0), size=4)

# --- S19 title in the void
V19 = Vector((0, 3000, 30))
new_obj("Void19", box_mesh("v", 400, 2, 200, False), black, loc=(V19.x, V19.y + 40, -50))
redE = M((0.9, 0.01, 0.01), 0.3, emit=(1.0, 0.02, 0.01), strength=6)
whiteE = M((0.9, 0.9, 0.9), 0.4, emit=(0.95, 0.95, 0.95), strength=2.2)
tt = [text3d("OPERATION", 1.1, whiteE, (V19.x, V19.y + 20, V19.z + 3.8), extrude=0.05),
      text3d("RED", 2.6, redE, (V19.x, V19.y + 20, V19.z + 1.15), extrude=0.12),
      text3d("BALLOON", 1.1, whiteE, (V19.x, V19.y + 20, V19.z - 1.3), extrude=0.05)]
for o, d in zip(tt, (97.3, 97.7, 98.1)):
    pop(o, d, 0.4)
bal19 = new_obj("TitleBalloon", sphere_mesh("tb", 0.55, 20, 14, (1, 1, 1.18)), redE)
str19 = new_obj("TitleStr", cyl_mesh("ts", 0.012, 5.0, 6), M((0.8, 0.8, 0.8), 0.9))
for f in range(int(F(95)), int(F(100)) + 1):
    t = (f - 1) / FPS
    u = seg(t, 95.0, 100.0)
    p = Vector((0.5 * math.sin(t * 1.3), V19.y + 16, V19.z + lerp(-4.6, 6.0, u)))
    for i in range(3):
        ANIM.put(bal19, "location", i, f, p[i])
        ANIM.put(str19, "location", i, f, (p - V(0, 0, 5.55))[i])
vis(bal19, [(95, 100.2)])
vis(str19, [(95, 100.2)])
lamp("balloon_glow", "POINT", (V19.x, V19.y + 14, V19.z), 0.0, (1, 0.1, 0.05), size=0.2)

# S10 tracker rings so the four family figures read from 40 m up (previs aid, visible only in that shot)
ringm = M((1, 1, 1), 0.5, emit=(1, 1, 1), strength=2.5)
for a in (FATHER, MOTHER, UNCLE, GIRL):
    r_ = new_obj("ring_" + a.name, cyl_mesh("ring", 1.1, 0.03, 20), ringm)
    for f in range(int(F(36)), int(F(41)) + 1, 2):
        x, y = a.pos_yaw((f - 1) / FPS)[:2]
        ANIM.put(r_, "location", 0, f, x)
        ANIM.put(r_, "location", 1, f, y)
        ANIM.put(r_, "location", 2, f, 0.05)
    vis(r_, [(36, 41)])

# ====================================================================== lights per shot
l3 = lamp("warm3", "POINT", (-8, -1, 2.6), 0, (1.0, 0.82, 0.6))
ANIM.put(l3, "location", 0, int(F(9)), -10.0, "lin"); ANIM.put(l3, "location", 0, int(F(14)), -4.5, "lin")
lamp_windows(l3, [(9, 14)], 450)
l4 = lamp("key4", "POINT", (-3.0, -0.8, 1.8), 0, (1.0, 0.86, 0.72))
lamp_windows(l4, [(14, 17)], 90)
lh = lamp("heroLight", "POINT", (env["hero_pos"].x - 0.9, env["hero_pos"].y - 0.5, env["hero_pos"].z + 0.3), 0, (1.0, 0.8, 0.6), size=0.1)
lamp_windows(lh, [(18.7, 20)], 700)
l6 = lamp("key6", "POINT", (3.6, 3.5, 2.2), 0, (1.0, 0.86, 0.72))
lamp_windows(l6, [(20, 25), (28, 36)], 250)
l7 = lamp("key7", "AREA", (3.6, 4.3, 1.2), 0, (1, 0.95, 0.9), size=0.4)
lamp_windows(l7, [(25, 28)], 30)
l11 = [lamp("key11a", "POINT", (33.4, 24.6, 2.4), 0, (1.0, 0.86, 0.74)), lamp("key11b", "POINT", (-3.3, 3.0, 2.4), 0, (1.0, 0.86, 0.74)),
       lamp("key11c", "POINT", (28.8, -1.8, 2.4), 0, (1.0, 0.86, 0.74))]
for ob, w in zip(l11, ((41, 42.3), (42.3, 43.6), (43.6, 45))):
    lamp_windows(ob, [w], 200)
l13 = lamp("key13", "POINT", (13.5, 4.0, 2.4), 0, (1.0, 0.8, 0.6))
lamp_windows(l13, [(45, 57)], 160)
l16 = lamp("cold16", "POINT", (14.6, 2.2, 2.0), 0, (0.7, 0.85, 1.0), size=0.2)
lamp_windows(l16, [(62, 68)], 120)
l15 = lamp("cold15", "POINT", (14, 0.5, 3.0), 0, (0.6, 0.7, 0.9))
lamp_windows(l15, [(57, 62)], 250)
# the told-grade: sodium lamps dim during the recreation
for ob in sod:
    e = ob.data.energy
    ANIM.put(ob.data, "energy", 0, 1, e, "const")
    ANIM.put(ob.data, "energy", 0, int(F(57)), e * 0.35, "const")
    ANIM.put(ob.data, "energy", 0, int(F(62)), e, "const")

# ====================================================================== cameras
def G(t):
    return Vector((lerp(g0, g1, (t - 9) / 5), gy, 0))


def cam1(t):
    u = seg(t, 0, 5)
    return dict(pos=vl((-72, -78, 64), (-30, -34, 38), u), look=vl((18, 22, 3), (0, 2, 0), u), lens=24, fstop=22)


def cam2(t):
    return dict(pos=(-26, 64, 7.0), look=(-26, 0, 1.4), lens=135, focus=Vector((-26, 8, 1.5)), fstop=4.0)


def cam3(t):
    u = seg(t, 9, 14)
    phi = lerp(180, 20, u)
    r, h = lerp(3.2, 2.8, u), lerp(1.5, 1.4, u)
    c = G(t) + Vector((0, 0.3, 0))
    return dict(pos=c + orbit(phi, r, h), look=c + Vector((0.3, 0.1, 1.1)), lens=35, fstop=5.6, focus=c)


def orbit(phi, r, h):
    p = math.radians(phi)
    return Vector((r * math.cos(p), r * math.sin(p), h))


def cam4(t):
    return dict(pos=(-2.7, -1.85, 0.95), look=(-4.5, -1.92, 0.9), lens=50, fstop=2.8, focus=Vector((-4.5, -1.85, 0.9)))


def cam5(t):
    p = Vector((-4.5, -1.85, 1.08))
    d = lerp(4.5, 20.5, seg(t, 17.8, 19.2))
    return dict(pos=p, look=(16, 2.9, 2.4), lens=85, fstop=1.4, focus=d)


def cam6(t):
    u = seg(t, 20, 25)
    return dict(pos=vl((3.6, 2.4, 0.95), (3.35, 2.85, 0.95), u), look=(2.8, 4.8, 0.98), lens=50, fstop=4.0, focus=2.4)


def cam7(t):
    return dict(pos=(3.83, 4.35, 0.86), look=(3.83, 4.95, 0.84), lens=100, fstop=2.0, focus=0.6)


def cam8(t):
    p = Vector((-4.6, 4.5, 1.45))
    d = DHRUV.J(t)["head_c"]
    return dict(pos=p, look=(10, 3.3, 1.2), lens=85, fstop=2.0, focus=d)


def cam9(t):
    p = Vector((4.4, 3.1, 1.35))
    f1 = Vector((7.5, 3.8, 1.3))
    mom = MOTHER.J(t)["head_c"]
    k = seg(t, 33.4, 34.1)
    return dict(pos=p, look=mom * 0.7 + Vector((2.9, 4.5, 1.2)) * 0.3, lens=50, fstop=2.0, focus=(f1 * (1 - k) + mom * k))


def cam10(t):
    return dict(pos=(3.0, 4.2, 40), look=(3.0, 4.5, 0), lens=24, fstop=22)


def whip(t, t0, t1, base_pos, base_look, ang=110):
    u = ease((t - t0) / (t1 - t0))
    d = Vector(base_look) - Vector(base_pos)
    a = math.radians(ang) * u * u
    c, s = math.cos(a), math.sin(a)
    return Vector(base_pos) + Vector((d.x * c - d.y * s, d.x * s + d.y * c, d.z))


def cam11(t):
    if t < 42.3:
        p, l = V(33.4, 25.0, 1.5), V(33.4, 26.6, 1.55)
        w = (42.1, 42.3)
    elif t < 43.6:
        p, l = V(-3.4, 3.0, 1.5), V(-3.0, 4.6, 1.45)
        w = (43.4, 43.6)
    else:
        p, l = V(28.9, -1.6, 1.5), V(28.5, -3.2, 1.5)
        w = (99, 100)
    return dict(pos=p, look=whip(t, w[0], w[1], p, l), lens=25, fstop=4.0, focus=(l - p).length)


def cam12(t):
    u = seg(t, 45, 49)
    return dict(pos=vl((5.2, 0.4, 1.45), (7.6, 0.9, 1.45), u), look=(15.8, 3.2, 1.9), lens=35, fstop=5.6, focus=11.0)


def cam13(t):
    j = VENDOR.J(t)
    f = fvec(VEN_YAW)
    back, right = -f, -lvec(VEN_YAW)
    p = Vector((VEN_P[0], VEN_P[1], 0)) + back * 0.9 + right * 0.35 + V(0, 0, 1.5)
    fh = FATHER.J(t)["head_c"]
    return dict(pos=p, look=fh + V(0, 0, 0.0), lens=50, fstop=2.2, focus=(fh - p).length)


def cam14(t):
    vh = VENDOR.J(t)["head_c"]
    p = Vector((14.9, 4.6, 1.35))
    return dict(pos=p, look=vh + V(0, 0, 0.0), lens=85, fstop=2.2, focus=(vh - p).length)


def cam15(t):
    u = seg(t, 57, 62)
    a, b, c = THIN.J(t)["root"], MAN2.J(t)["root"], DHRUV.J(t)["root"]
    mid = (a + b + c) / 3 + V(0, 0, 1.15)
    return dict(pos=vl((10.2, -0.9, 1.45), (14.4, 0.0, 1.45), u), look=mid, lens=35, fstop=4.0, focus=(mid - Vector((10.2, -0.9, 1.45))).length)


def cam16(t):
    u = seg(t, 62, 68)
    j = FATHER.J(t)
    d = lerp(1.35, 1.0, u)
    p = j["head_c"] + fvec(FY) * d + V(0, 0, -0.03)
    return dict(pos=p, look=j["head_c"] + V(0, 0, -0.01), lens=100, fstop=2.8, focus=d)


C0 = Vector((13.6, 1.9, 1.2))


def cam17(t):
    if t < 72.8:
        u = seg(t, 68, 72.8)
        h = 0.9 * (170 / 0.9) ** u
        off = 1 - u
        pos = C0 + Vector((3.2 * off, -3.0 * off, 0)) + Vector((0, 0, h))
        look = C0 * (1 - u) + Vector((13.6, 2.3, 0)) * u
        return dict(pos=pos, look=look, lens=24, fstop=22)
    v = min(1.0, (t - 72.8) / 4.2)
    return dict(pos=(13.6, 1.9, 175 * (22000 / 175) ** (v ** 1.15)), look=(13.6, 2.4, 0), lens=24, fstop=22)


def cam18(t):
    k = 0
    for i, (a, b) in enumerate(((77, 79.6), (79.6, 82.2), (82.2, 85.0), (85.0, 87.6), (87.6, 90.2))):
        if a <= t < b:
            it = item(i)
            u = (t - a) / (b - a)
            x = it.x + lerp(-0.045, 0.045, u)
            return dict(pos=(x, it.y - 0.5, it.z + 0.012), look=(x + 0.004, it.y, it.z), lens=100, fstop=2.8, focus=0.5)
    u = seg(t, 90.2, 95)
    return dict(pos=(LAD.x + 1.2, LAD.y - lerp(9.0, 10.5, u), LAD.z + 0.3), look=(LAD.x + 1.2, LAD.y, LAD.z + 0.3), lens=35, fstop=16)


def cam19(t):
    return dict(pos=(0, V19.y, V19.z + 0.5), look=(0, V19.y + 20, V19.z + 1.2), lens=50, fstop=16)


HAND = {1: 0.15, 2: 0, 3: 0.5, 4: 0, 5: 0.25, 6: 1.3, 7: 0, 8: 0, 9: 0.15, 10: 0.1, 11: 1.8, 12: 0.45, 13: 1.3, 14: 0.2,
        15: 2.0, 16: 0.12, 17: 0.2, 18: 0, 19: 0}
FN = {1: cam1, 2: cam2, 3: cam3, 4: cam4, 5: cam5, 6: cam6, 7: cam7, 8: cam8, 9: cam9, 10: cam10, 11: cam11, 12: cam12,
      13: cam13, 14: cam14, 15: cam15, 16: cam16, 17: cam17, 18: cam18, 19: cam19}


def lens_wrap(n):
    def f(t):
        c = FN[n](t)
        c.setdefault("lens", LENS[n])
        return c
    return f


for n, (a, b) in SH.items():
    cam.shot(a, b, lens_wrap(n), hand=HAND[n], seed=n)

# ====================================================================== crowd
T = T_END
regions = [(-60, 60, -5.2, 5.2, 520), (-60, 60, 12.8, 19.2, 150), (-60, 60, -19.2, -12.8, 150), (-29, -23, -5, 26, 150, "y"),
           (11.6, 16.4, -5, 26, 60, "y"), (33.6, 38.4, -5, 26, 60, "y"), (-42, -12, 23, 44, 60), (24, 44, 22, 42, 50)]
walkers = make_crowd(1250, 5, regions, T)

# keep-out discs: protagonists + camera
disc = []
for a in SH_FAM + (VENDOR, KEEPER, THIN, MAN2) + tuple(X) + tuple(Y):
    for (w0, w1) in a.windows:
        t = w0
        while t <= w1:
            x, y = a.pos_yaw(t)[:2]
            disc.append((t, x, y, 0.75))
            t += 0.4
for n, (a, b) in SH.items():
    if n in (3, 4, 5, 6, 8, 9, 12, 13, 14, 15, 16, 11):
        t = a
        while t < b:
            p = FN[n](t)["pos"]
            disc.append((t, p[0], p[1], 0.8 if n not in (2, 8, 5) else 1.2))
            t += 0.3
disc.append((0, VAN.x, VAN.y, 3.4))
disc.append((0, POLE.x, POLE.y, 1.0))
disc.append((0, 8.3, -0.6, 0.8))
for cx in (25.0, 28.5, 32.0):
    disc.append((0, cx, -5.0, 1.1))
disc.append((0, -26, 32, 5.0))
disc.append((0, 34, 32, 1.3))
sample_t = [i * 0.4 for i in range(int(T / 0.4) + 1)]
by_t = {}
for (t, x, y, r) in disc:
    by_t.setdefault(round(t / 0.4), []).append((x, y, r))
static = [d for d in disc if d[0] == 0 and d[3] > 0.9 and False]


def hit(w):
    for k in range(int(T / 0.4) + 1):
        x, y = walker_pos(w, k * 0.4, T)
        for (px, py, r) in by_t.get(k, ()):
            if (x - px) ** 2 + (y - py) ** 2 < r * r:
                return True
        for (px, py, r) in by_t.get(0, ()):
            if r > 0.9 and (x - px) ** 2 + (y - py) ** 2 < r * r:
                return True
    return False


kept = [w for w in walkers if not hit(w)]
print("crowd", len(walkers), "->", len(kept))
n_ok = write_crowd(kept, T)
# some walkers carry red balloons (planted, not dominant)
red = env["red_mat"]
bm = env["balloon_mesh"]
cnt = 0
for i, w in enumerate(kept):
    if cnt >= 14 or w["sp"] < 0.05 or i % 61 != 7:
        continue
    cnt += 1
    b = new_obj("crowdBal%d" % i, bm, red)
    s_ = new_obj("crowdBalStr%d" % i, capsule_mesh("cs", 0.4, 0.004), M((0.8, 0.8, 0.8), 0.9))
    b.location = (w["x"], w["y"], 2.35)
    s_.location = (w["x"], w["y"], 1.85)
    for k in range(2):
        ANIM.put(b, "location", 0, int(F(0)) if k == 0 else int(F(T)), w["x"] if k == 0 else w["ex"], "lin")
        ANIM.put(b, "location", 1, int(F(0)) if k == 0 else int(F(T)), w["y"] if k == 0 else w["ey"], "lin")
        ANIM.put(s_, "location", 0, int(F(0)) if k == 0 else int(F(T)), w["x"] if k == 0 else w["ex"], "lin")
        ANIM.put(s_, "location", 1, int(F(0)) if k == 0 else int(F(T)), w["y"] if k == 0 else w["ey"], "lin")

# ====================================================================== finish
ANIM.flush()
for n, (a, b) in SH.items():
    scene.timeline_markers.new("S%02d" % n, frame=int(F(a)))
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("saved", OUT)
