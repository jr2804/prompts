# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "matplotlib",
#   "numpy",
#   "pillow",
# ]
# ///
"""Smoke-test script: renders a canonical 2×2 multi-panel figure and exports it.

Run via:
    uv run scripts/figure_demo.py
    uv run scripts/figure_demo.py --out /tmp/fig --formats pdf png
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

# Local sibling imports — uv run adds scripts/ to sys.path automatically, but
# we make this defensive so the script is also useful when imported as a module.
sys.path.insert(0, str(Path(__file__).parent))

import matplotlib.pyplot as plt
from export_figure import export_publication_figure
from figure_size import size_for
from style_presets import apply_style


def make_demo_figure() -> plt.Figure:
    apply_style("nature")
    w, h = size_for("double", "4:3")
    fig, axes = plt.subplots(2, 2, figsize=(w, h * 2 / 1.5), constrained_layout=True)

    rng = np.random.default_rng(0)
    x = np.linspace(0, 4 * np.pi, 200)

    # Panel A: line plot
    axes[0, 0].plot(x, np.sin(x), label="sin", linewidth=1.2, color="#0072B2")
    axes[0, 0].plot(
        x, np.cos(x), label="cos", linewidth=1.2, color="#D55E00", linestyle="--"
    )
    axes[0, 0].set_xlabel("x (rad)")
    axes[0, 0].set_ylabel("amplitude")
    axes[0, 0].legend()
    axes[0, 0].set_title("A", loc="left")

    # Panel B: scatter
    n = 200
    px, py = rng.normal(size=n), rng.normal(size=n)
    axes[0, 1].scatter(px, py, s=8, color="#009E73", alpha=0.6)
    axes[0, 1].set_xlabel("x")
    axes[0, 1].set_ylabel("y")
    axes[0, 1].set_title("B", loc="left")

    # Panel C: bar
    axes[1, 0].bar(
        ["ctrl", "low", "high"],
        [3.1, 4.2, 5.5],
        color=["#0072B2", "#E69F00", "#D55E00"],
    )
    axes[1, 0].set_ylabel("response")
    axes[1, 0].set_title("C", loc="left")

    # Panel D: heatmap with perceptually uniform colormap
    grid = rng.standard_normal((20, 20)).cumsum(axis=0)
    im = axes[1, 1].imshow(grid, cmap="viridis", aspect="auto")
    fig.colorbar(im, ax=axes[1, 1])
    axes[1, 1].set_title("D", loc="left")

    return fig


if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description="Render and export a 2x2 demo multi-panel figure."
    )
    p.add_argument(
        "--out", default="figure_demo", help="Base output path (no extension)."
    )
    p.add_argument(
        "--formats",
        nargs="+",
        default=["svg", "png"],
        help="Output formats. SVG first; PNG only as a fallback (will be 300 DPI by default).",
    )
    p.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="Raster DPI (PNG/TIFF). 300 is print-ready floor; do not go below.",
    )
    p.add_argument("--no-show", action="store_true")
    a = p.parse_args()

    fig = make_demo_figure()
    export_publication_figure(fig, a.out, formats=a.formats, dpi=a.dpi)
    if not a.no_show:
        plt.show()
