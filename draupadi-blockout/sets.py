# sets.py - every location of the film at real scale, each at its own place in one world.
# Axes: x east, y north, z up, metres. Interior floors at z=0.
#   HOUSE    origin (0,0): drawing room, corridor, Mamta's room, Mother's room, kitchen, front steps, lane (ground -1.2)
#   SCHOOL   x 100..: classroom, veranda corridor, staff room, courtyard
#   STREET   y 200: small-town street
#   YARD     (200,200): hospital backyard with sheets on lines
#   RIVER    y -2000: dream river, boat, shore
# Lights are created at energy 0; scenes switch them with Ctx.state().
import math
import random

import bmesh
import bpy
from mathutils import Matrix, Vector

from kit import *
from film import lamp, aim, text3d, spin, kelvin, fog_box

C = {}          # material palette, filled by mats()


def mats():
    if C:
        return C
    C.update(
        wall_house=M((0.48, 0.50, 0.44), 0.95),        # grey-green distemper, dusty
        wall_dado=M((0.30, 0.32, 0.27), 0.95),
        wall_mamta=M((0.56, 0.52, 0.36), 0.95),        # faded yellow-ochre
        wall_mother=M((0.20, 0.30, 0.42), 0.95),       # muted blue (turns to water)
        wall_ext=M((0.50, 0.50, 0.47), 0.97),          # colourless facade
        floor_house=M((0.22, 0.20, 0.18), 0.6),        # old red-oxide / mosaic floor
        ceil=M((0.55, 0.55, 0.52), 0.95),
        wood=M((0.16, 0.08, 0.04), 0.55),
        wood_lt=M((0.30, 0.17, 0.08), 0.6),
        iron=M((0.05, 0.05, 0.05), 0.5, 0.8),
        rust=M((0.20, 0.09, 0.04), 0.8, 0.4),
        cushion=M((0.42, 0.33, 0.24), 0.95),
        cushion_red=M((0.35, 0.06, 0.06), 0.95),
        sheet=M((0.70, 0.70, 0.68), 0.9),
        blanket=M((0.32, 0.30, 0.42), 0.95),
        steel=M((0.75, 0.76, 0.78), 0.15, 1.0),
        glass=M((0.6, 0.65, 0.7), 0.05, alpha=0.25),
        mirror=M((0.9, 0.9, 0.9), 0.0, 1.0),
        net=M((0.85, 0.85, 0.8), 0.9, alpha=0.45),
        curtain=M((0.75, 0.72, 0.62), 0.9, alpha=0.6),
        photo=M((0.25, 0.22, 0.2), 0.3),
        ground=M((0.30, 0.27, 0.22), 1.0),             # dusty lane
        concrete=M((0.40, 0.39, 0.37), 0.95),
        clay=M((0.45, 0.20, 0.10), 0.9),
        leaf=M((0.08, 0.20, 0.06), 0.8),
        flower=M((0.9, 0.75, 0.15), 0.6),
        black=M((0.01, 0.01, 0.01), 1.0),
        school_wall=M((0.46, 0.36, 0.18), 0.95),       # ochre plaster like the reference
        school_dado=M((0.42, 0.24, 0.16), 0.95),
        blackboard=M((0.03, 0.05, 0.04), 0.7),
        bench=M((0.24, 0.14, 0.07), 0.7),
        column=M((0.62, 0.32, 0.24), 0.9),             # terracotta columns
        post=M((0.16, 0.18, 0.32), 0.7),               # blue posts
        tile=M((0.28, 0.13, 0.08), 0.8),
        shop=M((0.42, 0.40, 0.36), 0.95),
        shutter=M((0.32, 0.34, 0.36), 0.5, 0.6),
        awn1=M((0.25, 0.30, 0.38), 0.9), awn2=M((0.40, 0.33, 0.22), 0.9), awn3=M((0.30, 0.28, 0.26), 0.9),
        whitesheet=M((0.95, 0.95, 0.92), 0.9),
        water=M((0.012, 0.016, 0.022), 0.04),
        boat=M((0.10, 0.07, 0.05), 0.7),
        bank=M((0.06, 0.06, 0.05), 1.0),
        rope=M((0.55, 0.45, 0.30), 0.9),
    )
    # glowing materials (practicals); strengths are switched per shot
    C["bulb"] = M((1, 0.9, 0.7), 0.4, emit=kelvin(2700), strength=0.0)
    C["bulb2"] = M((1, 0.9, 0.7), 0.4, emit=kelvin(2900), strength=0.0)
    C["tube"] = M((0.9, 0.95, 1), 0.4, emit=(0.8, 1.0, 0.9), strength=0.0)
    C["tube2"] = M((0.9, 0.95, 1), 0.4, emit=(0.8, 1.0, 0.9), strength=0.0)
    C["porch"] = M((1, 0.9, 0.7), 0.4, emit=kelvin(3200), strength=0.0)
    C["fairy"] = M((1, 0.85, 0.5), 0.4, emit=kelvin(2500), strength=0.0)
    C["sky_win"] = M((0.02, 0.02, 0.02), 1.0, emit=(0.85, 0.9, 1.0), strength=0.0)      # bright window plates
    C["moon"] = M((1, 1, 1), 1.0, emit=(0.8, 0.88, 1.0), strength=30.0)
    return C


def wall(b, key, p0, p1, h, th=0.25, z0=0.0, holes=()):
    """wall along p0->p1 (centre line) with rectangular holes [(s0, s1, z_bottom, z_top)] measured along it."""
    p0, p1 = Vector((p0[0], p0[1], 0)), Vector((p1[0], p1[1], 0))
    d = p1 - p0
    L = d.length
    u = d / L
    ang = math.atan2(u.y, u.x)

    def piece(s0, s1, zb, zt):
        if s1 - s0 < 1e-3 or zt - zb < 1e-3:
            return
        c = p0 + u * ((s0 + s1) / 2)
        b.box(key, (c.x, c.y, z0 + (zb + zt) / 2), (s1 - s0, th, zt - zb), rz=ang)
    cur = 0.0
    for s0, s1, zb, zt in sorted(holes):
        piece(cur, s0, 0, h)
        piece(s0, s1, 0, zb)
        piece(s0, s1, zt, h)
        cur = s1
    piece(cur, L, 0, h)


def grille(b, key, p0, p1, z0, z1, step=0.11, r=0.011, horiz=(0.33, 0.66)):
    """vertical iron bars across an opening from p0 to p1 (in plan), z0..z1."""
    p0, p1 = Vector(p0), Vector(p1)
    n = max(2, int((p1 - p0).length / step))
    for i in range(1, n):
        q = p0.lerp(p1, i / n)
        b.cyl(key, (q.x, q.y, z0), (q.x, q.y, z1), r, 6)
    for k in horiz:
        z = z0 + (z1 - z0) * k
        b.box(key, ((p0.x + p1.x) / 2, (p0.y + p1.y) / 2, z), ((p1 - p0).length if abs(p1.x - p0.x) > abs(p1.y - p0.y) else 0.02,
                                                                  (p1 - p0).length if abs(p1.y - p0.y) >= abs(p1.x - p0.x) else 0.02, 0.025))


def box_obj(name, size, loc, mat, rz=0.0, parent=None):
    ob = new_obj(name, box_mesh(name, *size), mat, parent, loc=loc)
    ob.rotation_euler.z = rz
    return ob


def hinged(name, w, h, th, hinge, mat, rz0=0.0, flip=False):
    """door/flap object whose origin sits on its hinge; rotate about z to open."""
    me = box_mesh(name, w, th, h)
    me.transform(Matrix.Translation(((-w / 2) if flip else (w / 2), 0, 0)))
    ob = new_obj(name, me, mat, loc=hinge)
    ob.rotation_euler.z = rz0
    return ob


# ======================================================================================== HOUSE
# key coordinates (exported for blocking)
H = dict(
    door=Vector((0.0, 0.0)),                 # main door centre (south facade)
    dr_mid=Vector((0.0, 3.0)),               # drawing-room centre
    arch=Vector((-0.3, 6.0)),                # drawing room -> corridor opening
    sofa=Vector((4.35, 2.55)),               # sofa seat centre (against east wall, facing west)
    table=Vector((3.15, 2.55)),              # centre table
    cabinet=Vector((3.3, 5.7)),              # glass cabinet (north wall), faces south
    kitchen_door=Vector((5.0, 4.9)),
    lamp=Vector((4.55, 0.45)),               # table lamp, SE corner
    corr_y=6.8,                              # corridor centre line
    corr_win=Vector((-8.0, 6.8)),            # barred window at the corridor's west end
    in_win=Vector((-4.5, 7.6)),              # internal barred window into Mamta's room
    m_door=Vector((-1.45, 7.6)),             # Mamta's room door
    mo_door=Vector((2.5, 7.6)),              # Mother's room door
    m_bed=Vector((-1.3, 12.95)),            # Mamta's bed centre (NE corner, head north)
    almirah=Vector((-4.6, 13.3)),           # almirah front face centre
    m_win=Vector((-8.0, 10.4)),              # grille window (west), afternoon sun
    dresser=Vector((-0.75, 9.0)),            # dressing table (east wall), mirror faces west
    mo_bed=Vector((6.9, 12.95)),             # Mother's bed centre (NE corner)
    mo_win=Vector((8.0, 11.0)),              # Mother's window (east)
    mo_chair=Vector((5.45, 12.4)),
    mo_side=Vector((7.55, 11.25)),           # side table with steel jug
    crack=Vector((7.88, 9.7)),               # crack + flower in the east wall
    steps_top=Vector((0.0, -1.45)),
    ground=-1.2,
)
STEP_R, STEP_T, N_STEPS = 0.1714, 0.30, 7


def step_z(y):
    """ground height on the front steps at plan y (landing at 0 for y > -1.45)."""
    if y >= -1.45:
        return 0.0
    k = int((-1.45 - y) / STEP_T) + 1
    return max(-1.2, -STEP_R * k)


def build_house(t_end, night=False):
    c = mats()
    b = Builder()
    hgt = 3.2
    # ---- floors / ceilings / plinth
    b.box("floor_house", (0, 7.0, -0.05), (16.5, 14.5, 0.1))
    b.box("ceil", (0, 7.0, hgt + 0.1), (16.5, 14.5, 0.2))
    b.box("wall_ext", (0, 7.0, -0.62), (16.6, 14.6, 1.16))            # plinth below the house
    b.box("wall_ext", (0, 7.0, hgt + 0.45), (16.8, 14.8, 0.5))         # roof slab + parapet
    # ---- outer walls
    # south facade y=0: windows at x -3.8..-2.4 and 2.4..3.8, door -0.6..0.6 (s measured from x=-8)
    wall(b, "wall_ext", (-8.12, 0), (8.12, 0), hgt, holes=[(4.32, 5.72, 0.9, 2.3), (7.52, 8.72, 0, 2.35), (10.52, 11.92, 0.9, 2.3)])
    # north y=14
    wall(b, "wall_ext", (-8.12, 14), (8.12, 14), hgt)
    # west x=-8: corridor window y 6.2..7.4, Mamta's grille window y 9.6..11.2  (s measured from y=0)
    wall(b, "wall_ext", (-8, 0), (-8, 14), hgt, holes=[(6.2, 7.4, 0.9, 2.2), (9.6, 11.2, 0.8, 2.3)])
    # east x=8: Mother's window y 10.4..11.6 ; kitchen window y 1.5..2.7
    wall(b, "wall_ext", (8, 0), (8, 14), hgt, holes=[(1.5, 2.7, 1.0, 2.1), (10.4, 11.6, 1.0, 2.2)])
    # ---- inner walls
    wall(b, "wall_house", (-5, 0), (-5, 6), hgt, 0.2)                         # store | drawing room
    wall(b, "wall_house", (5, 0), (5, 6), hgt, 0.2, holes=[(4.4, 5.4, 0, 2.3)])  # drawing | kitchen (door)
    wall(b, "wall_house", (-8, 6), (8, 6), hgt, 0.2, holes=[(7.0, 8.4, 0, 2.5)])  # drawing | corridor (arch -1.0..0.4)
    # corridor north wall y=7.6: internal barred window x -5.3..-3.7, Mamta door -1.9..-1.0, Mother door 2.0..3.0
    wall(b, "wall_house", (-8, 7.6), (8, 7.6), hgt, 0.2, holes=[(2.7, 4.3, 0.8, 2.2), (6.1, 7.0, 0, 2.2), (10.0, 11.0, 0, 2.2)])
    wall(b, "wall_mamta", (-0.4, 7.7), (-0.4, 13.9), hgt, 0.2)                # Mamta | Mother
    # room paint layers (thin skins so each room has its own colour)
    for (x0, x1, y0, y1, key) in ((-7.86, -0.52, 7.72, 13.86, "wall_mamta"), (-0.28, 7.86, 7.72, 13.86, "wall_mother")):
        b.box(key, ((x0 + x1) / 2, y1 + 0.005, hgt / 2), (x1 - x0, 0.01, hgt))
    b.box("wall_mother", (7.865, 12.75, hgt / 2), (0.01, 2.2, hgt))
    b.box("wall_mother", (7.865, 8.95, hgt / 2), (0.01, 2.6, hgt))
    b.box("wall_mother", (7.865, 11.0, 0.5), (0.01, 1.2, 1.0))
    b.box("wall_mother", (7.865, 11.0, 2.7), (0.01, 1.2, 1.0))
    b.box("wall_mother", (-0.285, 10.8, hgt / 2), (0.01, 6.2, hgt))
    b.box("wall_mother", (5.45, 7.715, hgt / 2), (4.9, 0.01, hgt))
    b.box("wall_mother", (2.5, 7.715, 2.7), (1.0, 0.01, 1.0))
    b.box("wall_mother", (1.45, 7.715, hgt / 2), (1.1, 0.01, hgt))
    for (y0_, y1_, zb, zt) in ((7.7, 9.6, 0, 3.2), (11.2, 13.86, 0, 3.2), (9.6, 11.2, 0, 0.8), (9.6, 11.2, 2.3, 3.2)):
        b.box("wall_mamta", (-7.865, (y0_ + y1_) / 2, (zb + zt) / 2), (0.01, y1_ - y0_, zt - zb))
    for (x0_, x1_, zb, zt) in ((-7.86, -5.3, 0, 3.2), (-3.7, -1.9, 0, 3.2), (-1.0, -0.52, 0, 3.2), (-5.3, -3.7, 0, 0.8),
                               (-5.3, -3.7, 2.2, 3.2), (-1.9, -1.0, 2.2, 3.2)):
        b.box("wall_mamta", ((x0_ + x1_) / 2, 7.715, (zb + zt) / 2), (x1_ - x0_, 0.01, zt - zb))
    # dado band in drawing room / corridor
    for (x0, x1, y) in ((-4.9, 4.9, 0.13), (-4.9, -1.0, 5.89), (0.4, 4.9, 5.89)):
        b.box("wall_dado", ((x0 + x1) / 2, y, 0.45), (x1 - x0, 0.02, 0.9))
    # ---- grilles
    grille(b, "iron", (-8, 6.2), (-8, 7.4), 0.9, 2.2)
    grille(b, "rust", (-5.3, 7.6), (-3.7, 7.6), 0.8, 2.2, step=0.14, r=0.016)
    grille(b, "iron", (-8, 9.6), (-8, 11.2), 0.8, 2.3, step=0.12)
    grille(b, "iron", (8, 10.4), (8, 11.6), 1.0, 2.2, step=0.13)
    grille(b, "iron", (-3.8, 0), (-2.4, 0), 0.9, 2.3)
    grille(b, "iron", (2.4, 0), (3.8, 0), 0.9, 2.3)
    # window frames (wood)
    for (cx, cy, w, h_, z, rz) in ((-3.1, 0, 1.5, 1.5, 1.6, 0), (3.1, 0, 1.5, 1.5, 1.6, 0), (-8, 10.4, 1.7, 1.6, 1.55, math.pi / 2),
                                   (8, 11.0, 1.3, 1.3, 1.6, math.pi / 2), (-8, 6.8, 1.3, 1.4, 1.55, math.pi / 2)):
        for dz in (-h_ / 2, h_ / 2):
            b.box("wood", (cx, cy, z + dz), (w, 0.3, 0.07), rz=rz)
    # ---- DRAWING ROOM furniture
    sx, sy = H["sofa"]
    b.box("wood", (sx + 0.15, sy, 0.22), (0.8, 2.1, 0.12))                       # sofa base
    b.box("cushion", (sx + 0.05, sy, 0.36), (0.65, 1.95, 0.16))                  # seat (sags)
    b.box("cushion", (sx + 0.42, sy, 0.68), (0.16, 1.95, 0.55))                  # back
    for dy in (-1.08, 1.08):
        b.box("wood", (sx + 0.15, sy + dy, 0.45), (0.8, 0.08, 0.5))             # arms
    for dx, dy in ((-0.2, -1.0), (0.5, -1.0), (-0.2, 1.0), (0.5, 1.0)):
        b.cyl("wood", (sx + dx, sy + dy, 0), (sx + dx, sy + dy, 0.18), 0.03)
    b.box("cushion_red", (sx + 0.3, sy - 0.7, 0.6), (0.12, 0.38, 0.36), rz=0.1)
    tx, ty = H["table"]
    b.box("wood", (tx, ty, 0.42), (0.75, 1.2, 0.05))                             # centre table
    for dx, dy in ((-0.3, -0.5), (0.3, -0.5), (-0.3, 0.5), (0.3, 0.5)):
        b.box("wood", (tx + dx, ty + dy, 0.2), (0.05, 0.05, 0.4))
    for (ax, ay) in ((1.75, 1.1), (1.75, 4.0)):                                  # two armchairs facing east
        b.box("wood", (ax, ay, 0.4), (0.62, 0.62, 0.06))
        b.box("cushion", (ax, ay, 0.47), (0.55, 0.55, 0.08))
        b.box("wood", (ax - 0.3, ay, 0.75), (0.06, 0.6, 0.6))
        for dx, dy in ((-0.27, -0.27), (0.27, -0.27), (-0.27, 0.27), (0.27, 0.27)):
            b.box("wood", (ax + dx, ay + dy, 0.2), (0.05, 0.05, 0.4))
    cx_, cy_ = H["cabinet"]
    b.box("wood", (cx_, cy_ + 0.05, 0.95), (1.5, 0.45, 1.9))                     # cabinet body
    b.box("glass", (cx_, cy_ - 0.18, 1.3), (1.3, 0.02, 1.0))
    for i in range(6):                                                            # albums / files inside
        b.box("photo", (cx_ - 0.5 + i * 0.2, cy_ + 0.05, 0.55), (0.06, 0.3, 0.32))
    for i, (px, pz, w, h_) in enumerate(((4.88, 1.75, 0.5, 0.4), (4.88, 1.9, 0.35, 0.45), (4.88, 1.7, 0.4, 0.3))):
        b.box("photo", (px, 1.4 + i * 0.75, pz), (0.03, w, h_))                  # framed photos above the sofa
    b.box("photo", (-2.0, 5.87, 1.8), (0.4, 0.03, 0.55))                         # wall calendar
    b.box("photo", (1.9, 5.87, 2.35), (0.3, 0.03, 0.3))                          # wall clock
    # corridor / drawing-room furniture odds
    b.box("wood", (-4.6, 0.6, 0.4), (0.5, 0.9, 0.8))                             # side cabinet near window
    # ---- KITCHEN
    b.box("concrete", (7.4, 3.0, 0.45), (1.0, 5.6, 0.9))
    b.cyl("steel", (7.3, 3.4, 0.9), (7.3, 3.4, 1.12), 0.1)                       # pressure cooker
    # ---- MAMTA'S ROOM
    bx, by = H["m_bed"]
    b.box("wood", (bx, by, 0.25), (1.5, 2.0, 0.3))
    b.box("sheet", (bx, by - 0.05, 0.47), (1.4, 1.85, 0.14))
    b.box("sheet", (bx, by + 0.75, 0.6), (0.9, 0.3, 0.14))                       # pillow
    b.box("wood", (bx, by + 1.0, 0.65), (1.55, 0.08, 1.3))                       # headboard
    for dx in (-0.72, 0.72):
        b.cyl("wood", (bx + dx, by - 0.95, 0), (bx + dx, by - 0.95, 1.0), 0.04)
    dx_, dy_ = H["dresser"]
    b.box("wood", (dx_, dy_, 0.4), (0.45, 1.1, 0.8))                             # dressing table
    b.box("wood", (dx_ + 0.12, dy_, 1.25), (0.06, 0.62, 0.9))                    # centre mirror frame
    b.box("wood", (-1.45, 9.0, 0.22), (0.38, 0.38, 0.44))                        # stool
    ax_, ay_ = H["almirah"]
    b.box("wood", (ax_, ay_ + 0.275, 1.0), (1.3, 0.55, 2.0))                      # almirah body (front at ay_)
    b.box("wood", (ax_, ay_ + 0.275, 2.06), (1.4, 0.6, 0.12))
    b.box("black", (ax_, ay_ + 0.3, 1.02), (1.18, 0.45, 1.85))                    # dark interior
    b.box("wood", (-6.7, 8.2, 0.35), (1.0, 0.5, 0.7))                            # trunk / old desk
    # ---- MOTHER'S ROOM
    mx, my = H["mo_bed"]
    b.box("wood", (mx, my, 0.22), (1.3, 1.95, 0.26))
    b.box("sheet", (mx, my - 0.05, 0.42), (1.2, 1.85, 0.14))
    b.box("sheet", (mx, my + 0.72, 0.56), (0.8, 0.3, 0.16))
    b.box("wood", (mx, my + 0.98, 0.6), (1.35, 0.07, 1.1))
    sx2, sy2 = H["mo_side"]
    b.box("wood", (sx2, sy2, 0.3), (0.45, 0.45, 0.6))
    cx2, cy2 = H["mo_chair"]
    b.box("wood", (cx2, cy2, 0.44), (0.48, 0.48, 0.05))
    b.box("wood", (cx2 - 0.22, cy2, 0.8), (0.05, 0.46, 0.7))
    for ddx, ddy in ((-0.2, -0.2), (0.2, -0.2), (-0.2, 0.2), (0.2, 0.2)):
        b.box("wood", (cx2 + ddx, cy2 + ddy, 0.22), (0.04, 0.04, 0.44))
    b.box("wood", (1.6, 13.6, 0.9), (1.1, 0.5, 1.8))                             # Mother's old cupboard
    b.box("photo", (4.0, 13.84, 1.9), (0.5, 0.03, 0.6))                          # a framed god picture
    # ---- FRONT: landing, steps, lane, neighbours
    b.box("concrete", (0, -0.75, -0.05), (3.4, 1.5, 0.1))                         # landing
    for k in range(N_STEPS):
        y0 = -1.45 - k * STEP_T
        top = -STEP_R * (k + 1)
        b.box("concrete", (0, y0 - STEP_T / 2, (top - 1.2) / 2), (2.6, STEP_T, top + 1.2))
    for sxx in (-1.4, 1.4):                                                       # side walls of the steps
        b.box("wall_ext", (sxx, -2.4, -0.7), (0.2, 2.0, 1.0))
    b.box("ground", (0, -40, -1.25), (60, 78, 0.1))                               # lane ground
    b.box("ground", (0, 7, -1.25), (60, 20, 0.1))
    rnd = random.Random(3)
    for side in (-1, 1):
        b.box("wall_ext", (side * 4.3, -38, -0.25), (0.25, 70, 1.9))             # neighbour compound walls
        for k in range(6):                                                       # neighbour houses
            hh = rnd.uniform(4.0, 7.5)
            b.box("shop" if k % 2 else "wall_ext", (side * (7 + rnd.uniform(0, 2)), -8 - k * 11, -1.2 + hh / 2),
                  (5, rnd.uniform(7, 10), hh))
        for k in range(5):                                                       # electric poles
            px_ = side * 3.6
            py_ = -6 - k * 14
            b.cyl("concrete", (px_, py_, -1.2), (px_, py_, 6.5), 0.08)
    for k in range(4):                                                           # sagging wires
        b.cyl("black", (3.6, -6 - k * 14, 6.2), (3.6, -20 - k * 14, 6.0), 0.008, 4)
        b.cyl("black", (-3.6, -6 - k * 14, 6.2), (-3.6, -20 - k * 14, 6.0), 0.008, 4)
    # tree beside the house
    b.cyl("wood", (-6.5, -3.0, -1.2), (-6.5, -3.0, 3.2), 0.18)
    b.sph("leaf", (-6.5, -3.0, 4.6), 2.4, 10, 8, (1, 1, 0.75))
    # gamla with a struggling plant beside the stairs
    b.cyl("clay", (1.85, -2.6, -1.2), (1.85, -2.6, -0.82), 0.17, 12, 0.23)
    for i in range(4):
        a = i * 1.7
        b.cyl("leaf", (1.85, -2.6, -0.84), (1.85 + 0.09 * math.cos(a), -2.6 + 0.09 * math.sin(a), -0.6 + 0.04 * i), 0.006, 4)
    b.sph("leaf", (1.86, -2.58, -0.6), 0.045, 6, 4)
    obs = b.build(c, "HOUSE")
    # ---- separate (animated or switchable) pieces
    P = {}
    # main door: two leaves hinged at x=+-0.6 on the inner face, open inward (toward +y)
    P["doorL"] = hinged("DoorL", 0.6, 2.33, 0.06, (-0.6, 0.12, 0), c["wood"])
    P["doorR"] = hinged("DoorR", 0.6, 2.33, 0.06, (0.6, 0.12, 0), c["wood"], flip=True)
    P["doorL"].rotation_euler.z = 0
    # almirah doors (left door has the tally marks inside), hinged at the outer edges
    ax_, ay_ = H["almirah"]
    P["alm_L"] = hinged("AlmirahL", 0.6, 1.85, 0.035, (ax_ - 0.6, ay_ - 0.02, 0.08), c["wood_lt"])
    P["alm_R"] = hinged("AlmirahR", 0.6, 1.85, 0.035, (ax_ + 0.6, ay_ - 0.02, 0.08), c["wood_lt"], flip=True)
    tally(P["alm_L"])
    # mirror flaps on the dressing table (hinged on the centre mirror's edges), mirror glass
    dx_, dy_ = H["dresser"]
    P["mirC"] = box_obj("MirrorC", (0.02, 0.5, 0.78), (dx_ + 0.08, dy_, 0.86), c["mirror"])
    # flaps: closed = folded over the centre mirror; opened = angled 45 deg toward the sitter (-x)
    P["flapL"] = hinged("FlapL", 0.3, 0.74, 0.03, (dx_ + 0.05, dy_ - 0.3, 0.88), c["wood"], rz0=math.radians(90))
    P["flapR"] = hinged("FlapR", 0.3, 0.74, 0.03, (dx_ + 0.05, dy_ + 0.3, 0.88), c["wood"], rz0=math.radians(-90))
    for k, sy_ in (("flapL", -0.018), ("flapR", 0.018)):
        m = box_mesh("fg" + k, 0.26, 0.004, 0.66)
        m.transform(Matrix.Translation((0.15, sy_, 0.04)))
        new_obj(k + "_glass", m, c["mirror"], P[k])
    # net curtains in the facade windows, curtain in Mother's window, door curtain of Mamta's room
    for i, x in enumerate((-3.1, 3.1)):
        P["net%d" % i] = box_obj("Net%d" % i, (1.4, 0.01, 1.4), (x, 0.2, 0.9), c["net"])
    P["mo_curtain"] = box_obj("MoCurtain", (0.01, 1.3, 1.25), (7.82, 11.0, 0.98), c["curtain"])
    P["door_curtain"] = curtain_obj("DoorCurtain", 0.95, 2.1, (-1.45, 7.52, 0.08), c["curtain"])
    # crack + flower (sunrise payoff) on Mother's east wall
    P["flower"] = flower(H["crack"])
    # steel jug + glass on Mother's side table
    sx2, sy2 = H["mo_side"]
    P["jug"] = new_obj("SteelJug", cyl_mesh("jug", 0.07, 0.22, 16, 0.055), c["steel"], loc=(sx2 - 0.08, sy2 + 0.05, 0.6))
    P["glass"] = new_obj("SteelGlass", cyl_mesh("gls", 0.035, 0.1, 12, 0.03), c["steel"], loc=(sx2 + 0.1, sy2 - 0.08, 0.6))
    # ceiling fans: Mother's room + drawing room
    for name, (x, y) in (("FanMo", (5.2, 11.0)), ("FanDR", (0.0, 3.0))):
        hub = new_obj(name, cyl_mesh(name + "h", 0.12, 0.12, 12), c["wood"], loc=(x, y, hgt - 0.45))
        new_obj(name + "_rod", cyl_mesh(name + "r", 0.02, 0.4, 6), c["iron"], hub, loc=(0, 0, 0.05))
        for k in range(3):
            bl = new_obj(name + "_b%d" % k, box_mesh(name + "bl", 0.6, 0.12, 0.01), c["wood"], hub, loc=(0, 0, 0.04))
            bl.data.transform(Matrix.Translation((0.38, 0, 0)))
            bl.rotation_euler.z = k * 2.0944
        P[name] = hub
    # practicals: bulbs, tubes, lamp shade, porch light
    P["bulb_m"] = new_obj("BulbMamta", sphere_mesh("bm", 0.05, 10, 8), c["bulb"], loc=(-3.6, 11.2, 2.55))
    new_obj("BulbMamta_wire", cyl_mesh("bmw", 0.006, 0.6, 4), c["black"], P["bulb_m"], loc=(0, 0, 0.04))
    P["tube_corr"] = box_obj("TubeCorrFixture", (1.2, 0.05, 0.05), (-2.5, 7.48, 2.6), c["tube"])
    P["tube_dr"] = box_obj("TubeDRFixture", (1.2, 0.05, 0.05), (0.0, 5.85, 2.75), c["tube2"])
    P["shade"] = new_obj("LampShade", cyl_mesh("shd", 0.2, 0.25, 14, 0.12), c["cushion"], loc=(H["lamp"].x, H["lamp"].y, 0.95))
    new_obj("LampBody", cyl_mesh("lb", 0.06, 0.95, 8), c["wood"], loc=(H["lamp"].x, H["lamp"].y, 0.0))
    P["lampbulb"] = new_obj("LampBulb", sphere_mesh("lbb", 0.05, 8, 6), c["bulb2"], loc=(H["lamp"].x, H["lamp"].y, 1.02))
    P["porch"] = new_obj("PorchBulb", sphere_mesh("pb", 0.06, 8, 6), c["porch"], loc=(0.0, -0.35, 2.55))
    box_obj("PorchBracket", (0.05, 0.3, 0.05), (0.0, -0.18, 2.62), c["iron"])
    # window "sky" plates outside each window so a frame shows bright daylight, not void
    for name, (x, y, w, h_, z, rz) in (("PlateS1", (-3.1, -0.8, 2.4, 2.5, 1.6, 0)), ("PlateS2", (3.1, -0.8, 2.4, 2.5, 1.6, 0)),
                                       ("PlateMW", (-8.9, 10.4, 2.6, 2.8, 1.5, math.pi / 2)),
                                       ("PlateMoW", (8.9, 11.0, 2.2, 2.4, 1.6, math.pi / 2)),
                                       ("PlateCW", (-8.9, 6.8, 2.2, 2.4, 1.5, math.pi / 2))):
        P[name] = box_obj(name, (w, 0.02, h_), (x, y, z - h_ / 2), c["sky_win"], rz=rz)
        P[name].visible_shadow = False
    # ---- LIGHTS (all start at 0; scenes switch them)
    L = {}
    L["Sun"] = lamp("Sun", "SUN", (0, 0, 20), 0, size=math.radians(1.2))
    L["Sky"] = lamp("Sky", "SUN", (0, 0, 20), 0, size=math.radians(40), shadow=True)
    L["WinDR1"] = lamp("WinDR1", "AREA", (-3.1, -0.3, 1.6), 0, size=(1.4, 1.4))
    L["WinDR2"] = lamp("WinDR2", "AREA", (3.1, -0.3, 1.6), 0, size=(1.4, 1.4))
    L["WinM"] = lamp("WinM", "AREA", (-8.3, 10.4, 1.55), 0, size=(1.6, 1.5))
    L["WinMo"] = lamp("WinMo", "AREA", (8.3, 11.0, 1.6), 0, size=(1.2, 1.2))
    L["WinCorr"] = lamp("WinCorr", "AREA", (-8.3, 6.8, 1.55), 0, size=(1.2, 1.3))
    L["DoorDay"] = lamp("DoorDay", "AREA", (0.0, -0.6, 1.2), 0, size=(1.2, 2.3))
    L["Kitchen"] = lamp("Kitchen", "POINT", (6.6, 4.0, 2.3), 0, size=0.15)
    L["BulbM"] = lamp("BulbM", "POINT", (-3.6, 11.2, 2.45), 0, size=0.04)
    L["TubeCorr"] = lamp("TubeCorr", "AREA", (-2.5, 7.4, 2.55), 0, size=(1.2, 0.1))
    L["TubeDR"] = lamp("TubeDR", "AREA", (0.0, 5.75, 2.7), 0, size=(1.2, 0.1))
    L["Lamp"] = lamp("Lamp", "POINT", (H["lamp"].x, H["lamp"].y, 1.0), 0, size=0.08)
    L["Porch"] = lamp("Porch", "POINT", (0.0, -0.45, 2.45), 0, size=0.06)
    L["DRBulb"] = lamp("DRBulb", "POINT", (0.3, 3.0, 2.6), 0, size=0.05)
    L["MoBounce"] = lamp("MoBounce", "AREA", (5.2, 9.0, 2.9), 0, size=2.5, shadow=False)
    L["Moon"] = lamp("Moon", "SUN", (0, 0, 30), 0, size=math.radians(2.5))
    # area lights emit along local -Z: Rx(+90) -> +y, Ry(-90) -> +x, Ry(+90) -> -x, identity -> down
    for k in ("WinDR1", "WinDR2", "DoorDay"):
        L[k].rotation_euler = (math.radians(90), 0, 0)
    L["WinM"].rotation_euler = (0, math.radians(-90), 0)
    L["WinCorr"].rotation_euler = (0, math.radians(-90), 0)
    L["WinMo"].rotation_euler = (0, math.radians(90), 0)
    spin(P["FanMo"], "Z", 0.9, t_end)
    spin(P["FanDR"], "Z", 0.0, t_end)
    return dict(obs=obs, P=P, L=L)


def sun_dir(ob, az_deg, el_deg):
    """point a SUN lamp so light travels FROM azimuth az (deg, 0=+x east, 90=+y north) at elevation el."""
    d = -Vector((math.cos(math.radians(az_deg)) * math.cos(math.radians(el_deg)),
                 math.sin(math.radians(az_deg)) * math.cos(math.radians(el_deg)), math.sin(math.radians(el_deg))))
    ob.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def sun_keys(ob, t, az_deg, el_deg):
    d = -Vector((math.cos(math.radians(az_deg)) * math.cos(math.radians(el_deg)),
                 math.sin(math.radians(az_deg)) * math.cos(math.radians(el_deg)), math.sin(math.radians(el_deg))))
    e = d.to_track_quat("-Z", "Y").to_euler()
    for i in range(3):
        ANIM.put(ob, "rotation_euler", i, int(round(F(t))), e[i], "const")


def tally(door):
    """carvings on the inside face (local +y) of the almirah's left door: F 28, M 31, A 30, M 12 (stops).
    Seen from the room with the door open, local x runs right-to-left, so rows start at high x."""
    m = M((0.04, 0.025, 0.012), 0.9)
    rows = (("F", 28), ("M", 31), ("A", 30), ("M", 12))
    z = 1.62
    for label, n in rows:
        t = text3d(label, 0.075, m, (0, 0, 0), rot=(math.pi / 2, 0, math.pi), extrude=0.002, align="LEFT")
        t.parent = door
        t.location = (0.56, 0.022, z - 0.03)
        x = 0.47
        for g in range((n + 4) // 5):
            k = min(5, n - g * 5)
            for i in range(min(k, 4)):
                new_obj("tal", box_mesh("tl", 0.005, 0.004, 0.06, False), m, door, loc=(x - i * 0.013, 0.021, z))
            if k == 5:
                st = new_obj("tals", box_mesh("tls", 0.062, 0.004, 0.005, False), m, door, loc=(x - 0.02, 0.021, z))
                st.rotation_euler.y = math.radians(40)
            x -= 0.075
            if x < 0.06:
                x = 0.47
                z -= 0.08
        z -= 0.12


def curtain_obj(name, w, h, loc, mat):
    """a hanging curtain (doorway): a subdivided plane with a wave modifier so it ripples."""
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=16, y_segments=16, size=0.5)
    for v in bm.verts:
        v.co = Vector((v.co.x * w, (v.co.y + 0.5) * h, 0))
    me = to_mesh(name, bm)
    ob = new_obj(name, me, mat, loc=loc, rot=(math.pi / 2, 0, 0))
    wv = ob.modifiers.new("wave", "WAVE")
    wv.use_normal = False
    wv.use_y = True
    wv.use_x = False
    wv.height = 0.03
    wv.width = 0.6
    wv.speed = 0.04
    return ob


def flower(p):
    c = mats()
    root = empty("Flower", (p.x, p.y, 0.95))
    new_obj("crack", box_mesh("ck", 0.02, 0.02, 0.6, False), c["black"], root, loc=(0, 0, -0.1), rot=(0.25, 0, 0))
    new_obj("crack2", box_mesh("ck2", 0.02, 0.015, 0.35, False), c["black"], root, loc=(0, 0.06, 0.1), rot=(-0.5, 0, 0))
    new_obj("stem", cyl_mesh("st", 0.004, 0.22, 4), c["leaf"], root, loc=(-0.02, 0, 0), rot=(0, -0.5, 0))
    new_obj("leafA", sphere_mesh("lf", 0.03, 6, 4, (1, 0.3, 0.5)), c["leaf"], root, loc=(-0.06, 0.02, 0.08))
    hd_ = new_obj("bloom", sphere_mesh("bl", 0.035, 10, 6, (1, 1, 0.45)), c["flower"], root, loc=(-0.11, 0, 0.2), rot=(0, -1.0, 0))
    new_obj("bloomc", sphere_mesh("bc", 0.012, 6, 4), M((0.4, 0.2, 0.02), 0.6), hd_, loc=(0, 0, 0.012))
    return root


# ======================================================================================== SCHOOL
S = dict(
    cls_x0=100.0, cls_x1=109.0, cls_y0=0.0, cls_y1=12.0,
    teacher=Vector((104.5, 10.6)),             # teacher's table centre
    board=Vector((104.5, 11.85)),
    cls_door=Vector((109.0, 10.55)),           # classroom door (east wall)
    corr_x=110.5,                              # veranda centre line (x)
    staff_door=Vector((109.0, 17.5)),
    staff_seat=Vector((106.0, 17.4)),          # Papa's chair, back to the door
    bell=Vector((109.12, 13.3, 2.15)),
)
DESK_X = (101.2, 102.9, 106.1, 107.8)          # 4 desk columns, 2 kids each; centre aisle x 103.7..105.3
DESK_Y = [2.2 + i * 1.25 for i in range(6)]


def desk_seat(ci, ri, k):
    """seat point for kid k (0/1) at desk column ci, row ri (kids face north)."""
    return Vector((DESK_X[ci] - 0.4 + k * 0.8, DESK_Y[ri] - 0.55))


def build_school(t_end):
    c = mats()
    b = Builder()
    x0, x1, y0, y1 = S["cls_x0"], S["cls_x1"], S["cls_y0"], S["cls_y1"]
    hgt = 3.6
    b.box("floor_house", (104.5, 14, -0.05), (24, 60, 0.1))
    b.box("ceil", ((x0 + x1) / 2, (y0 + 22) / 2, hgt + 0.1), (9.4, 22.4, 0.2))
    # classroom walls: west windows, east door, north board
    wall(b, "school_wall", (x0, y0 - 0.12), (x0, y1 + 0.12), hgt, holes=[(1.6, 3.6, 0.9, 2.8), (4.8, 6.8, 0.9, 2.8), (8.0, 10.0, 0.9, 2.8)])
    wall(b, "school_wall", (x0 - 0.12, y0), (x1 + 0.12, y0), hgt)
    wall(b, "school_wall", (x0 - 0.12, y1), (x1 + 0.12, y1), hgt)
    wall(b, "school_wall", (x1, y0 - 12), (x1, 26), hgt, holes=[(12 + 10.0, 12 + 11.1, 0, 2.4), (12 + 17.0, 12 + 18.0, 0, 2.3),
                                                            (12 + 3.0, 12 + 4.5, 1.0, 2.2)])
    # staff room (north of the classroom): x 103..109, y 14..22, window on the west wall behind Papa
    wall(b, "school_wall", (103, 14), (109, 14), hgt)
    wall(b, "school_wall", (103, 22), (109, 22), hgt)
    wall(b, "school_wall", (103, 14), (103, 22), hgt, holes=[(2.8, 4.4, 0.9, 2.5)])
    for (xa, xb, ya) in ((x0, x1, y0 + 0.13), (x0, x1, y1 - 0.13)):
        b.box("school_dado", ((xa + xb) / 2, ya, 0.5), (xb - xa, 0.02, 1.0))
    b.box("school_dado", (x0 + 0.13, 6, 0.45), (0.02, 12, 0.9))
    # blackboard + its wooden shutters, teacher's table + chair
    bx_, by_ = S["board"]
    b.box("blackboard", (bx_, by_, 1.65), (4.0, 0.04, 1.3))
    b.box("tile", (bx_, by_ + 0.02, 1.65), (4.2, 0.03, 1.5))
    for dx in (-2.9, 2.9):
        b.box("wood_lt", (bx_ + dx, by_ - 0.02, 1.4), (1.4, 0.05, 2.0))
    tx, ty = S["teacher"]
    b.box("bench", (tx, ty, 0.76), (1.5, 0.75, 0.05))
    for dx, dy in ((-0.7, -0.33), (0.7, -0.33), (-0.7, 0.33), (0.7, 0.33)):
        b.box("bench", (tx + dx, ty + dy, 0.38), (0.05, 0.05, 0.76))
    b.box("bench", (tx + 0.2, ty + 0.75, 0.45), (0.45, 0.45, 0.05))
    b.box("photo", (tx - 0.4, ty, 0.8), (0.3, 0.22, 0.05))                        # register/books
    # platform under the board
    b.box("concrete", (bx_, 11.2, 0.08), (8.8, 1.6, 0.16))
    # desks + benches
    for xc in DESK_X:
        for yc in DESK_Y:
            b.box("bench", (xc, yc, 0.68), (1.6, 0.45, 0.05))
            b.box("bench", (xc, yc + 0.2, 0.45), (1.6, 0.04, 0.45))
            b.box("bench", (xc, yc - 0.55, 0.36), (1.6, 0.3, 0.04))
            for dx in (-0.76, 0.76):
                b.box("bench", (xc + dx, yc, 0.34), (0.04, 0.45, 0.68))
                b.box("bench", (xc + dx, yc - 0.55, 0.18), (0.04, 0.3, 0.36))
    # wall slogan band + "Time is money" type writing as dark strips (no readable text needed)
    b.box("cushion_red", (104.5, y1 - 0.14, 2.75), (5.0, 0.01, 0.12))
    # ---- veranda corridor east of the building
    b.box("tile", (110.6, 14, hgt + 0.2), (3.6, 60, 0.12))                       # sloping tile roof
    for k in range(-4, 14):
        y = k * 3.0
        b.cyl("column", (112.2, y, 0), (112.2, y, 2.6), 0.2, 10)
        b.box("post", (112.2, y, 3.0), (0.16, 0.16, 0.8))
        if k < 13:
            b.box("column", (112.2, y + 1.5, 0.4), (0.25, 2.6, 0.8))            # low parapet
    b.box("post", (110.6, 14, hgt - 0.05), (3.4, 0.1, 0.1))
    for k in range(-12, 42, 2):
        b.box("wood", (110.6, k, hgt + 0.05), (3.4, 0.08, 0.08))                # rafters
    # far ends: bright openings
    b.box("ground", (125, 14, -0.1), (24, 70, 0.1))                              # courtyard
    b.cyl("wood", (120, 6, 0), (120, 6, 4.5), 0.25)
    b.sph("leaf", (120, 6, 6.5), 3.0, 10, 8)
    b.box("school_wall", (126, 14, 2.5), (1, 60, 5))                             # other block across the yard
    obs = b.build(c, "SCHOOL")
    P, L = {}, {}
    # bell on the corridor wall
    bl = S["bell"]
    brass = M((0.62, 0.45, 0.16), 0.22, 1.0)
    P["bell"] = empty("Bell", (bl.x + 0.02, bl.y, bl.z))
    new_obj("BellBase", box_mesh("bb", 0.03, 0.22, 0.3, False), M((0.15, 0.1, 0.06), 0.6), P["bell"])
    dome = new_obj("BellDome", sphere_mesh("bd", 0.11, 18, 10, (1, 1, 1)), brass, P["bell"], loc=(0.06, 0, 0.02))
    dome.scale = (0.55, 1, 1)
    P["bell_arm"] = new_obj("BellArm", cyl_mesh("ba", 0.008, 0.16, 6), c["iron"], P["bell"], loc=(0.05, 0, -0.14))
    new_obj("BellBall", sphere_mesh("bbl", 0.018, 8, 6), c["iron"], P["bell_arm"], loc=(0, 0, 0.16))
    # classroom door (opens out into the corridor), staff-room door
    P["cls_door"] = hinged("ClsDoor", 1.1, 2.4, 0.05, (109.0, 10.0, 0), c["wood_lt"], rz0=math.radians(90))
    P["staff_door"] = hinged("StaffDoor", 1.0, 2.3, 0.05, (109.0, 17.0, 0), c["wood_lt"], rz0=math.radians(-60))
    # staff room table + chairs
    sx, sy = S["staff_seat"]
    box_obj("StaffTable", (0.9, 1.6, 0.05), (sx - 1.0, sy, 0.75), c["wood"])
    box_obj("StaffChair", (0.46, 0.46, 0.05), (sx + 0.05, sy, 0.42), c["wood"])
    box_obj("StaffChairBack", (0.05, 0.46, 0.55), (sx + 0.27, sy, 0.47), c["wood"])
    for dx, dy in ((-0.18, -0.18), (0.18, -0.18), (-0.18, 0.18), (0.18, 0.18)):
        box_obj("StaffChairLeg", (0.04, 0.04, 0.42), (sx + 0.05 + dx, sy + dy, 0), c["wood"])
    # ceiling fans + (off) tubelights
    for i, (x, y) in enumerate(((102.8, 4.5), (106.2, 4.5), (104.5, 8.5))):
        hub = new_obj("Fan%d" % i, cyl_mesh("fh", 0.12, 0.12, 12), c["wood"], loc=(x, y, hgt - 0.5))
        for k in range(3):
            blb = new_obj("Fan%d_b%d" % (i, k), box_mesh("fb", 0.6, 0.12, 0.01), c["wood"], hub, loc=(0, 0, 0.04))
            blb.data.transform(Matrix.Translation((0.38, 0, 0)))
            blb.rotation_euler.z = k * 2.0944
        spin(hub, "Z", 1.1, t_end, i)
    for x in (101.5, 107.5):
        box_obj("Tube%d" % x, (0.05, 1.2, 0.05), (x, 6, 3.3), M((0.8, 0.8, 0.8), 0.5))
    # window sky plates (west) and the far corridor arches (south / north ends)
    for i, y in enumerate((2.6, 5.8, 9.0)):
        P["plateW%d" % i] = box_obj("SchoolPlate%d" % i, (0.02, 2.4, 2.4), (99.0, y, 0.6), c["sky_win"])
    P["arch_s"] = box_obj("ArchS", (3.4, 0.02, 3.4), (110.6, -12.0, 0), c["sky_win"])
    P["arch_n"] = box_obj("ArchN", (3.4, 0.02, 3.4), (110.6, 40.0, 0), c["sky_win"])
    P["plate_staff"] = box_obj("StaffPlate", (0.02, 2.0, 2.0), (102.2, 17.6, 0.7), c["sky_win"])
    # lights
    L["S_Sky"] = lamp("S_Sky", "SUN", (100, 0, 20), 0, size=math.radians(60), shadow=False)
    L["S_Sun"] = lamp("S_Sun", "SUN", (100, 0, 20), 0, size=math.radians(1.5))
    for i, y in enumerate((2.6, 5.8, 9.0)):
        L["S_Win%d" % i] = lamp("S_Win%d" % i, "AREA", (99.6, y, 1.85), 0, size=(2.0, 1.9), rot=(0, math.radians(-90), 0))
    L["S_Yard"] = lamp("S_Yard", "AREA", (113.0, 14, 1.6), 0, size=(2.6, 50), rot=(0, math.radians(90), 0))
    L["S_ArchS"] = lamp("S_ArchS", "AREA", (110.6, -11.6, 1.7), 0, size=(3.2, 3.2), rot=(math.radians(90), 0, 0))
    L["S_ArchN"] = lamp("S_ArchN", "AREA", (110.6, 39.6, 1.7), 0, size=(3.2, 3.2), rot=(math.radians(-90), 0, 0))
    L["S_StaffWin"] = lamp("S_StaffWin", "AREA", (102.6, 17.6, 1.7), 0, size=(1.6, 1.6), rot=(0, math.radians(-90), 0))
    L["S_DoorSpill"] = lamp("S_DoorSpill", "AREA", (109.6, 10.55, 1.3), 0, size=(2.3, 1.1), rot=(0, math.radians(90), 0))
    return dict(obs=obs, P=P, L=L)


# ======================================================================================== STREET
def build_street(t_end):
    c = mats()
    b = Builder()
    y0 = 200.0
    b.box("ground", (0, y0, -0.05), (120, 40, 0.1))
    rnd = random.Random(8)
    for side in (-1, 1):
        x = -50.0
        while x < 50:
            w = rnd.uniform(3.2, 5.5)
            hh = rnd.uniform(5.5, 9.5)
            yy = y0 + side * (5.2 + 3.0)
            b.box("shop" if rnd.random() < 0.6 else "wall_ext", (x + w / 2, yy, hh / 2), (w - 0.05, 6.0, hh))
            b.box("shutter", (x + w / 2, y0 + side * 5.18, 1.3), (w - 0.6, 0.06, 2.6))
            b.box(rnd.choice(("awn1", "awn2", "awn3")), (x + w / 2, y0 + side * 4.7, 2.85), (w - 0.3, 1.1, 0.06), rx=side * 0.25)
            b.box("photo", (x + w / 2, y0 + side * 5.15, 3.4), (w * 0.7, 0.05, 0.6))          # signboard
            x += w
    for k in range(10):                                                                     # parked scooters, carts
        x = -40 + k * 8.5 + rnd.uniform(-1, 1)
        side = 1 if k % 2 else -1
        b.box("shutter", (x, y0 + side * 3.9, 0.55), (1.6, 0.5, 0.6))
        b.box("black", (x, y0 + side * 3.9, 0.95), (0.4, 0.45, 0.3))
    for k in range(3):
        x = -20 + k * 18
        b.box("wood_lt", (x, y0 - 3.3, 0.8), (1.8, 1.0, 0.1))                             # vendor carts
        b.cyl("black", (x - 0.6, y0 - 3.3, 0), (x - 0.6, y0 - 3.3, 0.4), 0.3, 10)
        b.box("leaf", (x, y0 - 3.3, 0.95), (1.5, 0.8, 0.2))
    for k in range(8):
        b.cyl("concrete", (-45 + k * 12, y0 + 4.6, 0), (-45 + k * 12, y0 + 4.6, 8), 0.09)
        b.cyl("black", (-45 + k * 12, y0 + 4.6, 7.6), (-33 + k * 12, y0 + 4.6, 7.3), 0.01, 4)
    obs = b.build(c, "STREET")
    L = dict(T_Sky=lamp("T_Sky", "SUN", (0, y0, 20), 0, size=math.radians(70), shadow=False),
             T_Sun=lamp("T_Sun", "SUN", (0, y0, 20), 0, size=math.radians(8)))
    return dict(obs=obs, P={}, L=L)


# ======================================================================================== HOSPITAL BACKYARD
YARD = Vector((200.0, 200.0))
LINES_Y = [204.0 + i * 2.3 for i in range(7)]


def build_yard(t_end):
    c = mats()
    b = Builder()
    b.box("ground", (200, 210, -0.05), (90, 70, 0.1))
    b.box("wall_ext", (200, 228, 6), (60, 4, 12))                                  # hospital back block
    for k in range(12):
        for r in range(3):
            b.box("black", (174 + k * 4.6, 225.95, 2.0 + r * 3.6), (1.2, 0.05, 1.6))
    b.box("wall_ext", (200, 182, 1.0), (60, 0.25, 2.0))                            # boundary wall behind camera
    for y in LINES_Y:
        for x in (182.0, 200.0, 218.0):
            b.cyl("iron", (x, y, 0), (x, y, 2.55), 0.035)
        b.cyl("rope", (182, y, 2.45), (218, y, 2.45), 0.008, 4)
    b.cyl("wood", (230, 210, 0), (230, 210, 5), 0.3)
    b.sph("leaf", (230, 210, 7), 3.4, 10, 8)
    obs = b.build(c, "YARD")
    # sheets: subdivided planes with wave modifiers so they breathe in the wind
    P = {"sheets": []}
    rnd = random.Random(12)
    for y in LINES_Y:
        x = 182.6
        while x < 217:
            w = rnd.uniform(1.4, 1.9)
            s = sheet_obj("Sheet", w, 2.0, (x + w / 2, y, 2.45), c["whitesheet"], rnd.random() * 10)
            P["sheets"].append(s)
            x += w + rnd.uniform(0.15, 0.6)
    L = dict(Y_Sun=lamp("Y_Sun", "SUN", (200, 220, 20), 0, size=math.radians(0.8)),
             Y_Sky=lamp("Y_Sky", "SUN", (200, 220, 20), 0, size=math.radians(70), shadow=False),
             Y_Bounce=lamp("Y_Bounce", "AREA", (200, 196, 1.6), 0, size=(30, 3), shadow=False))
    L["Y_Bounce"].rotation_euler = (math.radians(90), 0, 0)
    return dict(obs=obs, P=P, L=L)


SHEET_MAT = {}


def sheet_mat():
    if "m" in SHEET_MAT:
        return SHEET_MAT["m"]
    m = bpy.data.materials.new("SheetGlow")
    nt = m.node_tree
    bs = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    bs.inputs["Base Color"].default_value = (0.95, 0.95, 0.92, 1)
    bs.inputs["Roughness"].default_value = 0.9
    bs.inputs["Alpha"].default_value = 0.82
    bs.inputs["Emission Color"].default_value = (1.0, 0.86, 0.66, 1)
    bs.inputs["Emission Strength"].default_value = 0.0
    bs.inputs["Transmission Weight"].default_value = 0.35
    m.surface_render_method = "BLENDED"
    m.use_backface_culling = False
    SHEET_MAT["m"] = m
    return m


def sheet_obj(name, w, h, top, mat, phase):
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=10, y_segments=12, size=0.5)
    for v in bm.verts:
        v.co = Vector((v.co.x * w, -(v.co.y + 0.5) * h, 0))
    me = to_mesh(name, bm)
    ob = new_obj(name, me, sheet_mat(), loc=top, rot=(math.pi / 2, 0, 0))
    wv = ob.modifiers.new("wave", "WAVE")
    wv.use_normal = False
    wv.use_x = False
    wv.use_y = True
    wv.height = 0.09
    wv.width = 0.9
    wv.speed = 0.06
    wv.time_offset = -phase * 10
    return ob


# ======================================================================================== RIVER
RIV = Vector((0.0, -2000.0))


def build_river(t_end):
    c = mats()
    b = Builder()
    # shore: a long dark bank 22 m north of the boat's path, with ghat steps and posts
    b.box("bank", (0, RIV.y + 30, -0.4), (400, 16, 1.2))
    for k in range(4):
        b.box("concrete", (8, RIV.y + 22.6 + k * 0.6, -0.55 + k * 0.2), (14, 0.6, 0.3))
    for x in (-40, -24, 2, 16, 34, 52):
        b.cyl("wood", (x, RIV.y + 22.4, -0.5), (x, RIV.y + 22.4, 0.9), 0.08)
    rnd = random.Random(4)
    for k in range(18):                                                             # tree silhouettes on the bank
        x = -120 + k * 14 + rnd.uniform(-4, 4)
        hh = rnd.uniform(6, 12)
        b.cyl("bank", (x, RIV.y + 34, 0), (x, RIV.y + 34, hh), 0.3)
        b.sph("bank", (x, RIV.y + 34, hh + 2), rnd.uniform(3, 5), 8, 6)
    obs = b.build(c, "RIVER")
    P = {}
    # water: a big plane with an ocean modifier (gentle swell) and a dark glossy material
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=2, y_segments=2, size=600)
    me = to_mesh("Water", bm)
    w = new_obj("Water", me, c["water"], loc=(RIV.x, RIV.y, 0))
    oc = w.modifiers.new("ocean", "OCEAN")
    oc.geometry_mode = "GENERATE"
    oc.repeat_x = oc.repeat_y = 30
    oc.size = 1.0
    oc.spatial_size = 20
    oc.resolution = 7
    oc.wave_scale = 0.12
    oc.choppiness = 0.4
    oc.wind_velocity = 4
    ANIM.put(w, 'modifiers["ocean"].time', 0, 1, 0.0, "lin")
    ANIM.put(w, 'modifiers["ocean"].time', 0, F(t_end), t_end * 0.6, "lin")
    P["water"] = w
    # boat: tapered wooden hull 4.6 m, centre at origin of an empty that drifts
    P["boat"] = boat()
    P["rope"] = new_obj("Rope", cyl_mesh("rp", 0.012, 1.0, 6), c["rope"])
    P["moon"] = new_obj("MoonDisc", sphere_mesh("mn", 9, 24, 16), c["moon"], loc=(-60, RIV.y + 260, 70))
    P["fog"], P["fog_node"] = fog_box("RiverFog", (0, RIV.y + 10, 6), (500, 160, 14), 0.035, (0.75, 0.82, 0.95), 0.5)
    L = dict(R_Moon=lamp("R_Moon", "SUN", (0, RIV.y, 30), 0, size=math.radians(1.0)),
             R_Sky=lamp("R_Sky", "SUN", (0, RIV.y, 30), 0, size=math.radians(80), shadow=False),
             R_Rise=lamp("R_Rise", "SUN", (0, RIV.y, 30), 0, size=math.radians(2.0)),
             R_Lantern=lamp("R_Lantern", "POINT", (0, RIV.y, 0.6), 0, size=0.05))
    return dict(obs=obs, P=P, L=L)


def boat():
    c = mats()
    rootb = empty("Boat", (RIV.x, RIV.y, 0))
    bm = bmesh.new()
    L, W, Hh = 4.6, 1.25, 0.55
    prof = []
    for i in range(9):
        u = i / 8
        x = (u - 0.5) * L
        k = math.sin(math.pi * u) ** 0.6
        prof.append((x, W / 2 * k + 0.02, 0.1 + 0.25 * (abs(u - 0.5) * 2) ** 2))
    vs_t, vs_b = [], []
    for x, hw, rise in prof:
        for s in (1, -1):
            vs_t.append(bm.verts.new((x, s * hw, Hh + rise)))
            vs_b.append(bm.verts.new((x, s * hw * 0.55, 0.0)))
    n = len(prof)
    for i in range(n - 1):
        a, b_ = 2 * i, 2 * (i + 1)
        for s in (0, 1):
            bm.faces.new((vs_t[a + s], vs_t[b_ + s], vs_b[b_ + s], vs_b[a + s]))
        bm.faces.new((vs_b[a], vs_b[a + 1], vs_b[b_ + 1], vs_b[b_]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = to_mesh("Hull", bm)
    hull = new_obj("Hull", me, c["boat"], rootb, loc=(0, 0, -0.12))
    sol = hull.modifiers.new("sol", "SOLIDIFY")
    sol.thickness = 0.05
    for x in (-1.0, 0.3, 1.3):
        new_obj("Thwart", box_mesh("tw", 0.22, 1.1, 0.04), c["wood_lt"], rootb, loc=(x, 0, 0.36))
    new_obj("Deck", box_mesh("dk", 3.6, 0.7, 0.03), c["wood"], rootb, loc=(0, 0, 0.02))
    lan = new_obj("Lantern", cyl_mesh("ln", 0.07, 0.2, 10), M((1, 0.8, 0.4), 0.4, emit=kelvin(2200), strength=0.0), rootb, loc=(-1.7, 0, 0.1))
    C["lantern"] = lan.data.materials[0]
    return rootb
