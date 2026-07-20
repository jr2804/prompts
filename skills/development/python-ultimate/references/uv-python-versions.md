---
name: uv-python-versions
description: Python version and architecture management with uv — install, pin, find, --python flag, direct interpreter paths, and non-default architectures including 32-bit and free-threaded builds.
---

# uv Python Versions Reference

## Table of Contents

- [uv Python Versions Reference](#uv-python-versions-reference)
  - [Table of Contents](#table-of-contents)
  - [1. Installing and Pinning](#1-installing-and-pinning)
  - [2. Discovering Interpreters](#2-discovering-interpreters)
  - [3. Selecting an Interpreter at Run Time](#3-selecting-an-interpreter-at-run-time)
  - [4. Non-Default Architectures: 32-bit Python](#4-non-default-architectures-32-bit-python)
  - [5. Free-Threaded Python (PEP 703)](#5-free-threaded-python-pep-703)
  - [6. Installation Paths](#6-installation-paths)
  - [7. Environment Variables](#7-environment-variables)
  - [8. Troubleshooting](#8-troubleshooting)
  - [9. Related References](#9-related-references)

______________________________________________________________________

## 1. Installing and Pinning

```bash
uv python install              # default version (uv-managed; currently 3.13/3.14 depending on uv release)
uv python install 3.12         # specific minor
uv python install 3.12.6       # specific patch
uv python install 3.11 3.12    # multiple at once

uv python pin 3.12             # writes .python-version in the project
uv python pin 3.12.6           # pin to patch
```

`.python-version` is consulted by every later `uv run` in that directory, so
pinning once is enough — no need to repeat `--python` on every command.

______________________________________________________________________

## 2. Discovering Interpreters

```bash
uv python list                 # all available (downloadable + installed)
uv python list --installed     # only installed locally
uv python find 3.12            # absolute path to the resolved interpreter
uv python find 3.12 --verbose  # resolution detail
```

`uv python find` is the canonical way to learn where an interpreter lives —
do not guess paths.

______________________________________________________________________

## 3. Selecting an Interpreter at Run Time

```bash
uv run --python 3.12 script.py                         # by version
uv run --python 3.12.6 script.py                       # by patch
uv run --python /path/to/python script.py              # by direct path
uv run --directory /path/to/project --python 3.12 s.py # with working dir
```

For PEP 723 scripts, `requires-python` constrains the lower bound but does not
override the `--python` flag — pass `--python` explicitly for any non-default
selection.

______________________________________________________________________

## 4. Non-Default Architectures: 32-bit Python

**`uv` does not ship 32-bit CPython interpreters.** Astral's
`python-build-standalone` builds — which `uv python install` uses — target
`x86_64` on Windows, `x86_64`/`aarch64` on Linux and macOS. There is no
`windows-i686` (32-bit) build available through `uv`.

> Note: uv 0.9.7 release notes mention "Windows x86-32 support," but that refers
> to running the **`uv` binary** on 32-bit Windows. It does **not** mean `uv`
> ships a 32-bit Python interpreter.

### The workaround

Use a **system-installed 32-bit Python** as the interpreter, referenced by path:

```bash
# 1. Install Python 3.11 (32-bit) from python.org — the official installer
#    offers a "32-bit only" download. Default path on Windows:
#       C:\Users\<user>\AppData\Local\Programs\Python\Python311-32\python.exe
#    or, for all-users installs:
#       C:\Program Files (x86)\Python311-32\python.exe

# 2. Point uv at it explicitly.
uv run --python "C:\Program Files (x86)\Python311-32\python.exe" script.py

# 3. Or discover it from a script's working directory with a pinned version file.
uv python pin 3.11.9   # then ensure the system 32-bit interpreter satisfies it
```

### Pinning without `uv`-managed builds

For projects that must run on 32-bit:

1. Install the 32-bit interpreter once via the official installer.
2. Reference it explicitly with `uv run --python <path>` in every command, or
3. Set `UV_PYTHON_INSTALL_DIR` to a directory you populate manually (rare; only
   useful if you maintain your own 32-bit python-build-standalone fork).
4. Document the requirement in the project README — `.python-version` alone
   cannot express architecture.

### Verifying the architecture from inside Python

```python
import platform, struct

print(platform.architecture())   # ('32bit', 'WindowsPE') or ('64bit', 'WindowsPE')
print(struct.calcsize('P') * 8)  # 32 or 64 — bits per pointer
```

### Working example

See [`examples/uv_script_32bit.py`](../examples/uv_script_32bit.py) for a
PEP 723 script that targets Python 3.11 specifically and documents the 32-bit
interpreter invocation in its module docstring.

______________________________________________________________________

## 5. Free-Threaded Python (PEP 703)

Free-threaded (no-GIL) CPython is available from `uv` for Python 3.13+ via the
`+freethreaded` qualifier:

```bash
uv python install 3.14t
uv run --python 3.14t script.py
uv python pin 3.14t
```

Rules:

- Free-threaded builds are experimental; pin them deliberately, not by default.
- Pure-Python dependencies work; C extensions must be free-threaded-compatible
  or they will fail to import.
- Verify the build at runtime: `import sys; sys._is_gil_enabled()` returns
  `False` on a free-threaded interpreter.

______________________________________________________________________

## 6. Installation Paths

`uv`-managed interpreters live in platform-specific locations:

| Platform | Path |
| -------- | ---- |
| Linux | `~/.local/share/uv/python/cpython-<version>-<platform>/bin/python3` |
| macOS | `~/.local/share/uv/python/cpython-<version>-<platform>/bin/python3` |
| Windows | `%LOCALAPPDATA%\uv\python\cpython-<version>-<platform>\python.exe` |

Resolve with `uv python find` rather than hard-coding paths — the layout can
change across `uv` releases.

______________________________________________________________________

## 7. Environment Variables

| Variable | Effect |
| -------- | ------ |
| `UV_PYTHON_INSTALL_DIR` | Override the managed-Python install directory |
| `UV_PYTHON_PREFERENCE` | `only-managed` / `only-system` / `managed` / `system` |
| `UV_PROJECT_ENVIRONMENT` | Override `.venv` location |
| `UV_CACHE_DIR` | Override cache directory (see [uv.md §4](uv.md)) |

For 32-bit workflows, `UV_PYTHON_PREFERENCE=only-system` plus an explicit
`--python <path>` is the most reliable combination.

______________________________________________________________________

## 8. Troubleshooting

| Symptom | Cause | Fix |
| ------- | ----- | --- |
| `Python 3.x not found` | Not installed via `uv` or system | `uv python install 3.x`, or pass `--python <path>` |
| Wrong interpreter executes | Multiple Pythons on PATH | `uv python pin`, or `uv run --python <version>` |
| `Requires Python >=3.11 but found 3.10` | `requires-python` not satisfied | `uv python install 3.11`; then `uv run --python 3.11` |
| No 32-bit interpreter available from `uv python install` | By design — uv ships x86_64 only | Install system 32-bit Python, use `--python <path>` (see [§4](#4-non-default-architectures-32-bit-python)) |
| C extension fails to import under `3.14t` | Extension not free-threaded-compatible | Drop the `t` qualifier, or rebuild the extension |

______________________________________________________________________

## 9. Related References

- [uv.md](uv.md) — execution discipline
- [uv-scripts.md](uv-scripts.md) — PEP 723 standalone scripts
- [uv-projects.md](uv-projects.md) — project workflow
- [project-setup.md](project-setup.md) — project structure
