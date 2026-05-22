---
name: sdo-docx-operations
description: Cross-platform operational guardrails and deterministic helper scripts for officecli OOXML edits on .docx files. Use when editing .docx with officecli raw-set, fixing tab run issues, inserting bookmarks or field codes (SEQ/REF), validating XPath targeting, or preventing destructive raw-set mistakes. Applies across all SDOs -- concrete style names provided by the per-SDO drafting skill.
---

# SDO DOCX Operations -- officecli guardrails

Use this skill for reliable, repeatable officecli operations that require
XML-level edits on standards documents.

## Workflow

1. Open the document in resident mode before multi-step edits:
   `officecli open <doc>`
2. Run one mutation command at a time and check exit codes.
3. Use style/ordinal or explicit XPath targeting, not paraId targeting.
4. Prefer the Python helper scripts in `scripts/` for deterministic edits.
5. Validate with `officecli view`/`get`/`query` before and after mutation.
6. Close the document at the end: `officecli close <doc>`

## Script entry points

- `scripts/add_bookmarks.py` -- figure/table/reference bookmark insertion
  and reference run replacement.
- `scripts/fix_heading_tabs.py` -- heading number-tab-title run repair.
- `scripts/fix_enum_tabs.py` -- enumeration dash-tab-text run repair.
- `scripts/fix_note_tabs.py` -- NOTE number-tab-text run repair and
  sequence validation.
- `scripts/officecli_xml_common.py` -- shared helpers (run_officecli,
  raw_set, validate_doc, load_json_spec).

All scripts declare PEP 723 inline metadata and are run via `uv run`:

```bash
uv run scripts/add_bookmarks.py --doc <doc> --spec assets/specs/add_bookmarks.example.json
uv run scripts/fix_heading_tabs.py --doc <doc> --mapping assets/specs/fix_heading_tabs.example.json
uv run scripts/fix_enum_tabs.py --doc <doc> --items assets/specs/fix_enum_tabs.example.json
uv run scripts/fix_note_tabs.py --doc <doc> --notes assets/specs/fix_note_tabs.example.json
```

## JSON specs

- `assets/schemas/` -- JSON Schema contracts for each script input.
- `assets/specs/` -- example specs for reuse across projects.

## Safety rules

- Never use `raw-set --action replace` with an empty XML payload.
- Always keep bookmark names and IDs unique.
- Always preserve non-breaking spaces and explicit tab runs where required.
- Keep scripts platform-independent and executable via `uv run`.

## References

- [references/tool-usage.md](references/tool-usage.md)
- [references/constraints.md](references/constraints.md)
- [references/xpath-patterns.md](references/xpath-patterns.md)
- [references/field-code-patterns.md](references/field-code-patterns.md)
- [references/tracked-changes.md](references/tracked-changes.md)

## Cross-references

- `sdo-docx-formatting` -- formatting rules that these operations implement
- `3gpp-drafting` / `etsi-drafting` / `itut-drafting` -- concrete style names
  required for XPath targeting (e.g. `Heading1`, `B1`, `NO`, `TF`)
- `docx-svg` -- SVG image insertion when officecli is not available
