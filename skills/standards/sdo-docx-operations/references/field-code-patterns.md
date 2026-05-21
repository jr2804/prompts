# Field Code Patterns

Use OOXML field char runs for all dynamic references. Never hard-code
reference numbers or figure/table numbers as plain text.

## REF cross-reference pattern

```xml
<w:r><w:fldChar w:fldCharType="begin"/></w:r>
<w:r><w:instrText xml:space="preserve"> REF tbl_example \h </w:instrText></w:r>
<w:r><w:fldChar w:fldCharType="separate"/></w:r>
<w:r><w:t>Table&#160;1</w:t></w:r>
<w:r><w:fldChar w:fldCharType="end"/></w:r>
```

The `<w:t>` between `separate` and `end` is the cached display value --
Word replaces it when fields are updated (F9). Bookmark names follow
the convention `tbl_<short_name>`, `fig_<short_name>`, or `ref_<short_name>`.

## SEQ auto-numbering pattern (figures and tables)

```xml
<w:r><w:fldChar w:fldCharType="begin"/></w:r>
<w:r><w:instrText xml:space="preserve"> SEQ Figure \* ARABIC </w:instrText></w:r>
<w:r><w:fldChar w:fldCharType="separate"/></w:r>
<w:r><w:t>1</w:t></w:r>
<w:r><w:fldChar w:fldCharType="end"/></w:r>
```

Replace `Figure` with `Table` for table captions. The bookmark for
cross-referencing must wrap only the numbered label part (e.g.
`Figure&#160;1`), not the full caption text.

## Citation SEQ + bookmark pattern

For reference list entries, use `SEQ Ref \* ARABIC` and insert a bookmark
`ref_<short_name>` around only the sequence counter field (not the square
brackets). Cross-reference in body text with `REF ref_<short_name>`.
