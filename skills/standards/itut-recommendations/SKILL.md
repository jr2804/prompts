---
name: itut-recommendations
description: 'ITU-T Recommendation structure, approval processes, amendment/corrigendum procedures, and ITU-T | ISO/IEC common text conventions. Use when the agent needs to understand how ITU-T Recommendations are structured (clause order, element types, annex conventions), approved (TAP/AAP), amended, or how joint ITU-T/ISO/IEC texts work. Sources: Rec. ITU-T A.1 (09/2019) + Rules for presentation of ITU-T | ISO/IEC common text (2014).'
---

# ITU-T Recommendations -- structure & approval

## Document types by lifecycle stage

| Document type | Meaning | Approval |
|---------------|---------|----------|
| **Recommendation** | Normative output of a study group | TAP or AAP |
| **Amendment** | Changes/additions to published Recommendation | Same approval as the Recommendation |
| **Corrigendum** | Corrections to published Recommendation | Same approval as amendment |
| **Erratum** | Publication/editorial error fix | Published by TSB with Chairman concurrence (no SG approval) |
| **Annex** (integral) | Material necessary for completeness | Same approval as Recommendation |
| **Appendix** (non-integral) | Supplementary, not essential | Agreed by study group (not full approval) |

______________________________________________________________________

## Recommendation clause structure

Per the Rules for presentation of ITU-T | ISO/IEC common text, a
Recommendation is organized as follows:

| Clause | Element | Content |
|--------|---------|---------|
| *(preliminary)* | Cover page, Contents, Foreword, Introduction | Roman numeral pages |
| 1 | **Scope** | Defines subject and limits; no requirements |
| 2 | **Normative references** | Documents whose provisions are referenced normatively |
| 3 | **Definitions** *(optional)* | Terms defined for this Recommendation. Subdivided into 3.1 "Terms defined elsewhere" and 3.2 "Terms defined in this Recommendation" (if both are used). See term formatting below. |
| 4 | **Abbreviations** *(optional)* | All abbreviations used in the text |
| 5 | **Conventions** *(optional)* | Any particular notation used |
| 6+ | **Text** | Body of the Recommendation |
| Annex A+ | **Integral annexes** | Normative material (same approval as Recommendation) |
| Annex (continues) | **Non-integral annexes** | Informative/supplementary (SG agreement, not full approval) |
| *(last, optional)* | **Bibliography** | Informative references not cited normatively; heading style `Appendix_No & title` with page break before |
| *(last)* | **Index** *(optional)* | |

### Canonical skeleton template

For new Recommendation drafting and for checking currently published Word
style definitions, use the local downloaded skeleton first:

- `assets/itu-t-recommendation-skeleton.docx`

Upstream source URL (for refresh):

- `https://www.itu.int/en/ITU-T/studygroups/Documents/Doc-ITUT-Recs-Skelet.docx`

### Term formatting (clause 3)

Terms in clause 3 are formatted as **pseudo-subclauses**: they carry
subclause-style numbering (3.1.1, 3.1.2, ...) but are not real heading
paragraphs and do **not** appear in the table of contents.

Each term follows this pattern:

```
<bold>3.1.N\tTERM NAME</bold>: definition text
```

- The number prefix (`3.1.N`) and term name are **bold**
- A **tab** separates the number from the term name
- The term name ends with a **colon** and space, followed by the definition
  text (not bold)
- The paragraph uses `body-text` style with a manually set tab stop at
  1.5 cm (851 twips) — this tab stop is not part of the default
  `Normal` style in the ITU-T template

This format applies to both 3.1 "Terms defined elsewhere" and
3.2 "Terms defined in this Recommendation".

### Subdivision numbering

- Digits separated by periods: 1, 1.1, 1.1.1
- No trailing period after single number
- Do not create subclause 1.1 unless 1.2 also exists

______________________________________________________________________

## Bibliography

The Bibliography is an **optional, non-normative** clause containing
informative references (sources not cited normatively in the body).

- **Position:** Always the last clause of the Recommendation, after all
  integral and non-integral annexes (and before the Index if present).
- **Heading:** Formatted with style `Appendix_No & title` (the same style
  used for non-integral appendix headings). Write only the word
  `Bibliography` — no number prefix.
- **Page break:** There **must** be a page break immediately before the
  Bibliography heading. Apply it as `pageBreakBefore: true` on the heading
  paragraph, not as a separate break paragraph.
- **Entries:** Each entry uses style `References` — the same style as
  normative reference entries in clause 2. Format: `[N]\t<citation text>`
  with a `{SEQ Ref \* ARABIC}` field and bookmark.

See `itut-drafting` for the concrete style-name mapping and officecli
commands.

______________________________________________________________________

## Notes (from the Rules)

- Integrated in text: shall **not** contain requirements. Use "NOTE -- " for
  single note, "NOTE 1 -- ", "NOTE 2 -- " for multiple.
- Notes to tables/figures: **may** contain requirements. Start with
  "NOTE 1 -- ". Located within table frame or above figure title.
- Notes are indented from the main text margin.

______________________________________________________________________

## Use of normative words

| Word | Meaning |
|------|---------|
| **shall** | Mandatory requirement |
| **shall not** | Prohibition |
| **may** | Permission; indicates an action that is permitted but not required |
| **need not** | Negative of "may" (avoid "may not") |

______________________________________________________________________

## Figures and tables (from the Rules)

### Figures

- Numbered with Arabic numerals, independent of clauses (e.g. Figure 1, Figure 2)
- **Title below figure**, centred: "Figure x -- title"
- Referenced as "see Figure 1" (uppercase "F")

### Tables

- Numbered with Arabic numerals, independent of clauses (e.g. Table 1, Table 2)
- **Title above table**, centred: "Table x -- title"
- Columns framed, headings separated by horizontal line
- Spanning pages: "(continued)" / "Table x (concluded)"

______________________________________________________________________

## ITU-T | ISO/IEC common text

When a Recommendation is jointly developed with ISO/IEC:

### Terminology

- **Common text**: Identical text in both ITU-T Rec and ISO/IEC IS
- **Identical Recommendations | International Standards**: Same text
- **Paired Recommendations | International Standards**: Technically aligned but not identical ("twin text")

### Self-reference

- In Scope/boilerplate: "this Recommendation | International Standard"
- Elsewhere: use a capitalized descriptive term (e.g. "this Specification")

### Dual notation

External references use ITU-T first: "see Rec. ITU-T X.882 | ISO/IEC 13712-3"

### Title

- Introductory element: "Information technology"
- Up to 3 elements, general to particular
- First letter of each element capitalized

______________________________________________________________________

## References

- [references/rules-recommendation-structure.md](references/rules-recommendation-structure.md) -- detailed extract from Rules for presentation

## Cross-references

- `itut-basics` -- ITU-T organization, roles, meeting procedures
- `itut-contributions` -- contribution submission and TDocs
- `itut-drafting` -- ITU-T contribution .docx template and formatting
- `itut-patents` -- patent policy, IPR disclosure, licensing declarations
- `sdo-docx-formatting` -- formatting rules (delegated)
