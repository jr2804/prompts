---
name: mcp-vstash
description: MCP server integration for vstash document memory. Use when configuring Claude Desktop or other MCP-compatible AI assistants with persistent document memory, setting up vstash MCP tools for semantic search and Q&A, or integrating vstash with AI assistant workflows via Model Context Protocol.
---

# vstash MCP Server

Enable AI assistants (Claude Desktop, Cursor, Copilot) to search and answer questions from your local document memory via MCP.

## Setup

### 1. Install vstash

```bash
pip install vstash
```

### 2. Add to Claude Desktop config

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "vstash": {
      "command": "vstash-mcp"
    }
  }
}
```

> **pyenv users:** Use full path to binary:
> `"command": "/path/to/.pyenv/versions/3.x.x/bin/vstash-mcp"`

### 3. Restart Claude Desktop

The vstash tools appear in Claude's tool list.

## Available Tools

| Tool | Description |
|------|-------------|
| `vstash_add(path)` | Ingest file, directory, or URL into memory |
| `vstash_ask(query, top_k)` | Semantic search + LLM answer with sources |
| `vstash_search(query, top_k)` | Hybrid search with context expansion and relevance signal |
| `vstash_list()` | List all ingested documents |
| `vstash_stats()` | Database statistics (docs, chunks, size) |
| `vstash_forget(source)` | Remove document from memory |
| `vstash_collections()` | List all collections |
| `vstash_export(...)` | Export chunks as JSONL for training data curation |
| `vstash_job(job_id)` | Check status of background directory ingestion |

## Search Response Fields

`vstash_search` returns:

| Field | Description |
|-------|-------------|
| `chunks` | Array of results with ±1 adjacent chunks expanded |
| `relevance` | Confidence tier: `"high"`, `"medium"`, `"low"`, `"none"` |
| `hint` | Human-readable relevance explanation |
| `best_distance` | Cosine distance of best vector match (lower = more relevant) |

**Relevance tiers:**

| Distance | Tier | Meaning |
|----------|------|---------|
| ≤ 0.95 | high | Results are relevant |
| 0.95–0.98 | medium | Results may be tangential |
| > 0.98 | low | Results may not be relevant |

Works from first search — no warm-up period needed.

## API Key Configuration

MCP servers don't inherit shell environment variables. Configure inference in `~/.vstash/vstash.toml`:

```toml
[cerebras]
api_key = "your-key-here"
```

Or use fully local Ollama (no API key):

```toml
[inference]
backend = "ollama"

[ollama]
host = "http://localhost:11434"
model = "llama3.2"
```

## Troubleshooting

| Issue | Solution |
|-------|---------|
| Tools don't appear | Run `which vstash-mcp` to verify PATH |
| "No module named vstash" | MCP server uses different Python — use full path in config |
| `ask` fails but search works | Check inference backend configured in `vstash.toml` |

## Reference

See `references/mcp-reference.md` for tool-specific options and advanced configuration.
