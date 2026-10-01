# Contributing

Lessons from real runs are welcome. So are corrections.

## Fix a fact

`runtime-facts.md` and `knobs.md` describe Claude Code behaviour that changes between releases. If a fact is wrong, open an issue or a pull request with the Claude Code version you tested on and how you tested it: a local repro, a changelog entry, or a page on code.claude.com.

## Add a lesson

Put a lesson where it applies:

- **A rule for every project** goes in the file for the role that follows it: `SKILL.md` (main session), `director.md`, `rules.md` (every agent), `qa.md` or `context-turnover.md`.
- **A lesson for one agent type** goes in that agent's Lessons list in `agents/`, as one dated line.
- **A lesson for one kind of project** goes in `skills/directing-agent-teams/implementations/`. Each file has two parts: "Best execution", written with hindsight as a plan to copy, and "Lessons learned", what actually happened. Add the file to the table in `implementations/README.md`.

Your own runs are the easiest source. After a run, look in these places:

- **Agent lessons:** the project's `.claude/agents/`, or `~/.claude/agents/` for the ones you promoted.
- **The case study:** `.claude/directing-agent-teams/implementations/<project>.md`, or the same path under `~/.claude/`.
- **Rules for the skill:** the "Suggested skill changes" section at the end of the case study. The Director's final report lists them too.

Copy what applies beyond your project into this repository. Leave out anything private to your project, such as client names, paths and credentials.

Keep lessons to what the run showed. If a number is from one run, say so.

## Add an agent type

Add `agents/team-<role>.md` with `name`, `description`, `model`, and `disallowedTools: Agent` unless the role spawns. The body opens with "Read first", then the Contract, then Lessons. Name the new type in `director.md` → "Agent definitions" and in the agent table in `README.md`.

## Docs and diagrams

The pages in `docs/` explain the skill; the skill files are the source of truth. If you change a rule in the skill, update the page that describes it. `docs/architecture/index.md` maps each skill file to its pages.

The diagrams are D2 sources in `docs/diagrams/`, rendered to light and dark SVGs by `docs/diagrams/render.sh`. Edit the `.d2` file, re-render, and commit both SVGs. Read `docs/diagrams/CLAUDE.md` first.

## Before you open a pull request

```bash
python3 scripts/check_configs.py
python3 -m unittest discover -s tests -v
claude plugin validate . --strict
```

To try your change in a session without installing it:

```bash
claude --plugin-dir .
```
