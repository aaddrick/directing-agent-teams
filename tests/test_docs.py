"""The docs' links and diagrams hold together.

A renamed page or a re-rendered diagram breaks a link nobody clicks until a
reader does. These checks cover what a reviewer can't see in a diff.
"""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DIAGRAMS = DOCS / "diagrams"
PAGES = [ROOT / "README.md", ROOT / "CONTRIBUTING.md", *sorted(DOCS.rglob("*.md"))]
LINK = re.compile(r"\]\(([^)\s]+)\)|(?:src|srcset)=\"([^\"]+)\"")


def local_targets(page: Path):
    for match in LINK.finditer(page.read_text(encoding="utf-8")):
        target = match.group(1) or match.group(2)
        if re.match(r"^[a-z]+:", target) or target.startswith("#"):
            continue
        yield target


class DocsTest(unittest.TestCase):
    def test_every_local_link_resolves(self):
        for page in PAGES:
            for target in local_targets(page):
                path = target.split("#", 1)[0]
                with self.subTest(page=str(page.relative_to(ROOT)), link=target):
                    self.assertTrue((page.parent / path).exists(), f"{target} does not exist")

    def test_every_anchor_names_a_heading(self):
        for page in PAGES:
            for target in local_targets(page):
                if "#" not in target:
                    continue
                path, anchor = target.split("#", 1)
                dest = page.parent / path if path else page
                headings = re.findall(r"^#+ (.+)$", dest.read_text(encoding="utf-8"), re.M)
                slugs = {re.sub(r"[^\w\- ]", "", h).strip().lower().replace(" ", "-") for h in headings}
                with self.subTest(page=str(page.relative_to(ROOT)), link=target):
                    self.assertIn(anchor, slugs)

    def test_every_diagram_has_both_renders(self):
        for body in DIAGRAMS.glob("*.d2"):
            if body.name.startswith("theme-"):
                continue
            for mode in ("light", "dark"):
                with self.subTest(diagram=body.stem, mode=mode):
                    self.assertTrue((DIAGRAMS / f"{body.stem}-{mode}.svg").exists())

    def test_every_diagram_is_embedded(self):
        text = "\n".join(p.read_text(encoding="utf-8") for p in [*DOCS.rglob("*.md"), ROOT / "README.md"])
        for body in DIAGRAMS.glob("*.d2"):
            if body.name.startswith("theme-"):
                continue
            with self.subTest(diagram=body.stem):
                self.assertIn(f"{body.stem}-dark.svg", text)
                self.assertIn(f"{body.stem}-light.svg", text)

    def test_no_svg_uses_foreign_object(self):
        for svg in DIAGRAMS.glob("*.svg"):
            with self.subTest(svg=svg.name):
                self.assertNotIn("foreignObject", svg.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
