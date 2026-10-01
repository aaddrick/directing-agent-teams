# Rules for every agent (leads, workers, reviewers)

Read this, then the plan (`PLAN_<project>.md`) and `BOARD.md`. The plan fills in the project-specific values: lock names and order, preview definitions, owned paths and budgets. These rules apply to you, and to any agent you spawn: tell it to read this file.

## Communication
- **Message by agent ID** with `SendMessage`. Descriptions don't resolve. You have no `ListAgents`, so find everyone, including whoever spawned you, in **BOARD → Roster**.
- **When you spawn an agent, write its ID** (from the Agent result) into the Roster immediately, with its role and "spawned by". Nobody else can look it up.
- **Send status up one level:** workers to their lead, leads to the Director, never to the main session. Also update your BOARD status section.
- **Timestamps come from `date`,** never estimated. Guessed times on BOARD, ETAs and lock files mislead everyone who reads them.
- **Keep your BOARD status line current.** When your task changes, update it, and include the time from `date`. A stale line is the first thing the main session reads when the user asks for status.
- **Pointers, not payloads.** Put content in files (`qa/…`, `notes/…`, `handoff/…`) and send paths and one-line verdicts.
- **Delivery rule:**
  - If `SendMessage` fails ("no such agent"), or there's no reply by the time you need one, check the Roster (the role may have handed off) and resend to the current ID.
  - If the role is handing-off or empty, append the message under `Inbox → <role>` on BOARD, marked `(undelivered)`, and tell the level above. If your own lead is gone, the level above is the Director.
  - Check the Roster before messaging a role after a long gap.
  - **Never message a handed-off agent's old ID:** that resumes the stale agent.
- Messages arrive only at your next tool call, so don't sit in long blocking calls.

## Scarce resources
- **Every command that uses a scarce resource runs under its lock:** `flock -w 1800 <repo>/.<res>.lock <cmd>`. That includes previews and one-off scripts that touch the GPU. There's one job per resource, machine-wide, with no exceptions and no bypassing.
- **Multi-stage jobs** (e.g. bake, then render) **release one lock before taking the next.** Hold several locks at once only when a single step truly uses both, and then take them in the plan's **declared order**.
- **Say who holds a lock:** when you take it, write `<role> <agent ID> PID <pid> expected-end <time>` to `<repo>/.<res>.lock.owner`. Also log the job in BOARD → Resource log with its PID and expected duration. Estimate the duration from similar past jobs in the log. If there's no history, run a short timed sample first.
- **Run long jobs and lock waits in the background** (Bash `run_in_background`) and poll every few minutes by tailing the log. A foreground wait longer than `CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS` (default 10 min) aborts you, and any blocking wait leaves you deaf to messages.
- **Iterate on previews** as the plan defines them. **Full-scale runs happen only at gates, with the Director's approval**, and within the per-item cap. Check preconditions (e.g. AC power, disk space) first.
- **Log every job** as one line in BOARD → Resource log: who, what, start and end.
- If a lock wait times out, read `.<res>.lock.owner` and the Resource log, then post on BOARD and tell your lead or the Director what you found.
- **Stuck job:** a job counts as stuck when its log or output hasn't grown for more than about twice its expected duration. Report it with evidence. If its worker agent is also silent on BOARD, mark the worker's Roster row `dead`. That frees its slot, and the task can be re-run after its partial output is moved aside.
- **Killing processes:**
  - Never kill a process you didn't start. Report it instead.
  - **Exception:** the current holder of a role may stop that role's own jobs, including ones a previous generation or its workers started, once the Resource log and the owner file confirm it's the role's job.
  - Anything else goes to the Director.
  - Find processes with `ps -eo pid,args | awk '/pat/ && !/awk/'`, never `pkill -f`.

## Files
- **Touch only the paths you own** (BOARD → Ownership). For anything else, write the finding (file, line, repro) to `findings/<owner-role>/<time>-<you>.md` and send the owner that path. If it blocks your milestone and there's no ack by your next BOARD update, escalate to the Director.
- New work goes in new files and directories, and existing deliverables are never overwritten. With no git, back up a file before editing it. Never modify vendored or third-party directories.
- Before re-running a dead worker's task, move its partial output to `<path>.partial.<time>`. Never delete it.
- Keep work deterministic (seeded), and **measure before claiming**.

## Editing BOARD.md
Every agent writes to BOARD, so edits collide. In one run, concurrent writes erased status sections three times: once before the lock existed, and twice more from whole-file rewrites.
- **Edit in place, never rewrite the whole file.** Never use Write on BOARD, and never write it out from a copy you read earlier. Use the Edit tool's exact replacement, or a read-modify-write under the lock.
- **A read-modify-write runs under the BOARD lock:** `flock <repo>/.board.lock <cmd>`. Re-read the file inside the lock, change only your own section or row, write, release. Hold the lock for seconds, never around a long job.
- **Touch only your own section or row,** plus the Roster row of an agent you just spawned and the Inbox of a role you're writing to.
- **The Director snapshots BOARD** to `handoff/BOARD.snapshot.md` after each of its own edits, so a lost section can be restored.

## Scope
- Do only your assigned task. **Read only what it needs.** Grepping or tailing a big log yourself is fine; delegate to a worker when you'd need to read large portions of it.
- Put out-of-scope observations on BOARD for the Director. If you know the owner and have a concrete repro, use the `findings/` path instead. Don't act on either.
- Don't add deliverables. Put ideas in your notes as suggestions.
- **Leads:** run at most 2 workers at a time, review worker output before QA, and write `notes/<ws>.md` (methods, key numbers, paths) at each gate.
- **Workers:** one task, then finish.
- **You never certify your own work.** QA does. When your piece is ready for a gate, tell the Director `ready for M<n>: notes/<ws>.md`. The Director asks QA to review it.
- **Leads run only as many workers as the plan's cap schedule gives them**, up to 2. The cap wins. QA reviewers count as the QA lead's workers.
- **Leads may run jobs themselves.** Worker slots exist for parallelism, not permission. When the delegation rule meets a full slot, do the bounded version yourself (grep, tail, a single preview), or ask the Director for a temporary slot. Don't exceed the cap.

## Slices
- Work from a **slice card** on BOARD (goal, acceptance test, artefact, time box). If the card is missing, ask your lead for one before you build.
- **Stop at the time box.** Report PASS, FAIL or partial with the artefact path, and don't widen the scope to finish.
- One slice's artefact answers one question. Put other findings in `findings/` for the owner.
- **Builders:** self-check with the verifier's tool, and state the measurement method with every number. When the verifier's verdict reaches you inside your box, do one fix round against it.
- **Verifiers:** send the verdict path to the builder as well as the Director. Prove every new measuring tool on a known failing case before its PASSes count.

## Handoff
- **Keep `handoff/<role>.md` current**, updating it at every milestone step and before any long wait. It lists:
  - files owned
  - milestone state and next step
  - D-numbers relied on
  - live workers (ID, task, output path)
  - open QA findings (paths)
  - what you're waiting on
  - gotchas
- **Parking at a wind-down:** finish the current atomic step, stop or finish background jobs as the Director says, kill your own pollers and timers, release locks, update the handoff file and BOARD status, set the Roster row to `parked`, confirm up one level, then stop.
- **When your scope is done:** set your Roster row to `done` and stop.
- **Hand off** when your role's next phase is different work (at a milestone boundary), or when the level above asks:
  1. If a handoff below you is pending, spawn that replacement first, or put it under "Waiting on".
  2. Bring `handoff/<role>.md` up to date.
  3. Set your Roster row to `handing-off`.
  4. SendMessage the level above: `HANDOFF <role>: handoff/<role>.md, live workers: <IDs>, awaiting: <items>`.
  5. Stop. **Never stop without step 4.**
- **Don't wait for live workers before handing off.** List them. Your replacement takes them over and reviews their output before QA.
- **If you are a replacement:** check your Roster row, set it to `g<N+1>` and `active`, tell your peers and live workers "I'm now <role>; report to me", then process your Inbox, marking entries `(done <time>)`. Check a worker's aliveness from BOARD and its output files, not by messaging it.
- **If you are resumed after handing off** (someone messaged your old ID): don't act on it. Append the message under `Inbox → <role>` on BOARD, marked `(undelivered)`, tell the level above, then stop.
- Generations are numbered `g1`, `g2`, …. Lock and file names come from the plan.
