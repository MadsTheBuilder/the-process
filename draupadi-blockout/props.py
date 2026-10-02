# props.py - hand props and vehicles (all at real size). Each returns an object (root) to place / hold / bake.
import math
import random

import bmesh
from mathutils import Matrix, Quaternion, Vector

from kit import *
from film import kelvin

_m = {}


def mat(key, *a, **k):
    if key not in _m:
        _m[key] = M(*a, **k)
    return _m[key]


def suitcase(name="Suitcase", col=(0.20, 0.16, 0.12)):
    r = empty(name)
    new_obj(name + "_b", box_mesh(name + "b", 0.46, 0.2, 0.62), mat("case", col, 0.6), r, loc=(0, 0, 0.0))
    new_obj(name + "_h", box_mesh(name + "h", 0.14, 0.03, 0.04), mat("iron", (0.05, 0.05, 0.05), 0.5), r, loc=(0, 0, 0.62))
    return r


def duffel(name="Bag", col=(0.30, 0.26, 0.20)):
    r = empty(name)
    b = new_obj(name + "_b", capsule_mesh(name + "c", 0.46, 0.11), mat("duff", col, 0.9), r)
    b.rotation_euler = (0, math.pi / 2, 0)
    b.location = (-0.23, 0, 0.0)
    new_obj(name + "_s", box_mesh(name + "s", 0.02, 0.03, 0.42), mat("strap", (0.1, 0.08, 0.06), 0.8), r, loc=(0, 0, 0.1))
    return r


def book(name="Book", col=(0.3, 0.12, 0.08)):
    return new_obj(name, box_mesh(name, 0.16, 0.23, 0.025), mat("bk" + str(col), col, 0.7))


def paper(name="Paper"):
    return new_obj(name, box_mesh(name, 0.1, 0.15, 0.002), mat("paper", (0.85, 0.84, 0.8), 0.9))


def sweater(name="Sweater"):
    """an unfinished red sweater (folded knit) with two knitting needles."""
    r = empty(name)
    red = mat("redknit", (0.50, 0.02, 0.03), 0.95)
    new_obj(name + "_k", box_mesh(name + "k", 0.18, 0.04, 0.22, False), red, r)
    new_obj(name + "_s", box_mesh(name + "s", 0.06, 0.035, 0.12, False), red, r, loc=(0.1, 0, 0.04), rot=(0, 0.5, 0))
    for dx in (-0.03, 0.03):
        new_obj(name + "_n", cyl_mesh(name + "n", 0.003, 0.3, 4), mat("needle", (0.7, 0.7, 0.72), 0.3, 1.0), r,
                loc=(dx, 0.0, -0.05), rot=(0, 0.3 * (1 if dx > 0 else -1), 0))
    return r


def needle(name="Needle"):
    return new_obj(name, cyl_mesh(name, 0.003, 0.3, 4), mat("needle", (0.7, 0.7, 0.72), 0.3, 1.0))


def chain(name="Chain", turns=3, r=0.045, link=0.022):
    """heavy chain links coiled around a wrist (axis along local x)."""
    root = empty(name)
    steel = mat("chain", (0.45, 0.45, 0.47), 0.35, 1.0)
    n = int(turns * 2 * math.pi * r / link)
    for i in range(n):
        a = i / n * turns * 2 * math.pi
        x = (i / n - 0.5) * 0.12
        ob = new_obj(name + "_l", torus_mesh(link * 0.55, 0.0045), steel, root,
                     loc=(x, r * math.cos(a), r * math.sin(a)))
        ob.rotation_euler = (a + (math.pi / 2 if i % 2 else 0), 0.2, 0)
    # a length of chain hanging down from the coil
    for i in range(10):
        ob = new_obj(name + "_h", torus_mesh(link * 0.55, 0.0045), steel, root, loc=(0.07 + 0.0, 0.0, -r - i * link * 0.85))
        ob.rotation_euler = (0, math.pi / 2, (math.pi / 2) * (i % 2))
    return root


def torus_mesh(R, r):
    bm = bmesh.new()
    seg, ring = 10, 5
    vs = []
    for i in range(seg):
        a = i / seg * 2 * math.pi
        row = []
        for j in range(ring):
            b = j / ring * 2 * math.pi
            row.append(bm.verts.new(((R + r * math.cos(b)) * math.cos(a), (R + r * math.cos(b)) * math.sin(a), r * math.sin(b))))
        vs.append(row)
    for i in range(seg):
        for j in range(ring):
            bm.faces.new((vs[i][j], vs[(i + 1) % seg][j], vs[(i + 1) % seg][(j + 1) % ring], vs[i][(j + 1) % ring]))
    return to_mesh("torus", bm)


def thaali(name="Thaali"):
    r = empty(name)
    steel = mat("steel", (0.75, 0.76, 0.78), 0.15, 1.0)
    new_obj(name + "_p", cyl_mesh(name + "p", 0.15, 0.015, 24), steel, r)
    for i, (dx, dy) in enumerate(((0.06, 0.04), (-0.05, 0.05), (0.0, -0.07))):
        new_obj(name + "_k", cyl_mesh(name + "k", 0.035, 0.03, 12), steel, r, loc=(dx, dy, 0.015))
    new_obj(name + "_r", sphere_mesh(name + "r", 0.04, 8, 6, (1, 1, 0.4)), mat("roti", (0.7, 0.5, 0.25), 0.9), r, loc=(-0.06, -0.05, 0.02))
    return r


def ladle(name="Ladle"):
    r = empty(name)
    steel = mat("steel", (0.75, 0.76, 0.78), 0.15, 1.0)
    new_obj(name + "_h", cyl_mesh(name + "h", 0.006, 0.3, 6), steel, r)
    new_obj(name + "_c", sphere_mesh(name + "c", 0.035, 10, 6, (1, 1, 0.5)), mat("sabzi", (0.55, 0.35, 0.08), 0.6), r, loc=(0, 0, 0.32))
    return r


def poly_bag(name="PolyBag"):
    return new_obj(name, sphere_mesh(name, 0.09, 10, 8, (1, 0.6, 1.4)), mat("poly", (0.85, 0.85, 0.82), 0.3, alpha=0.7))


def lathi(name="Lathi"):
    return new_obj(name, cyl_mesh(name, 0.016, 1.6, 8), mat("bamboo", (0.42, 0.30, 0.15), 0.6))


def towel(name="Towel"):
    return new_obj(name, box_mesh(name, 0.3, 0.05, 0.45, False), mat("towel", (0.75, 0.70, 0.62), 1.0))


def dupatta_veil(name="Veil"):
    """red dupatta hanging over a face (for the bride): a draped box with a slight curve."""
    return new_obj(name, box_mesh(name, 0.42, 0.02, 0.62, False), mat("veil", (0.62, 0.02, 0.04), 0.9, alpha=0.88))


def photos_on_table(center, n=6, seed=1):
    r = empty("Photos", center)
    rnd = random.Random(seed)
    for i in range(n):
        p = new_obj("photo", box_mesh("ph", 0.1, 0.15, 0.003), mat("glossy", (0.4, 0.3, 0.28), 0.15), r,
                    loc=(rnd.uniform(-0.28, 0.28), rnd.uniform(-0.45, 0.45), 0.002 * i))
        p.rotation_euler.z = rnd.uniform(-0.4, 0.4)
    return r


def album(name="Album"):
    return new_obj(name, box_mesh(name, 0.28, 0.34, 0.05), mat("album", (0.25, 0.08, 0.06), 0.6))


def folder(name="Folder"):
    return new_obj(name, box_mesh(name, 0.24, 0.32, 0.03), mat("fold", (0.55, 0.45, 0.3), 0.8))


def rice_grain():
    return sphere_mesh("rice", 0.006, 5, 3, (1, 0.45, 0.45))


# ------------------------------------------------------------------ vehicles
def tuktuk(name="TukTuk"):
    """auto-rickshaw: front +x. ~2.6 m long."""
    r = empty(name)
    body = mat("tuk_y", (0.55, 0.45, 0.06), 0.5)
    green = mat("tuk_g", (0.08, 0.25, 0.12), 0.6)
    blk = mat("tuk_k", (0.03, 0.03, 0.03), 0.7)
    new_obj(name + "_floor", box_mesh("tf", 2.3, 1.3, 0.12), green, r, loc=(0, 0, 0.3))
    new_obj(name + "_seat", box_mesh("ts", 0.8, 1.2, 0.5), blk, r, loc=(-0.6, 0, 0.42))
    new_obj(name + "_back", box_mesh("tb", 0.15, 1.3, 0.75), green, r, loc=(-1.05, 0, 0.42))
    new_obj(name + "_roof", box_mesh("tr", 2.2, 1.35, 0.06), blk, r, loc=(-0.1, 0, 1.75))
    new_obj(name + "_cowl", box_mesh("tc", 0.5, 0.9, 1.3), green, r, loc=(0.95, 0, 0.42))
    new_obj(name + "_shield", box_mesh("tw", 0.04, 0.85, 0.5), mat("glass", (0.6, 0.65, 0.7), 0.05, alpha=0.3), r, loc=(1.15, 0, 1.2))
    for x, y in ((1.05, 0), (-0.75, 0.6), (-0.75, -0.6)):
        w = new_obj(name + "_w", cyl_mesh("tw", 0.22, 0.12, 14), blk, r, loc=(x, y - 0.06, 0.22))
        w.rotation_euler = (math.pi / 2, 0, 0)
    for z in (0.35, 1.7):
        new_obj(name + "_stripe", box_mesh("tsx", 2.2, 1.36, 0.06), body, r, loc=(-0.1, 0, z))
    return r


def wedding_car(name="WeddingCar"):
    """small white hatchback with marigold/rose garlands and fairy bulbs. Front +x, ~3.7 m."""
    r = empty(name)
    white = mat("car_w", (0.75, 0.75, 0.73), 0.3, 0.2)
    blk = mat("car_k", (0.02, 0.02, 0.02), 0.5)
    glass = mat("car_gl", (0.05, 0.06, 0.08), 0.05)
    new_obj(name + "_lower", box_mesh("cl", 3.7, 1.55, 0.7), white, r, loc=(0, 0, 0.25))
    new_obj(name + "_cabin", box_mesh("cc", 2.1, 1.45, 0.6), glass, r, loc=(-0.3, 0, 0.95))
    new_obj(name + "_rooftop", box_mesh("cr", 1.9, 1.4, 0.06), white, r, loc=(-0.35, 0, 1.53))
    for x in (1.2, -1.2):
        for y in (0.72, -0.72):
            w = new_obj(name + "_w", cyl_mesh("cw", 0.29, 0.18, 16), blk, r, loc=(x, y - 0.09 * (1 if y > 0 else -1) + 0.09, 0.29))
            w.rotation_euler = (math.pi / 2, 0, 0)
    marigold = mat("marigold", (0.85, 0.42, 0.02), 0.8)
    rose = mat("rose", (0.6, 0.02, 0.05), 0.8)
    fairy = mat("fairy_car", (1, 0.85, 0.5), 0.4, emit=kelvin(2400), strength=0.0)
    rnd = random.Random(3)
    # garlands looping over the bonnet and along the roof, bulbs along the roof edge
    for k in range(5):
        y = -0.6 + k * 0.3
        for i in range(14):
            u = i / 13
            p = (0.6 + u * 1.2, y, 0.95 + 0.05 * math.sin(u * math.pi))
            new_obj(name + "_g", sphere_mesh("g", 0.035, 6, 4), marigold if (i + k) % 3 else rose, r, loc=p)
    for i in range(24):
        u = i / 23
        for y in (0.72, -0.72):
            new_obj(name + "_b", sphere_mesh("b", 0.018, 6, 4), fairy, r, loc=(-1.25 + u * 1.9, y, 1.56))
    heart = new_obj(name + "_heart", sphere_mesh("ht", 0.25, 10, 8, (0.3, 1, 1)), rose, r, loc=(1.86, 0, 0.65))
    return r, fairy


def hand(name="Hand", skin=(0.50, 0.33, 0.24), sleeve=None, scale=1.0):
    """an articulated prop hand for inserts: root at the wrist, palm along local +y, fingers hinge at the knuckles
    (rotate hinge.rotation_euler.x negative to curl). Returns (root, [finger hinges], thumb hinge)."""
    sk = mat("skin" + str(skin), skin, 0.55)
    r = empty(name)
    s = scale
    new_obj(name + "_palm", box_mesh(name + "p", 0.08 * s, 0.09 * s, 0.025 * s, False), sk, r, loc=(0, 0.045 * s, 0))
    hs_ = []
    for i, dx in enumerate((-0.03, -0.01, 0.01, 0.03)):
        hg = empty(name + "_k%d" % i, (0, 0, 0), r)
        hg.location = (dx * s, 0.09 * s, 0)
        L = (0.075 - abs(dx) * 0.5) * s
        new_obj(name + "_f%d" % i, capsule_mesh(name + "f", L, 0.0085 * s), sk, hg, rot=(-math.pi / 2, 0, 0))
        hg.rotation_mode = "XYZ"
        hs_.append(hg)
    th = empty(name + "_th", (0, 0, 0), r)
    th.location = (0.04 * s, 0.02 * s, -0.005 * s)
    th.rotation_euler = (0, 0, -0.7)
    new_obj(name + "_thumb", capsule_mesh(name + "t", 0.055 * s, 0.01 * s), sk, th, rot=(-math.pi / 2, 0, 0))
    new_obj(name + "_arm", capsule_mesh(name + "a", 0.28 * s, 0.026 * s), sk, r, loc=(0, 0.0, 0), rot=(math.pi / 2, 0, 0))
    if sleeve:
        new_obj(name + "_sl", capsule_mesh(name + "s", 0.2 * s, 0.034 * s), mat("sl" + str(sleeve), sleeve, 0.9), r,
                loc=(0, -0.12 * s, 0), rot=(math.pi / 2, 0, 0))
    return r, hs_, th


def curl(fingers, pts):
    """pts [(t, amount 0..1)]: 0 straight, 1 fully curled (fist)."""
    for t, k in pts:
        for i, hg in enumerate(fingers):
            ANIM.put(hg, "rotation_euler", 0, F(t), -2.4 * k * (0.9 + 0.05 * i), "bez")
