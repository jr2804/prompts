---
name: coding-standards
description: Consolidated Python coding standards reference for type hints, strings, logging, code size, docstrings, comments, libraries, and error handling.
---

# Coding Standards Reference

## Table of Contents

- [Coding Standards Reference](#coding-standards-reference)
  - [Table of Contents](#table-of-contents)
  - [1. Type Hints (Mandatory)](#1-type-hints-mandatory)
  - [2. String Formatting](#2-string-formatting)
  - [3. Data Structures](#3-data-structures)
    - [Comprehensions](#comprehensions)
    - [pathlib.Path](#pathlibpath)
    - [enumerate()](#enumerate)
    - [Resource Management](#resource-management)
  - [3.5. Naming Conventions](#35-naming-conventions)
  - [4. Logging](#4-logging)
  - [5. Code Size Limits](#5-code-size-limits)
  - [6. Docstrings](#6-docstrings)
  - [7. Comments](#7-comments)
  - [8. Library Preferences](#8-library-preferences)
  - [9. Version Control](#9-version-control)
    - [Commit Message Format](#commit-message-format)
    - [Branch Naming](#branch-naming)
  - [10. Boolean Flags and Environment Variables](#10-boolean-flags-and-environment-variables)
    - [Boolean Flags](#boolean-flags)
    - [Environment Variables](#environment-variables)
  - [11. Error Handling](#11-error-handling)
  - [12. Prohibited Patterns](#12-prohibited-patterns)
    - [TYPE_CHECKING](#type_checking)
    - [Prohibited Linter Rules](#prohibited-linter-rules)
    - [os.path](#ospath)
    - [Optional[T]](#optionalt)
    - [Vague Type Annotations: object and Any](#vague-type-annotations-object-and-any)
  - [Linting and Formatting](#linting-and-formatting)

______________________________________________________________________

## 1. Type Hints (Mandatory)

Type hints are required for **all** function parameters and return values.

```python
def process_data(item_id: str, group_id: int) -> dict[str, str]:
    """Process a data item and return metadata."""
    return {"id": item_id, "group": group_id}

# Use pipe syntax for optional types
from pathlib import Path

def fetch_data(item_id: str, cache_dir: Path | None = None) -> dict[str, str] | None:
    """Fetch data metadata, returns None if not found."""
    if cache_dir is None:
        return None
    return {"id": item_id}
```

**Rules:**

- Use `T | None` instead of `Optional[T]`
- Use precise types (str, int, Path, etc.) — never default to `object` or `Any`
- If you need a union of known types, use `|`: `str | int | Path`
- For structured objects with known fields, define a `typing.Protocol` or `@dataclass`
- Only use `typing.Any` for genuinely dynamic values (e.g., binary blobs from embedded Python)
- When `Any` is truly unavoidable, prefer `typing.Any` over bare `object`

**Null comparisons:** Use `is` and `is not` for `None`, not `==` or `!=`.

______________________________________________________________________

## 2. String Formatting

Use f-strings for **all** string formatting.

```python
# CORRECT
name = "S4-123456"
meeting = "SA4#99e"
print(f"Processing {name} from {meeting}")

# WRONG
print("Processing {} from {}".format(name, meeting))
print("Processing %s from %s" % (name, meeting))
```

______________________________________________________________________

## 3. Data Structures

### Comprehensions

```python
# List comprehension
ids = [i.id for i in items if i.active]

# Dictionary comprehension
item_map = {i.id: i for i in items}
```

### pathlib.Path

```python
from pathlib import Path

# CORRECT
cache_dir = Path.home() / ".project-cache" / "data"
cache_dir.mkdir(parents=True, exist_ok=True)

# WRONG
import os.path
cache_dir = os.path.join(os.path.expanduser("~"), ".project-cache", "data")
```

### enumerate()

```python
# CORRECT - when you need both index and value
for i, item in enumerate(items):
    print(f"{i}: {item.id}")

# WRONG
for i in range(len(items)):
    print(f"{i}: {items[i].id}")
```

### Resource Management

Use `with` statements when working with files.

```python
# CORRECT
from pathlib import Path
with open("data.json") as f:
    data = json.load(f)

# WRONG
f = open("data.json")
data = json.load(f)
f.close()
```

______________________________________________________________________

## 3.5. Naming Conventions

See [naming-conventions.md](naming-conventions.md) for comprehensive naming conventions, including:

- Files and directories (suffix-based naming: `_file`, `_dir`, `_path`)
- Test naming conventions
- Fixture naming conventions
- Unused loop variables
- Constants and enums

______________________________________________________________________

## 4. Logging

Use the `logging` module instead of `print()`.

```python
import logging

logger = logging.getLogger(__name__)

logger.debug("Processing item: %s", item_id)
logger.info("Successfully fetched metadata for %s", item_id)
logger.warning("Retry attempt %d for %s", retry_count, item_id)
logger.error("Failed to process %s: %s", item_id, exc_info=True)
```

______________________________________________________________________

## 5. Code Size Limits

Keep modules and symbols small to preserve maintainability:

| Symbol | Limit |
| ------ | ----- |
| Modules (`.py` file) | < 250 lines |
| Functions | < 75 lines |
| Classes | < 200 lines |

**Refactor when limits are exceeded:**

- Split large functions into smaller helper functions
- Extract common logic to separate utilities
- Split large classes into composition of smaller classes

______________________________________________________________________

## 6. Docstrings

Write clear, concise docstrings using Google style.

```python
def fetch_item_metadata(item_id: str, source: str) -> dict[str, Any] | None:
    """Fetch data metadata from the specified source.

    Args:
        item_id: The unique identifier (e.g., "DOC-123456")
        source: The metadata source ("api", "database", or "cache")

    Returns:
        Dictionary with metadata fields (title, author, timestamp, etc.),
        or None if the item is not found.

    Raises:
        ValueError: If source is not recognized
        ConnectionError: If the API endpoint is unreachable

    Examples:
        >>> fetch_item_metadata("DOC-123456", "api")
        {"id": "DOC-123456", "title": "Example document", ...}
    """
```

______________________________________________________________________

## 7. Comments

Comments should explain **intent** or **subtle constraints**, not restate what's obvious.

```python
# GOOD - explains WHY
# IDs are case-insensitive, so normalize to uppercase
item_id = item_id.upper()

# GOOD - documents a subtle constraint
# The portal API rate-limits to 10 requests/second
time.sleep(0.1)

# BAD - restates what the code does
# Get the ID from the item object
id = item.id
```

**DO NOT:**

- Repeat obvious names (variable/function names already describe what they are)
- Include "what you did" (belongs in commit messages)
- Use decorative headings (`===== MIGRATION TOOLS =====`)
- Number steps (`// Step 3: Fetch data`)
- Use emojis or special Unicode characters

______________________________________________________________________

## 8. Library Preferences

| Task | Preferred Library | Notes |
| ---- | ----------------- | ----- |
| CLI | typer | Type hints for CLI |
| Terminal formatting | rich | Beautiful terminal output |
| Data models — validation / serialization | pydantic | API boundaries, user input, config files |
| Data models — simple containers | `@dataclass` (stdlib) | Internal DTOs, lightweight structs |
| App settings | pydantic-settings | Use BaseSettings for config |
| Database | oxyde | SQL backend for pydantic models |
| Testing | pytest | Testing framework |
| Formatting/linting | ruff, undersort, codespell | Code quality tools |
| Excel reading | pandas + python-calamine | Fast Excel reading |
| Excel writing | xlsxwriter | Excel output |
| Type checking | ty | Static type checking |

______________________________________________________________________

## 8.5. Data Modeling — Dataclass vs. Pydantic

Choose the right tool based on **what the data does**, not just what it holds.

### Decision Framework

| Use case | Use | Why |
|----------|-----|-----|
| Internal DTOs, geometric points, intermediate structs | `@dataclass` | Stdlib, zero deps, minimal overhead, immutable with `frozen=True` |
| API request/response models, user input, config files | `pydantic.BaseModel` | Runtime validation, type coercion, JSON serialization, clear error messages |
| Environment / file-based configuration | `pydantic-settings.BaseSettings` | Declarative env mapping, `.env` support, nested overrides |
| Dictionary-like structures with fixed keys | `TypedDict` | Lightweight typing for dict interfaces where you don't need a class |

### Rules

1. **Default to `@dataclass` for purely internal data.** If the data never crosses a trust boundary (user input, network, file), does not need JSON serialization, and does not need runtime validation, use `@dataclass`. It is faster, has no extra dependency, and `frozen=True` gives you value semantics for free.

2. **Use `pydantic` at trust boundaries.** Any time data comes from outside the program (HTTP request, CLI args parsed to a model, config file, database row), use `pydantic.BaseModel` so invalid data fails loudly and early with a descriptive error.

3. **Don't mix the two for the same concept.** If a type starts as `@dataclass` and later needs validation, convert it to `pydantic.BaseModel` rather than bolting on manual `__post_init__` validation in a dataclass.

### Examples

```python
from dataclasses import dataclass

# CORRECT — lightweight internal point, never leaves the process
@dataclass(frozen=True, slots=True)
class Point:
    x: float
    y: float
```

```python
from pydantic import BaseModel, Field, EmailStr

# CORRECT — user-facing data with validation at a trust boundary
class UserRegistration(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=150)
```

```python
from dataclasses import dataclass

# CORRECT — CLI parameter bundle, validated by Typer before reaching this struct
@dataclass
class RenderOptions:
    width: int
    height: int
    output_file: Path
```

```python
from typing import TypedDict

# CORRECT — dict-shaped data from an external JSON API you don't control
class GithubRepo(TypedDict):
    id: int
    name: str
    full_name: str
```

### Anti-patterns

```python
# WRONG — pydantic is overkill for a simple internal struct
from pydantic import BaseModel
class Point(BaseModel):
    x: float
    y: float

# WRONG — dataclass provides no runtime validation for untrusted input
@dataclass
class UserInput:
    email: str  # Accepts "not-an-email" silently
```

```python
# CORRECT
from dataclasses import dataclass
@dataclass(frozen=True, slots=True)
class Point:
    x: float
    y: float

from pydantic import BaseModel, EmailStr
class UserInput(BaseModel):
    email: EmailStr
```

______________________________________________________________________

## 9. Version Control

### Commit Message Format

```text
Type: feat, fix, docs, style, refactor, perf, test, chore
Scope: optional module/component
Subject: imperative, present tense, <50 chars
Body: optional detailed explanation
Footer: optional breaking changes, issue references
```

### Branch Naming

```text
Feature branches: feature/<name>
Bug fixes: fix/<description>
Documentation: docs/<topic>
Releases: release/v<version>
```

______________________________________________________________________

## 10. Boolean Flags and Environment Variables

### Boolean Flags

```python
class FeatureFlags:
    def __init__(self, **flags):
        self._flags = flags

    def is_enabled(self, flag_name: str) -> bool:
        return self._flags.get(flag_name, False)

    def enable(self, flag_name: str) -> None:
        self._flags[flag_name] = True

    def disable(self, flag_name: str) -> None:
        self._flags[flag_name] = False
```

### Environment Variables

```python
import os

def get_env_var(name: str, default: str | None = None) -> str:
    """Get environment variable with validation."""
    value = os.environ.get(name, default)
    if value is None:
        raise ValueError(f"Required environment variable {name} not set")
    return value
```

______________________________________________________________________

## 11. Error Handling

```python
def safe_operation(func, *args, **kwargs):
    """Execute function with universal error handling."""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error("Operation %s failed: %s", func.__name__, str(e), exc_info=True)
        return get_fallback_value(func)
```

______________________________________________________________________

## 12. Prohibited Patterns

### TYPE_CHECKING

Never use `TYPE_CHECKING` as a permanent solution for circular imports. Refactor to eliminate circular dependencies.

Canonical deep-dive guidance for this rule lives in [type-checking.md](type-checking.md). Keep this section concise and use the dedicated reference for alternatives and migration steps.

```python
# WRONG - permanent TYPE_CHECKING guard
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from my_project.database import ItemDatabase

# RIGHT - lazy import (temporary fix) or refactor
def _resolve_data_id(db_file: Path) -> int:
    from my_project.database import ItemDatabase  # Lazy import
    with ItemDatabase(db_file) as db:
        return db.resolve_data_id(name)
```

### Prohibited Linter Rules

Never suppress linter issues with `# noqa`. Fix the underlying issue instead.

Never introduce these rules:

- **PLC0415**, **E402** - Import at top of file
- **ANN001** - Missing type annotation for function argument
- **E402** - Module-level import not at top of file
- **ANN201** - Missing return type annotation for public function
- **ANN202** - Missing return type annotation for private function

### os.path

Use `pathlib.Path` instead of `os.path`.

### Optional[T]

Use `T | None` instead of `Optional[T]`.

### Vague Input/Output Types

Never design functions with wide, ambiguous parameter or return types that force the caller to handle many implicit cases. Such signatures are a sign that the function is doing too much input validation and output normalization internally — responsibilities that should belong to the caller.

**Anti-pattern — all of these are wrong:**

```python
def fear_to_failure_func(
    arg1: int | str | None,
    arg2: str | None = None,
    arg3: Any | None = None,
) -> int | None:
    if arg1 is None:
        return None
    if isinstance(arg1, str):
        try:
            arg1 = int(arg1)
        except ValueError:
            return None
    # ... boilerplate for arg2, arg3 ...
    if result > 0:
        return result
    return None
```

**Why it's wrong:**

- The function signature hides what it actually accepts, making callers guess.
- Repeated `isinstance` / `hasattr` checks inside the function are a code smell — they indicate the function is compensating for a vague signature.
- `T | None` for both input and output forces callers to handle many implicit branches.
- The function silently swallows cases (`return None`) instead of failing loudly, masking bugs.

**Principles to apply instead:**

1. **Be precise.** Use the narrowest type that describes the actual data, not the widest type you think might work. If `arg1` should be an `int`, say `int`, not `int | str | None`.
2. **Fail loudly.** If a caller passes an invalid type, raise a clear `TypeError` or `ValueError` immediately rather than returning `None`. Let the caller handle the error at the call site.
3. **Separate concerns.** Input conversion and output normalization are the caller's responsibility. The function should trust its contract.
4. **Avoid `Any` in signatures.** Use it only in genuinely untyped contexts (e.g., `**kwargs`). Prefer protocols or base types for structured flexibility.
5. **Single-responsibility functions.** If you find yourself writing `isinstance` or `hasattr` checks inside a function, split it into two functions: one that validates/transforms, one that does the work.

**Correct patterns:**

```python
# Input: accept only what you actually need
def process_item(item_id: int) -> dict[str, Any]:
    """Process a single item by its integer ID."""
    ...

# Output: use a dedicated result type instead of None-as-error
@dataclass
class ProcessResult:
    value: int
    reason: str | None = None

def process_item(item_id: int) -> ProcessResult:
    ...
```

**When `T | None` is acceptable:**

- Return type when `None` is a legitimate, documented outcome (e.g., "not found" vs "found"). Document it explicitly.
- Parameters that are genuinely optional in the business sense — e.g., `timeout: float | None = None` where `None` means "use default". Not because you are afraid of validation.

**Quick self-check:**

- Does the function body contain `isinstance` or `hasattr` on its own parameters? → Split or narrow the type.
- Does the function return `None` as a silent fallback for more than one condition? → Use a result type or raise an exception.
- Is `Any` in the signature because you don't know what the caller might pass? → The caller should convert first.

### Vague Type Annotations: `object` and `Any`

Using `object` or `typing.Any` as type annotations is almost always a sign of
laziness rather than genuine need. Both defeat static type checking and introduce
linter warnings. There is always a more precise option.

**Anti-pattern examples:**

```python
from typing import Any

# WRONG — callers and type checkers gain nothing from these signatures
def save_to_db(record: object) -> object: ...
def process(data: Any) -> Any: ...
```

**What to use instead:**

| Scenario | Preferred pattern | Example |
|----------|-------------------|---------|
| Value can be one of a few known types | Union via `\|` | `str \| int \| None` |
| Structured object with known fields | `typing.Protocol` | `class Renderable(Protocol): ...` |
| Simple data container | `@dataclass` or `TypedDict` | `@dataclass class Point: ...` |
| True dynamic / binary object | `Any` (rare exception) | Embedded Python binary blobs |

**Protocols over ABCs:**

For structural typing, prefer `typing.Protocol` over abstract base classes.
Protocols use duck typing — any object with the right methods satisfies the
protocol without explicit inheritance, which is cleaner and more flexible:

```python
from typing import Protocol

class Serializable(Protocol):
    """Anything with a to_dict method."""
    def to_dict(self) -> dict[str, str]: ...


def persist(obj: Serializable) -> None:
    data = obj.to_dict()
    ...

# No inheritance needed — any object with to_dict() works
persist(my_object)  # OK if my_object has to_dict()
```

**When `Any` is acceptable (rare):**

- Objects dynamically created by an embedded Python runtime (C/C++ extensions,
  embedded interpreter)
- Binary blobs passed through from a lower-level library where the type is truly
  opaque at the Python layer
- Generic deserialization helpers where the output type is determined at runtime
  (and a `TypeVar` or `@overload` won't work)

In these cases, use `typing.Any` rather than bare `object`. The linter
understands that `Any` is explicitly opt-in; bare `object` just looks like a
forgotten type annotation.

______________________________________________________________________

## Linting and Formatting

Run linters after significant changes:

```bash
# Run linter
ruff check src/ tests/

# Format code
ruff format src/ tests/

# Sort imports
ruff check src tests --select I --fix

# Type check
ty src/
```

Always use `uv run` for Python commands to ensure the virtual environment is activated.

For more details, see: [Ruff Rules](https://docs.astral.sh/ruff/rules/)
