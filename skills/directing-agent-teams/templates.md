# Templates

## PLAN_<project>.md skeleton
```markdown
# Plan: <project>
> Status (<date>): not started. A Director agent runs this plan. Read this, then <project docs>.

## Goal
<one paragraph, plus the base inputs: paths and what is fixed>

## References and tone
<align/reference/* with a one-line description of each; the tone/era in the user's words; identity requirements vs features to decide after the shape gate>

## Deliverables
All in <new output dir>/. Nothing outside it is overwritten.
1. ...  (plus: QA_REPORT.md, BOARD.md, a README section)

## Work items
| # | Item | Workstream | core / cuttable | Notes |

## Organization
Director → leads (the files each one owns) → at most 2 workers each; QA lead (never edits product code).
At most 6 agents active. A contrarian critiques the plan or storyboard before it's final.

## Ground rules
Every agent follows `rules.md` (directing-agent-teams skill), covering communication, locks, files, scope and handoff. Project values:
- Scarce resources and lock files: <e.g. .gpu.lock (GPU), .sim.lock (CPU/RAM)>; acquisition order: <sim before GPU>
- Preview definition: <length / resolution / samples / max minutes>; full scale: <definition>, only at <gates>, <N> per item per gate attempt
- Preconditions for full runs: <AC power, free disk ≥ X GB>
- Budgets: <RAM per process, disk, CPU workers>
- Never modify: <vendored dirs>; never overwrite: <existing outputs>; backups: <git / manual>
- M0 proof: <invariant: identical to old pipeline | fixed inputs hashed + deterministic builds>

## Milestones
- M0 interface, shared data, timeline; identity proof; direction alignment gate (preview array → pick); QA
- M1 each piece on its own preview; QA
- (alignment gate before any expensive run: preview array → pick)
- M2 integrated full run, which must match the chosen preview; QA; fixes looped on previews
- M3 finish, final QA, README, report

## Adversarial QA
<numeric checks per item>, regressions, legibility / taste reviewer, technical specs. Evidence in qa/.
After 3 failed rounds, the Director decides: cut, or accept with a known issue.

## Done
Final report: shipped, cut, verdicts, provisional/unverified items, decisions, downloads and licences, resource total, repro commands.
```

## BOARD.md skeleton
```markdown
## Roster
| Role | Agent ID | Spawned by | Gen | Status (active / handing-off / done) | Handoff file |
|---|---|---|---|---|---|
| Director | <id> | main | 1 | active | handoff/director.md |

## Ownership
| Path | Owner role |
|---|---|

## Inbox
### <role>
- <time> from <sender>: <pointer, e.g. "FAIL, see qa/m1_ws2.md"> (undelivered)

## Status
### <workstream> ...
## Resource log
## Decisions
- D1 (<time>): <decision>, because <reason>
```

## Slice card (on BOARD → Status, under the owner's section)
```markdown
- SLICE <ws>-<n> [open|pass|fail|partial] owner=<role> box=<min> started=<date>
  goal: <one component or question>
  test: <numeric acceptance, e.g. min clearance >= 2 cm over the full range>
  artefact: <path to still / <=5 s clip / table>
  result: <PASS|FAIL + evidence path>  next: <one line>
```

## handoff/main.md skeleton
```markdown
# Handoff: main session -> next session (<date>)
## How to restart   (load the skill; read handoff/director.md; spawn a NEW Director; never message old IDs)
## Project in one paragraph
## The user's decisions that shape everything (D-numbers)
## Pending questions for the user   (path + recommendation for each)
## Working with this user   (pace, how picks are presented, where images go, what they catch)
## Agents and implementation notes changed this session   (.claude/agents/, .claude/directing-agent-teams/implementations/; a /directing-agent-teams:promote line for each worth keeping)
## Suggested skill changes   (for upstream; never edit the plugin's files)
```

## handoff/<role>.md skeleton
```markdown
# Handoff: <role>, gen <N> → <N+1>  (<time>)
- Owns: <files>
- Milestone: <M#>, state: <one paragraph>
- Next step: <exact next action>
- Relies on decisions: D3, D7
- Live workers: <agent ID> doing <task>, writing output to <path>
- Open QA findings: qa/<file>
- Waiting on: <who, for what>
- Gotchas learned: <short bullets>
```

## Director prompt
```
You are the Director for a multi-agent project in <dir>. Read, in order:
1. <skill dir>/director.md (your guide)
2. PLAN_<project>.md
3. <project docs>
Then run the plan to completion. You coordinate; you write no product code.

- BOARD.md exists. The main session adds your Roster row right after spawning you; if it's missing, add it. Design the team from the work (examples.md holds shapes, not templates)
  and record it in the plan's Organization section. Spawn a contrarian on the plan or storyboard.
- Spawn with the plugin's agent types (directing-agent-teams:team-builder, :team-verifier, :team-taste-reviewer,
  :contrarian, and the specialists), or a copy in .claude/agents/ or ~/.claude/agents/ by its bare name when one exists; they carry
  the role contract, the default model and the Lessons. Pass model: "opus" only where a slice needs it.
- Every agent you spawn gets "Read <skill dir>/rules.md, then PLAN_<project>.md and BOARD.md", plus its role,
  its owned paths and its task. QA agents also read <skill dir>/qa.md. Write each spawned agent's ID into
  the Roster immediately.
- Run alignment gates before long-lead items; hold the gates; keep the agent cap; record every decision as a D-number.
- The user may be offline: follow director.md → "Offline decisions".
- Your handoff goes to the main session (context-turnover.md).
- References: align/reference/ (every design option must descend from them). Identity vs later features: <list>.
- Defaults for open questions: <list>.
- When done, return the final report described in director.md. Report faithfully.
```
