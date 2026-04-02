# Codebase Structure

**Analysis Date:** 2026-04-02

## Directory Layout

```
prompts/
├── .agents/                    # Installed/enabled skills for this workspace
│   └── skills/                 # Local skill copies (tracked in skills-lock.json)
│       ├── coding-principles/  # SKILL.md + support files
│       ├── python-cli/
│       ├── python-linter/
│       ├── python-no-type-checking-guard/
│       ├── python-standards/
│       └── testing-strategy/
├── .config/                    # Tool configuration
│   └── mise/
│       └── config.toml         # mise tool versions and task definitions
├── .planning/                  # Planning/analysis artifacts
│   └── codebase/               # Codebase analysis documents
├── agents-md/                  # AGENTS.md templates and guidelines
│   ├── AGENTS.md               # Template with {{variable}} placeholders
│   └── AGENTS-MD-GUIDELINES.md # Guidelines for writing AGENTS.md
├── commands/                   # Slash-command definitions for coding assistants
│   ├── commit-groups.md
│   ├── create-plan-md.md
│   ├── create-skill-from-url.md
│   ├── onboarding-new-agent-session.md
│   ├── py-lint.md
│   └── py-run-tests.md
├── instructions/               # Persistent instruction files
│   └── commit-instructions.md
├── skills/                     # Canonical skill definitions (organized by domain)
│   ├── AGENTS.md               # Skill creation/update guidelines
│   ├── database/               # Database-related skills
│   │   ├── database-schema/
│   │   └── sqlmodel/
│   ├── development/            # Development workflow skills
│   │   ├── code-auditor/
│   │   ├── code-execution/
│   │   ├── code-refactor/
│   │   ├── code-transfer/
│   │   ├── codebase-documenter/
│   │   ├── dispatching-parallel-agents/
│   │   ├── file-operations/
│   │   ├── plan-md/
│   │   ├── receiving-code-review/
│   │   ├── requesting-code-review/
│   │   ├── subagent-driven-development/
│   │   ├── systematic-debugging/
│   │   ├── test-driven-development/
│   │   ├── using-git-worktrees/
│   │   └── verification-before-completion/
│   ├── documentation/          # Documentation skills
│   │   └── documentation_standards/
│   ├── documents/              # Office document skills
│   │   ├── docx/
│   │   ├── pdf/
│   │   ├── pptx/
│   │   └── xlsx/
│   ├── mcp-servers/            # MCP server integration skills
│   │   ├── mcp-cytosnpy/
│   │   ├── mcp-desktop-commander/
│   │   ├── mcp-grepai/
│   │   ├── mcp-sequential-thinking/
│   │   └── mcp-vstash/
│   ├── misc/                   # Miscellaneous skills
│   │   └── prompt-engineering/
│   ├── python/                 # Python development skills
│   │   ├── coding-principles/
│   │   ├── python-cli/
│   │   ├── python-guidelines/
│   │   ├── python-linter/
│   │   ├── python-no-type-checking-guard/
│   │   ├── python-standards/
│   │   └── testing-strategy/
│   ├── skill-tools/            # Skill management tools
│   │   └── skill-creator/      # Scaffolding, validation, packaging
│   ├── standards/              # Standards body skills
│   │   ├── 3gpp-basics/
│   │   ├── 3gpp-change-request/
│   │   ├── 3gpp-meetings/
│   │   ├── 3gpp-portal-authentication/
│   │   ├── 3gpp-releases/
│   │   ├── 3gpp-specifications/
│   │   ├── 3gpp-tdocs/
│   │   ├── 3gpp-working-groups/
│   │   └── etsi-spec/
│   └── tools/                  # CLI tool skills
│       ├── cli-cytosnpy/
│       ├── cli-vstash/
│       ├── ripgrep/
│       ├── rtk/
│       └── tea/
├── pyproject.toml              # Python project config (for dev tooling)
├── skills-lock.json            # Tracks installed skill versions/hashes
├── uv.lock                     # Python dependency lockfile
├── LICENSE
└── README.md
```

## Directory Purposes

**`skills/`:**

- Purpose: Canonical source of all skill definitions, organized by domain
- Contains: SKILL.md files with YAML frontmatter + Markdown instructions, optional scripts/, references/, assets/, LICENSE.txt
- Key structure: `skills/<domain>/<skill-name>/SKILL.md`
- Each skill is self-contained and modular

**`.agents/skills/`:**

- Purpose: Workspace-local copies of installed/enabled skills
- Contains: Mirrored skill directories from `skills/`
- Key files: `skills-lock.json` at root tracks versions
- Generated: Yes (copied from `skills/`)
- Committed: Yes (contents tracked)

**`commands/`:**

- Purpose: Slash-command definitions for coding assistants
- Contains: Markdown files with workflow definitions
- Key files: `create-skill-from-url.md`, `py-lint.md`, `py-run-tests.md`

**`instructions/`:**

- Purpose: Persistent instruction files loaded by coding assistants
- Contains: Markdown instruction files
- Key files: `commit-instructions.md`

**`agents-md/`:**

- Purpose: AGENTS.md templates and writing guidelines
- Contains: Template AGENTS.md with `{{variable}}` placeholders, guidelines doc
- Key files: `AGENTS.md` (template), `AGENTS-MD-GUIDELINES.md`

**`.config/`:**

- Purpose: Development tool configuration
- Contains: mise config with tool versions and task definitions
- Key files: `mise/config.toml`

**`.planning/`:**

- Purpose: Planning and analysis artifacts
- Contains: Codebase analysis documents
- Committed: Depends on workflow

## Key File Locations

**Entry Points:**

- `pyproject.toml`: Python project definition (requires-python >=3.14, dependencies for dev tooling)
- `.config/mise/config.toml`: Tool versions (bun, npm, ripgrep, tree-cli) and tasks (format, env-sync)
- `skills-lock.json`: Skill version tracking for installed skills

**Configuration:**

- `pyproject.toml`: Python deps — mdformat, pyyaml, ruff, undersort
- `.config/mise/config.toml`: mise tools and tasks
- `skills-lock.json`: Installed skill hashes and sources

**Core Logic:**

- `skills/skill-tools/skill-creator/SKILL.md`: Skill anatomy and creation guide (379 lines, comprehensive)
- `skills/skill-tools/skill-creator/scripts/`: Scaffolding, validation, packaging scripts
- `skills/AGENTS.md`: Skill creation/update guidelines

**Documentation:**

- `README.md`: Project overview, install instructions, references
- `agents-md/AGENTS-MD-GUIDELINES.md`: How to write effective AGENTS.md files

## Naming Conventions

**Files:**

- Skill definition: `SKILL.md` (always uppercase, always in skill root)
- Support docs: `lowercase-with-hyphens.md` (e.g., `forms.md`, `reference.md`)
- Scripts: `snake_case.py` (e.g., `init_skill.py`, `quick_validate.py`)
- Commands: `lowercase-with-hyphens.md` (e.g., `create-skill-from-url.md`)

**Directories:**

- Skill directories: `lowercase-with-hyphens/` (e.g., `coding-principles/`, `code-execution/`)
- Domain directories: `lowercase/` (e.g., `python/`, `development/`, `documents/`)
- MCP skills: `mcp-<name>/` prefix (e.g., `mcp-cytosnpy/`, `mcp-vstash/`)
- Config dirs: `.lowercase/` (e.g., `.agents/`, `.config/`, `.planning/`)

## Where to Add New Code

**New Skill:**

- Primary location: `skills/<domain>/<skill-name>/SKILL.md`
- Use `skills/skill-tools/skill-creator/scripts/init_skill.py` for scaffolding
- Follow the skill anatomy: SKILL.md (frontmatter + body) + optional scripts/, references/, assets/
- Add to `.agents/skills/` if it should be enabled for this workspace

**New Command:**

- Location: `commands/<command-name>.md`
- Pattern: Markdown file with name, description, workflow steps

**New Instruction:**

- Location: `instructions/<topic>.md`
- Pattern: Markdown file with persistent instructions

**New Skill Domain:**

- Location: `skills/<new-domain>/`
- Create domain directory, then add skill subdirectories within it

**Skill Scripts:**

- Location: `skills/<domain>/<skill-name>/scripts/<script_name>.py`
- Use inline script metadata for dependencies (PEP 723)
- Run via `uv run` (never directly with system Python)

## Special Directories

**`.agents/`:**

- Purpose: Workspace-installed skills
- Generated: Partially (copied from `skills/`, but content may be customized)
- Committed: Yes

**`.planning/`:**

- Purpose: Planning artifacts (codebase analysis, etc.)
- Generated: Yes
- Committed: Depends on workflow

**`.config/`:**

- Purpose: Tool configuration
- Generated: No (manually maintained)
- Committed: Yes

**`skills/skill-tools/skill-creator/references/`:**

- Purpose: Reference documentation for skill creation
- Generated: No
- Committed: Yes

______________________________________________________________________

*Structure analysis: 2026-04-02*
