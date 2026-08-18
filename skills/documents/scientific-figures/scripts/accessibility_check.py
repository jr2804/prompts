# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "matplotlib",
#   "numpy",
#   "pillow",
# ]
# ///
"""Lightweight accessibility & quality checks on a finished figure PNG.

Usage:
    uv run scripts/accessibility_check.py figure.png
    uv run scripts/accessibility_check.py figure.png --strict   # exit non-zero on any warn

Checks:
1. File size < 10 MB (most journals cap individual figures at 10–20 MB).
2. Color-vision-deficiency simulation: defer to colorblind_check.py for full report,
   this script just summarizes collision count.
3. Pixel histogram: any single channel saturating > 99% may indicate the figure is
   clipped to white/black, suggesting a y-axis range problem.

This script does NOT measure actual rendered font sizes — that would require OCR,
and the rendered font size depends on the rendered pixel density which the journal
rescales anyway. Use the journal's required final-print font size in your style.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from colorblind_check import check_image
from PIL import Image

MAX_FIGURE_BYTES = 10 * 1024 * 1024  # 10 MB
SATURATION_WARN = 0.99  # > 99% of pixels clipped to one end


def check(path: Path) -> list[tuple[str, str, str]]:
    """Return a list of (severity, code, message) tuples."""
    findings: list[tuple[str, str, str]] = []

    size = path.stat().st_size
    if size > MAX_FIGURE_BYTES:
        findings.append(
            ("error", "size", f"{size / 1024 / 1024:.1f} MB exceeds 10 MB cap.")
        )
    elif size > 0.5 * MAX_FIGURE_BYTES:
        findings.append(
            (
                "warn",
                "size",
                f"{size / 1024 / 1024:.1f} MB; consider vector (PDF) instead.",
            )
        )

    img = Image.open(path).convert("RGB")
    px = img.getdata()
    total = img.width * img.height
    white = sum(1 for r, g, b in px if r > 250 and g > 250 and b > 250)
    black = sum(1 for r, g, b in px if r < 5 and g < 5 and b < 5)
    white_frac = white / total
    black_frac = black / total

    if white_frac > SATURATION_WARN:
        findings.append(
            (
                "warn",
                "clip",
                (
                    f"{white_frac:.1%} of pixels are nearly white. "
                    f"Check axis limits — figure may be clipping data."
                ),
            )
        )
    if black_frac > SATURATION_WARN:
        findings.append(
            (
                "warn",
                "clip",
                (
                    f"{black_frac:.1%} of pixels are nearly black. "
                    f"Possible background/text overflow into plot area."
                ),
            )
        )

    return findings


def _colorblind_summary(path: Path) -> str | None:
    """Run colorblind_check.py if importable as a sibling script; return summary.

    Imports the function directly so the caller doesn't need a sub-uv-subprocess dance.
    """
    here = Path(__file__).resolve().parent
    if str(here) not in sys.path:
        sys.path.insert(0, str(here))
    try:
        result = check_image(path)
    except Exception as e:  # ImportError, missing dep, etc.
        return f"CVD check skipped: {e}"
    sims = result.get("simulations", {})
    parts = []
    for sim_name, sim in sims.items():
        parts.append(f"{sim_name}={len(sim.get('collisions', []))}")
    return "CVD collisions: " + ", ".join(parts)


if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description="Run a fast accessibility/quality pass on a figure."
    )
    p.add_argument("image", type=Path)
    p.add_argument(
        "--strict",
        action="store_true",
        help="Exit with non-zero status on any warning or error.",
    )
    args = p.parse_args()

    if not args.image.is_file():
        print(f"error: not a file: {args.image}", file=sys.stderr)
        sys.exit(2)

    findings = check(args.image)
    print(f"== {args.image.name} ==")
    if not findings:
        print("  ok - no findings.")
    for sev, code, msg in findings:
        print(f"  [{sev}] {code}: {msg}")

    summary = _colorblind_summary(args.image)
    if summary:
        print(f"  info: {summary}")

    if args.strict and any(s in ("warn", "error") for s, *_ in findings):
        sys.exit(1)
