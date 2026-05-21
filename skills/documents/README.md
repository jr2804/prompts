# Document Processing Skills

This directory contains skills for working with various document formats.

## Skills

| Skill | Description |
|-------|-------------|
| **docx** | Word document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction |
| **xlsx** | Spreadsheet creation, editing, and analysis with formulas, formatting, data analysis, and visualization |
| **pptx** | Presentation creation, editing, and analysis — supports OOXML editing, PptxGenJS, and HTML-to-PPTX workflows |
| **pdf** | PDF manipulation including text/table extraction, creation, merging/splitting, and form handling |

## Origin

These skills are based on the [Anthropic skills repository](https://github.com/anthropics/skills/tree/main/skills) with local enhancements.

## Directory Structure

Each skill follows the same layout:

```
skill-name/
├── SKILL.md          # Skill definition and main documentation
├── LICENSE.txt       # License
├── assets/           # Static assets (schemas, etc.)
├── references/       # Detailed reference documentation
└── scripts/          # Python and JavaScript scripts
    ├── helpers/      # Shared helper modules
    ├── validators/   # XML validation modules
    └── templates/    # XML templates (where applicable)
```

## Running Helper Scripts

All helper scripts should be run using `uv`:

```bash
uv run <script-path>
```

This replaces older patterns like `python <script>` or direct script execution.
