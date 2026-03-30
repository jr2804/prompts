# vstash MCP Server Reference

Detailed MCP tool options and configuration.

## Tool Definitions

### vstash_add

Ingest files, directories, or URLs into memory.

```json
{
  "name": "vstash_add",
  "arguments": {
    "path": "/path/to/document.pdf"
  }
}
```

| Argument | Type | Description |
|----------|------|-------------|
| `path` | string | File path, directory path, or URL to ingest |

### vstash_search

Hybrid search with context expansion and relevance signal.

```json
{
  "name": "vstash_search",
  "arguments": {
    "query": "deployment strategy",
    "top_k": 5
  }
}
```

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `query` | string | required | Search query |
| `top_k` | integer | 5 | Number of results |

**Response:**
```json
{
  "chunks": [
    {
      "text": "...",
      "source": "/path/to/doc.pdf",
      "chunk_index": 3,
      "score": 0.87,
      "expanded_text": "..."  // ±1 adjacent chunks included
    }
  ],
  "relevance": "high",
  "hint": "Results match query well",
  "best_distance": 0.82
}
```

### vstash_ask

Semantic search + LLM-generated answer with sources.

```json
{
  "name": "vstash_ask",
  "arguments": {
    "query": "what's the main argument?",
    "top_k": 5
  }
}
```

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `query` | string | required | Question to answer |
| `top_k` | integer | 5 | Chunks to retrieve |

**Response:**
```json
{
  "answer": "The main argument is...",
  "chunks": [...],
  "sources": ["/path/to/doc.pdf"]
}
```

### vstash_list

List all ingested documents.

```json
{
  "name": "vstash_list",
  "arguments": {}
}
```

### vstash_stats

Database statistics.

```json
{
  "name": "vstash_stats",
  "arguments": {}
}
```

**Response:**
```json
{
  "documents": 42,
  "chunks": 1523,
  "size_bytes": 1048576
}
```

### vstash_forget

Remove a document from memory.

```json
{
  "name": "vstash_forget",
  "arguments": {
    "source": "/path/to/document.pdf"
  }
}
```

### vstash_collections

List all collections.

```json
{
  "name": "vstash_collections",
  "arguments": {}
}
```

### vstash_export

Export chunks with metadata for training data.

```json
{
  "name": "vstash_export",
  "arguments": {
    "project": "ml-survey",
    "format": "jsonl"
  }
}
```

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `project` | string | all | Filter by project |
| `collection` | string | all | Filter by collection |
| `format` | string | "jsonl" | Output format: "jsonl" or "csv" |

### vstash_job

Check status of background directory ingestion.

```json
{
  "name": "vstash_job",
  "arguments": {
    "job_id": "abc123"
  }
}
```

## Configuration Files

### claude_desktop_config.json

```json
{
  "mcpServers": {
    "vstash": {
      "command": "vstash-mcp",
      "env": {
        "VSTASH_CONFIG": "/path/to/vstash.toml"
      }
    }
  }
}
```

### vstash.toml (inference)

```toml
[inference]
backend = "ollama"  # or "cerebras", "openai"

[ollama]
host = "http://localhost:11434"
model = "llama3.2"
```

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `VSTASH_CONFIG` | Path to vstash.toml (useful for MCP when shell env doesn't apply) |

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Tools don't appear | vstash-mcp not on PATH | Use full path in config |
| "No module named vstash" | Different Python environment | Set `command` to full Python path |
| ask fails, search works | Missing inference config | Add backend + API key to vstash.toml |