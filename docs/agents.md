# Agents

The plugin ships nine agent types in [`agents/`](../agents). Claude Code loads them as `directing-agent-teams:<name>`. Each file is a role contract plus a dated list of Lessons from past runs, and it sets the role's default model and tools.

## The role map

| Agent | Model | Can spawn | Role |
|---|---|---|---|
| `team-director` | Opus | yes | Designs the team, writes slice cards, holds the gates, keeps the Roster. Writes no product code |
| `team-builder` | Sonnet | no | Builds one slice card in the paths it owns, time-boxed, then stops |
| `team-verifier` | Sonnet | no | Measures one slice's built output against its card and the requirements around it. PASS or FAIL with saved evidence |
| `team-taste-reviewer` | Sonnet | no | A skeptical audience for stills and clips. Flaws first, three best and three worst. Can't edit files |
| `team-animator` | Sonnet | no | Reworks one motion beat to a written motion brief, on a copy |
| `team-extent-verifier` | Sonnet | no | Compares every part of a new build with the last good one: size per axis, volume, vertex count, mirror pairs |
| `team-set-builder` | Sonnet | no | Adds set dressing, detail or access hardware as a layer that defaults to off |
| `team-surfacer` | Sonnet | no | Adds materials, wear and grime as a layer that defaults to off, with a licence log |
| `contrarian` | inherits | yes | Stress-tests a plan or storyboard before anyone builds: assumptions, pre-mortem, inversion |

The Director passes `model: "opus"` on a single spawn when a slice needs it, for example fiddly spatial work or a slice that failed twice on Sonnet. It notes the model and the reason in the Roster row. The definition's default doesn't change.

The four specialists (`team-animator`, `team-extent-verifier`, `team-set-builder`, `team-surfacer`) came out of the Blender mech run. Each exists because a general builder or verifier kept missing the same class of problem. See [Why it works this way](architecture/incidents.md).

## Contracts every agent shares

- **Read first:** `rules.md` from the skill, then `PLAN_<project>.md` and `BOARD.md`. Checkers also read `qa.md`. The Director puts the skill's directory in every spawn prompt, because the plugin's install path differs per machine.
- **Own only what the card lends.** Anything else goes to `findings/<owner-role>/` or a one-line BOARD note.
- **Never certify your own work.** Builders report "self-check, unverified"; only a verifier's verdict counts.
- **Report and stop.** One line plus paths to the Director by `SendMessage`, Roster row set to `done`, then stop.

## Which copy gets spawned

An agent type can exist in three places. The Director checks `ls .claude/agents/ ~/.claude/agents/` before each spawn:

| Where | Spawned as | Wins over |
|---|---|---|
| Project `.claude/agents/<name>.md` | `<name>` | everything |
| `~/.claude/agents/<name>.md` | `<name>` | the plugin's copy |
| The plugin's `agents/<name>.md` | `directing-agent-teams:<name>` | nothing |

When a copy exists in either folder, the Director spawns the bare name. Claude Code resolves a bare name to the project copy first, then the user copy. Otherwise it spawns the plugin's prefixed name.

The plugin's files are replaced on every plugin update, so nobody edits them in place. User-level copies are shared by every project, so the Director doesn't edit those either. It only writes to the project's `.claude/agents/`.

## How agents change during a run

The Director owns the project's agent definitions:

- **A Lesson** is one dated line, added as soon as a slice teaches a role something general: a check that caught a real failure, or a failure a check missed. If the project has no copy of the type yet, the Director first copies the one it would otherwise spawn (your user copy if you have one, otherwise the plugin's), then appends.
- **A new type** (`team-<role>`) is added when a role recurs across slices or projects and its contract differs from every existing type. A one-off need gets a slice card for an existing type instead.
- **A contract rewrite** backs the file up first, as `<file>.bak_<date>`. Appending a Lesson needs no backup.
- The Director tells the main session in one line whenever it adds a type or changes a contract. New files load without a restart, but a running agent may not see a new type for a few minutes. If a spawn is refused in that window, it falls back to `general-purpose` with the same model and retries later.

To keep a changed agent for every project, run [`/directing-agent-teams:promote`](commands.md).

## Writing a new agent type

Put it in the project's `.claude/agents/team-<role>.md`, or send it upstream in `agents/`. The shape:

```markdown
---
name: team-<role>
description: <one line: what it does and when to use it>
model: sonnet
disallowedTools: Agent
---

<One or two sentences: what this role is.>

## Read first
`<skill dir>` is the directing-agent-teams skill directory named in your spawn prompt.
1. `<skill dir>/rules.md` (and `<skill dir>/qa.md` for checkers).
2. The project's `PLAN_<project>.md` and `BOARD.md`: your slice card and Roster row.
3. Only the files your card names.

## Contract
- ...

## Lessons (append as the project teaches them; date each, keep each to one line)
```

Keep `disallowedTools: Agent` on anything that shouldn't spawn. Keep the file short: the contract and its Lessons, with no project detail. Project detail goes in the case study.
