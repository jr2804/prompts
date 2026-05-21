---
name: etsi-drafting
description: ETSI-specific deliverable drafting conventions: document structure, clause ordering, requirements writing (shall/should/may), figures/tables/equations, annexes, and ETSI style-name mapping. Use when preparing or editing ETSI deliverable .docx files (TS, ES, EN, TR, EG, SR, GS). Delegates formatting rules to sdo-docx-formatting and officecli operations to sdo-docx-operations.
---

# ETSI Deliverable Drafting

Use this skill for ETSI-specific document structure, deliverable conventions,
and concrete Word style names. For formatting rules (headings, enumerations,
notes, tables, figures, citations), see `sdo-docx-formatting`. For officecli
operations (tab-run injection, field codes, bookmarks), see
`sdo-docx-operations`.

## Assets

ETSI provides deliverable skeletons (Word templates) for each type via the
editHelp! website at https://portal.etsi.org/edithelp/home.asp. These contain
all required styles and structural elements. Always start from the appropriate
skeleton for the deliverable type being drafted. Do not add new styles or
modify existing ones.

---

## ETSI deliverable structure

Per the ETSI Drafting Rules (EDR), an ETSI deliverable follows this order:

**Unnumbered preliminary elements (informative):**
- Cover page (title, deliverable type, version, date, logos)
- Contents (generated)
- Intellectual Property Rights (provided by Secretariat -- do not modify)
- Foreword (TC that prepared it; optional: relationship to other docs,
  superseded docs, technical changes from previous version)
- Transposition table (EN only -- provided by Secretariat)
- Modal verbs terminology (provided by Secretariat -- do not modify)
- Executive summary (optional)
- Introduction (optional)

**Numbered core:**
1. Scope
2. References (2.1 Normative, 2.2 Informative)
3. Definitions of terms, abbreviations and symbols
   (3.1 Terms, 3.2 Symbols, 3.3 Abbreviations)
4+ Technical content

**Supplementary:**
- Annex A, B, C... (normative): title -- integral part of the deliverable
- Annex (continued lettering) (informative): title -- non-integral
- Bibliography (optional)
- Change history (required for EN HS; optional otherwise)
- History (provided by Secretariat)

---

## Key drafting rules

### Requirements language

| Verbal form | Meaning |
|-------------|---------|
| **shall** | Mandatory requirement |
| **shall not** | Prohibition |
| **should** | Recommendation |
| **should not** | Recommendation against |
| **may** | Permission |
| **need not** | No requirement |
| **can** | Possibility or capability (informative only) |
| **cannot** | Impossibility (informative only) |

Each requirement should be: necessary, unambiguous, complete, precise,
well-structured, consistent, and testable.

### Clause numbering
- Arabic numerals from 1 (for Scope)
- Up to 6 heading levels (e.g. 5.1, 5.1.1, 5.1.1.1, ...)
- If subdivisions exist, at least two at each level
- Never mix numbered and unnumbered subdivisions at the same level
- To insert between existing clauses: use alphanumeric (clause "8a")
- To delete: mark as "Void" to preserve numbering
- Automatic numbering may be used with proper ETSI styles

### Scope
Worded as statements of fact:
- "The present document specifies..." / "establishes..." / "gives guidelines for..."
- "The present document is applicable to..."

### References
- Normative references (2.1): must be publicly available in English
- Prefer specific (dated) references
- Non-specific (undated) allowed only if referring TC controls the document
- References to 3GPP deliverables: replace with ETSI equivalents
  (e.g. 3GPP TS 23.040 -> ETSI TS 123 040)

### Figures and tables
- Numbered with Arabic numerals from 1
- Title below figure: "Figure N: title"
- Title above table: "Table N: title"
- Notes within the figure/table frame

### Notes
- Integrated in text: "NOTE: " or "NOTE N: " for multiple
- Notes shall NOT contain requirements (except notes to tables/figures)
- Examples: "EXAMPLE: " or "EXAMPLE N: "
- Avoid footnotes; if used, shall not contain requirements

### Neutrality
Do not promote or endorse services, products, or technologies of one
company over another. If only one product/technology is available and
needed, follow the rules in EDR clause 4 (copyright provisions).

---

## ETSI style-name mapping

Concrete Word style IDs for ETSI deliverables. ETSI styles are provided
by the deliverable skeleton (from editHelp!). These are largely the same
as 3GPP styles.

| Abstract name (`sdo-docx-formatting`) | ETSI concrete style ID | Purpose |
|---|---|---|
| `body-text` | `Normal` | Main body paragraphs |
| `heading-1` | `Heading 1` | Top-level section heading |
| `heading-2` | `Heading 2` | Second-level section heading |
| `heading-3` | `Heading 3` | Third-level section heading |
| `enum-1` | `B1` | First-level enumeration |
| `enum-2` | `B2` | Second-level enumeration |
| `table-caption` | `TH` | Table caption (above table) |
| `table-header` | `TAH` | Table header row |
| `table-data` | `TAC` | Table data rows |
| `table-note` | `TAN` | Table note row |
| `figure-para` | `FL` | Paragraph containing image |
| `figure-caption` | `TF` | Figure caption (below figure) |
| `figure-note` | `NF` | Note below figure |
| `note-main` | `NO` | Last note in a consecutive block |
| `note-continuation` | `NW` | Preceding notes in a block |
| `reference-entry` | `EX` | References section entry |
| `code-text` | `PL` | Inline code / filenames |

> **Note:** These style names are based on the 3GPP/ETSI convention pool.
> Always verify with the skeleton template from editHelp! for the specific
> deliverable type. ETSI may define additional styles for specialised
> elements (front cover, IPR clause, etc.) that are handled by the
> Secretariat.

---

## References

- [references/etsi-drafting-rules.md](references/etsi-drafting-rules.md) -- detailed extract from the ETSI Drafting Rules (EDR)

## Cross-references

- `sdo-project-setup` -- common project bootstrap
- `sdo-docx-formatting` -- formatting rules (delegated; see mapping above)
- `sdo-docx-operations` -- officecli guardrails
- `sdo-writing-style` -- prose quality rules
- `sdo-writing-conventions` -- mechanical writing rules
- `etsi-basics` -- ETSI organisation, deliverable types, lifecycle
- `etsi-spec` -- ETSI specification metadata retrieval
