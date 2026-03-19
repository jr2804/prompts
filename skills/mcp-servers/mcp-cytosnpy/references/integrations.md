# CytoScnPy Integrations Reference

**Source:** https://djinn-soul.github.io/CytoScnPy/integrations/

## VS Code Extension

Real-time feedback while you code. Access via Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`).

### Commands

Available through VS Code Command Palette.

### Configuration

Customize in VS Code Settings (`Ctrl+,`). See SKILL.md for full settings table.

## MCP Server (AI Assistants)

Enable AI assistants to use CytoScnPy tools via Model Context Protocol.

### GitHub Copilot

Automatically registered when VS Code extension is installed.

### Manual Setup (Claude/Cursor)

Run the server using the standalone CLI:

```bash
cytoscnpy mcp-server
```

**Claude Desktop Config:**

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

### Available Tools

When connected, CytoScnPy exposes:
- Security scanning (secrets, keys, tokens)
- Dangerous code pattern detection
- Code quality metrics (complexity, maintainability)
- Clone detection
- Raw metrics (LOC, SLOC, comments, blanks)

### Configuration

Tools are configured via VS Code extension settings or CLI flags.

> **Note:** HTTP/SSE transport is planned for future releases to enable remote analysis.

> **Important:** The MCP server is available in the standalone CLI binary (install script or `cytoscnpy-cli` build). The Python `cytoscnpy` package does not run `mcp-server`.

## CI/CD Integration

CytoScnPy supports structured output formats:
- JSON
- GitLab
- SARIF
- GitHub Annotations

See the CI/CD Integration Guide in the User Guide for detailed setup.
