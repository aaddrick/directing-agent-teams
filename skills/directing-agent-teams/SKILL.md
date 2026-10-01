---
name: directing-agent-teams
description: Use when the user asks to "coordinate agents to coordinate agents", fan out a multi-workstream project to a team of subagents, run a Director/lead/worker hierarchy, or keep a large build going unattended (overnight, "don't do anything yourself") with adversarial QA and a scarce shared resource such as one GPU.
---

# Directing Agent Teams

## Overview
You (the main session) write the plan, launch **one Director** in the background, and from then on only **relay**: user decisions go down, results and pending choices go up. The Director designs the team from the work, runs gated milestones with independent adversarial QA, and reports.

**Core principle:** parallel agents fail at the seams: shared files, the shared resource, decisions that don't reach everyone, and self-certified work. Design those seams before anyone builds.

**Only the top two layers are fixed:** the main session (you) and the Director. Everything below is designed per project.

## Files: who reads what
Each agent reads only its own file, which keeps contexts small.

| File | Reader | Holds |
|---|---|---|
| `SKILL.md` | main session | this: launching, relaying, notifications |
| `director.md` | Director | team design, depth and cap, seams, alignment gates, gates, offline decisions, final report |
| `rules.md` | **every** lead, worker and reviewer | the ground rules: comms, locks, files, scope, handoff. Spawn prompts say "read rules.md" |
| `qa.md` | QA lead and reviewers | adversarial QA method and checks |
| `templates.md` | Director | skeletons for the plan, the BOARD, the handoff file and the Director prompt |
| `examples.md` | Director, while designing | team shapes: AR video, Blender via Python, music, research |
| `implementations/` | main session at launch, and the Director while designing, when a past project is similar | worked cases: how the project should have run, then the lessons learned. The Director writes new ones in the project; see `implementations/README.md` for where they live |
| `context-turnover.md` | whoever replaces an agent | replacement, silent death, edge cases |
| `runtime-facts.md`, `knobs.md` | anyone checking platform behaviour | tested facts, limits, env/settings knobs |

## Launch checklist (main session)
0. **Check for a similar past project** in this skill's `implementations/`, `~/.claude/directing-agent-teams/implementations/` and the project's `.claude/directing-agent-teams/implementations/`. If one exists, read its "Best execution" section, and use it to shape the questions and the plan.
1. **Write `PLAN_<project>.md`** from the `templates.md` skeleton: the goal, the deliverables, and what's fixed. Leave team design to the Director.
2. **Before launch, ask the user for** anything only they can supply (logos, brand colours, credentials, source data), delivery specs (formats, codecs, aspect handling), the agent cap (default 6; creative builds with parallel part modellers often want 8–10), and defaults for open questions.
   - **Designed or visual work (a character, product, vehicle, set, brand): a reference is required, not optional.** Get 1–3 reference images or links and save them to `align/reference/`. Also get the tone and era in the user's own words (e.g. "glossy advert", "gritty documentary", "near-future") and the premise (who uses it, and how). Without a reference, the design gate turns into rounds of guessing: each rejected sheet costs an hour, and one reference image moves the design further than any sheet.
   - **Ask one round of at most about 5 questions:** the reference, tone/era, identity vs features, delivery, and availability/cap. Propose defaults for everything else in the plan; don't ask about them.
   - **Split the requirements into identity and features.** Ask which items define the thing (e.g. its silhouette, role and scale) and which can wait until the core is picked (e.g. accessories, secondary parts, mechanisms). Features locked in as must-haves constrain the shape work before anyone knows the shape.
3. **Warn them before launch** that any permission prompt they haven't pre-approved will stall agents overnight.
4. **Create `BOARD.md`** from the skeleton in `templates.md`.
5. **Spawn the Director yourself**, with `run_in_background`, `subagent_type: "directing-agent-teams:team-director"` (or `team-director` if the project's `.claude/agents/` or `~/.claude/agents/` has its own copy) and the Director prompt from `templates.md`. Fill `<skill dir>` in that prompt with this skill's base directory, so every agent can find `rules.md` and `qa.md`. If an agent spawns the Director instead, every role loses a layer of depth.
   - **Agent definitions** ship with this plugin as `directing-agent-teams:<type>`: `team-director` (Opus), `team-builder`, `team-verifier` and `team-taste-reviewer` (Sonnet by default), the specialists `team-animator`, `team-extent-verifier`, `team-set-builder` and `team-surfacer`, plus the general `contrarian`. **The Director creates and updates local copies as the work needs** (director.md → "Agent definitions"): new `team-<role>` types, and dated one-line Lessons, in the project's `.claude/agents/`. If one reaches you, forward it to the Director rather than editing the file yourself, unless the user asks you to.
6. **Write the Director's row** (its agent ID) into `BOARD.md` → Roster immediately. Spawned agents have no `ListAgents`, so the Roster is the only directory.

## Relaying (your whole job after launch)
- **The user changes a requirement:** send their exact words to the **Director and directly to each affected lead**, by agent ID from the Roster. Ask the Director to confirm in one line that the change is applied. Work already in flight will predate it.
  - **Follow-ups get their own confirmation.** If the user adds to a change after you've relayed it ("but less smooth"), and the Director's confirmation doesn't mention the addition, ask again. The confirmation may predate it.
  - **Reference images:** download them to `align/reference/`, look at them, and relay the path plus a written description of what the reference shows. Agents can't open a user's link reliably.
  - **A reference from an existing franchise or product:** add "original design, inspired by, no copying of <IP>'s signature features, colours or markings" to the relay, so it goes into the D-number.
  - **Label your own observations.** If you spot a flaw the user hasn't mentioned, you may pass it on, marked "main-session observation, not a user decision".
- **A lead or worker messages you instead of the Director:** expect this. Nested replies can land at the root (open Claude Code bugs). Forward the message by ID to the right agent, and don't act on it yourself.
- **Alignment picks:** when the Director sends a contact sheet (`align/<item>/index.md`), look at the images yourself, then present them to the user: the paths, the options, and your honest read of each option's flaws. Ask in plain text, not only multiple choice. "None of these" plus a redirect is a common and valid answer for taste gates, and a forced choice hides it. Relay the pick, or the redirect, as a D-number.
- **Relaying results up:** say whether QA verified a claim. A builder's self-check reaches the user as "unverified until QA"; if a verified-sounding claim later fails, correct it to the user promptly.
- **Keep exchanges small:** one decision per ask, with one image or sheet and your recommendation. Queue non-urgent questions for the next natural checkpoint instead of stacking them.
- **The user goes offline:** tell the Director to keep going and make the calls itself (`director.md` → "Offline decisions").
- **Status questions:** read the Roster and Status sections of `BOARD.md`, never the logs. If a swap is in progress, say so rather than guessing.
- **Look at clips yourself.** Pull readable frames (e.g. `ffmpeg -vf "select=not(mod(n\,N)),scale=480:-1,tile=4x3"`) or crops rather than trusting thumbnail strips. The main session's own frame reads caught defects the numbers missed.
- **Check the machine when the team grows** and before long jobs: `uptime` (load vs cores), AC power, free RAM and disk. If load exceeds the core count, ask the Director for a CPU slot lock (N flock slots, pinned threads per job) next to the GPU lock. If on battery, hold long jobs and ask the user to plug in.
- **Correct yourself promptly.** When a verified-sounding result you relayed is withdrawn (e.g. a measuring-tool flaw), tell the user straight away and say which other results depend on it.
- **When the user won't pick:** relay their brief as a D-number, and let the Director decide by rule. Stop ending updates with choices; ask only for what only the user can supply (references, the render go, the cap).
- **Never message an old agent ID** that has handed off. Messaging a completed agent resumes it with stale context.
- **Notifications:** use `PushNotification`, if available, only when something needs the user or everything is done. For a sleeping user, one "done" is enough.
- **Your own context:** if the user wants a fresh session, first finish any Director swap. Then write `handoff/main.md` (the user's decisions, pending questions, the Director's current ID) and tell the user to start from that file and the plan.

## Winding down (the user wants to stop and hand off)
1. Send the Director the user's words plus the procedure in `director.md` → "Wind-down". Any user finding that arrives at the same time is recorded as the next session's first open item, not started.
2. Artefacts already in flight (a gate sheet, a clip) may still land. Present them, and carry the pick into the handoff as a pending decision.
3. When the Director reports "wind-down complete", **verify it yourself**. Check that no build or render processes are running (e.g. `pgrep -a blender`), the lock files are free, and the Roster shows every role as parked or done. Agent reports can lag: a stray timer can resume a parked agent afterwards, and that isn't new work.
4. Write `handoff/main.md`:
   - how to restart: load this skill, read `handoff/director.md`, and **spawn a new Director**. Never message an old ID.
   - the user's shaping decisions (D-numbers)
   - pending user questions, with paths and your recommendation
   - "working with this user": pace, how they like picks presented, where images go, what they catch by eye
   - the agent definitions the Director added or changed in `.claude/agents/`, the implementation file in `.claude/directing-agent-teams/implementations/`, and the `/directing-agent-teams:promote` command for each one worth keeping
   - suggested changes to the skill's own files, to send upstream (the plugin's files are replaced on update, so nobody edits them in place)

Relay the Director's report as it is, including what's **provisional or unverified**, what was cut, and decisions made without the user. Report faithfully.

## Common mistakes (main session)
| Mistake | Fix |
|---|---|
| Doing the work yourself "to help" | Relay; the Director assigns |
| A mid-run change sent only to the Director; a lead's in-flight draft misses it | Send to both, and get confirmation |
| Reading logs to answer status questions | Read BOARD Roster and Status |
| Asking for the user's logo or credentials after they've gone to bed | Ask before launch |
| Messaging a lead by its description, or by an old ID | Use the current ID from the Roster |
| Launching a design project from words alone; the user rejects sheet after sheet | Get a reference image and the tone/era words before launch |
| The user's follow-up lands after the Director has confirmed the change | Check that the follow-up appears in the confirmation; ask again if it doesn't |
| Forcing a taste pick through a multiple-choice widget | Show the images, give your read, and ask openly |
| Relaying the user's franchise reference without an originality note | Add "original, inspired by, no copying" to the relay |
| Passing a builder's "it works" to the user as fact | Mark it unverified until QA passes it |
