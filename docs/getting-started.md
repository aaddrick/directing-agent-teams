# Getting started

Everything you need before your first run: what the skill needs from Claude Code and your machine, how to install it, and what to set before you leave a team running overnight.

## Requirements

- **Claude Code.** The skill depends on background subagents, agents that spawn agents, and `SendMessage` between agents. It was built and tested on Claude Code v2.1.284 to v2.1.286. Other harnesses and the Claude apps are not supported.
- **A token budget to match.** A team of 6 to 14 agents running for hours uses a lot of tokens. The Director runs on Opus; the other agents default to Sonnet.
- **The tools your build uses,** installed and working in a shell: Blender, ffmpeg, Python, whatever the project needs. Agents run them headless.
- **`flock`** if the project has a scarce resource such as one GPU. It ships with util-linux on Linux. On macOS, install it (for example `brew install flock`).

## Install

```bash
claude plugin marketplace add aaddrick/directing-agent-teams
```

```bash
claude plugin install directing-agent-teams@directing-agent-teams
```

The skill loads on its own when you ask Claude to fan a project out to a team. To load it by hand:

```
/directing-agent-teams:directing-agent-teams
```

## Recommended settings

The defaults work for a small team. For a large build that runs unattended, set these in `~/.claude/settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH": "4",
    "CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS": "1800000"
  }
}
```

| Setting | Default | Why raise it |
|---|---|---|
| `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` | 3 | The Director is layer 1. At the default, the deepest layer can't spawn, so leads can't have workers of their own. Depth 4 lets them |
| `CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS` | 600000 (10 min) | A subagent with no progress for this long is aborted. Agents are told to run long jobs in the background, but a longer timeout gives a blocked wait more room |
| `CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY` | 10 | Caps parallel subagents together with read-only tools. Raise it if the agent cap in your plan is near 10 |

The skill's [`knobs.md`](../skills/directing-agent-teams/knobs.md) lists every setting it knows about, including the undocumented ones. Defaults in this area have changed several times; re-check them after a Claude Code upgrade.

## Permissions

**A permission prompt stalls the team until you answer it.** If you leave a run overnight, pre-approve everything the build needs before you launch:

- the tools the build runs (for example `Bash(blender:*)`, `Bash(ffmpeg:*)`, `Bash(flock:*)`)
- edits anywhere in the project directory
- edits to the project's `.claude/` folder, where the Director keeps its agent changes and its case study (see [How the team learns](architecture/learning.md))

Claude warns you about this before launch, but it can't approve anything for you.

## Your first run

Start Claude Code in the project directory and describe the project, saying that you want a team on it:

```
Use a team of agents to build a 20 second product render of this mech in Blender.
Don't do anything yourself. Keep it going overnight. The GPU is the bottleneck.
```

What happens next:

1. Claude looks for a similar past project in the skill's case studies and the ones you've kept.
2. It asks one round of at most about five questions: a reference, the tone in your own words, what defines the thing versus what can wait, delivery specs, and the agent cap (6 by default). **For designed or visual work, a reference image is required.** Without one, the first design gate turns into rounds of guessing.
3. It writes `PLAN_<project>.md` and `BOARD.md` in the project directory.
4. It spawns the Director in the background and writes its ID into the Roster.

From then on Claude only relays. See [Running a team](running-a-team.md).
