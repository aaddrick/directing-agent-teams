# Runtime facts and knobs (Claude Code v2.1.284, checked 2026-09-29)

These were verified by local tests (marked **tested**), or come from the docs at code.claude.com/docs/en/{sub-agents, env-vars, agent-teams} and CHANGELOG.md. Re-check them after upgrades; this area changes often.

## Facts the skill relies on
| Fact | Source |
|---|---|
| Agents can spawn agents up to **`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` layers below the main session** (default 3, where layer 3 had no `Agent` tool in testing). The deepest layer can't spawn. | tested + docs |
| If the Director isn't spawned directly by the main session, every role loses a layer. | follows from the above |
| **Background subagents have no `ListAgents`**, at any depth. They do have `SendMessage`. | tested + docs |
| **Messaging is session-wide by agent ID:** siblings, parent↔child and cross-branch all work (6/6 delivered). The runtime is one flat pool per session. | tested |
| A message is delivered at the receiver's **next tool round**. An agent inside a long blocking call doesn't see it until the call returns. | tested |
| Messaging a **completed** agent **resumes** it with its full history. An agent you stopped yourself doesn't auto-resume. | tested + docs |
| Sends by name are refused if the name now points to a newer agent. Use IDs. | docs (v2.1.199) |
| A child keeps running after its parent's last action. In interactive sessions the parent's completion is **held until its background children finish**; in `-p` and the SDK it isn't. | tested + docs |
| **Nested replies and completion notices can land at the root session** instead of the parent (open bugs #83599, #90463, #90256). | community issues |
| A subagent with **no progress for 10 minutes is aborted** by default (`CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS`). | docs |
| A rate-limit error ends a subagent early, and its result is never delivered. | docs |
| At most 20 concurrent subagents by default, and 10 parallel read-only tools plus subagents. Resumes bypass the limit. | docs |
| Subagents use the same auto-compaction as the main session. With `autoCompactEnabled: false` they don't compact, so a long context runs to the model's hard limit. | docs |
| **New agent definitions** (`~/.claude/agents/*.md`) hot-load: the main session sees them at once, and a running subagent picks them up too, but only after a lag (a spawn can be refused as "not in this session's list" for a while). No restart is needed; if a type is refused, fall back to general-purpose and retry later. Project definitions (`.claude/agents/*.md`) are expected to behave the same but haven't been tested. | tested 2026-09-29 (user level) |

## Observed in long runs (2026-11-10/11, about 300 agents; not re-tested on purpose)
| Fact | Source |
|---|---|
| A foreground command is moved to the background after about **3 minutes**, or when a message arrives. | observed |
| A message to an agent that has **ended its turn can be swallowed**: the send shows "Resuming", and the agent does nothing. One sat 90 minutes. | observed, several times |
| An agent resumed by a message while its own background chain ran **may not wake when the chain ends**. | observed, several times |
| A subagent that ends its turn with only background tasks running has **delivered its final report**; the background tasks don't keep it working. | observed |
| `TaskStop` from a subagent **can't stop an agent that subagent spawned** ("owned by"). | observed |
| Task notices go to the agent that **spawned** the child, even after that agent has handed off. | observed |
| Each subagent's transcript is `<session>/subagents/agent-<id>.jsonl`. Its **mtime shows liveness** without a ping, and its last usage block shows the context size. It can move to a new session folder between generations; find it with `find`. | observed |
| The **harness's token count** in a task notice (`<subagent_tokens>`) is reliable. Agents' own estimates ran about 70k low. | observed |
| The harness may **refuse a subagent's Write** of a deliverable named in a report, and a relayed user authorisation didn't change that. The Director, with the user's explicit authorisation, or the Edit tool lands such files. | observed 2026-11-06 |
| Fresh agents read about **150–160k tokens** (rules, plan, cases, handoff) before their first run, and finished heavy cards at 200–340k without harm. | observed |

## Consequences for the skill
- **The Roster is required**, because nobody below the main session can list agents.
- **Long waits must not block for 10 minutes or more.** Run long jobs, and `flock` waits, with Bash `run_in_background`, and poll every few minutes. A foreground `flock -w 1800` or a 30-minute render can trip the stall abort, and it makes the agent deaf to messages.
- **The main session forwards misrouted messages.** Reports from leads and workers may arrive at the root. Forward each one by ID to the right Director or lead, and don't act on it.
- **Silent deaths happen** from rate limits and stall aborts. Recover them from the handoff file.
- **Detect stalls from transcripts and files, not pings** (`context-turnover.md` → "Silent death").
- **Start an idle agent's next run with a file, not a message** (`go/<role>`): a message can be swallowed, a file can't.
- **Hand-off marks come from the harness's count,** set near 300k, because reading alone costs about 160k.

## Knobs
The settings and env vars to turn are in `knobs.md`.
