# Submission Release Checklist

Before a figure leaves your hands:

## Visual integrity

- [ ] No title inside the figure.
- [ ] Axis labels include units.
- [ ] All encoded variables have a legend or in-figure annotation.
- [ ] Error-bar type (SEM/SD/CI/IQR) is named in the caption or legend.
- [ ] Color is redundant with at least one other visual encoding (linestyle, marker, pattern).
- [ ] Grayscale-safe: prints to grayscale without losing information.
- [ ] No clipped axes without an explicit break mark.

## Typography

- [ ] Single typeface used consistently across all figures in the manuscript.
- [ ] Fonts at print size ≥ 6 pt for ticks, ≥ 7 pt for labels.
- [ ] `pdf.fonttype=42` and `ps.fonttype=42` are set (TrueType, not Type 3).
- [ ] All fonts embedded in the exported PDF.

## Color & accessibility

- [ ] Palette is CVD-distinguishable: `uv run scripts/colorblind_check.py figure.png` returns ≤ 1 collision per simulation.
- [ ] Colormap has a colorbar with units.
- [ ] Sequential colormaps do not include a divergent middle color.
- [ ] No `jet` colormap.

## Export

- [ ] Vector for plots; **SVG first**, PDF for journal venues that demand it.
- [ ] PNG/TIFF only as compatibility fallback; **300 DPI minimum** for any raster (Nature line art wants 600).
- [ ] File size < 10 MB per figure.
- [ ] Filename uses the manuscript's figure numbering (`fig01`, `fig02`, ...).
- [ ] Same source data and code in this repo produce the figure again (`scripts/figure_demo.py` example pattern).
- [ ] If the figure is embedded in a Word/PowerPoint document, the source is SVG, not PDF.

## Final pass

- [ ] Run `uv run scripts/accessibility_check.py figure.png --strict` (must exit 0).
- [ ] Open the PDF at column width on screen — verify everything is legible at print size.
- [ ] Print the PDF in grayscale — verify no information loss.
- [ ] Cross-reference: every figure number in the text actually exists in the figure set, and vice versa.
