---
name: python-ultimate
description: >-
  Comprehensive Python development skill covering coding standards, CLI development,
  linting, testing, debugging, refactoring, code review, auditing, documentation,
  project planning, uv project management, and standalone scripts. Use when writing,
  reviewing, refactoring, debugging, or documenting Python code; configuring linters;
  managing uv projects or standalone scripts; setting up CLI tools; planning features;
  performing code audits; checking Python antipatterns, forbidden methods, or bad
  style; or handling bulk operations (10+ files) that benefit from batch workflows.
license: MIT
---

# Python Ultimate

A modular Python guide. This entrypoint routes tasks to concise reference files; load only the guidance needed for the current task.

## Quick Start

- **Writing code:** [Coding Standards](references/coding-standards.md)
- **Checking names:** [Naming Conventions](references/naming-conventions.md)
- **Designing domain types:** [Domain Types, Enums, and Structured Data](references/type-design.md)
- **Handling module state, globals, or constant tables:** [Module State and Globals](references/module-state.md)
- **Building a CLI:** [CLI Development](references/cli-development.md)
- **Fixing linter errors:** [Linter Rules](references/linter-rules.md)
- **Writing tests:** [Testing](references/testing.md)
- **Debugging:** [Debugging](references/debugging.md)
- **Refactoring or bulk operations:** [Refactoring](references/refactoring.md)
- **Reviewing code:** [Code Review](references/code-review.md)
- **Auditing a codebase:** [Auditing](references/auditing.md)
- **Documenting:** [Documentation](references/documentation.md)
- **Planning:** [Planning](references/planning.md)
- **Running Python:** [uv Execution](references/uv.md)
- **Writing standalone scripts:** [uv Scripts](references/uv-scripts.md)
- **Managing a project:** [uv Projects](references/uv-projects.md)

## Routing and Commands

An optional topic/sub-command selects a focused review. If none is provided, perform a general antipattern check using the index below. For `help` or an unknown topic, show the command table. For a targeted topic, read and follow its linked reference; detailed procedures and examples live there rather than being duplicated here.

| Topic | What it covers | Canonical reference |
| --- | --- | --- |
| `naming` | File and directory variable naming; forbidden-scan fixtures | [naming-conventions.md](references/naming-conventions.md) |
| `type-checking` | `TYPE_CHECKING`, shared types, import cycles | [type-checking.md](references/type-checking.md) |
| `type-design` | `StrEnum`, `Literal`, repeated strings, structured data | [type-design.md](references/type-design.md) |
| `module-state` | Globals, `global`, cached getters, module constant tables | [module-state.md](references/module-state.md) |
| `imports` | Required and optional dependency imports | [imports-optional-dependencies.md](references/imports-optional-dependencies.md) |
| `coding-standards` | Types, formatting, paths, docstrings, data modeling | [coding-standards.md](references/coding-standards.md) |
| `linter-rules` | Context-aware Ruff fixes | [linter-rules.md](references/linter-rules.md) |
| `debugging` | Root-cause-first, four-phase debugging | [debugging.md](references/debugging.md) |
| `testing` | Tests, fixtures, mocks, TDD, coverage | [testing.md](references/testing.md) |
| `audit` | Six-dimension codebase audit | [auditing.md](references/auditing.md) |
| `verification` | Evidence-based completion claims | [verification.md](references/verification.md) |
| `code-review` | Evaluating and responding to review feedback | [code-review.md](references/code-review.md) |
| `documentation` | Documentation workflow, structure, and diagrams | [documentation.md](references/documentation.md) |
| `file-analysis` | Non-destructive file and codebase analysis | [file-analysis.md](references/file-analysis.md) |
| `planning` | Feature planning and plan structure | [planning.md](references/planning.md) |
| `project-setup` | Project structure, dependencies, and imports | [project-setup.md](references/project-setup.md) |
| `cli` | Command-line framework and application patterns | [cli-development.md](references/cli-development.md) |
| `python-versions` | Python-version selection and compatibility | [uv-python-versions.md](references/uv-python-versions.md) |
| `uv` | Python execution through `uv run` | [uv.md](references/uv.md) |
| `uv-scripts` | PEP 723 standalone scripts | [uv-scripts.md](references/uv-scripts.md) |
| `uv-projects` | Project setup, dependencies, and locking | [uv-projects.md](references/uv-projects.md) |

### Response Format

For focused reviews, report:

1. **Summary** — finding counts by severity and category
2. **Findings** — `file:line`, pattern class, and rationale
3. **Fix guidance** — preferred replacement, with a concise example when useful
4. **References** — direct links to relevant guidance
5. **Verification** — commands run and observed results

Use concise, technical language; avoid speculative claims.

## Antipatterns / Forbidden Styles Index

Use this as the default broad-review checklist. Detailed rationale and examples live in the linked references.

| Category | Forbidden pattern | Preferred pattern | Guidance |
| --- | --- | --- | --- |
| Type checking | `TYPE_CHECKING` import guards | Refactor module boundaries, use forward refs/protocols | [Type checking](references/type-checking.md) |
| Type hints | `Optional[T]` | `T \| None` | [Coding standards](references/coding-standards.md) |
| Domain values | Reusable `Literal["..."]` sets or duplicated domain strings | One `StrEnum` in its owning/shared module | [Type design](references/type-design.md) |
| Data modeling | `dict[str, Any]` / `dict[str, object]` used as records | Internal dataclass; validated wire model; precise map types | [Type design](references/type-design.md) |
| Module state | Module-level variables mutated at runtime; the `global` statement (PLW0603) | Pass state explicitly; `@functools.cache` getter for read-only values | [Module state](references/module-state.md) |
| Module state | Long or mutable module-level constant tables (`dict`/`list` of `str`) | Dedicated data module, `MappingProxyType`, enum keys + frozen records | [Module state](references/module-state.md) |
| String formatting | `.format()` or `%` formatting | f-strings | [Coding standards](references/coding-standards.md) |
| Paths | `os.path` usage | `pathlib.Path` | [Coding standards](references/coding-standards.md) |
| Imports | `sys.path` manipulation to make project modules importable | Fix package layout or installation | [Project setup](references/project-setup.md) |
| Lint suppression | `# noqa` used to hide issues | Fix the root cause | [Coding standards](references/coding-standards.md) |
| Imports | Defensive `try/except ImportError` for required dependencies | Normal top-level imports | [Optional dependencies](references/imports-optional-dependencies.md) |
| Path naming | Bare path names or prefix forms (`dir_x`, `file_x`) | `_dir` / `_file` suffixes | [Naming](references/naming-conventions.md) |
| Comments | Comments restating obvious code | Explain intent, constraints, or non-obvious choices | [Coding standards](references/coding-standards.md) |
| Debugging | Guess-and-check fixes before root-cause analysis | Follow the documented four-phase process | [Debugging](references/debugging.md) |
| Code review | Performative agreement without verification | Evaluate feedback and respond with evidence | [Code review](references/code-review.md) |
| Data modeling | Pydantic for lightweight internal structs; dataclass at trust boundaries | Dataclass internally; runtime validation at boundaries | [Coding standards](references/coding-standards.md) |
| Python execution | Bare `python` / `python3` outside documented exceptions | `uv run ...` | [uv](references/uv.md) |
| Script metadata | Hand-written/edited PEP 723 blocks | Manage metadata with `uv init/add/remove --script` | [uv scripts](references/uv-scripts.md) |
| Project dependencies | `pip install` in a `uv`-managed project | `uv add` | [uv projects](references/uv-projects.md) |
| Lockfiles | `uv sync` without `--locked` when reproducibility matters | `uv sync --locked` or trusted `--frozen` | [uv projects](references/uv-projects.md) |
| VCS hygiene | Commit `.venv/` or omit `uv.lock` | Ignore `.venv/`; commit `uv.lock` | [uv projects](references/uv-projects.md) |
| Python architectures | Assume `uv python install` supplies 32-bit Python | Use `uv run --python <system-interpreter-path>` | [Python versions](references/uv-python-versions.md) |
| Type annotations | Unjustified `Any` or `object` | Precise unions, generics, protocols, or narrowest type | [Coding standards](references/coding-standards.md) |
| Defaults | `None` for mutable collections or as a silent error signal | `field(default_factory=...)`; raise/return explicit result | [Coding standards](references/coding-standards.md) |

## Core Defaults

- Python 3.10+; annotate function parameters and return values.
- Use `uv run` for Python commands; follow `references/uv.md` for documented bootstrap or activated-environment exceptions.
- Avoid `TYPE_CHECKING` guards; fix dependency direction or use the documented alternatives.
- Prefer explicit domain types and precise data models; see the type-design and coding standards references.
- Never use the `global` statement or runtime-mutated module variables; model read-only process-wide values as a `@functools.cache` getter (see module state).
- Consult the task-specific reference for full procedures, examples, compatibility notes, and exceptions.

## Reference Map

| Reference | Use it for |
| --- | --- |
| [auditing.md](references/auditing.md) | Audit dimensions, severity, report format |
| [cli-development.md](references/cli-development.md) | Typer/Click, parameters, output, environment variables |
| [code-review.md](references/code-review.md) | Review-feedback workflow and technical responses |
| [coding-standards.md](references/coding-standards.md) | Type hints, formatting, paths, docstrings, data modeling |
| [debugging.md](references/debugging.md) | Root-cause investigation and debugging workflow |
| [documentation.md](references/documentation.md) | Documentation workflow, structure, diagrams |
| [file-analysis.md](references/file-analysis.md) | Non-destructive file and codebase analysis |
| [imports-optional-dependencies.md](references/imports-optional-dependencies.md) | Required vs. optional imports |
| [linter-rules.md](references/linter-rules.md) | Ruff rules and context-aware fixes |
| [module-state.md](references/module-state.md) | Globals, `global`/PLW0603, cached getters, constant tables |
| [naming-conventions.md](references/naming-conventions.md) | File, directory, variable, and fixed-vocabulary naming |
| [planning.md](references/planning.md) | Feature planning and plan structure |
| [project-setup.md](references/project-setup.md) | Project structure, dependencies, and imports |
| [refactoring.md](references/refactoring.md) | Safe refactoring, code transfer, bulk operations |
| [testing.md](references/testing.md) | Fixtures, parameterization, mocking, TDD, coverage |
| [type-checking.md](references/type-checking.md) | Type-only imports, shared types, circular dependencies |
| [type-design.md](references/type-design.md) | Enums, domain strings, records, precise mappings |
| [uv.md](references/uv.md) | Execution through `uv run` and sandboxing |
| [uv-projects.md](references/uv-projects.md) | Project workflow, locking, dependency groups, workspaces |
| [uv-python-versions.md](references/uv-python-versions.md) | Version selection and non-default architectures |
| [uv-scripts.md](references/uv-scripts.md) | PEP 723 metadata and standalone scripts |
| [verification.md](references/verification.md) | Evidence-based verification and completion claims |
