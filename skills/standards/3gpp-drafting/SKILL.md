---
name: 3gpp-drafting
description: "3GPP-specific TDoc authoring conventions: metadata schema, template substitution, revision workflow, DOCX property sync, project layout, and 3GPP style-name mapping. Use when preparing, updating, or validating 3GPP TDoc .docx files for meeting submissions. Delegates formatting rules to sdo-docx-formatting and officecli operations to sdo-docx-operations."
---

# 3GPP TDoc Drafting

Use this skill for 3GPP-specific document structure, metadata conventions,
and concrete Word style names. For formatting rules (headings, enumerations,
notes, tables, figures, citations), see `sdo-docx-formatting`. For officecli
operations (tab-run injection, field codes, bookmarks), see
`sdo-docx-operations`.

## Assets

- `assets/Tdoc_Template.docx` -- canonical Word template with all required
  3GPP styles. Copy to `ref/Tdoc_Template.docx` when initializing a new
  project (see `sdo-project-setup` for the common project bootstrap workflow).
  This is a user-crafted file containing all required styles
  (`B1`, `B2`, `NO`, `NW`, `TH`, `TAH`, `TF`, `EX`, `PL`, etc.) and is
  **not** tied to an official 3GPP release cycle.

## References

- `references/frontmatter.md` -- 3GPP-specific PLAN.md metadata keys.
- `references/template-substitution.md` -- Jinja2 placeholder substitution
  for the 3GPP TDoc template.
- `references/revision-workflow.md` -- 3GPP-specific header structure and
  copy-rename-patch procedure for revisions.

> **Moved to `sdo-project-setup`:** project layout, AGENTS.md template,
> universal project prompt, and `set_docx_props.py` (now generalized with a
> `--props` parameter). Load `sdo-project-setup` for these common functions.

---

## 3GPP style-name mapping

Concrete Word style IDs for 3GPP documents. Use these when applying
formatting rules from `sdo-docx-formatting`.

| Abstract name (`sdo-docx-formatting`) | 3GPP concrete style ID | Purpose |
|---|---|---|
| `body-text` | `Normal` | Main body paragraphs |
| `heading-1` | `Heading 1` | Top-level section heading |
| `heading-2` | `Heading 2` | Second-level section heading |
| `heading-3` | `Heading 3` | Third-level section heading |
| `enum-1` | `B1` | First-level enumeration (en-dash bullet) |
| `enum-2` | `B2` | Second-level enumeration |
| `enum-3` | `B3` | Third-level enumeration (if used) |
| `table-caption` | `TH` | Table caption (above table) |
| `table-header` | `TAH` | Table header row |
| `table-data` | `TAC` | Table data rows |
| `table-note` | `TAN` | Table merged-bottom-row note |
| `figure-para` | `FL` | Paragraph containing image |
| `figure-caption` | `TF` | Figure caption (below figure) |
| `figure-note` | `NF` | Note below figure, before caption |
| `note-main` | `NO` | Last note in a consecutive block |
| `note-continuation` | `NW` | Preceding notes in a block |
| `reference-entry` | `EX` | Each references section entry |
| `code-text` | `PL` | Inline code, function/variable names, filenames |

Additional 3GPP-specific styles (no abstract equivalent):

| Style ID | Purpose |
|----------|---------|
| `TDoc-Header` | Cover page header paragraphs (TDoc number, date, source, title, agenda item, target) |

## Heading conventions (3GPP-specific override)

3GPP headings use **manual numbering only** (never Word auto-numbering).
See `sdo-docx-formatting/references/headings.md` for full rules. The
`References` section is unnumbered and always the last section.

## Cross-references

- `sdo-project-setup` -- common project bootstrap (layout, metadata sync, autodetection)
- `sdo-docx-formatting` -- formatting rules (delegated; see mapping above)
- `sdo-docx-operations` -- officecli guardrails for raw-set, field codes, bookmarks
- `sdo-writing-style` -- prose quality rules
- `sdo-writing-conventions` -- mechanical writing rules (spelling, numbers, abbreviations)
- `3gpp-basics` -- 3GPP organisation context
- `3gpp-meetings` -- meeting structure and identifiers
- `3gpp-tdocs` -- TDoc numbering patterns and FTP access
- `3gpp-change-request` -- CR procedure when the contribution is a CR
