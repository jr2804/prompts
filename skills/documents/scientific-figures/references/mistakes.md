# Common Mistakes

A short list of figures that don't make it past peer review — and what to do instead.

## In the figure itself

- **Title inside the figure.** The caption belongs in the manuscript. Move it out.
- **`plt.show()` left in.** Export-only scripts should never rely on the GUI back-end. Set `matplotlib.use("Agg")` at the very top if running headless.
- **Grid by default.** Matplotlib's default style puts a gray grid behind everything. Turn it off (`axes.grid: False` in presets) unless you actively want it.
- **Black axis frame with `axes.spines` defaults.** Despine for a cleaner look.
- **`plt.title('My plot')`** on every panel. Just don't.
- **`fig.tight_layout()` but `ax.title` overflows.** Use `constrained_layout=True` at figure creation instead; it works earlier.
- **Saving with `dpi=100` and submitting to Nature.** Raster DPI must be ≥ 300. Vector formats (SVG/PDF) ignore dpi.
- **Saving PNG and dropping it into a paper.** PNG is bitmap and does not scale. Use SVG (preferred) or PDF when the consumer can take it.
- **Saving PDF and dropping it into a Word/PowerPoint document.** PDF imported into Office commonly rasterizes on import, losing crispness. Use SVG for office-doc figures.
- **`pdf.fonttype=3`** (the Type 3 bitmap font fallback). Use `pdf.fonttype=42` to embed TrueType.
- **JPEG for data.** Always PNG, TIFF, or vector. JPEG's lossy compression introduces artifacts near edges and labels.
- **Truncated axes without marking them.** Add `ax.plot([x_start]*2, y_range, '--', color='black', linewidth=0.5)` or use `ax.annotate(...)` to draw a break mark.
- **3D bar charts.** Almost always worse than a 2D heatmap or grouped bar. 3D is for genuinely volumetric data.
- **Color-only encoding** (e.g., red vs. green vs. blue boxes with no labels). Fails under CVD and in grayscale.

## In the data

- **Plotting raw points and a fit line without saying which is which.** Add a legend or annotation.
- **Error bars with no label.** Specify SEM, SD, 95% CI, IQR in the caption or legend.
- **No zero baseline on bar charts.** Either show zero explicitly, or label the y-axis to make the broken axis obvious.
- **Heatmap with no colorbar.** Without a colorbar, the reader cannot decode the values.
- **Heatmap with clipped values reported as zero.** Apply `np.clip` before plotting or use `vmin`/`vmax` explicitly.
- **Truncated x-axis that exaggerates a small effect.** Use `ax.set_xlim(...)` deliberately; don't rely on the auto-limits.

## In the manuscript workflow

- **Different fonts across figures in the same paper.** Use one preset; if you change preset, change it for every figure.
- **Saving to `figure1.pdf` then renaming to `figure1_v2_FINAL.pdf`.** Use figure numbers that match the manuscript (`fig01.pdf`, `fig02.pdf`).
- **Embedded bitmap preview as the submission figure.** Always re-export from source data.
- **Two nearly-identical figures instead of one multi-panel figure.** Reviewers notice.
- **A figure with only one data series of three points.** Could be a sentence.

## AI tells — don't ship these

- Title like "Bar Plot of Y vs X" (default seaborn/Matplotlib pattern).
- Equal-aspect scatter plots cropped tightly to a square (looks forced).
- A `fig.suptitle` that paraphrases the caption.
- Default matplotlib color cycle (`C0`, `C1`, ...) on a paper figure — it reads as unedited.
- Boxplots with no jitter and small `n`. The reader sees only the IQR and assumes many points.
- Confidence intervals as colored bands with no 0-line and no n= annotation.

## How this skill helps

- `style_presets.py` strips the most-cited defaults.
- `accessibility_check.py` flags clipped/whited-out figures and over-large file sizes.
- `colorblind_check.py` flags CVD collapses so you add redundant encoding instead of just hoping.
- `release-checklist.md` covers the rest.
