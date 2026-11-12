# Context and turnover

Agents stop, get replaced or die. The design goal is that none of those loses work, messages or workers. Files are the record; messages are pointers to files. This page covers the mechanics from the level above. [recovery-scenarios.md](recovery-scenarios.md) walks through each situation from the affected agent's side, and [context-management.md](context-management.md) covers keeping contexts small in the first place.

## Decomposition and small state

Context size is managed by keeping every agent in its lane and keeping what a replacement must read small. Long contexts are fine for workers. For the Director they're the run's largest cost, because every replacement re-reads its state: in the 2026-11 game refine run each Director re-read a ~3,200-line handoff and a ~950-line rulings file, at 370k–710k tokens per generation. Handoff files and the Decisions table therefore hold the current state only, about a page each, with history archived by path. When a scope grows, the Director splits it or hands the out-of-scope finding to its owner. Agents query large files with `jq`, `python` or `grep` instead of reading them whole, and leads send summaries instead of logs.

Image-heavy roles fill their context fastest (reviewing renders, contact sheets, screenshots). In the mech run, leads that reviewed many renders turned over three generations in one day. They hand off at natural boundaries, well before the limit.

## The handoff file

Every role keeps `handoff/<role>.md` current at every milestone step and before any long wait, not only when it's about to leave: files owned, milestone state and next step, D-numbers relied on, live workers, open QA findings, what it's waiting on, and gotchas. A silent death recovers only as well as the last handoff.

## Handing off on purpose

An agent hands off when its next phase is different work, or when the level above asks:

1. If a handoff below it is pending, it spawns that replacement first, or lists it under "Waiting on".
2. It brings `handoff/<role>.md` up to date.
3. It sets its Roster row to `handing-off`.
4. It messages the level above: `HANDOFF <role>: handoff/<role>.md, live workers: <IDs>, awaiting: <items>`.
5. It stops. Never without step 4.

It doesn't wait for its live workers. It lists them, and the replacement takes them over.

## Replacing an agent

The level above replaces it: the main session for the Director, the Director for leads, the QA lead for reviewers.

1. **Spawn in the background with only the plan, BOARD and the handoff file.** No logs, no transcript. The description carries the generation, for example `WS2 lead g2`. Write its ID into the Roster at once.
2. **The replacement** sets its row to `g<N+1>` and `active`, tells its peers and live workers "I'm now <role>; report to me", and processes its Inbox.
3. **It checks workers through BOARD and their output files,** never by messaging them: messaging a finished worker resumes it.

The outgoing agent stops right after announcing, so the brief overlap doesn't count against the cap.

## Stopped versus full

An agent stopped by a usage limit, not a full context, is **resumed**: the level above messages its ID once the limit resets, and it carries on with its context intact and no cold re-read. Only an agent whose context is full, or that has died, is replaced.

## Silent death

Agents die without announcing, from a full context, a rate limit (whose result is never delivered) or a stall abort. Messages to an agent that has ended its turn can also be swallowed. In the game refine run, dead or sleeping agents went unnoticed for 22, 63 and 90 minutes. So the level above checks on a **status pass every ~15 minutes**, without pinging anyone:

- **the transcript has stopped.** Each subagent's `agent-<id>.jsonl` shows when it last did anything. A transcript that ends on a tool call that never ran is a dead agent. One that ends on text beside a finished run is asleep, and gets one nudge naming the finished file.
- no status line for about 15 minutes while its work is in progress
- a task notification that the agent finished without `HANDOFF` (it goes to whoever spawned it)
- messages to it failing

A "dead" agent can still wake and write hours later, so the replacement works in a new output folder, on a copy of the dead agent's tree.

It spawns a replacement from the last handoff file plus the role's BOARD status and output files, and marks the Roster row `recovered: handoff may be stale`. The replacement re-verifies state before acting, and stops any pollers, wait loops or log followers the dead agent left behind. Every background wait has a `timeout` for the same reason: in the game refine run one log follower outlived its agent by 34 hours.

If a role's work is actually complete but it finished without `HANDOFF`, the level above verifies the outputs, marks it `done`, and doesn't respawn it.

## Hand-off marks

Hand-offs are ordered from the harness's token count (the agent's task notice, or its transcript's last usage block), never the agent's own estimate, which ran about 70k low. Fresh agents read about 160k before their first run, so marks sit near 300k, and heavy roles are split by phase (cases, measurement, verdict), one card per agent.

## Director rotation

A Director relaying a busy flat-slice team (10–14 agents, about 100 D-numbers) died of "prompt too long" after about six hours, and its handoff file was hours stale. So:

- The Director is rotated at each major phase, for example at the freeze or before the full render.
- The Director rewrites `handoff/director.md` at every milestone.
- The Director rotates by context size or after about 90 minutes of busy relaying, whichever comes first. In the game refine run a narrower brief (about 135 lines of rulings, no periodic digests, this rotation rule) took Directors from about 60 to about 88 minutes each. Both figures are from one run.
- If one dies anyway, the main session seeds the replacement from BOARD (Roster, Status, the latest D-numbers) and the live agents' IDs, and tells it to grep BOARD rather than read it whole.

## Concurrent handoffs

When the Director hands off while a lead's handoff is pending, the outgoing Director spawns the lead's replacement **before** announcing its own handoff. If it can't, the pending swap goes under "Waiting on" in `handoff/director.md`, so the next Director does it first.

## The main session's own limit

The main session can't replace itself. If you want a fresh session, it first finishes any Director swap and confirms the new Director is active, then writes `handoff/main.md` with your decisions, pending questions and the Director's current ID. You start a new session from that file and the plan.
