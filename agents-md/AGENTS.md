# LLM Coding Agent Guide for {{project-name}}

## Project Overview

You are a professional Python developer creating `{{project-name}}`, a {{project-description}}.

- When in doubt about algorithmic choices, choose the more independent approach
- Focus on clear, readable code over micro-optimizations
- Use modern Python idioms and best practices throughout
- Before implementing new helper functions or any new business logic, investigate if such functionality already exists. Duplicate code must be avoided at all costs.

## Project Structure

The project structure can be parsed using the following command from the root of the repository:

```shell
rg --files | tree-cli --fromfile
```

Notes:

- Command requires `ripgrep` and `tree-cli` tools, which can be installed in the project via: `mise up`.
- Files/folders are never listed in the present file, always generate the structure on the fly using the above command!

## Core Principles

### Code Quality Standards

- Write professional, production-ready Python code
- Follow PEP 8 style guidelines strictly
- Use type hints for all function signatures and class attributes
- Implement comprehensive error handling and input validation
- Write self-documenting code with clear variable and function names
- Include docstrings for all public classes, methods, and functions (Google style)
- Add mypy + ruff run to confirm static quality.
- Use numpy and scipy for numerical computations and signal processing
- Avoid unnecessary dependencies; keep the project lightweight
- Use `uv` for dependency management and project setup
- Structure the project for easy extensibility and maintainability
- Implement unit tests with pytest to cover all functionality
- Include conformance tests against official PESQ test vectors (see below)

### Implementation Steps

- Step 1
- Step 2
- Step 3

## Technical Requirements

## Architecture Guidelines

### Object-Oriented Design

- Implement using clean OOP patterns
- Create separate classes for major algorithm components:
  - `...`: Main algorithm
  - `...`:
  - `...`:
- Use composition over inheritance
- Implement proper data encapsulation with properties

### Performance Optimization

- Use NumPy vectorized operations wherever possible
- Implement efficient memory management (avoid unnecessary copies)
- Use SciPy for optimized FFT and filtering operations
- Profile critical paths and optimize bottlenecks
- Consider using numba for performance-critical sections if needed
- Optimize for performance using NumPy vectorized operations
- Avoid Python loops for signal processing tasks
- Profile and optimize critical code paths, when necessary
- Ensure memory efficiency, especially for large audio files
- Benchmark against the reference implementation for speed comparison
- Consider using numba for performance-critical sections if needed

### Error Handling

- Define custom exception classes for domain-specific errors
- Validate all inputs at API boundaries
- Provide meaningful error messages with context
- Use logging for debugging and operational information
- Implement graceful degradation where appropriate

### Core Algorithm Components

...

### CLI Implementation

```python
# Use typer for CLI with rich formatting
import typer
from rich.console import Console
from pathlib import Path

app = typer.Typer(name="free-pesq", help="[")
console = Console()

@app.command()
def evaluate(
    reference: Path = typer.Argument(..., help="Reference audio file"),
    degraded: Path = typer.Argument(..., help="Degraded audio file"),
    mode: str = typer.Option("wb", "--mode", "-m", help="Mode: nb or wb"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file")
) -> None:
    """Evaluate speech quality using PESQ algorithm."""
    # Implementation here
```

## Testing Strategy

### Unit Testing with pytest

- Test all public methods and edge cases
- Use parametrized tests for different input scenarios
- Mock external dependencies appropriately
- Achieve >95% code coverage
- Include property-based testing with Hypothesis

### Performance Testing

- Use pytest-benchmark for performance regression tests
- Memory usage profiling
- Regression testing for performance
- Load testing with various file sizes

## Success Criteria

1. **Functional Compliance**: Pass all conformance tests within specified tolerances
1. **Performance**: Match or exceed reference implementation speed
1. **Code Quality**: Pass all linting, typing, and testing requirements
1. **Usability**: Provide clear API and CLI matching reference tool functionality

## Documentation Requirements

### README.md Structure

- Clear project description and legal disclaimer/license
- Installation instructions using uv
- Quick start guide with examples
- Links to API documentation and contributing guidelines

### Code Documentation

- Google-style docstrings for all public APIs
- Type hints on all function signatures
- Inline comments for complex algorithms
- Examples in docstrings where appropriate
