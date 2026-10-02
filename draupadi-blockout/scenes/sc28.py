# Scene 28 - THE FLOWER - INT. House (Mother's Room) - Sunrise (shots 208-213, 35 s)
# Shot 184's frame, now warm: the first warm interior of the film. Mamta's head on her mother's chest; Mother's
# hand on her head, a small smile, the chest not moving. Papa's hand joins. The camera tracks out to a flower
# growing through a crack in the wall in a sunbeam (Mahavir's plant). Fade to white; the title.
import math

import bpy
from mathutils import Quaternion, Vector

from kit import *
from film import *
import cast
import hs
import props
import sets
from sets import H
from scenes.sc08 import mother_in_bed

CRACK = H["crack"]


def build(S):
    T = S.T
    a = {n: T[n][0] for n in T}
    b = {n: T[n][1] for n in T}
    E = S.END
    st = hs.house(S)
    C = sets.mats()
    sets.sun_dir(st["L"]["Sun"], 8, 7)
    S.state(0, Sun=(5.0, 3200), WinMo=(260, 3400), MoBounce=(40, 3600), WinCorr=(20, 5000))
    S.emit(0, C["sky_win"], 4.0)
    S.world(0, (0.3, 0.22, 0.15), 0.04)
    S.exposure(0, 0.55)
    haze, _ = fog_box("SunHaze", (5.4, 10.8, 1.6), (5.0, 6.0, 3.1), 0.02, (1.0, 0.85, 0.65), 0.6)
    MO = cast.mother()
    mother_in_bed(MO, 0, E)
    MA = cast.mamta("boat", name="Mamta")
    PA = cast.papa()
    SEAT = Vector((6.05, 13.15))
    MA.at(0, SEAT.x, SEAT.y, 0.0).stay(E)
    MA.act(0, E, fade=0, sit=1.0, seat=0.42, lean=1.05, hp=0.2, roll=0.25, eyes=0.15, mood=(0.0, 0.2, 0.0),
           armL=Vector((6.6, 13.0, 0.66)), armR=Vector((6.55, 12.7, 0.62)))
    MHEAD = lambda t: MA.J(t)["head_c"] + Vector((0, 0, 0.08))
    MO.act(0, E, eyes=0.12, smile=0.0, mood=(0.1, 0.35, 0.0), hp=0.35, look=lambda t, u: MHEAD(t),
           armR=lambda t, u: MHEAD(t) + Vector((0.02, 0.0, 0.03)))
    PA.at(a[211], 7.25, 10.8, math.pi / 2).walk(a[211] + 2.4, 7.3, 11.95, mode="smooth").stay(E, math.pi - 0.3)
    PA.act(a[211] + 2.2, E, sit=1.0, seat=0.5, look=lambda t, u: MHEAD(t), mood=(-0.6, -0.3, 0.0), hp=0.3,
           armR=lambda t, u: MHEAD(t) + Vector((0.06, -0.06, 0.06)) if t > a[211] + 3.4 else None)
    S.on(MA, list(range(208, 213)), step=3)
    S.on(MO, list(range(208, 213)), step=3)
    S.on(PA, [211, 212])
    # a sunbeam lands on the flower in the crack
    beam = lamp("FlowerBeam", "SPOT", (CRACK.x - 1.6, CRACK.y + 1.2, 2.2), 0, kelvin(3200), size=0.03, spot=9)
    aim(beam, (CRACK.x, CRACK.y, 1.1))
    S.state(0, FlowerBeam=(260, 3000))
    # title card (213): a white card with the title in a simple serif
    TC = Vector((0, -600, 10))
    card = new_obj("TitleCard", box_mesh("tc", 30, 0.2, 14, False), M((1, 1, 1), 1.0, emit=(1, 1, 1), strength=1.6), loc=TC + Vector((0, 4, 0)))
    try:
        font = bpy.data.fonts.load("C:/Windows/Fonts/georgia.ttf")
    except Exception:
        font = None
    tx = text3d("DRAUPADI SE DRAUPADI TAK", 0.55, M((0.05, 0.05, 0.05), 0.8), TC + Vector((0, 3.85, 0)))
    if font:
        tx.data.font = font
    S.shoot(213, lambda t: dict(pos=TC + Vector((0, -6, 0)), look=TC + Vector((0, 4, 0)), lens=50, focus=9.9, fstop=16))
    # cameras
    S.shoot(208, lambda t: dict(pos=Vector((5.0, 8.25, 1.6)), look=Vector((6.4, 12.75, 0.8)), focus=4.6, fstop=5.6))
    S.shoot(209, lambda t: dict(pos=MHEAD(t) + Vector((-0.5, -0.7, 0.3)), look=MHEAD(t) + Vector((0.05, 0, 0.02)), focus=0.9, fstop=2.8))
    S.shoot(210, lambda t: dict(pos=Vector((5.55, 13.25, 1.3)), look=head(MO, t) + Vector((0, -0.05, -0.05)), focus=1.5, fstop=2.0))
    S.shoot(211, lambda t: dict(pos=Vector((5.1, 9.6, 1.5)), look=est(PA, t) + Vector((0, 0, -0.5)), focus=3.0, fstop=2.8))

    def c212(t):                                 # dolly out, rack from the three to the flower
        u = seg(t, a[212], b[212])
        pos = Vector((6.3, 11.0, 1.35)).lerp(Vector((6.6, 8.2, 1.15)), u)
        look = Vector((6.6, 12.8, 0.8)).lerp(Vector((7.2, 11.6, 0.95)), u)
        fl = Vector((CRACK.x, CRACK.y, 1.1))
        focus = lerp((Vector((6.6, 12.8, 0.8)) - pos).length, (fl - pos).length, seg(t, a[212] + 6, a[212] + 9.5))
        return dict(pos=pos, look=look, focus=focus, fstop=2.0)
    S.shoot(212, c212)
    W = 3200
    S.light(208, (6.6, 12.9, 0.8), key=dict(side="R", ang=70, el=20, d=2.5, w=40, k=W, size=2.0))
    S.light(209, lambda t: MHEAD(t), key=dict(side="R", ang=60, el=20, d=1.2, w=20, k=W, size=1.0))
    S.light(210, lambda t: head(MO, t), key=dict(side="R", ang=40, el=30, d=1.4, w=35, k=W, size=1.2), fill=dict(side="L", ang=40, el=10, d=1.4, w=15, k=W))
    S.light(211, lambda t: head(PA, t), rim=dict(side="R", ang=160, el=15, d=1.6, w=60, k=W), fill=dict(side="L", ang=30, el=15, d=2, w=15, k=W))
    S.light(212, (6.6, 12.8, 0.8), key=dict(side="R", ang=70, el=20, d=2.5, w=35, k=W, size=2.0))
    S.light(213, TC, key=dict(side="L", ang=0, el=0, d=50, w=0))
