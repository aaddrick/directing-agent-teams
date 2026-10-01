# Knobs to turn (Claude Code v2.1.284, checked 2026-09-29)

These are env vars unless noted. Set them in `~/.claude/settings.json` under `"env": {...}`, in a project's `.claude/settings.json`, or in the shell before launching `claude`. Sources are code.claude.com/docs/en/{env-vars, settings, sub-agents, agent-teams} and CHANGELOG.md. **Re-check them after upgrades**, because defaults in this area have changed several times; spawn depth, for example, went 5 → 1 → 3 between June and July 2026.

## Most useful for directing agent teams (in order)
| Knob | Default | Use |
|---|---|---|
| `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` | 3 | Deeper trees (4–5), or 1 to turn nesting off. Open off-by-one report: #84974 |
| `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` | 20 | Fan-out ceiling. Set the plan's cap well below it |
| `CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY` | 10 | Parallel read-only tools plus subagents. The lower of this and the one above binds |
| `CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS` | 600000 | Raise it for agents that must block on long jobs |
| `CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS` | 10 min | In `-p` mode, how long to wait for background agents before exiting |
| `autoCompactEnabled` (setting), `CLAUDE_CODE_AUTO_COMPACT_WINDOW`, `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` | — | Whether and when long contexts compact, for subagents too |
| `CLAUDE_CODE_SUBAGENT_MODEL` / `_FORCE` | inherit | Cheaper model for workers |
| `CLAUDE_CODE_SUBAGENT_PROMPT_CACHE_TTL` / `subagentPromptCacheTtl` | — | Longer cache for long runs |
| `CLAUDE_CODE_WORKFLOW_MAX_CONCURRENT_AGENTS` | 16 | Workflow tool fan-out |
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` | off | Peer teams that message by name through mailboxes. Interactive only, and teams can't nest |
| Frontmatter `tools`, `disallowedTools`, `background`, `maxTurns` | — | Per-agent tool limits; leave `Agent` out to block spawning |

The following were found only in the local binary and are undocumented; their purpose is a guess from their names alone: `CLAUDE_CODE_SENDMESSAGE_HANDBACK`, `CLAUDE_CODE_EXPERIMENTAL_OBSERVER_AGENTS`, `CLAUDE_CODE_AUTO_BACKGROUND_TIMEOUT_MS`.

## Other documented knobs
| Knob | Use |
|---|---|
| `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS`, `CLAUDE_AUTO_BACKGROUND_TASKS` | Turn background tasks off, or run them automatically |
| `CLAUDE_CODE_AUTO_BACKGROUND_WORKER_CHECKIN_SECONDS` | How often background workers check in |
| `CLAUDE_CODE_FORK_SUBAGENT` | Fork-subagent behaviour. In a fork at the depth limit, `Agent` stays but errors |
| `CLAUDE_CODE_TEAM_TEARDOWN_PARK_TIMEOUT_MS` | Team teardown timing |
| `teammateMode` (setting) | How teammates run (with agent teams) |
| `CLAUDE_CODE_MAX_CONTEXT_TOKENS`, `DISABLE_AUTO_COMPACT` | Context ceiling; turn compaction off |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS`, `CLAUDE_CODE_MAX_TURNS` | Output and turn limits |
| `CLAUDE_CODE_FORWARD_SUBAGENT_TEXT` | Forward subagent text to the parent |
| `CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS`, `CLAUDE_CODE_DISABLE_AGENT_VIEW` | SDK built-ins; agent view UI |
| `maxBudgetUsd` (SDK) | Spend cap, subagents included |

## A setup that worked for overnight builds
These values ran a 10–14 agent build through a day and a night. Put them in `~/.claude/settings.json`:
```json
{
  "env": {
    "CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH": "4",
    "CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY": "20",
    "CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS": "1800000"
  }
}
```
- With depth 4, the Director (layer 1) can design leads → workers → sub-workers.
- With a 30-minute stall timeout, a blocking wait has more headroom, but backgrounding long jobs is still the rule, because a blocked agent can't receive messages.
- With `autoCompactEnabled: false`, a long subagent context runs to the model's hard limit instead of being summarized. That's fine if long contexts are acceptable, and the handoff and silent-death recovery rules cover the failure.

## Not documented (test locally before relying on them)
- What happens to live children when their parent is stopped with `TaskStop`.
- Any rate limiting per depth.
- How a subagent's context window is sized.
