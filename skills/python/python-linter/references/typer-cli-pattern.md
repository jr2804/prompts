# Typer CLI Argument Pattern (B008 Exception)

This document provides the correct pattern for using Typer CLI arguments that avoids B008 linter warnings while following Typer best practices.

## The Problem

Ruff's B008 rule flags function calls in default arguments as problematic. However, Typer's design **intentionally uses** `typer.Option()` and `typer.Argument()` calls in function signatures.

## The Solution: Annotated Pattern

Use Python's `Annotated` type with Typer options/arguments to satisfy both the linter and Typer's requirements.

### Complete Example

```python
"""
CLI module following Typer + Ruff best practices.
Avoids B008 linter warnings while maintaining Typer functionality.
"""

from typing import Annotated
from pathlib import Path
import typer

app = typer.Typer()


@app.command()
def process_data(
    # String option with help text
    input_file: Annotated[
        Path,
        typer.Argument(
            help="Input file to process",
            exists=True,
            file_okay=True,
            dir_okay=False,
        )
    ],
    
    # Optional string with default
    output_dir: Annotated[
        Path,
        typer.Option(
            "--output", "-o",
            help="Output directory for results"
        )
    ] = Path("./output"),
    
    # Boolean flag
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose", "-v",
            help="Enable verbose output"
        )
    ] = False,
    
    # Integer option with validation
    max_workers: Annotated[
        int,
        typer.Option(
            "--workers", "-w",
            help="Maximum number of worker threads",
            min=1,
            max=32,
        )
    ] = 4,
) -> None:
    """
    Process data from input file and save to output directory.
    
    Example:
        $ python cli.py data.csv --output results/ --workers 8
    """
    if verbose:
        typer.echo(f"Processing {input_file} with {max_workers} workers")
    
    # Your processing logic here
    output_dir.mkdir(parents=True, exist_ok=True)
    typer.echo(f"✓ Processed {input_file} → {output_dir}")


if __name__ == "__main__":
    app()
```

## Pattern Breakdown

### Structure

```python
parameter_name: Annotated[
    TypeHint,
    typer.Option(
        # Typer-specific configuration
        option_flags,
        help="Description",
        # validation, defaults, etc.
    )
] = default_value  # Python default (optional)
```

### Key Components

1. **`Annotated[...]`** - Python's type hint that includes metadata
2. **Type hint** - First argument: `str`, `int`, `Path`, `bool`, etc.
3. **`typer.Option()` / `typer.Argument()`** - Second argument: Typer configuration
4. **Python default** - After the annotation, standard Python default value

## Common Patterns

### Required Argument (No Default)

```python
config_file: Annotated[
    Path,
    typer.Argument(help="Configuration file path")
]
```

### Optional with Default

```python
log_level: Annotated[
    str,
    typer.Option("--log-level", help="Logging level")
] = "INFO"
```

### Boolean Flag

```python
dry_run: Annotated[
    bool,
    typer.Option("--dry-run", help="Simulate without making changes")
] = False
```

### List/Multiple Values

```python
tags: Annotated[
    list[str],
    typer.Option("--tag", help="Tags to apply (can be used multiple times)")
] = []
```

## Type Definitions Module Pattern

For complex CLIs, define argument types in a separate module:

```python
# my_package/cli/args.py
"""Reusable CLI argument type definitions."""

from typing import Annotated
from pathlib import Path
import typer

# Reusable type aliases
InputFile = Annotated[
    Path,
    typer.Argument(
        help="Input file path",
        exists=True,
        file_okay=True,
        dir_okay=False,
    )
]

OutputDir = Annotated[
    Path,
    typer.Option(
        "--output", "-o",
        help="Output directory"
    )
]

VerboseFlag = Annotated[
    bool,
    typer.Option(
        "--verbose", "-v",
        help="Enable verbose logging"
    )
]
```

Then use in commands:

```python
# my_package/cli/commands.py
from .args import InputFile, OutputDir, VerboseFlag

@app.command()
def process(
    input_file: InputFile,
    output_dir: OutputDir = Path("./output"),
    verbose: VerboseFlag = False,
) -> None:
    """Process command using shared type definitions."""
    ...
```

## Why This Works

1. **Satisfies Ruff:** The actual function parameter default is a simple value (not a function call)
2. **Satisfies Typer:** The `Annotated` metadata includes all Typer configuration
3. **Type-safe:** Full type checking support from mypy/pyright
4. **IDE-friendly:** Autocomplete and inline documentation work correctly

## References

- **Typer documentation:** https://typer.tiangolo.com/
- **Python Annotated:** https://docs.python.org/3/library/typing.html#typing.Annotated
- **Ruff B008 rule:** https://docs.astral.sh/ruff/rules/function-call-in-default-argument/

## When NOT to Use This Pattern

This pattern is **only for Typer CLI code**. For regular Python functions, follow the standard B008 fix:

```python
# Regular function (NOT Typer CLI)
def process_data(items: list[int] | None = None) -> list[int]:
    if items is None:
        items = []  # Initialize inside function
    return items
```
