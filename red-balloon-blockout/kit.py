# kit.py - engine for the Operation Red Balloon blockout (Blender 5.1, run via blender.sh -P).
# Pieces: math/ease helpers, material cache, bulk keyframe writer (Anim), merged-geometry Builder,
# articulated Mannequin (Actor) with walk cycle + two-bone IK + face, crowd walkers, shot camera.
import math
import random

import bmesh
import bpy
from mathutils import Matrix, Quaternion, Vector

FPS = 24
ZUP = Vector((0, 0, 1))


# ------------------------------------------------------------------ math
def F(t):
    return 1 + t * FPS


def ease(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * (3 - 2 * u)


def lerp(a, b, u):
    return a + (b - a) * u


def vl(a, b, u):
    return Vector(a).lerp(Vector(b), u)


def wrap(a):
    return (a + math.pi) % (2 * math.pi) - math.pi


def lerp_ang(a, b, u):
    return a + wrap(b - a) * u


def fvec(yaw):
    return Vector((math.cos(yaw), math.sin(yaw), 0))


def lvec(yaw):
    return Vector((-math.sin(yaw), math.cos(yaw), 0))


def V(*a):
    return Vector(a)


def seg(t, t0, t1):
    return ease((t - t0) / (t1 - t0))


def deg(a):
    return math.radians(a)


# ------------------------------------------------------------------ materials
_MC = {}


def M(rgb, rough=0.8, metal=0.0, emit=None, strength=0.0, alpha=1.0):
    k = (tuple(round(c, 3) for c in rgb), rough, metal, None if emit is None else tuple(emit), strength, alpha)
    if k in _MC:
        return _MC[k]
    m = bpy.data.materials.new("m%d" % len(_MC))
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emit is not None:
        b.inputs["Emission Color"].default_value = (*emit, 1)
        b.inputs["Emission Strength"].default_value = strength
    if alpha < 1:
        b.inputs["Alpha"].default_value = alpha
        m.surface_render_method = "BLENDED"
    _MC[k] = m
    return m


def bsdf(m, name):
    return m.node_tree.nodes["Principled BSDF"].inputs[name]


# ------------------------------------------------------------------ bulk keyframes
class Anim:
    """Collects samples, then writes them as F-curves in one go (fast; keyframe_insert is too slow for 1M keys)."""

    def __init__(self):
        self.d = {}

    def put(self, idb, path, idx, f, v, kind="bez"):
        ch = self.d.setdefault(idb, {}).setdefault((path, idx), [[], [], kind])
        ch[0].append(f)
        ch[1].append(v)

    def put_many(self, idb, path, f, vals, kind="bez"):
        for i, v in enumerate(vals):
            self.put(idb, path, i, f, v, kind)

    def flush(self):
        for idb, chs in self.d.items():
            act = bpy.data.actions.new(idb.name + "_A")
            slot = act.slots.new(id_type=idb.id_type, name=idb.name)
            layer = act.layers.new("L")
            strip = layer.strips.new(type="KEYFRAME")
            bag = strip.channelbag(slot, ensure=True)
            for (path, idx), (fr, vals, kind) in chs.items():
                n = len(fr)
                fc = bag.fcurves.new(data_path=path, index=idx)
                fc.keyframe_points.add(n)
                co = [0.0] * (2 * n)
                co[0::2] = fr
                co[1::2] = vals
                fc.keyframe_points.foreach_set("co", co)
                if kind != "bez":
                    mode = "CONSTANT" if kind == "const" else "LINEAR"
                    for kp in fc.keyframe_points:
                        kp.interpolation = mode
                fc.update()
            idb.animation_data_create()
            idb.animation_data.action = act
            idb.animation_data.action_slot = slot
        self.d = {}


ANIM = Anim()


# ------------------------------------------------------------------ object helpers
def link(ob, coll=None):
    (coll or bpy.context.scene.collection).objects.link(ob)
    return ob


def to_mesh(name, bm):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.update()
    return me


def new_obj(name, mesh, mat=None, parent=None, loc=(0, 0, 0), rot=None, scale=None):
    ob = bpy.data.objects.new(name, mesh)
    if mat is not None:
        if isinstance(mat, (list, tuple)):
            for m in mat:
                ob.data.materials.append(m)
        elif len(mesh.materials) == 0:
            mesh.materials.append(mat)
        else:                                  # shared mesh: per-object material override
            ob.material_slots[0].link = "OBJECT"
            ob.material_slots[0].material = mat
    link(ob)
    ob.location = loc
    if rot:
        ob.rotation_euler = rot
    if scale:
        ob.scale = scale
    if parent:
        ob.parent = parent
    return ob


def empty(name, loc=(0, 0, 0), parent=None):
    ob = bpy.data.objects.new(name, None)
    link(ob)
    ob.location = loc
    if parent:
        ob.parent = parent
    return ob


def sphere_mesh(name, r, u=12, v=8, sq=(1, 1, 1), off=(0, 0, 0)):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=u, v_segments=v, radius=r)
    for vt in bm.verts:
        vt.co = Vector((vt.co.x * sq[0] + off[0], vt.co.y * sq[1] + off[1], vt.co.z * sq[2] + off[2]))
    return to_mesh(name, bm)


def box_mesh(name, w, d, h, base=True):
    """Box w(x) d(y) h(z); origin at bottom-centre if base else centre."""
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for vt in bm.verts:
        vt.co = Vector((vt.co.x * w, vt.co.y * d, vt.co.z * h + (h / 2 if base else 0)))
    return to_mesh(name, bm)


def rbox_mesh(name, w, d, h, r):
    """Bottom-origin box with bevelled edges (reads as a soft mannequin torso)."""
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for vt in bm.verts:
        vt.co = Vector((vt.co.x * w, vt.co.y * d, vt.co.z * h + h / 2))
    bmesh.ops.bevel(bm, geom=list(bm.edges), offset=r, segments=2, affect="EDGES")
    return to_mesh(name, bm)


def capsule_mesh(name, L, r, seg=10):
    """Capsule along +Z from 0..L."""
    r = min(r, L / 2 - 1e-4)
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=6, radius=r)
    sh = (L - 2 * r) / 2
    for vt in bm.verts:
        z = vt.co.z
        z += sh if z > 1e-6 else (-sh if z < -1e-6 else 0)
        vt.co.z = z + L / 2
    return to_mesh(name, bm)


def cyl_mesh(name, r, h, seg=12, r2=None):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r if r2 is None else r2, depth=h)
    for vt in bm.verts:
        vt.co.z += h / 2
    return to_mesh(name, bm)


# ------------------------------------------------------------------ merged static geometry
class Builder:
    """Accumulates many boxes/cylinders/spheres per material key and emits ONE object per key."""

    def __init__(self):
        self.bms = {}

    def _bm(self, key):
        if key not in self.bms:
            self.bms[key] = bmesh.new()
        return self.bms[key]

    def box(self, key, c, size, rz=0.0, rx=0.0, ry=0.0):
        m = (Matrix.Translation(c) @ Matrix.Rotation(rz, 4, "Z") @ Matrix.Rotation(ry, 4, "Y")
             @ Matrix.Rotation(rx, 4, "X") @ Matrix.Diagonal((size[0], size[1], size[2], 1)))
        bmesh.ops.create_cube(self._bm(key), size=1.0, matrix=m)

    def cyl(self, key, p0, p1, r, seg=8, r2=None):
        p0, p1 = Vector(p0), Vector(p1)
        d = p1 - p0
        L = d.length
        if L < 1e-6:
            return
        q = ZUP.rotation_difference(d.normalized())
        m = Matrix.Translation((p0 + p1) / 2) @ q.to_matrix().to_4x4()
        bmesh.ops.create_cone(self._bm(key), cap_ends=True, segments=seg, radius1=r,
                              radius2=r if r2 is None else r2, depth=L, matrix=m)

    def sph(self, key, c, r, u=8, v=6, sq=(1, 1, 1)):
        m = Matrix.Translation(c) @ Matrix.Diagonal((sq[0], sq[1], sq[2], 1))
        bmesh.ops.create_uvsphere(self._bm(key), u_segments=u, v_segments=v, radius=r, matrix=m)

    def build(self, mats, prefix="B"):
        out = {}
        for key, bm in self.bms.items():
            me = to_mesh(prefix + "_" + key, bm)
            out[key] = new_obj(prefix + "_" + key, me, mats[key])
        self.bms = {}
        return out


# ------------------------------------------------------------------ two-bone IK
def ik2(A, T, a, b, pole):
    d = T - A
    L = d.length
    u = d / L if L > 1e-9 else Vector((0, 0, -1))
    L = max(min(L, a + b - 1e-4), abs(a - b) + 1e-4)
    x = (a * a - b * b + L * L) / (2 * L)
    h = math.sqrt(max(a * a - x * x, 0.0))
    pp = pole - u * pole.dot(u)
    if pp.length < 1e-6:
        pp = Vector((1, 0, 0)) - u * u.x
    pp.normalize()
    return A + u * x + pp * h, A + u * L


def seg_quat(p0, p1, prev=None):
    q = ZUP.rotation_difference((p1 - p0).normalized())
    if prev is not None and q.dot(prev) < 0:
        q.negate()
    return q


def basis_quat(x, z, prev=None):
    """Quaternion whose local X -> x (forward) and local Z -> z (up)."""
    x = Vector(x)
    z = Vector(z).normalized()
    x = (x - z * x.dot(z)).normalized()
    y = z.cross(x)
    q = Matrix(((x.x, y.x, z.x), (x.y, y.y, z.y), (x.z, y.z, z.z))).to_quaternion()
    if prev is not None and q.dot(prev) < 0:
        q.negate()
    return q


# ------------------------------------------------------------------ mannequin
SKIN = {"a": (0.50, 0.33, 0.24), "b": (0.42, 0.27, 0.19), "c": (0.58, 0.40, 0.30), "d": (0.35, 0.22, 0.16)}


class Actor:
    def __init__(self, name, H, top, bottom, skin="a", hair=(0.03, 0.025, 0.02), shoes=(0.05, 0.045, 0.04),
                 build=1.0, head_k=1.0, headwear=None, hw_col=(0.15, 0.15, 0.15), flags=(), sleeve=0.0,
                 silhouette=False):
        self.name, self.H, self.build = name, H, build
        self.wp = []
        self.acts = []
        self.windows = []
        self._jc = {}
        self._dist = None
        self.silhouette = silhouette
        sk = SKIN[skin] if not silhouette else (0.012, 0.012, 0.014)
        if silhouette:
            top = bottom = hair = shoes = (0.014, 0.014, 0.016)
            hw_col = (0.012, 0.012, 0.014)
        u = H
        s = self
        s.hipH, s.shH = 0.53 * u, 0.82 * u
        s.torsoL = s.shH - s.hipH
        s.hw, s.sw = 0.055 * u * build, 0.115 * u * build
        s.thigh = s.shin = 0.245 * u
        s.ua, s.fa = 0.18 * u, 0.16 * u
        s.hr = 0.068 * u * head_k
        s.ankle = 0.04 * u
        self.root = empty(name + "_root")
        R = self.root
        mT, mB, mS = M(top, 0.9), M(bottom, 0.9), M(sk, 0.7)
        mSh, mH = M(shoes, 0.9), M(hair, 0.9)
        P = {}
        P["torso"] = new_obj(name + "_torso", rbox_mesh(name + "t", 2 * s.sw * 1.05, 0.15 * u * build, s.torsoL, 0.03 * u), mT, R)
        new_obj(name + "_pelvis", rbox_mesh(name + "p", 2 * s.hw * 1.5, 0.14 * u * build, 0.11 * u, 0.02 * u), mB, P["torso"],
                loc=(0, 0, -0.02 * u))
        P["head"] = new_obj(name + "_head", sphere_mesh(name + "h", s.hr, 14, 10), mS, R)
        for side in "LR":
            ul = mT if sleeve > 0.5 else mS
            P["ua" + side] = new_obj(name + "_ua" + side, capsule_mesh(name + "ua", s.ua, 0.036 * u * build), mT if sleeve else mS, R)
            P["fa" + side] = new_obj(name + "_fa" + side, capsule_mesh(name + "fa", s.fa, 0.030 * u * build), mT if sleeve > 1.5 else mS, R)
            new_obj(name + "_hand" + side, sphere_mesh(name + "hd", 0.032 * u, 8, 6), mS, P["fa" + side], loc=(0, 0, s.fa + 0.02 * u))
            P["th" + side] = new_obj(name + "_th" + side, capsule_mesh(name + "th", s.thigh, 0.056 * u * build), mB, R)
            P["sh" + side] = new_obj(name + "_sh" + side, capsule_mesh(name + "sh", s.shin, 0.044 * u * build), mB, R)
            P["ft" + side] = new_obj(name + "_ft" + side, box_mesh(name + "ft", 0.16 * u, 0.065 * u, 0.045 * u), mSh, R)
        s.P = P
        # face
        r = s.hr
        hd = P["head"]
        dark = M((0.015, 0.012, 0.012), 0.5)
        if not silhouette:
            for sd, sg in (("L", 1), ("R", -1)):
                new_obj(name + "_eye" + sd, sphere_mesh(name + "e", 0.115 * r, 6, 4), M((0.9, 0.88, 0.85), 0.4),
                        hd, loc=(0.86 * r, sg * 0.38 * r, 0.12 * r))
                new_obj(name + "_pup" + sd, sphere_mesh(name + "pu", 0.07 * r, 6, 4), dark, hd,
                        loc=(0.93 * r, sg * 0.38 * r, 0.12 * r))
                P["brow" + sd] = new_obj(name + "_brow" + sd, box_mesh(name + "b", 0.1 * r, 0.5 * r, 0.1 * r, False), mH, hd,
                                         loc=(0.9 * r, sg * 0.4 * r, 0.42 * r))
                P["lip" + sd] = new_obj(name + "_lip" + sd, box_mesh(name + "l", 0.1 * r, 0.3 * r, 0.075 * r, False),
                                        M(tuple(c * 0.55 for c in sk), 0.7), hd, loc=(0.94 * r, sg * 0.17 * r, -0.42 * r))
            P["cav"] = new_obj(name + "_cav", box_mesh(name + "c", 0.1 * r, 0.42 * r, 0.5 * r, False), dark, hd,
                               loc=(0.9 * r, 0, -0.44 * r), scale=(1, 1, 0.01))
        new_obj(name + "_nose", box_mesh(name + "n", 0.22 * r, 0.16 * r, 0.3 * r, False), mS, hd, loc=(0.95 * r, 0, -0.05 * r))
        new_obj(name + "_hair", sphere_mesh(name + "hr", r * 1.06, 12, 8, (1, 1, 0.66)), mH, hd, loc=(-0.06 * r, 0, 0.32 * r))
        if headwear == "cap":
            m = M(hw_col, 0.8)
            new_obj(name + "_cap", sphere_mesh(name + "cp", r * 1.1, 12, 8, (1, 1, 0.7)), m, hd, loc=(-0.02 * r, 0, 0.38 * r))
            new_obj(name + "_brim", box_mesh(name + "br", 0.7 * r, 1.1 * r, 0.05 * r, False), m, hd, loc=(1.0 * r, 0, 0.42 * r))
        if "bun" in flags:
            new_obj(name + "_bun", sphere_mesh(name + "bn", r * 0.45, 8, 6), mH, hd, loc=(-0.85 * r, 0, 0.55 * r))
        if "moustache" in flags:
            new_obj(name + "_mous", box_mesh(name + "m", 0.1 * r, 0.75 * r, 0.14 * r, False), mH, hd, loc=(0.96 * r, 0, -0.27 * r))
        T = P["torso"]
        td = 0.15 * u * build
        if "scarf" in flags:
            sc = M((0.72, 0.66, 0.45), 0.9)
            new_obj(name + "_scarf", box_mesh(name + "sc", td * 1.5, 2 * s.sw * 0.7, 0.07 * u, False), sc, T,
                    loc=(0, 0, s.torsoL - 0.015 * u))
            new_obj(name + "_scarftail", box_mesh(name + "st", 0.02 * u, 0.1 * u, 0.26 * u), sc, T,
                    loc=(td * 0.55, s.sw * 0.3, s.torsoL * 0.55))
        if "dupatta" in flags:
            dp = M((0.17, 0.42, 0.42), 0.9)
            new_obj(name + "_dup", box_mesh(name + "dp", td * 1.25, 0.09 * u, s.torsoL * 1.0, False), dp, T,
                    loc=(0, -s.sw * 0.1, s.torsoL * 0.5), rot=(math.radians(-38), 0, 0))
            new_obj(name + "_duptail", box_mesh(name + "dt", 0.025 * u, 0.1 * u, 0.5 * u), dp, T,
                    loc=(0, -s.sw * 1.02, s.torsoL * 0.85 - 0.5 * u))
        if "pin" in flags:
            new_obj(name + "_pin", box_mesh(name + "pn", 0.012 * u, 0.025 * u, 0.012 * u, False),
                    M((0.85, 0.85, 0.9), 0.25, 1.0), T, loc=(td / 2 + 0.006 * u, 0.0, s.torsoL * 0.62))
            new_obj(name + "_zip", box_mesh(name + "zp", 0.006 * u, 0.012 * u, s.torsoL * 0.8, False),
                    M((0.25, 0.28, 0.35), 0.6), T, loc=(td / 2 + 0.002 * u, 0.0, s.torsoL * 0.5))
        self.flags = flags

    # --------------------------------------------------------------- authoring
    def at(self, t, x, y, yaw=0.0):
        if self.wp:
            last = self.wp[-1]
            self.wp.append(dict(t=t - 1e-4, x=last["x"], y=last["y"], yaw=last["yaw"], mode="lin", gait="stand", tt=0.5))
        self.wp.append(dict(t=t, x=x, y=y, yaw=yaw, mode="lin", gait="stand", tt=0.5))
        return self

    def walk(self, t, x, y, yaw=None, mode="lin", gait="walk", tt=0.45):
        last = self.wp[-1]
        if yaw is None:
            yaw = math.atan2(y - last["y"], x - last["x"])
        self.wp.append(dict(t=t, x=x, y=y, yaw=yaw, mode=mode, gait=gait, tt=tt))
        return self

    def stay(self, t, yaw=None, tt=0.5):
        last = self.wp[-1]
        self.wp.append(dict(t=t, x=last["x"], y=last["y"], yaw=last["yaw"] if yaw is None else yaw, mode="lin",
                            gait="stand", tt=tt))
        return self

    def act(self, t0, t1, fade=0.25, **kw):
        self.acts.append((t0, t1, fade, kw))
        return self

    def show(self, t0, t1):
        self.windows.append((t0, t1))
        return self

    def _seg(self, t):
        wp = self.wp
        if t <= wp[0]["t"]:
            return None, wp[0]
        for i in range(1, len(wp)):
            if t <= wp[i]["t"]:
                return wp[i - 1], wp[i]
        return None, wp[-1]

    def pos_yaw(self, t):
        a, b = self._seg(t)
        if a is None:
            return b["x"], b["y"], b["yaw"], 0.0, "stand"
        dt = b["t"] - a["t"]
        u = (t - a["t"]) / dt if dt > 1e-6 else 1.0
        e = ease(u) if b["mode"] == "smooth" else u
        x, y = lerp(a["x"], b["x"], e), lerp(a["y"], b["y"], e)
        yaw = lerp_ang(a["yaw"], b["yaw"], ease(min(1.0, (t - a["t"]) / max(b["tt"], 1e-3))))
        v = 0.0
        if b["gait"] != "stand" and dt > 1e-6:
            dist = math.hypot(b["x"] - a["x"], b["y"] - a["y"])
            v = dist / dt * (1.0 if b["mode"] == "lin" else 6 * u * (1 - u))
        return x, y, yaw, v, b["gait"]

    def _prep_dist(self):
        T0, T1 = self.wp[0]["t"], self.wp[-1]["t"]
        dt = 1 / 120
        n = int((T1 - T0) / dt) + 2
        arr, d = [0.0], 0.0
        for i in range(1, n):
            v = self.pos_yaw(T0 + i * dt)[3]
            d += v * dt
            arr.append(d)
        self._dist = (T0, dt, arr)

    def dist(self, t):
        if self._dist is None:
            self._prep_dist()
        T0, dt, arr = self._dist
        i = min(max(int((t - T0) / dt), 0), len(arr) - 1)
        return arr[i]

    # --------------------------------------------------------------- skeleton
    def J(self, t):
        key = round(t * 2400)
        if key in self._jc:
            return self._jc[key]
        s, H = self, self.H
        x, y, yaw, v, gait = s.pos_yaw(t)
        run = gait == "run"
        walking = v > 0.12
        # numeric overlays
        pr = dict(lean=0.0, crouch=0.0, twist=0.0, hy=0.0, hp=0.0, brow=0.0, smile=0.12, open=0.0, bob=0.0, bobf=0.0)
        armL = armR = look = None
        wL = wR = wLk = 0.0
        for t0, t1, fade, kw in s.acts:
            if not (t0 <= t <= t1):
                continue
            w = min(ease((t - t0) / fade), ease((t1 - t) / fade)) if fade > 0 else 1.0
            u = (t - t0) / max(t1 - t0, 1e-6)
            for k, val in kw.items():
                if k in ("armL", "armR", "look"):
                    val = (lambda f_, t_, u_: (lambda: f_(t_, u_)))(val, t, u) if callable(val) else val   # resolved lazily
                    if k == "armL":
                        armL, wL = val, w
                    elif k == "armR":
                        armR, wR = val, w
                    else:
                        look, wLk = val, w
                elif k == "mood":
                    b_, s_, o_ = val(t, u) if callable(val) else val
                    pr["brow"] = lerp(pr["brow"], b_, w)
                    pr["smile"] = lerp(pr["smile"], s_, w)
                    pr["open"] = lerp(pr["open"], o_, w)
                elif k in pr:
                    val = val(t, u) if callable(val) else val
                    pr[k] = lerp(pr[k], val, w)
        # body
        fv, lv = fvec(yaw), lvec(yaw)
        root = Vector((x, y, 0))
        C = (0.95 if run else 0.82) * H
        A = C / 4
        ph = s.dist(t) / C
        sway = 0.0 if walking else math.sin(t * 1.1 + len(s.name)) * 0.008 * H
        bob = pr["bob"] * math.sin(2 * math.pi * pr["bobf"] * t) if pr["bobf"] else 0.0
        breath = 0.004 * H * math.sin(t * 2.0 + len(s.name))
        crouch = pr["crouch"] * H
        hipz = s.hipH - crouch + (0.012 * H * abs(math.sin(math.pi * ph * 2)) * -1 if walking else 0.0) + bob * H
        lean = pr["lean"] + (0.28 if run else (0.04 if walking else 0.0))
        hip_c = root + Vector((0, 0, hipz)) + lv * sway - fv * (crouch * 0.4 + math.sin(lean) * 0.0)
        spine = (fv * math.sin(lean) + ZUP * math.cos(lean)).normalized()
        sh_c = hip_c + spine * s.torsoL + ZUP * breath
        ty = yaw + pr["twist"]
        tf, tl = fvec(ty), lvec(ty)
        tf = (tf - spine * tf.dot(spine)).normalized()
        shL, shR = sh_c + tl * s.sw, sh_c - tl * s.sw
        # head
        hyaw, hpit = pr["hy"], pr["hp"]
        neck = sh_c + spine * 0.012 * H
        self._jc[key] = dict(root=root, yaw=yaw, hip_c=hip_c, spine=spine, tf=tf, tl=tl, sh_c=sh_c, ty=ty, H=H, pr=pr, v=v)
        if look is not None:
            look = look() if callable(look) else look
            tgt = Vector(look)
            hc0 = neck + spine * (s.hr + 0.006 * H)
            d = tgt - hc0
            ly = wrap(math.atan2(d.y, d.x) - ty)
            lp = math.atan2(-d.z, max(math.hypot(d.x, d.y), 1e-6))
            ly = max(-1.25, min(1.25, ly))
            lp = max(-0.7, min(0.7, lp))
            hyaw, hpit = lerp(hyaw, ly, wLk), lerp(hpit, lp, wLk)
        hfy = fvec(ty + hyaw)
        hf = hfy * math.cos(hpit) - ZUP * math.sin(hpit)
        hu = ZUP * math.cos(hpit) + hfy * math.sin(hpit)
        hu = (hu + spine * 0.0).normalized()
        head_c = neck + hu * (s.hr + 0.006 * H)
        # legs
        hipL, hipR = hip_c + lv * s.hw, hip_c - lv * s.hw
        ft = {}
        for sd, sg, off in (("L", 1, 0.0), ("R", -1, 0.5)):
            if walking:
                cyc = 2 * math.pi * (ph + off)
                fwd = A * math.cos(cyc) * min(1.0, v / 1.0)
                lift = max(0.0, -math.sin(cyc)) * (0.13 if run else 0.045) * H * min(1.0, v / 0.8)
                p = root + fv * fwd + lv * sg * s.hw * 0.9 + Vector((0, 0, lift))
            else:
                p = root + lv * sg * (s.hw * 1.05) + fv * (0.01 * H * sg)
            ft[sd] = p
        pole = fv
        out = self._jc[key]
        out.update(head_c=head_c, hf=hf, hu=hu, ft=ft, walking=walking)
        kn, an = {}, {}
        for sd, hp_ in (("L", hipL), ("R", hipR)):
            tgt = ft[sd] + Vector((0, 0, s.ankle))
            k_, a_ = ik2(hp_, tgt, s.thigh, s.shin, pole + (lv if sd == "L" else -lv) * 0.15)
            kn[sd], an[sd] = k_, a_
        # arms
        swing = (0.11 if not run else 0.2) * H * min(1.0, v / 1.0) if walking else 0.0
        arms = {}
        for sd, sg, shp, ov, wv in (("L", 1, shL, armL, wL), ("R", -1, shR, armR, wR)):
            drop = 0.33 * H if not run else 0.22 * H
            fw = (-swing * math.cos(2 * math.pi * ph) * sg) if walking else 0.015 * H * math.sin(t * 0.9 + sg)
            nat = shp + tf * fw + tl * sg * 0.035 * H + Vector((0, 0, -drop + (0.04 * H if run else 0)))
            if callable(ov):
                ov = ov()
            if ov is not None:
                if isinstance(ov, tuple):
                    kind = ov[0]
                    if kind == "loc":
                        ov = root + fv * ov[1] * H + lv * ov[2] * H + ZUP * ov[3] * H
                    elif kind == "rel":
                        ov = shp + tf * ov[1] * H + tl * ov[2] * H + ZUP * ov[3] * H
                tgt = nat.lerp(Vector(ov), wv)
            else:
                tgt = nat
            pole_a = Vector((0, 0, -1)) + tl * sg * 0.45 - tf * 0.25
            el, wr = ik2(shp, tgt, s.ua, s.fa + 0.0, pole_a)
            arms[sd] = (shp, el, wr)
        out.update(kn=kn, an=an, hip=(hipL, hipR), arms=arms)
        out["wrist"] = {k: arms[k][2] for k in "LR"}
        out["hand"] = {k: arms[k][2] + (arms[k][2] - arms[k][1]).normalized() * (0.02 * H + 0.032 * H) for k in "LR"}
        out["torso_M"] = Matrix.Translation(hip_c) @ basis_quat(tf, spine).to_matrix().to_4x4()
        return out

    # --------------------------------------------------------------- baking
    def bake(self, t0, t1, anim=ANIM, full_face=True):
        self.windows.append((t0, t1)) if (t0, t1) not in self.windows else None
        prev = {}
        f0, f1 = int(round(F(t0))), int(round(F(t1)))
        P, s, H = self.P, self, self.H
        for f in range(f0, f1 + 1):
            t = (f - 1) / FPS
            j = self.J(t)
            # torso / head
            q = basis_quat(j["tf"], j["spine"], prev.get("torso"))
            prev["torso"] = q
            self._put(anim, P["torso"], f, j["hip_c"], q)
            q = basis_quat(j["hf"], j["hu"], prev.get("head"))
            prev["head"] = q
            self._put(anim, P["head"], f, j["head_c"], q)
            for sd in "LR":
                shp, el, wr = j["arms"][sd]
                q = seg_quat(shp, el, prev.get("ua" + sd))
                prev["ua" + sd] = q
                self._put(anim, P["ua" + sd], f, shp, q)
                q = seg_quat(el, wr, prev.get("fa" + sd))
                prev["fa" + sd] = q
                self._put(anim, P["fa" + sd], f, el, q)
                hp_ = j["hip"][0 if sd == "L" else 1]
                q = seg_quat(hp_, j["kn"][sd], prev.get("th" + sd))
                prev["th" + sd] = q
                self._put(anim, P["th" + sd], f, hp_, q)
                q = seg_quat(j["kn"][sd], j["an"][sd], prev.get("sh" + sd))
                prev["sh" + sd] = q
                self._put(anim, P["sh" + sd], f, j["kn"][sd], q)
                fq = Quaternion((0, 0, 1), j["yaw"])
                self._put(anim, P["ft" + sd], f, j["ft"][sd] + j["tf"].normalized() * 0.0 + fvec(j["yaw"]) * 0.03 * H, fq)
            if full_face and "browL" in P:
                pr = j["pr"]
                k = pr["brow"] * 0.6
                anim.put(P["browL"], "rotation_euler", 0, f, k)
                anim.put(P["browR"], "rotation_euler", 0, f, -k)
                sm = pr["smile"] * 0.7
                anim.put(P["lipL"], "rotation_euler", 0, f, sm)
                anim.put(P["lipR"], "rotation_euler", 0, f, -sm)
                anim.put(P["cav"], "scale", 2, f, max(0.01, pr["open"]))
        # root visibility (parent scale; children collapse when hidden)
        return self

    def _put(self, anim, ob, f, loc, q):
        anim.put(ob, "location", 0, f, loc.x)
        anim.put(ob, "location", 1, f, loc.y)
        anim.put(ob, "location", 2, f, loc.z)
        anim.put(ob, "rotation_quaternion", 0, f, q.w)
        anim.put(ob, "rotation_quaternion", 1, f, q.x)
        anim.put(ob, "rotation_quaternion", 2, f, q.y)
        anim.put(ob, "rotation_quaternion", 3, f, q.z)

    def finalize(self, end_t, anim=ANIM):
        for k in ("torso", "head"):
            self.P[k].rotation_mode = "QUATERNION"
        for k, ob in self.P.items():
            if k[:2] in ("ua", "fa", "th", "sh", "ft"):
                ob.rotation_mode = "QUATERNION"
        # scale-hide windows
        ws = sorted(self.windows)
        evs = [(1, 1e-5)]
        for a, b in ws:
            evs.append((int(round(F(a))), 1.0))
            evs.append((int(round(F(b))) + 1, 1e-5))
        for f, val in evs:
            for i in range(3):
                anim.put(self.root, "scale", i, f, val, "const")


# ------------------------------------------------------------------ crowd
_CROWD = {}


def crowd_mesh(i, cloth):
    if i in _CROWD:
        return _CROWD[i]
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=8, v_segments=6, radius=0.2)
    for vt in bm.verts:
        z = vt.co.z
        vt.co.z = (z + 0.55) if z > 1e-6 else (z - 0.55 if z < -1e-6 else z)
        vt.co.z += 0.78
        vt.co.x *= 0.85
    bmesh.ops.create_uvsphere(bm, u_segments=8, v_segments=5, radius=0.11, matrix=Matrix.Translation((0, 0, 1.64)))
    for f_ in bm.faces:
        f_.material_index = 1 if f_.calc_center_median().z > 1.5 else 0
    out = to_mesh("crowdm%d" % i, bm)
    out.materials.append(M(cloth, 0.9))
    out.materials.append(M(SKIN["abcd"[i % 4]], 0.7))
    _CROWD[i] = out
    return out


CROWD_COLORS = [(0.20, 0.22, 0.28), (0.30, 0.26, 0.20), (0.18, 0.28, 0.25), (0.34, 0.33, 0.30), (0.25, 0.20, 0.30),
                (0.40, 0.36, 0.25), (0.14, 0.14, 0.16), (0.30, 0.30, 0.38), (0.36, 0.27, 0.22), (0.22, 0.33, 0.20)]


def make_crowd(n, seed, regions, T, speed=(0.1, 1.15), stand_frac=0.28):
    """regions: [(x0,x1,y0,y1,weight[,axis])]; walkers drift along the region's axis for the whole film."""
    rnd = random.Random(seed)
    tot = sum(r[4] for r in regions)
    out = []
    for i in range(n):
        pick, acc = rnd.random() * tot, 0
        for r in regions:
            acc += r[4]
            if pick <= acc:
                break
        x0, x1, y0, y1 = r[:4]
        ax = r[5] if len(r) > 5 else "x"
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        sp = 0.02 if rnd.random() < stand_frac else rnd.uniform(*speed)
        dirn = rnd.choice((-1, 1))
        lo, hi, cur = (x0, x1, x) if ax == "x" else (y0, y1, y)
        room = (hi - cur) if dirn > 0 else (cur - lo)
        if room < sp * T:
            dirn = -dirn
            room = (hi - cur) if dirn > 0 else (cur - lo)
            sp = min(sp, max(room, 0.2) / T)
        d = dirn * sp * T
        ex, ey = (x + d, y) if ax == "x" else (x, y + d)
        yaw = (0.0 if dirn > 0 else math.pi) if ax == "x" else (math.pi / 2 if dirn > 0 else -math.pi / 2)
        out.append(dict(x=x, y=y, ex=ex, ey=ey, h=rnd.uniform(1.52, 1.86), c=i % len(CROWD_COLORS),
                        yaw=yaw if sp > 0.05 else rnd.uniform(0, 6.28), sp=sp))
    return out


def write_crowd(walkers, T, prune=None):
    cnt = 0
    for i, w in enumerate(walkers):
        if prune and prune(w):
            continue
        ob = bpy.data.objects.new("crowd%d" % i, crowd_mesh(w["c"], CROWD_COLORS[w["c"]]))
        link(ob)
        ob.location = (w["x"], w["y"], 0)
        ob.rotation_euler = (0, 0, w["yaw"])
        ob.scale = (1, 1, w["h"] / 1.75)
        if w["sp"] > 0.05:
            for k, (a, b) in enumerate(((w["x"], w["ex"]), (w["y"], w["ey"]))):
                ANIM.put(ob, "location", k, 1, a, "lin")
                ANIM.put(ob, "location", k, F(T), b, "lin")
        cnt += 1
    return cnt


def walker_pos(w, t, T):
    u = min(max(t / T, 0), 1)
    return w["x"] + (w["ex"] - w["x"]) * u, w["y"] + (w["ey"] - w["y"]) * u


# ------------------------------------------------------------------ camera
def noise(t, seed, f=1.0):
    r = random.Random(seed)
    ph = [r.uniform(0, 6.28) for _ in range(6)]
    return (math.sin(t * 2.1 * f + ph[0]) * 0.5 + math.sin(t * 3.7 * f + ph[1]) * 0.3 + math.sin(t * 6.3 * f + ph[2]) * 0.2,
            math.sin(t * 1.9 * f + ph[3]) * 0.5 + math.sin(t * 4.1 * f + ph[4]) * 0.3 + math.sin(t * 7.1 * f + ph[5]) * 0.2)


class Cam:
    def __init__(self, name="Film_Cam"):
        d = bpy.data.cameras.new(name)
        d.sensor_fit = "AUTO"
        d.sensor_width = 36
        d.clip_start, d.clip_end = 0.05, 20000
        d.dof.use_dof = True
        self.ob = bpy.data.objects.new(name, d)
        link(self.ob)
        self.ob.rotation_mode = "QUATERNION"
        bpy.context.scene.camera = self.ob
        self.d = d
        self.prev = None
        self.log = []

    def shot(self, t0, t1, fn, hand=0.0, seed=0, fstop_default=16.0):
        """fn(t) -> dict(pos, look, lens, focus (point or dist), fstop). hand = handheld amount (0..1)."""
        f0, f1 = int(round(F(t0))), int(round(F(t1))) - 1
        prev = None
        for f in range(f0, f1 + 1):
            t = (f - 1) / FPS
            c = fn(t)
            pos, look = Vector(c["pos"]), Vector(c["look"])
            if hand:
                nx, ny = noise(t, seed * 7 + 1)
                nz, nr = noise(t, seed * 7 + 2, 1.3)
                pos = pos + Vector((nx, ny, nz)) * 0.012 * hand
                d = (look - pos)
                dist = max(d.length, 0.5)
                look = look + Vector((noise(t, seed * 7 + 3)[0], noise(t, seed * 7 + 4)[1], noise(t, seed * 7 + 5)[0])) * 0.012 * hand * dist * 0.9
            up = Vector((0, 0, 1))
            q = (look - pos).to_track_quat("-Z", "Y")
            roll = c.get("roll", 0.0)
            if roll:
                q = q @ Quaternion((0, 0, 1), roll)
            if prev is not None and q.dot(prev) < 0:
                q.negate()
            prev = q
            ob = self.ob
            for i, v in enumerate(pos):
                ANIM.put(ob, "location", i, f, v)
            for i, v in enumerate((q.w, q.x, q.y, q.z)):
                ANIM.put(ob, "rotation_quaternion", i, f, v)
            ANIM.put(self.d, "lens", 0, f, c["lens"])
            fo = c.get("focus")
            if fo is None:
                fd = (look - pos).length
            elif isinstance(fo, (int, float)):
                fd = fo
            else:
                fd = (Vector(fo) - pos).length
            ANIM.put(self.d, "dof.focus_distance", 0, f, max(fd, 0.1))
            ANIM.put(self.d, "dof.aperture_fstop", 0, f, c.get("fstop", fstop_default))
