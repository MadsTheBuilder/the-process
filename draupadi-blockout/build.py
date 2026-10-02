# build.py - build one scene of the blockout:  ./blender.sh -P build.py -- <scene no> <abs out.blend>
import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import film

args = sys.argv[sys.argv.index("--") + 1:]
no = int(args[0])
out = args[1]
S = film.Ctx(no)
film.new_film(S.END)
mod = importlib.import_module("scenes.sc%02d" % no)
mod.build(S)
S.bake_actors()
S.bake_cameras()
S.finish(out)
