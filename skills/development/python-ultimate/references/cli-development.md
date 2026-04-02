# CLI Development Reference

Universal patterns for developing command-line interfaces in Python.

## Table of Contents

1. [Framework Selection](#1-framework-selection)
2. [Project Structure](#2-project-structure)
3. [Parameter Handling](#3-parameter-handling)
4. [Output Formatting](#4-output-formatting)
5. [Environment Variables Integration](#5-environment-variables-integration)
6. [Error Handling](#6-error-handling)
7. [Help Text and Documentation](#7-help-text-and-documentation)
8. [Testing CLI Applications](#8-testing-cli-applications)

---

## 1. Framework Selection

Choose the right framework based on project complexity:

| Framework | Use Case | Key Features |
|-----------|----------|--------------|
| **Typer** | Simple CLIs with type annotations | Auto-generated help, shell completion |
| **Click** | Complex CLIs, nested commands | Commands, groups, plugin system |
| **Argparse** | Standard library, minimal deps | Built-in, no external dependencies |

```python
# Typer - Simple, type-annotated CLIs
import typer
from typing import Optional

def main(
    input_file: str = typer.Argument(..., help="Input file path"),
    output_file: Optional[str] = typer.Option(None, "-o", "--output", help="Output file path"),
    verbose: bool = typer.Option(False, "-v", "--verbose", help="Verbose output")
):
    """Universal CLI entry point"""
    typer.echo(f"Processing {input_file}")

if __name__ == "__main__":
    typer.run(main)
```

```python
# Click - Complex CLIs with nested commands
import click

@click.group()
def cli():
    """Main CLI entry point"""
    pass

@cli.command()
@click.argument("input_file")
@click.option("-o", "--output", help="Output file path")
def process(input_file, output):
    """Process a file"""
    click.echo(f"Processing {input_file}")

if __name__ == "__main__":
    cli()
```

```python
# Argparse - Standard library approach
import argparse

parser = argparse.ArgumentParser(description="Universal CLI")
parser.add_argument("input_file", help="Input file path")
parser.add_argument("-o", "--output", help="Output file path")
args = parser.parse_args()
```

---

## 2. Project Structure

Organize CLI applications for maintainability:

```
project/
├── src/
│   └── project/
│       ├── __init__.py
│       ├── cli/
│       │   ├── __init__.py
│       │   ├── main.py          # Entry point
│       │   ├── commands/        # Command modules
│       │   │   ├── __init__.py
│       │   │   ├── process.py
│       │   │   └── config.py
│       │   └── shared/          # Shared utilities
│       │       ├── __init__.py
│       │       ├── options.py   # Common options
│       │       └── formatting.py # Output formatting
│       └── core/
│           └── ...
├── tests/
│   └── test_cli/
├── pyproject.toml
└── README.md
```

```python
# src/project/cli/main.py
import typer
from typing import Optional

app = typer.Typer(help="Project CLI", no_args_is_help=True)

@app.command()
def process(
    input_file: str = typer.Argument(..., help="Input file path"),
    output: Optional[str] = typer.Option(None, "-o", "--output", help="Output file"),
    verbose: bool = typer.Option(False, "-v", "--verbose", help="Verbose output")
):
    """Process the input file"""
    ...

if __name__ == "__main__":
    app()
```

---

## 3. Parameter Handling

Structure parameters consistently and validate early:

```python
# Parameter handling with validation
import os
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class CLIParameters:
    """Structured CLI parameters with validation"""
    input_file: str
    output_file: Optional[str] = None
    verbose: bool = False
    timeout: int = 30

    @classmethod
    def from_args(cls, args) -> "CLIParameters":
        """Parse arguments into structured parameters"""
        output = args.output or cls._default_output(args.input_file)
        return cls(
            input_file=args.input_file,
            output_file=output,
            verbose=args.verbose
        )

    @staticmethod
    def _default_output(input_file: str) -> str:
        """Generate default output filename"""
        name, ext = os.path.splitext(input_file)
        return f"{name}_out{ext}"

    def validate(self) -> None:
        """Validate parameters before execution"""
        if not os.path.exists(self.input_file):
            raise FileNotFoundError(f"Input file not found: {self.input_file}")
        if self.timeout <= 0:
            raise ValueError("Timeout must be positive")
```

**Parameter Types:**

```python
# Positional arguments (required)
input_file: str = typer.Argument(..., help="Input file path")

# Options (with defaults)
output: Optional[str] = typer.Option(None, "-o", "--output", help="Output file")
verbose: bool = typer.Option(False, "-v", "--verbose", help="Verbose output")
count: int = typer.Option(1, "-c", "--count", help="Number of iterations")

# Flags with explicit True/False
force: bool = typer.Option(False, "--force/--no-force", help="Force operation")

# Multiple values
files: list[str] = typer.Option([], "-f", "--file", help="Input files (multiple allowed)")
```

---

## 4. Output Formatting

Use Rich for beautiful, informative output:

```python
# Rich output formatting
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

# Status messages
console.print("[green]✓[/green] Operation completed successfully")
console.print("[red]✗[/red] Error: File not found")
console.print("[yellow]⚠[/yellow] Warning: Deprecated feature used")
console.print("[cyan]?[/cyan] Processing: file.txt")

# Panel output
panel = Panel.fit(
    "Result content",
    title="Results",
    border_style="blue",
    padding=(1, 2)
)
console.print(panel)

# Table output
table = Table(title="Files")
table.add_column("Name", style="cyan")
table.add_column("Size", justify="right", style="green")
table.add_column("Status", style="yellow")
table.add_row("file1.txt", "1.2 KB", "OK")
table.add_row("file2.txt", "3.4 KB", "OK")
console.print(table)

# Progress indicators
with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    console=console
) as progress:
    task = progress.add_task("Processing...", total=100)
    # Work here
    progress.update(task, advance=50)
```

---

## 5. Environment Variables Integration

Manage configuration via environment variables:

```python
# Environment variable patterns
import os
from dotenv import load_dotenv
from dataclasses import dataclass

# Load .env file in development
load_dotenv()

@dataclass
class EnvConfig:
    """Environment-based configuration"""
    debug: bool = False
    timeout: int = 30
    api_key: str = ""
    max_retries: int = 3

    @classmethod
    def from_env(cls) -> "EnvConfig":
        """Load configuration from environment variables"""
        return cls(
            debug=os.getenv("DEBUG", "false").lower() == "true",
            timeout=int(os.getenv("TIMEOUT", "30")),
            api_key=os.getenv("API_KEY", ""),
            max_retries=int(os.getenv("MAX_RETRIES", "3"))
        )

    def validate(self) -> None:
        """Validate required environment variables"""
        if not self.api_key and not self.debug:
            raise EnvironmentError("API_KEY environment variable required")
```

**Accessing env vars in Click:**

```python
# Click with environment variables
import click
from dotenv import load_dotenv

load_dotenv()

@click.option("--config", envvar="APP_CONFIG", help="Config file path")
@click.option("--debug", envvar="DEBUG", is_flag=True, help="Debug mode")
def process(config, debug):
    ...
```

---

## 6. Error Handling

Provide clear, actionable error messages:

```python
# Error handling with user-friendly messages
from rich.console import Console
import sys

console = Console()

def handle_cli_error(error, context="CLI", verbose: bool = False) -> int:
    """Handle errors with user-friendly messages, return exit code"""
    if isinstance(error, FileNotFoundError):
        console.print(f"[red]✗[/red] File not found: {error.filename}")
        suggest_similar_files(error.filename)
        return 1
    elif isinstance(error, PermissionError):
        console.print(f"[red]✗[/red] Permission denied: {error.filename}")
        console.print("[yellow]⚠[/yellow] Try running with elevated privileges")
        return 1
    elif isinstance(error, ValueError) as e:
        console.print(f"[red]✗[/red] Invalid value: {str(e)}")
        return 1
    else:
        console.print(f"[red]✗[/red] {context} error: {str(error)}")
        if verbose:
            console.print_exception()
        return 1

def suggest_similar_files(filename: str) -> None:
    """Suggest similar files when file not found"""
    import os
    directory = os.path.dirname(filename)
    basename = os.path.basename(filename)
    if os.path.exists(directory):
        matches = [f for f in os.listdir(directory) if basename.lower() in f.lower()]
        if matches:
            console.print(f"[cyan]Did you mean:[/cyan] {', '.join(matches)}")

# Main entry point with error handling
def main():
    try:
        cli_params = CLIParameters.from_args(args)
        cli_params.validate()
        run_process(cli_params)
    except Exception as e:
        sys.exit(handle_cli_error(e, verbose=args.verbose))
```

**Exit codes:**

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Misuse of command |
| 127 | Command not found |

---

## 7. Help Text and Documentation

Write clear, useful help text:

```python
# Good help text patterns
def main(
    input_file: str = typer.Argument(
        ...,
        help="Path to input file",
        show_default=False
    ),
    output: Optional[str] = typer.Option(
        None,
        "-o", "--output",
        help="Output file path [default: auto-generated from input]",
        show_default=False
    ),
    workers: int = typer.Option(
        4,
        "-w", "--workers",
        help="Number of parallel workers",
        min=1,
        max=32
    ),
    verbose: bool = typer.Option(
        False,
        "-v", "--verbose",
        help="Enable verbose output"
    )
):
    """
    Process INPUT_FILE and generate formatted output.

    Examples:

        python cli.py process data.txt -o result.txt

        python cli.py process data.txt --workers 8 --verbose
    """
    ...
```

**Help text guidelines:**

- Keep descriptions concise (one line if possible)
- Use imperative mood ("Process file" not "Processes file")
- Show defaults when relevant
- Provide examples for complex commands
- Document exit codes for scripts

---

## 8. Testing CLI Applications

Test CLI applications thoroughly:

```python
# Testing CLI applications
import pytest
from typer.testing import CliRunner
from project.cli.main import app

runner = CliRunner()

def test_cli_basic_invocation():
    """Test basic CLI invocation"""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "--help" in result.output

def test_cli_process_file(tmp_path):
    """Test file processing command"""
    input_file = tmp_path / "input.txt"
    input_file.write_text("test content")

    result = runner.invoke(app, ["process", str(input_file)])
    assert result.exit_code == 0
    assert "Processing" in result.output

def test_cli_missing_file():
    """Test error handling for missing file"""
    result = runner.invoke(app, ["process", "/nonexistent/file.txt"])
    assert result.exit_code == 1
    assert "not found" in result.output.lower()

def test_cli_with_options(tmp_path):
    """Test CLI with various options"""
    input_file = tmp_path / "input.txt"
    input_file.write_text("test content")

    result = runner.invoke(app, [
        "process",
        str(input_file),
        "-o", str(tmp_path / "output.txt"),
        "-v"
    ])
    assert result.exit_code == 0

# Fixture for CLI runner
@pytest.fixture
def cli_runner():
    """Provide a CLI runner for tests"""
    return CliRunner()

# Isolated filesystem tests
def test_cli_isolated_filesystem(cli_runner):
    """Test CLI with isolated filesystem"""
    with cli_runner.isolated_filesystem():
        # Create test files
        os.mkdir("input")
        # Run CLI
        result = cli_runner.invoke(app, ["process", "input/file.txt"])
        # Assertions
```
