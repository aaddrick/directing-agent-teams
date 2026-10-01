"""The README's install commands name the plugin the manifests ship.

A rename in plugin.json or marketplace.json that misses the README hands every
new user a command that fails. Nothing else rereads the README.
"""

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ReadmeTest(unittest.TestCase):
    def setUp(self):
        self.readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.plugin = json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))["name"]
        self.market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))["name"]
        self.repo = re.search(r"github\.com/([\w-]+/[\w-]+)",
                              json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))["repository"]).group(1)

    def test_marketplace_add_names_the_repo(self):
        self.assertIn(f"claude plugin marketplace add {self.repo}\n", self.readme)

    def test_install_names_plugin_at_marketplace(self):
        self.assertIn(f"claude plugin install {self.plugin}@{self.market}\n", self.readme)

    def test_every_install_command_matches(self):
        for cmd in re.findall(r"^claude plugin install (\S+)$", self.readme, re.M):
            with self.subTest(cmd=cmd):
                self.assertEqual(f"{self.plugin}@{self.market}", cmd)

    def test_slash_command_matches(self):
        skill = next((ROOT / "skills").iterdir()).name
        self.assertIn(f"/{self.plugin}:{skill}", self.readme)

    def test_every_agent_is_listed(self):
        for path in sorted((ROOT / "agents").glob("*.md")):
            with self.subTest(agent=path.stem):
                self.assertIn(f"`{path.stem}`", self.readme)


if __name__ == "__main__":
    unittest.main()
