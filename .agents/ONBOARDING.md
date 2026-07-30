# AGENTS.md — ONBOARDING

Read this when starting a new session. After first read, only revisit when
project structure or tooling changes significantly.

## Project

Curated prompt/skill/instruction collection for AI coding assistants, plus
Python helper scripts for skill development. Full catalog at `README.md`.

## Quick start

```bash
# install toolchain and repo dependencies
mise up

# run Python helper scripts (ALWAYS through uv)
uv run ./skills/skill-creator/scripts/<script>.py

# lint Python code
ruff check <paths> --fix

# lint Markdown files (no writes)
mise run lint-md

# format Markdown files
mise run format-md

# run tests
uv run pytest <paths> -v --tb=short

# validate a skill against the Agent Skills spec
uvx skills-ref validate <path-to-skill>
```

## Entry points (read these first)

| File | Why |
|------|-----|
| `AGENTS.md` | Root rail — rules + `.agents/` index |
| `.agents/POLICIES.md` | Boundaries, priorities, verification |
| `.agents/FILES.md` | Source-of-truth locations |
| `skills/AGENTS.md` | Skill authoring contract |

## Where to dig deeper

- `README.md` — project overview and skill catalog
- `agents-md/AGENTS-MD-GUIDELINES.md` — guidance for writing AGENTS.md files
- `instructions/commit-instructions.md` — commit message format
- `.agents/HISTORY.md` — past decisions and rationale
- Subtree `AGENTS.md` files — local contracts for each area

## Available tools

No project-specific code-search or issue-tracking tools (codegraph, grepai,
repowise, beads) are installed in this workspace. Use standard `rg` / `find`
for navigation.
