# Implementations

Case studies from real runs. The general rules live in the other skill files; these files hold what was specific to one kind of project.

**Readers:** the main session at launch, when the new project resembles a case here, and the Director while designing the team.

**Each file has these parts:**
1. **Best execution:** how the project *should* have run from launch to delivery, written with hindsight as a plan to copy. It covers the launch questions, the team, the gates, the checks and the order.
2. **Lessons learned:** what actually happened, and what each misstep cost. One section per run, headed `Lessons learned (run of <date>)`, newest run last.
3. **Suggested skill changes** (optional, always last): general rules this project taught, each naming the skill file it belongs in. See "General rules" below.

## Where they live
The plugin's own folder is replaced on every plugin update, so nobody writes here. Cases are read from three places, and written to the first:

| Folder | Holds | Written by |
|---|---|---|
| `.claude/directing-agent-teams/implementations/` in the project directory | this project's case, while the project runs | the Director |
| `~/.claude/directing-agent-teams/implementations/` | cases the user kept for every project | `/directing-agent-teams:promote <case>` |
| this folder | cases that ship with the plugin | pull requests upstream |

The Director names the file after the project (`<project>.md`), starts it at M0 with the parts above, and brings it up to date at each gate and at wind-down.

## General rules
When a run teaches something general, don't edit `SKILL.md`, `director.md`, `qa.md`, `rules.md` or `context-turnover.md`: they belong to the plugin. Add the rule to a **Suggested skill changes** section at the end of the case file, naming the file it belongs in, and keep only the case-specific detail in the rest of the case. The Director's final report lists these, so the user can send them upstream.

## Cases that ship with the plugin
| File | Project |
|---|---|
| `blender-mech-advert.md` | A procedural bpy mech (a ~18 m headless guardian): model, rig, self-righting, and a 20 s advert-style showcase render |
