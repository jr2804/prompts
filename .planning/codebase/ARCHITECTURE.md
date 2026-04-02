# Architecture

**Analysis Date:** 2026-04-02

## Pattern Overview

**Overall:** Content-organized knowledge repository following the [Agent Skills Specification](https://agentskills.io/specification).

**Key Characteristics:**
- Domain-driven skill organization (`skills/` directory tree)
- Dual-location skill model: canonical (`skills/`) and installed (`.agents/skills/`)
- Markdown-first content with YAML frontmatter metadata
- Optional Python scripts for deterministic/repetitive tasks
- Designed as a source for `saddle-cli` skill installation

## Layers

**Skills Layer (`skills/`):**
- Purpose: Canonical skill definitions organized by domain
- Location: `skills/`
- Contains: SKILL.md files, optional scripts/, references/, assets/, LICENSE.txt
- Depends on: Agent Skills Specification
- Used by: saddle-cli, coding assistants (Claude, etc.)

**Installed Skills Layer (`.agents/skills/`):**
- Purpose: Local copies of skills installed/enabled for the workspace
- Location: `.agents/skills/`
- Contains: SKILL.md + optional support files (mirrors skills/ structure)
- Depends on: `skills-lock.json` for version tracking
- Used by: Coding assistants during agent sessions

**Commands Layer (`commands/`):**
- Purpose: Reusable slash-command definitions for coding assistants
- Location: `commands/`
- Contains: Markdown files with command definitions
- Depends on: Nothing external
- Used by: Coding assistants (Claude Code, etc.)

**Instructions Layer (`instructions/`):**
- Purpose: Persistent instruction files for coding assistants
- Location: `instructions/`
- Contains: Markdown instruction files
- Depends on: Nothing external
- Used by: Coding assistants

**Agents Layer (`agents-md/`):**
- Purpose: AGENTS.md templates and guidelines
- Location: `agents-md/`
- Contains: Template AGENTS.md files, guidelines documentation
- Depends on: Nothing external
- Used by: Projects adopting AGENTS.md patterns

**Infrastructure Layer (`.config/`):**
- Purpose: Tool configuration (mise, etc.)
- Location: `.config/mise/config.toml`
- Contains: Tool versions, task definitions
- Depends on: mise, uv, bun
- Used by: Developer environment setup

## Data Flow

**Skill Creation Flow:**

1. Developer creates skill directory under `skills/<domain>/<skill-name>/`
2. SKILL.md written with YAML frontmatter (name, description) + Markdown body
3. Optional: scripts/, references/, assets/ directories added
4. `skills/skill-creator/scripts/init_skill.py` scaffolds the structure
5. `skills/skill-creator/scripts/quick_validate.py` validates compliance

**Skill Installation Flow:**

1. `saddle-cli` or `skills add` reads from this repository as source
2. Skills are copied/linked to `.agents/skills/`
3. `skills-lock.json` records source, ref, and content hash
4. Installed skills are available to coding assistants

**Skill Consumption Flow:**

1. Coding assistant reads SKILL.md frontmatter (name + description) from available skills
2. Based on user request, matching skill is loaded into context
3. Full SKILL.md body + bundled resources loaded on trigger
4. Scripts executed via `uv run` when deterministic operations needed

## Key Abstractions

**Skill (SKILL.md):**
- Purpose: Self-contained capability package for coding assistants
- Examples: `skills/python/coding-principles/SKILL.md`, `skills/documents/pdf/SKILL.md`
- Pattern: YAML frontmatter (name, description) + Markdown instructions + optional bundled resources

**Command (commands/*.md):**
- Purpose: Slash-command definition for coding assistants
- Examples: `commands/create-skill-from-url.md`, `commands/py-lint.md`
- Pattern: Markdown file with workflow steps, triggered by name

**Agent Guide (agents-md/AGENTS.md):**
- Purpose: Template for repository-level agent configuration
- Examples: `agents-md/AGENTS.md` (template with placeholders)
- Pattern: Markdown with `{{variable}}` template placeholders

**Skill Lock (skills-lock.json):**
- Purpose: Tracks installed skill versions and sources
- Examples: Root `skills-lock.json`
- Pattern: JSON with skill name → {source, ref, sourceType, computedHash}

## Entry Points

**Primary Entry Point - saddle-cli:**
- Location: Installed via `bunx saddle-cli`
- Triggers: `bunx saddle-cli` at project root
- Responsibilities: Install skills from this repository to target projects

**Skill Validation:**
- Location: `skills/skill-tools/skill-creator/scripts/quick_validate.py`
- Triggers: `uv run skills/skill-tools/skill-creator/scripts/quick_validate.py`
- Responsibilities: Validate skill structure compliance

**Task Runner - mise:**
- Location: `.config/mise/config.toml`
- Triggers: `mise run <task>`
- Responsibilities: Format code, sync environment, manage tools

## Error Handling

**Strategy:** Validation-first with clear error messages

**Patterns:**
- `quick_validate.py` checks skill structure before submission
- `init_skill.py` scaffolds correct structure to prevent errors
- `package_skill.py` bundles skills for distribution

## Cross-Cutting Concerns

**Formatting:** Managed via `mise run format` — runs undersort, ruff, mdformat
**Dependencies:** Python deps via `uv` (pyproject.toml), JS deps via `bun`/`npm`
**Version Control:** Git with .gitignore for uv.lock and __pycache__
**Installation:** saddle-cli for skill distribution to target projects

---

*Architecture analysis: 2026-04-02*
