---
name: itut-drafting
description: "ITU-T-specific contribution document drafting: template structure, header table fields, style-name mapping, equation conventions, and batch workflows. Use when preparing or editing ITU-T contribution .docx files (C-series or TD-series). Delegates formatting rules to sdo-docx-formatting and officecli operations to sdo-docx-operations."
---

# ITU-T Contribution Drafting

Use this skill for ITU-T-specific document structure, template conventions,
and concrete Word style names. For formatting rules (headings, enumerations,
notes, tables, figures, citations), see `sdo-docx-formatting`. For officecli
operations (tab-run injection, field codes, bookmarks), see
`sdo-docx-operations`.

## Critical rules from delegated skills

These key constraints are inlined here to reduce cross-referencing:

**From `sdo-docx-formatting`:**
- Apply formatting through **named styles** from the template, never manual
  overrides (bold, italic, font size, colour).
- Keep numbering **update-safe** — use SEQ fields and bookmarks, never
  hard-coded numbers.
- Use **non-breaking spaces** (`\u00a0`) for semantic units (number+unit,
  Figure/Table+number).
- Use **real tab runs** (`<w:tab/>`), never spaces, for structural tabs
  (heading number+title, enumeration bullet+text, note label+text).

**From `sdo-docx-operations`:**
- Open in resident mode (`officecli open <doc>`) before multi-step edits;
  close at end.
- Prefer style/ordinal or explicit XPath targeting, not paraId targeting.
- Never use `raw-set --action replace` with an empty XML payload.
- Always preserve non-breaking spaces and explicit tab runs.
- Validate with `officecli validate <doc>` after every major batch update.

## Assets

- `assets/template.docx` -- canonical ITU-T contribution Word template with
  all required styles and header structure (9-row header table, abstract
  table, running header, footer). Copy or use as reference when starting a
  new contribution. This is a user-provided template carrying ITU-T branding,
  predefined styles, and placeholder content. Do **not** modify the original;
  always work on a copy.

---

## ITU-T style-name mapping

Concrete Word style IDs for ITU-T documents. Use these when applying
formatting rules from `sdo-docx-formatting`.

| Abstract name (`sdo-docx-formatting`) | ITU-T concrete style ID | Notes |
|---|---|---|
| `body-text` | `Body Text` | If absent, fall back to `Normal`; verify with `officecli get <doc> /styles` |
| `heading-1` | `Heading 1` | Section headings (numbered) |
| `heading-2` | `Heading 2` | Subsection headings |
| `heading-3` | `Heading 3` | Sub-subsection headings |
| `enum-1` | `enumlev1` | First-level enumeration |
| `enum-2` | `enumlev2` | Second-level enumeration |
| `enum-3` | `enumlev3` | Third-level enumeration (if used) |
| `table-caption` | `Table_No & title` | officecli styleId: `TableNotitle` |
| `table-header` | `Table_head` | officecli styleId: `Tablehead` |
| `table-data` | `Table_text` | officecli styleId: `Tabletext` |
| `table-note` | (varies by template) | If not found in template, omit styling and add a TODO comment for manual review |
| `figure-para` | `Figure` | Paragraph containing image |
| `figure-caption` | `Figure_No & title` | Below figure |
| `figure-note` | (varies by template) | If not found in template, omit styling and add a TODO comment for manual review |
| `note-main` | `Note` | Last note in block |
| `note-continuation` | (varies by template) | If not found in template, omit styling and add a TODO comment for manual review |
| `reference-entry` | `References` | Each references entry |
| `code-text` | `Macro Text` | officecli styleId: `MacroText` |

Additional ITU-T-specific styles (no abstract equivalent):

| Style ID | Purpose |
|----------|---------|
| `Equation` | Display equation paragraph (centred equation + right-aligned label via tab stops) |
| `Equation_legend` | officecli styleId: `Equation_legend` -- annotation paragraph following equation |
| `Headingb` | Sub-headings within a proposed clause block (not auto-numbered) |
| `TSBHeaderSummary` | Abstract table cell content |

---

## Template structure

ITU-T contribution documents use a structured header **table** (not
paragraphs). This differs from 3GPP.

### Header table (`/body/tbl[1]`)

9 rows with the following cell layout:

| Row | Cell | Content |
|-----|------|---------|
| tr[1]/tc[3] | Document number | 3rd run is the highlighted placeholder; set text to `0xxx` |
| tr[4]/tc[2] | Question(s) | e.g. `Question 9/12` |
| tr[4]/tc[3] | Place and date | e.g. `Geneva, 09-17 June 2026` |
| tr[6]/tc[2] | Source organization | e.g. `HEAD acoustics GmbH` |
| tr[7]/tc[2] | Title | Contribution title |
| tr[8]/tc[2] | Contact 1 | Tab-separated: `Name\tOrganization\tCountry` |
| tr[8]/tc[3]/p[1]/r[4] | Tel number | Highlighted run |
| tr[8]/tc[3]/p[1]/r[8] | E-mail | Highlighted run |
| tr[9] | Contact 2 | Clear with `""` if unused |

### Abstract table (`/body/tbl[2]`)

1 row x 2 cells: `"Abstract:"` label (tc[1]) + content (tc[2]/p[1]).

### Running header

`/header[1]/p[@paraId=00100052]/r[4]` -- document number (e.g. `SG12-C0xxx`).

### Instruction paragraphs to delete

Remove all 8 yellow-highlighted instruction paragraphs (paraIds
`0010003A` through `00100048`) using `remove` commands in a setup batch
before adding content.

### Horizontal rule

`/body/p[@paraId=0010004C]` -- `_______________________` separator.

### First content paragraph

`/body/p[@paraId=0010004E]` -- empty paragraph after the rule; first
content goes after this.

> **Key finding:** The ITU-T template may NOT contain a `Body Text` style.
> If absent, use `Normal` for body paragraphs. Always verify with
> `officecli get <doc> /styles --depth 1` on any new template.

---

## Equation conventions

### Display equations (numbered, standalone)

Use a **single paragraph** with style `Equation` containing
`\t[inline equation]\t(7-X)`. The `Equation` style has two tab stops:
first centred (for the equation), second right-aligned (for the label).
This centres the equation and right-aligns the label on the same line.
Set paragraph `alignment: left` so the tab stops (not paragraph
justification) control positioning — `left` here means "do not
centre-justify the paragraph itself," not "left-align the equation."

Target structure:

```
[p intro sentence]
[p style=Equation]  <- \t + inline oMath + \t(7-X)  -- one paragraph
[p ind.left=720]    <- "where..." annotation paragraph
```

Build with officecli in order:

```json
[
  { "command": "set", "path": "/body/p[@paraId=XXXX]",
    "props": { "style": "Equation", "alignment": "left", "text": "\t" } },
  { "command": "add", "parent": "/body/p[@paraId=XXXX]", "type": "equation",
    "props": { "mode": "inline", "formula": "..." } },
  { "command": "add", "parent": "/body/p[@paraId=XXXX]", "type": "run",
    "props": { "text": "\t(7-A)" } }
]
```

**IMPORTANT:** Do NOT combine `ind.left` with `alignment` in a single
`add` paragraph command. officecli emits `w:ind` AFTER `w:jc` in the
OOXML, violating the schema. Use a separate `set` call to add indentation
after creation.

### Inline equations in body text

Rebuild paragraphs with mixed text + inline equations as a sequence of
`set` + `add` commands (run, equation, run, ...). Each JSON array
passed to `officecli batch` must contain at most 12 JSON command objects.
If more are needed, split into sequential batch calls.

### Known KaTeX constraints

| Forbidden | Use instead |
|---|---|
| `\text{word}` | `\mathrm{word}` |
| `\left(...\right)` with sub/superscripts inside | plain `(...)` -- OMML auto-sizes |
| `\tag{label}` | Put label in the same paragraph with tab |
| `\mathcal{L}` | `\mathit{L}` |

---

## Heading conventions (ITU-T-specific)

- **No hard-coded numbers in heading text.** The template's heading styles
  have automatic outline numbering. Write just the title: `"Introduction"`
  not `"1\tIntroduction"`.
- `Headingb` style is used for sub-headings *within a proposed clause
  block* (e.g. `"7.5.4 Maximum absolute prediction error (maxabs)"`,
  subsection labels `"a)\tUnconstrained least-squares fit"`). These appear
  in the TOC as `Heading_b` entries but do NOT get automatic numbering.

---

## Batch workflow patterns

### General workflow

1. **Start from template**: `Copy-Item "docs\template.docx" -Destination "<output>.docx" -Force`
2. **Resident mode**: `officecli open <doc>` before editing; `officecli close <doc>` at end.
3. **Batch mode**: pipe JSON arrays to `officecli batch <doc>`. Each JSON
   array must contain at most 12 JSON command objects. If more are needed,
   split into sequential batch calls.
4. **Validate frequently**: `officecli validate <doc>` after every major
   batch update.

### Common errors

| Error | Root Cause | Fix |
|-------|-----------|-----|
| Conclusion heading missing | Batch added heading + table together; table `set` commands failed (index didn't exist yet) | Split: add heading separately, then table, then fill with dedicated batch |
| `\left\right` with subscripts crashes equation | OMML parser limitation | Use plain `(` `)` delimiters |
| "Body Text" style not found | Template uses `Normal` as body style | Use `Normal` for body paragraphs |
| Running header shows placeholder | Header paragraph r[4] not updated | Target `/header[1]/p[@paraId=00100052]/r[4]` and set text |
| `ind.left` + `alignment` in one command | Schema ordering bug in officecli | Split into separate `add` + `set` calls |

### Indentation for proposed clause text

Text inside a proposed new/amended clause uses `"ind.left":"720"`
(720 twips = 0.5 inch). Sub-items use `"ind.left":"1080"`.

---

## Cross-references

- `sdo-project-setup` -- common project bootstrap (layout, metadata sync, autodetection)
- `sdo-docx-formatting` -- formatting rules (delegated; see mapping above)
- `sdo-docx-operations` -- officecli guardrails for raw-set, field codes, bookmarks
- `sdo-writing-style` -- prose quality rules
- `sdo-writing-conventions` -- mechanical writing rules
- `itut-basics` -- ITU-T organisation context
- `itut-contributions` -- contribution types and numbering
- `itut-patents` -- patent policy, IPR disclosure, licensing declarations
- `itut-recommendations` -- Recommendation structure and approval
