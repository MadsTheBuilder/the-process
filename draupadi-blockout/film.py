# film.py - helpers shared by every scene of the DRAUPADI SE DRAUPADI TAK blockout.
# Timeline context (shot times from shots.json), lens-aware camera framing, per-shot key/fill/rim rig,
# light states, props that ride on hands, tears, text. Built on kit.py (mannequins, Anim, Builder, Cam).
import json
import math
import os
import re

import bpy
from mathutils import Euler, Matrix, Quaternion, Vector

from kit import *

HERE = os.path.dirname(os.path.abspath(__file__))
SENSOR_W = 36.0
ASPECT = 2.39
SENSOR_H = SENSOR_W / ASPECT          # 15.06 mm: the vertical gate for 2.39:1
RES = (1920, 804)

# frame heights (m) a magnification fills, measured on the subject plane
MAG_H = {"ECU": 0.13, "CU": 0.34, "MCU": 0.58, "MS": 1.0, "MLS": 1.45, "LS": 3.2, "WS": 4.2, "EWS": 30.0,
         "GS": 1.6, "INS": 0.42, "CI": 0.35, "2S": 1.1, "OTS": 0.7, "POV": 1.0}


def kelvin(k):
    """Colour temperature -> linear-ish RGB (Tanner Helland fit, normalised so 6500K ~ white)."""
    t = k / 100.0
    if t <= 66:
        r = 255
        g = 99.47 * math.log(t) - 161.12
        b = 0 if t <= 19 else 138.52 * math.log(t - 10) - 305.04
    else:
        r = 329.7 * (t - 60) ** -0.1332
        g = 288.12 * (t - 60) ** -0.0755
        b = 255
    c = [min(max(v, 0), 255) / 255 for v in (r, g, b)]
    return tuple(v ** 2.2 for v in c)


GREEN = (0.55, 1.0, 0.6)      # plusgreen gel tint, multiplied in


def tint(a, b):
    return tuple(x * y for x, y in zip(a, b))


# ---------------------------------------------------------------------------------------- objects
def lamp(name, kind, loc, energy=0.0, color=(1, 1, 1), size=0.3, shadow=True, spot=None, rot=None):
    d = bpy.data.lights.new(name, kind)
    d.energy, d.color, d.use_shadow = energy, color, shadow
    if kind in ("POINT", "SPOT"):
        d.shadow_soft_size = size
    elif kind == "AREA":
        d.shape = "RECTANGLE"
        if isinstance(size, (tuple, list)):
            d.size, d.size_y = size
        else:
            d.size = d.size_y = size
    elif kind == "SUN":
        d.angle = size
    if kind == "SPOT" and spot:
        d.spot_size = math.radians(spot)
        d.spot_blend = 0.6
    ob = bpy.data.objects.new(name, d)
    link(ob)
    ob.location = loc
    if rot is not None:
        ob.rotation_euler = rot
    return ob


def aim(ob, target):
    q = (Vector(target) - ob.location).to_track_quat("-Z", "Y")
    ob.rotation_euler = q.to_euler()
    return ob


def aim_quat(pos, target):
    return (Vector(target) - Vector(pos)).to_track_quat("-Z", "Y")


def text3d(body, size, mat, loc, rot=(math.pi / 2, 0, 0), extrude=0.0, align="CENTER"):
    c = bpy.data.curves.new("txt", "FONT")
    c.body, c.size, c.align_x, c.align_y, c.extrude = body, size, align, "CENTER", extrude
    ob = bpy.data.objects.new("txt", c)
    ob.data.materials.append(mat)
    link(ob)
    ob.location, ob.rotation_euler = loc, rot
    return ob


def vis(ob, wins, inverse=False):
    """visible only during windows (or hidden during them when inverse). Constant keys."""
    on, off = (1, 0) if inverse else (0, 1)
    for p in ("hide_render", "hide_viewport"):
        ANIM.put(ob, p, 0, 1, off, "const")
        for a, b in wins:
            ANIM.put(ob, p, 0, int(round(F(a))), on, "const")
            ANIM.put(ob, p, 0, int(round(F(b))), off, "const")


def vis_tree(ob, wins, inverse=False):
    vis(ob, wins, inverse)
    for ch in ob.children_recursive:
        vis(ch, wins, inverse)


def spin(ob, axis, rps, t_end, phase=0.0):
    """constant rotation (ceiling fans) over the whole timeline."""
    ob.rotation_mode = "XYZ"
    i = "XYZ".index(axis)
    ANIM.put(ob, "rotation_euler", i, 1, phase, "lin")
    ANIM.put(ob, "rotation_euler", i, F(t_end), phase + 2 * math.pi * rps * t_end, "lin")


def keys(ob, path, idx, pts, kind="bez"):
    """pts: [(t, value)] -> keys on the timeline."""
    for t, v in pts:
        ANIM.put(ob, path, idx, F(t), v, kind)


def keys_vec(ob, path, pts, kind="bez"):
    for t, v in pts:
        for i, c in enumerate(v):
            ANIM.put(ob, path, i, F(t), c, kind)


def bake_fn(ob, t0, t1, fn, step=1, rot=True):
    """fn(t) -> (loc, quat or None). Per-frame transform bake for props."""
    ob.rotation_mode = "QUATERNION"
    prev = None
    f0, f1 = int(round(F(t0))), int(round(F(t1)))
    for f in list(range(f0, f1 + 1, step)) + [f1]:
        t = (f - 1) / FPS
        loc, q = fn(t)
        for i in range(3):
            ANIM.put(ob, "location", i, f, loc[i])
        if q is not None and rot:
            q = Quaternion(q)
            if prev is not None and q.dot(prev) < 0:
                q.negate()
            prev = q
            for i, v in enumerate((q.w, q.x, q.y, q.z)):
                ANIM.put(ob, "rotation_quaternion", i, f, v)


def hold(ob, actor, side, t0, t1, off=(0, 0, 0), along=True, step=1):
    """prop rides on a hand: off is in the forearm frame (x along forearm, z up-ish)."""
    def fn(t):
        j = actor.J(t)
        sh, el, wr = j["arms"][side]
        h = j["hand"][side]
        q = seg_quat(el, wr) if along else Quaternion()
        return h + q @ Vector(off), q
    bake_fn(ob, t0, t1, fn, step)


# ---------------------------------------------------------------------------------------- camera framing
def dist_for(mag, lens, h=None):
    h = h or MAG_H.get(mag.split()[0].replace("/", ""), 1.0)
    return h * lens / SENSOR_H


def width_at(d, lens):
    return d * SENSOR_W / lens


def from_dir(az_deg, el_deg):
    a, e = math.radians(az_deg), math.radians(el_deg)
    return Vector((math.cos(a) * math.cos(e), math.sin(a) * math.cos(e), math.sin(e)))


def frame(target, face_yaw, lens, mag=None, d=None, az=0.0, el=0.0, third=0.0, up=0.0, fstop=None, h=None):
    """Camera looking at `target` from direction az (deg, relative to the subject's facing: 0 = in front),
    el (deg above). d from the magnification unless given. third: -1/+1 shifts the subject to a frame third
    (positive puts the subject on frame-left). up: look-point offset in metres (headroom)."""
    target = Vector(target)
    d = d or dist_for(mag, lens, h)
    dirv = from_dir(math.degrees(face_yaw) + az, el)
    pos = target + dirv * d
    look = target + Vector((0, 0, up))
    if third:
        fwd = (look - pos).normalized()
        right = fwd.cross(ZUP).normalized()
        look = look + right * third * width_at(d, lens) / 6
    out = dict(pos=pos, look=look, lens=lens, focus=d)
    if fstop:
        out["fstop"] = fstop
    return out


def head(a, t, dz=0.0):
    return a.J(t)["head_c"] + Vector((0, 0, dz))


def eyes(a, t):
    j = a.J(t)
    return j["head_c"] + j["hf"] * a.hr * 0.6 + j["hu"] * a.hr * 0.1


def est(a, t, k=0.93):
    """head estimate from the waypoints only (no skeleton): safe inside another actor's look/arm lambdas."""
    x, y = a.pos_yaw(t)[:2]
    return Vector((x, y, a.H * k))


def est_seated(a, t, seat=0.4):
    x, y = a.pos_yaw(t)[:2]
    return Vector((x, y, seat + 0.05 * a.H + 0.29 * a.H + a.hr))


def chest(a, t):
    j = a.J(t)
    return j["sh_c"] - j["spine"] * 0.12 * a.H


def waist(a, t):
    return a.J(t)["hip_c"] + Vector((0, 0, 0.15 * a.H))


def face_yaw(a, t):
    j = a.J(t)
    return math.atan2(j["hf"].y, j["hf"].x)


def mid(*ps):
    v = Vector()
    for p in ps:
        v += Vector(p)
    return v / len(ps)


def on(a, t, mag, lens, az=0.0, el=0.0, third=0.0, h=None, yaw=None, tt=None, dx=0.0, fstop=None):
    """frame a person: eyes on the upper-third line. yaw: facing used for az (default the actor's face yaw at tt)."""
    tt = t if tt is None else tt
    hh = h or MAG_H.get(mag.split()[0].replace("/", ""), 1.0)
    e = eyes(a, t)
    tgt = e - Vector((0, 0, hh / 6))
    y = face_yaw(a, tt) if yaw is None else yaw
    c = frame(tgt, y, lens, mag, h=hh, az=az, el=el, third=third, fstop=fstop)
    if dx:
        c["pos"] = Vector(c["pos"]) + Vector((math.cos(y + math.pi / 2), math.sin(y + math.pi / 2), 0)) * dx
    c["focus"] = (e - Vector(c["pos"])).length
    return c


def ots(over, onto, t, lens, mag="MCU", side=1, out_=0.3, dz=0.06, h=None, back=None):
    """Over `over`'s shoulder onto `onto`, at the distance the magnification needs (long-lens OTS).
    side=+1 over the left shoulder of `over` (the near shoulder lands frame-right), -1 the right shoulder."""
    jo = over.J(t)
    tgt = eyes(onto, t)
    sh = jo["sh_c"]
    fwd = tgt - sh
    fwd.z = 0
    fwd.normalize()
    lat = ZUP.cross(fwd) * side
    through = sh + lat * out_ + Vector((0, 0, over.hr * 1.3 + dz))
    d = dist_for(mag, lens, h)
    d = max(d, (tgt - through).length + 0.45)
    pos = tgt + (through - tgt).normalized() * d
    return dict(pos=pos, look=tgt + Vector((0, 0, -0.04)) - lat * width_at(d, lens) * 0.07, lens=lens, focus=d)


def push(c0, k, toward=None):
    """move camera dict c0 a fraction k of the way to its look point (push in)."""
    c = dict(c0)
    p, l = Vector(c0["pos"]), Vector(toward or c0["look"])
    c["pos"] = p.lerp(l, k)
    c["focus"] = (Vector(c0["look"]) - c["pos"]).length
    return c


def blend(c0, c1, u):
    c = dict(c1)
    c["pos"] = Vector(c0["pos"]).lerp(Vector(c1["pos"]), u)
    c["look"] = Vector(c0["look"]).lerp(Vector(c1["look"]), u)
    c["lens"] = lerp(c0.get("lens", 50), c1.get("lens", 50), u)
    if "focus" in c0 and "focus" in c1 and isinstance(c0["focus"], (int, float)) and isinstance(c1["focus"], (int, float)):
        c["focus"] = lerp(c0["focus"], c1["focus"], u)
    return c


# ---------------------------------------------------------------------------------------- scene context
def lens_of(s):
    m = re.match(r"(\d+)", s)
    return int(m.group(1)) if m else 50


def hand_of(mov):
    m = mov.lower()
    if "handheld (nervous)" in m or "whip" in m:
        return 1.7
    if "handheld" in m:
        return 0.7
    if "gimbal" in m or "steadicam" in m:
        return 0.3
    if "drone" in m or "crane" in m:
        return 0.15
    if "boat" in m:
        return 0.35
    return 0.04                    # a locked-off tripod still breathes a hair


class Ctx:
    def __init__(self, scene_no):
        data = json.load(open(os.path.join(HERE, "shots.json"), encoding="utf8"))
        self.no = scene_no
        self.sc = data[scene_no - 1]
        self.shots = {s["no"]: s for s in self.sc["shots"]}
        self.T = {}
        t = 0.0
        for s in self.sc["shots"]:
            self.T[s["no"]] = (t, t + s["dur"])
            t += s["dur"]
        self.END = t
        self.cams = {}
        self.hands = {}
        self.actors = []
        self.keys_ = {}
        self.rig = None
        self.cam = None

    def first(self):
        return self.sc["shots"][0]["no"]

    def last(self):
        return self.sc["shots"][-1]["no"]

    def lens(self, n):
        return lens_of(self.shots[n]["lens"])

    def shoot(self, n, fn, hand=None):
        """register the camera function for shot n; fn(t)->dict(pos, look[, lens, focus, fstop, roll])."""
        self.cams[n] = fn
        if hand is not None:
            self.hands[n] = hand

    def on(self, a, shots, step=1, pad=0.0):
        """bake actor a over the listed shots (contiguous shots merge into one window)."""
        shots = sorted(shots)
        wins = []
        for n in shots:
            t0, t1 = self.T[n]
            if wins and abs(wins[-1][1] - t0) < 1e-6:
                wins[-1][1] = t1
            else:
                wins.append([t0, t1])
        self._pending = getattr(self, "_pending", [])
        for w0, w1 in wins:
            self._pending.append((a, max(0.0, w0 - pad), min(self.END, w1), step))
        self.add(a)
        return a

    def bake_actors(self):
        """baking is deferred until every actor's waypoints exist (actors look at / reach for each other)."""
        for a, w0, w1, step in getattr(self, "_pending", []):
            a.bake(w0, w1, step=step)
        self._pending = []

    def add(self, *actors):
        for a in actors:
            if a not in self.actors:
                self.actors.append(a)

    # ------------------------------------------------ per-shot lighting rig (key / fill / rim follow the shot)
    def make_rig(self):
        self.rig = dict(key=lamp("RIG_key", "AREA", (0, 0, -50), 0, size=1.2),
                        fill=lamp("RIG_fill", "AREA", (0, 0, -50), 0, size=2.0, shadow=False),
                        rim=lamp("RIG_rim", "AREA", (0, 0, -50), 0, size=0.8),
                        kick=lamp("RIG_kick", "SPOT", (0, 0, -50), 0, size=0.05, spot=30))
        for ob in self.rig.values():
            ob.rotation_mode = "QUATERNION"

    def light(self, n, subj, key=None, fill=None, rim=None, kick=None, t=None):
        """Shot-local light rig. Each spec: dict(side='L'/'R' (frame side the light comes from), ang=45 (deg off
        the lens axis), el=25, d=2.0, w=watts, k=kelvin, size, tint). Rim specs come from behind (ang ~150).
        subj: point or callable(t). Lights jump at the cut (constant keys)."""
        if self.rig is None:
            self.make_rig()
        t0, t1 = self.T[n]
        tt = t if t is not None else t0 + 0.01
        c = self.cams[n](tt)
        S = Vector(subj(tt) if callable(subj) else subj)
        cp = Vector(c["pos"])
        to_cam = cp - S
        to_cam.z = 0
        if to_cam.length < 1e-4:
            to_cam = Vector((0, -1, 0))
        to_cam.normalize()
        for name, spec in (("key", key), ("fill", fill), ("rim", rim), ("kick", kick)):
            ob = self.rig[name]
            if not spec:
                self._lk(ob, t0, None)
                continue
            side = 1 if spec.get("side", "L") == "L" else -1
            ang = math.radians(spec.get("ang", 45 if name != "rim" else 150))
            # frame-left of the camera = the subject's right as seen from the lens
            left = ZUP.cross(-to_cam)          # camera's left in world
            hd = (to_cam * math.cos(ang) + left * side * math.sin(ang)).normalized()
            el = math.radians(spec.get("el", 22))
            d = spec.get("d", 2.2)
            pos = S + (hd * math.cos(el) + ZUP * math.sin(el)) * d
            col = kelvin(spec.get("k", 5600))
            if spec.get("tint"):
                col = tint(col, spec["tint"])
            self._lk(ob, t0, (pos, aim_quat(pos, S), spec.get("w", 60), col, spec.get("size")))

    def _lk(self, ob, t0, st):
        f = int(round(F(t0)))
        if st is None:
            ANIM.put(ob.data, "energy", 0, f, 0.0, "const")
            return
        pos, q, w, col, size = st
        for i in range(3):
            ANIM.put(ob, "location", i, f, pos[i], "const")
            ANIM.put(ob.data, "color", i, f, col[i], "const")
        for i, v in enumerate((q.w, q.x, q.y, q.z)):
            ANIM.put(ob, "rotation_quaternion", i, f, v, "const")
        ANIM.put(ob.data, "energy", 0, f, w, "const")
        if size and ob.data.type == "AREA":
            ANIM.put(ob.data, "size", 0, f, size, "const")
            ANIM.put(ob.data, "size_y", 0, f, size, "const")

    # ------------------------------------------------ light states for set lights (constant keys)
    def state(self, t, **lights):
        """state(t, Win=(watts, kelvin[, tint]), Bulb=0, ...): set-light energies/colours from time t."""
        f = int(round(F(t)))
        for name, v in lights.items():
            ob = bpy.data.objects.get(name)
            if ob is None or ob.type != "LIGHT":
                raise KeyError("no light " + name)
            if isinstance(v, (int, float)):
                ANIM.put(ob.data, "energy", 0, f, float(v), "const")
                continue
            w, k = v[0], v[1]
            col = kelvin(k)
            if len(v) > 2 and v[2]:
                col = tint(col, v[2])
            ANIM.put(ob.data, "energy", 0, f, float(w), "const")
            for i in range(3):
                ANIM.put(ob.data, "color", i, f, col[i], "const")

    def emit(self, t, mat, strength, color=None):
        """emissive material strength state (practical bulbs, fairy lights)."""
        f = int(round(F(t)))
        ANIM.put(mat.node_tree, 'nodes["Principled BSDF"].inputs[\"Emission Strength\"].default_value', 0, f, strength, "const")
        if color:
            for i in range(3):
                ANIM.put(mat.node_tree, 'nodes["Principled BSDF"].inputs[\"Emission Color\"].default_value', i, f, color[i], "const")

    def world(self, t, color, strength):
        w = bpy.context.scene.world
        bg = w.node_tree.nodes["Background"]
        f = int(round(F(t)))
        for i in range(3):
            ANIM.put(w.node_tree, 'nodes["Background"].inputs[0].default_value', i, f, color[i], "const")
        ANIM.put(w.node_tree, 'nodes["Background"].inputs[1].default_value', 0, f, strength, "const")

    def exposure(self, t, ev):
        ANIM.put(bpy.context.scene, "view_settings.exposure", 0, int(round(F(t))), ev, "const")

    # ------------------------------------------------ bake everything
    def bake_cameras(self):
        cam = self.cam or Cam()
        self.cam = cam
        for n, (a, b) in self.T.items():
            if n not in self.cams:
                continue
            fn = self.cams[n]
            ln = self.lens(n)
            hand = self.hands.get(n, hand_of(self.shots[n]["mov"]))

            def wrap(t, fn=fn, ln=ln):
                c = fn(t)
                c.setdefault("lens", ln)
                c.setdefault("fstop", 2.0 if c["lens"] >= 85 else (2.8 if c["lens"] >= 50 else 4.0))
                return c
            cam.shot(a, b, wrap, hand=hand, seed=n)
            self._check_line(n, wrap((a + b) / 2))
        return cam

    def _check_line(self, n, c):
        """warn when set geometry sits between the lens and what it looks at (camera inside a wall etc.)."""
        dg = bpy.context.evaluated_depsgraph_get()
        sc = bpy.context.scene
        p, l = Vector(c["pos"]), Vector(c["look"])
        d = p - l
        dist = d.length
        if dist < 0.05:
            return
        hit, loc, nrm, idx, ob, mtx = sc.ray_cast(dg, l + d.normalized() * 0.02, d.normalized(), distance=dist - 0.04)
        if hit and ob and ob.name.split("_")[0] in ("HOUSE", "SCHOOL", "STREET", "YARD", "RIVER") and (loc - l).length > 0.15:
            print("WARN shot %d: %s blocks the lens (%.2f m in front of the camera)" % (n, ob.name, (loc - p).length))

    def finish(self, out):
        for a in self.actors:
            a.finalize(self.END)
        ANIM.flush()
        sc = bpy.context.scene
        for n, (a, b) in self.T.items():
            sc.timeline_markers.new("S%03d" % n, frame=int(round(F(a))))
        if self.cam:
            for m in sc.timeline_markers:
                m.camera = self.cam.ob
        sc.frame_set(1)
        bpy.ops.wm.save_as_mainfile(filepath=out)
        print("saved", out)


# ---------------------------------------------------------------------------------------- scene setup
def new_film(end_t, exposure=0.0):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.fps = FPS
    sc.frame_start, sc.frame_end = 1, int(round(end_t * FPS))
    sc.render.resolution_x, sc.render.resolution_y = RES
    sc.render.engine = "BLENDER_EEVEE"
    sc.eevee.taa_render_samples = 16
    try:
        sc.eevee.use_shadows = True
    except Exception:
        pass
    try:
        sc.view_settings.view_transform = "AgX"
        sc.view_settings.look = "AgX - Punchy"
    except TypeError:
        pass
    sc.view_settings.exposure = exposure
    for k, v in (("volumetric_end", 600.0), ("volumetric_start", 0.1), ("volumetric_tile_size", "8"),
                 ("use_volumetric_shadows", True), ("shadow_ray_count", 1), ("shadow_step_count", 4)):
        try:
            setattr(sc.eevee, k, v)
        except Exception as e:
            print("eevee setting skipped", k, e)
    w = bpy.data.worlds.new("World")
    sc.world = w
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.05, 0.06, 0.08, 1)
    w.node_tree.nodes["Background"].inputs[1].default_value = 0.3
    return sc


def fog_box(name, center, size, density, color=(0.8, 0.85, 0.9), aniso=0.3):
    """volume scatter cube (haze, dust in light beams, river fog)."""
    me = box_mesh(name, size[0], size[1], size[2], False)
    ob = new_obj(name, me)
    ob.location = center
    m = bpy.data.materials.new(name + "_vol")
    nt = m.node_tree
    for n in list(nt.nodes):
        if n.type == "BSDF_PRINCIPLED":
            nt.nodes.remove(n)
    out = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")
    v = nt.nodes.new("ShaderNodeVolumePrincipled")
    v.inputs["Density"].default_value = density
    v.inputs["Color"].default_value = (*color, 1)
    v.inputs["Anisotropy"].default_value = aniso
    nt.links.new(v.outputs[0], out.inputs["Volume"])
    ob.data.materials.append(m)
    ob.visible_shadow = False
    return ob, v


def ramp(ob, path, idx, t0, t1, v0, v1):
    """smooth change of a property inside a shot (keys at t0 and t1; holds after)."""
    ANIM.put(ob, path, idx, F(t0), v0, "bez")
    ANIM.put(ob, path, idx, F(t1), v1, "const")


def talk(t0, t1, base=(0.0, 0.1), amt=0.32, rate=8.5, seed=0):
    """mood callable: mouth flaps through a spoken line (brow, smile kept at base)."""
    def f(t, u):
        if t < t0 or t > t1:
            return (base[0], base[1], 0.0)
        k = abs(math.sin(t * rate + seed)) * (0.6 + 0.4 * math.sin(t * 2.3 + seed * 1.7))
        return (base[0], base[1], max(0.0, amt * k))
    return f


def tear(actor, t0, dur=1.6, side=0.5, name="tear"):
    """a bright drop that runs down the cheek."""
    m = M((0.85, 0.9, 1.0), 0.02, emit=(0.8, 0.9, 1.0), strength=1.5)
    d = new_obj(name, sphere_mesh("tr", 0.0045 * actor.H / 1.6, 6, 4, (1, 1, 1.6)), m)
    r = actor.hr

    def fn(t):
        u = min(max((t - t0) / dur, 0), 1)
        j = actor.J(t)
        p = j["head_c"] + j["hf"] * r * 0.9 + (j["hf"].cross(j["hu"])) * -side * r * 0.42 + j["hu"] * r * (0.1 - 0.75 * u)
        return p, None
    bake_fn(d, t0, t0 + dur, fn, 2, rot=False)
    vis(d, [(t0, t0 + dur)])
    return d


def caustics(mat, t0, t1, strength=1.5, scale=6.0, color=(0.55, 0.75, 1.0), speed=0.35, name="Caus"):
    """water caustics on a material: an animated voronoi edge pattern added as emission between t0 and t1."""
    nt = mat.node_tree
    bs = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.name = name + "Map"
    vor = nt.nodes.new("ShaderNodeTexVoronoi")
    vor.feature = "DISTANCE_TO_EDGE"
    vor.inputs["Scale"].default_value = scale
    rmp = nt.nodes.new("ShaderNodeMapRange")
    rmp.inputs["From Min"].default_value = 0.0
    rmp.inputs["From Max"].default_value = 0.012
    rmp.inputs["To Min"].default_value = 1.0
    rmp.inputs["To Max"].default_value = 0.0
    mul = nt.nodes.new("ShaderNodeMath")
    mul.operation = "MULTIPLY"
    mul.name = name + "Gain"
    mul.inputs[1].default_value = 0.0
    nt.links.new(geo.outputs["Position"], mp.inputs["Vector"])
    nt.links.new(mp.outputs["Vector"], vor.inputs["Vector"])
    nt.links.new(vor.outputs["Distance"], rmp.inputs["Value"])
    nt.links.new(rmp.outputs["Result"], mul.inputs[0])
    nt.links.new(mul.outputs[0], bs.inputs["Emission Strength"])
    bs.inputs["Emission Color"].default_value = (*color, 1)
    path_g = 'nodes["%sGain"].inputs[1].default_value' % name
    ANIM.put(nt, path_g, 0, 1, 0.0, "const")
    ANIM.put(nt, path_g, 0, F(t0), strength, "const")
    ANIM.put(nt, path_g, 0, F(t1), 0.0, "const")
    path_l = 'nodes["%sMap"].inputs[1].default_value' % name
    for i, k in enumerate((1.0, 0.6, 0.8)):
        ANIM.put(nt, path_l, i, F(t0), 0.0, "lin")
        ANIM.put(nt, path_l, i, F(t1), speed * k * (t1 - t0), "lin")
