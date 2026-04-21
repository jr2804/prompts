# Improvement Patterns

Common skill quality issues and their fixes.

## Critical Issues

### Missing Required Fields

**Issue:** SKILL.md missing `name` or `description` frontmatter field

**Before:**

```yaml
---
description: Does something useful.
---
```

**After:**

```yaml
---
name: my-skill
description: Does something useful. Use when working with data files.
---
```

### Invalid YAML Syntax

**Issue:** Malformed frontmatter (typos, wrong indentation, unclosed quotes)

**Before:**

```yaml
---
name: my skill
description: Very useful.
---
```

**After:**

```yaml
---
name: my-skill
description: Very useful.
---
```

### Broken File References

**Issue:** SKILL.md references files that don't exist

**Example:** `[Reference](references/guide.md)` but `references/guide.md` doesn't exist

**Fix:** Either create the referenced file or remove the reference

______________________________________________________________________

## Major Issues

### Weak Trigger Descriptions

**Issue:** Description too vague to trigger skill appropriately

**Before:**

```yaml
description: Helps with documents.
```

**After:**

```yaml
description: >
  Process, create, and modify Word documents (.docx). Use when the user
  wants to create reports, edit documents, add formatting, or work with
  Word files — even if they don't explicitly say "docx" or "Word".
```

### Second Person Voice

**Issue:** Description uses "you" or second person instead of imperative

**Before:**

```yaml
description: This skill helps you when you need to process CSVs.
```

**After:**

```yaml
description: Process and analyze CSV files. Use when the user has CSV data
  and wants to explore, transform, or export it.
```

### SKILL.md Too Long

**Issue:** Main SKILL.md exceeds 500 lines without using references/

**Fix:** Move detailed content to `references/` files with clear "see [file] for details" links

**Example SKILL.md structure:**

```markdown
# CSV Processing

## Quick Start
[brief overview with example]

## Advanced Features
- **Formulas**: See [references/formulas.md](references/formulas.md)
- **Performance**: See [references/performance.md](references/performance.md)
```

### Missing When to Use Section

**Issue:** SKILL.md doesn't explicitly state triggering scenarios

**Before:**

```markdown
# CSV Processing

This skill processes CSV files...
[content]
```

**After:**

```markdown
# CSV Processing

## When to Use
- User has CSV/TSV data and wants analysis
- User mentions spreadsheet data needing processing
- User asks to "clean" or "transform" tabular data

## How to Use
[workflow]
```

______________________________________________________________________

## Minor Issues

### Overly Verbose Descriptions

**Issue:** Description longer than necessary

**Before:**

```yaml
description: This skill is designed to help you process CSV files in an
  efficient and effective manner. It provides capabilities for reading
  CSV data, analyzing CSV data, transforming CSV data, and exporting
  CSV data in various formats.
```

**After:**

```yaml
description: Process, analyze, and export CSV files. Use when working
  with tabular data or spreadsheet imports.
```

### Missing Examples

**Issue:** Complex workflow without concrete examples

**Fix:** Add input/output example pairs where helpful

**Example:**

```markdown
## Example

**Input:** "Analyze sales data in monthly_sales.csv"
**Output:** Summary with top 5 products, monthly trend chart, profit margins
```

### Inconsistent Formatting

**Issue:** Mixed heading styles, inconsistent code blocks

**Fix:** Standardize formatting — use sentence case for headings, consistent code block language tags

______________________________________________________________________

## Before/After Patterns

### Name Format

**Before:**

```yaml
name: My_Skill
name: PDF-Processing
name: csv processor
```

**After:**

```yaml
name: my-skill
name: pdf-processing
name: csv-processor
```

### Description Imperative

**Before:**

```yaml
description: This skill does X. It is helpful when you need Y.
```

**After:**

```yaml
description: Do X. Use when you need Y.
```

### Section Organization

**Before:**

```markdown
# Skill Name

Everything you need to know about this skill...

[500+ lines of dense content]
```

**After:**

```markdown
# Skill Name

## Overview
[Brief purpose statement]

## Core Workflow
[Essential steps]

## When to Use
[Triggering scenarios]

## See Also
- [Detailed API](references/api.md)
- [Patterns](references/patterns.md)
```

______________________________________________________________________

## Verification Checklist

After applying fixes, verify:

- [ ] `uvx skills-ref validate` passes
- [ ] Description ≤1024 characters
- [ ] Name is hyphen-case, ≤64 characters
- [ ] No agent-specific references in body
- [ ] SKILL.md \<500 lines OR references/ used for overflow
- [ ] All file references resolve to existing files
