# Architecture

Directing Agent Teams is a skill plus a set of agent definitions. There's no engine: the rules live in Markdown that each agent reads, and the state of a run lives in files in your project. These pages explain how the pieces fit and why. **The skill files are the source of truth.** Where a page and a skill file disagree, the skill file wins, and the page is a bug.

| File | Contents |
| --- | --- |
| [overview.md](overview.md) | The team's shape: the fixed top two layers, what's designed per project, depth and the agent cap, and the diagram legend. |
| [run-lifecycle.md](run-lifecycle.md) | A run from launch to report: the milestones, alignment gates, offline decisions, the freeze, and the wind-down. |
| [slices-and-qa.md](slices-and-qa.md) | How work is cut into time-boxed slices, the builder–verifier loop, and what independent QA checks. |
| [communication.md](communication.md) | The Roster, messaging by ID, the delivery rule, misrouted replies, and why files carry the content. |
| [resources-and-locks.md](resources-and-locks.md) | Sharing one GPU (or any scarce resource): locks, owner files, background jobs, stuck jobs, and who may kill what. |
| [context-management.md](context-management.md) | Keeping contexts small: what each agent reads, decomposition, extension versus new scope, compaction, and when to start fresh. |
| [context-and-turnover.md](context-and-turnover.md) | Handoff files, replacing an agent, silent deaths, Director rotation, and concurrent handoffs. |
| [recovery-scenarios.md](recovery-scenarios.md) | What each agent does when something changes around it: its lead was replaced, a worker went quiet, it was resumed by an old ID, the Director died, the cap is exceeded, and more. |
| [learning.md](learning.md) | How lessons move from a run to every run: agent copies, case studies, `/promote`, and upstream. |
| [incidents.md](incidents.md) | Each rule next to the incident that produced it. |

## Where each rule lives in the skill

| Skill file | Read by | Covered on |
| --- | --- | --- |
| [`SKILL.md`](../../skills/directing-agent-teams/SKILL.md) | the main session | [run-lifecycle.md](run-lifecycle.md), [communication.md](communication.md) |
| [`director.md`](../../skills/directing-agent-teams/director.md) | the Director | [overview.md](overview.md), [run-lifecycle.md](run-lifecycle.md), [slices-and-qa.md](slices-and-qa.md), [learning.md](learning.md) |
| [`rules.md`](../../skills/directing-agent-teams/rules.md) | every agent | [communication.md](communication.md), [resources-and-locks.md](resources-and-locks.md), [recovery-scenarios.md](recovery-scenarios.md) |
| [`qa.md`](../../skills/directing-agent-teams/qa.md) | verifiers and reviewers | [slices-and-qa.md](slices-and-qa.md) |
| [`context-turnover.md`](../../skills/directing-agent-teams/context-turnover.md) | whoever replaces an agent | [context-and-turnover.md](context-and-turnover.md), [recovery-scenarios.md](recovery-scenarios.md), [context-management.md](context-management.md) |
| [`templates.md`](../../skills/directing-agent-teams/templates.md) | the Director | [../project-files.md](../project-files.md) |
| [`examples.md`](../../skills/directing-agent-teams/examples.md) | the Director, while designing | [overview.md](overview.md) |
| [`runtime-facts.md`](../../skills/directing-agent-teams/runtime-facts.md), [`knobs.md`](../../skills/directing-agent-teams/knobs.md) | anyone | [../troubleshooting.md](../troubleshooting.md), [../getting-started.md](../getting-started.md) |
| [`implementations/`](../../skills/directing-agent-teams/implementations/README.md) | the main session and the Director | [learning.md](learning.md) |
