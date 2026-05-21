# Headings

## Critical constraints

- **Never use MS Word automatic numbering** for sections or subsections.
  Automatic numbering causes formatting inconsistencies and can break
  references when using revision marks.

## Numbering format

- Section: `N` (e.g. `1`)
- Subsection: `N.M` (e.g. `2.1`)
- Sub-subsection: `N.M.P` (e.g. `2.1.1`)
- The `Introduction` clause is numbered like any other section
  (e.g. `1\tIntroduction`).

## Formatting

- Insert a real `<w:tab/>` run element between the heading number and the
  heading title; never use spaces for indentation (see
  `sdo-docx-operations` for officecli tab-run injection patterns).
- Use heading styles by level:
  `heading-1` (→ concrete style), `heading-2`, `heading-3`, etc.
- Do not apply manual font-size or bold overrides to heading paragraphs --
  rely on style definitions.
- The `References` section is the **last** section and does **not** get a
  number. Use `heading-1` style but write only the word `References` without
  a manual number prefix.

## Style mapping

| Abstract | Concrete (per SDO drafting skill) |
|----------|-----------------------------------|
| `heading-1` | SDO-specific style for top-level headings |
| `heading-2` | SDO-specific style for second-level headings |
| `heading-3` | SDO-specific style for third-level headings |
