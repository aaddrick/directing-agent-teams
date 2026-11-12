# Templates

## PLAN_<project>.md skeleton
```markdown
# Plan: <project>
> Status (<date>): not started. A Director agent runs this plan. Read this, then <project docs>.

## Goal
<one paragraph, plus the base inputs: paths and what is fixed>

## References and tone
<align/reference/* with a one-line description of each; the tone/era in the user's words; identity requirements vs features to decide after the shape gate>

## Budget and stop line
Tokens: <budget>. Stop at: <end time, or "after M<n>">. Tokens per agent go in the Roster when it ends.

## User-only choices (asked before launch)
| Choice | User's answer, or PROVISIONAL default + cheap swap |

## Deliverables
All in <new output dir>/. Nothing outside it is overwritten.
1. ...  (plus: QA_REPORT.md, BOARD.md, a README section)

## Work items (in the order the user named them; built in this order)
| # | Item | Workstream | core / cuttable | Risk (high / normal / low) | Notes |

## Deciding rows (frozen when building starts; new asks become new slices)
### <item #>
1. <what the end user meets, measurable>   (script: qa/tools/<check> | human check)
2. ...  (3–5 rows per item)

## Human checks
| Milestone | What the user tries (~15 min) | What it settles |

## Backlog
Defects found along the way that aren't high risk: <item, evidence path>.

## Organization
Director → leads (the files each one owns) → at most 2 workers each; QA lead (never edits product code).
At most 6 agents active; parallel lanes ≤ scarcest resource's slots + 1. A contrarian critiques the plan or storyboard before it's final.
| Role | Model | Why (required for any Opus override) |

## Ground rules
Every agent follows `rules.md` (directing-agent-teams skill), covering communication, locks, files, scope and handoff. Project values:
- Scarce resources and lock files: <e.g. .gpu.lock (GPU), .sim.lock (CPU/RAM)>; acquisition order: <sim before GPU>
- Preview definition: <length / resolution / samples / max minutes>; full scale: <definition>, only at <gates>, <N> per item per gate attempt
- Preconditions for full runs: <AC power, free disk ≥ X GB>
- Budgets: <RAM per process, disk, CPU workers>
- Never modify: <vendored dirs>; never overwrite: <existing outputs>; backups: <git / manual>
- M0 proof: <invariant: identical to old pipeline | fixed inputs hashed + deterministic builds>; identity tested only on paths that repeat exactly, else tolerance <x>
- User data: never touch <user's save/config/log dirs>; tests use <own data dir>; <separate copy + "in use" watcher, if the user uses the product during the run>
- Committed checks: qa/tools/<check> (pass/fail exit, planted failing case beside it)

## Milestones
- M0 interface, shared data, timeline; identity proof; direction alignment gate (preview array → pick); QA
- M1 each piece on its own preview; QA
- (alignment gate before any expensive run: preview array → pick)
- M2 integrated full run, which must match the chosen preview; QA; fixes looped on previews
- M3 finish, final QA from a clean export running the docs' commands as written, README, report
- Every milestone: its human check row

## Adversarial QA
<numeric checks per item>, regressions, legibility / taste reviewer, technical specs. Evidence in qa/.
Verification by risk tier: high = 2 verifiers + planted failures; normal = 1 verifier; low = self-test + Director look.
After 3 failed rounds, the Director decides: cut, or accept with a known issue.

## Done
Final report: shipped, cut, verdicts, provisional/unverified items, decisions, downloads and licences, resource total, repro commands.
```

## BOARD.md skeleton
```markdown
## Roster
| Role | Agent ID | Spawned by | Gen | Model | Status (active / handing-off / done) | Handoff file | Tokens (at end) |
|---|---|---|---|---|---|---|---|
| Director | <id> | main | 1 | <model> | active | handoff/director.md | |

## Ownership
| Path | Owner role |
|---|---|

## Inbox
### <role>
- <time> from <sender>: <pointer, e.g. "FAIL, see qa/m1_ws2.md"> (undelivered)

## Status
### <workstream> ...
## Resource log
## Decisions (what stands now; delete superseded lines, or move them to handoff/archive/)
| D# | Decided (<time>) | Because | Replaces |
|---|---|---|---|
| D1 | <decision> | <reason> | |
```

## Slice card (on BOARD → Status, under the owner's section)
```markdown
- SLICE <ws>-<n> [open|pass|fail|partial] owner=<role> box=<min> risk=<high|normal|low> started=<date>
  goal: <one component or question>
  test: <numeric acceptance, e.g. min clearance >= 2 cm over the full range; the plan's deciding row it serves>
  checks: <qa/tools/ scripts to run>  re-gate: <rows this change can touch>
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
Current state only, about a page. Rewrite it; don't append. History goes to `handoff/archive/` and is referenced by path.
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
- Budget: <tokens>; stop line: <time or milestone>. Record each agent's tokens in the Roster when it ends.
- Build the work items in the plan's order. Deciding rows are frozen; new asks become new slices, and
  non-high-risk defects go to the Backlog. Verify by each slice's risk tier.
- Keep handoff/director.md and BOARD → Decisions as current state, about a page each. Rotate yourself by
  context size or after about 90 minutes of busy relaying.
- When done, return the final report described in director.md. Report faithfully.
```
