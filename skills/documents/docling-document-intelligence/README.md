# Docling agent skill (Cursor & compatible assistants)

This folder is an **[Agent Skill](https://agentskills.io/specification)**-style bundle for AI coding assistants: structured instructions (`SKILL.md`), a pipeline reference (`pipelines.md`), and a quality evaluator (`scripts/docling-evaluate.py`).

Conversion is done via the **`docling` CLI** (included with `pip install docling`).
The evaluator provides a **convert → evaluate → refine** feedback loop that the
existing CLI does not cover.

It complements the official [Docling documentation](https://docling-project.github.io/docling/) and the [`docling` CLI reference](https://docling-project.github.io/docling/reference/cli/).

The same layout is published in the Docling repo at `docs/examples/agent_skill/docling-document-intelligence/` (for docs and PRs).

## Contents

| Path | Purpose |
|------|---------|
| [`SKILL.md`](SKILL.md) | Full skill instructions (pipelines, chunking, evaluation loop) |
| [`pipelines.md`](pipelines.md) | Standard vs VLM pipelines, OCR engines, API notes |
| [`EXAMPLE.md`](EXAMPLE.md) | Installing into `~/.cursor/skills/`; running the CLI and evaluator |
| [`improvement-log.md`](improvement-log.md) | Optional template for local "what worked" notes |
| [`scripts/docling-evaluate.py`](scripts/docling-evaluate.py) | Heuristic quality report on JSON (+ optional Markdown) — self-contained via PEP 723 inline deps |

## Quick start

```bash
uv tool install docling

# Convert to Markdown
docling https://arxiv.org/pdf/2408.09869 --output /tmp/

# Convert to JSON
docling https://arxiv.org/pdf/2408.09869 --to json --output /tmp/

# Evaluate quality (uv resolves deps automatically via PEP 723 metadata)
uv run scripts/docling-evaluate.py /tmp/2408.09869.json --markdown /tmp/2408.09869.md
```

Use `--pipeline vlm` for vision-model pipelines; see `SKILL.md` and `pipelines.md`.

## License

MIT (aligned with [Docling](https://github.com/docling-project/docling)).
