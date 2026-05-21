---
name: etsi-basics
description: "ETSI organisation overview, deliverable types, standards development lifecycle, and key roles. Use when the agent needs context about how ETSI works: Technical Committees, deliverable types (TS, ES, EN, HS, TR, EG, SR, GS), approval processes, the standards development lifecycle (Work Item through publication), or ETSI-specific terminology. Sources: ETSI Guide to Writing World Class Standards + ETSI Directives."
---

# ETSI Basics

## Overview

ETSI (European Telecommunications Standards Institute) is one of three
European Standards Organizations (ESOs), alongside CEN and CENELEC.
ETSI produces globally recognized standards for information and
communications technologies (ICT), with about 2 500 standards published
each year.

## ETSI deliverable types

| Type | Full name | Content | Approval scope |
|------|-----------|---------|----------------|
| **TS** | Technical Specification | Normative | Technical Committee |
| **ES** | ETSI Standard | Normative | ETSI membership |
| **EN** | European Standard | Normative | TC + National Standards Orgs / National Delegations |
| **EN (HS)** | Harmonised Standard | Normative (special EN, EU mandate) | EN process + EU publication |
| **EN (CS)** | Community Specification | Normative (civil aviation) | EN process |
| **TR** | Technical Report | Informative (preferred) | Technical Committee |
| **EG** | ETSI Guide | Informative (org guidance) | ETSI membership |
| **SR** | Special Report | Informative (reference) | Technical Committee |
| **GS** | Group Specification | Normative or informative | Industry Specification Group |

**Key terms:**
- **Normative** = prescriptive = how to comply with the standard
- **Informative** = descriptive = helps with conceptual understanding
- **Requirement** = the criteria to be fulfilled for compliance
- **Provision** = collective term for requirements, recommendations, permissions

### Choosing type
For normative provisions, focus on the approving stakeholders. Larger
stakeholder groups mean more complex approval: EN > ES > TS. Prefer TS
unless broader approval is needed. TS requires approval by just the
Technical Committee.

### Numbering format
`ETSI <type> <number>[-<part>]`:
- ETSI TS 123 456
- ETSI ES 201 999-1, ETSI ES 201 999-2 (multi-part)
- ETSI EN 300 356-33-10 (sub-part)

---

## Standards development lifecycle

```
Create Work Item -> Develop draft -> Validate & Review
    -> Editorial Check -> Approval -> Publication
    -> Maintenance & Evolution (loop back)
```

| Stage | Key activities |
|-------|---------------|
| **1. Create Work Item** | Define scope, title, deliverable type, milestones, responsible TC/WG/rapporteur, validation plan |
| **2. Develop draft** | Structured drafting; clear, complete, testable requirements; use specialised notations |
| **3. Validate** | Peer review, interoperability events, implementation feedback, test development |
| **4. Editorial check** | Submit to editHelp! via Technical Officer; checks English, references, abbreviations, definitions (not technical content) |
| **5. Approve & publish** | Process per deliverable type; web-based voting; feedback collection |
| **6. Maintain & evolve** | Defect correction, alignment with related standards, planned revisions |

---

## Key roles

| Role | Description |
|------|-------------|
| **Technical Committee (TC)** | Develops and approves deliverables |
| **Working Group (WG)** | Subset of TC for specific topics |
| **Rapporteur** | Coordinates detailed study of a work item |
| **Industry Specification Group (ISG)** | Creates GS deliverables; lighter process |
| **Technical Officer** | Secretariat support; ETSI rules and technology knowledge |
| **editHelp! Service** | Checks editing, English, refs, abbreviations, definitions |
| **Specialist Task Force (STF)** | Funded experts for specific drafting tasks |

---

## ETSI resources

- ETSI Portal: https://portal.etsi.org/
- editHelp! (skeletons, templates): https://portal.etsi.org/edithelp/home.asp
- TEDDI (terms database): https://webapp.etsi.org/Teddi/
- ETSI Directives: https://portal.etsi.org/Resources/ETSIDirectives.aspx
- ETSI "Use of English" guide: https://ocgwiki.etsi.org/index.php?title=Use_of_English

## References

- [references/etsi-basics.md](references/etsi-basics.md) -- detailed extract (deliverable types, lifecycle, roles, Harmonised Standards)

## Cross-references

- `etsi-drafting` -- ETSI deliverable structure, formatting rules, style names
- `etsi-spec` -- ETSI specification metadata retrieval
- `sdo-docx-formatting` -- formatting rules (delegated)
- `sdo-project-setup` -- project bootstrap workflow
