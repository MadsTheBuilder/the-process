"""Generate index.html from shots.json (+ captions below). Run: python build.py
Timing comes only from shots.json durations; drawings live in panels.js; engine in sketch.js."""
import json, re, html

N = 'NARRATOR (VO)'
CAPS = {
 1: [(N, "Shaam ke 7 baj rahe the.")],
 2: [(N, "Mirzapur ke mele mein chaaron taraf bas bheed hi bheed thi.")],
 3: [(N, "Isi bheed mein Gupta family bhi thi...")],
 4: [(N, "Aur unhi bachchon mein tha 8 saal ka Dhruv.")],
 5: [],
 6: [(N, "Blue jacket pehne Dhruv pichhle aadhe ghante se balloon lene ki zid kar raha tha.")],
 7: [(N, "Jab kisi ne uski baat nahi suni...")],
 8: [(N, "...to woh chupchaap balloon lene khud chala gaya.")],
 9: [(N, "Kareeb 10 minute baad gharwalon ko jab wo kahin nahi dikha...")],
 10: [(N, "To unhe laga kisi jhoole ya dukaan ke paas ruk gaya hoga. Sab alag-alag taraf dhoondhne lage.")],
 11: [(N, "Par Dhruv nahi mila."), ("PARENTS (CALLING OUT)", "Dhruv!")],
 12: [(N, "Dhoondhte-dhoondhte Dhruv ke maa-baap ek balloon bechne wale ke paas pahunche.")],
 13: [("FATHER", "Bhaiya, blue jacket pehne ek chhota bachcha yahan aaya tha kya?")],
 14: [("BALLOON SELLER", "Haan. Abhi kuch der pehle aaya tha. Lekin balloon lene se pehle do aadmi uske paas aaye...")],
 15: [("BALLOON SELLER (CONT., AS VO)", "...Unhone use red balloon diya, white van mein bithaya... aur us gate se nikal gaye.")],
 16: [(N, "Dhruv ke pita ke is ek sawal ke unhe 5 jawab mile. Aur jawab bhi aise the ki sun kar dono ke pasine chhoot gaye.")],
 17: [(N, "Par ye dar sirf Gupta family tak rukne wala nahi tha. Mela Chowki ke Constable se lekar Lucknow mein baithe DGP tak - Dhruv ki talaash Police system ke har level ko hilane wali thi.")],
 18: [(N, "Isliye hamare liye ye sirf kidnapping ka case nahi hai... SHO, IO, CO - ye ranks hain ya kuch aur?")],
 19: [(N, "Aur seedhi mein sabse upar pahunch kar hum is ek sawal ka jawab dhoondhenge, ki Police mein sabse powerful kaun hai.")],
 20: [(N, "Dhruv ke parents balloon wale ko lekar paas ki Mela Chowki pahunchte hai.")],
 21: [(N, "Aur bahar unhe milta hai Police system ka pehla common chehra - Constable Ravi.")],
 22: [("FATHER", "Sir, hamara beta nahi mil raha. Ye bhaiya keh rahe hain do log use van mein lekar chale gaye.")],
 23: [("CONSTABLE RAVI", "Photo WhatsApp kariye.")],
 24: [("SFX", "WhatsApp ping")],
 25: [("CONSTABLE RAVI (TO SELLER)", "Gaadi kaunsi thi? Colour kya tha? Kahan se nikal ke gayi?")],
 26: [("CONSTABLE RAVI (ON WIRELESS)", "Constable Ravi bol raha hoon, shayad ek 8 saal ka ladka kidnap hua hai... Sabko bacche ki Photo forward kar raha hoon.")],
 27: [(N, "Kuch hi seconds mein Dhruv ki photo aur gaadi ki details mele ke sare constables tak pahunch chuki thi.")],
 28: [(N, "Abhi tak case me koi senior officer shaamil nahi hua tha. Na FIR likhi gayi thi na investigation shuru hui thi. Par zameen par police harkat me a chuki thi.")],
 29: [(N, "Reason tha Golden Hours... Aur inhi golden hours mein sabse kaam ki rank SP ya DGP nahi, Constable hoti hai.")],
 30: [(N, "Isliye aaj hum sirf ranks ko dekhenge nahi... RESPONSE, DECISION, INVESTIGATION, COMMAND, REACH...")],
 31: [(N, "Ab isi basis pe Constable Ravi ka meter dekhiye.")],
 32: [(N, "Wireless message ke baad Constable Ravi seedha Chowki ke andar chala gaya. Kyunki response to shuru ho chuka tha. Ab zarurat thi use organise karne ki.")],
 33: [(N, "Poora mela ek hi chowki ke under ata tha. Aur us chowki par the Head Constable Mishra.")],
 34: [("HEAD CONSTABLE MISHRA (ON WIRELESS)", "Exit gate ki checking badhao... Aur Ravi, tum Parents aur witness ko Police Station lekar jao.")],
 35: [("MUSIC + AMBIENCE", "no dialogue")],
 36: [(N, "Ab dekhiye, Constable Ravi ka response ghatna pe hue reaction jaisa tha. Par wahin Head Constable ka response ek plan jaisa tha.")],
 37: [(N, "Aur ye unke Meter mein bhi dikhta hai.")],
 38: [(N, "Head Constable jante the ki sirf mele mein dhoondhna kaafi nahi tha... Taaki investigation sahi tareeke se agey badh paye.")],
 39: [(N, "Dhruv ke parents aur balloon wala Police Station pahunchte hain.")],
 40: [(N, "Jahan Duty desk par unhe milti hai Assistant Sub-Inspector Aditi.")],
 41: [("ASI ADITI", "Bachcha balloon lene aaya tha?"), ("BALLOON SELLER", "Haan madam."), ("ASI ADITI", "Phir?"), ("BALLOON SELLER", "Do aadmi aaye..."), ("ASI ADITI", "Zabardasti?"), ("BALLOON SELLER", "Nahi madam. Bachcha khud gaya...")],
 42: [("MOTHER", "Report abhi ho jayegi na?..."), ("ASI ADITI", "Ji, baccho ke case mein aisa nahi hota. FIR abhi register hogi.")],
 43: [(N, "ASI Aditi ne turant FIR register kar li. Lekin FIR to bas pehla step tha.")],
 44: [(N, "Iske baad ek bada decision hona tha - Witness ko detail mein kaun examine karega?... is case ka Investigating Officer kaun hoga?")],
 45: [("ASI ADITI (ON PHONE)", "Sir, child kidnapping ka case lag raha hai..."), ("INSPECTOR KHAN (VOICE ONLY)", "Sub-Inspector Pandey ko bulao. Wahi case investigate karenge...")],
 46: [(N, "Aditi ne yahan koi case solve nahi kiya. Usne bas Dhruv ko ek missing bacche se ek registered case me badal diya.")],
 47: [("FATHER", "Madam, Inspector sahab se baat kara dijiye."), ("ASI ADITI", "Sir se abhi baat hui hai... aapke bete ka case Pandey sir dekhenge.")],
 48: [(N, "Yahin ek chhota sa confusion clear kar lete hain... Aur post batati hai is waqt uske pass kya responsibility hai.")],
 49: [("BALLOON SELLER", "Madam, main yahin ruk jaata hoon. Bacche ka milna zaruri hai.")],
 50: [(N, "ASI Aditi ko bhi baat sahi lagi... Par ab is case ka asli test shuru hone wala tha.")],
}
shots = json.load(open('shots.json', encoding='utf8'))
dur = {s['no']: int(re.search(r'\d+', s['dur']).group()) for s in shots}
total = sum(dur.values()); t = 0; clips = []
for s in shots:
    n = s['no']; d = dur[n]; caps = CAPS.get(n, [])
    muted = n in (24, 35)
    lines = ''.join(f'<div class="ln{" mute" if muted else ""}" data-at="{round(i * d / len(caps), 2)}"><b>{html.escape(w)}</b><span>{html.escape(x)}</span></div>' for i, (w, x) in enumerate(caps))
    long = ' lg' if sum(len(x) for _, x in caps) > 150 else ''
    clips.append(f'''<div class="clip shot" id="s{n}" data-n="{n}" data-start="{t}" data-duration="{d}" data-track-index="0">
  <div class="win"><svg class="cam" viewBox="0 0 1800 840" width="1800" height="840"></svg></div>
  <div class="num">{n:02d}</div>
  <div class="cap{long}{" multi" if len(caps) > 1 else ""}">{lines}</div>
</div>''')
    t += d

page = f'''<!DOCTYPE html>
<html lang="en" data-resolution="landscape">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=1920, height=1080">
<title>Operation Red Balloon — Sketch Storyboard S1-4</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{margin:0;width:1920px;height:1080px;overflow:hidden;background:#F3EFE6}}
#root{{position:relative;width:100%;height:100%;overflow:hidden;background:#F3EFE6;color:#26231F;font-family:'Space Mono',monospace}}
.clip{{position:absolute;inset:0}}
.win{{position:absolute;left:60px;top:40px;width:1800px;height:840px;overflow:hidden}}
.cam{{position:absolute;left:0;top:0;width:1800px;height:840px;transform-origin:50% 50%}}
.shot .num{{position:absolute;left:1760px;top:842px;font:600 26px Oswald,sans-serif;color:#5E5A51}}
.cap{{position:absolute;left:60px;top:905px;width:1800px;height:150px;display:flex;flex-direction:column;justify-content:flex-start;gap:6px}}
.ln{{opacity:0;display:flex;flex-direction:column;gap:2px}}
.cap.multi .ln{{position:absolute;left:0;top:0;width:100%}}
.ln b{{font:600 24px Oswald,sans-serif;letter-spacing:.12em;color:#5E5A51}}
.ln span{{font:400 34px/1.25 'Space Mono',monospace;color:#26231F}}
.cap.lg .ln span{{font-size:28px;line-height:1.22}}
.cap.lg .ln b{{font-size:22px}}
.ln.mute span{{font-style:italic;color:#5E5A51}}
#frame{{position:absolute;inset:0}}
</style></head>
<body>
<div id="root" data-composition-id="rb-sketch" data-start="0" data-duration="{total}" data-width="1920" data-height="1080">
{chr(10).join(clips)}
<div class="clip" id="frame" data-start="0" data-duration="{total}" data-track-index="5" style="pointer-events:none">
  <svg width="1920" height="1080" viewBox="0 0 1920 1080" id="border"></svg>
</div>
</div>
<script src="sketch.js"></script>
<script src="panels.js"></script>
<script src="panels2.js"></script>
<script>
(function(){{
  const tl = gsap.timeline({{paused:true}});
  // uneven hand-drawn panel border (seeded)
  SK.begin(99); SK.rect(60,40,1800,840,{{w:6}}); SK.line(56,46,1864,42,{{w:2,o:.5,c:SK.PEN}}); SK.line(64,884,1856,880,{{w:2,o:.5,c:SK.PEN}});
  document.getElementById('border').innerHTML = SK.end().replace(/stroke-dasharray="1 2"/g,'');
  // keep drawings inside the panel window: clip the sheet to the panel rect
  document.querySelectorAll('.shot').forEach(el => {{
    const n = +el.dataset.n, def = PANELS[n], dur = +el.dataset.duration, t0 = +el.dataset.start, svg = el.querySelector('.cam');
    if (def) {{
      SK.begin(def.seed || n); def.draw(); svg.innerHTML = SK.end();
      const subsEls = [...svg.querySelectorAll(':scope > .sub')];
      const slots = def.subs || [0], map = def.show || slots.map((_, i) => i);
      const budgetFull = def.budget || Math.min(3.2, dur * .45);
      const shown = new Set();
      slots.forEach((st, i) => {{
        const sidx = map[i], sub = subsEls[sidx]; if (!sub) return;
        const end = i + 1 < slots.length ? slots[i + 1] : dur, sd = end - st, T = t0 + st;
        if (slots.length > 1) {{ tl.set(sub, {{opacity:1}}, T); subsEls.forEach((o, j) => {{ if (j !== sidx) tl.set(o, {{opacity:0}}, T); }}); }}
        if (shown.has(sidx)) return; shown.add(sidx);
        const gr = [...sub.querySelectorAll(':scope > .gr')], budget = Math.min(budgetFull, def.budget ? sd * .85 : sd * .5);
        gr.forEach((g, gi) => {{
          const gs = T + (gr.length > 1 ? gi * (budget * .8 / (gr.length - 1)) : 0), gd = Math.max(.3, budget * .35);
          const fills = g.querySelectorAll('.f'), ds = g.querySelectorAll('.d');
          if (fills.length) tl.fromTo(fills, {{opacity:0}}, {{opacity:1, duration:.25, ease:'none'}}, gs);
          if (ds.length) tl.fromTo(ds, {{strokeDashoffset:1}}, {{strokeDashoffset:0, duration:gd, ease:'none'}}, gs);
        }});
      }});
      const c = def.cam || [[1,0,0],[1,0,0]];
      tl.fromTo(svg, {{scale:c[0][0], x:c[0][1], y:c[0][2]}}, {{scale:c[1][0], x:c[1][1], y:c[1][2], duration:dur, ease:'none'}}, t0);
      if (def.anim) def.anim(tl, svg, t0, dur, (q) => svg.querySelectorAll(q));
    }}
    const lns = [...el.querySelectorAll('.ln')];
    lns.forEach((ln, i) => {{ tl.fromTo(ln, {{opacity:0}}, {{opacity:1, duration:.3}}, t0 + (+ln.dataset.at) + .2); if (lns.length > 1 && i + 1 < lns.length) tl.to(ln, {{opacity:0, duration:.2}}, t0 + (+lns[i + 1].dataset.at) + .1); }});
  }});
  window.__timelines = window.__timelines || {{}};
  window.__timelines['rb-sketch'] = tl;
}})();
</script>
</body></html>
'''
open('index.html', 'w', encoding='utf8').write(page)
print('index.html', total, 's', len(shots), 'shots')
