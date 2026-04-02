# Technology Stack

**Analysis Date:** 2026-04-02

## Languages

**Primary:**

- Markdown — Skills, prompts, commands, AGENTS.md guides, and documentation
- Python >= 3.14 — Helper scripts for skill validation, packaging, and Office document processing

**Secondary:**

- JSON — Skill lock file (`skills-lock.json`), MCP server configuration
- TOML — mise configuration (`config.toml`), vstash inference config

## Runtime

**Environment:**

- Python >= 3.14 (required in `pyproject.toml`)

**Package Manager:**

- `uv` (primary) — Python dependency and virtual environment manager
- `bun` — Node.js package manager for CLI tools (via mise)
- `mise` — Polyglot tool version manager; orchestrates `uv`, `bun`, ripgrep, tree-cli
- Lockfile: `uv.lock` (present, revision 3)

**Virtual Environment:**

- `.venv/` directory present at project root

## Frameworks

**Core:**

- None — This is a collection of skills, prompts, and instructions, not a single application

**Code Quality:**

- `ruff` >= 0.15.7 — Linting (isort-equivalent import sorting) and code formatting
- `mdformat` >= 1.0.0 — Markdown formatting

**Build/Dev:**

- `undersort` >= 0.1.5 — Underscore-prefixed import sorting (depends on `libcst`, `rich`)
- `saddle-cli` (npm) — Skill installation tool referenced in README

## Key Dependencies

**Direct (pyproject.toml):**

- `mdformat` >= 1.0.0 — Markdown auto-formatter
- `pyyaml` >= 6.0.3 — YAML parsing (used by skill validation scripts)
- `ruff` >= 0.15.8 — Python linter and formatter
- `undersort` >= 0.1.5 — Import sorting

**Transitive:**

- `libcst` >= 1.8.6 — Concrete syntax tree library (undersort dependency)
- `rich` >= 14.3.3 — Terminal formatting (undersort dependency)
- `pygments` >= 2.20.0 — Syntax highlighting (rich dependency)
- `markdown-it-py` >= 4.0.0 — Markdown parser (mdformat dependency)

**Skill Script Dependencies (declared via inline script metadata):**

- `requests`, `rich` — Referenced in `skills/AGENTS.md` example
- `pyyaml` — Used in `scripts/quick_validate.py`
- Various per-skill deps declared in `# /// script` blocks within individual Python scripts

**Mise-managed CLI Tools (via config.toml):**

- `ripgrep` (latest) — Fast file search
- `tree` / `tree-cli` (GitHub: peteretelej/tree) — Directory tree visualization
- `bun` (latest) — Node.js runtime
- `npm` (latest) — Node.js package manager
- `saddle-cli` (npm) — Skill management tool

## Configuration

**Environment:**

- `.env` files: Not detected (intentionally absent; secrets not managed in-repo)
- Configuration files: `.config/mise/config.toml`

**Build/Dev Tasks (mise tasks):**

- `env-sync`: `uv sync -U --dev --all-extras --all-groups`
- `format`: Runs undersort, ruff isort, ruff format, mdformat
- `add-skills`: Installs skills from various GitHub repositories via saddle-cli
- `upgrade-tools`: Upgrades all mise-managed tools

**MCP Server Configuration:**

- Configured per AI assistant (Claude Desktop, Cursor, VS Code Copilot) in assistant-specific config files
- Not stored in-repo; documented in individual MCP skill files under `skills/mcp-servers/`

## Platform Requirements

**Development:**

- Python >= 3.14
- `mise` installed (for tool management)
- `uv` installed (via mise or directly)
- `bun` installed (via mise)

**Production:**

- Not applicable — This is a skill/prompt collection, not a deployed application
- Skills are consumed by AI coding assistants (Claude Code, Cursor, Copilot, etc.)

______________________________________________________________________

*Stack analysis: 2026-04-02*
