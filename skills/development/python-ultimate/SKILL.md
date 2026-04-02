---
name: python-ultimate
description: >
  Comprehensive Python development skill covering coding standards, CLI development,
  linting, testing, debugging, refactoring, code review, auditing, documentation,
  and project planning. Use when writing, reviewing, refactoring, debugging, or
  documenting Python code; configuring linters; setting up CLI tools; planning
  features; or performing code audits. Consolidates 17 specialized Python skills
  into one reference.
---

# Python Ultimate

Complete Python development reference. Covers standards, tooling, workflows, and best practices.

## Quick Start

**Writing code?** → Start with [Coding Standards](#coding-standards)
**Building a CLI?** → Go to [CLI Development](#cli-development)
**Fixing linter errors?** → Go to [Linter Rules](#linter-rules)
**Writing tests?** → Go to [Testing](#testing)
**Debugging a bug?** → Go to [Debugging](#debugging)
**Refactoring?** → Go to [Refactoring](#refactoring)
**Reviewing code?** → Go to [Code Review](#code-review)
**Auditing codebase?** → Go to [Auditing](#auditing)
**Documenting?** → Go to [Documentation](#documentation)
**Planning a feature?** → Go to [Planning](#planning)

---

## Coding Standards

Core Python coding rules. See [references/coding-standards.md](references/coding-standards.md) for full details.

### Type Hints

Mandatory everywhere. Use pipe syntax (`T | None`), never `Optional[T]`. Python 3.10+ required.

```python
def process(data: str, limit: int | None = None) -> list[str]: ...
```

**Never use `TYPE_CHECKING` guards.** See [references/type-checking.md](references/type-checking.md) for alternatives.

### String Formatting

Use f-strings only. No `.format()` or `%` formatting.

### Code Size Limits

| Target | Limit |
|--------|-------|
| Module | < 250 lines |
| Function | < 75 lines |
| Class | < 200 lines |

### Docstrings

Google style. Required for public functions and classes.

### Prohibited Patterns

- `TYPE_CHECKING` guards
- `os.path` (use `pathlib.Path`)
- `Optional[T]` (use `T | None`)
- `# noqa` comments
- `sys.path` manipulation

---

## CLI Development

Building Python CLIs with Typer or Click. See [references/cli-development.md](references/cli-development.md).

### Framework Selection

Use **Typer** for new projects (type-hint driven, less boilerplate). Use **Click** for complex parameter handling.

### Key Patterns

- Parameter validation with type hints
- Rich output formatting
- Environment variable integration
- Exit codes for error states

---

## Linter Rules

Context-aware fixes for Ruff linter rules. See [references/linter-rules.md](references/linter-rules.md).

### Covered Rules

| Rule | Description | Quick Fix |
|------|-------------|-----------|
| E402 | Module-level import not at top | Move imports to top |
| B007 | Unused loop variable | Prefix with `_` |
| B008 | Function call in default arg | Use `None` sentinel |
| S108 | Hardcoded temp file path | Use `tempfile` |
| PLC0415 | Import not at top-level | Move to module level |
| NPY002 | Legacy numpy random | Use `numpy.random` |
| S311 | Standard random | Use `secrets` for security |

### Typer Exception

B008 is allowed for Typer `Annotated` parameters. See [references/linter-rules.md](references/linter-rules.md#typer-cli-exception-for-b008).

---

## Testing

Test organization, fixtures, mocking, and TDD. See [references/testing.md](references/testing.md).

### Quick Commands

```bash
uv run pytest -v --tb=short
uv run pytest --cov=src --cov-report=term-missing
```

### Key Practices

- Co-located tests: `<module>_test.py` alongside implementation
- 90%+ coverage target
- Fixtures in `conftest.py`
- Parameterized testing for multiple inputs
- `unittest.mock` for external dependencies

### TDD Cycle

Red → Green → Refactor. No production code without a failing test first. See [references/testing.md](references/testing.md#test-driven-development).

---

## Debugging

Systematic 4-phase debugging process. See [references/debugging.md](references/debugging.md).

### Iron Law

**No fixes without root cause investigation first.**

### 4-Phase Process

1. **Root Cause** — Reproduce, isolate, trace data flow
2. **Pattern Analysis** — Identify state changes, timing issues
3. **Hypothesis** — Form testable prediction
4. **Implementation** — Minimal fix, verify with test

### Red Flags

- "Let me just try changing X"
- Fixing symptoms without understanding cause
- Multiple failed fix attempts

---

## Refactoring

Find → Replace → Verify workflow. See [references/refactoring.md](references/refactoring.md).

### Workflow

1. **Find** — Grep for target pattern
2. **Replace** — Edit with `replace_all` for bulk changes
3. **Verify** — Run tests, check for regressions

### Code Transfer

Line-based code movement between files. See [references/refactoring.md](references/refactoring.md#code-transfer).

---

## Code Review

Receiving and evaluating code review feedback. See [references/code-review.md](references/code-review.md).

### Workflow

Read → Understand → Verify → Evaluate → Respond → Implement

### Key Principles

- No performative agreement
- Push back with technical reasoning
- Verify feedback before implementing
- Evaluate: is the suggestion correct?

---

## Auditing

6-dimension codebase analysis. See [references/auditing.md](references/auditing.md).

### Dimensions

1. **Architecture** — Structure, modularity, dependencies
2. **Quality** — Readability, complexity, duplication
3. **Security** — Input validation, secrets, injection
4. **Performance** — Bottlenecks, memory, I/O
5. **Testing** — Coverage, quality, edge cases
6. **Maintainability** — Documentation, technical debt

### Severity Ratings

Critical → High → Medium → Low

---

## Documentation

10-section documentation structure. See [references/documentation.md](references/documentation.md).

### Workflow

Explore → Map → Read → Synthesize

### Sections

Project Overview, Architecture, Key Components, Data Flow, API Reference, Configuration, Setup Guide, Development Guide, Testing, Deployment

### Mermaid Diagrams

Use for architecture, sequence, and flowchart visualizations.

---

## Planning

PLAN.md living document for feature implementation. See [references/planning.md](references/planning.md).

### When to Use

Features spanning 3-15 prompts. Self-contained for fresh sessions.

### Structure

Goal → Context → Phases → Validation → Progress → Decisions → Notes

---

## Project Setup

Project structure, dependencies, and imports. See [references/project-setup.md](references/project-setup.md).

### Key Tools

- **uv** for dependency management
- **src layout** for packages
- **pyproject.toml** for configuration

### Import Order

1. Standard library
2. Third-party
3. Local (absolute imports)

---

## File Analysis

Non-destructive file and codebase analysis. See [references/file-analysis.md](references/file-analysis.md).

### Tools

- `stat` for metadata
- `wc` for line counts
- Grep for pattern searching
- Glob for file discovery

---

## Type Checking Alternatives

Never use `TYPE_CHECKING` guards. See [references/type-checking.md](references/type-checking.md).

### Alternatives

1. Extract shared types to dedicated modules
2. Use protocols for structural typing
3. Forward references (string literals)
4. Local imports (last resort)

---

## Reference Files

All detailed content lives in `references/`. Load only what you need:

| File | Content |
|------|---------|
| `coding-standards.md` | Type hints, formatting, size limits, docstrings, comments |
| `cli-development.md` | Typer/Click, parameters, Rich output, env vars |
| `linter-rules.md` | Ruff rules E402, B007, B008, S108, PLC0415, NPY002, S311 |
| `testing.md` | Fixtures, parameterized, mocking, TDD, coverage |
| `type-checking.md` | TYPE_CHECKING alternatives, protocols, forward refs |
| `debugging.md` | 4-phase process, red flags, rationalizations |
| `refactoring.md` | Bulk operations, code transfer, safety checks |
| `code-review.md` | Receiving feedback, push back, evaluation |
| `auditing.md` | 6-dimension analysis, severity ratings |
| `documentation.md` | 10-section structure, Mermaid diagrams |
| `planning.md` | PLAN.md template and example |
| `file-analysis.md` | Metadata, line counting, pattern searching |
| `project-setup.md` | Project structure, uv, imports |
