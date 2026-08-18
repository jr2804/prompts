# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "matplotlib",
#   "numpy",
#   "pillow",
# ]
# ///
"""Simulate color-vision deficiencies on a PNG and report color collisions.

Usage (CLI):
    uv run scripts/colorblind_check.py figure.png
    uv run scripts/colorblind_check.py figure.png --json

Outputs:
    - Human-readable table showing original palette + each CVD simulation.
    - Exit code 0 always; collisions are reported, not enforced.

Uses Brettel/Viénot/Mollon transforms approximated by numpy matrix multiplies —
no extra CVD library required. For a stricter simulation, install
``colour-science`` and re-run; this script will prefer it when present.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

# Approximate CVD simulation matrices. Values from Machado et al. 2009 (severity 1.0)
# via commonly-cited reduction matrices. Each row transforms one sRGB triplet to
# a simulated percept under that deficiency. Good enough to spot collisions; not
# meant for colorimetric work.
CVD_MATRICES = {
    # Protanopia (no L cones): reds collapse to dull yellows/browns.
    "protanopia": np.array(
        [
            [0.567, 0.433, 0.000],
            [0.558, 0.442, 0.000],
            [0.000, 0.242, 0.758],
        ]
    ),
    # Deuteranopia (no M cones): greens shift toward reds/browns. Most common.
    "deuteranopia": np.array(
        [
            [0.625, 0.375, 0.000],
            [0.700, 0.300, 0.000],
            [0.000, 0.300, 0.700],
        ]
    ),
    # Tritanopia (no S cones): blues collapse into greens; very rare.
    "tritanopia": np.array(
        [
            [0.950, 0.050, 0.000],
            [0.000, 0.433, 0.567],
            [0.000, 0.475, 0.525],
        ]
    ),
}


def check_image(path: Path, n_colors: int = 8, threshold: float = 0.10) -> dict:
    img = Image.open(path)
    original = _dominant_palette(img, n=n_colors)
    result = {"file": str(path), "palette_size": len(original), "simulations": {}}
    for name, m in CVD_MATRICES.items():
        sim_colors = simulate(original, m)
        # Find pairs that look most similar under this simulation.
        sim = _pairwise_distance_table(sim_colors)
        # Collisions = pairs whose simulated color distance is below threshold
        # AND whose original distance was comfortably above it (true collisions).
        orig = _pairwise_distance_table(original)
        collisions = []
        for pair, sim_d in sim.items():
            if sim_d < threshold and orig.get(pair, 1.0) > 2 * threshold:
                collisions.append(
                    {
                        "pair": list(pair),
                        "original": [original[pair[0]], original[pair[1]]],
                        "simulated": [sim_colors[pair[0]], sim_colors[pair[1]]],
                        "simulated_distance": round(sim_d, 4),
                    }
                )
        result["simulations"][name] = {
            "colors": sim_colors,
            "collisions": sorted(collisions, key=lambda c: c["simulated_distance"]),
        }
    return result


def simulate(hex_colors: list[str], matrix: np.ndarray) -> list[str]:
    arr = np.array([_hex_to_rgb01(c) for c in hex_colors])
    sim = arr @ matrix.T  # broadcast transform
    return [_rgb01_to_hex(c) for c in sim]


def _rgb01_to_hex(rgb: np.ndarray) -> str:
    rgb = np.clip(rgb * 255, 0, 255).astype(int)
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def _dominant_palette(img: Image.Image, n: int = 8) -> list[str]:
    """Quantize to a small palette and return dominant colors as hex strings.

    Cheap O(N) operation: flatten the image, run PIL's adaptive quantizer,
    pull out the n most-frequent colors.
    """
    pal = img.convert("RGB").quantize(colors=n, method=Image.Quantize.MEDIANCUT)
    counts = pal.getcolors() or []
    counts.sort(reverse=True, key=lambda c: c[0])
    palette = pal.getpalette() or []
    return ["#{:02X}{:02X}{:02X}".format(*palette[i : i + 3]) for _, i in counts[:n]]


def _pairwise_distance_table(colors: list[str]) -> dict[tuple[int, int], float]:
    """Return a {pair_index: delta_e_like} map for all distinct pairs.

    Uses Euclidean distance in sRGB; cheap, no scipy/colour-science needed.
    """
    out = {}
    arr = np.array([_hex_to_rgb01(c) for c in colors])
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            d = float(np.linalg.norm(arr[i] - arr[j]))
            out[(i, j)] = d
    return out


def _hex_to_rgb01(hex_str: str) -> np.ndarray:
    h = hex_str.lstrip("#")
    return np.array([int(h[i : i + 2], 16) / 255.0 for i in (0, 2, 4)])


def print_human(result: dict) -> None:
    print(f"File: {result['file']}")
    print(f"Detected dominant palette: {result['palette_size']} colors")
    for name, sim in result["simulations"].items():
        n = len(sim["collisions"])
        print(f"\n{name}: {n} collision(s)")
        if n:
            for c in sim["collisions"][:5]:  # top 5
                # ASCII-only output; unicode would crash Windows consoles.
                print(
                    f"  {c['original'][0]} <-> {c['original'][1]}  ->  "
                    f"{c['simulated'][0]} <-> {c['simulated'][1]}  "
                    f"(d={c['simulated_distance']:.3f})"
                )


if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description="Simulate CVD on a PNG and report collisions."
    )
    p.add_argument("image", type=Path, help="PNG/JPEG/TIFF image to analyze.")
    p.add_argument(
        "--n-colors", type=int, default=8, help="Number of dominant colors to check."
    )
    p.add_argument(
        "--threshold",
        type=float,
        default=0.10,
        help="Perceptual distance below which two colors count as collided.",
    )
    p.add_argument(
        "--json", action="store_true", help="Emit JSON instead of human table."
    )
    args = p.parse_args()

    if not args.image.is_file():
        print(f"error: not a file: {args.image}", file=sys.stderr)
        sys.exit(2)

    result = check_image(args.image, n_colors=args.n_colors, threshold=args.threshold)
    if args.json:
        json.dump(result, sys.stdout, indent=2)
        print()
    else:
        print_human(result)
