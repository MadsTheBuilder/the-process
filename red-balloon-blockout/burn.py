# burn.py <frames_dir> <out.mp4>  : encode frames + burn shot number / lens / VO caption (ffmpeg drawtext)
import json, os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
frames, out = sys.argv[1], sys.argv[2]
shots = json.load(open(os.path.join(here, "shots_scene1.json"), encoding="utf8"))
SH = {1: (0, 5), 2: (5, 9), 3: (9, 14), 4: (14, 17), 5: (17, 20), 6: (20, 25), 7: (25, 28), 8: (28, 32), 9: (32, 36), 10: (36, 41),
      11: (41, 45), 12: (45, 49), 13: (49, 52), 14: (52, 57), 15: (57, 62), 16: (62, 68), 17: (68, 77), 18: (77, 95), 19: (95, 102)}
td = os.path.join(here, "captions"); os.makedirs(td, exist_ok=True)
FONT = "C\:/Windows/Fonts/arial.ttf"
f = []
for s in shots:
    n = s["no"]; a, b = SH[n]
    head = "SHOT %02d  |  %s  |  %s  |  %smm  |  %s" % (n, s["mag"], s["mov"], s["lens"].replace(" Macro", ""), s["angle"])
    vo = s["audio"]
    for key, txt, y, size in (("h", head, "10", 20), ("v", vo, "h-th-14", 22)):
        fn = os.path.join(td, "s%02d%s.txt" % (n, key)); open(fn, "w", encoding="utf8").write(txt)
        p = fn.replace("\\", "/").replace(":", "\:")
        f.append("drawtext=fontfile='%s':textfile='%s':x=12:y=%s:fontsize=%d:fontcolor=white:box=1:boxcolor=black@0.55:boxborderw=6:enable='between(t,%s,%s)'" % (FONT, p, y, size, a, b - 0.001))
env = dict(os.environ, FONTCONFIG_FILE=os.path.join(here, "fonts.conf"))
open(os.path.join(here, "fonts.conf"), "w").write('<?xml version="1.0"?><fontconfig><dir>C:/Windows/Fonts</dir></fontconfig>')
cmd = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", "24", "-i", os.path.join(frames, "f_%04d.png"), "-vf", ",".join(f), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", out]
subprocess.run(cmd, check=True, env=env)
print("wrote", out)
