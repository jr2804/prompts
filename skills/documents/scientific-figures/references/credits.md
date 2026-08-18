# Credits

This skill is a fresh reimplementation built on inspiration from several open-source sources. It does not copy any of them verbatim — the structure, the scripts, and the references were rewritten for this repository's conventions (`uv run`-everywhere, PEP 723 inline deps, agent-neutral voice, SVG-first exports, xy-as-the-preferred-default). Where we retained specific design choices, we list them here so the line of credit is clear.

## Reference skills consulted

All four sources were fetched and studied, but no code, table, or text was lifted wholesale. The script structure (`style_presets.py`, `color_palettes.py`, `export_figure.py`, `figure_size.py`) and the references/ layout were re-implemented from scratch against the needs surfaced in our own design session.

### 1. [davila7/scientific-visualization](https://github.com/davila7/claude-code-templates/tree/main/cli-tool/components/skills/scientific/scientific-visualization)

The closest analog. It informed the journal presets (`nature`, `science`, `plos`, `ieee`, `poster`), the use of Okabe-Ito as the default categorical palette, the style-file approach, and the journal requirements table. What we changed:

- **No PEP 723 metadata** in their scripts; we made every script self-contained under `uv run`.
- **No `colorblind_check.py`** in theirs; we added it and wired the same Machado 2009 matrices the broader viz community uses.
- **No `accessibility_check.py`** in theirs; we added the file-size + clipping + CVD-summary pass.
- **No `figure_size.py`** in theirs; we added column-target → inches arithmetic.
- **No SVG export reasoning**; we made SVG the canonical default and explained when PDF/PNG is appropriate.
- **xy not first-class**; we made `xy` the preferred default with matplotlib as a documented drop-in.
- **`style_presets.py`** in the upstream skill duplicated values across two helper functions; we consolidated to a single `PRESETS` dict.
- The upstream `.mplstyle` files include a `prop_cycle: cycler(...)` line that matplotlib silently rejects on `plt.style.use()`. We kept the same content but moved the prop-cycle install into `apply_style()` (the Python helper) and documented the limitation in `SKILL.md`.

### 2. [davila7/matplotlib](https://github.com/davila7/claude-code-templates/tree/main/cli-tool/components/skills/scientific/matplotlib)

A pure-matplotlib teaching resource. It informed the api-reference style (`references/figure-types.md` follows its `api_reference.md` pattern) and the troubleshooting mindset. We did not keep its `plot_template.py` (a 200-line argparser-driven demo) because our `figure_demo.py` and `references/figure-types.md` cover the same surface with less code.

### 3. [davila7/plotly](https://github.com/davila7/claude-code-templates/tree/main/cli-tool/components/skills/scientific/plotly)

A plotly-specific reference. We did not adopt any of its structure — plotly is presented in this skill as a special-case library, not a default — but we credit it as the source for thinking through chart-type organization.

### 4. [lingzhi227/figure-generation](https://github.com/lingzhi227/agent-research-skills/tree/main/skills/figure-generation)

A pipeline-oriented skill built around query expansion → code generation → VLM feedback. Two ideas we kept:

- The "no title in the figure; caption belongs in the manuscript" rule (we surface it as a hard rule in `SKILL.md` and expand on it in `references/mistakes.md`).
- The three-phase pipeline (spec → render → verify) is reflected in our workflow steps 1–6 in `SKILL.md`.

We did not adopt its MatPlotAgent-style self-prompting recipe; that's an agent-level workflow, not a skill-level convention. It also uses `python ~/.claude/skills/...` paths, which we deliberately replaced with `uv run scripts/...`.

## Palette, colormap, and accessibility citations

These are the academic sources cited inline from `references/color-and-accessibility.md` and `scripts/color_palettes.py`:

### Okabe-Ito (2008)

Okabe, M., & Ito, K. (2008). *Color Universal Design — using a series of distinguishable colors for the graphical representation of categorical data.* The de facto categorical palette for colorblind-safe scientific plots. We use their full 8-color set as the default.

### Wong (2011)

Wong, B. (2011). *Points of view: Color blindness.* Nature Methods, 8(6), 441. Re-ordered Okabe-Ito hues, often cited as Nature Portfolio's house style. We ship the same hues (the reordering is minor) under the name `wong` for users submitting to Nature titles.

### Paul Tol palettes

Tol, P. (2021 and ongoing). *Colour schemes.* <https://personal.sron.nl/~pault/>. We include the `tol_bright` (7 colors, projector-friendly), `tol_muted` (9 colors, grayscale-safe), and a `tol_diverging` subset.

### Machado, Oliveira & Fernandes (2009)

Machado, G. M., Oliveira, M. M., & Fernandes, L. A. F. (2009). *A physiologically-based model for simulation of color vision deficiency.* IEEE TVCG, 15(6), 1291–1298. The CVD simulation matrices in `scripts/colorblind_check.py` are the severity-1.0 reductions commonly cited from this paper. Values are approximations, not colorimetric ground truth.

### Borland & Taylor (2007) and rainbow/`jet` discussion

Borland, D., & Taylor, R. M. (2007). *Rainbow color map (still) considered harmful.* IEEE VIS. Cited in `references/color-and-accessibility.md` and `references/mistakes.md` as the canonical argument against `jet` and other rainbow colormaps.

### Colormaps cited by name

`viridis`, `plasma`, `cividis`, `magma`, `inferno`, `RdBu`, `coolwarm` are matplotlib built-ins. Their perceptual-uniformity properties were established by various authors; the matplotlib documentation links the relevant papers at <https://matplotlib.org/stable/users/explain/colors/colormaps.html>.

## Emerging libraries

### reflex-xy

[reflex-dev/xy](https://github.com/reflex-dev/xy) (alpha). We promote it as the preferred default for new projects because of its `xy.pyplot` matplotlib-compatible namespace and its ability to render 10⁹ points interactively via the Rust core. The `references/xy.md` quick-start links upstream's [matplotlib compatibility guide](https://github.com/reflex-dev/xy/blob/main/spec/matplotlib/compat.md).

### Other mentions

- [marimo](https://marimo.io) — reactive notebook; mentioned in `references/xy.md` as a companion to xy/plotly.
- [ggmosaic](https://github.com/has2k1/plotnine) (plotnine / ggplot for Python) — mentioned as a grammar-of-graphics alternative.
- [altair](https://altair-viz.github.io/) — declarative Vega-Lite binding; mentioned for small interactive web figures.
- [colour-science](https://github.com/colour-science/colour) — the strict CVD-simulation fallback; mentioned in `references/color-and-accessibility.md` as the upgrade path for `scripts/colorblind_check.py`.

## Tools and infrastructure

This skill would not exist without:

- **[uv](https://docs.astral.sh/uv/)** — for PEP 723 script metadata and dependency resolution.
- **[matplotlib](https://matplotlib.org/)** — the default plotting library, and the API surface that `xy` mirrors.
- **[Pillow](https://pillow.readthedocs.io/)** — used by `scripts/colorblind_check.py` (palette quantization) and `scripts/accessibility_check.py` (pixel statistics).
- **[NumPy](https://numpy.org/)** — used by every script that produces or analyzes image data.

## This repository

The skill follows the conventions documented in `../../AGENTS.md` and `../SKILL.md` for sibling skills in this repo:

- PEP 723 inline metadata for every script.
- `uv run`-only execution; no assumption of pre-installed Python packages.
- agent-neutral wording (no vendor names).
- `references/` and `assets/` subfolders for materials.

The DOX-chain owners of this skill are listed in the repository's `AGENTS.md` hierarchy.

If you spot an attribution that's missing or wrong, please open an issue against this repo and we'll update this file.
