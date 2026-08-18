# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Compute figure sizes in inches for common column targets.

Usage (CLI):
    uv run scripts/figure_size.py --target single --ratio 4:3
    uv run scripts/figure_size.py --target 1.5col --ratio golden

Usage (library):
    from figure_size import size_for
    w, h = size_for("single", "4:3")           # → (3.54, 2.66)
    w, h = size_for("double", "golden")        # → (7.09, 4.38)
"""

from __future__ import annotations

import argparse
import re

# Column widths per common journals (in inches). Trimmed to the dominant case.
# 1 inch == 25.4 mm. Nature/IEEE/etc. are 89 mm single column.
TARGETS: dict[str, float] = {
    "single": 3.54,  # ~89 mm  (Nature, Science, IEEE, ...; the default)
    "1.5col": 4.72,  # ~120 mm (Nature 1.5 column)
    "double": 7.09,  # ~180 mm (Nature double column)
    "plos": 5.20,  # ~132 mm (PLOS body)
    "poster": 10.00,  # ~254 mm slimmer side of a poster tile
}


def size_for(target: str, ratio: str = "4:3") -> tuple[float, float]:
    """Return (width_in, height_in) for the given target column and ratio.

    `ratio` accepts: "W:H" like "4:3" or "16:9", or keywords "square", "golden".
    """
    if target not in TARGETS:
        raise KeyError(f"unknown target {target!r}; choose from {list(TARGETS)}")

    w = TARGETS[target]
    if ratio == "square":
        h = w
    elif ratio == "golden":
        h = w / 1.6180339887
    else:
        m = re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*:\s*(\d+(?:\.\d+)?)\s*", ratio)
        if not m:
            raise ValueError(
                f"invalid ratio {ratio!r}; use 'W:H', 'square', or 'golden'"
            )
        a, b = float(m.group(1)), float(m.group(2))
        if b == 0:
            raise ValueError("ratio denominator must be > 0")
        h = w * b / a
    return round(w, 2), round(h, 2)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Compute (w, h) for a column target.")
    p.add_argument(
        "--target",
        required=True,
        choices=list(TARGETS),
        help="column target; affects width in inches",
    )
    p.add_argument(
        "--ratio", default="4:3", help="aspect ratio; 'W:H', 'square', or 'golden'"
    )
    a = p.parse_args()
    w, h = size_for(a.target, a.ratio)
    print(f"{w} x {h} in   ({a.target}, {a.ratio})")
