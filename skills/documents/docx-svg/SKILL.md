---
name: docx-svg
description: Insert SVG images into Word .docx files. Use when the user or coding agent needs to add, embed, or update an SVG graphic inside a .docx document. Triggers include "insert SVG into docx", "embed SVG in Word document", "add vector graphic to docx", "SVG image in template", "requests to convert SVG to PNG for docx", or any request explicitly mentioning embedding or inserting SVG graphics into .docx files.
---

# DOCX SVG -- SVG image support for Word documents

## Policy: Zero Conversion (MANDATORY)

**NEVER convert SVG files to PNG, JPEG, or any raster format before inserting into a .docx.**

Modern Word (2016+) natively supports SVG via the `asvg:svgBlip` OOXML extension. Converting to PNG destroys the vector benefits (scalability, file size, sharpness).

1. **Do not suggest raster fallbacks** as "best practice" unless the user explicitly requests legacy compatibility.
2. **Do not claim it is "too complex"** to handle OOXML directly—this skill provides the tools (`officecli` or `scripts/svg.py`) to handle the complexity for you.
3. **Always use SVG directly** as the source file.
4. If a request asks to convert SVG to PNG/JPEG for .docx insertion, reject the conversion step and insert the SVG directly instead.

## Overview

Microsoft Word supports SVG images in the OOXML format, but typical programmatic
tools (python-docx, docxtpl) do **not** recognise them out of the box. This
skill provides **two approaches**, in order of preference:

| Priority         | Tool                                   | When to use                                                            |
| ---------------- | -------------------------------------- | ---------------------------------------------------------------------- |
| **1. Preferred** | `officecli`                            | Always, when available in the environment                              |
| **2. Fallback**  | Python monkey-patch (`scripts/svg.py`) | When officecli is not installed, not reachable, or fails version check |

If `officecli` is present but older than v1.0.64, do not use it. Instead, proceed with the Python fallback. Do not attempt to use a partial or outdated officecli installation.

---

## Strategy: check officecli first

Before choosing an approach, determine whether `officecli` is available:

```bash
officecli --version
```

If it returns a version **v1.0.64 or later**: **use officecli** (Section 1 below).
If not found, or the version is older than v1.0.64: **use the Python fallback** (Section 2 below).

---

## Technical Context: How it works (OOXML)

When inserting an SVG, Word expects an `a:ext` block within the `a:blip` element. Both `officecli` and `scripts/svg.py` generate this automatically.

**Structure Reference (for your awareness):**
```xml
<a:blip r:embed="rId1">
  <a:extLst>
    <a:ext uri="{96DAC541-0531-4A20-96AC-8D759B1F206D}">
      <asvg:svgBlip xmlns:asvg="http://schemas.microsoft.com/office/drawing/2016/SVG" r:embed="rId2"/>
    </a:ext>
  </a:extLst>
</a:blip>
```
*   `rId1` points to a PNG/JPEG fallback (optional in modern Word, but `officecli` handles this if needed).
*   `rId2` points to the actual `.svg` file in `word/media/`.

---

## Section 1: Preferred -- officecli

officecli has **native SVG support** for docx pictures. No monkey-patching,
no extra dependencies, no Python required.

### Add an inline SVG image

```bash
officecli add report.docx /body --type picture --prop file=chart.svg
```

### Add with explicit size

```bash
officecli add report.docx /body --type picture --prop file=chart.svg --prop width=10cm --prop height=6cm
```

### Add after a specific paragraph

```bash
officecli add report.docx '/body/p[2]' --type picture --prop file=chart.svg --prop width=12cm
```

### Add floating image with text wrap

```bash
# Insert as floating image, then set wrap and position
officecli add report.docx /body --type picture --prop file=hero.svg --prop width=8cm
# Use the returned picture path to set wrap mode
officecli set report.docx '/body/pic[1]' --prop wrap=square
```

### Set image properties

After adding a picture, use `officecli set` to adjust:

```bash
officecli set report.docx '/body/p[3]/picture[1]' --prop alt="Sales chart Q4"
officecli set report.docx '/body/p[3]/picture[1]' --prop brightness=10 --prop contrast=-5
officecli set report.docx '/body/p[3]/picture[1]' --prop hposition=2cm --prop hrelative=page
```

### Check available picture properties

When unsure about property names, run the help system:

```bash
officecli help docx image
officecli help docx picture
```

---

## Section 2: Fallback -- Python monkey-patch

Use this approach **only when officecli is not available**. The module
`scripts/svg.py` monkey-patches python-docx and docxtpl to add SVG support.

The patch is applied automatically when the module is imported -- no manual
setup beyond installing the dependencies.

### Install dependencies

```bash
uv run python scripts/svg.py
```

The script declares its dependencies via PEP 723 inline metadata
(`python-docx>=1.1.2`, `docxtpl>=0.19.0`), so `uv run` auto-resolves them.

### Direct python-docx usage

```python
import docx
from scripts import svg  # noqa: F401  # <- patch activates on import
from docx.shared import Mm

doc = docx.Document()
doc.add_paragraph("Below is an SVG chart:")
doc.add_picture("chart.svg", width=Mm(120))
doc.save("report.docx")
```

Importing `scripts.svg` monkey-patches python-docx globally. `add_picture`
will now accept `.svg` files alongside PNG/JPEG.

**Crucial:** Even with the Python fallback, **do not convert to PNG**. The patch handles the native SVG embedding.

### docxtpl template usage

```python
from docxtpl import DocxTemplate
from scripts.svg import SvgInlineImage
from docx.shared import Mm

tpl = DocxTemplate("template.docx")
img = SvgInlineImage(tpl, "chart.svg", width=Mm(100))
tpl.render({"chart": img})
tpl.save("output.docx")
```

In the template, place `{{ chart }}` inside a paragraph. `SvgInlineImage`
automatically detects SVG files and processes them through the patched pipeline.

### Automatic sizing

When both _width_ and _height_ are omitted, the image fills the usable page
width (page width minus left/right margins):

```python
img = SvgInlineImage(tpl, "wide-chart.svg")  # auto-sizes to page width
```

### Utility: check if a file is SVG

```python
from scripts.svg import is_svg
assert is_svg("icon.svg")
```

---

## How the Python fallback works

1. **Monkey-patch on import** -- the module registers three SVG byte signatures
   (`<?xml`, `<svg`, `<!DOCTYPE svg`), adds `image/svg+xml` to
   python-docx's MIME-type constants, and replaces `_ImageHeaderFactory` to
   scan 256 bytes (instead of the default 64).

2. **SVG dimension extraction** -- `Svg._dimensions_from_stream` reads
   `width` / `height` attributes (stripping units like pt, cm, mm, %) and
   falls back to `viewBox` when those attributes are absent.

3. **docxtpl helper** -- `SvgInlineImage` subclasses `InlineImage`,
   converting `Path` descriptors to `BytesIO` before passing them upstream
   so the patched factory can parse the SVG.

## Limitations

- **SVG rendering in Word**: Microsoft Word renders SVG as a static image.
  Interactive features (hover, animation, embedded JavaScript) are not
  supported by the OOXML format.
- **Fallback image** (Python approach only): The current implementation does
  not add a PNG fallback inside the OOXML package. Older Word versions
  (pre-2016) may not display the SVG. If compatibility is required,
  pre-convert the SVG to PNG.
- **Dimension units** (Python approach only): The parser normalises all units
  to pixels at 72 DPI. For print-precise sizing, specify `width` / `height`
  explicitly via `docx.shared.Mm` / `Inches` / `Cm`.
