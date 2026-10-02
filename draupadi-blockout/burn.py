# burn.py <scene no> <frames dir> <out.mp4> : grade + caption a rendered scene (system python3 + ffmpeg).
# Top-left: scene / shot / magnification / move / lens / angle. Bottom: the shot's verbatim audio line.
import json
import os
import subprocess
import sys
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
no, frames, out = int(sys.argv[1]), sys.argv[2], sys.argv[3]
sc = json.load(open(os.path.join(HERE, "shots.json"), encoding="utf8"))[no - 1]

# colour grades (the Notes/Lighting columns: present day cold + desaturated, memories warm, flashes coloured)
G = dict(
    cold="eq=saturation=0.70:contrast=1.07:gamma=0.97,colorbalance=rs=-0.03:gs=-0.005:bs=0.045:rm=-0.02:bm=0.03",
    grey="eq=saturation=0.60:contrast=1.04,colorbalance=rs=-0.02:bs=0.04:bm=0.02",
    green="eq=saturation=0.75:contrast=1.12,colorbalance=rs=-0.05:gs=0.05:bs=-0.01:rm=-0.04:gm=0.05",
    warm="eq=saturation=1.08:contrast=1.04,colorbalance=rs=0.05:bs=-0.05:rm=0.03:bm=-0.03",
    sheets="eq=saturation=1.0:brightness=0.03:contrast=0.98,colorbalance=rs=0.05:gs=0.02:bs=-0.06:rh=0.04:bh=-0.04",
    night="eq=saturation=0.80:contrast=1.08,colorbalance=rs=-0.04:bs=0.06:rm=-0.03:bm=0.05",
    river="eq=saturation=0.82:contrast=1.05,colorbalance=rs=-0.05:gs=-0.01:bs=0.07:rm=-0.04:bm=0.06",
    sunrise="eq=saturation=1.05:contrast=1.02,colorbalance=rs=0.06:gs=0.02:bs=-0.06:rm=0.04:bm=-0.04",
    tung="eq=saturation=1.02:contrast=1.10,colorbalance=rs=0.04:bs=-0.04:rm=0.02",
)
SCENE_GRADE = {1: "cold", 2: "cold", 3: "grey", 4: "warm", 5: "green", 6: "green", 7: "cold", 8: "cold", 9: "cold",
               10: "cold", 11: "grey", 12: "sheets", 13: "cold", 14: "cold", 15: "tung", 16: "cold", 17: "cold",
               18: "tung", 19: "cold", 20: "night", 21: "tung", 22: "night", 23: "night", 24: "night", 25: "night",
               26: "river", 27: "river", 28: "sunrise"}
SHOT_GRADE = {32: "grey", 33: "grey", 41: "cold", 42: "cold", 83: "cold", 84: "grey", 102: "cold", 103: "cold", 104: "cold",
              113: "night", 114: "night", 115: "night", 129: "night", 130: "night", 207: "sunrise"}

FONT = "C\\:/Windows/Fonts/arial.ttf"
td = os.path.join(HERE, "out", "captions%02d" % no)
os.makedirs(td, exist_ok=True)
filters, t = [], 0.0
grades = []
for s in sc["shots"]:
    a, b = t, t + s["dur"]
    t = b
    head = "SC %d  |  SHOT %d  |  %s  |  %s  |  %s  |  %s" % (no, s["no"], s["mag"], s["mov"],
                                                         s["lens"] if s["lens"] == "N/A" else s["lens"].replace(" Macro", "mm macro") + ("" if "Macro" in s["lens"] else "mm"),
                                                         s["angle"])
    audio = "\n".join(textwrap.wrap(s["audio"].replace("'", "\u2019"), 105)[:3])
    for key, txt, y, size in (("h", head, "10", 15), ("a", audio, "h-th-12", 17)):
        fn = os.path.join(td, "s%03d%s.txt" % (s["no"], key))
        open(fn, "w", encoding="utf8").write(txt)
        p = fn.replace("\\", "/").replace(":", "\\:")
        filters.append("drawtext=fontfile='%s':textfile='%s':x=12:y=%s:fontsize=%d:fontcolor=white@0.92:line_spacing=1:"
                       "box=1:boxcolor=black@0.5:boxborderw=5:enable='between(t,%.3f,%.3f)'" % (FONT, p, y, size, a, b - 0.001))
    g = G[SHOT_GRADE.get(s["no"], SCENE_GRADE[no])]
    if s["no"] == 212:
        g += ",fade=t=out:st=%.2f:d=1.4:color=white" % (s["dur"] - 1.4)
    if s["no"] == 213:
        g = "fade=t=in:st=0:d=1.2:color=white,fade=t=out:st=%.2f:d=0.8:color=white" % (s["dur"] - 0.8)
    grades.append((a, b, g))

# grade per shot: split the stream by shot, grade each, then concat (cuts are hard so no blending needed)
parts, labels = [], []
for i, (a, b, g) in enumerate(grades):
    parts.append("[0:v]trim=start=%.4f:end=%.4f,setpts=PTS-STARTPTS,%s[g%d]" % (a, b, g, i))
    labels.append("[g%d]" % i)
fc = ";".join(parts) + ";" + "".join(labels) + "concat=n=%d:v=1:a=0[gr];[gr]scale=960:402:flags=lanczos,%s[v]" % (len(grades), ",".join(filters))
env = dict(os.environ, FONTCONFIG_FILE=os.path.join(HERE, "fonts.conf"))
open(os.path.join(HERE, "fonts.conf"), "w").write('<?xml version="1.0"?><fontconfig><dir>C:/Windows/Fonts</dir></fontconfig>')
fcf = os.path.join(td, "filter.txt")
open(fcf, "w", encoding="utf8").write(fc)
cmd = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", "24", "-i", os.path.join(frames, "f_%04d.jpg"),
       "-filter_complex_script", fcf, "-map", "[v]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", out]
subprocess.run(cmd, check=True, env=env)
print("wrote", out)
