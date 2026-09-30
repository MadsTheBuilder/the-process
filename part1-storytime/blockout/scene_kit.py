# scene_kit.py — small helpers for timed Blender blockouts (Blender 5.1, run with `blender -b -P`).
# Import from a scene script that lives next to this file:
#   sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from scene_kit import *
import math

import bpy
from mathutils import Vector

# ---------------------------------------------------------------- timing / easing
FPS = 24


def frame(t, fps=None):
    """Seconds -> frame number (frame 1 = 0.0s)."""
    return 1 + t * (fps or FPS)


def ease(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * (3 - 2 * u)


def seg(t, t0, t1):
    """Eased 0..1 progress of t through [t0, t1]; clamps outside."""
    return ease((t - t0) / (t1 - t0))


def lerp(a, b, u):
    return a + (b - a) * u


def vlerp(a, b, u):
    return Vector(a).lerp(Vector(b), u)


def integrate(speed_fn, duration, dt=1 / 240):
    """speed(t) in m/s -> position(t) in m, by numeric integration."""
    xs = [0.0]
    for i in range(int(duration / dt) + 2):
        xs.append(xs[-1] + speed_fn(i * dt) * dt)
    return lambda t: xs[min(max(int(t / dt), 0), len(xs) - 1)]


# ---------------------------------------------------------------- camera geometry
def orbit(phi_deg, r, h):
    """Point on a circle round the subject. phi 0 = +X (nose), 90 = +Y (subject's left); anticlockwise from above."""
    p = math.radians(phi_deg)
    return Vector((r * math.cos(p), r * math.sin(p), h))


def heading(psi_deg, drop=0.0):
    """Unit-ish look direction in the XY plane (psi like orbit), tilted down by `drop`."""
    p = math.radians(psi_deg)
    return Vector((math.cos(p), math.sin(p), -drop))


def look_quat(pos, target, prev=None):
    """Camera quaternion looking from pos at target; sign-matched to prev so baked keys never flip."""
    q = (Vector(target) - Vector(pos)).to_track_quat("-Z", "Y")
    if prev is not None and q.dot(prev) < 0:
        q.negate()
    return q


def visible_width(distance, fov_long_deg, res_x, res_y):
    """Metres visible across the frame's width at `distance` with sensor_fit AUTO (fov on the long side)."""
    long_side, short_side = max(res_x, res_y), min(res_x, res_y)
    half = math.tan(math.radians(fov_long_deg) / 2)
    if res_x >= res_y:
        return 2 * distance * half
    return 2 * distance * half * short_side / long_side


# ---------------------------------------------------------------- scene building
def reset(res=(1080, 1920), fps=24, seconds=10.0, engine="BLENDER_EEVEE"):
    """Empty scene with resolution, fps and frame range set. Only safe with BLENDER_USER_RESOURCES isolated."""
    global FPS
    FPS = fps
    bpy.ops.wm.read_factory_settings(use_empty=True)
    s = bpy.context.scene
    s.render.fps = fps
    s.frame_start, s.frame_end = 1, int(seconds * fps)
    s.render.resolution_x, s.render.resolution_y = res
    s.render.engine = engine
    return s


def mat(name, rgb, rough=0.6, metal=0.0, emit=None, strength=0.0, alpha=1.0):
    m = bpy.data.materials.new(name)
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1)
        b.inputs["Emission Strength"].default_value = strength
    if alpha < 1:
        b.inputs["Alpha"].default_value = alpha
        m.surface_render_method = "BLENDED"
    return m


def bsdf_input(material, name):
    """A Principled BSDF socket, e.g. to keyframe 'Emission Strength' or 'Roughness'."""
    return material.node_tree.nodes["Principled BSDF"].inputs[name]


def collection(name):
    c = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(c)
    return c


def move_to(ob, coll):
    for c in list(ob.users_collection):
        c.objects.unlink(ob)
    coll.objects.link(ob)


def add_box(name, loc, size, material, parent=None, rot=(0, 0, 0), coll=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    ob = bpy.context.active_object
    ob.name, ob.scale = name, size
    bpy.ops.object.transform_apply(scale=True)
    ob.data.materials.append(material)
    if parent:
        parent_keep(ob, parent)
    if coll:
        move_to(ob, coll)
    return ob


def empty(name, loc=(0, 0, 0), parent=None, coll=None):
    ob = bpy.data.objects.new(name, None)
    (coll or bpy.context.scene.collection).objects.link(ob)
    ob.location = loc
    if parent:
        ob.parent = parent
    return ob


def parent_keep(ob, parent):
    """Parent without moving: ob keeps its world position. Updates the view layer first,
    otherwise a freshly moved parent's matrix_world is stale and children land in the wrong place."""
    bpy.context.view_layer.update()
    ob.parent = parent
    ob.matrix_parent_inverse = parent.matrix_world.inverted()


def join(objs, name):
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    objs[0].name = name
    return objs[0]


def light(name, kind, loc, energy=0.0, coll=None, **props):
    """kind: POINT / SPOT / AREA / SUN. Lights shine down their local -Z."""
    d = bpy.data.lights.new(name, kind)
    d.energy = energy
    for k, v in props.items():
        setattr(d, k, v)
    ob = bpy.data.objects.new(name, d)
    (coll or bpy.context.scene.collection).objects.link(ob)
    ob.location = loc
    return ob


def aim(ob, target):
    """Point a light or camera's -Z at another object (use an empty as a movable target)."""
    tr = ob.constraints.new("TRACK_TO")
    tr.target, tr.track_axis, tr.up_axis = target, "TRACK_NEGATIVE_Z", "UP_Y"
    return tr


def world(rgb=(0.78, 0.74, 0.66), strength=0.05):
    w = bpy.data.worlds.new("World")
    w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (*rgb, 1)
    bg.inputs["Strength"].default_value = strength
    bpy.context.scene.world = w
    return w, bg


def camera(name="Film_Cam", sensor_fit="AUTO"):
    """Scene camera, quaternion rotation (bake with look_quat). AUTO fit: FOV applies to the long side."""
    d = bpy.data.cameras.new(name)
    d.sensor_fit = sensor_fit
    ob = bpy.data.objects.new(name, d)
    bpy.context.scene.collection.objects.link(ob)
    bpy.context.scene.camera = ob
    ob.rotation_mode = "QUATERNION"
    return ob


# ---------------------------------------------------------------- keys
def key(owner, path, value, t):
    """Set owner.<path> = value and keyframe it at time t (seconds). Works on sockets via path 'default_value'."""
    setattr(owner, path, value)
    owner.keyframe_insert(path, frame=frame(t))


def fcurves(idb):
    """All F-curves on an ID (Blender 5 layered actions: layers -> strips -> channelbags)."""
    ad = getattr(idb, "animation_data", None)
    if not (ad and ad.action):
        return []
    if hasattr(ad.action, "fcurves"):
        return list(ad.action.fcurves)
    return [fc for layer in ad.action.layers for strip in layer.strips
            for bag in strip.channelbags for fc in bag.fcurves]


def set_interpolation(idbs, kind="CONSTANT"):
    """Keys from Python default to Bezier, which FADES light switches, hides and flickers.
    Call this on every ID whose keys are state switches. Pass material/world node_trees, light datas, objects.
    (preferences.edit.keyframe_new_interpolation_type does NOT apply to keyframe_insert from Python.)"""
    for idb in idbs:
        for fc in fcurves(idb):
            for k in fc.keyframe_points:
                k.interpolation = kind


def markers(pairs):
    """[(label, seconds), ...] -> timeline markers."""
    for label, t in pairs:
        bpy.context.scene.timeline_markers.new(label, frame=int(frame(t)))


def bake(fn):
    """Call fn(frame, t) for every frame in the scene range, with the frame set. fn sets values and keys them."""
    s = bpy.context.scene
    for f in range(s.frame_start, s.frame_end + 1):
        fn(f, (f - 1) / s.render.fps)


def save(path):
    bpy.context.scene.frame_set(1)
    bpy.ops.wm.save_as_mainfile(filepath=path)
