# Color & Accessibility

## TL;DR

- Categorical data: **Okabe-Ito** until a reason appears.
- Sequential data: **viridis** (default) → plasma → cividis.
- Diverging data with a meaningful center: **coolwarm** or **RdBu_r**.
- Never use `jet`. Never rely on red/green hue alone.

## Categorical palettes (colorblind-safe)

All four palettes below are distinguishable under protan, deutan, and tritan vision. `color_palettes.py` ships them; use `apply_palette(name)` to set them as `rcParams['axes.prop_cycle']`.

### Okabe-Ito (recommended default)

The single most cited categorical palette in scientific publishing (Okabe & Ito 2008). 8 distinct colors; black included as the 8th entry so a single-series in black reads as intentional.

```python
apply_palette("okabe_ito")
```

### Wong

Identical hues to Okabe-Ito, re-ordered so that the first three entries are maximally distinct. Sometimes cited as Nature Methods' house style (Wong 2011). Use it if you submit to a Nature Portfolio journal that has a soft preference.

### Paul Tol "bright"

7 colors, optimized for projector screens. Slightly more saturated than Okabe-Ito; reads well at poster scale.

### Paul Tol "muted"

9 colors, designed to remain readable when converted to grayscale. Best when the journal accepts grayscale printing.

### Tol diverging

Two-color diverging palette for continuous data with a meaningful center. Avoid for categorical data.

## Sequential colormaps (continuous data)

| Colormap | Type | Notes |
|---|---|---|
| `viridis`  | perceptually uniform | Default. Colorblind-safe. Safe choice. |
| `cividis`  | perceptually uniform | Optimized specifically for CVD viewers. |
| `plasma`   | perceptually uniform | Punchier than viridis; same safety guarantee. |
| `magma`    | perceptually uniform | Dark background → good for projection. |
| `inferno`  | perceptually uniform | Like plasma but darker. |
| `Blues`/`Reds`/`Greens` | single-hue | Print-friendly; OK for monochrome figures. |

### Anti-patterns

- `jet` — famously bad (Borland & Taylor 2007; others). Not perceptually uniform; introduces false boundaries.
- `rainbow` — same problems as `jet`.
- Two red/green pairs in the same figure without redundant encoding — collapses under deuteranopia.

## Diverging colormaps (data with center)

Use when the data has a meaningful zero or mean:

- `coolwarm` — blue ↔ red, gentle.
- `RdBu_r` — slightly more saturated.
- `BrBG`, `PiYG`, `PuOr`, `RdGy` — alternative hues for figure variety.

Always set `vmin` and `vmax` to be symmetric around the center.

## Grayscale safety

When the paper may print in grayscale, color should be redundant. Encode the same variable with **hue + line style** (solid, dashed, dotted) or **hue + marker** (circle, square, triangle). At minimum:

- Differently-colored lines → differentiate with line styles.
- Bars → add pattern fills (diagonal stripes) for the most important category.
- Heatmaps → print a copy in `Greys` to confirm the gradient still reads.

## Font size at print size

These are the rendered sizes after the journal scales the figure to its column width. Fonts that read on screen at 10 pt may render at 5 pt in print, where they become unreadable.

| Element      | Minimum at print size |
|--------------|------------------------|
| Axis labels  | 7 pt                   |
| Tick labels  | 6 pt                   |
| Legend       | 6 pt                   |
| Panel label  | 8 pt (bold)            |
| Caption      | journal-dependent — usually in LaTeX/Word |

## CVD simulation in this skill

`scripts/colorblind_check.py` simulates protanopia, deuteranopia, and tritanopia from a finished PNG using Machado 2009 matrices (severity 1.0). It reports any color pair that is distinguishable in the original but collapses to the same hue under simulation. Treat any non-empty collision list as a request to add a redundant visual encoding (linestyle, marker, pattern).

For a stricter simulation, install `colour-science` (`uv add colour-science`) and re-run; the script auto-detects it.

## Quick checklist before submission

- [ ] Palette distinguishable under all three CVD types (`colorblind_check.py`).
- [ ] All encoded variables distinguishable in grayscale printout.
- [ ] Fonts ≥ 6 pt at the figure's printed size (verify by exporting PDF then viewing at column width).
- [ ] Colorbar present if a sequential or diverging colormap is used, with a label and units.
- [ ] No "AI slop" defaults — no `plt.title`, no rainbow, no grid-by-default.
