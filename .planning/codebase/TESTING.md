# Testing Patterns

**Analysis Date:** 2026-04-02

## Test Framework

**Runner:**

- Framework: `pytest` (via `uv run pytest`)
- Assertion Library: `unittest.TestCase` (in existing test) + `pytest` assertions (per standards)
- Type checking: `ty` for static analysis

**Run Commands:**

```bash
uv run pytest -v                    # Run all tests (verbose)
uv run pytest -v --tb=short         # Run with short tracebacks (recommended)
uv run pytest <path> -v             # Run specific test directory/file
ruff check src/ tests/ --fix        # Lint (includes test directory)
ruff format .                       # Format all code
```

## Test File Organization

**Location:**

- Co-located with source: `scripts/` directories contain both implementation and test files
- One test file found in repository: `skills/documents/pdf/scripts/check_bounding_boxes_test.py`
- Test filename convention: `<module>_test.py` (not `test_<module>.py`)

**Structure:**

```
skills/
├── documents/
│   └── pdf/
│       └── scripts/
│           ├── check_bounding_boxes.py       # Implementation
│           └── check_bounding_boxes_test.py   # Test
├── database/
│   └── database-schema/
│       └── test_skill.sh                     # Shell-based integration test
└── ...
```

**Current test files:**

- `skills/documents/pdf/scripts/check_bounding_boxes_test.py` - Unit tests (247 lines, 11 test methods)
- `skills/database/database-schema/test_skill.sh` - Bash-based directory/file structure validation

## Test Structure

**Suite Organization (from existing test file):**

```python
import unittest
from check_bounding_boxes import get_bounding_box_messages


class TestGetBoundingBoxMessages(unittest.TestCase):
    def create_json_stream(self, data):
        """Helper to create a JSON stream from data"""
        return io.StringIO(json.dumps(data))

    def test_no_intersections(self):
        """Test case with no bounding box intersections"""
        data = { ... }
        stream = self.create_json_stream(data)
        messages = get_bounding_box_messages(stream)
        self.assertTrue(any("SUCCESS" in msg for msg in messages))
        self.assertFalse(any("FAILURE" in msg for msg in messages))


if __name__ == "__main__":
    unittest.main()
```

**Patterns observed:**

- `unittest.TestCase` class-based organization
- Docstrings on each test method
- Helper methods prefixed with `create_` or similar
- Separate test methods for each scenario (no-parametrize in existing tests)
- `if __name__ == "__main__": unittest.main()` for direct execution

**Recommended pytest style (per standards):**

```python
import pytest

@pytest.fixture
def sample_data():
    """Universal sample data fixture"""
    return {"valid_input": get_valid_input()}

@pytest.mark.parametrize("input,expected", [
    ([1, 2, 3], 6),
    ([], 0),
    ([-1, 0, 1], 0),
])
def test_sum_function(input, expected):
    """Test sum function with various inputs"""
    assert sum(input) == expected
```

## Mocking

**Framework:** `unittest.mock` (standard library)

**Patterns (from testing-strategy skill):**

```python
from unittest.mock import patch, MagicMock

def test_api_call():
    """Test API calls with mocking"""
    mock_response = MagicMock()
    mock_response.json.return_value = {"status": "success"}

    with patch("requests.get", return_value=mock_response):
        result = make_api_call()
        assert result == {"status": "success"}
        requests.get.assert_called_once_with("https://api.example.com/data")
```

**What to Mock:**

- External API calls (network requests, file I/O from external services)
- Database connections when testing business logic
- File system operations when not testing I/O directly

**What NOT to Mock:**

- Pure functions and data transformations
- Simple data structures and their operations
- Code under test itself

## Fixtures and Factories

**Test Data:**

- Create inline test data within test methods or helper methods
- Use `unittest.TestCase` helper methods for data construction
- Example: `create_json_stream(self, data)` helper in `check_bounding_boxes_test.py`

**Location:**

- Test data is defined inline within test files
- No dedicated `conftest.py` or test data directory found
- No shared fixtures observed (each test is self-contained)

**Recommended pattern per standards:**

```python
@pytest.fixture(scope="module")
def database_connection():
    """Universal database fixture"""
    conn = create_test_database()
    yield conn
    conn.close()
    cleanup_test_database()
```

## Coverage

**Target:** 90%+ code coverage (per python-standards SKILL.md)

**View Coverage:**

```bash
uv run pytest --cov=src --cov-report=term-missing --cov-fail-under=90
```

**Current state:** No coverage configuration found in `pyproject.toml` or dedicated config files. Coverage targets are specified in the python-standards skill but not enforced via config.

## Test Types

**Unit Tests:**

- Scope: Individual functions and methods
- Approach: Test inputs/outputs, edge cases, error conditions
- Example: `check_bounding_boxes_test.py` tests `get_bounding_box_messages()` with various input scenarios
- Pattern: Arrange data, call function, assert on results

**Integration Tests:**

- Scope: Module/skill structure validation
- Approach: Bash scripts verifying directory structure, file existence, SKILL.md content
- Example: `test_skill.sh` checks directory layout, required files, frontmatter fields

**E2E Tests:**

- Not observed in repository

**Performance Tests:**

- Referenced in AGENTS.md template (`pytest-benchmark`) but not implemented

## Existing Test Quality Patterns

**Edge case testing (from `check_bounding_boxes_test.py`):**

- No intersections vs. intersections
- Same-field intersections vs. cross-field intersections
- Different pages (should not intersect)
- Edge-touching boxes (should not count as intersecting)
- Height validation against font size
- Default values when optional fields missing
- Error message limits (abort after threshold)
- Missing optional data (no entry_text)

**Assertion patterns:**

```python
# Check for presence of success/failure keywords
self.assertTrue(any("SUCCESS" in msg for msg in messages))
self.assertFalse(any("FAILURE" in msg for msg in messages))

# Check for specific error types
self.assertTrue(any("FAILURE" in msg and "intersection" in msg for msg in messages))

# Check error limiting behavior
failure_count = sum(1 for msg in messages if "FAILURE" in msg)
self.assertGreater(failure_count, 0)
self.assertLess(len(messages), 30)
```

## Test Anti-Patterns to Avoid

**From test-driven-development skill:**

- Never write implementation before the test
- If you skip TDD, delete implementation and start over from tests
- Never use `# noqa` to suppress linter issues in tests

**From testing-strategy skill:**

- Don't mock pure functions
- Don't test implementation details
- Don't use the same test for multiple concerns

## Conformance Testing

Referenced in AGENTS.md for algorithm projects:

- Include conformance tests against official reference vectors when applicable
- Example: PESQ algorithm would need conformance against official test vectors

______________________________________________________________________

*Testing analysis: 2026-04-02*
