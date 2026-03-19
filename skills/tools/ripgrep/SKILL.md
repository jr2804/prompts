---
name: ripgrep
description: Fast, recursive search tool for pattern matching in files with regex support, ignore handling, and glob filtering. Use when searching codebases for patterns, finding function definitions, filtering by file type, or performing find/replace operations. Triggers: "search for X in files", "find all occurrences of Y", "grep with glob patterns", "recursive search", "find using regex".
---

# ripgrep (rg)

Fast recursive search tool that searches files line-by-line for patterns.

## Basic Usage

```bash
rg <pattern> [path]        # Recursive search (default)
rg -F <literal> [path]     # Fixed string (no regex)
rg 'pattern' -g '*.rs'     # With glob filter
```

## Key Features

### Automatic Filtering (Default)
- Ignores `.gitignore`, `.ignore`, `.rgignore` patterns
- Skips hidden files/directories
- Skips binary files (files with NUL bytes)
- Doesn't follow symlinks

Override with:
```bash
--no-ignore          # Disable ignore filtering
--hidden -u          # Show hidden files (-u = --unrestricted)
-a --text            # Search binary files
-L --follow          # Follow symlinks
-uuu                 # Disable all filtering (3x unrestricted)
```

### Manual Filtering: Globs
```bash
rg pattern -g '*.toml'           # Only .toml files
rg pattern -g '!*.toml'           # Exclude .toml files
rg pattern -g '*.rs' -g '!test*' # Combine filters
```

### File Types
```bash
rg pattern --type rust           # -t<type> shorthand
rg pattern --type-not rust       # -T<type> exclude type
rg pattern --type-list            # List available types
rg --type-add 'web:*.{html,css,js}' -tweb pattern  # Custom type
```

### Replacements
```bash
rg fast README.md --replace FAST           # -r shorthand
rg '^.*fast.*$' README.md -r FAST        # Replace entire line
rg 'fast\s+(\w+)' -r 'fast-$1'           # Capture groups
```

### Configuration
Set `RIPGREP_CONFIG_PATH` env var. Each line is a flag:
```
--max-columns=150
--hidden
--smart-case
```

## Common Options

| Flag | Description |
|------|-------------|
| `-i --ignore-case` | Case insensitive search |
| `-S --smart-case` | Case insensitive unless pattern has uppercase |
| `-w --word-regexp` | Match whole words only |
| `-c --count` | Count matching lines |
| `-C --context N` | Show N lines around match |
| `-U --multiline` | Allow multiline matches |
| `-M --max-columns N` | Truncate long lines |
| `-z --search-zip` | Search compressed files |
| `-l --files-with-matches` | Print only filenames |
| `-o --only-matching` | Show only match, not full line |
| `--debug` | Show debug info (why files ignored, config loaded) |

## Preprocessor (Search Binary/Non-text)
```bash
# Create preprocessor script
cat preprocess
#!/bin/sh
exec pdftotext - -

# Use it
rg --pre ./preprocess 'pattern' file.pdf
rg --pre ./preprocess --pre-glob '*.pdf' 'pattern' .
```
