# Game refinement: improving a playable game the user is still playing

**Project:** a refine run on an existing small driving game: a batch of user-named improvements (engine sound, reversing, wind acting on the vehicle, "more exciting for a young player"), landed as a versioned release. The game was being played by its end user during the run. A headless self-test, a rendered mode and real-time paced soaks; two graphics slots on one machine. Director on the most expensive model, every builder and verifier on Opus, the main session relaying and committing.

---

## Best execution

### Launch (main session)
1. **Goals in the user's order.** Write them in the plan in that order and build them in that order. The first-named goal is the one to protect.
2. **User-only choices now.** Anything only the user can choose (here: which engine voice) is asked before launch, with sample options, while the user is present.
3. **Budget and stop line.** A token budget and an end time ("overnight, stop by 08:00" or "stop after v0.2.0"). Track each agent's tokens on the Roster.
4. **Deciding rows.** Three to five rows per goal, written as what the player meets ("the engine is audible over the wind at full throttle in the in-cab view"). Frozen once building starts.
5. **Human check.** About 15 minutes of the player (or the user) at each milestone: listen to the sound, hold the gamepad, look at a real window. Feel and loudness questions go there, not into hours of measurement.

### Team
- **Director**, with a handoff of about a page and a current-state Decisions table. Rotates by context size or after about 90 minutes.
- **Two or three lanes**, not five: the graphics slots are the bottleneck, and extra lanes only queue on them.
- **Builders on Opus for the hard slices; verifiers by risk.** High-risk rows (flashing or other photosensitivity, crashes, save data, anything frightening) get two verifiers, planted failures and an unfixed-build control. Behaviour and feel get one verifier. Cosmetics and text get the self-test. Run-and-tabulate verifiers and verdict writers can try a cheaper model on one checkpoint first.

### Checks as permanent repo tests (M0)
Write these once, as scripts with pass/fail exits and a planted failing case each, before any verifier needs them:
- flash counter (frames over a luminance-change threshold per second)
- peak and loudness meter on the mixed output, including every fixed gain in the chain
- collider probe, with rays that can't hit neighbouring props
- repeat-drive comparison, on contact-free drives only, or with a tolerance

### Gates
1. **M0:** the scripts above and their planted failures; a separate play copy and a "someone is playing" watcher; tests on their own data folder.
2. **Per goal:** gate a subsystem once, when its levels are right. Re-gate only the rows a change can touch.
3. **Final:** one paced soak, then a clean export running the README's commands exactly as written.

### Order
Sound first (the first-named goal, and the one with a user-only choice), then the rest in the user's order. Defects found along the way go to the backlog unless they're high risk.

---

## Lessons learned (run of 2026-11-10 to 2026-11-11)

**Cost.** About 35 hours, 19 commits, each with its own freeze, test gate, landing and live check. 28 Directors and 315 agent IDs; 13,667 logged game runs (11,499 headless, 1,603 rendered). Directors used about 370k to 710k tokens each; verifiers 160k to 270k each, several per checkpoint. Most of the cost was coordination and re-testing, not building. Scope grew from four goals to nine areas. The run hit the Director model's usage limit once.

**What went wrong:**
- Verifiers rebuilt the flash counter, peak meter, collider probe and repeat-drive comparison as one-off tools. Twice a tool was wrong (a ray hit the neighbouring street light; a level reader left out a fixed gain) and the wrong number reached a decision.
- Every row got the same adversarial gate: a 1 cm flag-pole reading as much as the lightning flash. A one-constant change to the sound fix was priced at about 50 minutes of re-testing.
- The sound gate picked up five addenda, mostly from the main session's mid-flight rulings, and each reopened finished rows. Five gates landed as "fail as written, pass by ruling".
- Five lanes queued on two graphics slots. The handoff file grew to about 3,200 lines and the append-only rulings file to about 950–1,000; every new Director re-read both.
- The first-named goal (engine sound) was gated last and cut, after waiting all day on the user's choice of engine voice. Nobody listened to the sound, held a gamepad or saw a real window.
- Several rulings and statements to the user rested on one unchecked number that was later corrected (a vehicle "stopped on nothing", an output "1.6 dB hotter", a peak "at top volume").
- "Identical drive" rows failed on drives that touched something: contact doesn't repeat byte for byte across unrelated code changes.
- A publish step's test start cut into the log of a game the player was running; it now uses its own data folder.
- Agents died silently and left wait loops and log followers running, one for 34 hours.

**What worked:**
- Planted failures caught a wrong measuring tool, and showed which checks couldn't fail; those were reported as "not proven".
- The final check from a clean export, running the README as written, found two faults every earlier gate had missed (the self-test's default time limit, a missing argument). Earlier gates had set a wider limit by hand.
- The separate play copy and "someone is playing" watcher: the player played for over an hour during the run and nothing of theirs was touched.
- Reading the verdict's written lines before a commit, and looking at pictures at full size.
- One landing at a time, each with a live check, only on a written verdict line.
- Resuming a Director stopped by the usage limit instead of replacing it.
- A narrower Director brief late in the run (about 135 lines of rulings, only the agents the remaining work named, no periodic digests, rotation by context size or ~90 min): Directors lasted about 88 minutes instead of about 60, and the handoff went from about 3,400 lines to about 110.
- A late fix allowed only if it was one line, with a lean re-check planned; it wasn't one line, so it went to the backlog instead of slipping the freeze.

The savings above are estimates from this one run.
