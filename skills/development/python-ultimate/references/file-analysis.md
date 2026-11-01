# File Analysis Reference

Comprehensive guide for non-destructive file analysis using read-only operations.

## Table of Contents

1. [Non-Destructive Principle](#non-destructive-principle)
2. [File Metadata](#file-metadata)
3. [Line Counting](#line-counting)
4. [Pattern Searching](#pattern-searching)
5. [Content Statistics](#content-statistics)
6. [Codebase Analysis Patterns](#codebase-analysis-patterns)

______________________________________________________________________

## Non-Destructive Principle

**Core Rule**: Never modify files during analysis. Use only read-only operations.

### Allowed Operations

| Capability | Purpose | Safe for Large Files |
|------|---------|---------------------|
| File inspection | View file contents; use bounded reads for large files | Partial reads with offsets/limits |
| Filesystem metadata/listing | File sizes, timestamps, and directory contents | Yes |
| `wc -l` | Line counting | Yes |
| Text search (for example, `rg`) | Pattern searching | Yes |
| File discovery (for example, `find` or `rg --files`) | Locate files by path or pattern | Yes |

### Forbidden Operations

- `sed`, `awk` for in-place editing
- `echo > file` or output redirection for writing
- Any tool that modifies file content

______________________________________________________________________

## File Metadata

### Get Single File Metadata

```bash
stat -f "%z bytes, modified %Sm" [file_path]     # macOS
stat --printf="%s bytes, modified %y\n" [file_path]  # Linux
```

### List Multiple Files with Sizes

```bash
ls -lh [directory]                              # Human-readable sizes
ls -ltr [directory]                            # Sort by modification time
```

### Get Directory Disk Usage

```bash
du -h [file_path]                              # Human-readable
du -sh [directory]                             # Total only
du -ah [directory] | sort -rh | head -20       # Largest files
```

### File Modification Times

```bash
stat [file_path]                               # Full stat output
ls -l [file_path]                              # Modification time
```

______________________________________________________________________

## Line Counting

### Single File

```bash
wc -l [file_path]                              # Line count
```

### Multiple Files

```bash
wc -l [file1] [file2] [file3]                  # Count multiple files
wc -l *.py                                     # Wildcard expansion
```

### Directory Totals

```bash
find [dir] -name "*.py" | xargs wc -l           # All Python files
find . -type f -name "*.py" -exec wc -l {} +    # Recursive with exec
```

### Filtered Counting

```bash
find . -name "test_*.py" | xargs wc -l          # Test files only
find . -path ./node_modules -prune -o -type f -print | xargs wc -l  # Exclude directories
```

______________________________________________________________________

## Pattern Searching

### Count Matches

```bash
rg -c '^def ' src/
rg -c '^class ' src/
rg -c '^import ' src/
```

### Find with Line Numbers

```bash
rg -n 'TODO|FIXME|HACK' .
```

### Find Files by Pattern

```bash
rg --files -g '*.py'
rg --files docs/ -g '*.md'
```

### Search with Inclusion Filter

```bash
rg -n 'function' src/ -g '*.js'
rg -n 'class' . -g '*.ts'
```

### Common Patterns for Code Analysis

| Pattern | Purpose |
|---------|---------|
| `^def` | Top-level functions |
| `^class` | Top-level classes |
| `^import` | Import statements |
| `^from` | From imports |
| `TODO\|FIXME\|HACK` | Code markers |
| `console\.log` | Debug statements |
| `print\(` | Print statements |

______________________________________________________________________

## Content Statistics

### Analyze File Structure

1. Inspect the file to understand its structure
2. Count functions: `rg -c '^def ' file.py`
3. Count classes: `rg -c '^class ' file.py`
4. Count imports: `rg -c '^(import |from )' file.py`

### Code Quality Metrics

```bash
# Total lines of code
find . -name "*.py" -not -path "./venv/*" | xargs wc -l

# Comment lines
rg -c '^[[:space:]]*#' -g '*.py' .

# Blank lines
rg -c '^$' -g '*.py' .

# Calculate comment ratio
# (comment lines / total lines) * 100
```

### Find Largest Files

```bash
find . -type f -not -path "./node_modules/*" -not -path "./.git/*" \
  -exec du -h {} + | sort -rh | head -20
```

______________________________________________________________________

## Codebase Analysis Patterns

### Comprehensive File Analysis Workflow

1. **Get metadata**: use the platform's file metadata command
2. **Count lines**: `wc -l file.py`
3. **Inspect file**: use a file viewer or editor in read-only mode
4. **Count functions**: `rg -c '^def ' file.py`
5. **Count classes**: `rg -c '^class ' file.py`

### Compare File Sizes

1. **Find files**: `rg --files src/ -g '*.py'`
2. **Get sizes**: `ls -lh src/**/*.py`
3. **Total size**: `du -sh src/`

### Project-wide Analysis

1. **Count all source files**: `rg --files -g '*.py' | wc -l`
2. **Lines per file**: `find . -name "*.py" | xargs wc -l | sort -n`
3. **Identify largest files**: `du -ah . | sort -rh | head -20`
4. **Find duplicate names**: `find . -name "*.py" | xargs -I{} basename {} | sort | uniq -c | sort -rn`

From the repository root, [examples/codebase_audit.py](../examples/codebase_audit.py)
provides a runnable complexity and file-size audit example:

```bash
uv run skills/development/python-ultimate/examples/codebase_audit.py
```

### Integration with Other Skills

- **code-auditor**: Use file analysis before auditing
- **code-transfer**: Analyze large files before transfer decisions
- **codebase-documenter**: Use stats to understand file purposes

______________________________________________________________________

## Best Practices

1. **Always prefer read-only**: Never modify files during analysis
2. **Use efficient tools**: inspect small files fully and search large files by pattern
3. **Context-aware**: Compare to project averages
4. **Partial reads for large files**: use bounded reads with offsets and limits
5. **Chain operations**: combine file discovery and text search for targeted analysis
6. **Sort and filter**: Use `sort`, `head`, `tail` for useful outputs
