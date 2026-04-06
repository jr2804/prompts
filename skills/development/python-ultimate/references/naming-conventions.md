---
name: naming-conventions
description: Consolidated naming conventions for Python code covering files, directories, tests, fixtures, loop variables, and constants.
---

# Naming Conventions

Consolidated naming conventions for Python code, covering variables, functions, classes, files, directories, and tests.

______________________________________________________________________

## Table of Contents

1. [Files and Directories](#1-files-and-directories)
2. [Test Naming](#2-test-naming)
3. [Fixtures](#3-fixtures)
4. [Unused Loop Variables](#4-unused-loop-variables)
5. [Constants and Enums](#5-constants-and-enums)
6. [Reserved for Future](#6-reserved-for-future)

______________________________________________________________________

## 1. Files and Directories

Clear naming prevents confusion between files, directories, and generic paths.

### 1.1 Variable Naming Rules

**Suffix-based naming** for path variables:

```python
from pathlib import Path

# CORRECT - File variables end with "_file"
output_file = Path("results/output.json")
config_file = Path.home() / ".config" / "app.toml"
log_file = temp_dir / "app.log"

# CORRECT - Directory variables end with "_dir"
output_dir = Path("results")
cache_dir = Path.home() / ".cache" / "app"
temp_dir = Path(tempfile.mkdtemp())

# CORRECT - "_path" ONLY when type is genuinely ambiguous
# (rare - only when truly unknown if file or directory)
data_path = Path("data")  # Could be file or directory, unknown at this point

# WRONG - Generic "path" is ambiguous
path = Path("output")  # File or directory?

# WRONG - "results" is ambiguous
results = Path("results")  # Folder? File? Result object?

# WRONG - "dir" and "file" as prefixes
dir_output = Path("output")  # Should be: output_dir
file_output = Path("output.txt")  # Should be: output_file
```

### 1.2 Rules Summary

| Suffix | Usage | Example |
|--------|-------|---------|
| `_file` | Variable represents a **file** | `output_file`, `config_file`, `log_file` |
| `_dir` | Variable represents a **directory** | `output_dir`, `cache_dir`, `temp_dir` |
| `_path` | **Exceptional cases only** - when genuinely unclear if file or directory | `data_path` (if type unknown) |

### 1.3 Anti-Patterns

**Never use these patterns:**

1. **Generic "path"** - Too ambiguous

   - ❌ `path = Path("foo")`
   - ✅ `config_file = Path("config.toml")`
   - ✅ `data_dir = Path("data")`

2. **Ambiguous names** - Could be object, file, or folder

   - ❌ `results = Path("results")`
   - ✅ `results_dir = Path("results")`
   - ✅ `results_file = Path("results.json")`

3. **"path" suffix for known types** - Be specific

   - ❌ `example_path = Path("example.txt")`
   - ✅ `example_file = Path("example.txt")`

4. **"dir"/"file" as prefix** - Always use as suffix

   - ❌ `dir_output = Path("output")`
   - ❌ `file_output = Path("output.txt")`
   - ✅ `output_dir = Path("output")`
   - ✅ `output_file = Path("output.txt")`

5. **Bare generic names for path-related variables** - Names like `path`, `file`, `folder`, `dir`, `directory`, `output`, `input`, `source`, `target`, `dest` are too ambiguous when they represent file system paths. They could refer to a file, a directory, a result object, a string, or anything else.

   - ❌ `file = Path("data.txt")`
   - ❌ `folder = Path("output")`
   - ❌ `dir = Path("cache")`
   - ❌ `directory = Path("build")`
   - ❌ `source = Path("src")`
   - ❌ `target = Path("dist")`
   - ✅ `input_file = Path("data.txt")`
   - ✅ `output_dir = Path("output")`
   - ✅ `cache_dir = Path("cache")`
   - ✅ `build_dir = Path("build")`
   - ✅ `source_dir = Path("src")`
   - ✅ `dist_dir = Path("dist")`

   **Exception:** These bare names are acceptable for *non-path* variables (e.g., `file` as a file handle/open file object, `source` as a string of source code, `target` as a function argument name in a generic API). The violation occurs specifically when the variable holds a `Path` object or a path string.

### 1.4 Rationale

- **Consistency with `pathlib.Path`**: Since `Path` objects can represent both files and directories, the variable name must clarify which is intended.
- **Prevents bugs**: Clear naming prevents accidentally calling `.mkdir()` on a file path or `.unlink()` on a directory.
- **Self-documenting code**: Variable names communicate intent without comments.

### 1.5 Automated Validation

Use the included validator script to check naming:

```bash
# Check a single variable name
uv run assets/check_path_naming.py output_file
# Output: is_file

# Scan Python files for violations
uv run assets/check_path_naming.py --check-files src/
```

______________________________________________________________________

## 2. Test Naming

### 2.1 Test Files

```python
# CORRECT - test_<module>.py
test_processor.py
test_validation.py
test_cli.py

# WRONG
tests_processor.py
processor_test.py
processor_tests.py
```

### 2.2 Test Classes

```python
# CORRECT - PascalCase with "Test" prefix
class TestDataProcessor:
    """Test suite for data processor"""

class TestValidation:
    """Test suite for validation logic"""

# WRONG
class DataProcessorTests:
class DataProcessorTest:
class test_data_processor:
```

### 2.3 Test Methods

```python
# CORRECT - snake_case with "test_" prefix
def test_process_data(self):
def test_validation_fails_on_empty_input(self):
def test_handles_unicode_characters(self):

# WRONG
def process_data_test(self):
def testProcessData(self):
def test(self):
```

______________________________________________________________________

## 3. Fixtures

Fixtures use snake_case and should clearly describe what they provide:

```python
# CORRECT - snake_case, descriptive names
@pytest.fixture
def sample_data():
    """Provide sample data for testing"""
    return {"input": [1, 2, 3], "expected": [2, 4, 6]}

@pytest.fixture(scope="module")
def database_connection():
    """Database fixture with setup/teardown"""

@pytest.fixture
def cache_dir(tmp_path):
    """Standard cache directory for tests"""
    return tmp_path / "cache"

# WRONG - unclear purpose
@pytest.fixture
def data():
@pytest.fixture
def temp():
```

______________________________________________________________________

## 4. Unused Loop Variables

Prefix intentionally unused loop variables with underscore:

```python
# CORRECT - underscore prefix for unused
for _ in items:
    process_items()

for i, _ in enumerate(pairs):
    process_index(i)

# WRONG - linter error B007
for item in items:  # 'item' never used
    process_items()

# WRONG - misleading double underscore
for __ in items:  # looks like dunder, not "unused"
    process_items()
```

______________________________________________________________________

## 5. Constants and Enums

Use UPPER_SNAKE_CASE for module-level constants:

```python
# CORRECT - UPPER_SNAKE_CASE
MAX_RETRY_COUNT = 3
DEFAULT_TIMEOUT_SECONDS = 30
SUPPORTED_FORMATS = ["json", "xml", "yaml"]

# Enum values also use UPPER_SNAKE_CASE
class Status(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

# WRONG
maxRetryCount = 3
DefaultTimeout = 30
supported_formats = ["json", "xml"]
```

______________________________________________________________________

## 6. Reserved for Future

This section is reserved for additional naming conventions that may be added in the future, such as:

- Class naming conventions (PascalCase requirements)
- Function naming conventions (snake_case requirements)
- Private vs public member naming (\_leading_underscore)
- Type variable naming (T, KT, VT, etc.)

______________________________________________________________________
