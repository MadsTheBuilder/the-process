import os, glob
import nvidia.cublas, nvidia.cudnn
for p in (nvidia.cublas.__path__[0], nvidia.cudnn.__path__[0]):
    os.add_dll_directory(os.path.join(p, "bin")); os.environ["PATH"] = os.path.join(p, "bin") + os.pathsep + os.environ["PATH"]
import json, sys, torch
from faster_whisper import WhisperModel
import os; dev = os.environ.get("DEV","cuda")
print("device", dev, flush=True)
m = WhisperModel("large-v3", device=dev, compute_type="float16" if dev=="cuda" else "int8")
segs, info = m.transcribe(sys.argv[1], language="hi", word_timestamps=True, vad_filter=True, vad_parameters=dict(min_silence_duration_ms=250, max_speech_duration_s=8), condition_on_previous_text=False, beam_size=5)
out = []
for s in segs:
    out.append({"start": s.start, "end": s.end, "text": s.text, "words": [{"w": w.word, "s": w.start, "e": w.end} for w in s.words]})
    print(f"[{s.start:7.2f}-{s.end:7.2f}] {s.text}", flush=True)
json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
