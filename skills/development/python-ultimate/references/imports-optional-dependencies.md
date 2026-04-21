# Imports for Required vs Optional Dependencies

Rule for runtime imports and dependency groups.

## Table of Contents

1. [Hard Rule](#1-hard-rule)
2. [Why This Matters](#2-why-this-matters)
3. [Patterns](#3-patterns)
4. [Special Cases](#4-special-cases)
5. [How to Check](#5-how-to-check)

______________________________________________________________________

## 1. Hard Rule

**Never wrap imports for required dependencies in `try/except ImportError`.**

If a package is listed in `[project.dependencies]`, import it normally at module top level.
A missing required dependency is a setup error and should fail fast.

```python
# CORRECT - required dependency import
import numpy as np
import requests
```

**Allowed exception:** optional or plugin dependencies that are intentionally not installed in every environment.
Those belong in `[project.optional-dependencies]` and must be handled with explicit fallback behavior.

______________________________________________________________________

## 2. Why This Matters

Defensive imports for required packages create avoidable complexity:

- They hide environment problems that should be fixed at install time.
- They force repeated `is not None` checks throughout the code.
- They defer failures to unrelated runtime paths.
- They make behavior harder to reason about and test.

Fail fast for required dependencies. Degrade gracefully only for truly optional features.

______________________________________________________________________

## 3. Patterns

### 3.1 Anti-Pattern: Defensive Import for Required Dependency

```python
# WRONG - required dependency should not be optionalized
try:
    import my_package
except ImportError:
    my_package = None


def run_feature() -> None:
    if my_package is not None:
        my_package.some_method()


def run_other_feature() -> None:
    if my_package is not None:
        my_package.other_method()
    else:
        raise RuntimeError("my_package not installed")
```

### 3.2 Correct: Required Dependency Imported Normally

```python
# CORRECT - dependency is required by project configuration
import my_package


def run_feature() -> None:
    my_package.some_method()


def run_other_feature() -> None:
    my_package.other_method()
```

### 3.3 Allowed: Optional Dependency with Localized Handling

```python
from collections.abc import Callable


def build_optional_renderer() -> Callable[[str], str] | None:
    """Return renderer when optional extra is installed, otherwise None."""
    try:
        import rich
    except ImportError:
        return None

    def render(message: str) -> str:
        return rich.markup.escape(message)

    return render
```

Guidelines for optional imports:

- Keep handling near one boundary (startup, factory, or plugin loader).
- Avoid scattering repeated `if package is not None` checks.
- Return explicit fallback behavior (None, no-op object, or clear error).
- Document why the dependency is optional.

______________________________________________________________________

## 4. Special Cases

### Plugin Systems

Dynamic plugin imports can use guarded imports. On failure, log or report a clear plugin-level error and continue only if the plugin is optional.

### Version Gates

Conditional imports based on Python version or platform are acceptable when they are runtime compatibility decisions, not missing dependency masking.

### Development Tooling

Do not treat core development tools as optional in CI. If a required tool is missing, fail immediately and fix the environment.

______________________________________________________________________

## 5. How to Check

1. Open `pyproject.toml`.
2. If package is in `[project.dependencies]`, use normal top-level import.
3. If package is in `[project.optional-dependencies]`, guarded import is allowed with explicit fallback behavior.
4. Search for likely violations:

```bash
rg "try:\\n\\s+import .*\\nexcept ImportError" src tests
```

Then classify each match as required vs optional and refactor accordingly.
