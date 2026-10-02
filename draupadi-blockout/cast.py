# cast.py - the people of the film as articulated mannequins, one constructor per character look.
# Colours follow the costume boards (Desktop/test references/costume breakdowns): present-day Mamta in dull,
# faded colours; young Mamta in colour; RED only for the bride, the sweater and the dupatta (motif).
import random

from kit import Actor, CROWD_COLORS

HAIR_BLACK = (0.025, 0.02, 0.018)
HAIR_GREY = (0.32, 0.31, 0.30)
HAIR_SALT = (0.16, 0.15, 0.14)
RED = (0.55, 0.02, 0.03)


def mamta(look="school", name="Mamta"):
    """Mamta at 35."""
    L = dict(
        school=dict(top=(0.46, 0.42, 0.36), bottom=(0.46, 0.42, 0.36), dup=(0.16, 0.30, 0.30), flags=("bun", "skirt", "pallu")),
        home=dict(top=(0.22, 0.30, 0.18), bottom=(0.30, 0.32, 0.26), dup=(0.30, 0.34, 0.24), flags=("bun", "dupatta")),
        fresh=dict(top=(0.22, 0.36, 0.40), bottom=(0.30, 0.36, 0.38), dup=(0.20, 0.30, 0.34), flags=("bun",)),
        night=dict(top=(0.22, 0.36, 0.40), bottom=(0.30, 0.36, 0.38), dup=(0.28, 0.28, 0.30), flags=("bun", "dupatta")),
        boat=dict(top=(0.70, 0.74, 0.80), bottom=(0.70, 0.74, 0.80), dup=(0.66, 0.72, 0.82), flags=("bun", "skirt", "pallu")),
    )[look]
    return Actor(name, 1.60, L["top"], L["bottom"], skin="a", hair=HAIR_BLACK, flags=L["flags"], sleeve=1.0, build=0.92,
                 dup=L["dup"], head_k=0.86)


def young_mamta(look="dev", name="YMamta"):
    """Mamta at 22."""
    L = dict(
        dev=dict(top=(0.62, 0.30, 0.36), bottom=(0.70, 0.62, 0.52), dup=(0.72, 0.55, 0.40), flags=("braid", "dupatta")),
        pregnant=dict(top=(0.62, 0.42, 0.44), bottom=(0.62, 0.42, 0.44), dup=None, flags=("braid", "belly", "skirt")),
        bride=dict(top=RED, bottom=RED, dup=(0.62, 0.03, 0.05), flags=("bun", "skirt", "veilhead", "tikka")),
        bride_bare=dict(top=RED, bottom=RED, dup=(0.62, 0.03, 0.05), flags=("bun", "skirt", "tikka")),
        birth=dict(top=(0.30, 0.06, 0.10), bottom=(0.30, 0.06, 0.10), dup=None, flags=("braid", "belly", "skirt")),
        after=dict(top=(0.30, 0.06, 0.10), bottom=(0.30, 0.06, 0.10), dup=None, flags=("braid", "skirt")),
    )[look]
    return Actor(name, 1.60, L["top"], L["bottom"], skin="a", hair=HAIR_BLACK, flags=L["flags"], sleeve=1.0, build=0.9,
                 dup=L["dup"], head_k=0.86)


def papa(young=False, name=None):
    if young:
        return Actor(name or "YPapa", 1.72, (0.40, 0.52, 0.66), (0.16, 0.15, 0.14), skin="b", hair=HAIR_BLACK, sleeve=1.0,
                     flags=("moustache",), build=1.05)
    return Actor(name or "Papa", 1.70, (0.74, 0.71, 0.64), (0.70, 0.68, 0.62), skin="b", hair=HAIR_GREY, sleeve=2.0,
                 flags=("moustache", "glasses", "scarf"), build=0.98)


def mother(young=False, name=None):
    if young:
        return Actor(name or "YMother", 1.56, (0.34, 0.12, 0.10), (0.34, 0.12, 0.10), skin="a", hair=HAIR_BLACK, sleeve=1.0,
                     flags=("bun", "skirt", "pallu"), dup=(0.40, 0.22, 0.10), build=1.0)
    return Actor(name or "Mother", 1.54, (0.44, 0.44, 0.58), (0.44, 0.44, 0.58), skin="c", hair=HAIR_GREY, sleeve=1.0,
                 flags=("bun", "skirt", "pallu"), dup=(0.50, 0.50, 0.62), build=0.9)


def dev(look="coat", name="Dev"):
    if look == "coat":
        return Actor(name, 1.80, (0.88, 0.88, 0.86), (0.18, 0.20, 0.28), skin="c", hair=HAIR_BLACK, sleeve=2.0,
                     flags=("coat",), skirt_col=(0.88, 0.88, 0.86))
    if look == "river":
        return Actor(name, 1.80, (0.72, 0.66, 0.56), (0.70, 0.64, 0.54), skin="c", hair=HAIR_BLACK, sleeve=2.0, flags=("scarf",))
    return Actor(name, 1.80, (0.62, 0.20, 0.08), (0.18, 0.18, 0.22), skin="c", hair=HAIR_BLACK, sleeve=1.0)   # red-orange shirt


def jagdish(look="shirt", name="Jagdish"):
    if look == "sherwani":
        return Actor(name, 1.76, (0.66, 0.58, 0.40), (0.72, 0.68, 0.58), skin="b", hair=HAIR_BLACK, sleeve=2.0,
                     flags=("moustache", "coat"), skirt_col=(0.66, 0.58, 0.40), headwear="safa", hw_col=(0.70, 0.45, 0.20))
    return Actor(name, 1.76, (0.70, 0.60, 0.34), (0.16, 0.16, 0.18), skin="b", hair=HAIR_BLACK, sleeve=2.0, flags=("moustache",))


def kid(i, seed=0, girl=None, name=None):
    r = random.Random(seed * 100 + i)
    girl = (r.random() < 0.5) if girl is None else girl
    H = r.uniform(1.22, 1.38)
    return Actor(name or "Kid%d" % i, H, (0.86, 0.86, 0.84), (0.10, 0.14, 0.30) if not girl else (0.12, 0.16, 0.34),
                 skin=r.choice("abcd"), hair=HAIR_BLACK, head_k=1.08, build=0.85, sleeve=1.0,
                 flags=("braid",) if girl else ())


def extra(name, seed, top=None, coat=False, H=None, skirt=False, dup=None):
    r = random.Random(seed)
    H = H or r.uniform(1.55, 1.82)
    top = top or r.choice(CROWD_COLORS)
    flags = ()
    if coat:
        flags = ("coat",)
    if skirt:
        flags = ("bun", "skirt", "pallu")
    return Actor(name, H, top, (0.1 + r.random() * 0.1, 0.1, 0.12 + r.random() * 0.1) if not skirt else top,
                 skin=r.choice("abcd"), build=r.uniform(0.9, 1.1), sleeve=2.0 if coat else 1.0, flags=flags,
                 skirt_col=(0.9, 0.9, 0.88) if coat else None, dup=dup, hair=HAIR_BLACK)


def peon():
    return Actor("Peon", 1.66, (0.48, 0.42, 0.28), (0.40, 0.35, 0.24), skin="d", hair=HAIR_SALT, sleeve=1.0, flags=("moustache",))


def nurse():
    return Actor("Nurse", 1.58, (0.82, 0.84, 0.86), (0.82, 0.84, 0.86), skin="c", hair=HAIR_BLACK, flags=("bun", "skirt"), sleeve=1.0)


def doctor():
    return Actor("Doctor", 1.70, (0.86, 0.86, 0.84), (0.20, 0.20, 0.22), skin="b", hair=HAIR_SALT, sleeve=2.0,
                 flags=("coat", "glasses"), skirt_col=(0.86, 0.86, 0.84))
