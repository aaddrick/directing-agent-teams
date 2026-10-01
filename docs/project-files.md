# Project files

A run keeps its state in files in the project directory, not in any agent's context. Messages between agents are pointers to these files. That's what lets an agent die, or be replaced, without losing work.

## Layout

```text
<project>/
├── PLAN_<project>.md          the plan: goal, deliverables, team, seams, milestones
├── BOARD.md                   the live board: Roster, Ownership, Inbox, Status, Decisions
├── QA_REPORT.md               verdict per item, worst remaining issue, rounds
├── align/
│   ├── reference/             your reference images, described in words
│   └── <item>/index.md        a contact sheet of options A–H
├── qa/
│   ├── slices/<slice-id>/     a verifier's verdict.md and evidence
│   ├── taste/<slice-id>.md    a taste reviewer's read
│   └── tools/                 verifiers' measuring tools, shared read-only with builders
├── findings/<owner-role>/     out-of-scope findings, addressed to the owner
├── notes/<ws>.md              a lead's methods, key numbers and paths, at each gate
├── handoff/
│   ├── main.md                main session → next session
│   ├── director.md            Director → next Director
│   ├── BOARD.snapshot.md      the Director's copy of BOARD after each of its edits
│   └── <role>.md              each lead's current state
├── .board.lock                taken for every read-modify-write of BOARD.md
├── .<res>.lock                one lock per scarce resource (e.g. .gpu.lock)
├── .<res>.lock.owner          who holds it, PID, expected end
└── .claude/
    ├── agents/                this project's agent copies and new types
    └── directing-agent-teams/
        └── implementations/<project>.md   this project's case study
```

The skeletons for the plan, the BOARD, slice cards and handoff files are in the skill's [`templates.md`](../skills/directing-agent-teams/templates.md).

## PLAN_<project>.md

Written by the main session before launch, then owned by the Director. It holds the goal and fixed inputs, references and tone in your words, deliverables, work items marked core or cuttable, the team (Organization), the project's ground-rule values (lock names and order, what counts as a preview, budgets, what never to touch), milestones, and the QA plan.

## BOARD.md

The one place everyone reads. Its sections:

| Section | Holds | Written by |
|---|---|---|
| Roster | role, agent ID, spawned by, generation, status, handoff file | whoever spawns an agent, at once |
| Ownership | every path the work touches and its owner role | the Director |
| Inbox | messages for a role that couldn't be delivered | any sender; cleared only by the role's owner |
| Status | a line per workstream, and slice cards | each role, with the time from `date` |
| Resource log | one line per job on a scarce resource | whoever runs the job |
| Decisions | D-numbers: your words and the Director's calls, with reasons | the Director |

**Edit BOARD in place, under its lock.** Every agent writes to it, and concurrent writes once erased whole sections. Agents change only their own section or row, with the Edit tool or a read-modify-write under `flock .board.lock`, and never rewrite the whole file. The Director snapshots it to `handoff/BOARD.snapshot.md` after its own edits. See [`rules.md`](../skills/directing-agent-teams/rules.md) → Editing BOARD.md.

**The Roster is the only directory.** Subagents have no way to list agents, so an agent that isn't in the Roster can't be reached.

## Slice cards

A slice card lives on BOARD under its owner's Status section:

```markdown
- SLICE <ws>-<n> [open|pass|fail|partial] owner=<role> box=<min> started=<date>
  goal: <one component or question>
  test: <numeric acceptance, e.g. min clearance >= 2 cm over the full range>
  artefact: <path to still / <=5 s clip / table>
  result: <PASS|FAIL + evidence path>  next: <one line>
```

The Director also lists the neighbouring requirements that must still hold, so a fix to one thing doesn't quietly break the one next to it.

## Handoff files

Every lead keeps `handoff/<role>.md` current at every milestone step and before any long wait: files owned, milestone state and next step, D-numbers relied on, live workers (ID, task, output path), open QA findings, what it's waiting on, and gotchas. A replacement is spawned with only the plan, BOARD and this file. See [Context and turnover](architecture/context-and-turnover.md).

## Should these go in git?

That's up to you. The files are plain Markdown and small. Committing `PLAN_*.md`, `BOARD.md`, `QA_REPORT.md` and `handoff/` gives you a history of the run. Lock files and their owner files are live state; leave them out.
