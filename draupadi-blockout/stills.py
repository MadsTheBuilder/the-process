# usage: ./blender.sh scene.blend -P stills.py -- outdir pct t1 t2 ...   (seconds)
import bpy, sys, os
a = sys.argv[sys.argv.index("--") + 1:]
out, pct, ts = a[0], int(a[1]), [float(x) for x in a[2:]]
os.makedirs(out, exist_ok=True)
s = bpy.context.scene
s.render.resolution_percentage = pct
s.eevee.taa_render_samples = 8
for t in ts:
    s.frame_set(int(round(1 + t * 24)))
    s.render.filepath = os.path.join(out, "t%07.2f.png" % t)
    bpy.ops.render.render(write_still=True)
