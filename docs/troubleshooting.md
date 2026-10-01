# Troubleshooting

For what each agent does when a teammate is replaced or dies, see [Recovery scenarios](architecture/recovery-scenarios.md).

Most of these come from Claude Code behaviour listed in the skill's [`runtime-facts.md`](../skills/directing-agent-teams/runtime-facts.md), which records the version it was checked on. Re-check after an upgrade.

- **The team stopped overnight and nothing is failing.** An agent is waiting on a permission prompt. Answer it, then pre-approve that tool before the next run. See [Permissions](getting-started.md#permissions).
- **"Not in this session's list" when spawning an agent type.** A new definition loads without a restart, but a running agent can take a few minutes to see it. The Director falls back to `general-purpose` with the same model and retries later. Nothing to fix.
- **A lead or worker messages the main session instead of the Director.** Nested replies and completion notices sometimes land at the root session (open Claude Code bugs). Claude forwards the message by ID to the right agent and doesn't act on it. Expect it.
- **An agent was aborted after 10 minutes.** A subagent with no progress for `CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS` (default 10 minutes) is aborted. Long jobs and lock waits should run in the background with polling. Raise the timeout if your jobs block for longer; see [Recommended settings](getting-started.md#recommended-settings).
- **An agent finished and its result never arrived.** A rate-limit error ends a subagent early, and its result is never delivered. The level above spots the silence and spawns a replacement from the role's handoff file. See [Silent death](architecture/context-and-turnover.md#silent-death).
- **The Director died with "prompt too long".** A Director relaying a busy team fills its context in hours. It should be rotated at each major phase, and it rewrites `handoff/director.md` at every milestone. If one dies, Claude seeds a replacement from BOARD and the live agents' IDs.
- **Messaging an agent woke up an old one.** Messaging a finished agent resumes it with its old context. Always look up the current ID in the Roster. An agent resumed this way files the message in BOARD → Inbox and stops.
- **Leads can't spawn workers.** They're at the deepest layer your spawn depth allows. Raise `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`, or let the Director spawn the workers itself. There's an open off-by-one report on this setting, so the Director checks it at M0 when the plan relies on the deepest layer.
- **The Director's completion notice never comes.** A parent's completion is held until its background children finish. Read BOARD's Roster and Status instead of waiting.
- **The GPU lock is stuck.** Read `.<res>.lock.owner` and the Resource log, then find the holder with `ps -eo pid,args`. One known cause: wrapping a script in `flock` when the script already takes the same lock deadlocks. Only the role that owns the job, or the Director, may stop it.
- **A parked agent started working again after the wind-down.** A leftover wait timer resumed it. That's harmless, and it's why Claude checks for running processes and free locks itself instead of trusting the reports.
- **BOARD timestamps and ETAs are hours off.** An agent guessed the time instead of running `date`. The rules require `date`; point the agent at `rules.md` → Communication.
- **The Director spawned the wrong copy of an agent.** Precedence is project `.claude/agents/`, then `~/.claude/agents/`, then the plugin. Check both folders for a copy with that name. See [Which copy gets spawned](agents.md#which-copy-gets-spawned).
- **An old user-level agent reads the wrong `rules.md`.** Agent copies made before the plugin existed point at `~/.claude/skills/directing-agent-teams/`. Change their "Read first" to use `<skill dir>`, as the shipped agents do, or delete them and use the plugin's.
