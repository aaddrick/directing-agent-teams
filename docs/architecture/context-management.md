# Context management

Every agent has a context window, and a long run fills them. The skill doesn't count tokens. It keeps each context small by design, keeps the record in files so a full context costs little, and replaces agents before or after they fill up.

## Small by design

- **Each agent reads only its own file.** The main session reads `SKILL.md`, the Director reads `director.md`, every other agent reads `rules.md`, and checkers add `qa.md`. Nobody loads the whole skill.
- **Read only what the task needs.** Agents query big files with `jq`, `python` or `grep` instead of reading them whole. Grepping or tailing a big log is fine. Reading large parts of one is a job for a worker.
- **Workers do one task, then finish.** A worker's context never outlives its task, so it never fills up.
- **Fresh reviewers for each gate.** A reviewer doesn't carry the last gate's renders into this one.
- **Pointers, not payloads.** Messages carry a path and a one-line verdict. The content sits in a file that only the agent that needs it opens.
- **Summaries go up, logs stay down.** The Director asks leads for summaries and doesn't read their logs. The main session answers status questions from BOARD's Roster and Status, never from logs.
- **Downstream roles read notes, not code.** Each lead writes `notes/<ws>.md` (methods, key numbers, paths) at each gate, so another workstream gets what it needs without reading the code.

## Keeping agents in their lane

Context is managed by **decomposition**: keep every agent to its scope, and split a scope that grows. In practice:

- **Out-of-scope findings aren't acted on.** The agent writes them to `findings/<owner-role>/` or a BOARD note, and the owner or the Director deals with them.
- **One agent doesn't pile up phases.** When a role's next phase is different work, it hands off at the boundary rather than carrying the old phase's context into the new one.
- **Extension or new scope?** If new work touches the same files and is the same kind of work, the current owner extends it (a recorded decision). New files or a different kind of work means a new lead, seeded with the previous lead's handoff file and notes.

## When contexts fill anyway

Image-heavy roles (reviewing renders, contact sheets, screenshots) fill up fastest; in the mech run, leads like that turned over three generations in a day. They hand off at natural boundaries, well before the limit. The Director also doesn't hand a verifier past about 200k tokens a new card; it spawns a fresh one and points it at the old verdicts and tools. Handoffs, silent deaths and Director rotation are in [context-and-turnover.md](context-and-turnover.md).

## Compaction

Subagents use the same auto-compaction as the main session. You can turn it off with `autoCompactEnabled: false` (or `DISABLE_AUTO_COMPACT`), or tune when it triggers with `CLAUDE_CODE_AUTO_COMPACT_WINDOW` and `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`. See [`knobs.md`](../../skills/directing-agent-teams/knobs.md).

- **With compaction on,** a long context is summarized, and details the agent needed can go missing from the summary.
- **With compaction off,** a long context runs to the model's hard limit and the agent dies. The handoff and silent-death rules exist for exactly that, and the mech runs used this setting.

Either way, the files are the record. An agent that compacts or dies is recovered from its handoff file and BOARD, not from its memory.

## The main session's own context

The main session can't replace itself, so it stays lean: it relays, reads BOARD instead of logs, and asks one decision at a time. See [context-and-turnover.md](context-and-turnover.md#the-main-sessions-own-limit).

## Not yet known

How a subagent's context window is sized isn't documented. Test it locally before planning around it.
