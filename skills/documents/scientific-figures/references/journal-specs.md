# Journal Specs at a Glance

Always confirm against the journal's current author guidelines. Numbers below are based on publicly posted guides as of writing.

| Venue           | Single col | 1.5 col | Double col | Min font at print | Raster DPI | Vector allowed |
|-----------------|-----------:|--------:|-----------:|------------------:|-----------:|----------------|
| Nature          | 89 mm      | 120 mm  | 183 mm     | 5 pt              | 300–600    | PDF, EPS, AI   |
| Science         | 5.5 cm     | —       | 12 cm      | 6 pt              | 300        | PDF, EPS       |
| PLOS            | 5.2" body  | —       | 7.5" body  | 8 pt              | 300        | PDF, EPS, TIFF |
| IEEE            | 3.5"       | —       | 7.16"      | 8 pt              | 300        | PDF, EPS       |
| Cell            | 8.5 cm     | —       | 17.5 cm    | 6 pt              | 300        | PDF, EPS, AI   |
| Elsevier (most) | 7.5 cm 1col / 13 cm 2col | — | — | 7 pt    | 300        | PDF, EPS       |
| ACS             | 8.5 cm     | —       | 17.5 cm    | 7 pt              | 300        | PDF, EPS, TIFF |

## Format selection (SVG / PDF / PNG)

Three questions, in order:

1. **Who is the consumer?**
   - **A journal submission system.** Check the table above. Nature takes PDF, EPS, AI. PLOS takes PDF, EPS, TIFF. Most journals do not list SVG — produce the format they accept.
   - **A Word/PowerPoint document.** SVG. Insert > Picture in modern Office renders SVG crisply at any zoom. PDF imported into Word commonly rasterizes and becomes blurry; importing PDF into PowerPoint is worse.
   - **A web page or dashboard.** SVG or HTML. Avoid raster.
   - **A legacy tool that cannot ingest vector.** Then PNG, at 300 DPI minimum.

2. **Is the figure a plot or an image?**
   - Plot (line/scatter/bar/heatmap/…) → vector. SVG first, then PDF.
   - Image (photograph, microscopy, gel, MRI slice) → raster. TIFF 600 DPI for print, PNG 300 DPI for screen/slides.

3. **Is paper size an issue?**
   - Vector: typically < 1 MB; thumbnails well, zoom without pixelation.
   - PNG: scales poorly. A 1× DPI PNG of a Nature double-column figure renders as ~0.4 MB but visibly soft when printed at print size. Always 300 DPI minimum.

### Default `export_publication_figure` choice

This skill defaults to SVG (single format) and to SVG + PNG at 300 DPI (vector + compatibility fallback) when both are requested. PDF is added when the consumer is a journal or LaTeX workflow. Pass `formats=["svg", "pdf", "png"]` if the figure will travel through several consumers.

### Why not PDF for Office documents?

PDF was designed as a print-format exchange, not an editing format. Most Word/PowerPoint versions import PDF by either:

1. Embedding it as an opaque icon (Office 365 sub-system allows zooming in to PDF, but editing is gone), or
2. Rasterizing on import — the figure becomes a bitmapped blob that no longer scales.

SVG, by contrast, is an open vector format that Office renders losslessly and that Inkscape/Illustrator can re-edit. The only reason to use PDF in an Office workflow is if the document is being sent to someone who must use Acrobat Reader (e.g., a formal review process).

## What's universal

- Sans-serif fonts (Arial, Helvetica) are accepted everywhere. Times is sometimes permitted, sometimes forbidden (check style guide).
- Vector for plots (PDF, EPS); raster for images (TIFF, PNG). Never JPEG.
- Color: RGB for screen-first journals (Nature is RGB), CMYK for print-first venues (Elsevier, ACS prefer CMYK but accept RGB).
- Embed all fonts in the PDF (`savefig.bbox='tight'`, `pdf.fonttype=42`, `ps.fonttype=42`).

## matplotlib knobs that hit all the universal items

```python
mpl.rcParams.update(
    {
        "savefig.bbox": "tight",  # never let whitespace survive
        "savefig.pad_inches": 0.05,
        "pdf.fonttype": 42,  # TrueType, not Type 3
        "ps.fonttype": 42,
        "savefig.transparent": False,  # white background unless requested
    }
)
```

These are baked into every preset in `style_presets.py`.

## EPS-specific gotcha

EPS does not support transparency. If `savefig.transparent=True`, switch to PDF (or generate PNG/EPS and accept the white background). Many journals still demand EPS specifically — produce it anyway and live with the white box around subplots.

## File size limits

Most journals cap individual figures at **10–20 MB** and total at **150 MB**. If the PDF is large, the figure probably contains embedded bitmap data — re-export from vector source data, not from a screen-grabbed raster.

## Permissions checklist

If you reproduced a figure from another paper or a dataset with restricted terms, you may need:

- Permission from the original publisher (most allow use in a derivative work after embargo).
- A credit line in the caption, e.g., *"Figure adapted from Smith et al. 2023 with permission."*

The skill does not manage permissions — that's the author's job.
