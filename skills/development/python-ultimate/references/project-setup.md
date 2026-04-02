# Project Setup Reference

Universal Python project structure and dependency management guidelines.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Dependency Management](#dependency-management)
3. [Import Organization](#import-organization)
4. [Virtual Environments](#virtual-environments)
5. [Python Version](#python-version)
6. [Package Configuration](#package-configuration)

---

## Project Structure

```
project/
├── src/                  # Main source code
│   └── package/          # Importable package
├── tests/                # Test suite
├── docs/                 # Documentation
├── scripts/              # Utility scripts
├── pyproject.toml        # Project configuration
├── README.md             # Project overview
└── .gitignore            # Version control ignore
```

**Key principles:**
- Place all importable code under `src/`
- Keep tests alongside source or in dedicated `tests/` directory
- Use `pyproject.toml` for all project metadata

---

## Dependency Management

**Use `uv` for all package operations:**

```bash
uv add package-name          # Add production dependency
uv add package-name --dev    # Add development dependency
uv remove package-name       # Remove dependency
uv sync --all-extras -U     # Update all dependencies
```

**`pyproject.toml` configuration:**

```toml
[project]
name = "package-name"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "requests>=2.28",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "ruff>=0.1.0",
]
```

---

## Import Organization

Organize imports in three blocks, separated by blank lines:

```python
# 1. Standard library imports
import os
import sys
from pathlib import Path
from typing import Any

# 2. Third-party imports
import numpy as np
import pandas as pd
from pydantic import BaseModel

# 3. Local application imports
from .utils import helpers
from .core import processors
```

**Rules:**
- Never use relative imports beyond a single level (prefer `from .module` over `from ..module`)
- Avoid `import *`
- Sort alphabetically within each block

---

## Virtual Environments

```bash
# Create environment with uv
uv venv .venv

# Activate (Linux/macOS)
source .venv/bin/activate

# Activate (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Install project with dependencies
uv sync
```

---

## Python Version

**Minimum: Python 3.10**

Use modern type hint syntax:

```python
# Use | instead of Union or Optional
def process_data(
    input_data: list[dict[str, int | str]],
    config: dict[str, str] | None = None
) -> dict[str, list[float]]:
    ...
```

---

## Package Configuration

**Standard `pyproject.toml` sections:**

```toml
[project]
name = "package-name"
version = "0.1.0"
description = "Package description"
requires-python = ">=3.10"
dependencies = []

[project.optional-dependencies]
dev = ["pytest", "ruff"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.ruff]
line-length = 100
target-version = "py310"
```
