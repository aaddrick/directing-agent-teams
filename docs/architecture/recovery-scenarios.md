# Recovery scenarios

What an agent does when something around it changes or breaks, from that agent's side. The thread through all of it: **BOARD is the source of truth, and nobody checks on an agent by messaging it**, because messaging a finished agent resumes it with its old context.

## My lead was replaced

A worker goes to report, but the lead that spawned it has handed off.

1. **Report to the Roster's current ID,** not the remembered one. Check the Roster before messaging after a long gap.
2. Usually the new lead has already said "I'm now <role>; report to me". It messages every live worker in its handoff file when it starts.
3. If `SendMessage` fails or no reply comes in time, check the Roster again and resend.
4. If the lead's row says `handing-off` or is empty, append the message under `Inbox → <role>` on BOARD, marked `(undelivered)`, and tell the level above.
5. **If your own lead is gone, the level above is the Director.**

The new lead works through its Inbox when it starts, so nothing sent in the gap is lost.

## My worker went quiet

Check BOARD and the worker's output files, not the worker.

- **Finished:** its row says `done` or its output is complete. Review it before QA, then accept it or re-dispatch the task.
- **Stuck:** no growth in its log or output for about twice the expected duration. Report it with evidence. If it's also silent on BOARD, mark its row `dead` to free the slot.
- **Before re-running a dead worker's task,** move its partial output to `<path>.partial.<time>`. Never delete it.

## I was woken by an old ID

Someone messaged an agent that had already handed off. Don't act on it: file the message under `Inbox → <role>`, marked `(undelivered)`, tell the level above, and stop.

## I'm the replacement

Set your Roster row to `g<N+1>` and `active`, read only the plan, BOARD and your handoff file, announce yourself to peers and live workers, and process your Inbox. If your row says `recovered: handoff may be stale`, re-verify state before acting. Details: [context-and-turnover.md](context-and-turnover.md#replacing-an-agent).

## Someone died without handing off

The level above notices (no status for about 30 minutes, a completion without `HANDOFF`, or failing messages) and respawns the role from its handoff file. If the work turns out complete, it marks the role `done` instead. For the Director, the main session does this. See [Silent death](context-and-turnover.md#silent-death).

## The cap is already exceeded

Inherited workers count normally; only an outgoing agent's brief overlap is exempt. The Director tells idle or finished leads to hand off or mark themselves `done` until the count fits.

## My worker slots are full

Slots exist for parallelism, not permission. Do the bounded version yourself (a grep, a tail, a single preview), or ask the Director for a temporary slot. Never exceed the cap.

## A finding is outside my paths

Write it to `findings/<owner-role>/<time>-<you>.md` with the file, line and a repro, and send the owner the path. If it blocks your milestone and there's no ack by your next BOARD update, escalate to the Director.

## A requirement changed mid-slice

Work in flight predates the change, so the main session sends your words to the Director **and** every affected lead, and the Director confirms. The change becomes a queued slice, unless it changes the identity or the milestone, in which case the Director re-plans.

## Elsewhere

- A message landed at the main session: [communication.md](communication.md#misrouted-replies).
- A lock is held by a dead agent: [resources-and-locks.md](resources-and-locks.md#who-may-kill-what).
- A spawn was refused: [troubleshooting](../troubleshooting.md).
