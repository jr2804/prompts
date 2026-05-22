---
name: itut-recommendations
description: "ITU-T Recommendation structure, approval processes, amendment/corrigendum procedures, and ITU-T | ISO/IEC common text conventions. Use when the agent needs to understand how ITU-T Recommendations are structured (clause order, element types, annex conventions), approved (TAP/AAP), amended, or how joint ITU-T/ISO/IEC texts work. Sources: Rec. ITU-T A.1 (09/2019) + Rules for presentation of ITU-T | ISO/IEC common text (2014)."
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

---

## Recommendation clause structure

Per the Rules for presentation of ITU-T | ISO/IEC common text, a
Recommendation is organized as follows:

| Clause | Element | Content |
|--------|---------|---------|
| *(preliminary)* | Cover page, Contents, Foreword, Introduction | Roman numeral pages |
| 1 | **Scope** | Defines subject and limits; no requirements |
| 2 | **Normative references** | Documents whose provisions are referenced normatively |
| 3 | **Definitions** *(optional)* | Terms defined for this Recommendation |
| 4 | **Abbreviations** *(optional)* | All abbreviations used in the text |
| 5 | **Conventions** *(optional)* | Any particular notation used |
| 6+ | **Text** | Body of the Recommendation |
| Annex A+ | **Integral annexes** | Normative material (same approval as Recommendation) |
| Annex (continues) | **Non-integral annexes** | Informative/supplementary (SG agreement, not full approval) |
| *(last)* | **Index** *(optional)* | |

### Subdivision numbering
- Digits separated by periods: 1, 1.1, 1.1.1
- No trailing period after single number
- Do not create subclause 1.1 unless 1.2 also exists

---

## Notes (from the Rules)

- Integrated in text: shall **not** contain requirements. Use "NOTE -- " for
  single note, "NOTE 1 -- ", "NOTE 2 -- " for multiple.
- Notes to tables/figures: **may** contain requirements. Start with
  "NOTE 1 -- ". Located within table frame or above figure title.
- Notes are indented from the main text margin.

---

## Use of normative words

| Word | Meaning |
|------|---------|
| **shall** | Mandatory requirement |
| **shall not** | Prohibition |
| **may** | Permission; indicates an action that is permitted but not required |
| **need not** | Negative of "may" (avoid "may not") |

---

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

---

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

---

## References

- [references/rules-recommendation-structure.md](references/rules-recommendation-structure.md) -- detailed extract from Rules for presentation

## Cross-references

- `itut-basics` -- ITU-T organization, roles, meeting procedures
- `itut-contributions` -- contribution submission and TDocs
- `itut-drafting` -- ITU-T contribution .docx template and formatting
- `itut-patents` -- patent policy, IPR disclosure, licensing declarations
- `sdo-docx-formatting` -- formatting rules (delegated)
