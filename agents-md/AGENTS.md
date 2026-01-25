# LLM Coding Agent Guide for {{project-name}}

## Project Overview

You are a professional Python developer creating `{{project-name}}`, a {{project-description}}.

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

### Performance Considerations

- Optimize for performance using NumPy vectorized operations
- Avoid Python loops for signal processing tasks
- Profile and optimize critical code paths, when necessary
- Ensure memory efficiency, especially for large audio files
- Benchmark against the reference implementation for speed comparison
- Consider using numba for performance-critical sections if needed

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
- Avoid Python loops for signal processing operations
- Implement efficient memory management (avoid unnecessary copies)
- Use SciPy for optimized FFT and filtering operations
- Profile critical paths and optimize bottlenecks
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

### Conformance Testing

```python
# Download and test against official conformance samples
def test_conformance_p862():
    """Test against P.862 conformance samples."""
    # Download official test vectors
    # Run reference implementation (patched with corrigenda)
    # Run free-pesq implementation
    # Compare results within tolerance
    pass

def test_conformance_p862_1():
    """Test against P.862.1 conformance samples."""
    pass

def test_conformance_p862_2():
    """Test against P.862.2 conformance samples."""
    pass
```

### Performance Testing
- Use pytest-benchmark for performance regression tests
- Build conformance harness skeleton: discover WAV pairs, store expected placeholder JSON, add failing (xfail) tests as reminders.
- Benchmark against reference implementation speed
- Memory usage profiling
- Regression testing for performance
- Load testing with various file sizes

## File Structure
```
free-pesq/
├── pyproject.toml
├── README.md
├── AGENTS.md
├── src/
│   └── free_pesq/
│       ├── __init__.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── processor.py
│       │   ├── preprocessor.py
│       │   ├── aligner.py
│       │   ├── disturbance.py
│       │   └── mapper.py
│       ├── cli/
│       │   ├── __init__.py
│       │   └── main.py
│       └── utils/
│           ├── __init__.py
│           ├── audio.py
│           └── validation.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_core/
│   ├── test_cli/
│   ├── test_conformance/
│   └── data/
├── docs/
│   ├── api.md
│   ├── conformance.md
│   └── examples.md
└── scripts/
    ├── download_conformance_data.py
    ├── build_reference_tool.py
    └── run_conformance_tests.py
```

## Documentation Requirements

### README.md Structure
- Clear project description and legal disclaimer
- Installation instructions using uv
- Quick start guide with examples
- API documentation links
- Conformance testing information
- Contributing guidelines

### Code Documentation
- Google-style docstrings for all public APIs
- Type hints on all function signatures
- Inline comments for complex algorithms
- Examples in docstrings where appropriate

## Development Workflow

### Initial Setup
```bash
# Initialize project with uv
uv init {{project-name}}
cd free-pesq

# Install dependencies
uv add numpy scipy typer rich pydantic
uv add --dev pytest pytest-cov black isort mypy ruff

# Set up pre-commit hooks
uv add --dev pre-commit
```

### Code Quality Checks
```bash
# Format code
uv run black src tests
uv run isort src tests

# Lint code
uv run ruff check src tests
uv run ty src

# Run tests
uv run pytest tests/ -v --cov=src/free_pesq
```

## Legal and Compliance Notes

### Independence Requirements
- Never reference ITU source code during development
- Document all algorithmic choices as independent decisions
- Use different mathematical formulations where equivalent options exist
- Maintain development logs showing clean-room practices

### Trademark Considerations
- Use "implements ITU-T P.862" rather than "PESQ" in product descriptions
- Include appropriate disclaimers about trademark ownership
- Avoid suggesting official endorsement or affiliation

### Patent Considerations
- Verify current patent status in relevant jurisdictions
- Document that implementation is based on expired or non-applicable patents
- Include patent disclaimer in documentation

## Success Criteria

1. **Functional Compliance**: Pass all conformance tests within specified tolerances
2. **Performance**: Match or exceed reference implementation speed
3. **Code Quality**: Pass all linting, typing, and testing requirements
4. **Legal Safety**: Maintain complete independence from reference implementation
5. **Usability**: Provide clear API and CLI matching reference tool functionality

## Notes for LLM Implementation

- Always prioritize legal compliance over code simplicity
- When in doubt about algorithmic choices, choose the more independent approach
- Focus on clear, readable code over micro-optimizations
- Test extensively against conformance data
- Document all major algorithmic decisions and their independence rationale
- Use modern Python idioms and best practices throughout

## Annex A: Reference Implementation, Standard documents & additional material
The official reference implementation (C-code) is provided in the subdirectory `./itut-p862-ref-docs-data/T-REC-P.862-200511-W!Amd2!SOFT-ZST-E/Software/source`).

Several standard documents are provided along with the source code, which can be used to analyze the PESQ algorithm further in detail.

General information about PESQ algorithm:
- [ITU-T P.862 Recommendation](https://www.itu.int/rec/dologin_pub.asp?lang=e&id=T-REC-P.862-200102-W!!SOFT-ZST-E)
- [ITU-T P.862 Recommendation Corrigendum 1](https://www.itu.int/rec/dologin.asp?lang=e&id=T-REC-P.862-200710-W!Cor1!PDF-E)
- [ITU-T P.862 Recommendation Corrigendum 2](https://www.itu.int/rec/dologin.asp?lang=e&id=T-REC-P.862-201803-W!Cor2!ZIP-E)

Application Guide:
- [P.862.3: Application guide for objective quality measurement based on P.862](https://www.itu.int/rec/dologin_pub.asp?lang=e&id=T-REC-P.862.3-200711-W!!PDF-E)
- [P.862.3 (2007) Corrigendum 1 (11/11)](https://www.itu.int/rec/dologin.asp?lang=e&id=T-REC-P.862.3-201111-W!Cor1!PDF-E)

Narrowband (NB) mode of PESQ:
- [P.862.1: Mapping function for transforming P.862 raw result scores to MOS-LQO](https://www.itu.int/rec/dologin_pub.asp?lang=e&id=T-REC-P.862.1-200311-W!!PDF-E)

Wideband (WB) mode of PESQ:
- [P.862: Wideband extension to Recommendation P.862 for the assessment of wideband telephone networks and speech codecs](https://www.itu.int/rec/dologin_pub.asp?lang=e&id=T-REC-P.862.2-200711-W!!PDF-E)
- [P.862: Recommendation P.862.2 (2007) Corrigendum 1 (10/17)](https://www.itu.int/rec/dologin.asp?lang=e&id=T-REC-P.862.2-201710-W!Cor1!PDF-E)
- [P.862: Revised Annex A - Reference implementations and conformance testing for ITU-T Recs P.862, P.862.1 and P.862.2](https://www.itu.int/rec/dologin_pub.asp?lang=e&id=T-REC-P.862-200511-W!Amd2!SOFT-ZST-E&type=items)