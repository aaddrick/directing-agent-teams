# Why it works this way

Most rules in the skill exist because something went wrong in a real run without them. This page pairs each rule with the incident behind it. Most come from the Blender mech run (see its [case study](../../skills/directing-agent-teams/implementations/blender-mech-advert.md)) and the game refine run ([case study](../../skills/directing-agent-teams/implementations/game-refine-run.md)); the rest come from the AR video run in [`examples.md`](../../skills/directing-agent-teams/examples.md) and from the agents' Lessons.

## Launch and design

| Rule | Incident it answers |
| --- | --- |
| A reference image is required for designed or visual work | The mech run launched without one ([the sheets](run-lifecycle.md#from-the-mech-run)). Five rounds of design sheets were rejected before the concept stuck, and each reference you supplied moved the design further than any sheet had |
| Split identity from features before the shape gate | Backwards knees, the sword and the gun were locked in as must-haves, and constrained the shape work until you freed them |
| Render a gate at the fidelity its question needs | Flat Workbench blockouts were judged as the design: "looks out of the 50's or 90's" |
| After two rejected sheets, ask for a reference | More variants on a brief that has already been rejected cost about an hour each and moved nothing |
| Repeated drift needs a named technique, a test piece and a measurable gate | "Rounded, cast" came back as boxes three or four times, and stopped only when the modellers had to name the technique and pass a test piece and an automatic shape gate |
| The approved pick becomes an automatic check | The build drifted from the approved concept (the pauldrons in v7.1), and nobody caught it until the Director compared renders by eye |
| Run weapon and reach checks at the design stage | "The gun is in his chest" only showed up once rifle, arm and chest were integrated and animated. A solver sweep later proved the two-handed grip couldn't clear the chest at all |

## Slices and verification

| Rule | Incident it answers |
| --- | --- |
| Slices, not whole-system rounds | Each spec revision rebuilt the whole machine, took one to three hours, and came back with hundreds of findings (245 rest-pose overlaps, 247 joint fits). Your feedback landed on work that was already stale |
| Verify on the built output, not the spec | Self-righting passed on the spec and failed on the built mesh: the knee guards sat 25–33 cm off the ground, and 5 of 9 poses tipped |
| A builder's claim is "unverified until QA" | A builder's "every frame within a few cm of the ground" reached you before QA had checked it, and had to be retracted |
| Sweep every joint through its full range | You spotted ram clipping by eye before any sweep existed. The sweep then showed every leg ram clipping, worst 0.48 m, at a pose QA hadn't swept |
| Put neighbouring requirements on the card | An aim re-solve ([D72-1](slices-and-qa.md#a-real-slice-d72-1)) cleared the chest but put every joint on its stops and swung the barrel 28° off the line of fire |
| Builders self-check with the verifier's tool | A builder reported pelvis drops of 0.30/0.43/0.49; the verifier measured 0.298/0.224/0.242 |
| Agree exception rules at M1 | The pass rule for designed nested parts was tightened at the final gate, and most of 247 joint fits failed right before the freeze |
| Compare part sizes with the last good build (`team-extent-verifier`) | A boolean hollow pass silently shrank 46 parts, turning a 5.1 m pauldron into a 1.65 m cylinder and a 0.71 m housing into a 0.08 m plate, and the only check was "manifold". Mirror checks missed it because both sides shrank |
| Measure penetration signed, never nearest-face | Nearest-face depth read a 3 cm finger-in-rib penetration as 0.8 cm |
| Every measured problem gets an owner the same hour | A finding sat unowned for about 90 minutes before the main session noticed |
| Say what got worse, not only what improved | Lowering exposure fixed a washed-out coat and hid the scale props |

## Coordination

| Rule | Incident it answers |
| --- | --- |
| Relay changes to the Director and every affected lead, with a confirmation | In the AR run, you changed the flight path mid-run, and a storyboard already in progress missed it |
| Write a verifier's Roster row before its builder needs it | Builders couldn't reach verifiers whose rows weren't written yet |
| Edit BOARD in place, under `.board.lock`, and only your own section | In the mech run, a concurrent write erased a status block, so the Director added the lock (D13). Sections were erased twice more despite it, until whole-file rewrites were banned (D26) |
| Timestamps come from `date` | Agents estimated times, and BOARD timestamps and ETAs were hours off |
| Never wrap a script in a lock it already takes | A double `flock` on `.gpu.lock` deadlocked the GPU for about 20 minutes, held by an agent that had already finished |
| Taste that only you can judge is listed as unverified | In the AR run, only you could hear the audio |

## Context and wind-down

| Rule | Incident it answers |
| --- | --- |
| Keep the handoff file current at every milestone, not only at handoff | The mech run's design lead died from a full context with a stale handoff |
| Rotate the Director at each major phase | A Director relaying 10–14 agents died of "prompt too long" after about six hours, with a handoff hours stale |
| The main session checks processes and locks itself after a wind-down | A parked lead's leftover 20-minute wait timer fired and resumed it after the wind-down was reported complete |
| Park, don't delete | The animation lead was parked through a handoff, so your reversal (cut, then reinstated) cost a respawn instead of a rebuild |
| A written wind-down procedure | Once it was written down, leads parked in about 15 minutes, with next steps in priority order |

## Cost and scope

From the game refine run: about 35 hours, 28 Directors and 315 agent IDs, most of it spent on coordination and re-testing rather than building.

| Rule | Incident it answers |
| --- | --- |
| Agree a budget and a stop line before launch | The run had neither. It began as an overnight run and took 35 hours |
| Ask user-only choices before launch, and build in the user's order | The first-named goal (engine sound) waited all day on the user's choice of voice, was gated last, and was the one goal that didn't ship |
| Verify by risk | Every row got the full adversarial gate; a one-constant change was priced at about 50 minutes of re-testing |
| Checks are committed scripts with planted failures | Verifiers rebuilt the same tools per slice; two were wrong, and their numbers reached decisions |
| Deciding rows freeze when building starts | One gate picked up five addenda mid-flight, each reopening finished rows; five gates landed "fail as written, pass by ruling" |
| Lanes ≤ scarce slots + 1 | Five lanes queued on two graphics slots and filled the Director's context hourly |
| Handoffs and Decisions are current state, about a page | Each new Director re-read a ~3,200-line handoff and a ~950-line rulings file; trimming them took Directors from ~60 to ~88 minutes |
| Don't rule on one reading | Several rulings and statements to the user rested on one number later corrected |
| A human check at each milestone | Nobody listened to the sound or held a gamepad; feel questions were measured for hours and still open at the end |
| Tests never use the user's live data | A test start cut into the log of a game the user was playing |
| Every background wait has a timeout | A log follower outlived its agent by 34 hours |
| The final check runs the docs as written, from a clean export | It found two faults every earlier gate had missed, because those gates set limits by hand |
| The Director reads status on a 15-minute pass; cards are files and prompts are short | A Director that answered every agent message itself stood at 440k after 85 minutes |
| Stalls are found from transcript mtimes, not pings | Dead or sleeping agents went unnoticed for 22, 63 and 90 minutes; a message to one was swallowed |
| Scarce runs start on a go-file | A "go" message to an idle verifier showed "Resuming" and produced nothing for 90 minutes |
| Hand-off marks come from the harness's count, near 300k | Agents read themselves about 70k low; a 150k mark made successors hand off before measuring anything |
| Every card names its base tree; frozen trees are diffed and intersected | Two fixes were built on a base one checkpoint old; rows were read on the tree before the last fix |
| High-risk gates run as blind cases → rows → verdict writer | Single verifiers doing all three reached 270k before their first capture |
| Tools print what they measured | A gap tool charged a neighbouring street light's collider to the stop sign, and the wrong cause reached the user |
| The Director adds no bars or definitions of its own | Two Director-added bars contradicted the user's own rows |
| Ask as fact + pick + cheap swap, at once | Asked that way, the main session answered seven times in an hour, in one to three minutes each |
| Shell traps in `rules.md` | 27 self-matching pollers, pattern-kills hitting another agent's runs four times, two agents dead inside compound `rm -rf` lines |
