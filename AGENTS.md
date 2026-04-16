# prompts (and more)

Repository context for AI coding agents working in this project.

## Purpose

- Curated prompt/skill/instruction collection for AI coding assistants.
- Primary content lives in `commands/`, `skills/`, `instructions/`, and `agents-md/`.
- Python tooling exists mainly to run validation or helper scripts for skill development.

## Quick Commands

```bash
# Install toolchain and repo dependencies
mise up

# Run Python scripts (always through uv)
uv run ./skills/skill-creator/scripts/<script>.py

# Lint Python code
ruff check <paths> --fix

# Run tests
uv run pytest <paths> -v --tb=short
```

## Hard Requirements

- **ALWAYS** use `uv run` for Python execution.
- **ALWAYS** keep skill definitions compatible with the Agent Skills Specification: <https://agentskills.io/specification>
- **PREFER** pointers to canonical files over duplicated guidance.
- **KEEP** root agent docs short and high-signal; avoid long prose and auto-generated file trees.

## Project Map

- `commands/`: reusable operational prompts (linting, tests, planning, onboarding).
- `skills/`: capability modules grouped by domain (development, docs, MCP, tools, standards).
- `instructions/`: workflow-specific conventions (for example commit rules).
- `agents-md/`: AGENTS.md guidelines and templates.
- `documents/`: document-format-specific skills (`docx`, `pptx`, `xlsx`, `pdf`).

## Source of Truth

- Project overview and catalog: `README.md`
- Skill authoring constraints: `skills/AGENTS.md`
- AGENTS.md writing guidance: `agents-md/AGENTS-MD-GUIDELINES.md`
- Commit format and conventions: `instructions/commit-instructions.md`
- Python/runtime metadata: `pyproject.toml`

## Working Norms For Agents

- Make minimal, targeted edits; do not refactor unrelated areas.
- Before adding new logic or files, verify an equivalent pattern does not already exist.
- Validate changes with the smallest relevant lint/test scope.
- If task-specific details are needed, open the nearest domain `SKILL.md` file first.
