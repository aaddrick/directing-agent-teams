# Running a team

Once the Director is running, the main session (the Claude you're talking to) only relays. It never builds, and it forwards anything that reaches it by mistake. This page covers what you do in the meantime.

## Asking for status

Ask Claude how it's going. It reads the Roster and Status sections of `BOARD.md` and answers from those, not from logs. If a role is being replaced at that moment, it says so rather than guessing.

Results reach you per slice: "slice <id>: PASS / FAIL, <artefact path>, <next>". A builder's own claim reaches you as **unverified until QA**. If a result Claude relayed later turns out wrong, it tells you straight away and says which other results depended on it.

## What the main session does on its own

Besides relaying, the main session has a few habits from the skill:

- **It looks at clips itself.** It pulls readable frames with `ffmpeg` (a tiled contact sheet or crops) rather than trusting thumbnail strips. Its own frame reads have caught defects the numbers missed.
- **It labels its own observations.** If it spots a flaw you haven't mentioned, it may pass it on, marked "main-session observation, not a user decision".
- **It checks the machine** when the team grows and before long jobs: load against the core count, AC power, free RAM and disk. If load exceeds the cores, it asks the Director for a CPU slot lock. On battery, long jobs wait and it asks you to plug in.
- **It keeps exchanges small:** one decision per ask, with one image or sheet and its recommendation. Questions that aren't urgent wait for the next natural checkpoint.

## Changing your mind

Say it in your own words. Claude sends your exact words to the Director **and** directly to every lead the change affects, then asks the Director to confirm in one line that it's applied. Work already in flight predates the change, so that confirmation matters.

- **Adding to a change** ("but less smooth") gets its own confirmation. If the Director's reply doesn't mention the addition, Claude asks again.
- **A new reference image:** Claude downloads it to `align/reference/`, looks at it, and relays the path plus a written description. Agents can't open your link reliably.
- **A reference from an existing franchise or product:** Claude adds "original design, inspired by, no copying of its signature features" to the relay, so it becomes part of the recorded decision.

Every decision is recorded on `BOARD.md` as a D-number with your exact words, so later agents don't argue it again.

## Picking from a contact sheet

Before anything expensive (a full render, a long composition, a training run), the Director builds 4 to 8 cheap options labelled A to H on one sheet at `align/<item>/index.md`. Claude looks at the images itself, then shows you the paths, the options and its honest read of each option's flaws.

It asks in plain text, not a multiple-choice widget. **"None of these" plus a redirect is a normal answer** for taste gates. After two rejected sheets, the Director stops generating variants and asks you for a reference or a list of what's wrong.

If you'd rather not pick at all, give a brief instead. In the mech run: *"I am not going to pick. Just make sure it moves like it's a building sized war machine... controlled but powerful."* The Director turns it into tests on every card, decides by a declared rule, and shows you results instead of options.

## Going offline

Tell Claude you're going to bed. The Director keeps going and makes the calls itself:

- A choice that **blocks** other work gets a provisional pick by a rule declared in advance, labelled PROVISIONAL, with the runner-up kept cheap to swap to.
- A choice that blocks nothing waits for you as a comparison table marked PENDING USER DECISION.

You get a push notification only when something needs you or everything is done, if notifications are available.

## Stopping for the day

Tell Claude you want to stop. The wind-down runs in order:

1. The Director tells every lead to finish its current step, start nothing new, and leave no half-written files. Short background jobs may finish; long ones stop at a resumable point.
2. Each lead brings its handoff file up to date, sets its Roster row to `parked`, and confirms.
3. Locks are released, and the Director writes `handoff/director.md` with the state, pending decisions, next steps in priority order, and the team to respawn.
4. **Claude checks for itself** that no build or render processes are left and the lock files are free. A leftover timer can wake a parked agent, and reports can lag.
5. Claude writes `handoff/main.md`: how to restart, your decisions, pending questions, how you like picks presented, and the agent changes worth keeping.

Anything that lands during the wind-down, such as a gate sheet already in flight, is carried into the handoff as a pending pick.

## Restarting later

Start a new session in the project directory and point Claude at `handoff/main.md`. It loads the skill, reads `handoff/director.md`, and spawns a **new** Director. It never messages an old agent ID: messaging a finished agent resumes it with stale context.

## Reading the final report

The Director's final report covers:

- what shipped, with paths and specs
- what was cut and why
- the QA verdict per item, with its worst remaining issue
- what's provisional or unverified
- decisions made without you
- downloads and licences, and total resource use
- exact commands to reproduce everything
- agent changes and the case study worth keeping, each with its `/directing-agent-teams:promote` line (see [Commands](commands.md))
- general rules the run taught, as suggested changes to the skill
