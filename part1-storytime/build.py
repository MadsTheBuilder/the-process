# Builds index.html for the Part 1 storytime edit from the VO timing below.
# Re-run after changing any timing: python build.py
import json

# --- recorded VO (rec seconds) -> output timeline -------------------------
# The recording skips the witness dialogue, so two silent "statement" inserts
# are spliced in: 4.0 s after rec 42.88 and 12.0 s after rec 45.87.
PRE = 3.5            # cold open (0A zoom) before the first word
INS_A, INS_B = 4.0, 12.0
CUT_A, CUT_B, REC_END = 42.88, 45.87, 91.6
TAIL = 3.0           # hold on the end card after the last word


def T(rec):
    if rec <= CUT_A: return round(rec + PRE, 2)
    if rec <= CUT_B: return round(rec + PRE + INS_A, 2)
    return round(rec + PRE + INS_A + INS_B, 2)


TOTAL = round(T(REC_END) + TAIL, 2)  # 114.1, matches broll/index.html

# phrase captions: (rec start, rec end, text) — *word* = highlighted
CAPS = [
    (0.00, 1.90, "Shaam ke *7 baj* rahe the"),
    (1.90, 3.46, "Mirzapur ke mele mein"),
    (3.46, 6.00, "chaaron taraf bas *bheed hi bheed* thi"),
    (6.00, 8.85, "Isi bheed mein *Gupta family* bhi thi"),
    (8.85, 11.76, "jo bachchon ke saath mela ghoomne aayi thi"),
    (11.76, 13.33, "Aur unhi bachchon mein tha"),
    (13.33, 15.16, "*8 saal ka Dhruv*"),
    (15.16, 17.23, "*Blue jacket* pehne Dhruv"),
    (17.23, 18.78, "pichhle aadhe ghante se"),
    (18.78, 20.82, "*balloon* lene ki zid kar raha tha"),
    (20.82, 23.10, "Jab kisi ne uski baat nahi suni"),
    (23.10, 26.23, "to woh chupchaap balloon lene *khud chala gaya*"),
    (26.23, 28.07, "Kareeb *10 minute* baad"),
    (28.07, 29.98, "gharwalon ko jab wo *kahin nahi dikha*"),
    (29.98, 30.90, "to unhe laga"),
    (30.90, 33.56, "kisi jhoole ya dukaan ke paas ruk gaya hoga"),
    (33.56, 36.15, "Sab alag-alag taraf dhoondhne lage"),
    (36.15, 37.63, "Par *Dhruv nahi mila*"),
    (37.63, 40.22, "Dhoondhte-dhoondhte Dhruv ke maa-baap"),
    (40.22, 42.88, "ek *balloon bechne wale* ke paas pahunche"),
    (42.88, 45.87, "Balloon wale ne *turant* kaha —"),
    (45.87, 48.30, "Dhruv ke pita ke is *ek sawal* ke"),
    (48.30, 50.68, "unhe *5 jawab* mile"),
    (50.68, 52.35, "Aur jawab bhi aise the"),
    (52.35, 54.68, "ki sun kar dono ke *pasine chhoot gaye*"),
    (54.68, 56.60, "Par ye dar sirf Gupta family tak"),
    (56.60, 58.34, "*rukne wala nahi tha*"),
    (58.34, 60.72, "Mela Chowki ke *Constable* se lekar"),
    (60.72, 62.84, "Lucknow mein baithe *DGP* tak"),
    (62.84, 64.13, "Dhruv ki talaash"),
    (64.13, 66.73, "Police system ke *har level* ko hilane wali thi"),
    (66.73, 69.88, "Isliye ye sirf *kidnapping ka case* nahi hai"),
    (69.88, 72.72, "Balki ye wo *seedhi* hai jispar chadh kar"),
    (72.72, 74.72, "hum ek-ek karke dekhenge"),
    (74.72, 76.59, "ki uniform pe lage *stars*"),
    (76.59, 78.53, "aur *badges* ka matlab kya hota hai?"),
    (78.53, 80.29, "Police ki alag-alag *ranks*"),
    (80.29, 82.03, "actually mein karti kya hain"),
    (82.03, 84.29, "*SHO, IO, CO*"),
    (84.29, 85.82, "ye ranks hain *ya kuch aur?*"),
    (85.82, 88.99, "Aur ant mein hum is *ek sawal* ka jawab dhoondhenge"),
    (88.99, 91.60, "ki Police mein *sabse powerful kaun hai*"),
]

# witness statements shown during the silent inserts (output seconds)
STMT = [
    (T(CUT_A), INS_A, "DHRUV KE PITA", "Bhaiya, blue jacket pehne ek chhota bachcha yahan aaya tha kya?"),
    (T(CUT_B), 3.0, "BALLOON WALA", "Haan. Abhi kuch der pehle aaya tha."),
    (T(CUT_B) + 3.0, 3.6, "BALLOON WALA", "Lekin balloon lene se pehle do aadmi uske paas aaye."),
    (T(CUT_B) + 6.6, 5.4, "BALLOON WALA", "Unhone use red balloon diya, white van mein bithaya… aur us gate se nikal gaye."),
]

# picture windows (output seconds)
FACE = [(T(58.34), T(74.72)), (T(78.53), T(88.99))]          # host full-frame
BROLL = [(0, FACE[0][0]), (FACE[0][1], FACE[1][0]), (FACE[1][1], TOTAL)]
PIP = [(PRE, T(CUT_A)), (T(CUT_A) + INS_A, T(CUT_B)), (T(CUT_B) + INS_B, FACE[0][0]), (FACE[0][1], FACE[1][0]), (FACE[1][1], T(REC_END))]
VO = [(PRE, T(CUT_A), 0.0), (T(CUT_A) + INS_A, T(CUT_B), CUT_A), (T(CUT_B) + INS_B, T(REC_END), CUT_B)]
CHAPTERS = [(PRE, 29.73, "CASE 01 · MIRZAPUR MELA · 19:00"), (29.73, 41.13, "19:10 · THE SEARCH"),
            (41.13, 74.18, "19:15 · THE WITNESS"), (74.18, T(REC_END), "THE LADDER")]


def media_at(t):  # output second -> rec second (only valid inside VO windows)
    for a, b, m in VO:
        if a - 1e-6 <= t <= b + 1e-6: return round(m + t - a, 2)
    raise ValueError(t)


r2 = lambda x: f"{round(x, 2):g}"
clips = []

for i, (a, b) in enumerate(BROLL):
    clips.append(f'<video id="broll{i}" class="clip full" src="assets/broll-clean.mp4" data-start="{r2(a)}" data-duration="{r2(b - a)}" data-media-start="{r2(a)}" data-track-index="0" muted playsinline></video>')
for i, (a, b) in enumerate(FACE):
    clips.append(f'<div class="fcwrap" id="fcw{i}"><video id="face{i}" class="clip full" src="assets/facecam-part1.mp4" data-start="{r2(a)}" data-duration="{r2(b - a)}" data-media-start="{r2(media_at(a))}" data-track-index="1" muted playsinline></video></div>')
for i, (a, b) in enumerate(FACE):
    clips.append(f'<div id="lad{i}" class="clip ladder" data-start="{r2(a)}" data-duration="{r2(b - a)}" data-track-index="2"></div>')
for i, (a, b) in enumerate(PIP):
    clips.append(f'<div id="pipring{i}" class="clip pipring" data-start="{r2(a)}" data-duration="{r2(b - a)}" data-track-index="3"></div>')
clips.append('<div class="pip" id="pip">' + "".join(
    f'<video id="pipv{i}" class="clip" src="assets/facecam-part1.mp4" data-start="{r2(a)}" data-duration="{r2(b - a)}" data-media-start="{r2(media_at(a))}" data-track-index="4" data-layout-allow-overflow muted playsinline></video>'
    for i, (a, b) in enumerate(PIP)) + "</div>")
for i, (a, b, label) in enumerate(CHAPTERS):
    clips.append(f'<div id="ch{i}" class="clip chapter" data-start="{r2(a)}" data-duration="{r2(b - a)}" data-track-index="5"><i></i>{label}</div>')
for i, (a, d, who, line) in enumerate(STMT):
    chars = "".join(f"<span>{c}</span>" if c != " " else " " for c in f"“{line}”")
    clips.append(f'<div id="st{i}" class="clip stmt" data-start="{r2(a)}" data-duration="{r2(d)}" data-track-index="6"><div class="lb">WITNESS STATEMENT · 19:15 · {who}</div><div class="tx">{chars}</div></div>')
for i, (s, e, txt) in enumerate(CAPS):
    a, b = round(T(s + 0.001), 2), T(e)  # a phrase starting exactly on a cut lands after the insert
    parts = txt.split("*")
    html = "".join(f"<em>{p}</em>" if k % 2 else p for k, p in enumerate(parts))
    clips.append(f'<div id="cap{i}" class="clip cap" data-start="{r2(a)}" data-duration="{r2(b - a)}" data-track-index="7"><span>{html}</span></div>')
clips.append(f'<div id="title" class="clip title" data-start="0" data-duration="{r2(PRE)}" data-track-index="8"><div class="k">MIRZAPUR · UTTAR PRADESH</div><h1>OPERATION RED BALLOON</h1><div class="p">PART 1 <b>·</b> MELA</div></div>')

# --- audio ------------------------------------------------------------------
aud = []
for i, (a, b, m) in enumerate(VO):
    aud.append(f'<audio id="vo{i}" src="assets/vo.wav" data-start="{r2(a)}" data-duration="{r2(b - a)}" data-media-start="{r2(m)}" data-track-index="10" data-volume="1"></audio>')
ins = [(T(CUT_A), T(CUT_A) + INS_A), (T(CUT_B), T(CUT_B) + INS_B)]
pts = [{"t": 0, "v": 0.55}]
for a, b in ins + [(T(REC_END), TOTAL)]:
    pts += [{"t": round(a - 0.3, 2), "v": 0.55}, {"t": round(a + 0.4, 2), "v": 1.0}, {"t": round(b - 0.2, 2), "v": 1.0}, {"t": round(b + 0.3, 2), "v": 0.55}]
pts = [p for p in pts if p["t"] <= TOTAL - 1.2] + [{"t": round(TOTAL - 1.2, 2), "v": 1.0}, {"t": TOTAL, "v": 0}]
aud.append(f'<audio id="bed" src="assets/drone.wav" data-start="0" data-duration="{r2(TOTAL)}" data-track-index="11" data-volume="0.8" data-automation=\'{json.dumps({"version": 1, "lanes": [{"target": "volume", "points": pts}]})}\'></audio>')
SFX = [("impact-bass-1", 0.2, 0.9), ("whoosh-cinematic", 1.4, 0.55), ("whoosh-short", FACE[0][0] - 0.15, 0.6), ("whoosh-short", FACE[0][1] - 0.15, 0.6),
       ("whoosh-short", FACE[1][0] - 0.15, 0.6), ("whoosh-short", FACE[1][1] - 0.15, 0.6), ("impact-bass-2", T(90.9) - 0.05, 0.85),
       ("glitch-1", T(53.2), 0.25), ("impact-bass-1", T(49.1), 0.45), ("impact-bass-1", T(54.68), 0.4)]
SFX += [("typing", a + 0.1 + k * 1.5, 0.28) for a, d, _, _ in STMT for k in range(int((d - 0.8) // 1.5) + 1)]
SFX += [("click-soft", T(45.88) + 1.6 + k * 0.3, 0.5) for k in range(5)]
SFX_LEN = {"impact-bass-1": 2.1, "impact-bass-2": 2.59, "whoosh-cinematic": 5.54, "whoosh-short": 0.57, "glitch-1": 2.63, "typing": 1.5, "click-soft": 0.36}
lanes = []  # greedy lane packing so no two SFX overlap on one track
for i, (n, t, v) in enumerate(sorted(SFX, key=lambda x: x[1])):
    d = min(SFX_LEN[n], TOTAL - t)
    k = next((j for j, end in enumerate(lanes) if end <= t), len(lanes))
    if k == len(lanes): lanes.append(0)
    lanes[k] = t + d
    aud.append(f'<audio id="sfx{i}" src="assets/sfx/{n}.mp3" data-start="{r2(t)}" data-duration="{r2(d)}" data-track-index="{12 + k}" data-volume="{v}"></audio>')

cfg = dict(TOTAL=TOTAL, FACE=FACE, PIP=PIP, T_CONST=T(59.5), T_DGP=T(61.8), T_HILA=T(65.8), T_SEEDHI=T(71.0),
           T_TAGS=[T(82.05), T(82.75), T(83.45)], T_RANKQ=T(84.6), T_ANT=T(85.82))

html = open("template.html.tpl", encoding="utf-8").read()
html = html.replace("%%TOTAL%%", r2(TOTAL)).replace("%%CLIPS%%", "\n      ".join(clips + aud)).replace("%%CFG%%", json.dumps(cfg))
open("index.html", "w", encoding="utf-8").write(html)
print("total", TOTAL, "clips", len(clips), "audio", len(aud))
