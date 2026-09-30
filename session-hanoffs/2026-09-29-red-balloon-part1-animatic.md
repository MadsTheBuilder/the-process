# Session handoff: Operation Red Balloon, Part 1 animatic storyboard

**Date:** 2026-09-29
**Project:** `C:\Users\madhu\Mads_builds\tarun-mirzapur\red-balloon-part1\` (HyperFrames 0.8.91)
**Status:** The opening of Part 1 is built and rendered, but **the full Part 1 script is not covered yet**. The final scene is missing: the parents search for Dhruv, reach the balloon vendor, and hear his account. It is not in the animated storyboard video. See the "Not done" section below.

---

## 1. What was asked for

- An animated storyboard (animatic) of Part 1 of the script, made in HyperFrames.
- Primitive blocks and stick figures only. **No generated images.**
- Every panel shows the camera, lighting, environment and characters.
- Each setup gets three angles: a wide overview of the full environment, a medium shot and a close shot.
- Pull references from the visual reference book and the reference image folder.
- Added later: a city-wide opening shot with an infinite zoom from `map.png` into `overhead view of meela.png`, landing exactly on shot 1A.

## 2. What is done

### Rendered outputs

| File | What it is |
|---|---|
| `red-balloon-part1/renders/red-balloon-part1-animatic-v2.mp4` | **Current version.** 23.5 s, 1920x1080, 25 fps, 10 shots (0A plus 1A–3C) |
| `red-balloon-part1/renders/red-balloon-part1-animatic.mp4` | v1. 20 s, 9 shots, without the 0A zoom. Kept for comparison |

### Shot list in v2 (all in `index.html`)

The script text each shot covers is on page 1 of the script. Timings are estimates made from the narration at about 3.3 words per second; no recorded voiceover exists yet.

| Shot | Angle | Time | Narration / sound | Content |
|---|---|---|---|---|
| 0A | Wide (city) | 0.0–3.5 | Sound effects only: mela ambience rising | Infinite zoom from `map.png` (Mela / Fair Ground marker) into the overhead mela plate, landing on 1A. Readout goes ×1 → ×40 |
| 1A | Wide | 3.5–6.5 | "Shaam ke 7 baj rahe the." | Rooftop view at 6 m, 24mm, slow push-in. "GHANTA 00 · 19:00" clock appears (added in post) |
| 1B | Medium | 6.5–8.8 | "Mirzapur ke mele mein chaaron taraf…" | Stall lane, 35mm, eye level 1.55 m, lateral drift. Foreground people cross the frame |
| 1C | Close | 8.8–10.5 | "…bas bheed hi bheed thi." | Balloon bundle above the heads, red balloon picked out, seller kept off-frame |
| 2A | Wide | 10.5–12.7 | "Isi bheed mein Gupta family bhi thi," | Family fixed in a moving crowd (book board 01A) |
| 2B | Medium | 12.7–14.3 | "jo bachchon ke saath mela ghoomne aayi thi." | Family of four walking to camera, 50mm, camera pulls back with them |
| 2C | Close | 14.3–16.0 | "Aur unhi bachchon mein tha 8 saal ka Dhruv." | Dhruv at 85mm, child eye level 1.05 m, tiny push-in |
| 3A | Medium | 16.0–19.3 | "Blue jacket pehne Dhruv … zid kar raha tha." | Dhruv tugs his father's sleeve and points at the balloons. Jalebi counter; father's head out of frame |
| 3B | Close | 19.3–21.1 | "Jab kisi ne uski baat nahi suni," | Dhruv's eye-line swings from his parents to the balloons. Adults at the frame edges, turned away |
| 3C | Wide | 21.1–23.5 | "to woh chupchaap balloon lene khud chala gaya." | Dhruv exits frame-right, a passer-by crosses, then the camera holds on the empty child-height space |

### What each frame contains

- **Panel (1216x684):** an SVG stick-figure scene with the environment (stalls, wiring, bulb strings, ferris wheel, clock tower), lighting arrows (3000K amber key, 6500K cool fill), rust focus rings and the camera move.
- **Panel overlays:** a label row with lens, height and move, and a top-down camera plan (field of view, subjects, key light).
- **Side card:** camera, lighting, environment, characters and a direction note, plus two reference thumbnails (one from the reference folder, one from the book).
- **Below the panel:** the narration line (Hinglish with an English translation) and a timeline strip with a playhead, grouped by sequence.

## 3. Files and sources

### Sources outside the project

| Source | Path | Used for |
|---|---|---|
| Script V11 | `C:\Users\madhu\Desktop\OPERATION RED BALLOON 11.pdf` | 27 pages. Part 1 (Mela) is on page 1 and the top of page 2 |
| Visual reference book | `C:\Users\madhu\Documents\Operation_Red_Balloon_Visual_Reference_Book.pdf` | 85 pages, listed below |
| Reference image folder | `C:\Users\madhu\Mads_builds\tarun-mirzapur\Rederence-images\` | Character, environment and scene references |

**Book pages to know:**

| Page | Contents |
|---|---|
| p.02 | Board legend: navy figure = subject, rust ring = focus target, amber arrow = key light |
| p.03 | World anchors: mela, gate, circus, balloon stall, chowki, road |
| p.05 | Character binding rules |
| p.08 | Scene 01 boards 01A–01D |
| p.09 | Scene 01 camera, light, colour and prompts |
| **p.10** | **Scene 02 boards 02A–02D (balloon stall, "Five answers, one witness")** |
| **p.11** | **Scene 02 recipe and prompts** |
| p.68–71 | Style, camera and light bible, plus the story clock |

**Reference folder contents:**

- `Enviorment/map.png`: district map, used for the 0A zoom.
- `Enviorment/overhead view of meela.png`: overhead mela view, used for the 0A zoom.
- The rooftop mela wide image (`ChatGPT Image Sep 29, 2026, 02_30_15 PM.png`) is **no longer in the folder**. Its thumbnail survives as `assets/refs/env_wide.jpg`.
- `character/Family/`: father, mother, son, daughter, close up of son, son asking for ballon, son wandring off, family discovery dhruvs mission, and d8485548 (family walking).
- `character/baloon vendor/`: baloon vendor, medium shot, face close up.
- `character/scene ref/`: family speaking with baloon vendor (1 and 2), family going to police station, family at police station.

### Project files (`red-balloon-part1/`)

| File | Purpose |
|---|---|
| `index.html` | The whole composition. Holds the SVG drawing helpers (`fig`, `bust`, `stall`, `bulbs`, `ferris`, `arrow`, `label`, `balloonBunch`, `crowd`), one `scenes.sXX()` function per shot, the `SHOTS` data array (all side-card text and references), the 0A zoom (`applyZoom`) and a single GSAP timeline |
| `BRIEF.md` | HyperFrames brief. Workflow `general-video`, `storyboard: yes`, length 23.5 s |
| `assets/refs/*.jpg` | 640 px thumbnails of the reference images, plus book crops: `board01A/B/C.jpg` (p.08), `book_mela.jpg` and `book_stall.jpg` (p.03), `book_cover.jpg` (p.01) |
| `assets/zoom/map.jpg`, `assets/zoom/overhead.jpg` | Full-resolution plates for the 0A zoom |
| `snapshots/` | Check stills. Throwaway |
| `hyperframes.json`, `package.json`, `meta.json`, `AGENTS.md`, `CLAUDE.md` | Created by `hyperframes init` |

## 4. How to work on it

Run these from inside `red-balloon-part1/`:

```bash
npx --yes hyperframes@0.8.91 check                                  # must be 0 errors (4 warnings are known and fine)
npx --yes hyperframes@0.8.91 snapshot --at 1.8,4.2 --no-end         # stills in snapshots/, plus contact-sheet.jpg
npx --yes hyperframes@0.8.91 render -o renders/<name>.mp4 --fps 25  # about 40 s
npx --yes hyperframes@0.8.91 preview --background                   # Studio at http://localhost:3002/#project/red-balloon-part1
npx --yes hyperframes@0.8.91 preview --stop                         # a preview may still be running from this session
```

**Adding a shot:**

1. Add a `<section id="sXX" class="clip shot" data-start data-duration data-track-index="1">`.
2. Add a `scenes.sXX` function.
3. Add a `SHOTS` entry. Its `start` must match `data-start`.
4. Add its tweens at absolute times.
5. Update the root and `#chrome` `data-duration`, the `00:23.5` total in the header timecode, the playhead and timecode tween durations, the `PX = 1824 / total` constant, and the sequence-bar ranges in the strip builder.

## 5. Gotchas found this session

- **Studio edits the file.** While a preview runs, Studio adds `data-hf-id` attributes to `index.html`. That is harmless.
- **Selector lint error.** `lint` rejects `querySelector` with a template literal. Use `getElementById(id).querySelector(".x")`.
- **`arrow()` argument order.** The signature is `(x1, y1, x2, y2, colour, markerId, text, opts)`. Leaving out the marker id produces NaN SVG and a runtime error.
- **Rust label contrast.** Rust text on the dark label chips fails contrast. `label()` already swaps it to `#ee7d60`.
- **Python for PDF work.** PyMuPDF (`fitz`) is installed in the system Python at `C:\Users\madhu\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\python.exe`. The `python` on the Bash PATH is a hermes venv without it.
- **PDF rendering.** The Read tool can't render PDFs because poppler isn't installed. Extract text or images with PyMuPDF instead.

## 6. Rules the user set (also saved in memory)

- **No image generation and no external services** (such as treg, or uploading files) unless the user asks. Propose the tool and its cost first. Paid runs stay under $1.
- **Incident this session:** 6 reference images were uploaded to public treg.to links without being asked. The links expire on 2026-10-06. The treg CLI was also self-updated and reinstalled; it is now version 0.22.0. Nothing was generated and nothing was spent.

## 7. Not done: the rest of Part 1 (next task)

The animatic stops at "…khud chala gaya." The rest of Part 1 has **not** been storyboarded, including the key scene where the parents search, reach the balloon vendor, and he tells them what he saw.

### Missing script (V11, page 1)

> Kareeb 10 minute baad gharwalon ko jab wo kahin nahi dikha,
> To unhe laga kisi jhoole ya dukaan ke paas ruk gaya hoga.
> Sab alag-alag taraf dhoondhne lage.
> Par Dhruv nahi mila.
> Dhoondhte-dhoondhte Dhruv ke maa-baap ek balloon bechne wale ke paas pahunche.
> "Bhaiya, blue jacket pehne ek chhota bachcha yahan aaya tha kya?"
> Balloon wale ne turant kaha,
> "Haan. Abhi kuch der pehle aaya tha. Lekin balloon lene se pehle do aadmi uske paas aaye. Unhone use red balloon diya, white van mein bithaya... aur us gate se nikal gaye."
> Dhruv ke pita ke is ek sawal ke unhe 5 jawab mile.
> Aur jawab bhi aise the ki sun kar dono ke pasine chhoot gaye.

Part 1 then closes with a narrator bridge: from "Par ye dar sirf gupta family tak rukne wala nahi tha…" on page 1 through "…Police mein sabse powerful kaun hai." on page 2. The book stages this as a narrator set (board 02D). **Confirm with the user whether it is in scope.**

### What the book says for these beats

- **Board 01D, "The missing lower third" (p.08):** medium shot, 85mm, eye level 1.5 m, tiny push then hold. The mother searches past camera with the parents at opposite frame edges and an empty child-height gap in the centre. Mela music thins when she notices the gap.
- **Boards 02A–02C (p.10–11), balloon stall, about 19:15:**
  - **02A:** medium shot, 35mm, parents left and seller right, balloon bundle behind the seller.
  - **02B:** close-up, 85mm, on the seller's eyes: "certainty, not corroboration".
  - **02C:** close-up, 85mm, on the mother's eyes, father soft at the frame edge: "fear lands on the listener".
- **Scene 02 rules:**
  - Keep every kidnapping claim attached to the seller.
  - **Do not** stage his account as an objective flashback. No van or kidnappers on screen.
  - **Do not** light the seller as a villain. He shares the same warm stall bulb as the parents.
- **References to use:**
  - `scene ref/family speaking with baloon vendor.png` and `…vendor 2.png`
  - `Family/family discovery dhruvs mission.png` (for the search)
  - `baloon vendor/*.png` (all three)
  - Book p.03 balloon stall, already cropped as `assets/refs/book_stall.jpg`

### Suggested plan (keeping the wide / medium / close convention)

- **SEQ 4, The search (about 4 shots):**
  - **Wide:** family scattering in different directions across the lane.
  - **Medium:** board 01D, the parents at the frame edges with the empty child-height gap.
  - **Close:** mother's eyes searching.
  - **Optional:** a jhoola or stall they check.
- **SEQ 5, The witness (about 4 or 5 shots):**
  - **Wide:** parents arrive at the balloon stall (02A geography).
  - **Medium:** the father asks the question (02A).
  - **Close:** the seller answers (02B).
  - **Close:** the mother reacts (02C), then both parents: "5 jawab… pasine chhoot gaye".
- **Build:** add these as new sections after 3C, starting at 23.5 s, using the same helpers and `SHOTS` fields. Pace them to the narration as before. The seller's quoted line is long, about 6–7 s at speaking pace, so it may need to span the close-up and the reaction shot.
- **Finish:** re-render as `renders/red-balloon-part1-animatic-v3.mp4`.

---

## 8. Update (later on 2026-09-29): v3 covers all of Part 1

- **Current version:** `renders/red-balloon-part1-animatic-v3.mp4`. 1:42.3, 26 shots, the whole of Part 1 through "…Police mein sabse powerful kaun hai."
- **1C removed.** 1B now carries the whole line "…chaaron taraf bas bheed hi bheed thi." The 1C thumbnail is reused for 5D.
- **No length cap.** Every shot is paced to its narration at about 3 words per second. The squeezed Seq 1–3 shots were lengthened too (2B, 2C, 3A and others).
- **New sequences:**
  - SEQ 4, The search: 4A (board 01D), 4B, 4C, 4D.
  - SEQ 5, The witness: 5A–5G (boards 02A–02C, five answer cards, no van on screen).
  - SEQ 6, The ladder: 6A–6G, the narrator bridge (board 02D).
- **Timing now comes from the data.** Shot starts are computed from `dur` in `SHOTS`, and tweens are placed as `A.id + offset`. To retime a shot, change its `dur` in `SHOTS` and the matching `<section>` `data-start`/`data-duration`. The script throws if the two disagree.
- **New thumbnails in `assets/refs/`:** `board01D`, `board02A–D`, `fam_discovery`, `vendor_talk1/2`, `vendor_face`, `vendor_full`.
