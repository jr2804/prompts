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

## Term formatting (clause 3 Definitions)

Terms in clause 3 (both 3.1 "Terms defined elsewhere" and
3.2 "Terms defined in this Recommendation") use **pseudo-subclause**
formatting:

- Numbered like subclauses (3.1.1, 3.1.2, ...) but are NOT heading
  paragraphs — they do NOT appear in the table of contents
- Style: `Normal` (body-text style, fallback if `Body Text` absent)
- Each term is a single paragraph in the format:

  `<bold>3.1.N\tTERM NAME</bold>: definition text`

### Run structure

| Run | Content | Format |
|-----|---------|--------|
| r[1] | `3.1.N` (number prefix) | bold |
| r[2] | `<w:tab/>` | bold (on run) |
| r[3] | term name | bold |
| r[4] | `: ` + definition text | normal |

### Tab stop

The ITU-T template's `Normal` style does **not** include a tab stop at
1.5 cm. Each term paragraph must have this added manually:

```xml
<w:pPr>
  <w:tabs>
    <w:tab w:val="left" w:pos="851"/>
  </w:tabs>
</w:pPr>
```

851 twips = 1.5 cm. Use `raw-set` to inject this since officecli L2
`set` on a paragraph with revision marks does not create tracked
changes.

### Creating terms with tracked changes

Since officecli L2 `set`/`add` does not create revision marks, terms
must be built via `raw-set` with the content wrapped in `w:ins`
elements:

```xml
<w:p xmlns:w="..." xmlns:w14="..." w14:paraId="PARAID">
  <w:pPr>
    <w:tabs>
      <w:tab w:val="left" w:pos="851"/>
    </w:tabs>
  </w:pPr>
  <w:ins w:author="Author Name" w:date="..." w:id="...">
    <w:r>
      <w:rPr><w:b/></w:rPr>
      <w:t xml:space="preserve">3.1.N</w:t>
    </w:r>
    <w:r>
      <w:rPr><w:b/></w:rPr>
      <w:tab/>
    </w:r>
    <w:r>
      <w:rPr><w:b/></w:rPr>
      <w:t xml:space="preserve">TERM NAME</w:t>
    </w:r>
    <w:r>
      <w:t xml:space="preserve">: definition text</w:t>
    </w:r>
  </w:ins>
</w:p>
```

Replace the target paragraph via:

```
officeli raw-set <doc> /document \
  --xpath '//w:p[@w14:paraId="PARAID"]' \
  --action replace \
  --xml '<w:p>...</w:p>'
```

### Notes attached to terms

A `Note`-style paragraph that belongs to a term (e.g., clarifying a
definition) stays after the term paragraph with style `Note`. These are
not pseudo-subclauses — use the standard note formatting convention.

---

## Table and figure numbering (per-clause counters)

ITU-T Recommendations use **per-clause** SEQ field counters for tables
and figures. This differs from the generic `sdo-docx-formatting` convention
(global `SEQ Figure` / `SEQ Table`).

### SEQ field naming

| Element | SEQ field name | Bookmark prefix | Caption style ID |
|---------|---------------|-----------------|-------------------|
| Figures | `FIG<N>` where N = clause number | `FIG_` | `FigureNotitle0` (`Figure_No & title`) |
| Tables | `TAB<N>` where N = clause number | `TAB_` | `TableNoTitle` (`Table_No & title`) |

Examples:
- Clause 6 figures: `SEQ FIG6`, bookmarks `FIG_EQUIPMENT_*`
- Clause 8 tables: `SEQ TAB8`, bookmarks `TAB_SETUP_*`

### Caption structure

```
Figure\u00a0<N>-{SEQ FIG<N>}: caption text
Table\u00a0<N>-{SEQ TAB<N>}: caption text
```

- The clause-number prefix (`6-`) is hardcoded text before the field
- The SEQ field provides the running number within the clause
- A non-breaking space separates "Figure"/"Table" from the number
- The bookmark wraps around the full compound number (`6-1`, `6-2`, etc.)
  — start bookmark before the `6-` run, end bookmark after the field end

### Bookmark naming

Use `FIG_` / `TAB_` prefix followed by a short descriptive name in
UPPER_SNAKE_CASE. Follow the naming scheme already used in the document:
- Look at existing bookmarks in nearby clauses for the naming pattern
- Choose a 1–2 word description that fits the topic
- Examples: `FIG_EQUIPMENT_RRS_SP`, `TAB_SIGNALS_ACCURACYMEASUREMENTS`

### Run-level structure for a correct caption

```
r[1]   run          "Figure "           (non-breaking space)
       bookmark     (around 6-N)         name="FIG_xxx"
r[2]   run          "6-"
r[3]   fieldChar    begin
r[4]   instrText    " SEQ FIG6 "
r[5]   fieldChar    separate
r[6]   run          "N"                 (field result)
r[7]   fieldChar    end
       bookmarkEnd
r[8]   run          ": caption text"
```

### Cross-references

Body text references use `REF` fields pointing to the bookmark:

```
{ REF FIG_EQUIPMENT_RRS_SP \h }
{ REF TAB_SIGNALS_ACCURACYMEASUREMENTS \h }
```

### Procedure: fix table/figure numbering in a clause

When asked to "fix table/figure numbers in clause N", follow this workflow:

1. **Analyse**: Scan all figure/table captions in the clause. For each,
   check:
   - Does it have a `SEQ FIG<N>` / `SEQ TAB<N>` field?
   - Does it have a bookmark with `FIG_` / `TAB_` prefix?
   - Is the number hardcoded (no field) or auto-numbered?
   - Are there duplicate numbers?

2. **Add missing SEQ fields**: For captions with hardcoded numbers,
   replace the hardcoded number with `{SEQ FIG<N>}` / `{SEQ TAB<N>}`.

3. **Add missing bookmarks**: For captions without bookmarks, add a
   bookmark around the compound number (`N-M`). Choose a descriptive
   name that fits the naming pattern of existing bookmarks in that
   clause.

4. **Fix duplicate numbers**: If adding SEQ fields changes the sequence
   order, the field results will auto-update. If a figure/table has a
   duplicate hardcoded number, let the SEQ field resolve it — do not
   assign numbers manually.

5. **Check cross-references**: Search the clause body text for `REF`
   fields. Verify each references a bookmark that still exists with
   the correct name. If a hardcoded reference (plain text "Figure 6-3")
   is found, replace it with a `{REF <bookmark> \h}` field.

6. **Rebuild captions**: Use `raw-set` with `--action replace` targeting
   `//w:p[@w14:paraId="PARAID"]` to replace each caption paragraph with
   a correctly structured one. The replacement XML must include:
   - `w:pPr` with the correct style (`FigureNotitle0` / `TableNoTitle`)
   - Bookmark start/end around the number
   - SEQ field (begin/instrText/separate/result/end)
   - Caption text after the field

7. **Refresh fields**: Run `officecli refresh <doc>` to re-evaluate all
   SEQ and REF fields.

8. **Verify**: Check field results in the raw XML:
   ```bash
   officecli raw <doc> /document | grep -A1 'fldCharType="separate"'
   ```

### Common pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| Duplicate figure/table numbers | Missing SEQ field, hardcoded number | Add SEQ field; let field auto-resolve |
| Cross-reference shows wrong number | REF bookmark name doesn't match caption bookmark | Update REF instruction to point to correct bookmark |
| Caption shows empty number | `officecli refresh` didn't update the field | Re-run `officecli refresh`; check raw XML for result |
| Bookmark name doesn't match nearby pattern | Newly invented name inconsistent with document | Review existing bookmarks in clause; match the naming scheme |

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
