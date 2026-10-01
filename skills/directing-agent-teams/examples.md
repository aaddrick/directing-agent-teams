# Team shapes by project type

These are **shapes to adapt, not templates**. The Director designs each team from the work in front of it: split by ownership boundaries, size to the agent cap, and use the depth budget only where a lead really needs sub-workers. Every example keeps the fixed top (main session → Director), an independent QA function, a scarce-resource lock, and alignment gates before long-lead items.

---

## 1. AR room tour on a Gaussian splat (this skill's origin, 2026-09)
**Goal:** turn a splat room tour into a 70–80 s AR video: 3D-anchored callouts, a TV and window screen replacement, holograms, a spinning fan, lamps, a dollhouse view, music, and a LinkedIn cut.
**Scarce resource:** one 16 GB GPU, used for renders, segmentation and generative fill. `flock` on `.gpu.lock`; previews are ≤ 5 s at 540×675; full 1080×1350 renders only at M2 and M3.
**M0 interface:**
- `render_ar.py`, with `pre_render` hooks for splat edits and `post` hooks for overlays
- `annotations.json`, holding the 3D anchors and planes
- `timeline.json`, holding tour time, hold beats and effect windows
- an identity proof that with every effect off the render is bit-identical to the old tour

**Team (the actual run):**
| Lead | Owned | Workers did |
|---|---|---|
| Infra | renderer, plugin API, anchor tool | anchor survey from capture frames |
| Annotations | callouts, outlines, measurements | per-effect previews |
| Screens and holograms | TV, window, hologram boards, cards | plane fits, procedural imagery |
| Scene edits | fan, lamps, pop-out, dust (splat edits) | segmentation, splat selection |
| Transitions | scanner sweep, dollhouse, mini-map, generative fill | LaMa inpainting for unseen views |
| Edit and package | storyboard, timeline, music, audio, mux, LinkedIn cut | procedural music styles |
| QA | per-gate reviewers, a taste reviewer | drift (KLT px), occlusion scrubs, loudness |

**Alignment arrays that worked, or should have run earlier:**
- storyboard v1–v3
- 4, then 8 music styles as 11 s reels over the picture, picked by the user
- rerouted camera paths checked with `--report-only`
- top-down dollhouse stills before committing to the hold

**Cuttables:** dust, the pop-out, the dollhouse, the Gaussian-built hologram.
**Lessons:**
- Previews caught most failures, but two M2 full renders still failed on fixes that were only proven on slices.
- The user changed the flight path mid-run, and the storyboard version already in progress missed it.
- Only the user could hear the audio.

---

## 2. Blender scene via Python (e.g. a product animation or architectural walkthrough)
**Goal:** build a 30–60 s shot sequence built entirely from `bpy` scripts, run headless with `blender -b -P build.py`, so the .blend is a **build artifact**, never hand-edited.
**Scarce resources:** the GPU for Cycles, a lock like the one above, and RAM for large scenes.
- **Preview tiers:** Workbench or clay renders → Eevee → Cycles at 16 spp and half resolution, denoised → final.
- **Full renders:** only at gates, rendered as frame ranges in the background, and resumable (skip frames that already exist).
- **Iterate on stills and short clips** (5 s or less) by default. The full-length render waits until the user has approved the stills and clips.

**M0 interface:**
- `scene_manifest.json`, listing collections, asset IDs, transforms, materials and cameras by name
- `build.py`, which assembles the scene from per-owner modules: `assets/<name>.py`, `materials.py`, `lighting.py`, `cameras.py`, `anim.py`
- a determinism proof: two builds with the same seed produce identical scene hashes (object, vertex and material counts, transforms)

**Team:**
| Lead | Owns | Sub-workers (depth 4 lets this lead split further) |
|---|---|---|
| Assets | `assets/*.py`, the procedural geometry library | one worker per hero asset; sub-workers for variants such as LODs and damage states |
| Look dev | `materials.py`, textures, HDRIs (with licences recorded) | material-ball previews per asset |
| Lighting and camera | `lighting.py`, `cameras.py`, the shot list | light-rig variants, camera path variants |
| Animation | `anim.py`, drivers, the timing map | per-shot blocking |
| Render and compositing | render settings, the compositor graph, the frame queue, the encode | background frame-range jobs under the lock |
| QA | reviewers | see below |

**With a designed hero asset (a vehicle, character, creature or product):** split Assets in two (see `director.md` → ideation vs implementation).
| Lead | Owns | Sub-workers |
|---|---|---|
| Design | `design/brief.md`, `design/spec.json` (dimensions, joints, part envelopes), callout sheets, the engineering pass (loads, drives, manufacture, service access) | none; this lead only ideates |
| Implementer | `assets/<hero>/*.py`, built strictly from `spec.json` | one part modeller per region or component |

QA checks the build against `spec.json`, including joint positions, envelopes and height.

**Alignment arrays:**
- **Design gate first:** hero-asset options built from the user's reference (`align/reference/`). Show them in Eevee or Cycles with neutral materials in the chosen set, next to a human and a vehicle for scale. Flat Workbench is enough only when the question is purely the silhouette.
- a 6-frame storyboard per shot as Workbench stills
- 4 lighting moods on the hero frame at Eevee
- 3 camera paths as low-resolution playblasts
- a material sheet with every asset under neutral light

The user or the Director picks each one before any Cycles time is spent.
**QA checks:**
- scene hash and naming conventions
- polycount and texture memory against budget
- no missing textures (a pink-material scan)
- no flipped normals or z-fighting (check render passes)
- continuity of the frame range
- flicker between frames (fireflies, noise shimmer)
- the final frame matches the aligned preview
- licences for any downloaded asset or HDRI

**Cuttables:** secondary animation, volumetrics, a second camera angle.
**Pitfalls:**
- Two leads writing the same collection. The manifest names one owner per collection.
- GUI-only features that `bpy` can't reach headless. Test them at M0.
- Procedural modelling drifts toward primitive boxes. Curved or organic forms need an explicit technique (subdivision cages, lofts), proven on a test piece.
- A rig checked in its rest pose hides clashes. Sweep every joint through its full range on the built mesh.
- Worked case: `implementations/blender-mech-advert.md`.
- A Cycles render or fluid bake in the foreground can trip the stall timeout, and it blocks messages. Always run them in the background and poll.
- Simulations (fluid, cloth, smoke) don't scale predictably from low-resolution previews. Their alignment array is a short pilot at production resolution, with a separate `.sim.lock` (CPU and RAM) taken before `.gpu.lock`.

---

## 3. Serious music composition (e.g. a 3–5 minute cue or piece with stems)
**Goal:** a composed, arranged and mixed piece, delivered as stems plus a master, with a score (MusicXML or MIDI) as the source of truth. It's rendered with synths or soundfonts in code (numpy/scipy, fluidsynth, sfizz), and every sample library's licence is recorded.
**Scarce resources:** CPU for offline renders (use a lock for full-length bounces), and **the user's ears**. No agent can hear, so taste is always verified by the user and listed as unverified until then.
**M0 interface:**
- `score/` (MusicXML or MIDI per part)
- `form.json`, with sections, bar ranges, a tempo map, key and meter changes, and hit points if it's scored to picture
- `render.py`, which turns parts into stems with fixed seeds
- `mix.json`, with levels, sends and buses
- an identity proof: the same score gives the same stems, bit for bit

**Team:**
| Lead | Owns | Workers |
|---|---|---|
| Composition | themes, harmony, form (`form.json`, melody and harmony parts) | motif variants, reharmonizations |
| Orchestration and arrangement | voicings, instrument ranges, part writing per section | per-section orchestration, counter-lines |
| Sound design | synth patches and instruments (`instruments/`), textures, one-shots | patch sketches per instrument role |
| Mix and master | `mix.json`, buses, loudness, the master chain, stem export | reference-matching passes |
| QA | theory, technical and taste reviewers | see below |

**Alignment arrays**, played to the user as short MP3s, one contact page per round:
1. **Direction:** 4–6 contrasting 16–30 s sketches. Vary genre, palette, tempo and key.
2. **Themes:** 3–4 motif and harmony variants of the chosen direction.
3. **Form map:** 2–3 section structures, as a timeline image plus a rough bounce.
4. **Orchestration:** 2–3 palettes on the same 30 s excerpt.
5. **Mix:** 2 balances before the final master.

Each round is cheap, and it prevents a full-length arrangement being built on an unapproved theme.
**QA checks:**
- theory lints: parallel fifths and octaves where style forbids them, voice crossing, unresolved tendency tones
- every part stays within its instrument's range and is playable, if it will ever be performed live
- the tempo map matches the hit points
- clipping, true peak and LUFS targets per delivery
- no audible loop seams or clicks (a transient scan)
- spectral balance: no holes, no build-up in the mud range
- the stems sum to the master
- **taste is unverified until the user listens**, so the report says so

**Cuttables:** alternate mixes, a live-performable score, extra stems.
**Pitfalls:**
- "Fuller" requests mean arrangement density (more layers, low-mids, counter-lines), not level. Level fights the sound effects and the limiter.
- Mix decisions made before the arrangement is locked get redone.
- Theory lints are style-dependent, so declare the style rules at M0.

---

## 4. Research (e.g. a landscape review, technical due diligence, a literature survey)
**Goal:** a sourced report answering a question, with every claim traceable to a fetched source.
**Scarce resources:** web fetch budget and rate limits (log fetches in the resource log), and the reader's attention (the report length budget).
**M0 interface:**
- `questions.md`, the question broken into 4–8 sub-questions, each with a scope and exclusions
- `ledger.jsonl`, one row per claim: claim, source URL, date, exact quote, confidence, sub-question, the agent that added it
- `sources.jsonl`, with the URL, title, date and type (official, community or paper), deduplicated
- the report outline

**Team:**
| Lead | Owns | Workers |
|---|---|---|
| One lead per sub-question cluster, 2–4 of them | its sub-questions' ledger rows | search and read workers, **one source or one query set each**. Each returns ledger rows and never prose, which keeps contexts small |
| Synthesis | the report and the outline; reads only the ledger, never raw pages | section drafters |
| QA | citation checkers, a red team | see below |

**Alignment arrays:**
- 3 scope framings of the question, e.g. narrow and deep versus broad survey
- 2–3 report outlines
- a key-source shortlist, the top 10 with one line each, before any deep reading

The user or the Director picks. Later, a draft executive summary goes out for review before the full write-up.
**QA checks:**
- **citation verification:** a fresh agent re-fetches each cited URL and confirms the quote exists and supports the claim. Any failure is a FAIL on that claim.
- **recency:** dates are within the declared window, and anything superseded is flagged
- **contradiction search:** a red-team worker looks for sources that disagree with each key claim
- **coverage matrix:** every sub-question is answered, or marked open
- **no orphan claims** in the report, meaning claims with no ledger row
- **official versus community labelling**
- **unverifiable items** listed under "not found" instead of guessed

**Cuttables:** lower-priority sub-questions, appendices, comparison tables.
**Pitfalls:**
- Workers summarizing into prose and losing their citations. The ledger rows are the only output.
- Duplicate searches across leads. Check `sources.jsonl` first.
- The synthesis lead reading raw pages and blowing its scope.
- Treating a changelog or doc snapshot as current. Record the fetch date.
