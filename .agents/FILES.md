# AGENTS.md — FILES

Single source of truth for paths, config keys, and naming conventions.
Kept compact — agents hallucinate less when they know where definitions live.

## Pattern

- One file owns each class of definition (paths, config defaults, enums).
- Import from that file. Never hard-code values in other modules.
- Variables that address files get `_file` suffix; directories get `_dir`.

## Project-specific sources of truth

| What | Where | Key names / Notes |
|------|-------|-------------------|
| Project overview & skill catalog | `README.md` | Content tables, MCP/CLI tool list |
| Runtime metadata | `pyproject.toml` | `name`, `requires-python`, `dependencies` |
| Skill authoring contract | `skills/AGENTS.md` | Spec compliance, script metadata, agent-neutrality |
| AGENTS.md writing guidance | `agents-md/AGENTS-MD-GUIDELINES.md` | Authoring rules, section order |
| AGENTS.md template | `agents-md/AGENTS.md` | `{{project-name}}` / `{{project-description}}` template |
| Commit message format | `instructions/commit-instructions.md` | gitmoji + conventional-commit subject, body rules |
| Toolchain (tools + tasks) | `.config/mise/config.toml` | `[tools]`, `format-md`, `lint-md`, `format` tasks |
| Markdown lint/format config | `.config/rumdl.toml` | `line-length`, `flavor`, `exclude`, `per-file-ignores` |
| Skill spec (external) | <https://agentskills.io/specification> | Canonical Agent Skills Specification |

## Notes

- This repo has no central `paths.py` / `config.py` / `enums.py` — it is a
  content collection, not an application. Do not fabricate source files.
- Python helper scripts live inline under individual skills
  (e.g. `skills/skill-creator/scripts/`); each declares its own dependencies
  via inline script metadata.
