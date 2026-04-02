---
name: coding-standards
description: Consolidated Python coding standards reference for type hints, strings, logging, code size, docstrings, comments, libraries, and error handling.
---

# Coding Standards Reference

## Table of Contents

1. [Type Hints](#1-type-hints-mandatory)
2. [String Formatting](#2-string-formatting)
3. [Data Structures](#3-data-structures)
4. [Logging](#4-logging)
5. [Code Size Limits](#5-code-size-limits)
6. [Docstrings](#6-docstrings)
7. [Comments](#7-comments)
8. [Library Preferences](#8-library-preferences)
9. [Version Control](#9-version-control)
10. [Boolean Flags and Environment Variables](#10-boolean-flags-and-environment-variables)
11. [Error Handling](#11-error-handling)
12. [Prohibited Patterns](#12-prohibited-patterns)

---

## 1. Type Hints (Mandatory)

Type hints are required for **all** function parameters and return values.

```python
from typing import Any

def process_data(item_id: str, group_id: int) -> dict[str, Any]:
    """Process a data item and return metadata."""
    return {"id": item_id, "group": group_id}

# Use pipe syntax for optional types
def fetch_data(item_id: str | None) -> dict[str, Any] | None:
    """Fetch data metadata, returns None if not found."""
    if item_id is None:
        return None
    return {"id": item_id}
```

**Rules:**
- Use `T | None` instead of `Optional[T]`
- Use `Any` from `typing` instead of `object`
- Include type hints in docstrings for parameters and returns

**Null comparisons:** Use `is` and `is not` for `None`, not `==` or `!=`.

---

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

---

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

---

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

---

## 5. Code Size Limits

Keep modules and symbols small to preserve maintainability:

| Symbol | Limit |
|--------|-------|
| Modules (`.py` file) | < 250 lines |
| Functions | < 75 lines |
| Classes | < 200 lines |

**Refactor when limits are exceeded:**
- Split large functions into smaller helper functions
- Extract common logic to separate utilities
- Split large classes into composition of smaller classes

---

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

---

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

---

## 8. Library Preferences

| Task | Preferred Library | Notes |
|------|-------------------|-------|
| CLI | typer | Type hints for CLI |
| Terminal formatting | rich | Beautiful terminal output |
| Data models | pydantic | Validation and serialization |
| App settings | pydantic-settings | Use BaseSettings for config |
| Database | oxyde | SQL backend for pydantic models |
| Testing | pytest | Testing framework |
| Formatting/linting | ruff, undersort, codespell | Code quality tools |
| Excel reading | pandas + python-calamine | Fast Excel reading |
| Excel writing | xlsxwriter | Excel output |
| Type checking | ty | Static type checking |

---

## 9. Version Control

### Commit Message Format

```
Type: feat, fix, docs, style, refactor, perf, test, chore
Scope: optional module/component
Subject: imperative, present tense, <50 chars
Body: optional detailed explanation
Footer: optional breaking changes, issue references
```

### Branch Naming

```
Feature branches: feature/<name>
Bug fixes: fix/<description>
Documentation: docs/<topic>
Releases: release/v<version>
```

---

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

---

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

---

## 12. Prohibited Patterns

### TYPE_CHECKING

Never use `TYPE_CHECKING` as a permanent solution for circular imports. Refactor to eliminate circular dependencies.

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

---

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
