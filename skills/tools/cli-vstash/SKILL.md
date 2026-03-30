---
name: cli-vstash
description: "Local document memory with semantic search for AI-assisted workflows. Use when managing project documentation, codebases, or research papers that need persistent memory across sessions. Triggers on: vstash add/search/ask commands, document ingestion, semantic search, RAG pipelines, local knowledge bases, or configuring vstash for personal projects."
---

# vstash CLI

Local document memory with instant semantic search. Drop any file, ask anything.

## Core Commands

```bash
# Ingest documents (PDF, DOCX, PPTX, XLSX, Markdown, code, URLs)
vstash add paper.pdf notes.md https://example.com/article
vstash add ./docs --collection research --project ml-survey

# Semantic search (free, no LLM needed)
vstash search "what's the main argument about X?"

# Ask with LLM (requires inference backend)
vstash ask "summarize the key findings"

# Interactive chat session
vstash chat

# Document management
vstash list                          # Show all ingested documents
vstash stats                         # DB statistics (docs, chunks, size)
vstash forget paper.pdf              # Remove document from memory
vstash reindex                       # Switch embedding model without re-ingesting

# Auto-ingest on file changes
vstash watch ./docs

# Export for training data curation
vstash export --project ml-survey --format jsonl

# Show current configuration
vstash config
```

## Ingestion Pipeline

```
file/URL → parse → chunk → embed → store vectors → index text
```

**Parsing:**
- Non-code: markitdown (preserves structure)
- Code (`code_aware=true`): raw UTF-8 to preserve syntax

**Chunking strategies:**

| Mode | Files | Strategy |
|------|-------|----------|
| Semantic | MD, PDF, DOCX | Headers → paragraphs → fixed-window → merge small |
| Code-aware | Python, JS/TS, Go, Rust, Java | Split at top-level `def`/`class`/`func`/`fn` |

## Search Pipeline

```
query → embed → vector search (top-k×10) → keyword search (top-k×10) → RRF fusion → memory scoring → dedup → relevance signal → top-k
```

**Reciprocal Rank Fusion (RRF):** Merges vector + keyword rankings without comparable scores.

**Relevance signal:** Distance-based confidence tiers:
- ≤ 0.95: high (full confidence)
- 0.95–0.98: medium (uncertain)
- > 0.98: low (results may not match)

**Context expansion:** ±1 adjacent chunks included for LLM answers (2.64× more context).

## Configuration

Create `vstash.toml` in current directory or `~/.vstash/vstash.toml`:

```toml
[inference]
backend = "ollama"  # or "cerebras", "openai"

[ollama]
host = "http://localhost:11434"
model = "llama3.2"

[embeddings]
model = "BAAI/bge-small-en-v1.5"  # multilingual: "BAAI/bge-m3"

[chunking]
size = 1024
overlap = 128
code_aware = true

[scoring]
enabled = true  # frequency + temporal decay re-ranking
```

Run `vstash config` to see active settings.

## Metadata Filtering

```bash
vstash add notes.md --collection research --project ml-survey --tags "attention,transformers"
vstash list --project ml-survey
vstash ask "what architectures were compared?" --project ml-survey
```

Documents with YAML frontmatter are parsed automatically.

## Privacy

| Component | Local? |
|-----------|--------|
| Embeddings (FastEmbed ONNX) | Yes |
| Vector store (sqlite-vec) | Yes |
| Semantic search | Yes |
| Inference (Ollama) | Yes |
| Inference (Cerebras/OpenAI) | No — chunks sent to API |

For full privacy, use `backend = "ollama"` or use `vstash search` instead of `vstash ask`.

## Reference

See `references/cli-reference.md` for full option details.