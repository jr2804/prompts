---
name: python-ultimate
description: >-
  Comprehensive Python development skill covering coding standards, CLI development,
  linting, testing, debugging, refactoring, code review, auditing, documentation,
  project planning, and bulk operations. Use when writing, reviewing, refactoring,
  debugging, or documenting Python code; configuring linters; setting up CLI tools;
  planning features; performing code audits; or handling bulk operations (10+ files)
  that need 90%+ token savings.
license: MIT
---

# Python Ultimate

Complete Python development reference. Covers standards, tooling, workflows, and best practices.

## Quick Start

**Writing code?** → Start with [Coding Standards](references/coding-standards.md)
**Checking naming?** → Go to [Naming Conventions](references/naming-conventions.md)
**Building a CLI?** → Go to [CLI Development](references/cli-development.md)
**Fixing linter errors?** → Go to [Linter Rules](references/linter-rules.md)
**Writing tests?** → Go to [Testing](references/testing.md)
**Debugging a bug?** → Go to [Debugging](references/debugging.md)
**Refactoring?** → Go to [Refactoring](references/refactoring.md)
**Reviewing code?** → Go to [Code Review](references/code-review.md)
**Auditing codebase?** → Go to [Auditing](references/auditing.md)
**Documenting?** → Go to [Documentation](references/documentation.md)
**Planning a feature?** → Go to [Planning](references/planning.md)
**Bulk operations?** → Go to [Bulk Operations](#bulk-operations) (10+ files, 90%+ token savings)

______________________________________________________________________

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
- Defensive `try/except ImportError` for required dependencies (see [references/imports-optional-dependencies.md](references/imports-optional-dependencies.md))
- Vague or wide parameter/return types with hidden `isinstance`/`hasattr` checks and `None`-as-error returns (see [references/coding-standards.md](#vague-inputoutput-types))

______________________________________________________________________

## Naming Conventions

Variable naming standards for clarity and consistency. See [references/naming-conventions.md](references/naming-conventions.md) for full details.

### Files and Directories

| Pattern | Suffix | Example |
|---------|--------|---------|
| Files | `_file` | `output_file`, `config_file` |
| Directories | `_dir` | `cache_dir`, `output_dir` |
| Unknown type | `_path` | `data_path` (exceptional only) |

**Anti-patterns (always invalid for path variables):**

- Bare generic names: `path`, `file`, `folder`, `dir`, `directory`, `output`, `input`, `source`, `target`, `dest`
- Prefix instead of suffix: `dir_output`, `file_config`
- Missing suffix: `results`, `data`, `config` (ambiguous)

See [references/naming-conventions.md](references/naming-conventions.md#13-anti-patterns) for the complete anti-pattern list.

### Test Naming

- Files: `test_<module>.py`
- Classes: `Test<DataProcessor>` (PascalCase with Test prefix)
- Methods: `test_<description>` (snake_case with test\_ prefix)

### Automated Validation

```bash
# Check a variable name
uv run assets/check_path_naming.py output_file
# Output: is_file

# Scan for violations
uv run assets/check_path_naming.py --check-files src/
```

______________________________________________________________________

## CLI Development

Building Python CLIs with Typer or Click. See [references/cli-development.md](references/cli-development.md).

### Framework Selection

Use **Typer** for new projects (type-hint driven, less boilerplate). Use **Click** for complex parameter handling.

### Key Patterns

- Parameter validation with type hints
- Rich output formatting
- Environment variable integration
- Exit codes for error states

______________________________________________________________________

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

______________________________________________________________________

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

______________________________________________________________________

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

______________________________________________________________________

## Refactoring

Find → Replace → Verify workflow. See [references/refactoring.md](references/refactoring.md).

### Workflow

1. **Find** — Grep for target pattern
2. **Replace** — Edit with `replace_all` for bulk changes
3. **Verify** — Run tests, check for regressions

### Code Transfer

Line-based code movement between files. See [references/refactoring.md](references/refactoring.md#code-transfer).

______________________________________________________________________

## Code Review

Receiving and evaluating code review feedback. See [references/code-review.md](references/code-review.md).

### Workflow

Read → Understand → Verify → Evaluate → Respond → Implement

### Key Principles

- No performative agreement
- Push back with technical reasoning
- Verify feedback before implementing
- Evaluate: is the suggestion correct?

______________________________________________________________________

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

______________________________________________________________________

## Documentation

10-section documentation structure. See [references/documentation.md](references/documentation.md).

### Workflow

Explore → Map → Read → Synthesize

### Sections

Project Overview, Architecture, Key Components, Data Flow, API Reference, Configuration, Setup Guide, Development Guide, Testing, Deployment

### Mermaid Diagrams

Use for architecture, sequence, and flowchart visualizations.

______________________________________________________________________

## Planning

PLAN.md living document for feature implementation. See [references/planning.md](references/planning.md).

### When to Use

Features spanning 3-15 prompts. Self-contained for fresh sessions.

### Structure

Goal → Context → Phases → Validation → Progress → Decisions → Notes

______________________________________________________________________

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

______________________________________________________________________

## File Analysis

Non-destructive file and codebase analysis. See [references/file-analysis.md](references/file-analysis.md).

### Tools

- `stat` for metadata
- `wc` for line counts
- Grep for pattern searching
- Glob for file discovery

______________________________________________________________________

## Type Checking Alternatives

Never use `TYPE_CHECKING` guards. See [references/type-checking.md](references/type-checking.md).

### Alternatives

1. Extract shared types to dedicated modules
2. Use protocols for structural typing
3. Forward references (string literals)
4. Local imports (last resort)

______________________________________________________________________

## Bulk Operations

High-efficiency Python execution for 10+ file operations. **90-99% token savings** vs. iterative approaches.

**When to use:**
- Bulk operations (10+ files)
- Complex multi-step workflows
- Iterative processing across many files
- User mentions efficiency/performance

**Workflow pattern:**
1. **Analyze locally** — Use metadata operations (file counts, grep patterns)
2. **Process locally** — Execute all transformations in Python
3. **Return summary** — Report counts, not full data

**Example patterns:**

```python
# Bulk refactor across 50 files
from pathlib import Path
import re

files = list(Path('.').glob('**/*.py'))
modified = 0

for f in files:
    content = f.read_text()
    new_content = re.sub(r'old_pattern', 'new_pattern', content)
    if new_content != content:
        f.write_text(new_content)
        modified += 1

result = {'files_scanned': len(files), 'files_modified': modified}
```

```python
# Code audit metadata extraction
from pathlib import Path
import ast

files = list(Path('src').glob('**/*.py'))
complexity_issues = []

for f in files:
    tree = ast.parse(f.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Calculate simple complexity metric
            nested = sum(1 for n in ast.walk(node) if isinstance(n, (ast.If, ast.For, ast.While)))
            if nested > 10:
                complexity_issues.append({'file': str(f), 'function': node.name, 'complexity': nested})

result = {'files_audited': len(files), 'high_complexity': len(complexity_issues)}
```

**Best practices:**
- ✅ Return summaries, not full data
- ✅ Batch operations where possible
- ✅ Use `pathlib.Path` for file operations
- ✅ Handle errors gracefully, return error counts
- ❌ Don't read full source into context when metadata suffices
- ❌ Don't process files one-by-one interactively

**Token savings scale with file count:**

| Files | Interactive | Bulk Operation | Savings |
|-------|-------------|----------------|---------|
| 10    | ~5K tokens  | ~500 tokens    | 90%     |
| 50    | ~25K tokens | ~600 tokens    | 97.6%   |
| 100   | ~150K tokens| ~1K tokens     | 99.3%   |

______________________________________________________________________

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
| `verification.md` | Pre-commit hooks, tox, Makefile targets |
| `imports-optional-dependencies.md` | Required vs optional dependency import patterns |
