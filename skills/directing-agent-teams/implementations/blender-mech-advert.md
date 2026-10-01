# Blender mech: design, rig and advert render (headless bpy)

**Project:** a large piloted mech, designed and modelled entirely from `bpy` scripts, with a rig (articulated fingers and toes, IK legs, weapon attach/detach), a self-righting ability, and a ~20 s 1080p30 Cycles showcase (walk-in, fire, stow, draw sword, slash, hero pose). One laptop GPU (RTX 5080, CUDA). The user was available for picks.

---

## Best execution

### Launch (main session): one round of about 5 questions
1. **Reference images (1–3).** For a mech, ask for the silhouette family (e.g. a game or anime unit), and save the images to `align/reference/`. Describe each one in words in the plan.
2. **Premise and tone, in the user's words:** who pilots it and how (in this run: a neural link, no windows), its role (a guardian or "mobile castle"), its era ("practical 2133"), and the presentation ("manufacturer advert: clean, new, functional"; matte powder coat, not plastic).
3. **Identity vs features:** the core is the silhouette, scale and role. Leg type, weapons and hand detail are settled after the shape gate.
4. **Delivery:** length, resolution, fps, codec; stills and ≤ 5 s clips first; whether the full render waits for the user.
5. **Cap and availability:** 10 agents suited this build.

### Team (cap 10)
- **Director**
- **DESIGN lead**, ideation only. It owns `design/brief.md`, `design/spec.json` (joints, ranges, part envelopes, mass, drives, contacts) and annotated callout sheets. It runs the plausibility pass per subsystem: loads at the real scale, what drives each joint, how it's manufactured, and service access.
- **MECH lead**, implementer, with part modellers per region: legs/feet, torso/core/back, arms/hands, weapons. It adds a **cast/curved-surface specialist** from the start.
- **LOOK lead:** coatings, sets and lighting, decals, and a fictional maker brand.
- **QA lead**, running alongside the build from M0.
- **ANIM lead,** once the shape is picked.
- **PIPE lead** (build, determinism, render and encode) at M0, then again at the render.
- **A contrarian** at each design gate.

### Gates
1. **M0:** the build skeleton, a GPU smoke test (check OptiX vs CUDA on the distro build) and a determinism proof. In parallel, **a design gate from the reference**: 3 options, rendered in Eevee or Cycles with neutral matte materials next to a human and a truck. Flat Workbench blockouts read as retro or toy-like, and cost this run several rejections.
2. **Design language gate** before any detailing: the plausibility review per subsystem, with callout sheets, and a whole-body envelope preview. The user approves the concept.
3. **Method proof:** one curved cast armour piece and one toe forging built with the curved-surface technique (subdivision cage + creases + solidify worked). Approve these before rolling the technique out.
4. **M1:** the model and rig. QA gates run **on the built mesh**:
   - full range-of-motion sweeps of every joint, with the minimum rod-to-structure clearance through the whole range;
   - the self-righting balance (CoM inside the real contact polygon) per key pose and per in-between pose;
   - an automatic shape check against the approved concept (outline overlap plus the flat-face fraction on cast parts);
   - rest-pose overlaps, with pass rules for designed nested parts agreed at M1.
5. **Look gate:** coats and set on the real hero frame.
6. **Storyboard and blocking playblast**, then **Cycles preview stills and a ≤ 5 s clip** for the user.
7. **The full render** after explicit user approval, AC and disk checks, in the background as resumable frame ranges under `.gpu.lock`.

### Design facts worth reusing
- **Scale:** at 15–20 m, human proportions look spindly. It needs thick load paths, a wide stance, big feet and a low centre of mass. Mass came out at about 500–550 t with zoned armour (heavy only in the frontal arc), versus ~670 t fully armoured.
- **Joint drives:** no ram linkage clears a ~125° knee or hip-pitch range. Use rotary drum drives there, and keep rams at the ankle, toes, hip roll, waist and wrist.
- **Self-righting:** it needs designed contact hardware (knee skid plates, hand heel pads, toe tip pads), stronger elbow and wrist drives, and solved in-between poses. Linear interpolation between key poses drives the fingertips through the floor.
- **Cast armour:** tank-turret-style doubly curved armour gives rounded mass without a consumer-product look. Pillowy single shells read as "Apple"; stacked chamfered boxes read as 1990s.
- **Finish:** matte powder coat or CARC-style coating over metal. Bare metal only on ram rods and bearing races; safety yellow only on service points.
- **Weapon ergonomics:** check early that the hand socket's orientation lets the gun be aimed upright (it was rolled 180° in this run), that the draw and stow targets are reachable, and that the trigger finger has a visible job.

---

## Lessons learned (run of 2026-09-29)

- **Launched without a reference.** Five design sheets were rejected (A–E, then V1–V4, H1–H3, S1–S4, then V6) before the concept stuck. Each user reference (a BattleTech chicken-walker, then Overwatch's Bastion) moved the design further than any sheet had.
- **Features were locked in as must-haves:** backwards knees, the sword and the gun. They constrained the shape work until the user freed them.
- **Flat Workbench gates read as dated.** The user judged the render style as the design ("looks out of the 50's or 90's").
- **The same drift came back 3–4 times.** "Rounded/cast" kept arriving as boxes, and it stopped only when the modellers had to name the technique, pass a test piece, and pass an automatic shape gate.
- **The build drifted from the approved concept** (the pauldrons in v7.1), and nobody caught it until the Director compared the renders by eye.
- **The self-righting passed on the spec but failed on the built mesh.** The knee guards sat 25–33 cm off the ground, so 5 of the 9 poses tipped. A builder's "every frame within a few cm of the ground" reached the user before QA had checked it and had to be retracted.
- **The user spotted ram clipping by eye** before any sweep existed. The sweep then showed every leg ram clipping, worst 0.48 m, at a pose QA hadn't swept.
- **The nested-part pass rule was tightened at the final gate.** Most of the 247 joint fits failed right before the freeze.
- **Context deaths:** the DESIGN lead died from a full context with a stale handoff. Leads that reviewed many renders turned over three generations in one day.
- **Clocks:** agents estimated times instead of running `date`, so the BOARD timestamps and ETAs were hours off.
- **What worked:**
  - relaying the user's exact words to the Director and every affected lead, with a one-line confirmation;
  - main-session observations labelled as such;
  - parking the animation lead through a handoff, which made the user's reversal (cut, then reinstated) cheap;
  - a time-boxed final round before the freeze;
  - the DESIGN/MECH split with parallel region modellers off one spec.

### Focus and wind-down (same run)
- **Rounds were too big.** Each spec revision (v7 → v7.1 → v7.2 → 7.2.12) rebuilt the whole machine, took one to three hours, and came back with QA findings in the hundreds (245 rest-pose overlaps, 247 joint fits). The user's feedback arrived at whole-machine scale and landed on work that was already stale. Slices would have fit this project well:
  - "left leg: ram clearance through the full range";
  - "one pauldron: cast technique test piece";
  - "get-up frame 03: CoM margin on the built mesh";
  - "rifle aim pose: no receiver/chest intersection".
- **Late integration exposed a cross-component bug.** "The gun is in his chest" was a weapon-ergonomics bug that only showed up once the rifle, arm and chest were integrated and animated. A small early slice would have caught it: aim the rifle two-handed on the rig and check clearance.
- **Wind-down went cleanly** once the procedure was written down. Leads parked in about 15 minutes, `handoff/director.md` listed the next steps in priority order, and `handoff/main.md` recorded the user's preferences. Afterwards, a parked lead's leftover 20-minute wait timer fired and resumed it. That was harmless, but it's why the main session checks for running processes and lock files itself, rather than trusting the reports.
- **Deliverables still arrived during the wind-down** (the tempo gate), and were carried into the handoff as a pending pick.

### D73 slice session (same project, 2026-09-29)
- `tools/render_frames.sh` takes `.gpu.lock` itself. Wrapping it in another `flock .gpu.lock` deadlocked the GPU for ~20 min, and the stuck job belonged to an agent that had already finished. The Director checks `ps` for leftover lock holders whenever a render stalls.
- "The gun is in his chest": two-handed aim with a 2.2 m fore-grip can't clear an 18.7 m machine's chest while aiming on line. It was proved by a solver sweep (4 regimes x 12 seeds), and the user picked one-handed fire braced on the stock. Run the weapon-ergonomics sweep at the design stage.
- D62's boolean hollow pass accepted a closed but wrong result (a 0.08 m plate for a 0.71 m housing). Mirror checks miss symmetric collapses, so compare extents against the last good build.

## Session 2 lessons (2026-09-29 evening: D73–D106, flat slices)
- **Flat builder/verifier slices (D74) moved many items at once:** 20–30 min cards, each with a paired verifier, and the user saw a result every few minutes. Leads and workers weren't needed.
- **Aim clearance:** a two-handed grip on a long fore-grip was geometrically infeasible (the hand wanted to sit 0.7 m above the grip). Four solver setups proved it before anyone changed the design. One-handed braced fire (D81) fixed it with pose only.
- **Motion at 18.7 m / 550 t:** the recoil went from 11 g "bounce" to one 0.44 m brace-down plus 0.11 m kicks at 0.7 g. Readability came from a closer, lower camera and secondary FX, not bigger motion. The weapon stow must be as slow as the rest (≥ 30 frames).
- **Slash:** wind-up to one back-most point on every axis, a late-peaking strike, follow-through ≥ 60° past vertical, and ≥ 0.5 m of hip weight transfer under 1 g. Trim dead tails.
- **The hollow-cut (boolean) pass silently shrank 46 parts** (a pauldron went from 5.1 m to a 1.65 m cylinder). Reject any cut that shrinks a part > 10%, and run an extent-regression check against the last good build on every build.
- **Grip checks:** nearest-face penetration under-reads, so use signed or parity measures. A pinned weapon plus open fingers clips through handovers, so choreograph the approach and a staggered close.
- **Scale props:** people must stand at or behind the mech's depth, never between the camera and the mech. A low (1.4 m), 20°-up, 20 mm hero camera made it loom.
- **Look:** a grey sweep reads as a studio. A ribbed hangar with a crane runway reads as a place. Wear must also exist at a scale that reads from the hero distance.
