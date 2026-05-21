---
name: docx
description: "Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). Triggers include: any mention of 'Word doc', 'word document', '.docx', or requests to produce professional documents with formatting like tables of contents, headings, page numbers, or letterheads. Also use when extracting or reorganizing content from .docx files, inserting or replacing images in documents, performing find-and-replace in Word files, working with tracked changes or comments, or converting content into a polished Word document. If the user asks for a 'report', 'memo', 'letter', 'template', or similar deliverable as a Word or .docx file, use this skill. Do NOT use for PDFs, spreadsheets, Google Docs, or general coding tasks unrelated to document generation."
license: Proprietary. LICENSE.txt has complete terms
---

# DOCX creation, editing, and analysis

## Overview

A .docx file is a ZIP archive containing XML files.

## Quick Reference

| Task | Approach |
|------|----------|
| Read/analyze content | `pandoc` or unpack for raw XML |
| Create new document | Use docx-js — see references/docx-js.md |
| Edit existing document | Unpack → edit XML → repack |
| Redlining (tracked changes) | Use Document library — see references/ooxml.md |

### Converting .doc to .docx

Legacy `.doc` files must be converted before editing:

```bash
python scripts/soffice.py --headless --convert-to docx document.doc
```

### Reading Content

```bash
# Text extraction with tracked changes
pandoc --track-changes=all document.docx -o output.md

# Raw XML access
python scripts/unpack.py document.docx unpacked/
```

### Converting to Images

```bash
python scripts/soffice.py --headless --convert-to pdf document.docx
pdftoppm -jpeg -r 150 document.pdf page
```

### Accepting Tracked Changes

To produce a clean document with all tracked changes accepted (requires LibreOffice):

```bash
python scripts/accept_changes.py input.docx output.docx
```

---

## Creating New Documents

Generate .docx files with JavaScript. See **references/docx-js.md** for the complete API reference.

### Workflow

1. **MANDATORY — READ ENTIRE FILE**: Read [`references/docx-js.md`](references/docx-js.md) completely before proceeding.
2. Create a JavaScript/TypeScript file using Document, Paragraph, TextRun components.
3. Validate: `python scripts/validate.py --original <any_existing.docx> unpacked/` or after packing.

---

## Editing Existing Documents

**Follow all 3 steps in order.**

### Step 1: Unpack

```bash
python scripts/unpack.py document.docx unpacked/
```

Extracts XML, pretty-prints, merges adjacent runs, simplifies tracked changes, and converts smart quotes to XML entities (`&#x201C;` etc.) so they survive editing. Use `--merge-runs false` to skip run merging.

**Note the suggested RSID** printed by the unpack script — use it for tracked changes.

### Step 2: Edit XML

Edit files in `unpacked/word/`. See **references/ooxml.md** for XML patterns and the Document Library API.

**Two approaches:**

1. **Direct XML editing** — Use the agent's native edit tool for string replacements. Best for simple tracked changes and straightforward edits.
2. **Document Library (Python)** — Use for complex batched operations, programmatic node finding, and redlining workflows. See "Document Library" section in references/ooxml.md.

#### Using the Document Library

```bash
# Set PYTHONPATH to the skill root, then run your script
PYTHONPATH=/path/to/docx-skill uv run your_script.py
```

```python
from scripts.document import Document, DocxXMLEditor

doc = Document('unpacked', author="Claude", initials="C")
node = doc["word/document.xml"].get_node(tag="w:r", contains="old text")
doc["word/document.xml"].replace_node(node, '<w:del>...<w:ins>...')
doc.save()
```

#### Adding Comments

Use `comment.py` to handle boilerplate across multiple XML files:

```bash
python scripts/comment.py unpacked/ 0 "Comment text with &amp; and &#x2019;"
python scripts/comment.py unpacked/ 1 "Reply text" --parent 0  # reply to comment 0
```

Then add markers to document.xml (see Comments in references/ooxml.md).

### Step 3: Pack

```bash
python scripts/pack.py unpacked/ output.docx --original document.docx
```

Validates with auto-repair, condenses XML, and creates DOCX. Use `--validate false` to skip.

**Auto-repair will fix:**
- `durableId` >= 0x7FFFFFFF (regenerates valid ID)
- Missing `xml:space="preserve"` on `<w:t>` with whitespace

**Auto-repair won't fix:**
- Malformed XML, invalid element nesting, missing relationships, schema violations

---

## Redlining Workflow for Document Review

This workflow is for comprehensive tracked changes on someone else's document. **See references/ooxml.md** for the complete Document Library API and XML patterns.

**Batching Strategy**: Group related changes into batches of 3-10 changes. This makes debugging manageable while maintaining efficiency.

**Principle: Minimal, Precise Edits**
Only mark text that actually changes. Repeating unchanged text makes edits harder to review and appears unprofessional. Break replacements into: [unchanged text] + [deletion] + [insertion] + [unchanged text].

### Tracked changes workflow

1. **Get markdown representation**: `pandoc --track-changes=all path-to-file.docx -o current.md`
2. **Identify and group changes**: Organize into logical batches (by section, type, or proximity)
3. **Read documentation and unpack**:
   - **MANDATORY**: Read [`references/ooxml.md`](references/ooxml.md) completely
   - Unpack: `python scripts/unpack.py file.docx dir`
   - Note the suggested RSID
4. **Implement changes in batches**: Use the Document Library for complex operations, or edit XML directly for simple ones
5. **Pack**: `python scripts/pack.py dir reviewed.docx --original file.docx`
6. **Final verification**: `pandoc --track-changes=all reviewed.docx -o verification.md`

---

## Dependencies

- **pandoc**: Text extraction (`apt-get install pandoc`)
- **docx**: `npm install -g docx` (new documents)
- **LibreOffice**: PDF conversion, tracked change acceptance (via `scripts/soffice.py`)
- **Poppler**: `pdftoppm` for images (`apt-get install poppler-utils`)
- **defusedxml**: Secure XML parsing (`pip install defusedxml`)
