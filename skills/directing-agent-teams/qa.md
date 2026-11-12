# QA guide (QA lead and reviewers)

Read `rules.md` first. QA is independent: you **find failures**, you don't confirm success, and you **never edit product code**.

## How QA runs
- **Fresh reviewers for each gate**, at most 2 at a time unless the plan says otherwise. Reviewers produce their own evidence rather than reading builders' logs.
- **Match the effort to the slice's risk tier** (`director.md` → "Verify by risk"): two verifiers and planted failures for `high`, one verifier for `normal`, none for `low`.
- **Run the committed checks first.** `qa/tools/` holds the project's pass/fail scripts. Run them, then spend your time on their failures and on the rows no script covers. A new check you write that will be needed again goes in as a script with its planted failing case (`director.md` → "Checks are scripts").
- **Evidence for every finding:** a path, timestamp or frame, plus a saved crop, log excerpt or measurement in `qa/`.
- **Verdicts:** PASS or FAIL per item, and every FAIL comes with a concrete repro. Send the owner a pointer (`FAIL, see qa/<file>`). If it doesn't land, follow the delivery rule in `rules.md`.
- **Rounds:** a FAIL goes back to the owning lead, and a fresh reviewer checks the fix. After **3 FAIL rounds** on one item, the Director decides whether to cut it or accept it with a known issue. That decision is recorded in `QA_REPORT.md`.
- **A fix to another owner's file** re-runs that owner's affected checks.

## What to check
- **Numbers where possible:** drift in px, diff outside the declared mask, loudness and true peak, timing against cues, budgets such as polycount or memory, citation re-fetches.
- **Regressions:** unchanged areas still match the old output or the M0 proof. Byte-identical comparisons only prove something on paths that repeat exactly across unrelated changes; where they don't (contact physics, threads, timing), use a stated tolerance.
- **No ruling on one reading.** A number that decides a verdict needs a second reading, or a planted control that shows the tool would have seen the failure. Say which you did.
- **Measure the built output,** not the spec or the builder's simplified model. A result from the spec alone is reported as spec-only.
- **The approved pick as a reference:** after each alignment pick, build an automatic comparison against it (outline overlap, key dimensions, golden files) and run it on every later build.
- **Declared exceptions:** agree with the Director at M1 how designed exceptions (nested parts, allowed overlaps) pass, and on what evidence.
- **Alignment match:** the full-scale result matches the chosen preview, within the declared tolerances for pilots. Drift is a FAIL.
- **Adversarial scrubs:** step frame by frame (or bar by bar, or claim by claim) through the hardest stretches, such as fast motion, occlusion boundaries, seams and transitions.
- **Technical specs:** format, duration, resolution, frame rate, codec, and file integrity (no dropped or duplicated frames).
- **Licences** for every downloaded asset or model.
- **Taste:** a separate reviewer acts as a skeptical audience. They rank the three best and three worst moments, flag clutter and drag, and suggest cuts. They recommend; the Director or the user decides.
- **Unverified:** anything no agent can verify, such as how audio sounds or how it looks on real devices, is **listed as unverified**, never passed silently, and goes on the milestone's human check row.
- **Checks that can't fail aren't passes.** If a planted failure doesn't trip a check, report the row as "not proven", not PASS.
- **The final check runs as the user would:** from a clean export, with the docs' commands exactly as written, no hand-set limits or extra arguments.
- **Validate measuring tools first.** A new or changed tool must catch a known deep failure before its PASSes count. Penetration is measured signed or by ray parity, never nearest-face depth, which caps at half a feature's thickness and silently under-reads. When a tool is found flawed, re-run every verdict that used it.
- **Test motion against scale physics,** not only the card: acceleration caps (e.g. ≲ 1 g for a building-sized machine), step timing for the scale (Froude), balance, and a physics checker (inverse dynamics) where one exists. Card numbers can pass while the motion is physically absurd.
- **"Never reverses" tests cover every axis** (height, reach, angle), not one scalar. A monotonic swing angle hid a 4.8 m height pump.
- **Known issues and visibility:** before a defect is accepted, ray-test whether the shot cameras see it. If a viewer can see it, it's fix-if-visible, not accepted.
- **Readability vs realism:** when correct motion reads too small, fix it with camera framing and secondary cues (shake, dust, reactions), not by breaking the physics.

## Output
`QA_REPORT.md` has a summary table (item, verdict, worst remaining issue, rounds) and links to evidence in `qa/`.
