# Handoff: test the `/shot-breakdown` skill

**Date:** 2026-10-02. **Previous session cwd:** `C:\Users\madhu\Mads_builds\tarun-mirzapur`

## Goal for the next session
Run skill-creator's eval loop on the new global `shot-breakdown` skill: with-skill runs vs. baseline runs, grading, the eval viewer, user feedback, then iterate. After that, optionally tune the skill's description so it triggers reliably.

## What already exists (read these; this doc doesn't repeat them)
- **Approved plan:** `C:\Users\madhu\.claude\plans\pasted-content-id-aaa9-understand-how-curious-whale.md`. It records every design decision from the user Q&A (originally 9 fixed columns, **now 10 with Lighting**; xlsx output, a "read the script then ask" vision interview, the shot-code list, verbatim audio with English for everything else, principles only, global install).
- **Skill:** `C:\Users\madhu\.claude\skills\shot-breakdown\`
  - `SKILL.md`: a 6-step workflow (ingest, vision interview, Vision Brief, build JSON, render and validate, report)
  - `references/director-principles.md`, `references/vision-playbooks.md`, `references/shot-codes.md`, `references/lighting-design.md`
  - `scripts/build_xlsx.py`: turns JSON into a formatted xlsx and validates it. Run `--selftest` to test it.
- **Eval workspace:** `C:\Users\madhu\.claude\skills\shot-breakdown-workspace\evals\evals.json`. Eval 1 is Red Balloon as a dark documentary; eval 2 is Red Balloon as a 90s, 9:16, AI-generated (Seedance) reel. Eval 3 is the user's `Desktop\Test_script.pdf` (a short drama, 2.39:1, about 15 min).
- **Origin case study:** the old session transcript `~/.claude/projects/c--Users-madhu-Mads-builds-tarun-mirzapur/3903c08e-807d-4ae4-a66f-8b0164b1de4f.jsonl`. It produced the hand-made breakdown at `C:\Users\madhu\Desktop\Operation_Red_Balloon_Shot_Breakdown.csv` (161 shots, about 22 min), which is useful as a quality reference for eval 1.
- **Test script:** `C:\Users\madhu\Desktop\OPERATION RED BALLOON 11.pdf`

## Update 2026-10-02: lighting + a deeper interview added
- **10 columns:** `Shot no., Description, Magnification, Movment, Lens, Angle, Lighting, Notes, Audio, Duration`.
- **Lighting is designed per scene** (the user's rule): each scene has a `lighting` setup shown in its header row as `| LIGHT: ...`; each shot's Lighting cell adapts that setup to its framing (gaffer level). Scenes change their light with the emotion. The validator requires a scene setup and Lighting on every non-GFX shot.
- **Interview round 2:** the idea underneath, overall look + references, and narrowing questions on the visual feel of each key scene. These feed a **Lighting bible** (philosophy, arc of light, per-scene looks) in the Vision Brief.
- `shot-breakdown-workspace/manual-run-test-script/breakdown.json` predates the Lighting column, so treat it as a stale reference (it will fail the new validation).
- The lighting expectations are already appended to each eval's `expected_output` in `evals.json`.

## State and verified facts
- `build_xlsx.py --selftest` passes. A smoke test that converted the old Red Balloon CSV gave 13 scenes, 161 shots and 1319s, and correctly flagged the old free-form magnification codes (INSERT, TWO-SHOT, SPLIT SCREEN, etc.) as invalid.
- **Python gotcha:** in Bash and PowerShell, `python` resolves to a hermes venv that has no pip and no openpyxl. Use **`python3`** (WindowsApps Python 3.12), which has `openpyxl` and `python-docx` installed. SKILL.md already says to use `python3`.
- Nothing is committed. The skill lives outside the repo, in `~/.claude/skills`.

## Before launching
Confirm with the user that the 3 evals in `evals.json` are still the ones they want, and mention the token cost.

## Notes for running the evals
- Subagents can't answer AskUserQuestion, so every eval prompt includes the vision answers inline (see evals 1–2). With-skill runners should treat those answers as the interview result and skip asking.
- The runs are heavy: about 6 runs, each writing a breakdown of 100+ shots. Mention the token cost to the user before launching. Memory rule: no paid external generation and no unrequested external services. This eval loop is all local subagents, which is fine.
- Assertions to draft (programmatic where possible): xlsx exists; headers match the 9 fixed columns exactly (including "Movment"); `build_xlsx.py` validation is ok; runtime is within ±10% of the target (about 22 min for eval 1, 90s for eval 2); a sample of script VO lines appears verbatim in Audio; eval 2 has every shot ≤10s and mentions 9:16/vertical; Notes contain PLANT/PAYOFF/MOTIF cross-references; a Vision Brief appears in the transcript or report. The key qualitative check is that **evals 1 and 2 are clearly different** (the vision drives the breakdown).
- Launch the reviewer with skill-creator's `eval-viewer/generate_review.py`, not custom HTML.

## Suggested skills
- **`skill-creator:skill-creator`**: drives the whole eval, grade, viewer and iterate loop, plus description optimization (`scripts.run_loop`).
- **`shot-breakdown`**: the skill under test. Invoke it directly for a manual sanity run if needed.
- **`verify-before-complete`**: before claiming the skill passes.
