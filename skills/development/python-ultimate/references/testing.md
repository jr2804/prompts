# Testing Reference

Quick reference for writing effective Python tests.

## Table of Contents

1. [Test Organization](#test-organization)
2. [Coverage Standards](#coverage-standards)
3. [Fixtures](#fixtures)
4. [Parameterized Testing](#parameterized-testing)
5. [Mocking](#mocking)
6. [Performance Testing](#performance-testing)
7. [Test-Driven Development](#test-driven-development)
8. [Running Tests](#running-tests)
9. [Test File Conventions](#test-file-conventions)

______________________________________________________________________

## Test Organization

### Directory Structure

```
tests/
├── unit/
│   ├── core/          # Core functionality tests
│   └── utils/         # Utility function tests
├── integration/       # Integration tests
├── conftest.py        # Shared fixtures
└── test_data/         # Test data files
```

### Test File Naming

- Name test files `test_<module>.py`
- Place tests co-located with source code or in `tests/` directory
- Use `conftest.py` for shared fixtures at any directory level

### Test Class Naming

```python
class TestDataProcessor:
    """Test suite for data processor"""

    def test_process_data(self):
        """Test data processing with sample input"""
        ...
```

______________________________________________________________________

## Coverage Standards

| Level | Target |
|-------|--------|
| Unit Tests | 90%+ code coverage |
| Integration Tests | 80%+ scenario coverage |
| End-to-End | Critical user journeys |

Run coverage with fail-under:

```bash
pytest --cov=src --cov-report=term-missing --cov-fail-under=90 tests/
```

______________________________________________________________________

## Fixtures

### Basic Fixture

```python
@pytest.fixture
def sample_data():
    """Provide sample data for testing"""
    return {"input": [1, 2, 3], "expected": [2, 4, 6]}
```

### Fixture with Teardown

```python
@pytest.fixture(scope="module")
def database_connection():
    """Database fixture with setup/teardown"""
    conn = create_test_database()
    yield conn
    conn.close()
    cleanup_test_database()
```

### Using Fixtures in Tests

```python
def test_process_data(self, sample_data):
    """Test with fixture"""
    result = process_data(sample_data["input"])
    assert result == sample_data["expected"]
```

### Shared Fixtures (conftest.py)

Place reusable fixtures in `conftest.py` at the test directory root:

```python
# tests/conftest.py
import pytest

@pytest.fixture
def cache_dir(tmp_path):
    """Standard cache directory for tests"""
    return tmp_path / "cache"
```

______________________________________________________________________

## Parameterized Testing

### Basic Parametrization

```python
@pytest.mark.parametrize("input,expected", [
    ([1, 2, 3], 6),
    ([], 0),
    ([-1, 0, 1], 0),
    ([1.5, 2.5], 4.0)
])
def test_sum_function(input, expected):
    """Test sum function with various inputs"""
    assert sum(input) == expected
```

### Multiple Parameters

```python
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_addition(a, b, expected):
    assert a + b == expected
```

______________________________________________________________________

## Mocking

### Basic Mocking

```python
from unittest.mock import patch, MagicMock

def test_api_call():
    """Test API call with mocking"""
    mock_response = MagicMock()
    mock_response.json.return_value = {"status": "success"}

    with patch("requests.get", return_value=mock_response):
        result = make_api_call()
        assert result == {"status": "success"}
        requests.get.assert_called_once_with("https://api.example.com/data")
```

### Mocking External Services

```python
@patch("mylib.external_service.fetch")
def test_with_external_mock(mock_fetch):
    """Test function that calls external service"""
    mock_fetch.return_value = {"data": "test"}
    result = my_function()
    assert result == expected_value
```

### Spy/Mock Combination

```python
def test_callback_is_called():
    """Test that callback is invoked with correct arguments"""
    callback = MagicMock()
    process_items([1, 2, 3], callback=callback)
    callback.assert_called_once_with(3)  # Total sum
```

______________________________________________________________________

## Performance Testing

### Basic Performance Test

```python
import time
import pytest

@pytest.mark.performance
def test_processing_speed():
    """Test processing speed meets requirements"""
    start_time = time.time()

    result = process_large_dataset()

    duration = time.time() - start_time
    assert duration < 5.0, f"Processing took {duration:.2f}s, expected <5.0s"
    assert result.is_valid()
```

### Performance with Benchmarking

```python
def test_sorting_performance(benchmark):
    """Benchmark sorting performance"""
    data = list(range(1000))
    result = benchmark(sorted, data)
    assert result == data
```

______________________________________________________________________

## Test-Driven Development

### Red-Green-Refactor Cycle

1. **Red**: Write a failing test first
2. **Green**: Write minimum production code to pass
3. **Refactor**: Improve code while keeping tests passing

### Iron Law of TDD

> Never write production code without a failing test first.

**Apply this sequence:**

1. Write a single failing test describing the desired behavior
2. Run tests to confirm failure (Red)
3. Write minimum code to make test pass (Green)
4. Verify all tests pass
5. Refactor if needed
6. Repeat

**Rationale**: Tests written after code often miss edge cases and don't drive design.

______________________________________________________________________

## Running Tests

### Standard Run

```bash
# Run all tests with verbose output
uv run pytest -v --tb=short

# Run with coverage
uv run pytest --cov=src --cov-report=term-missing

# Run specific file
uv run pytest tests/unit/test_processor.py

# Run tests matching pattern
uv run pytest -k "test_process"
```

### Useful Options

```bash
# Stop on first failure
pytest -x

# Show local variables in tracebacks
pytest -l

# Run only failed tests from last run
pytest --lf

# Run tests with output capture disabled
pytest -s
```

______________________________________________________________________

## Test File Conventions

### File Structure

```python
# test_<module_name>.py
import pytest
from unittest.mock import patch

class TestModuleName:
    """Test suite for module_name"""

    @pytest.fixture
    def setup(self):
        """Setup for each test"""
        ...

    def test_something(self):
        """Test description"""
        ...

    @pytest.mark.parametrize(...)
    def test_parametrized(self, ...):
        ...
```

### Test Data Location

- Use `./tests/cache` for test cache/database files
- Use `tmp_path` fixture for temporary test files
- Store static test data in `./tests/test_data/`

### Best Practices

1. **One assertion per test** when practical; multiple related assertions are acceptable
2. **Descriptive test names**: `test_user_cannot_login_with_invalid_password`
3. **Isolation**: Each test should be independent
4. **No shared mutable state** between tests
5. **Clean up** after tests that modify global state
