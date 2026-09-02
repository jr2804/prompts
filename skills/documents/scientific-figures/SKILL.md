---
name: scientific-figures
description: Create, style, export, and validate publication-quality scientific and technical figures. xy is the preferred default (matplotlib.pyplot-compatible for easy migration); matplotlib/seaborn/plotly also supported. Use when the user asks for a "publication figure", "paper figure", "journal-ready plot", "scientific visualization", "SVG/PDF/TIFF export", "colorblind-safe palette", "multi-panel layout", "error bars / significance markers", or works with figure scripts that import matplotlib, seaborn, plotly, or xy.
---

# Scientific & Technical Figures

## Overview

For new projects, build figures on **`xy.pyplot`** (`import xy.pyplot as plt`). XY is a near-drop-in for the matplotlib object-oriented API, scales to billions of points for the same code, and exports to SVG / PDF / PNG / HTML out of the box. If the project already uses `matplotlib` directly, keep that — the two imports are interchangeable for any code that doesn't depend on matplotlib-only extension APIs. Use the helper scripts in `scripts/` for journal sizing, palette selection, format-correct export, and accessibility checks. Treat every other library (seaborn, plotly, bokeh, altair) as a special-case — they all cost you something in either typographic control, vector fidelity, or reproducibility.

## When to use this skill

- Creating a figure for a paper, thesis, technical report, or grant.
- Re-styling a chart to meet a specific journal's spec (size, DPI, font).
- Picking a colorblind-safe palette or verifying one.
- Exporting one source figure to multiple formats (SVG first, PDF for journal, PNG only when the consumer demands raster).
- Building a multi-panel figure with consistent typography across panels.
- Migrating from pure-matplotlib to xy (or back).

If the user just wants to eyeball a dataframe (`df.plot()` in a notebook), this skill is overkill — use plain matplotlib.

## Workflow

1. Pick the figure type → see `references/figure-types.md` for the canonical recipe per type (line, scatter, bar, heatmap, contour, errorbar, multi-panel, 3D).
2. Pick a sizing target → single column / 1.5 column / double column / poster. Defaults: `figure-size --target single|one5|double|poster`.
3. Pick a color palette → see `references/color-and-accessibility.md`. Validate it: `colorblind-check --palette NAME`.
4. Build the figure with the matplotlib OO API:

   ```python
   fig, ax = plt.subplots(figsize=(3.5, 2.6), constrained_layout=True)
   # ...
   ```

   Apply a base style: `from style_presets import apply_style; apply_style("nature")`.
5. Export: `uv run scripts/export_figure.py demo --out figure1 --formats svg pdf --also png --dpi 300`. SVG is the preferred default; PDF is what most journals actually accept; PNG at 300 DPI is a compatibility fallback for downstream tools that cannot consume SVG.
6. Verify → `accessibility-check --image figure.png` simulates the three common CVD types and reports which colors collapse.

Run every script via `uv run scripts/<name>.py ...` — never assume matplotlib is already installed.

## Hard rules (apply before doing anything else)

- **Object-oriented API.** `fig, ax = plt.subplots(...)`, never `plt.plot` for non-trivial work. Same in matplotlib and xy.
- **Sans-serif at print size.** 7–9 pt for axis labels, 6–8 pt for ticks, ≥8 pt for panel labels (A, B, C).
- **No `jet`.** Use `viridis`, `plasma`, or `cividis` for sequential; `coolwarm` or `RdBu` for diverging.
- **No JPEG for data.** PNG, TIFF, or vector (PDF/EPS/SVG).
- **SVG first, PDF for journal, PNG only as compatibility fallback.** SVG is the most flexible vector format (lossless, browser-renderable, designer-friendly, edit-friendly in Inkscape/Illustrator). PDF is what most journals demand; PDF is also the format that *doesn't* drop nicely into Word/PowerPoint, which is why SVG is the better default for figures that need to flow back into office documents. PNG is bitmap and does not scale — only emit PNG when the consumer can't ingest SVG; if you must, use 300 DPI (not the matplotlib default of 100 or 200).
- **Vector for plots, raster for images.** Plots → SVG → PDF. Photographs/microscopy → TIFF 300–600 DPI.
- **Color = redundant encoding.** Color-blind safety is mandatory; mapping hue + shape or hue + linestyle is the gold standard.
- **No titles inside the figure.** The caption belongs in LaTeX/Word. The figure shows data.
- **Log axes: replace `10ⁿ` with domain values.** Default log ticks show powers of ten (`10²`, `10³`). For domain-specific ranges (audio: 20, 50, 100, 200, 500, 1k, 2k, 5k, 10k, 20k Hz; time: 1 ms, 2 ms, 5 ms, 10 ms …), set manual `tick_values` and `tick_labels` so the axis reads like a professional in that field expects. See `references/figure-types.md` § "Logarithmic axes — tick formatting".
- **Cite, don't show, matplotlib defaults.** Nothing screams "AI-generated" louder than `plt.title("My Plot")`.

## Library guidance

| Library | Use when | Avoid when |
|---|---|---|
| **reflex-xy** (`xy.pyplot`) | **Preferred default for new projects.** Drop-in `matplotlib.pyplot` syntax; scales to 10⁹ points; exports SVG / PDF / PNG / HTML from the same source. | You depend on a matplotlib-only extension API (rare). |
| **matplotlib** (`matplotlib.pyplot`) | Project already uses it; you need a matplotlib-only extension API; you're submitting to a venue with strict EPS/PDF font rules. | New project with no prior commitment — prefer xy. |
| **seaborn** | Quick statistical aggregates (box/violin/pair). Built on matplotlib. | Custom projection or non-statistical figure (use xy/mpl directly). |
| **plotly** | Interactive figures for HTML supplements / dashboards. | Static journal submission (use xy/mpl). |
| **bokeh / altair** | Web apps, declarative grammar fans. | Static publication submission. |

`xy.pyplot` and `matplotlib.pyplot` are interchangeable for the vast majority of plotting code. Pick `xy` for new work and switch the import only when you hit a method xy doesn't yet implement — see the compatibility table in `references/xy.md` for what's covered.

## Resources

### scripts/ (run via `uv run scripts/<name>.py ...`)

- `style_presets.py` — apply named journal/preset styles (`nature`, `science`, `plos`, `ieee`, `poster`).
- `figure_size.py` — compute `(width, height)` in inches for any column target.
- `color_palettes.py` — colorblind-safe palettes (Okabe-Ito, Wong, Tol-bright, Tol-muted).
- `export_figure.py` — save a figure to one or more formats at journal-correct DPI; embeds fonts in PDF.
- `colorblind_check.py` — simulate protan/deutan/tritan CVD on a PNG and report collisions.
- `accessibility_check.py` — font-size, contrast, and palette checks on a finished PNG.
- `figure_demo.py` — one-shot demo that renders + exports a canonical line/scatter/bar/multi-panel example.

### references/

- `color-and-accessibility.md` — palette catalog, CVD types, contrast guidance, colormap selection.
- `figure-types.md` — recipes for line, scatter, bar, heatmap, contour, errorbar, multi-panel, 3D.
- `journal-specs.md` — Nature, Science, PLOS, IEEE, Elsevier size/DPI/font tables.
- `xy.md` — reflex-xy quick-start and `xy.pyplot` matplotlib compatibility notes.
- `mistakes.md` — recurring anti-patterns (titles in figures, default styles, color-only encoding).
- `release-checklist.md` — pre-submission figure QA list.

### assets/

- `style_nature.mplstyle`, `style_science.mplstyle`, `style_plos.mplstyle`, `style_ieee.mplstyle`, `style_poster.mplstyle` — drop-in styles per target venue. Load via `apply_style("nature")` (the Python API), not `plt.style.use(...)` directly — matplotlib's style loader silently ignores `axes.prop_cycle`, so the Python helper is what actually installs the Okabe-Ito palette.

## Verification

Before declaring a figure done, run `uv run scripts/accessibility_check.py <png>` and confirm:

- No font < 6 pt at print size.
- No two CVD simulations collapse the same line pair to the same color.
- No axis labels truncated by figure bounds.
- File size &lt; 10 MB (most journals cap at 10–20 MB per figure).
