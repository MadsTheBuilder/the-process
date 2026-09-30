import os, re, subprocess, json, sys
import nvidia.cublas, nvidia.cudnn
for p in (nvidia.cublas.__path__[0], nvidia.cudnn.__path__[0]):
    os.add_dll_directory(os.path.join(p, "bin")); os.environ["PATH"] = os.path.join(p, "bin") + os.pathsep + os.environ["PATH"]
from faster_whisper import WhisperModel
import numpy as np, wave
w = wave.open("p1.wav"); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768; sr = 16000
log = subprocess.run(["ffmpeg","-i","p1.wav","-af","silencedetect=noise=-32dB:d=0.22","-f","null","-"], capture_output=True, text=True).stderr
st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]; en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
cuts = [(s+e)/2 for s, e in zip(st, en)]
bounds = [0.0] + cuts + [len(a)/sr]
m = WhisperModel("large-v3", device="cuda", compute_type="float16")
out = []
for s, e in zip(bounds, bounds[1:]):
    segs, _ = m.transcribe(a[int(s*sr):int(e*sr)], language="hi", beam_size=5, condition_on_previous_text=False, vad_filter=False)
    t = "".join(x.text for x in segs).strip()
    out.append({"s": round(s,2), "e": round(e,2), "t": t}); print(f"{s:6.2f}-{e:6.2f} {t}", flush=True)
json.dump(out, open("p1_chunks.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
