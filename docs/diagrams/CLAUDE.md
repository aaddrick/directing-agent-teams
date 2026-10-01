# Working on the diagrams

Read this before editing anything in `docs/diagrams/`. The rules here were learned on ticketmill's diagrams, which use the same themes and render script.

## What lives here

| File | Role |
| --- | --- |
| `theme-light.d2`, `theme-dark.d2` | Palette and class definitions. No nodes, no edges. |
| `team-structure.d2` | Who talks to whom. Embedded in `docs/architecture/overview.md`. |
| `run-lifecycle.d2` | Launch to report. Embedded in `docs/architecture/run-lifecycle.md`. |
| `slice-loop.d2` | One builder and its verifier. Embedded in `docs/architecture/slices-and-qa.md`. |
| `learning.d2` | Project to user to upstream. Embedded in `docs/architecture/learning.md`. |
| `render.sh` | Regenerates every SVG. The only supported way to produce them. |
| `*-light.svg`, `*-dark.svg` | **Generated.** Never hand-edit. |

Diagram bodies contain **no colors**. They reference class names only. All color lives in the two theme files.

## Requirements

[D2](https://d2lang.com) v0.7.x on PATH, or pointed at with `D2`:

```bash
D2=/path/to/d2 ./render.sh
```

The generated SVGs are committed, so nobody needs d2 to read the docs, only to change them.

## How to make a change

1. Edit the `.d2` body, or a theme file.
2. Run `./render.sh`. It writes both the light and the dark SVG for every diagram. Always commit the pair.
3. Look at the result at the width it will be viewed at (see "Verifying"). Compiling isn't verifying.
4. If you added or removed a diagram, update the `<picture>` blocks in the page that embeds it, and the table above.
5. If you changed what a class means, update the legend in `docs/architecture/overview.md`. The legend and the theme files are a contract.

`render.sh` builds each diagram by concatenating a theme file and a body into a temp file. That's why bodies must not declare their own `vars` or `classes`.

## Class vocabulary

Both theme files must define exactly the same class names. A class only one theme defines falls back to d2's defaults in the other mode, silently.

| Class | Means here |
| --- | --- |
| `stage` | An ordinary agent or step |
| `gate` | A gate or decision point: work is held until it passes |
| `optional` | Used only when the project needs it (dashed border) |
| `terminal` | Where results land: a record or an end state |
| `human` | A place where the user is required |
| `phase` | A container or grouping box |
| `flow` | A normal forward edge |
| `loop` | A loop, read-back or fix round (dashed amber) |

## Rules

- **Comments are `#`, not `//`.** d2 parses `//` lines as shapes.
- **Never use `|md|` blocks.** They render as `foreignObject`, which breaks when GitHub embeds the SVG through `<img>`. Use quoted labels with `\n`. Check with `grep -c foreignObject *.svg`; every count must be 0.
- **Two themes, because d2 inlines custom fills.** One SVG can't carry both palettes, so each page pairs them in a `<picture>` element.
- **Keep the canvas transparent.** Both themes set `style.fill: transparent`; without it the dark SVG sits on a white slab.
- **Chains in a grid, branches on dagre.** `run-lifecycle` and `learning` are chains, drawn as grid snakes: row 1 left to right, down the last column, row 2 back right to left. `slice-loop` branches, so it stays on dagre. `team-structure` is a grid whose fan-out is one container cell.
- **The diagonal rule.** A grid edge is straight only between neighbours in the same row or column. Anything else is a diagonal, and an edge spanning two cells draws through the cell between them. Place nodes to suit the edges.
- **Declaration order is placement.** Cells fill row-major in the order they're declared. For a snake, declare row 2 so the cell under the last column comes last. Declare `grid-rows` before `grid-columns`.
- **Spacer cells (`sp*`) are load-bearing.** Deleting one reflows the grid.
- **Column width is shared.** One wide cell widens its whole column.
- **Two-cycles get one `<->` connector** with a combined, short, multi-line label. Two separate edges stack their labels on top of each other.

## Size budget

The SVGs scale to their container, and GitHub's Markdown column is about 1012px wide. Aim for a natural width near 1012px and a height under about 550px. Much wider shrinks the text; much narrower blows the boxes up. Check after every edit:

```bash
for f in *-light.svg; do
  printf "%-30s " "$f"; grep -o 'viewBox="[^"]*"' "$f" | head -1
done
```

## Verifying

Render at real width and look at it, in both themes:

```bash
cat > /tmp/preview.html <<HTML
<html><body style="margin:0;background:#fff">
<div style="max-width:1012px;margin:0 auto">
  <img src="file://$PWD/slice-loop-light.svg" style="max-width:100%">
</div></body></html>
HTML
google-chrome --headless --disable-gpu --screenshot=/tmp/preview.png \
  --window-size=1030,700 --hide-scrollbars file:///tmp/preview.html
```

Swap the background to `#0d1117` and the suffix to `-dark` for dark mode. Use a browser; `inkscape` and `rsvg-convert` don't show what GitHub shows.
