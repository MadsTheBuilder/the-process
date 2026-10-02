# usage: blender.sh scene.blend -P stills.py -- outdir t1 t2 ...   (seconds)
import bpy, sys, os
a = sys.argv[sys.argv.index("--") + 1:]
out, ts = a[0], [float(x) for x in a[1:]]
os.makedirs(out, exist_ok=True)
s = bpy.context.scene
s.render.resolution_percentage = 50
s.eevee.taa_render_samples = 8
for t in ts:
    s.frame_set(int(round(1 + t * 24)))
    s.render.filepath = os.path.join(out, "t%06.2f.png" % t)
    bpy.ops.render.render(write_still=True)
