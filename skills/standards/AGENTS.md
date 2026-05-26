# Standards skills -- planning

## Purpose

Skills in this directory enable coding agents to autonomously write meeting
contribution documents for Standards Developing Organizations (SDOs)
in `.docx` format. Initial focus: ETSI, 3GPP, ITU-T.

## Source material inventory

| Source | Content | Used by |
|--------|---------|---------|
| `tmp/WRITING.md` | General writing rules, ITU-T .docx styling | `sdo-writing-style`, `itut-drafting` |
| `tmp/findings.md` | ITU-T template analysis, style mapping, equation/batch workflows | `itut-drafting`, `sdo-docx-operations` |
| `tmp/officecli-operational-constraints/` | officecli guardrails, tab-run injection, field-code patterns, helper scripts | `sdo-docx-operations` |
| `tmp/tdoc-example/` | Worked example of 3GPP TDoc project (PLAN.md, AGENTS.md) | `3gpp-drafting` (patterns) |
| `tmp/awesome-3gpp-skills/skills/standards-document-formatting/` | Reusable formatting conventions (headings, tables, figures, notes, citations, enumerations, text) | `sdo-docx-formatting` |
| `tmp/awesome-3gpp-skills/skills/3gpp-tdoc-conventions/` | 3GPP template, metadata, revision workflow, project layout, set_docx_props.py | `3gpp-drafting` |

## Three-layer architecture

```
┌──────────────────────────────────────────────────────────────┐
│ Layer 1 -- Common drafting tools (prefix: sdo-)              │
│   Writing style, .docx formatting rules, officecli guardrails│
├──────────────────────────────────────────────────────────────┤
│ Layer 2 -- SDO reference (per-SDO prefix)                    │
│   Organisation, meetings, procedures, resources, terminology │
├──────────────────────────────────────────────────────────────┤
│ Layer 3 -- SDO drafting (per-SDO prefix)                     │
│   Template structure, style-name mapping, metadata convention│
│   Each delegates formatting rules to Layer 1, style names to │
│   its own mapping table.                                     │
└──────────────────────────────────────────────────────────────┘
```

### Layer 1 -- Common drafting skills (`sdo-` prefix)

Apply across all SDOs. These describe **what** to do and **how** to do it
at the conceptual level; concrete style names live in Layer 3.

| # | Skill | Lines from | Description |
|---|-------|-----------|-------------|
| 1 | `sdo-writing-style` | `tmp/WRITING.md` Core rules + Required checks (strip .docx-specific) | General prose quality, specificity, fact discipline, anti-genericity, register, medium routing. Applies to the *textual content* of any standards document regardless of SDO. |
| 2 | `sdo-docx-formatting` | `tmp/awesome-3gpp-skills/skills/standards-document-formatting/` | Reusable .docx formatting conventions: manual heading numbering (never auto-number), table/figure captions with SEQ fields + bookmarks + REF cross-references, note formatting (NO/NW sequence), citation format ([N] + SEQ Ref), enumeration hierarchy (B1/B2/B3 en-dash), non-breaking spaces, style-based formatting only (no manual overrides). **Uses abstract style names** (e.g. "heading style for level N", "body text style", "table caption style"); concrete mapping deferred to Layer 3. |
| 3 | `sdo-docx-operations` | `tmp/officecli-operational-constraints/` | officecli operational guardrails: resident mode, batch limits, tab-run injection via raw-set (constraint 3), field-code injection (SEQ/REF), paraId unreliability, raw-set safety rules. Includes helper scripts from `tmp/officecli-operational-constraints/scripts/` for deterministic edits (add_bookmarks, fix_heading_tabs, fix_enum_tabs, fix_note_tabs). |

**Key design decision -- style-name abstraction:**

`sdo-docx-formatting` describes formatting **rules** using abstract/conceptual
style names. Each SDO's Layer 3 drafting skill provides a mapping table from
abstract names to concrete style IDs. This keeps the formatting rules in one
place while style names vary per SDO.

Example abstract names used in `sdo-docx-formatting`:

| Abstract name | What it is | 3GPP / ETSI | ITU-T |
|---|---|---|---|
| `body-text` | Main body paragraph | `Normal` | `Body Text` (or `Normal`) |
| `heading-1` to `heading-3` | Section headings | `Heading 1`--`Heading 3` | `Heading 1`--`Heading 3` |
| `enum-1` to `enum-3` | Enumeration levels | `B1`, `B2`, `B3` | `enumlev1`, `enumlev2`, `enumlev3` |
| `table-caption` | Caption above table | `TH` | `Table_No & title` (`TableNotitle`) |
| `table-header` | Header row | `TAH` | `Table_head` (`Tablehead`) |
| `table-data` | Data rows | `TAC` | `Table_text` (`Tabletext`) |
| `table-note` | Merged bottom row note | `TAN` | (varies) |
| `figure-para` | Paragraph containing image | `FL` | `Figure` |
| `figure-caption` | Caption below figure | `TF` | `Figure_No & title` |
| `figure-note` | Note below figure | `NF` | (varies) |
| `note-main` | Last note in block | `NO` | `Note` |
| `note-continuation` | Preceding notes in block | `NW` | (varies) |
| `reference-entry` | Each references entry | `EX` | `References` |
| `code-text` | Inline code / filenames | `PL` | `Macro Text` (`MacroText`) |
| `equation-label` | Display equation paragraph | (varies) | `Equation` |

### Layer 2 -- SDO reference skills (per-SDO prefix)

Describe an SDO's organisation, meeting structure, procedures, naming
conventions, and resources. Background knowledge needed to draft correctly
for a given SDO -- no document formatting.

**Already exist:**

| Skill | Scope |
|-------|-------|
| `3gpp-basics` | Organisation, partners, TSGs, scope |
| `3gpp-working-groups` | WG nomenclature, tbid/SubTB, hierarchy |
| `3gpp-meetings` | Meeting structure, quarterly plenaries |
| `3gpp-tdocs` | TDoc patterns, filename conventions, FTP/HTTP |
| `3gpp-releases` | Release structure, versioning, freeze |
| `3gpp-specifications` | TS/TR numbering, file formats, directories |
| `3gpp-portal-authentication` | EOL accounts, AJAX login |
| `3gpp-change-request` | CR procedure, workflow, status |
| `etsi-spec` | ETSI spec metadata retrieval (already in repo) |

**To create (ETSI):**

| Skill | Content |
|-------|---------|
| `etsi-basics` | ETSI organisation, membership types, TB/TC structure, deliverable types (EN, ES, EG, TS, TR, SR, GS, GR), IPR policy |
| `etsi-meetings` | Meeting structure, numbering, document submission deadlines, ETSI portal |
| `etsi-contributions` | Contribution types, TDoc numbering conventions, header requirements |
| `etsi-work-items` | Work Item lifecycle, rapporteur role, milestone dates, approval procedures |

**To create (ITU-T):**

| Skill | Content |
|-------|---------|
| `itut-basics` | ITU-T organisation, Study Groups, Questions, Recommendations, approval processes (TAP, AAP), ITU-T languages |
| `itut-meetings` | SG/WP meeting structure, contribution deadlines, document numbering (C, TD series) |
| `itut-contributions` | Contribution types, cover page fields, header table structure, abstract |
| `itut-patents` | Common Patent Policy (ITU-T/ITU-R/ISO/IEC), IPR disclosure obligations, 3 licensing options (RF/RAND/refusal), declaration forms, patent database, neutrality principles |
| `itut-recommendations` | Recommendation structure (clause numbering), amendment vs revision, consent/approval, publication stages |

### Layer 3 -- SDO drafting skills (per-SDO prefix)

SDO-specific document formatting: template structure, metadata conventions,
style-name mappings. Each skill **delegates** formatting rules to
`sdo-docx-formatting` and operational constraints to `sdo-docx-operations`.

| Skill | Content | Source material |
|-------|---------|-----------------|
| `3gpp-drafting` | 3GPP TDoc template (`Tdoc_Template.docx`), PLAN.md metadata schema, Jinja2 placeholder substitution (`{{ title }}`, `{{ tdoc }}`, etc.), header paragraph structure, revision workflow (copy-rename-patch, `revision_of` handling), DOCX custom property sync (`set_docx_props.py`), project layout conventions (`tmp/`, `figures/`, `ref/`), AGENTS.md template pattern. **Style-name table**: 3GPP column from the mapping above. | `tmp/awesome-3gpp-skills/skills/3gpp-tdoc-conventions/` + `tmp/tdoc-example/` |
| `etsi-drafting` | ETSI contribution template structure, metadata fields, ETSI-style header, document numbering. **Style-name table**: ETSI column (= same as 3GPP for most styles; document any deviations). | To be researched |
| `itut-drafting` | ITU-T contribution template structure (9-row header table: logo, doc number, question, place, source, title, contacts; abstract table; running header), metadata fields, equation conventions (Equation style with tab stops), style deviations from 3GPP/ETSI. **Style-name table**: ITU-T column from the mapping above. | `tmp/findings.md` Phase 7 + `tmp/WRITING.md` Styling section |

### Cross-reference map

```
sdo-writing-style
    │
    └── sdo-docx-formatting ── sdo-docx-operations
              │                       │
    ┌─────────┼───────────────────────┼───────────────────┐
    │         │                       │                   │
  ETSI      3GPP                    ITU-T                all
    │         │                       │                   │
etsi-basics  3gpp-basics        itut-basics               │
etsi-meet   3gpp-meetings       itut-meetings             │
etsi-contrib 3gpp-tdocs         itut-contributions        │
etsi-wi     3gpp-releases       itut-recommendations      │
    │        3gpp-specs               │                   │
    │        3gpp-wg                  │                   │
    │        3gpp-portal              │                   │
    │        3gpp-cr                  │                   │
    │            │                    │                   │
etsi-drafting 3gpp-drafting     itut-drafting ────────────┘
    │            │                    │
    └────────────┴────────────────────┘
                    │
          officecli / python-docx+docxtpl / docx skill
                    │
    ┌───────────────┼───────────────┐
    │               │               │
  Draw.io      teddi-cli         xleak
 (diagrams)   (abbreviations)   (xlsx data)
```

## Toolchain strategy (encoded in Layer 1, inherited by Layer 3)

```
Preferred:  officecli              (native .docx editing, SVG support,
                                    raw-set for field codes / tab runs)
Fallback:   python-docx + docxtpl  (programmatic control, templates,
                                    SVG via docx-svg skill)
Fallback:   docx skill              (general python-docx guidance)
```

Ancillary tools:

- Draw.io MCP / `drawio` skill → SVG diagrams (follow Draw.io SVG export guidelines)
- `teddi` / `teddi-cli` → unknown abbreviations and terms
- `xleak` / `python-docx` → reading XLSX data for table inclusion

## Project layout convention (from 3gpp-tdoc-conventions)

When an agent works on a specific contribution, the project root follows:

```
<project>/
├── PLAN.md              # YAML frontmatter = metadata source of truth
├── AGENTS.md            # Orchestration-only (scope, structure, tool refs)
├── <tdoc> - <title>.docx  # Working document
├── figures/             # Versioned SVG/PNG figure assets
├── ref/                 # Cited source documents + Tdoc_Template.docx
├── scripts/             # Analysis/helper scripts
└── tmp/                 # Transient artifacts (keep root clean)
```

`PLAN.md` frontmatter keys (per-SDO; example from 3GPP):
`meeting`, `tdoc`, `date`, `place`, `source`, `title`, `agenda_item`, `target`,
`revision_of` (set to `~` when not a revision).

## Naming convention

| Prefix | Scope | Examples |
|--------|-------|---------|
| `sdo-` | Common across all SDOs | `sdo-project-setup`, `sdo-writing-style`, `sdo-docx-formatting`, `sdo-docx-operations` |
| `3gpp-` | 3GPP-specific | `3gpp-basics`, `3gpp-tdocs`, `3gpp-drafting` |
| `etsi-` | ETSI-specific | `etsi-spec`, `etsi-basics`, `etsi-drafting` |
| `itut-` | ITU-T-specific | `itut-basics`, `itut-contributions`, `itut-drafting`, `itut-patents` |

Existing skills in this repo already follow this convention; no renames needed.

## Existing skill inventory vs. planned

### Already in this repo (`skills/standards/`)

| Skill | Layer | Status |
|-------|-------|--------|
| `3gpp-basics` | 2 | Done |
| `3gpp-working-groups` | 2 | Done |
| `3gpp-meetings` | 2 | Done |
| `3gpp-tdocs` | 2 | Done |
| `3gpp-releases` | 2 | Done |
| `3gpp-specifications` | 2 | Done |
| `3gpp-portal-authentication` | 2 | Done |
| `3gpp-change-request` | 2 | Done |
| `etsi-spec` | 2 | Done |
| `sdo-project-setup` | 1 | Done |
| `sdo-docx-formatting` | 1 | Done |
| `sdo-docx-operations` | 1 | Done |
| `sdo-writing-style` | 1 | Done |
| `sdo-writing-conventions` | 1 | Done |
| `3gpp-drafting` | 3 | Done |
| `itut-basics` | 2 | Done |
| `itut-contributions` | 2 | Done |
| `itut-patents` | 2 | Done |
| `itut-recommendations` | 2 | Done |
| `itut-drafting` | 3 | Done |
| `etsi-basics` | 2 | Done |
| `etsi-drafting` | 3 | Done |

### To create (all layers)

| # | Skill | Layer | Priority | Source |
|---|-------|-------|----------|--------|
| 1 | `etsi-meetings` | 2 | Low | ETSI portal |
| 2 | `etsi-contributions` | 2 | Low | ETSI portal |
| 3 | `etsi-work-items` | 2 | Low | ETSI portal |

### Key differences from awesome-3gpp-skills

| awesome-3gpp-skills | This repo (prompts) |
|---|---|
| `standards-document-formatting` uses hardcoded 3GPP style names | `sdo-docx-formatting` uses abstract names; style mapping lives in Layer 3 per-SDO drafting skills |
| No ITU-T or ETSI skills | Full three-SDO coverage planned |
| No `sdo-writing-style` | Included as Layer 1 skill |
| No `sdo-docx-operations` (separate skill) | Included (from tmp/officecli-operational-constraints) |
| `3gpp-tdoc-conventions` standalone | Split into `3gpp-drafting` (SDO-specific) + `sdo-project-setup` (common) |
| No project bootstrap skill | `sdo-project-setup` provides layout, AGENTS.md template, property sync, autodetection |

## Skill dependency chain (loading order)

When an agent drafts a contribution for a specific SDO, load skills in this order:

```
1. sdo-project-setup        (bootstrap: detect new/ongoing, sync metadata, ensure layout)
2. sdo-writing-style        (if producing prose content)
3. sdo-docx-formatting      (formatting rules using abstract names)
4. sdo-docx-operations      (officecli guardrails)
5. <sdo>-drafting           (SDO-specific template + style mapping)
   └── delegates to 2-4 for rules; provides concrete style names
6. <sdo>-basics             (if org/terminology context needed)
7. <sdo>-meetings           (if meeting procedures relevant)
8. <sdo>-contributions      (if contribution numbering relevant)
```

## Next steps (proposed order)

1. **`itut-*` Layer 2 skills** -- ITU-T reference info
2. **`etsi-drafting`** -- ETSI Layer 3 drafting (template + style mapping)
3. **`etsi-*` Layer 2 skills** -- ETSI reference info
