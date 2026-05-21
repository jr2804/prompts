# OfficeCLI Constraints

## 1. Resident mode required

Open the document once with `officecli open <doc>` before editing, close
with `officecli close <doc>` afterwards. All intermediate commands run
in-memory. Skipping this causes repeated file I/O and risks partial writes.

## 2. One command at a time

Run one command and check the exit code before proceeding. Never execute a
batch of commands blindly -- if one fails, subsequent commands build on a
broken state.

## 3. `set --prop text=` cannot produce Word tab characters

Text values go into `<w:t>` XML nodes; `\t` in the string is treated as a
space. This affects headings (number/title separated by tab), enumerations
(bullet/text), and notes (NOTE colon/text). Consequence: tabs appear as
spaces, causing wrong indentation, misaligned bullets, and broken note
formatting.

**Workaround -- inject a separate `<w:r><w:tab/></w:r>` run:**

```xml
<!-- Heading 1 with correct tab -->
<w:r><w:t>1</w:t></w:r><w:r><w:tab/></w:r><w:r><w:t>Introduction</w:t></w:r>

<!-- Enumeration with correct tab -->
<w:r><w:t>&#8211;</w:t></w:r><w:r><w:tab/></w:r><w:r><w:t xml:space="preserve">Enumeration text.</w:t></w:r>

<!-- Note with correct tab after colon -->
<w:r><w:t>NOTE&#160;1:</w:t></w:r><w:r><w:tab/></w:r><w:r><w:t xml:space="preserve">Note text.</w:t></w:r>
```

Use the helper scripts in `scripts/` to apply these patterns without
hand-writing XML.

## 4. High-level commands cannot insert REF/SEQ field codes

Using `set --prop text=` for cross-references produces hardcoded plain text
that breaks when the document is revised. Always inject field codes via
`officecli raw-set`. See `references/field-code-patterns.md` for OOXML
snippets.

## 5. `paraId` targeting is unreliable

XPath like `//w:p[@w:paraId='101C5D24']` matches zero elements because
`paraId` is in the `w14:` namespace, not auto-registered. Consequence: the
command silently affects 0 elements and reports success.

**Workaround -- use style-based positional XPath:**

- `(//w:p[w:pPr/w:pStyle/@w:val='Heading1'])[N]/w:r[1]`
- `(//w:p[w:pPr/w:pStyle/@w:val='B1'])[N]/w:r[1]`
- `//w:p[starts-with(normalize-space(.),'Target text')]/w:r[1]`

Always verify match count first with `officecli query <doc> "paragraph[style=...]"`.

## 6. `raw-set --action replace --xml ""` is destructive

An empty XML string replaces the matched element with nothing, permanently
deleting it -- with no undo. This mistake occurred during document
production and required manual restoration of a deleted figure caption
paragraph.

**Safe inspection alternative:** use `officecli get <doc> "/body/p[N]" --depth 5`
or `officecli view <doc> annotated`. Never use `raw-set --action replace`
for inspection.
