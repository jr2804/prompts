# CytoScnPy CLI Reference

**Source:** https://djinn-soul.github.io/CytoScnPy/CLI/

## Command Syntax

```
cytoscnpy [OPTIONS] [COMMAND]
```

## Main Options

### Input & Output

Flags for specifying input paths and output formats.

### Scan Types

- `raw` — Raw metrics (LOC, LLOC, SLOC, Comments, Multi, Blank)
- `cc` — Cyclomatic Complexity
- `hal` — Halstead Metrics
- `mi` — Maintainability Index
- `stats` — Comprehensive project statistics report
- `table` — Per-file metrics table

### Analysis Configuration

Configuration options for scan behavior and output.

### Quality Thresholds (Gate Overrides)

Strict gates that cause exit code 1 when exceeded. Useful for CI enforcement.

## Subcommands

### `raw`

Calculate raw metrics (LOC, LLOC, SLOC, Comments, Multi, Blank).

```bash
cytoscnpy raw [OPTIONS] <PATH>
```

### `cc`

Calculate Cyclomatic Complexity.

```bash
cytoscnpy cc [OPTIONS] <PATH>
```

### `hal`

Calculate Halstead Metrics.

```bash
cytoscnpy hal [OPTIONS] <PATH>
```

### `mi`

Calculate Maintainability Index.

### `stats`

Generate comprehensive project statistics report.

### `table`

Show per-file metrics table.

### `mcp-server`

Start MCP server for LLM integration.

> **Note:** The `mcp-server` subcommand is handled by the `cytoscnpy-cli` binary. If you installed the Python package, `cytoscnpy mcp-server` will print an error. Use the standalone CLI build for MCP.

### `init`

Initialize CytoScnPy configuration in the current directory.

Creates `.cytoscnpy.toml` (or appends `[tool.cytoscnpy]` to `pyproject.toml`) and adds `.cytoscnpy` to `.gitignore` when possible.
