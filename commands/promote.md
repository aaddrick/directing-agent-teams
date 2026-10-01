---
description: Move a team agent or an implementation case from this project to your user folder, so every directing-agent-teams project uses it.
argument-hint: "[agent-or-case-name]"
allowed-tools: Read, Write, Edit, Bash(ls:*), Bash(diff:*), Bash(date:*), Bash(cp:*), Bash(rm:*), Bash(rmdir:*), Bash(mkdir:*), Bash(grep:*)
---

Promote a project file to user level. The name to promote: $ARGUMENTS

A directing-agent-teams Director keeps its changes in the project, and each kind has a user-level home where every project finds it:

| Kind | Project path | User path |
|---|---|---|
| agent | `.claude/agents/<name>.md` | `~/.claude/agents/<name>.md` |
| case | `.claude/directing-agent-teams/implementations/<name>.md` | `~/.claude/directing-agent-teams/implementations/<name>.md` |

A project agent wins over a user agent with the same name, and a project case would be read twice, so this is a move, not a copy.

1. **Pick the file.** If no name was given, list both project folders. For each file show its kind, its Lessons count for an agent or its run sections for a case, and whether the user path already exists. Ask which to promote, and stop if both folders are empty. Accept a name with or without `.md` and with or without a `directing-agent-teams:` prefix. If the name exists in both project folders, ask which one.
2. **Read both sides.** Read the project file in full. If the user path exists, read it too and run `diff` on the two.
3. **No user copy yet:** create the user folder with `mkdir -p`, then copy the project file there unchanged.
4. **A user copy exists:** merge rather than overwrite.
   - Back up the user copy to `<user path>.bak_<date>`, with the date from `date +%F`.
   - **Agent:** keep every Lessons line the user copy has, in its order, then append the project's Lessons it lacks. Treat lines as the same only when their text matches after trimming.
   - **Case:** keep the user copy's sections in order. Add each "Lessons learned" section from the project that the user copy lacks, matched by heading, after the user copy's last run and before "Suggested skill changes", which stays last. For a section with the same heading and different text, append the project's lines that the user copy lacks.
   - When two lines say the same thing in different words, keep both and list them for the user.
   - **Everything else** (an agent's frontmatter and contract, a case's "Best execution"): if it differs, show the user the diff and ask which side to keep, or whether to keep both changes. Don't choose for them.
   - Write the merged file to the user path.
5. **Remove the project copy** only after reading back the user copy and confirming it contains every line of the project copy, or the version the user chose for the parts that differed. Then delete the project file, and remove each folder that leaves empty, up to but not including `.claude/` (`rmdir` only removes empty ones).
6. **Report** in a few lines: the path written, what was added, any near-duplicates, and the backup path if there was one. Then, for an agent:
   - Every project's Director now spawns it by its bare name (`<name>`). If it's one of the plugin's own types, that replaces `directing-agent-teams:<name>`.
   - A user copy of a plugin type no longer gets the plugin's updates to it. To go back to the plugin's version, delete the user copy.
   - A running Director may take a few minutes to see the change.

   For a case: the main session and the Director will now find it when a new project looks similar. If it has "Suggested skill changes", say that they only take effect once sent upstream as a pull request.
