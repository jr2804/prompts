---
name: sdo-docx-formatting
description: Reusable .docx formatting conventions for formal standardization documents. Use when formatting headings, notes, enumerations, tables, figures, cross-references, citations, and text in technical standards documents. Applies across SDOs -- concrete style names are provided by the per-SDO drafting skill. Triggers include "format this document", "apply styles", "add cross-references", "insert table/figure", "format notes or citations".
---

# Standards Document Formatting

Apply these conventions for formal technical documents across all SDOs
(3GPP, ETSI, ITU-T). This skill describes **what** to do at the conceptual
level. Concrete Word style names vary per SDO and are provided by the
per-SDO drafting skill (`3gpp-drafting`, `etsi-drafting`, `itut-drafting`).

## Core rules

1. Apply formatting through **named styles** defined in the document template,
   never through manual formatting (bold, italic, font size, colour overrides).
2. Keep numbering and references **update-safe** -- use SEQ fields and
   bookmarks, never hard-coded numbers.
3. Use **non-breaking spaces** (`\u00a0`) for semantic units (number+unit,
   Figure/Table+number).
4. Use **real tab runs** (`<w:tab/>`), never spaces, for tab-separated
   structural elements (heading number+title, enumeration bullet+text,
   note label+text). See `sdo-docx-operations` for officecli patterns.

## Style-name abstraction

This skill uses **abstract style names**. Each SDO drafting skill provides
the concrete mapping. Example:

| Abstract name | Purpose | 3GPP / ETSI | ITU-T |
|---|---|---|---|
| `body-text` | Main body paragraphs | `Normal` | `Body Text` |
| `heading-1` through `heading-3` | Section headings | `Heading 1`--`Heading 3` | `Heading 1`--`Heading 3` |

Always consult the per-SDO drafting skill for the correct concrete style IDs.

## Conventions by domain

- [references/headings.md](references/headings.md)
- [references/enumerations.md](references/enumerations.md)
- [references/notes.md](references/notes.md)
- [references/tables-figures.md](references/tables-figures.md)
- [references/citations.md](references/citations.md)
- [references/text-formatting.md](references/text-formatting.md)

## Cross-references

- `sdo-docx-operations` -- officecli patterns for tab-run injection, field-code injection, bookmark insertion
- `sdo-writing-style` -- prose quality rules for the textual content
- Per-SDO drafting skill (`3gpp-drafting`, `etsi-drafting`, `itut-drafting`) -- concrete style name mapping
