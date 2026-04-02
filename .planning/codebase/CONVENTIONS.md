# Coding Conventions

**Analysis Date:** 2026-04-02

## Naming Patterns

**Files:**

- Python scripts: `snake_case.py` (e.g., `get_etsi_spec.py`, `quick_validate.py`, `init_skill.py`)
- Skill directories: `hyphen-case` (e.g., `etsi-spec`, `skill-creator`, `code-execution`)
- Markdown files: `UPPER_SNAKE_CASE.md` for top-level docs (e.g., `SKILL.md`, `README.md`), `hyphen-case.md` for references
- YAML/JSON: `snake_case` (e.g., `skills-lock.json`, `pyproject.toml`)

**Functions:**

- `snake_case` throughout (e.g., `extract_text_inventory`, `get_bounding_box_messages`, `validate_skill`)
- Class methods: `snake_case` (e.g., `to_dict`, `_estimate_frame_overflow`, `get_default_font_size`)
- Private/internal methods: prefix with `_` (e.g., `_calculate_slide_overflow`, `_wrap_text_line`, `_detect_bullet_issues`)
- Factory functions: `verb_noun` pattern (e.g., `collect_shapes_with_absolute_positions`, `extract_pdf_metadata`)

**Variables:**

- `snake_case` for all variables (e.g., `skill_dir`, `font_path`, `total_height_px`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `SKILL_TEMPLATE`, `ALLOWED_PROPERTIES`, `TEMPLATE_DIR`, `DOCUMENT_TYPE_ALIASES`)
- Type aliases: `PascalCase` (e.g., `JsonValue`, `ParagraphDict`, `InventoryData`, `ShapeDict`)
- Module-level typed constants remain `UPPER_SNAKE_CASE`

**Types:**

- Dataclasses: `PascalCase` (e.g., `ShapeWithPosition`, `ParagraphData`, `ShapeData`)
- Type aliases: defined at module level using `type` or assignment (e.g., `JsonValue = Union[str, int, float, bool, None]`)

## Code Style

**Formatting:**

- Ruff formatter (`ruff format .`)
- Undersort for import ordering (`undersort .`)
- Ruff isort-style sorting (`ruff check --select I --fix`)
- mdformat for Markdown files (`mdformat .`)
- Configuration: `pyproject.toml` at project root; mise tasks defined in `.config/mise/config.toml`
- No custom ruff.toml or .ruff.toml found -- defaults from ruff apply

**Linting:**

- Tool: `ruff check`
- Run command: `ruff check src/ tests/ --fix`
- Formatting command: `ruff format .`
- Type checking command: `ty src/`
- **NEVER** suppress linter issues with `# noqa` in any directory
- Prohibited rules (must be fixed, never suppressed):
  - `PLC0415`, `E402` - Imports must be at top of file
  - `ANN001` - Missing type annotation for function argument
  - `ANN201` - Missing return type annotation for public function
  - `ANN202` - Missing return type annotation for private function
- Circular imports: refactor to eliminate; never use `TYPE_CHECKING` guards as permanent solution

## Import Organization

**Order:**

1. Standard library imports
2. Third-party imports
3. Local/project imports

**Style:**

- Absolute imports preferred
- `from X import Y` for specific names
- Sort via `ruff check --select I --fix` (isort equivalent)
- Undersort for additional import organization

**Script Dependencies:**

- Skill scripts declare dependencies as inline script metadata:
  ```python
  # /// script
  # requires-python = ">=3.11"
  # dependencies = [
  #   "requests<3",
  #   "rich",
  # ]
  # ///
  ```
- Run with `uv run <script>`

## Type Hints

**Required everywhere:**

- All function parameters and return values must have type hints
- Use `T | None` instead of `Optional[T]` (pipe syntax)
- Use `Any` from `typing` instead of `object`
- Include type hints in docstrings for parameters and return values
- Never use `from typing import TYPE_CHECKING` / `if TYPE_CHECKING:` guards

**Examples from codebase:**

```python
def extract_text_inventory(
    pptx_path: Path, prs: Any | None = None, issues_only: bool = False
) -> InventoryData:
    ...

def fetch_data(item_id: str | None) -> dict[str, Any] | None:
    ...
```

## String Formatting

- **Always** use f-strings
- **Never** use `.format()` or `%` formatting

```python
# CORRECT
print(f"Processing {name} from {meeting}")

# WRONG
print("Processing {} from {}".format(name, meeting))
```

## Error Handling

**Patterns:**

- Use specific exception types (`ValueError`, `requests.RequestException`, etc.)
- Catch broad `Exception` only at top-level `main()` with traceback printing
- Validate inputs early (e.g., file existence, correct extension)
- Provide meaningful error messages with context

```python
# Pattern from codebase
try:
    result = some_operation()
except ValueError as e:
    print(f"Error: {e}")
    sys.exit(1)
except requests.RequestException as e:
    print(f"Network error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Unexpected error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
```

**Return values:**

- Functions return `None` for missing/optional results
- Raise exceptions for actual errors (not missing data)
- Use `Optional` return for "not found" cases

## Logging

**Framework:** Standard `logging` module (per python-standards SKILL.md)

```python
import logging
logger = logging.getLogger(__name__)
logger.debug("Processing item: %s", item_id)
```

**Note:** Existing scripts use `print()` for CLI output. Logging module is the standard for library code.

## Comments

**When to Comment:**

- Explain WHY, not WHAT
- Document subtle constraints, rate limits, algorithm choices
- Avoid decorative headings, numbered steps, emojis, or special Unicode

**Docstrings:**

- Google-style docstrings for all public classes, methods, and functions
- Include Args, Returns, Raises, and Examples sections

```python
def parse_spec_number(spec_input: str) -> dict[str, str | None]:
    """
    Parse specification number from various input formats.

    Accepts:
    - "103224" (six digits, defaults to TS)
    - "103 224" (three digits, space, three digits)
    - "ETSI TS 103 224" (prefix + three digits, space, three digits)

    Returns:
        dict: {'doc_type': 'TS', 'prefix': '103', 'number': '224', 'part': None}
    """
```

## Function Design

**Size limits (from python-standards):**

- Modules (.py): < 250 lines (exception: CLI registration files)
- Functions: < 75 lines
- Classes: < 200 lines

**Parameters:** Prefer explicit parameters over `**kwargs`; use `argparse` for CLI entry points

**Return Values:** Prefer returning dataclasses or typed dicts over raw dicts

## Module Design

**Entry points:**

- Use `if __name__ == "__main__":` pattern
- Use `argparse` or `typer` for CLI argument parsing
- Exit with `sys.exit(0)` on success, `sys.exit(1)` on error

**Exports:**

- No barrel files or `__init__.py` re-exports observed
- Scripts are standalone with inline dependency declarations

## Data Structures

**Prefer built-in comprehensions:**

```python
ids = [i.id for i in items if i.active]
item_map = {i.id: i for i in items}
```

**Prefer `pathlib.Path` over `os.path`:**

```python
from pathlib import Path
cache_dir = Path.home() / ".project-cache" / "data"
```

**Prefer `enumerate()` over manual index tracking:**

```python
for i, item in enumerate(items):
    print(f"{i}: {item.id}")
```

**Null comparisons:** Use `is None` / `is not None`, never `== None`

**Resource management:** Use `with` statements for files

## Code Size Limits

- **Modules**: < 250 lines
- **Functions**: < 75 lines
- **Classes**: < 200 lines
- Split large modules/functions/classes when limits exceeded

______________________________________________________________________

*Convention analysis: 2026-04-02*
