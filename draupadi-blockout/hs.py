# hs.py - shared setup for the house scenes: build, all-lights-off baseline, door / almirah / mirror helpers,
# fairy lights, and a few repeated blocking helpers.
import math
import random

from mathutils import Vector

from kit import *
from film import *
import sets
from sets import H, step_z

HOUSE_LIGHTS = ("Sun", "Sky", "WinDR1", "WinDR2", "WinM", "WinMo", "WinCorr", "DoorDay", "Kitchen", "BulbM", "TubeCorr",
                "TubeDR", "Lamp", "Porch", "DRBulb", "MoBounce", "Moon")
EMIT = ("sky_win", "bulb", "bulb2", "tube", "tube2", "porch", "fairy")


def house(S):
    st = sets.build_house(S.END)
    S.state(0, **{k: 0 for k in HOUSE_LIGHTS})
    C = sets.mats()
    for k in EMIT:
        S.emit(0, C[k], 0.0)
    return st


def door_keys(st, pts):
    """pts: [(t, angle_deg, kind)] for both leaves."""
    for t, ang, kind in pts:
        for k, sg in (("doorL", 1), ("doorR", -1)):
            ANIM.put(st["P"][k], "rotation_euler", 2, F(t), sg * math.radians(ang), kind)


def almirah_keys(st, left=(), right=()):
    """almirah doors: 0 = shut, 90 = open. left/right: [(t, deg, kind)]."""
    for t, ang, kind in left:
        ANIM.put(st["P"]["alm_L"], "rotation_euler", 2, F(t), -math.radians(ang), kind)
    for t, ang, kind in right:
        ANIM.put(st["P"]["alm_R"], "rotation_euler", 2, F(t), math.radians(ang), kind)


def flaps(st, pts):
    """dressing-table mirror flaps: 0 = folded shut, 1 = open. pts [(t, k, kind)]."""
    for t, k, kind in pts:
        ANIM.put(st["P"]["flapL"], "rotation_euler", 2, F(t), math.radians(lerp(90, 225, k)), kind)
        ANIM.put(st["P"]["flapR"], "rotation_euler", 2, F(t), math.radians(lerp(-90, -225, k)), kind)


def fairy_strings(mat, seed=2):
    """wedding light strings: down the facade, over the door, along the step walls and the lane walls."""
    rnd = random.Random(seed)
    b = Builder()
    def string(p0, p1, sag, n):
        p0, p1 = Vector(p0), Vector(p1)
        for i in range(n + 1):
            u = i / n
            p = p0.lerp(p1, u) + Vector((0, 0, -sag * 4 * u * (1 - u)))
            b.sph("fairy", p, 0.022, 4, 3)
    for x in [-7.8 + i * 0.52 for i in range(31)]:                         # vertical drops down the facade
        string((x, -0.16, 3.6), (x, -0.16, 0.3 + rnd.uniform(0, 0.8)), 0.0, 14)
    string((-8, -0.2, 3.65), (8, -0.2, 3.65), 0.0, 70)
    string((-0.9, -0.2, 2.5), (0.9, -0.2, 2.5), 0.25, 10)
    for sx in (-1.4, 1.4):
        string((sx, -1.45, -0.15), (sx, -3.5, -0.65), 0.05, 12)
    for side in (-1, 1):
        for k in range(4):
            y0 = -4 - k * 4
            string((side * 4.3, y0, 0.75), (side * 4.3, y0 - 4, 0.75), 0.25, 14)
    for k in range(4):                                                     # canopy strings across the lane
        y = -5 - k * 3.2
        string((-4.3, y, 3.0), (4.3, y, 3.0), 0.6, 26)
    obs = b.build({"fairy": mat}, "FAIRY")
    return obs["fairy"]


def on_stairs(a):
    """z callable so an actor's feet follow the front steps."""
    return lambda t, u: step_z(a.pos_yaw(t)[1])


def hide_plates(st, wins=None):
    """the bright window plates sit outside the windows; hide them for exterior shots."""
    for k, ob in st["P"].items():
        if k.startswith("Plate"):
            if wins is None:
                ob.hide_render = ob.hide_viewport = True
            else:
                vis(ob, wins, inverse=True)


def mirror_probes(st):
    """planar reflection probes on the dressing-table mirror and both flaps (EEVEE planar probes)."""
    import bpy
    out = []
    dx, dy = H["dresser"]
    pd = bpy.data.lightprobes.new("MirrorProbeC", "PLANE")
    ob = bpy.data.objects.new("MirrorProbeC", pd)
    link(ob)
    ob.location = (dx + 0.065, dy, 1.25)
    ob.rotation_euler = (0, math.radians(-90), 0)
    ob.scale = (0.4, 0.26, 1)
    out.append(ob)
    for k, rx, sy in (("flapL", 90, -0.02), ("flapR", -90, 0.02)):
        pd = bpy.data.lightprobes.new("MirrorProbe" + k, "PLANE")
        ob = bpy.data.objects.new("MirrorProbe" + k, pd)
        link(ob)
        ob.parent = st["P"][k]
        ob.location = (0.15, sy, 0.37)
        ob.rotation_euler = (math.radians(rx), 0, 0)
        ob.scale = (0.14, 0.34, 1)
        out.append(ob)
    return out


def vanity_bulbs(t_on, t_off):
    """a row of bare bulbs round the dressing-table mirror (the bride's hard frontal key)."""
    dx, dy = H["dresser"]
    m = M((1, 0.9, 0.7), 0.4, emit=kelvin(2700), strength=0.0)
    for k, (oy, oz) in enumerate(((-0.3, 1.72), (-0.1, 1.74), (0.1, 1.74), (0.3, 1.72))):
        new_obj("VanityBulb", sphere_mesh("vb", 0.035, 8, 6), m, loc=(dx + 0.02, dy + oy, oz))
    L_ = lamp("VanityKey", "AREA", (dx - 0.05, dy, 1.72), 0, kelvin(2700), size=(0.15, 0.7))
    L_.rotation_euler = (0, math.radians(90 - 25), 0)
    return m, L_
