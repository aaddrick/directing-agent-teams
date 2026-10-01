#!/usr/bin/env python3
"""Check the manifests, the skill and the agents. Exit 1 on any failure.

- Both JSON manifests parse, and the marketplace lists the plugin by its own name.
- SKILL.md has frontmatter with `name` and `description`, and the name matches its folder.
- Every file the skill names in backticks (`rules.md`, `implementations/...`) exists.
- Every agent has `name` and `description`, its name matches its file, and its model is a known alias.
- Every `team-<role>` agent the skill or the agents name ships in `agents/`.
- Every command has a description.
- No shipped file points at a machine-local skill path or is a leftover backup.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "directing-agent-teams"
AGENT_DIR = ROOT / "agents"
MODELS = {"opus", "sonnet", "haiku", "inherit"}
SKILL_REF = re.compile(r"`((?:implementations/)?[\w.-]+\.md)`")
# Project files the skill tells agents to create; they are not shipped.
PROJECT_FILES = {"BOARD.md", "QA_REPORT.md", "README.md", "questions.md"}
AGENT_REF = re.compile(r"\bteam-[a-z]+(?:-[a-z]+)*\b(?![<\w-])")
LOCAL_PATH = re.compile(r"~/\.claude/skills/")

errors: list[str] = []


def frontmatter(path: Path) -> dict[str, str] | None:
    match = re.match(r"^---\n(.*?)\n---\n", path.read_text(encoding="utf-8"), re.S)
    if not match:
        return None
    fields = {}
    for line in match.group(1).splitlines():
        if re.match(r"^\w", line) and ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    fields["__raw__"] = match.group(1)
    return fields


manifests = {}
for rel in (".claude-plugin/plugin.json", ".claude-plugin/marketplace.json"):
    try:
        manifests[rel] = json.loads((ROOT / rel).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{rel}: {exc}")

plugin, market = manifests.get(".claude-plugin/plugin.json"), manifests.get(".claude-plugin/marketplace.json")
if plugin and market:
    if plugin["name"] not in {p["name"] for p in market.get("plugins", [])}:
        errors.append("marketplace.json does not list the plugin by the name in plugin.json")
    if plugin["name"] != SKILL_DIR.name:
        errors.append("plugin name and skill folder differ")

fm = frontmatter(SKILL_DIR / "SKILL.md")
if fm is None:
    errors.append("SKILL.md: no frontmatter")
else:
    keys = [k for k in fm if k != "__raw__"]
    if keys != ["name", "description"]:
        errors.append(f"SKILL.md: frontmatter keys must be name, description; found {keys}")
    if fm.get("name") != SKILL_DIR.name:
        errors.append("SKILL.md: name does not match its folder")
    if len(fm["__raw__"]) > 1024:
        errors.append("SKILL.md: frontmatter is over 1024 characters")

for md in SKILL_DIR.rglob("*.md"):
    for ref in SKILL_REF.findall(md.read_text(encoding="utf-8")):
        if ref in PROJECT_FILES or "<" in ref:
            continue
        if not any((base / ref).exists() for base in (md.parent, SKILL_DIR, SKILL_DIR / "implementations")):
            errors.append(f"{md.relative_to(ROOT)}: names `{ref}`, which does not exist")

shipped = set()
for path in sorted(AGENT_DIR.glob("*.md")):
    fm = frontmatter(path)
    if fm is None:
        errors.append(f"{path.relative_to(ROOT)}: no frontmatter")
        continue
    shipped.add(fm.get("name", ""))
    if fm.get("name") != path.stem:
        errors.append(f"{path.relative_to(ROOT)}: name does not match its file")
    if not fm.get("description"):
        errors.append(f"{path.relative_to(ROOT)}: no description")
    if "model" in fm and fm["model"] not in MODELS:
        errors.append(f"{path.relative_to(ROOT)}: unknown model {fm['model']!r}")

for path in sorted((ROOT / "commands").glob("*.md")):
    fm = frontmatter(path)
    if fm is None or not fm.get("description"):
        errors.append(f"{path.relative_to(ROOT)}: no description in frontmatter")

for path in [*SKILL_DIR.rglob("*.md"), *AGENT_DIR.glob("*.md")]:
    text = path.read_text(encoding="utf-8")
    for name in set(AGENT_REF.findall(text)) - shipped:
        errors.append(f"{path.relative_to(ROOT)}: names agent {name}, which does not ship in agents/")
    if LOCAL_PATH.search(text):
        errors.append(f"{path.relative_to(ROOT)}: points at ~/.claude/skills/; use <skill dir>")

for path in ROOT.rglob("*.bak*"):
    if ".git" not in path.parts:
        errors.append(f"{path.relative_to(ROOT)}: backup file in the repo")

for e in errors:
    print(f"error: {e}")
print("ok" if not errors else f"{len(errors)} error(s)")
sys.exit(1 if errors else 0)
