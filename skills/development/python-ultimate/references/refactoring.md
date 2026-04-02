# Refactoring Reference

Quick reference for bulk code refactoring and transfer operations.

## Table of Contents

1. [Refactoring Workflow](#refactoring-workflow)
2. [Bulk Operations](#bulk-operations)
3. [Code Transfer](#code-transfer)
4. [Line-Based Operations](#line-based-operations)
5. [Execution Mode (10+ Files)](#execution-mode-10-files)
6. [Safety Checks](#safety-checks)
7. [Common Patterns](#common-patterns)

______________________________________________________________________

## Refactoring Workflow

**Find → Replace → Verify**

### 1. Find All Occurrences

```
Grep(pattern="oldName", output_mode="files_with_matches")           # Find files
Grep(pattern="oldName", output_mode="content", -n=true, -B=2, -A=2) # Verify with context
```

### 2. Replace All Instances

```
Edit(
  file_path="src/api.js",
  old_string="oldName",
  new_string="newName",
  replace_all=true
)
```

### 3. Verify Changes

```
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

**Read → Extract → Insert**

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

```
Edit(
  file_path="src/utils.py",
  old_string="def existing():\n    pass",
  new_string="def existing():\n    pass\n\ndef new():\n    return True"
)
```

______________________________________________________________________

## Line-Based Operations

Use `line_insert.py` script for exact line insertion:

```bash
python3 skills/code-transfer/scripts/line_insert.py <file> <line_number> <code> [--backup]
```

**Examples:**

```bash
# Insert function at line 50
python3 skills/code-transfer/scripts/line_insert.py src/utils.py 50 "def helper():\n    pass"

# Insert with backup
python3 skills/code-transfer/scripts/line_insert.py src/utils.py 50 "code" --backup

# Insert at beginning
python3 skills/code-transfer/scripts/line_insert.py src/new.py 1 "import os"
```

**When to use:**

- User specifies exact line number
- Inserting into new/empty files
- Inserting at beginning/end without context

______________________________________________________________________

## Execution Mode (10+ Files)

**Auto-switches for 90% token savings on 10+ files.**

### Refactoring

```python
from api.code_transform import rename_identifier

result = rename_identifier('.', 'oldName', 'newName', '**/*.py')
# Returns: {'files_modified': 50, 'total_replacements': 247}
```

### Code Transfer

```python
from api.filesystem import batch_copy
from api.code_analysis import find_functions

functions = find_functions('app.py', pattern='handle_.*')
operations = [{
    'source_file': 'app.py',
    'start_line': f['start_line'],
    'end_line': f['end_line'],
    'target_file': 'handlers.py',
    'target_line': -1
} for f in functions]
batch_copy(operations)
```

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
