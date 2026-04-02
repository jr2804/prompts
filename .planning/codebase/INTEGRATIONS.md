# External Integrations

**Analysis Date:** 2026-04-02

## APIs & External Services

**Skill Registries:**

- GitHub (jr2804/prompts) — Source for locked skills in `skills-lock.json`
  - Source type: `github`
  - Ref: `main`
  - Skills locked: `coding-principles`, `python-cli`, `python-linter`, `python-no-type-checking-guard`, `python-standards`, `testing-strategy`
- Various GitHub repos via saddle-cli — Skills installed to `.agents/skills/` (managed by `mise add-skills` task)

**AI Assistant Platforms (consumers):**

- Claude Desktop — MCP server integration target
- Cursor — MCP server integration target
- VS Code + Copilot — MCP server integration target

**External MCP Servers (documented, not bundled):**

- `vstash` — Document memory (semantic search, Q&A)

  - Install: `pip install vstash`
  - Config: `~/.vstash/vstash.toml` (Cerebras API key or local Ollama)
  - Binary: `vstash-mcp`

- `grepai` — Semantic code search

  - GitHub: https://github.com/yoanbernabeu/grepai
  - Commands: `grepai search`, `grepai trace`

- `cytoscnpy` — Code metrics analysis

  - Binary: `cytoscnpy-cli` (standalone binary required)
  - GitHub: https://github.com/djinn-soul/CytoScnPy
  - Subcommand: `cytoscnpy mcp-server`

- `sequential-thinking` — Step-by-step reasoning

  - Skill location: `skills/mcp-servers/mcp-sequential-thinking/`

- `desktop-commander` — Desktop automation

  - Skill location: `skills/mcp-servers/mcp-desktop-commander/`

## Data Storage

**Databases:**

- None — No persistent database in this repository
- Skill `database-schema` references PostgreSQL, SQLite, and MongoDB in documentation assets only

**File Storage:**

- Local filesystem only — Skills, prompts, and instructions stored as Markdown and Python files

**Caching:**

- `__pycache__` — Standard Python bytecode cache (gitignored)

## Authentication & Identity

**Auth Provider:**

- Not applicable — No authentication in this repository
- Skill `3gpp-portal-authentication` documents 3GPP portal auth patterns for external use

## Monitoring & Observability

**Error Tracking:**

- None

**Logs:**

- Not applicable — No runtime application

## CI/CD & Deployment

**Hosting:**

- GitHub (jr2804/prompts) — Source repository

**CI Pipeline:**

- None detected — No GitHub Actions workflows or CI configuration files

**Deployment:**

- Skills are deployed to AI assistants via `saddle-cli` or manual installation
- `mise add-skills` task automates skill installation from GitHub

## Environment Configuration

**Required env vars:**

- None for the repository itself
- MCP servers documented in skills may require API keys:
  - `vstash`: Cerebras API key in `~/.vstash/vstash.toml`
  - Other MCP servers: Configure per their individual documentation

**Secrets location:**

- Not managed in-repo
- `.env` files gitignored (not present)

## Webhooks & Callbacks

**Incoming:**

- None

**Outgoing:**

- None — Skills describe patterns but this repo does not fire webhooks

## Agent Skill Ecosystem

**Installed Skills (.agents/skills/):**

- `coding-principles` — Source: `jr2804/prompts`
- `python-cli` — Source: `jr2804/prompts`
- `python-linter` — Source: `jr2804/prompts`
- `python-no-type-checking-guard` — Source: `jr2804/prompts`
- `python-standards` — Source: `jr2804/prompts`
- `testing-strategy` — Source: `jr2804/prompts`

**External Skills (managed by add-skills task):**

- `visual-explainer` — Source: `nicobailon/visual-explainer`
- `code-deduplication` — Source: `alinaqi/claude-bootstrap` (skill: `code-deduplication`)
- `stop-slop` — Source: `hardikpandya/stop-slop`
- `kreuzberg` — Source: `kreuzberg-dev/kreuzberg`
- `debug-skill` — Source: `AlmogBaku/debug-skill`

**Skill Metadata:**

- Lock file: `skills-lock.json` (version 1)
- Each locked skill has: `source`, `ref`, `sourceType`, `computedHash`
- Skill hash verification prevents stale skill updates

______________________________________________________________________

*Integration audit: 2026-04-02*
