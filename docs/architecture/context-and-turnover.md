# Context and turnover

Agents stop, get replaced or die. The design goal is that none of those loses work, messages or workers. Files are the record; messages are pointers to files. This page covers the mechanics from the level above. [recovery-scenarios.md](recovery-scenarios.md) walks through each situation from the affected agent's side, and [context-management.md](context-management.md) covers keeping contexts small in the first place.

## Decomposition, not counters

Context size is managed by keeping every agent in its lane, not by counting tokens. Long contexts are fine. When a scope grows, the Director splits it or hands the out-of-scope finding to its owner. Agents query large files with `jq`, `python` or `grep` instead of reading them whole, and leads send summaries instead of logs.

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

## Silent death

Agents die without announcing, from a full context, a rate limit (whose result is never delivered) or a stall abort. The level above notices one of:

- a task notification that the agent finished without `HANDOFF`
- no BOARD status update for about 30 minutes while its work is in progress
- messages to it failing

It spawns a replacement from the last handoff file plus the role's BOARD status and output files, and marks the Roster row `recovered: handoff may be stale`. The replacement re-verifies state before acting.

If a role's work is actually complete but it finished without `HANDOFF`, the level above verifies the outputs, marks it `done`, and doesn't respawn it.

## Director rotation

A Director relaying a busy flat-slice team (10–14 agents, about 100 D-numbers) died of "prompt too long" after about six hours, and its handoff file was hours stale. So:

- The Director is rotated at each major phase, for example at the freeze or before the full render.
- The Director rewrites `handoff/director.md` at every milestone.
- If one dies anyway, the main session seeds the replacement from BOARD (Roster, Status, the latest D-numbers) and the live agents' IDs, and tells it to grep BOARD rather than read it whole.

## Concurrent handoffs

When the Director hands off while a lead's handoff is pending, the outgoing Director spawns the lead's replacement **before** announcing its own handoff. If it can't, the pending swap goes under "Waiting on" in `handoff/director.md`, so the next Director does it first.

## The main session's own limit

The main session can't replace itself. If you want a fresh session, it first finishes any Director swap and confirms the new Director is active, then writes `handoff/main.md` with your decisions, pending questions and the Director's current ID. You start a new session from that file and the plan.
