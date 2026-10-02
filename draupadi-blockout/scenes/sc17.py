# Scene 17 - DUSK - INT. House (Mother's Room) - Evening (shot 112, 8 s)
# The wide of Shot 105, locked off. Mother asleep, Mamta dozing in the chair. Only the light moves: warm sunset
# (3500K) -> blue dusk (7000K) -> near black, ramped like a dimmer.
import math

from mathutils import Vector

from kit import *
from film import *
import cast
import hs
import sets
from sets import H
from scenes.sc08 import mother_in_bed


def build(S):
    a, b = S.T[112]
    st = hs.house(S)
    C = sets.mats()
    L = st["L"]
    win = L["WinMo"].data
    sets.sun_dir(L["Sun"], 200, 6)
    S.world(0, (0.05, 0.06, 0.1), 0.02)
    S.exposure(0, 1.3)
    # dimmer ramp: energy and colour over the shot
    for t, w, k in ((0, 420, 3500), (2.5, 300, 4200), (5.0, 150, 7000), (8.0, 10, 7500)):
        ANIM.put(win, "energy", 0, F(t), w)
        for i, c in enumerate(kelvin(k)):
            ANIM.put(win, "color", i, F(t), c)
    ANIM.put(C["sky_win"].node_tree, 'nodes["Principled BSDF"].inputs["Emission Strength"].default_value', 0, F(0), 3.0)
    ANIM.put(C["sky_win"].node_tree, 'nodes["Principled BSDF"].inputs["Emission Strength"].default_value', 0, F(8), 0.05)
    MO = cast.mother()
    mother_in_bed(MO, 0, S.END)
    MO.act(0, S.END, eyes=0.1, hp=0.4)
    MA = cast.mamta("fresh")
    CH = H["mo_chair"]
    MA.at(0, CH.x, CH.y, 0.15).stay(S.END)
    MA.act(0, S.END, fade=0, sit=1.0, seat=0.47, hp=0.55, roll=0.12, eyes=0.1, armL=("rel", 0.15, 0.1, -0.35), armR=("rel", 0.15, -0.1, -0.35))
    S.on(MO, [112], step=6)
    S.on(MA, [112], step=6)
    S.shoot(112, lambda t: dict(pos=Vector((5.0, 8.15, 1.6)), look=Vector((6.3, 12.6, 0.8)), focus=4.6, fstop=5.6))
