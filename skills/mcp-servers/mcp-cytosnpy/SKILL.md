---
name: mcp-cytosnpy
description: >
  MCP server integration for CytoScnPy code metrics analysis.
  Use when configuring CytoScnPy MCP server for AI assistants (Claude, Cursor, Copilot),
  setting up VS Code extension integration, or exposing code quality tools via MCP.
  Triggers on: mcp-cytosnpy, cytoscnpy mcp-server, MCP server setup, AI assistant
  code analysis integration, VS Code extension configuration.
---

# CytoScnPy MCP Server

Enable AI assistants (Claude, Cursor, Copilot) to use CytoScnPy code metrics tools via MCP.

> **Requires:** Standalone CLI binary (`cytoscnpy-cli`). The Python package does not support `mcp-server`.

## Quick Setup

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "cytoscnpy": {
      "command": "cytoscnpy",
      "args": ["mcp-server"]
    }
  }
}
```

### VS Code + Copilot

The VS Code extension automatically registers the MCP server. Just ask Copilot:

```
"Run a security scan on this file"
```

No extra config needed when extension is installed.

### Cursor

Same config as Claude Desktop — add to Cursor's MCP settings.

## Available Tools

When connected, CytoScnPy exposes code analysis tools to the AI assistant:

- **Security scan** — Detect secrets, keys, tokens
- **Danger scan** — Detect dangerous code patterns
- **Quality scan** — Code quality metrics (complexity, maintainability)
- **Clone detection** — Find duplicate code
- **Raw metrics** — LOC, SLOC, comments, blanks

## VS Code Extension Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `cytoscnpy.analysisMode` | `workspace` | `workspace` (accurate) or `file` (fast) |
| `cytoscnpy.enableSecretsScan` | `false` | Scan for keys/tokens |
| `cytoscnpy.enableDangerScan` | `false` | Dangerous code patterns |
| `cytoscnpy.enableQualityScan` | `false` | Code quality metrics |
| `cytoscnpy.enableCloneScan` | `false` | Clone detection |
| `cytoscnpy.confidenceThreshold` | `0` | Min confidence (0-100) |
| `cytoscnpy.excludeFolders` | `[]` | Folders to exclude |
| `cytoscnpy.includeFolders` | `[]` | Folders to force-include |
| `cytoscnpy.maxComplexity` | `10` | Max Cyclomatic Complexity |
| `cytoscnpy.minMaintainabilityIndex` | `40` | Min Maintainability Index |
| `cytoscnpy.maxNesting` | `3` | Max nesting depth |
| `cytoscnpy.maxArguments` | `5` | Max function arguments |
| `cytoscnpy.maxLines` | `50` | Max function lines |

## CI/CD Output Formats

CytoScnPy supports JSON, GitLab, SARIF, and GitHub Annotations for CI/CD integration.

## Reference

See `references/integrations.md` for full details.
