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

```bash
rg -l 'oldName' src/                 # Files containing the name
rg -n -C 2 'oldName' src/            # Matches with surrounding context
```

### 2. Replace All Instances

Use an editor or a narrowly scoped script to replace the exact old text with
its replacement. Review the resulting diff before applying additional changes.

### 3. Verify Changes

```bash
rg -n 'oldName' src/                 # No output means no remaining matches
rg -n 'newName' src/                 # Confirm replacement locations
```

______________________________________________________________________

## Bulk Operations

For a small number of files, search for matches, inspect each context, edit the
intended occurrences, and verify the diff.

### Rename Function

1. Find files: `rg -l 'getUserData' src/`
2. Inspect matches and count occurrences; establish scope before editing.
3. Replace only intended occurrences, accounting for comments and strings.
4. Verify: `rg -n 'getUserData' src/` should return no matches.
5. Run relevant tests.

### Replace Deprecated Pattern

1. Find: `rg -n '\bvar\s+\w+' src/`
2. Analyze whether each occurrence should be reassigned or constant.
3. Replace only reviewed matches.
4. Verify that no unintended deprecated patterns remain.

### Update API Calls

1. Find: `rg -n '/api/auth/login' src/`
2. Replace the intended endpoint occurrences.
3. Run relevant integration tests.

______________________________________________________________________

## Code Transfer

Workflow: inspect → extract → insert.

### Copy Function Between Files

1. Locate the definition with a search such as `rg -n -A 20 'def validate_user' src/`.
2. Inspect the full definition, including decorators and related imports.
3. Check the target module for naming conflicts and existing dependencies.
4. Insert the code, update imports, and test both modules.

### Extract Functions to a New File

From the repository root, [examples/extract_functions.py](../examples/extract_functions.py)
provides a typed helper that moves matching module-level `def` and `async def`
definitions, including decorators. It creates a new target without overwriting an
existing file and removes moved definitions from the source only after staging
both outputs. This is a mechanical text move, not a dependency-aware refactor: it
copies imports but does not migrate module-level helpers/constants, callers, or
other imports. Inspect and update those references manually, then test both modules.

```bash
uv run skills/development/python-ultimate/examples/extract_functions.py \
  path/to/source.py path/to/new_module.py '.*_util$'
```

Replace the example paths and pattern with the project-specific values. The target
must not already exist. Review the diff and test both modules after the move.

### Extract Class to New File

1. Locate the definition, for example `rg -n -A 50 'class DatabaseConnection' src/`.
2. Inspect the full class and its dependencies.
3. Create the target module, update imports in the source, then remove the old class.
4. Check for import cycles and test both modules.

______________________________________________________________________

## Line-Based Operations

Prefer context-aware edits over fixed line numbers because earlier changes can
shift the target. For a new file or a user-specified insertion line, use an
available editor or a small script, then inspect the resulting diff and run
syntax checks and tests. Do not rely on an external insertion helper unless it
is present in the current repository and its behavior has been verified.

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

1. **Search** → Find all instances first.
2. **Analyze** → Verify changes are appropriate.
3. **Inform** → Tell user of scope before proceeding.
4. **Execute** → Make changes.
5. **Verify** → Confirm changes applied correctly.
6. **Test** → Run relevant checks.

### Always Check

- Strings/comments: clarify whether they should change.
- Exported APIs: warn of breaking changes.
- Case sensitivity: be explicit in search patterns.
- Import statements: update after moving code.

______________________________________________________________________

## Common Patterns

### Planning Checklist

- [ ] Find all instances first.
- [ ] Review context of each match.
- [ ] Inform user of scope.
- [ ] Consider edge cases (strings, comments).
- [ ] Identify exact start/end of code blocks.
- [ ] Check target file structure.

### Preservation Checklist

- [ ] Include docstrings and comments.
- [ ] Transfer related functions together.
- [ ] Update imports in both source and target.
- [ ] Maintain formatting and indentation.

### Validation Checklist

- [ ] Verify insertion placement.
- [ ] Check syntax after changes.
- [ ] Test imports work correctly.
- [ ] Run project tests.
