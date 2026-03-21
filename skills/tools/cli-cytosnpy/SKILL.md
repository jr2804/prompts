______________________________________________________________________

## name: cli-cytosnpy description: > CLI tool for CytoScnPy - code metrics analysis for Python projects. Use when running code quality scans, calculating cyclomatic complexity, Halstead metrics, maintainability index, or generating project statistics. Triggers on: cytoscnpy commands, code metrics analysis, complexity reports, maintainability scoring, or MCP server setup for LLM integration.

# CytoScnPy CLI

Code metrics analysis tool for Python projects. Calculates LOC, complexity, Halstead metrics, and maintainability.

## Commands

```bash
# Raw metrics (LOC, LLOC, SLOC, Comments, Blank)
cytoscnpy raw [OPTIONS] <PATH>

# Cyclomatic Complexity
cytoscnpy cc [OPTIONS] <PATH>

# Halstead Metrics
cytoscnpy hal [OPTIONS] <PATH>

# Maintainability Index
cytoscnpy mi [OPTIONS] <PATH>

# Full project statistics report
cytoscnpy stats [OPTIONS] <PATH>

# Per-file metrics table
cytoscnpy table [OPTIONS] <PATH>

# MCP server for LLM integration
cytoscnpy mcp-server

# Initialize config (.cytoscnpy.toml)
cytoscnpy init
```

## Quality Gates

Use strict flags to fail CI when thresholds are exceeded (exit code 1):

```bash
cytoscnpy raw --max-loc 500 --max-complexity 15 <PATH>
```

## Configuration

Create `.cytoscnpy.toml` in project root, or add `[tool.cytoscnpy]` to `pyproject.toml`.

```bash
cytoscnpy init  # scaffolds config file
```

## MCP Server

Starts an MCP server for LLM integration. Requires the standalone CLI build (not the Python package).

```bash
cytoscnpy mcp-server
```

## Reference

See `references/cli-reference.md` for full option details.
