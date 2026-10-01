# Resources and locks

Many agents, one GPU. Every scarce resource gets one lock, and every job that uses it runs under that lock in the background.

## One lock per resource

The plan names a lock file per scarce resource: `.gpu.lock` for the GPU, `.sim.lock` for a CPU- and RAM-heavy simulation, or one for an API quota. It also declares a **fixed acquisition order**, for example simulation before GPU, and budgets for RAM, disk and CPU workers.

Every command that touches the resource runs under its lock, previews and one-off scripts included:

```bash
flock -w 1800 <repo>/.gpu.lock <cmd>
```

One job per resource, machine-wide. No exceptions and no bypassing.

- **Multi-stage jobs release one lock before taking the next** (bake, then render). An agent holds two locks at once only when one step truly uses both, and then takes them in the declared order.
- **Never wrap a script in a lock it already takes.** In the mech run, a render script that took `.gpu.lock` itself was wrapped in another `flock` on the same file, and it deadlocked the GPU for about 20 minutes.

## Saying who holds it

When an agent takes a lock, it writes `<role> <agent ID> PID <pid> expected-end <time>` to `.<res>.lock.owner`, and logs the job in BOARD → Resource log with its PID and expected duration. It estimates the duration from similar jobs in the log, or runs a short timed sample if there's no history.

## Background jobs

A subagent with no progress for `CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS` (default 10 minutes) is aborted, and an agent in a blocking call can't receive messages. So every long job and every lock wait runs with Bash `run_in_background`, and the agent polls every few minutes by tailing the log. A foreground `flock -w 1800` or a 30-minute render can trip the abort.

## Preconditions

Full-scale runs happen only at gates, with the Director's approval, after a precondition check: AC power, free disk, and machine load. When the team grows, the main session checks `uptime` against the core count, power, RAM and disk. If load exceeds the cores, it asks the Director for a CPU slot lock (N `flock` slots, pinned threads per job) next to the GPU lock. On battery, long jobs wait.

## Stuck jobs

A job counts as stuck when its log or output hasn't grown for more than about twice its expected duration. The agent reports it with evidence. If the job's worker is also silent on BOARD, its Roster row is marked `dead`, which frees its slot, and the task can be re-run after its partial output is moved aside to `<path>.partial.<time>`. Partial output is never deleted.

## Who may kill what

- **Never kill a process you didn't start.** Report it.
- **Exception:** the current holder of a role may stop that role's own jobs, including ones an earlier generation or its workers started, once the Resource log and the owner file confirm the job is the role's.
- **Anything else goes to the Director.** For an orphaned lock (a dead agent's job still holding it), the Director first confirms on the Roster that the owner is dead or recovered, and that the process is the team's job and not yours. Then it stops it and records a D-number. `flock` releases the lock when the process exits.
- **Find processes with `ps -eo pid,args | awk '/pat/ && !/awk/'`,** never `pkill -f`, which can match far more than intended.
