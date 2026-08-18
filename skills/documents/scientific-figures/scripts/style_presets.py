# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "matplotlib",
# ]
# ///
"""Apply named journal/venue styles to matplotlib rcParams.

Usage (from another script or REPL):
    from style_presets import apply_style, list_styles
    apply_style("nature")               # Nature single/double column
    apply_style("science")              # Science
    apply_style("plos")                 # PLOS / PLOS ONE
    apply_style("ieee")                 # IEEE journals/conferences
    apply_style("poster")               # Posters / slides
    print(list_styles())
"""

from __future__ import annotations

import matplotlib as mpl

# Palette: Okabe-Ito, colorblind-safe (de facto standard for scientific pubs).
OKABE_ITO = [
    "#000000",
    "#E69F00",
    "#56B4E9",
    "#009E73",
    "#F0E442",
    "#0072B2",
    "#D55E00",
    "#CC79A7",
]

# Each preset is a flat dict of rcParams keys. Values copied/condensed from
# davila7/scientific-visualization (Nature/Publication/Presentation) and the
# matplotlib defaults reference. Keep these small — only override what matters.
PRESETS: dict[str, dict] = {
    # Nature: 89 mm single col, 183 mm double, Arial/Helvetica, small fonts.
    "nature": {
        "figure.figsize": (3.5, 2.6),
        "figure.dpi": 100,
        "savefig.dpi": 600,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.05,
        "savefig.transparent": False,
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": 7,
        "axes.labelsize": 8,
        "axes.titlesize": 8,
        "axes.linewidth": 0.5,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.edgecolor": "black",
        "axes.labelcolor": "black",
        "axes.prop_cycle": mpl.cycler(color=OKABE_ITO),
        "xtick.labelsize": 6,
        "ytick.labelsize": 6,
        "xtick.major.size": 2.5,
        "ytick.major.size": 2.5,
        "xtick.major.width": 0.5,
        "ytick.major.width": 0.5,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "lines.linewidth": 1.2,
        "lines.markersize": 3,
        "lines.markeredgewidth": 0.4,
        "legend.fontsize": 6,
        "legend.frameon": False,
        "image.cmap": "viridis",
        "figure.constrained_layout.use": True,
    },
    # Science: 5.5 cm single col, ~12 cm double. Slightly larger fonts than Nature.
    "science": {
        "figure.figsize": (3.27, 2.45),
        "figure.dpi": 100,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.05,
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": 8,
        "axes.labelsize": 9,
        "axes.titlesize": 9,
        "axes.linewidth": 0.6,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.prop_cycle": mpl.cycler(color=OKABE_ITO),
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "lines.linewidth": 1.5,
        "lines.markersize": 4,
        "legend.fontsize": 7,
        "legend.frameon": False,
        "image.cmap": "viridis",
        "figure.constrained_layout.use": True,
    },
    # PLOS: 7.5" max width body, ~13.22 cm column width; serif often preferred.
    "plos": {
        "figure.figsize": (5.2, 3.9),
        "figure.dpi": 100,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif"],
        "font.size": 9,
        "axes.labelsize": 10,
        "axes.titlesize": 10,
        "axes.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.prop_cycle": mpl.cycler(color=OKABE_ITO),
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "lines.linewidth": 1.5,
        "legend.fontsize": 8,
        "legend.frameon": False,
        "image.cmap": "viridis",
        "figure.constrained_layout.use": True,
    },
    # IEEE: 3.5" single col, often used in conferences/journals, Times-like font.
    "ieee": {
        "figure.figsize": (3.5, 2.6),
        "figure.dpi": 100,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif"],
        "font.size": 8,
        "axes.labelsize": 9,
        "axes.titlesize": 9,
        "axes.linewidth": 0.6,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.prop_cycle": mpl.cycler(color=OKABE_ITO),
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "lines.linewidth": 1.2,
        "legend.fontsize": 7,
        "legend.frameon": False,
        "image.cmap": "viridis",
        "figure.constrained_layout.use": True,
    },
    # Poster / slide: ~10x bigger fonts and thicker lines for projection.
    "poster": {
        "figure.figsize": (10, 7.5),
        "figure.dpi": 100,
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.1,
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "Calibri"],
        "font.size": 14,
        "axes.labelsize": 16,
        "axes.titlesize": 18,
        "axes.linewidth": 1.5,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.prop_cycle": mpl.cycler(color=OKABE_ITO),
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
        "xtick.major.size": 6,
        "ytick.major.size": 6,
        "xtick.major.width": 1.5,
        "ytick.major.width": 1.5,
        "lines.linewidth": 2.5,
        "lines.markersize": 8,
        "legend.fontsize": 12,
        "legend.frameon": False,
        "image.cmap": "viridis",
        "figure.constrained_layout.use": True,
    },
}


def list_styles() -> list[str]:
    return sorted(PRESETS)


def apply_style(name: str) -> None:
    """Apply preset to matplotlib's global rcParams.

    Raises KeyError if name is unknown; call ``list_styles()`` for valid keys.
    """
    mpl.rcParams.update(PRESETS[name])


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(description="Apply a named matplotlib style preset.")
    p.add_argument("name", nargs="?", help="One of: " + ", ".join(list_styles()))
    p.add_argument(
        "--list", action="store_true", help="List available styles and exit."
    )
    a = p.parse_args()
    if a.list or a.name is None:
        print("Available styles:")
        for n in list_styles():
            print(f"  {n}")
    else:
        apply_style(a.name)
        print(f"Applied style: {a.name}")
