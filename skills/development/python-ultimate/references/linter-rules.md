# Ruff Linter Rules Reference

## Table of Contents

- [Overview](#overview)
- [E402: Module Level Import Not at Top of File](#e402-module-level-import-not-at-top-of-file)
- [B007: Loop Control Variable Not Used](#b007-loop-control-variable-not-used)
- [B008: Function Call in Default Argument](#b008-function-call-in-default-argument)
- [S108: Hardcoded Temp File](#s108-hardcoded-temp-file)
- [PLC0415: Import Outside Top-Level](#plc0415-import-outside-top-level)
- [PLW0603: Global Statement](#plw0603-global-statement)
- [NPY002: Legacy NumPy Random Generation](#npy002-legacy-numpy-random-generation)
- [S311: Suspicious Non-Cryptographic Random Usage](#s311-suspicious-non-cryptographic-random-usage)
- [Typer CLI Exception for B008](#typer-cli-exception-for-b008)
- [General Fix Strategy](#general-fix-strategy)

______________________________________________________________________

## Overview

Ruff is a fast Python linter written in Rust that identifies issues following PEP 8 and other best practices. It provides context-aware fixes that distinguish between production code, test code, and CLI frameworks.

When fixing linter errors:

1. Identify the rule code from the linter output
2. Select the appropriate fix pattern based on your code's context
3. Apply the fix and verify it resolves the issue without introducing new problems

______________________________________________________________________

## E402: Module Level Import Not at Top of File

**Rule Code:** E402

**Description:** An import statement appears after code that is not an import, comment, or docstring.

**Problem Pattern:** Imports placed after executable code in a module.

**Fix Pattern:** Keep module-level imports at the top by default, grouped by standard library, third-party, then local imports. Follow [canonical import guidance](imports-optional-dependencies.md) for justified local imports.

**Example:**

```python
# BEFORE (linter error)
def get_platform():
    import platform  # Error: import after code

    return platform.system()


# AFTER (fixed)
import platform


def get_platform():
    return platform.system()
```

______________________________________________________________________

## B007: Loop Control Variable Not Used

**Rule Code:** B007

**Description:** A variable defined in a `for` loop is never used within the loop body.

**Problem Pattern:** Loop variables that are never referenced after assignment.

**Fix Pattern:** Prefix unused loop variables with an underscore (`_`) to indicate intentional non-use. See [naming-conventions.md](naming-conventions.md) for complete guidelines.

**Example:**

```python
# BEFORE (linter error)
for item in items:
    process_items()  # 'item' never used

# AFTER (fixed)
for _ in items:
    process_items()
```

______________________________________________________________________

## B008: Function Call in Default Argument

**Rule Code:** B008

**Description:** A function call is used as a default argument value, evaluated only once at function definition time.

**Problem Pattern:** Mutable or dynamic return values captured at module load time instead of call time.

**Fix Pattern:** Use `None` as default and initialize inside the function body.

**Example:**

```python
# BEFORE (linter error)
def create_list():
    return [1, 2, 3]


def process_data(items: list[int] = create_list()):
    items.append(4)
    return items


# AFTER (fixed)
def process_data(items: list[int] | None = None):
    if items is None:
        items = create_list()
    items.append(4)
    return items
```

______________________________________________________________________

## S108: Hardcoded Temp File

**Rule Code:** S108

**Description:** Hardcoded paths like `/tmp/`, `/var/tmp/`, or `C:\Temp\` for temporary files.

**Problem Pattern:** Using predictable temporary file paths instead of secure, platform-appropriate alternatives.

**Fix Pattern (Production):** Use `tempfile.NamedTemporaryFile` with `delete=False`.

**Fix Pattern (Test):** Use pytest's `tmp_path` fixture.

**Example - Production:**

```python
# BEFORE (linter error)
with open("/tmp/data.txt", "w") as f:
    f.write(data)

# AFTER (fixed)
import tempfile

with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
    f.write(data)
    temp_path = f.name
```

**Example - Test:**

```python
# BEFORE (linter error)
def test_file_processing():
    test_file = "/tmp/test_data.txt"
    with open(test_file, "w") as f:
        f.write("test")


# AFTER (fixed)
def test_file_processing(tmp_path: Path):
    test_file = tmp_path / "test_data.txt"
    test_file.write_text("test")
```

______________________________________________________________________

## PLC0415: Import Outside Top-Level

**Rule Code:** PLC0415

**Description:** Import statements placed inside functions, methods, or class definitions instead of at module level.

**Problem Pattern:** Imports buried within function bodies, making dependencies unclear.

**Fix Pattern:** Prefer module-level imports; see [canonical import guidance](imports-optional-dependencies.md) for justified local imports.

**Example:**

```python
# BEFORE (linter error)
def print_version():
    import platform

    print(platform.python_version())


# AFTER (fixed)
import platform


def print_version():
    print(platform.python_version())
```

**Standard Import Organization:**

```python
# 1. Standard library imports
import os
import sys
from pathlib import Path

# 2. Third-party imports
import typer
from rich.console import Console

# 3. Local application imports
from .utils import helpers
from .core import processors
```

______________________________________________________________________

## PLW0603: Global Statement

**Rule Code:** PLW0603 (`global-statement`)

**Description:** A function uses the `global` statement to rebind a
module-level name.

**Problem Pattern:** Treating a module-level variable as mutable shared state.

**Fix Pattern:** **Never fix this by suppressing it.** `# noqa: PLW0603` and
disabling the rule are both forbidden — the finding always indicates a design
problem. Replace the shared variable with explicit state:

- **Changing value** → return the new value, or hold it on an object that is
  passed in (`self._next += 1`).
- **Read-only value computed once** → a `@functools.cache` getter returning a
  frozen value.
- **Temporary context** → an explicit parameter or a small dataclass passed
  through the call chain.

**Example:**

```python
# WRONG
_cache: dict[str, str] = {}


def load(name: str) -> str:
    global _cache  # PLW0603
    if name not in _cache:
        _cache[name] = name.upper()
    return _cache[name]


# RIGHT — module variable becomes a cached getter result
from functools import cache


@cache
def load(name: str) -> str:
    return name.upper()
```

**Related:** [Module State and Globals](module-state.md) covers the full
rationale, mutability checks for module-level containers, and the
module-constant-table rules.

______________________________________________________________________

## NPY002: Legacy NumPy Random Generation

**Rule Code:** NPY002

**Description:** Usage of legacy `numpy.random` functions (`np.random.seed`, `np.random.normal`) instead of the modern `Generator` API.

**Problem Pattern:** Using frozen `RandomState` methods with global state and poorer statistical properties.

**Fix Pattern:** Use `numpy.random.default_rng()` for the modern `Generator` API.

**Example:**

```python
# BEFORE (linter error)
import numpy as np

np.random.seed(1337)
data = np.random.normal(size=100)

# AFTER (fixed)
import numpy as np

rng = np.random.default_rng(1337)
data = rng.normal(size=100)
```

______________________________________________________________________

## S311: Suspicious Non-Cryptographic Random Usage

**Rule Code:** S311

**Description:** Standard `random` module used in potentially sensitive contexts where cryptographic security is needed.

**Problem Pattern:** Using predictable pseudo-random generators for security-sensitive values.

**Fix Pattern (Security Context):** Use `secrets` module for tokens, passwords, or authentication.\
**Fix Pattern (Non-Security Context):** Use NumPy's `default_rng()` for better performance.

**Example - Security Context:**

```python
# BEFORE (security risk)
import random

token = random.randrange(1000000)

# AFTER (secure)
import secrets

token = secrets.randbelow(1000000)
```

**Example - Non-Security Context:**

```python
# Use NumPy for simulation/data analysis
import numpy as np

rng = np.random.default_rng()
data = rng.random(100)
```

______________________________________________________________________

## Typer CLI Exception for B008

When using `typer.Option()` or `typer.Argument()`, function calls in defaults are **intentional and required**. Apply this special annotation pattern instead of fixing B008:

```python
from typing import Annotated
import typer


def main(
    config: Annotated[
        str, typer.Option(help="Configuration file path")
    ] = "config.yaml",
) -> None:
    """CLI command with proper Typer annotations."""
    ...
```

**Key Pattern:** Use `Annotated` with `typer.Option`/`typer.Argument`, keeping the default value on the parameter itself.

______________________________________________________________________

## General Fix Strategy

| Context | Recommended Approach |
|---------|---------------------|
| **Production Code** | Use `tempfile` module for temp files, `secrets` for security |
| **Test Code** | Use pytest fixtures (`tmp_path`) for temp files |
| **CLI (Typer)** | Use `Annotated` pattern, do not fix B008 |
| **Data Science** | Prefer NumPy `default_rng()` over standard `random` |
| **Imports** | Module level by default; see [canonical import guidance](imports-optional-dependencies.md) for exceptions |
| **Global State** | Never suppress PLW0603; use explicit state or a `@cache` getter ([module state](module-state.md)) |

**When in doubt:**

1. Production vs Test: Choose based on module location and purpose
2. Security vs Non-Security: Default to `secrets` for any token, password, or key generation
3. Typer B008: Preserve the pattern, do not apply standard B008 fix
4. NumPy Random: Always prefer `default_rng()` for new code

**Reference:** [Ruff Full Rule Index](https://docs.astral.sh/ruff/rules/)
