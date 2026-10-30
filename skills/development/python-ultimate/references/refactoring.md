# Refactoring Reference

Quick reference for bulk code refactoring and transfer operations.

## Table of Contents

1. [Refactoring Workflow](#refactoring-workflow)
2. [Bulk Operations](#bulk-operations)
3. [Code Transfer](#code-transfer)
4. [Line-Based Operations](#line-based-operations)
5. [Python Batch Operations (10+ Files)](#python-batch-operations-10-files)
6. [Safety Checks](#safety-checks)
7. [Common Patterns](#common-patterns)

______________________________________________________________________

## Refactoring Workflow

Workflow: Find → Replace → Verify.

### 1. Find All Occurrences

```text
Grep(pattern="oldName", output_mode="files_with_matches")           # Find files
Grep(pattern="oldName", output_mode="content", -n=true, -B=2, -A=2) # Verify with context
```

### 2. Replace All Instances

```text
Edit(
  file_path="src/api.js",
  old_string="oldName",
  new_string="newName",
  replace_all=true
)
```

### 3. Verify Changes

```text
Grep(pattern="oldName", output_mode="files_with_matches")  # Should return none
Grep(pattern="newName", output_mode="content", -n=true)     # Confirm replacements
```

______________________________________________________________________

## Bulk Operations

**Use Grep + Edit with replace_all for 1-9 files.**

### Rename Function

1. Find: `Grep(pattern="getUserData", output_mode="files_with_matches")`
2. Count occurrences and inform user of scope
3. Replace in each file with `replace_all=true`
4. Verify: Re-run Grep for old name (should be empty)
5. Suggest running tests

### Replace Deprecated Pattern

1. Find: `Grep(pattern="\\bvar\\s+\\w+", output_mode="content", -n=true)`
2. Analyze: Check if reassigned (let) or constant (const)
3. Replace: `Edit(old_string="var count = 0", new_string="let count = 0")`
4. Verify: `Grep` for deprecated pattern returns empty

### Update API Calls

1. Find: `Grep(pattern="/api/auth/login", output_mode="content", -n=true)`
2. Replace: `Edit(old_string="'/api/auth/login'", new_string="'/api/v2/auth/login'", replace_all=true)`
3. Test: Recommend integration tests

______________________________________________________________________

## Code Transfer

Workflow: Read → Extract → Insert.

### Copy Function Between Files

1. Find: `Grep(pattern="def validate_user", -n=true, -A=20)`
2. Extract: `Read(file_path="auth.py", offset=45, limit=15)`
3. Check target: `Read(file_path="validators.py")`
4. Insert: Use Edit or line_insert.py

### Extract Class to New File

1. Locate: `Grep(pattern="class DatabaseConnection", -n=true, -A=50)`
2. Extract: `Read(file_path="original.py", offset=100, limit=50)`
3. Create: `Write(file_path="database.py", content="<extracted>")`
4. Update imports: `Edit` in original file
5. Remove old class: `Edit` with replacement

### Insert Relative to Content

Use **Edit** when insertion point is relative to existing code:

```text
Edit(
  file_path="src/utils.py",
  old_string="def existing():\n    pass",
  new_string="def existing():\n    pass\n\ndef new():\n    return True"
)
```

______________________________________________________________________

## Line-Based Operations

Prefer context-aware edits over fixed line numbers because earlier changes can
shift the target. For a new file or a user-specified insertion line, use the
available editor or a small script, then inspect the resulting diff and run
syntax/tests. Do not rely on an external `line_insert.py` helper unless it is
present in the current repository and its behavior has been verified.

______________________________________________________________________

## Python Batch Operations (10+ Files)

For a repetitive operation across many files, use one deterministic `uv`-run
script rather than serially editing each file. Define the scope first, preview
all intended changes, and make writing opt-in. Avoid claims of fixed token or
speed savings; measure outcomes for the actual task.

From the repository root, the companion [bulk_refactor.py](../examples/bulk_refactor.py)
demonstrates a textual identifier rename. It previews by default and changes
files only when passed `--apply`:

```bash
uv run skills/development/python-ultimate/examples/bulk_refactor.py --root src --old old_name --new new_name
uv run skills/development/python-ultimate/examples/bulk_refactor.py --root src --old old_name --new new_name --apply
```

This is a textual replacement example, not a syntax-aware Python refactor: it
also matches comments and strings. Review the preview and diff; use an AST-aware
or project-specific refactor when matches must be limited to Python identifiers.

### Batch Safety Checklist

1. Enumerate and count the target files before editing.
2. Exclude generated, virtual-environment, vendored, and build directories.
3. Preview matched locations and intended replacements; keep preview as default.
4. Apply only after confirming the scope and preserving a recoverable diff.
5. Run focused tests, formatters, and searches for missed or unintended matches.
6. Report files scanned, files changed, replacement counts, and verification.

______________________________________________________________________

## Safety Checks

**Verify after each change.**

1. **Search** → Find all instances first
2. **Analyze** → Verify changes are appropriate
3. **Inform** → Tell user of scope before proceeding
4. **Execute** → Make changes
5. **Verify** → Confirm changes applied correctly
6. **Test** → Suggest running tests

### Always Check

- Strings/comments: Ask if should update
- Exported APIs: Warn of breaking changes
- Case sensitivity: Be explicit in patterns
- Import statements: Update after moving code

### Tool Reference

**Edit with replace_all:**

- `replace_all=true`: Replace all occurrences
- `replace_all=false`: Replace only first (or fail if multiple)
- Must match EXACTLY (whitespace, quotes)

**Grep options:**

- `-n=true`: Show line numbers
- `-B=N, -A=N`: Context lines before/after
- `-i=true`: Case-insensitive
- `type="py"`: Filter by file type

______________________________________________________________________

## Common Patterns

### Planning Checklist

- [ ] Find all instances first
- [ ] Review context of each match
- [ ] Inform user of scope
- [ ] Consider edge cases (strings, comments)
- [ ] Identify exact start/end of code blocks
- [ ] Check target file structure

### Preservation Checklist

- [ ] Include docstrings and comments
- [ ] Transfer related functions together
- [ ] Update imports in both source and target
- [ ] Maintain formatting/indentation
- [ ] Use `--backup` for significant changes

### Validation Checklist

- [ ] Verify insertion placement
- [ ] Check syntax after changes
- [ ] Test imports work correctly
- [ ] Run project tests
