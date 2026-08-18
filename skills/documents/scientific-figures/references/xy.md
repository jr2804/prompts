# reflex-xy

[reflex-xy](https://github.com/reflex-dev/xy) is the recommended default for any new scientific figure project. Two facts make it worth caring about:

1. It claims to render **10⁹ points** in a browser interactively by computing only what fits the viewport.
2. It ships a **`import xy.pyplot as plt`** module that mimics the matplotlib idiom — so the import is the only thing you usually change.

## xy as the matplotlib drop-in

For the vast majority of code, `xy.pyplot` and `matplotlib.pyplot` are interchangeable. Use `xy` whenever you start a new figure. Use `matplotlib` directly only when:

- You depend on a matplotlib-only extension API (rare).
- You're submitting to a venue with strict EPS/PDF font rules; matplotlib's PDF embed pipeline is older and more battle-tested than xy's at the time of writing.
- You're maintaining a project that was already on matplotlib and the cost of the swap isn't worth it.

```python
import numpy as np
import xy.pyplot as plt  # swap this for `import matplotlib.pyplot as plt` to revert

x = np.linspace(0, 10, 200)
fig, ax = plt.subplots()
ax.plot(x, np.sin(x), "r--", label="signal")
ax.legend()
plt.show()
```

The matplotlib helpers in this skill (`apply_style`, `size_for`, `export_publication_figure` from `scripts/`) work as long as the underlying library exposes the standard `Figure` / `Axes` / `subplots()` API — which `xy.pyplot` does. If you hit a method that `xy` doesn't yet implement, fall back to matplotlib by changing only the import line; the rest of the code is unchanged.

See the upstream compatibility guide at <https://github.com/reflex-dev/xy/blob/main/spec/matplotlib/compat.md> for what's covered in the current xy version.

## When to consider xy specifically

- Datasets larger than ~10⁷ points where matplotlib's `scatter` would be unusable.
- You need interactive zoom/pan/select on the web (HTML output) and PDF/PNG/SVG for the paper from the same source.
- You want declarative or matplotlib-style code; you don't want a JavaScript toolchain.

## When NOT to use xy

- Fine typographic control is required (it's catching up but still cruder than matplotlib).
- The figure must be PDF/EPS and pass strict journal font checks — matplotlib still wins.
- You're already in a seaborn/plotly/bokeh ecosystem.

## Quick start

```bash
uv add xy
```

```python
import xy

chart = xy.line_chart(xy.line([1, 2, 3, 4, 5], [120, 180, 165, 240, 310]))
# Output choices:
# chart.to_html("chart.html")
# chart.to_png("chart.png")
# chart.to_svg("chart.svg")
chart  # in a notebook, renders inline
```

## Exposing xy as SVG/PDF/PNG for the paper

```python
chart.to_svg("figure_xy.svg")  # preferred vector
chart.to_pdf("figure_xy.pdf")  # journal submission
chart.to_png("figure_xy.png", scale=2)  # compatibility fallback, 2x ≈ 200 DPI
```

Treat SVG as the paper/source-of-truth file and `.to_html()` as the supplementary interactive version. PDF only for venues that demand it (most journals).

## Maturity caveat

xy is alpha. Pin a version (`uv add 'xy>=0.1,<0.2'` or similar) and re-test export before any submission. Don't depend on edge features that aren't in the compat docs.

## Other emerging libraries (worth knowing about)

| Library     | What it does | Why it matters |
|-------------|--------------|----------------|
| **marimo**  | Reactive notebook; figures auto-rerun when data changes. | Pairs naturally with xy/plotly for iterative figures. |
| **mosaic** (`ggmosaic`) | Grammar-of-graphics for matplotlib. | If you prefer ggplot-style layering. |
| **altair**  | Declarative Vega-Lite binding. | Best for small interactive web figures. |
| **pythony** | Newer matplotlib alternatives; check `awesome-python-data-science`. | Survey before committing. |
