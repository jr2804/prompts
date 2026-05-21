# Tool Usage

## Primary tool: officecli

Use `officecli` as the primary tool for all Word document editing.
Preferred invocation order:

1. Via the MCP server `officecli` (if available in the session).
2. Via the `officecli` CLI in the terminal: verify availability first with
   `officecli --help`.
3. If the CLI is not on PATH, use `everything-search` (if available) to
   locate `officecli.exe`, then invoke with the full path.

## Secondary tool: python-docx (fallback only)

Use `python-docx` only for specific tasks that cannot be done with
`officecli`, such as programmatic table creation or image insertion. Do not
use it for general document editing -- it does not support all template
styles and can introduce formatting inconsistencies.

## Figures and illustrations

- Use the Draw.io MCP server as the primary tool for creating diagrams.
- As a fallback, use the `drawio` skill for file-based diagram creation
  via the Draw.io desktop app.

## SVG export

Always export figures in SVG format for maximum quality in Word. If SVG
insertion fails:

1. First fallback: use python-docx with the SVG patch (`docx-svg` skill).
2. Last fallback: export as PNG at >= 300 dpi.

When exporting Draw.io diagrams to SVG, follow the
[Draw.io SVG text rendering guidelines](https://www.drawio.com/doc/faq/svg-export-text-problems)
to prevent text display issues in Word.
