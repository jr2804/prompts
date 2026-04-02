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

| Tool | Purpose | Safe for Large Files |
|------|---------|---------------------|
| `Read` | View file contents | Partial reads with offset/limit |
| `stat` / `bash ls` | File metadata | Yes |
| `wc -l` | Line counting | Yes |
| `Grep` | Pattern searching | Yes |
| `Glob` | File discovery | Yes |

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

```
Grep(pattern="^def ", output_mode="count", path="src/")
Grep(pattern="^class ", output_mode="count", path="src/")
Grep(pattern="^import ", output_mode="count", path="src/")
```

### Find with Line Numbers

```
Grep(pattern="TODO|FIXME|HACK", output_mode="content", -n=true)
```

### Find Files by Pattern

```
Glob(pattern="**/*.py")
Glob(pattern="**/*.md", path="docs/")
```

### Search with Inclusion Filter

```
Grep(pattern="function", include="*.js", path="src/")
Grep(pattern="class", include="*.ts", path=".")
```

### Common Patterns for Code Analysis

| Pattern | Purpose |
|---------|---------|
| `^def ` | Top-level functions |
| `^class ` | Top-level classes |
| `^import ` | Import statements |
| `^from ` | From imports |
| `TODO\|FIXME\|HACK` | Code markers |
| `console\.log` | Debug statements |
| `print\(` | Print statements |

______________________________________________________________________

## Content Statistics

### Analyze File Structure

1. Read the file to understand structure
2. Count functions: `Grep(pattern="^def ", output_mode="count")`
3. Count classes: `Grep(pattern="^class ", output_mode="count")`
4. Count imports: `Grep(pattern="^import |^from ", output_mode="count")`

### Code Quality Metrics

```bash
# Total lines of code
find . -name "*.py" -not -path "./venv/*" | xargs wc -l

# Comment lines
Grep(pattern="^[[:space:]]*#", output_mode="count", include="*.py")

# Blank lines
Grep(pattern="^$", output_mode="count", include="*.py")

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

1. **Get metadata**: `stat -f "%z bytes, modified %Sm" file.py`
2. **Count lines**: `wc -l file.py`
3. **Read file**: `Read(file_path="file.py")`
4. **Count functions**: `Grep(pattern="^def ", output_mode="count")`
5. **Count classes**: `Grep(pattern="^class ", output_mode="count")`

### Compare File Sizes

1. **Find files**: `Glob(pattern="src/**/*.py")`
2. **Get sizes**: `ls -lh src/**/*.py`
3. **Total size**: `du -sh src/`

### Project-wide Analysis

1. **Count all source files**: `Glob(pattern="**/*.py")` then count
2. **Lines per file**: `find . -name "*.py" | xargs wc -l | sort -n`
3. **Identify largest files**: `du -ah . | sort -rh | head -20`
4. **Find duplicate names**: `find . -name "*.py" | xargs -I{} basename {} | sort | uniq -c | sort -rn`

### Integration with Other Skills

- **code-auditor**: Use file analysis before auditing
- **code-transfer**: Analyze large files before transfer decisions
- **codebase-documenter**: Use stats to understand file purposes

______________________________________________________________________

## Best Practices

1. **Always prefer read-only**: Never modify files during analysis
2. **Use efficient tools**: Read small files fully, use Grep for large files
3. **Context-aware**: Compare to project averages
4. **Partial reads for large files**: Use `Read` with offset/limit
5. **Chain operations**: Combine Glob + Grep for targeted analysis
6. **Sort and filter**: Use `sort`, `head`, `tail` for useful outputs
