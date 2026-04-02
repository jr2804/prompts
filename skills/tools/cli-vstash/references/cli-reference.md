# vstash CLI Reference

Full command-line options for vstash.

## Global Flags

| Flag | Description |
|------|-------------|
| `--help, -h` | Show help message |
| `--version, -v` | Show version number |

## Commands

### vstash add

Add files, directories, or URLs to memory.

```bash
vstash add <path> [path ...] [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--collection <name>` | Assign to a collection |
| `--project <name>` | Assign project metadata |
| `--tags <tags>` | Comma-separated tags |
| `--dry-run` | Preview without ingesting |

**Examples:**

```bash
vstash add paper.pdf
vstash add ./docs --collection research --project ml-survey --tags "attention,transformers"
vstash add https://arxiv.org/abs/2310.06825
```

### vstash search

Semantic search without LLM (free, local).

```bash
vstash search "<query>" [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--top-k <n>` | Number of results (default: 5) |
| `--project <name>` | Filter by project |
| `--collection <name>` | Filter by collection |
| `--format <json\|pretty>` | Output format |

**Examples:**

```bash
vstash search "what's the main argument?"
vstash search "deployment strategy" --top-k 10
```

### vstash ask

Semantic search + LLM-generated answer.

```bash
vstash ask "<question>" [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--top-k <n>` | Number of chunks to retrieve (default: 5) |
| `--project <name>` | Filter by project |
| `--collection <name>` | Filter by collection |

**Examples:**

```bash
vstash ask "summarize the key findings"
vstash ask "what architectures were compared?" --project ml-survey
```

### vstash chat

Interactive Q&A session.

```bash
vstash chat [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--project <name>` | Filter by project |
| `--collection <name>` | Filter by collection |

### vstash list

List all ingested documents.

```bash
vstash list [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--project <name>` | Filter by project |
| `--collection <name>` | Filter by collection |
| `--format <table\|json>` | Output format |

### vstash stats

Show database statistics.

```bash
vstash stats
```

Returns: document count, total chunks, database size.

### vstash forget

Remove a document from memory.

```bash
vstash forget <source>
```

**Example:**

```bash
vstash forget paper.pdf
```

### vstash reindex

Re-embed all chunks with a new model (without re-ingesting).

```bash
vstash reindex [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--model <name>` | New embedding model |
| `--batch-size <n>` | Batch size for re-embedding |

### vstash watch

Watch directory for changes and auto-ingest.

```bash
vstash watch <directory> [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--collection <name>` | Default collection |
| `--project <name>` | Default project |
| `--interval <seconds>` | Check interval (default: 60) |

### vstash export

Export chunks as JSONL for training data.

```bash
vstash export [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--project <name>` | Filter by project |
| `--collection <name>` | Filter by collection |
| `--format <jsonl\|csv>` | Output format |
| `--output <file>` | Output file |

### vstash config

Show current configuration.

```bash
vstash config
```

### vstash-mcp

Start MCP server for Claude Desktop integration.

```bash
vstash-mcp
```

See [mcp-vstash skill](../mcp-servers/mcp-vstash/SKILL.md) for setup.
