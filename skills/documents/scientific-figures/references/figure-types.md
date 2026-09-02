# Figure Types — Recipes

Every recipe assumes the matplotlib object-oriented API: `fig, ax = plt.subplots(...)`. Apply a preset first (`from style_presets import apply_style; apply_style("nature")`).

## Line plot

```python
fig, ax = plt.subplots(figsize=size_for("single", "golden"), constrained_layout=True)
ax.plot(x, y, label="data", color="#0072B2", linewidth=1.2)
ax.fill_between(x, y - sd, y + sd, color="#0072B2", alpha=0.2, label="±1σ")
ax.set_xlabel("time (s)")
ax.set_ylabel("response (a.u.)")
ax.legend(frameon=False)
```

## Logarithmic axes — tick formatting

Default log-axis ticks show powers of ten (`10²`, `10³`, `10⁴`). This is
mathematically correct but often unreadable for domain-specific ranges
(audio frequencies, spatial scales, etc.). Replace them with human-friendly
labels and intermediate steps.

### Audio-frequency example (20 Hz – 20 kHz)

Standard audio engineering uses ISO 266 / IEC 61260 preferred values:
20, 50, 100, 200, 500, 1k, 2k, 5k, 10k, 20k Hz.

**With `xy.pyplot` / matplotlib:**

```python
_AUDIO_FREQ_TICKS = [20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]
_AUDIO_FREQ_LABELS = [
    f"{t / 1000:g}k" if t >= 1000 else f"{t:g}" for t in _AUDIO_FREQ_TICKS
]

ax.set_xscale("log")
ax.set_xticks(_AUDIO_FREQ_TICKS)
ax.set_xticklabels(_AUDIO_FREQ_LABELS)
# or for a y-axis:
ax.set_yticks(_AUDIO_FREQ_TICKS)
ax.set_yticklabels(_AUDIO_FREQ_LABELS)
```

**With `xy.chart` (declarative marks API):**

```python
xy.x_axis(
    label="Frequency (Hz)",
    type_="log",
    tick_values=_AUDIO_FREQ_TICKS,
    tick_labels=_AUDIO_FREQ_LABELS,
)
```

### General rule

- For any log axis, ask: "what are the canonical values in this field?"
- Audio → 20, 50, 100, 200, 500, 1k, 2k, 5k, 10k, 20k.
- Vision / spatial → 1′, 2′, 5′, 10′, 30′, 1°, 2°, 5°, 10° (arcmin/deg).
- Time → 1 ms, 2 ms, 5 ms, 10 ms, 20 ms, 50 ms, 100 ms, 200 ms, 500 ms, 1 s.
- Never leave the raw `10ⁿ` labels on a figure intended for domain experts.

## Scatter

```python
fig, ax = plt.subplots(figsize=size_for("single", "square"), constrained_layout=True)
sc = ax.scatter(x, y, c=group, cmap="viridis", s=10, alpha=0.7, edgecolors="none")
fig.colorbar(sc, ax=ax, label="group")
ax.set_xlabel("x")
ax.set_ylabel("y")
```

## Bar / column

```python
fig, ax = plt.subplots(figsize=size_for("single", "4:3"), constrained_layout=True)
ax.bar(labels, values, color="#56B4E9", edgecolor="black", linewidth=0.5)
ax.errorbar(
    labels, values, yerr=errs, fmt="none", ecolor="black", capsize=3, linewidth=0.8
)
ax.set_ylabel("metric")
```

For grouped bars, use `np.arange` for x-positions and shift each series by `±width`.

## Heatmap

```python
fig, ax = plt.subplots(figsize=size_for("single", "4:3"), constrained_layout=True)
im = ax.imshow(matrix, cmap="viridis", aspect="auto", vmin=0, vmax=matrix.max())
fig.colorbar(im, ax=ax, label="intensity")
ax.set_xticks(range(matrix.shape[1]))
ax.set_yticks(range(matrix.shape[0]))
ax.set_xticklabels(col_labels, rotation=45, ha="right")
```

For annotated heatmaps, loop and call `ax.text(j, i, f"{matrix[i, j]:.2f}", ...)`, font size ≤ 6 pt.

## Contour / contourf

```python
fig, ax = plt.subplots(figsize=size_for("double", "golden"), constrained_layout=True)
levels = np.linspace(z.min(), z.max(), 11)
cf = ax.contourf(X, Y, Z, levels=levels, cmap="viridis")
ax.contour(X, Y, Z, levels=levels, colors="black", linewidths=0.4)
fig.colorbar(cf, ax=ax)
```

## Error bars

- Use `errorbar()`, not raw `plot()` plus patches.
- `capsize=3` for visible endcaps; linewidth `0.8` is the journal norm.
- Always specify which kind: SEM, SD, 95% CI, IQR. Put it in the caption.

## Multi-panel (single figure, several Axes)

Three common patterns:

### `plt.subplots` for a regular grid

```python
fig, axes = plt.subplots(
    2, 3, figsize=size_for("double", "16:9"), constrained_layout=True, sharex=True
)
```

### `GridSpec` for irregular layouts

```python
import matplotlib.gridspec as gridspec

fig = plt.figure(figsize=size_for("double", "16:9"))
gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.4, wspace=0.4)
ax_top = fig.add_subplot(gs[0, :])  # wide panel on top
ax_bl = fig.add_subplot(gs[1, 0])
ax_br = fig.add_subplot(gs[1, 1])
```

### Shared axes

Pass `sharex=True` or `sharey=True` to `plt.subplots`; then `ax.tick_params(labelbottom=False)` on interior panels.

Panel labels (A, B, C, D): `ax.set_title("A", loc="left", fontweight="bold")` is the cleanest pattern. Make them 8–9 pt bold, sans-serif, no period.

## 3D

Avoid 3D for data that isn't intrinsically volumetric. If you must:

```python
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (registers the projection)

fig = plt.figure(figsize=size_for("single", "square"))
ax = fig.add_subplot(111, projection="3d")
ax.plot_surface(X, Y, Z, cmap="viridis", edgecolor="none")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
```

Always set `ax.view_init(elev=20, azim=-60)` explicitly. Default angles are wrong for almost every plot.

## Polar / geographic / heatmap on a disk

Less common, but if you need them: `projection="polar"` or `projection="aitoff"` on the subplot. See `matplotlib/projections/` for built-ins.

## Subplot alignment tricks

- `constrained_layout=True` (matplotlib ≥ 3.4) replaces `tight_layout` for most cases.
- For fine manual control, use `fig.subplots_adjust(left=..., right=..., bottom=..., top=..., wspace=..., hspace=...)`.
- Anchored cartesian axes inside a polar axes: `ax.inset_axes([x, y, w, h])`.

## Subplot reference numbering

When a panel is referenced in the caption as "Fig. 1B", use uppercase bold panel labels and consistent placement (top-left of each panel). The reviewer should never have to guess which panel is which.
