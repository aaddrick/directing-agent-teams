# Context turnover

The goal is for agents to stop, be replaced or die without losing work, messages or workers. Context size is managed by decomposition and scope (see `director.md`), not by counters, and long contexts are acceptable. Files are the record; messages are only pointers to files.

## Rules for every agent
The handoff, delivery and scope rules every agent follows are in `rules.md` → "Communication" and "Handoff". This file covers what the **level above** does.

## Replacing an agent (done by the level above: the main session for the Director, the Director for leads and QA, the QA lead for reviewers)
1. **Spawn** in the background with only the plan, `BOARD.md` and `handoff/<role>.md`. No logs and no transcript. Give it a description with its generation, e.g. `WS2 lead g2`. The prompt says: "You replace <role> g<N>. Read rules.md, the plan, BOARD and your handoff file, then process your Inbox." Write its ID into the Roster immediately.
2. **The replacement:**
   - checks that its spawner wrote its ID into its Roster row, then sets `g<N+1>`, `active`
   - messages its peers and every live worker listed in the handoff: "I'm now <role>; report to me"
   - takes over the live workers by ID from the handoff file. Workers keep running after their spawner stops (tested). Spawned agents lack `ListAgents`, so aliveness is checked by the worker's BOARD status and its output files. Don't ping a possibly finished worker to check, because messaging it resumes it. For a worker that has finished or died, check its output path and either accept the output (after review) or re-dispatch the task.
   - processes its Inbox, striking each entry as `(done <time>)`. **Only the role owner clears its own Inbox.**
3. **Cap accounting:** the outgoing agent stops right after announcing, so a brief overlap doesn't count against the active-agent cap. If there are more workstreams than cap slots, finished or idle leads hand off and stop, and they're respawned from their handoff file when needed. Turnover doubles as scheduling.

## Staying ahead of the context limit
- **Keep the handoff file current at every milestone and major decision,** not only when handing off. A silent death from a full context recovers only as well as the last handoff.
- **Image-heavy roles fill their context fastest** (reviewing renders, contact sheets, screenshots). They hand off at natural boundaries, well before the limit.
- **Query large files; don't read them whole.** Use `jq`, `python` or `grep` on specs, logs and JSON.

## Silent death (no HANDOFF announced)
The level above detects it in one of three ways:
- a task notification that the agent finished without announcing `HANDOFF`
- no BOARD status update for about 30 minutes while its work is marked in progress
- messages to it failing

It recovers by spawning a replacement from the last `handoff/<role>.md`, plus the role's BOARD status and its output files. The Roster row is marked `recovered: handoff may be stale`, and the replacement re-verifies state before acting. Because the handoff is always current, the loss is small.

## Concurrent handoffs
When the Director hands off while a lead's handoff is pending, the outgoing Director spawns the lead's replacement **before** announcing its own handoff. If that isn't possible, the pending swap goes under "Waiting on" in `handoff/director.md`, so the next Director does it first.

## The main session
- **Stays lean:** relays only; reads BOARD's Roster and Status sections, never logs, and tells the user when a swap is in progress rather than guessing.
- **Its own limit:** it can't replace itself. If the user wants a fresh session (e.g. a multi-day project), it writes `handoff/main.md`, covering the user's decisions so far, pending questions, the Director's current agent ID. It then tells the user to start a new session from that file and the plan.

## Edge cases
- **Finished vs died:** a role whose work is complete sets its Roster row to `done` before stopping. If it finished without `HANDOFF` but BOARD or its handoff file shows the work complete, the level above verifies the outputs, marks the role `done`, and doesn't respawn it.
- **Don't depend on task notifications:** they may not reach a parent that has been replaced, and an agent's own completion notification is **held until its live children finish** (observed). Every agent's results land in files and in BOARD status. A replacement checks those, plus the Roster, instead of waiting for notifications.
- **Resolve roles through the Roster, always.** A replacement has a new agent ID. The old ID still resolves, but messaging it resumes the stale agent. The Roster is the only lookup from role to current ID.
- **Partial output:** before re-dispatching a dead worker's task, move its partial output to `<path>.partial.<time>` (never delete it), and have the new worker write to the original path.
- **Cap already exceeded:** the Director tells idle or finished leads to hand off or mark themselves `done` until the count fits. Inherited workers count normally; only the outgoing agent's brief overlap is exempt.
- **Order for the main session:** finish any Director swap first, and confirm the new Director is active on the Roster. Only then write `handoff/main.md`, which should include the Director's current agent ID.
- **Orphaned lock:** if a dead agent's job still holds the resource lock, the current holder of that role may stop it (per `rules.md`, after checking `.<res>.lock.owner` and the Resource log). Otherwise only the Director may stop it. It first confirms the owner is dead or recovered on the Roster, and that the process belongs to this team's job, not the user's. It records a D-number. `flock` releases the lock when the process exits.

## Proactive Director rotation (learned 2026-09-29)
A Director relaying a busy flat-slice team (10–14 agents, ~100 D-numbers) died of "prompt too long" after about 6 hours, and its handoff file was hours stale. Rotate the Director at each major phase (e.g. at the freeze, before the full render), and require it to rewrite `handoff/director.md` at every milestone. When one dies, the main session seeds the replacement from BOARD (Roster, Status, the latest D-numbers) and the live agents' IDs, and tells it to grep BOARD rather than read it whole.
