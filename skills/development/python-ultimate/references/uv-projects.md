---
name: uv-projects
description: uv project workflow — init, add, sync, lock, --locked vs --frozen, dependency groups, workspaces, publish, and tool-vs-uvx decisions.
---

# uv Projects Reference

## Table of Contents

- [uv Projects Reference](#uv-projects-reference)
  - [Table of Contents](#table-of-contents)
  - [1. When to Use This Reference](#1-when-to-use-this-reference)
  - [2. Project Initialization](#2-project-initialization)
  - [3. Dependency Management](#3-dependency-management)
  - [4. Locking and Syncing](#4-locking-and-syncing)
  - [5. Locked vs Frozen vs Neither](#5-locked-vs-frozen-vs-neither)
  - [6. Workspaces (Monorepos)](#6-workspaces-monorepos)
  - [7. Building and Publishing](#7-building-and-publishing)
  - [8. Tool Execution: uvx vs uv tool install](#8-tool-execution-uvx-vs-uv-tool-install)
  - [9. Environment Variables](#9-environment-variables)
  - [10. Common Mistakes](#10-common-mistakes)
  - [11. Migration Cheatsheet](#11-migration-cheatsheet)
  - [12. Related References](#12-related-references)

______________________________________________________________________

## 1. When to Use This Reference

For **multi-file Python projects** managed by `pyproject.toml` and `uv.lock`.

For single-file standalone scripts with inline dependencies, use
[uv-scripts.md](uv-scripts.md) instead. The two modes are mutually exclusive.

______________________________________________________________________

## 2. Project Initialization

```bash
uv init my-project          # new project in a subdirectory
uv init                     # initialize the current directory
uv init --lib               # library with src/ layout and py.typed
uv init --app               # application (default)
uv init --package           # project that builds into an installable package
```

`uv init` creates `pyproject.toml`, `.python-version`, `.gitignore`, `README.md`,
and a starter `main.py` (or `src/<pkg>/__init__.py` for `--lib`).

______________________________________________________________________

## 3. Dependency Management

```bash
uv add requests                         # production dependency
uv add "flask>=2.0"                     # pinned specifier
uv add httpx aiofiles                   # multiple at once
uv add --dev pytest ruff mypy           # dev group ([dependency-groups] dev)
uv add --group docs mkdocs              # custom group
uv add --optional postgres psycopg      # optional extra ([project.optional-dependencies])
uv add --optional gui pyqt6
uv remove requests                      # remove from pyproject + lockfile
uv add -r requirements.txt              # import legacy requirements file
```

Rules:

- Prefer `uv add` / `uv remove` over editing `pyproject.toml` by hand for
  dependency lines — `uv` re-locks atomically.
- Pin with PEP 508 specifiers (`">=2.0,<3"`) rather than bare names for anything
  you intend to ship or revisit.
- Use `--dev` for test/lint/format tooling, `--group <name>` for grouped extras
  (docs, ci-tools), `--optional <name>` for installable library extras.

______________________________________________________________________

## 4. Locking and Syncing

```bash
uv lock                          # create/update uv.lock
uv lock --upgrade-package flask  # targeted upgrade of one package
uv lock --upgrade                # upgrade everything (use deliberately, not routinely)

uv sync                          # install locked deps into .venv
uv sync --all-extras             # include optional extras
uv sync --all-groups             # include all dependency groups
```

`uv sync` creates `.venv` if missing — never call `uv venv` then `uv sync`.

______________________________________________________________________

## 5. Locked vs Frozen vs Neither

| Flag | Behavior | When to use |
| ---- | -------- | ----------- |
| *(none)* `uv sync` | Re-resolves if `pyproject.toml` changed since last lock | Day-to-day dev |
| `uv sync --locked` | Refuses to run if the lockfile is stale; never mutates it | Reproducible installs where staleness is an error |
| `uv sync --frozen` | Uses `uv.lock` as-is, skips all checks, never mutates | Fast installs from a known-good committed lockfile |

Default to `--locked` whenever reproducibility matters more than convenience
(shared branches, release prep). Reserve `--frozen` for when you trust the
lockfile absolutely and want speed.

______________________________________________________________________

## 6. Workspaces (Monorepos)

Declare a workspace in the root `pyproject.toml`:

```toml
[tool.uv.workspace]
members = ["packages/*"]
```

Each member is its own package with its own `pyproject.toml`; all members share
one root `uv.lock`. Cross-package dependencies use local paths:

```toml
[tool.uv.sources]
my-shared-lib = { workspace = true }
```

Run a command in a specific member:

```bash
uv run --package api pytest
```

______________________________________________________________________

## 7. Building and Publishing

```bash
uv build                  # produces sdist + wheel in dist/
uv build --out-dir out    # custom output directory
uv publish                # upload to PyPI
uv publish --token ...    # explicit token (or set UV_PUBLISH_TOKEN)
```

For trusted publishing from CI, configure OIDC on the indexer side and use
`uv publish` without a token.

______________________________________________________________________

## 8. Tool Execution: uvx vs uv tool install

| Need | Command | Example |
| ---- | ------- | ------- |
| Run a tool once | `uvx <tool>` | `uvx ruff check .` |
| Run a tool with extra packages | `uvx --with mkdocs-material mkdocs build` | |
| Run a pinned tool | `uvx ruff@0.8.0 check .` | |
| Install a frequently-used tool | `uv tool install ruff` | |
| Upgrade an installed tool | `uv tool upgrade ruff` | |
| List installed tools | `uv tool list` | |

Rules:

- `uv tool install` for daily-use dev tools (ruff, black, mypy, pytest).
- `uvx` for one-offs and version-pinned invocations.
- Pin versions for reproducibility (`ruff@0.8.0`); avoid `@latest`.

For MCP server execution and IDE configuration with `uvx --from`, see the
standalone `uv` skill — that topic is out of scope here.

______________________________________________________________________

## 9. Environment Variables

| Variable | Effect |
| -------- | ------ |
| `UV_COMPILE_BYTECODE=1` | Pre-compile `.pyc` for faster startup |
| `UV_NO_SYNC=1` | Skip sync during `uv run` |
| `UV_LINK_MODE=copy` | Copy files instead of hardlinks (cross-filesystem safety) |
| `UV_MANAGED_PYTHON=1` | Use only uv-managed Python interpreters |
| `UV_PROJECT_ENVIRONMENT` | Override `.venv` location |
| `UV_CACHE_DIR` | Override cache directory (see [uv.md §4](uv.md)) |
| `UV_PYTHON_INSTALL_DIR` | Override managed-Python install location |

______________________________________________________________________

## 10. Common Mistakes

| Mistake | Correct pattern |
| ------- | --------------- |
| `pip install X` inside a uv project | `uv add X` (managed by `pyproject.toml`) |
| Activating `.venv` before `uv run` | `uv run` handles activation automatically |
| Running `uv venv` then `uv sync` | `uv sync` creates `.venv` — skip `uv venv` |
| Committing `.venv/` | Add `.venv/` to `.gitignore`; commit `uv.lock` |
| Not committing `uv.lock` | Always commit `uv.lock` for reproducible installs |
| `uv sync` without `--locked` where reproducibility matters | `uv sync --locked` |
| `uv lock --upgrade` routinely | Upgrade intentionally; use `--upgrade-package` for targets |
| Mixing `pip` and `uv` management in one project | Pick one — `uv` |
| `uv pip install` for project deps | `uv add` / `uv sync` for managed projects |
| Hand-editing PEP 723 metadata in scripts | Use `uv add --script` (see [uv-scripts.md](uv-scripts.md)) |

______________________________________________________________________

## 11. Migration Cheatsheet

| From | To |
| ---- | -- |
| `pip install X` | `uv add X` |
| `pip install -r requirements.txt` | `uv add -r requirements.txt` |
| `pip install -r requirements.in` (compile) | `uv pip compile requirements.in -o requirements.txt` |
| `python script.py` | `uv run script.py` |
| `pipx run ruff` | `uvx ruff` |
| `pipx install ruff` | `uv tool install ruff` |
| `pyenv install 3.12` | `uv python install 3.12` |
| `poetry add X` | `uv add X` |
| `poetry install` | `uv sync` |
| `poetry lock` | `uv lock` |
| `python -m venv .venv` | *(not needed)* `uv sync` creates `.venv` |

______________________________________________________________________

## 12. Related References

- [uv.md](uv.md) — execution discipline
- [uv-scripts.md](uv-scripts.md) — PEP 723 standalone scripts
- [uv-python-versions.md](uv-python-versions.md) — version + architecture management
- [project-setup.md](project-setup.md) — project structure and imports
