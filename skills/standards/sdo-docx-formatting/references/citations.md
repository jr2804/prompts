# Citations

## References section placement

- The `References` section is always the **last** section in the document,
  after any annexes.
- Unlike all other sections, `References` is **not** numbered; use
  `heading-1` style without a manual number prefix.

## Entry format

- Each entry: `[N]\t<citation text>` -- bracket-wrapped number, real tab
  run, then citation text.
- Style: `reference-entry` (→ concrete style) for every reference entry.
- Do **not** hard-code the number. Use a `{SEQ Ref \* ARABIC}` field and
  place a **bookmark** (`ref_<short_name>`) around the sequence field only
  -- not around the square brackets.
- Cross-reference in body text with `{REF ref_<short_name>}`. Never use
  hard-coded plain-text reference numbers.
- See `sdo-docx-operations` for officecli field-code and bookmark injection.

## Ordering and completeness

- List references in the order they first appear in the body text.
- Every listed reference **must** be cited at least once in the body.
- Do not include uncited references.

## Style mapping

| Abstract | Concrete (per SDO drafting skill) |
|----------|-----------------------------------|
| `reference-entry` | SDO-specific style for each references entry |
