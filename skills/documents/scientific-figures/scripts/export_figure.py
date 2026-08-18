# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "matplotlib",
#   "pillow",
# ]
# ///
"""Export a matplotlib figure to one or more publication-grade file formats.

Format priority (defaults assume the consumer is flexible):
    SVG  — preferred default. Lossless vector; embeds fonts; editable in
           Inkscape/Illustrator; renders correctly in modern browsers;
           drops cleanly into Word/PowerPoint via Insert > Picture.
    PDF  — second choice. Great for journal submission and LaTeX, but PDF
           often rasterizes when imported into office documents, losing
           crispness and editability.
    PNG  — bitmap fallback ONLY. Does not scale. Use only when the consumer
           cannot ingest SVG/PDF (some legacy formatters, slide decks with
           heavy styling). When raster is unavoidable, 300 DPI is the floor
           (the matplotlib default of 100/200 DPI is not enough for print).

Usage (CLI):
    uv run scripts/export_figure.py demo --out figure1 --formats svg
    uv run scripts/export_figure.py demo --out figure1 --formats svg pdf
    uv run scripts/export_figure.py demo --out figure1 --formats svg pdf png --dpi 300

You can also call export_publication_figure(fig, ...) from your own script:

    from export_figure import export_publication_figure
    export_publication_figure(fig, "figure1")                              # SVG only
    export_publication_figure(fig, "figure1", formats=["svg", "png"], dpi=300)
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Iterable
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from style_presets import apply_style

try:
    # Pillow's Ghostscript backend is needed for vector→raster of PDF/EPS captions.
    from PIL import Image  # noqa: F401  (presence check; used in raster exporters)

    HAS_PIL = True
except ImportError:
    HAS_PIL = False


# Per-format defaults: dpi is the raster DPI; rest are format-specific safety knobs.
_FORMAT_DEFAULT_KWARGS = {
    "pdf": {"metadata": {"Creator": "scientific-figures skill", "Title": ""}},
    "eps": {},
    "svg": {},
    "png": {},
    "tiff": {"pil_kwargs": {"compression": "tiff_lzw"}},
}


def _demo(out: str, formats: list[str], dpi: int) -> None:
    fig = _make_demo_figure()
    export_publication_figure(fig, out, formats=formats, dpi=dpi)
    plt.show()


def export_publication_figure(
    fig: plt.Figure,
    base: str | Path,
    *,
    formats: Iterable[str] = ("svg",),
    dpi: int = 300,
    transparent: bool = False,
    bbox_inches: str = "tight",
    pad_inches: float = 0.05,
    facecolor: str = "white",
) -> list[Path]:
    """Save `fig` to one or more formats. Returns paths actually written.

    Vector formats (svg, pdf, eps) ignore `dpi` (use bbox_inches='tight' for cropping).
    Raster formats (png, tiff) use `dpi`. The default raster DPI is 300 (print-ready);
    matplotlib's own default of 100 DPI is below every reasonable journal minimum.

    When you ask for both vector and raster, you usually want the same figure saved
    twice with different suffixes — callers can pass e.g. formats=["svg", "png"].
    """
    base = Path(base)
    if base.suffix:
        base = base.with_suffix("")  # caller-provided suffix would double-up

    written: list[Path] = []
    for fmt in formats:
        fmt = fmt.lower().lstrip(".")
        kw = {
            "format": fmt,
            "bbox_inches": bbox_inches,
            "pad_inches": pad_inches,
            "transparent": transparent,
            "facecolor": facecolor,
        }
        # Per-format extras, e.g., PDF metadata, TIFF compression.
        defaults = _FORMAT_DEFAULT_KWARGS.get(fmt, {})
        for k, v in defaults.items():
            if k == "pil_kwargs":
                continue
            kw[k] = v
        # Raster needs dpi, vector ignores it (don't pass and trigger a warning).
        if fmt in ("png", "tiff", "jpg", "jpeg"):
            kw["dpi"] = dpi
        out = base.with_suffix("." + fmt)
        fig.savefig(
            out,
            **{
                k: v
                for k, v in kw.items()
                if v is not None or k in {"format", "bbox_inches"}
            },
        )
        written.append(out)
        print(f"Wrote {out}")
    return written


def _make_demo_figure() -> plt.Figure:
    """A canonical line+scatter example so the demo command works standalone."""

    sys.path.insert(0, str(Path(__file__).parent))

    apply_style("nature")

    fig, ax = plt.subplots(constrained_layout=True)
    x = np.linspace(0, 10, 200)
    ax.plot(x, np.sin(x), label="sin(x)", linewidth=1.2, color="#0072B2")
    ax.plot(
        x, np.cos(x), label="cos(x)", linewidth=1.2, color="#D55E00", linestyle="--"
    )
    ax.scatter(x[::20], np.sin(x[::20]), s=8, color="#0072B2", zorder=3)
    ax.set_xlabel("x (radians)")
    ax.set_ylabel("amplitude")
    ax.legend(loc="lower right")
    return fig


if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description="Export a matplotlib figure to publication formats."
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("demo", help="Render and export a demo line plot.")
    d.add_argument("--out", default="figure_demo")
    d.add_argument(
        "--formats",
        nargs="+",
        default=["svg", "png"],
        help="Output formats. SVG first; PNG only as a fallback (will be 300 DPI by default).",
    )
    d.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="Raster DPI (PNG/TIFF). 300 is print-ready floor; do not go below.",
    )
    d.add_argument(
        "--no-show", action="store_true", help="Skip the interactive plt.show()."
    )

    args = p.parse_args()
    if args.cmd == "demo":
        fig = _make_demo_figure()
        export_publication_figure(fig, args.out, formats=args.formats, dpi=args.dpi)
        if not args.no_show:
            plt.show()
