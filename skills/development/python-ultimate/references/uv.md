---
name: uv
description: Execution discipline for running Python through uv — never bare python/python3, always uv run, with sandboxing and on-sight translation rules.
---

# uv Execution Discipline Reference

## Table of Contents

- [uv Execution Discipline Reference](#uv-execution-discipline-reference)
  - [Table of Contents](#table-of-contents)
  - [1. The Iron Rule](#1-the-iron-rule)
  - [2. Canonical Execution Patterns](#2-canonical-execution-patterns)
  - [3. Translate-on-Sight](#3-translate-on-sight)
  - [4. Sandboxing with UV_CACHE_DIR](#4-sandboxing-with-uv_cache_dir)
  - [5. When bare `python` Is Genuinely Required](#5-when-bare-python-is-genuinely-required)
  - [6. Scope Boundary](#6-scope-boundary)
  - [7. Related References](#7-related-references)

______________________________________________________________________

## 1. The Iron Rule

**Always run Python through `uv`. Never call bare `python` or `python3`.**

`uv` is the entrypoint that controls interpreter selection, environment setup, and
dependency resolution. Calling `python` directly bypasses all of it and silently
falls back to whatever interpreter happens to be first on `PATH`.

```bash
# BAD — which interpreter is this? Which deps? Nobody knows.
python script.py
python3 -m pytest
python -c "print('hello')"

# GOOD — uv selects the interpreter, syncs the env, resolves deps.
uv run script.py
uv run -m pytest
uv run python -c "print('hello')"
```

Using `python` *inside* `uv run ...` is correct, because `uv` is still the entrypoint:

```bash
# GOOD — uv is the entrypoint; python is the payload.
uv run python -c "print('hello')"
uv run --with rich python -c "import rich; rich.print('ok')"
```

______________________________________________________________________

## 2. Canonical Execution Patterns

| Task | Command |
| ---- | ------- |
| Run a script | `uv run path/to/script.py` |
| Run a module | `uv run -m package.module` |
| Run a one-liner | `uv run python -c "..."` |
| Run a tool exposed by a dependency | `uv run ruff check .` |
| Run with an ephemeral extra dependency | `uv run --with httpx python -c "..."` |
| Run with a specific Python version | `uv run --python 3.11 script.py` |
| Run with a specific interpreter path | `uv run --python C:\Python311-32\python.exe script.py` |
| Run in a different working directory | `uv run --directory /path/to/dir script.py` |

For Python version selection (including non-default architectures such as 32-bit),
see [uv-python-versions.md](uv-python-versions.md).

______________________________________________________________________

## 3. Translate-on-Sight

When documentation, a README, or a user message shows a bare `python` invocation,
translate it to the closest `uv` form **before executing or writing it into a file**.

| Original | Translated |
| -------- | ---------- |
| `python script.py` | `uv run script.py` |
| `python -m pytest` | `uv run -m pytest` |
| `python -c "..."` | `uv run python -c "..."` |
| `pip install X` | `uv add X` (in a project) or `uv run --with X ...` (ephemeral) |
| `python -m http.server` | `uv run python -m http.server` |

The only exception is when the user explicitly requires a bare interpreter call —
then call out the conflict (see [§5](#5-when-bare-python-is-genuinely-required)).

______________________________________________________________________

## 4. Sandboxing with UV_CACHE_DIR

When operating in a sandboxed or read-only environment where `uv`'s default cache
directory is not writable, set `UV_CACHE_DIR` to a writable temporary directory
before invoking `uv`. Otherwise `uv` will fail on the first network operation or
wheel cache write.

```bash
# POSIX
UV_CACHE_DIR=/tmp/uv-cache uv run script.py

# Windows PowerShell
$env:UV_CACHE_DIR = "$env:TEMP\uv-cache"; uv run script.py

# Windows cmd
set UV_CACHE_DIR=%TEMP%\uv-cache && uv run script.py
```

**Rules:**

- Set `UV_CACHE_DIR` once per shell session; do not prepend it to every command
  in documentation that humans will read.
- If the project already defines its own cache directory (e.g. via `.env` or a
  mise task), prefer that over `/tmp/uv-cache`.
- Combine with `uv run` — never set `UV_CACHE_DIR` and then call bare `python`.

______________________________________________________________________

## 5. When bare `python` Is Genuinely Required

Rare. Valid reasons:

- Bootstrapping `uv` itself before it is installed (`python -m pip install uv`).
- A user explicitly insists on a system-interpreter-only workflow and accepts the
  trade-off. In that case, call out the conflict with this skill in the response,
  do not silently comply.
- Inside an already-activated `uv`-managed venv where `python` is the venv
  interpreter (still prefer `uv run` for consistency).

If you find yourself reaching for `python` because `uv run` "isn't working," that
is a debugging signal — see [debugging.md](debugging.md). Do not paper over it by
switching to bare `python`.

______________________________________________________________________

## 6. Scope Boundary

This reference covers **how to run Python through uv**. It does not cover:

- Installing `uv` itself or running MCP servers with `uvx` — those belong to the
  standalone `uv` skill (`~/.agents/skills/uv`).
- Authoring PEP 723 standalone scripts — see [uv-scripts.md](uv-scripts.md).
- Managing `pyproject.toml` projects — see [uv-projects.md](uv-projects.md).
- Selecting non-default Python versions or architectures — see
  [uv-python-versions.md](uv-python-versions.md).

______________________________________________________________________

## 7. Related References

- [uv-scripts.md](uv-scripts.md) — PEP 723 standalone scripts
- [uv-projects.md](uv-projects.md) — project workflow (init, add, sync, lock)
- [uv-python-versions.md](uv-python-versions.md) — version + architecture management
- [project-setup.md](project-setup.md) — project structure and import organization
- [coding-standards.md](coding-standards.md) — coding rules
