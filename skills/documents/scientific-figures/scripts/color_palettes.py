# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "matplotlib",
# ]
# ///
"""Colorblind-safe categorical palettes, with one-call apply helpers.

Usage (CLI):
    uv run scripts/color_palettes.py --list
    uv run scripts/color_palettes.py --palette okabe_ito --show
    uv run scripts/color_palettes.py --palette tol_bright --set-globally

Usage (library):
    from color_palettes import PALETTES, apply_palette
    apply_palette("okabe_ito")
    print(PALETTES["wong"])
"""

from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt

# Each value list: hex strings, ordered so the i-th series gets the i-th color.
PALETTES: dict[str, list[str]] = {
    # Okabe & Ito 2008 — the de facto categorical standard for accessibility.
    "okabe_ito": [
        "#000000",
        "#E69F00",
        "#56B4E9",
        "#009E73",
        "#F0E442",
        "#0072B2",
        "#D55E00",
        "#CC79A7",
    ],
    # Wong 2011 (Nature Methods) — same colors, slightly different ordering.
    "wong": [
        "#000000",
        "#E69F00",
        "#56B4E9",
        "#009E73",
        "#F0E442",
        "#0072B2",
        "#D55E00",
        "#CC79A7",
    ],
    # Paul Tol's "bright" qualitative — 7 distinct colors, colorblind-safe.
    "tol_bright": [
        "#4477AA",
        "#EE6677",
        "#228833",
        "#CCBB44",
        "#66CCEE",
        "#AA3377",
        "#BBBBBB",
    ],
    # Paul Tol's "muted" qualitative — 9 colors, gentler on grayscale printing.
    "tol_muted": [
        "#332288",
        "#88CCEE",
        "#44AA99",
        "#117733",
        "#999933",
        "#DDCC77",
        "#CC6677",
        "#882255",
        "#AA4499",
    ],
    # Paul Tol's diverging — for data with a meaningful center.
    "tol_diverging": ["#CC6677", "#332288"],
}


def apply_palette(name: str) -> None:
    """Install the palette as matplotlib's default prop_cycle."""
    if name not in PALETTES:
        raise KeyError(f"unknown palette {name!r}; choose from {list_palettes()}")
    mpl.rcParams["axes.prop_cycle"] = mpl.cycler(color=PALETTES[name])


def list_palettes() -> list[str]:
    return sorted(PALETTES)


def show_palette(name: str) -> None:
    """Render a palette as a horizontal strip, useful for previewing."""
    colors = PALETTES[name]
    _fig, ax = plt.subplots(figsize=(len(colors) * 0.5, 0.8))
    for i, c in enumerate(colors):
        ax.add_patch(mpl.patches.Rectangle((i, 0), 1, 1, color=c, ec="white"))
    ax.set_xlim(0, len(colors))
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for i, c in enumerate(colors):
        ax.text(
            i + 0.5, -0.15, c, ha="center", va="top", fontsize=7, family="monospace"
        )
    ax.set_title(name, loc="left")
    for s in ("top", "right", "bottom", "left"):
        ax.spines[s].set_visible(False)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(description="Inspect or apply a categorical palette.")
    p.add_argument("--list", action="store_true", help="List known palettes.")
    p.add_argument("--palette", help="Palette name.")
    p.add_argument("--show", action="store_true", help="Render the palette to screen.")
    p.add_argument(
        "--set-globally", action="store_true", help="Apply as matplotlib prop_cycle."
    )
    a = p.parse_args()

    if a.list or a.palette is None:
        print("Available palettes:")
        for n in list_palettes():
            print(f"  {n}  ({len(PALETTES[n])} colors)")
    elif a.show:
        show_palette(a.palette)
    elif a.set_globally:
        apply_palette(a.palette)
        print(f"Applied {a.palette} to rcParams['axes.prop_cycle'].")
    else:
        for c in PALETTES[a.palette]:
            print(c)
