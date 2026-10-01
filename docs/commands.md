# Commands

The plugin has one command. The skill itself loads on its own, or by hand with `/directing-agent-teams:directing-agent-teams`.

## `/directing-agent-teams:promote [name]`

Moves an agent or a case study the Director wrote in this project to your user folder, so every future project uses it. Run it from the project directory.

| Kind | From (project) | To (user) |
|---|---|---|
| Agent | `.claude/agents/<name>.md` | `~/.claude/agents/<name>.md` |
| Case study | `.claude/directing-agent-teams/implementations/<name>.md` | `~/.claude/directing-agent-teams/implementations/<name>.md` |

It's a move, not a copy. A project agent wins over a user agent with the same name, so leaving the project copy behind would hide the promoted one in this project.

**With no name,** it lists both project folders with each file's kind, its Lessons or run count, and whether you already have a user copy, then asks which one.

**Names** are accepted with or without `.md` and with or without the `directing-agent-teams:` prefix. If the name exists in both folders, it asks which one you mean.

### When you already have a user copy

It merges instead of overwriting:

1. It backs up your copy to `<file>.bak_<date>`.
2. **Agents:** it keeps your Lessons in their order and adds the project's Lessons you don't have. Lines count as the same only when the text matches exactly after trimming.
3. **Case studies:** it keeps your sections in order and adds each `Lessons learned (run of <date>)` section you don't have, before "Suggested skill changes", which stays last.
4. Two lines that say the same thing in different words both stay, and it lists them so you can delete one.
5. If an agent's frontmatter or contract, or a case's "Best execution", differs, it shows you the diff and asks. It never picks for you.

It deletes the project copy only after reading the user copy back and confirming nothing was lost, then removes any folder that leaves empty.

### After promoting

- The Director spawns the agent by its bare name (`team-verifier`) in every project, instead of the plugin's `directing-agent-teams:team-verifier`.
- A user copy of one of the plugin's agents no longer gets the plugin's updates to that agent. To go back, delete your copy.
- A Director that's running may take a few minutes to see the change.
- "Suggested skill changes" in a case study only take effect once they're sent upstream as a pull request. See [CONTRIBUTING](../CONTRIBUTING.md).

See [How the team learns](architecture/learning.md) for the full picture.
