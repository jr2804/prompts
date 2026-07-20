---
name: uv-scripts
description: PEP 723 standalone Python scripts managed exclusively through uv — init/add/remove/lock --script, agentic script design rules, and scripts-vs-projects boundary.
---

# uv Standalone Scripts Reference (PEP 723)

## Table of Contents

- [uv Standalone Scripts Reference (PEP 723)](#uv-standalone-scripts-reference-pep-723)
  - [Table of Contents](#table-of-contents)
  - [1. The Iron Rule](#1-the-iron-rule)
  - [2. Core Workflow](#2-core-workflow)
  - [3. PEP 723 Block Syntax](#3-pep-723-block-syntax)
  - [4. Running Scripts](#4-running-scripts)
  - [5. Locking Scripts for Reproducibility](#5-locking-scripts-for-reproducibility)
  - [6. Scripts vs Projects](#6-scripts-vs-projects)
  - [7. Agentic Script Design](#7-agentic-script-design)
  - [8. Working Example](#8-working-example)
  - [9. Troubleshooting](#9-troubleshooting)
  - [10. Related References](#10-related-references)

______________________________________________________________________

## 1. The Iron Rule

**Never hand-write and never hand-edit PEP 723 inline metadata.**

Manage the metadata block exclusively through `uv`:

- Create it with `uv init --script`.
- Add dependencies with `uv add --script`.
- Remove dependencies with `uv remove --script`.

You may freely edit the Python *code* in the script. You may not edit the
`# /// script ... # ///` block by hand. Patching TOML by hand risks malformed
metadata, broken dependency specifiers, and silent version drift; the `uv`
commands validate and rewrite the block atomically.

```python
# BAD — author wrote this by hand. Drift, typos, and omissions are likely.
# /// script
# dependencies = ["requests"]
# ///

# GOOD — generated and maintained by `uv init --script` / `uv add --script`.
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests>=2.32,<3",
# ]
# ///
```

______________________________________________________________________

## 2. Core Workflow

For a new standalone script:

```bash
# 1. Initialize the script (creates the PEP 723 header on disk).
uv init --script path/to/script.py

# 2. Add dependencies.
uv add --script path/to/script.py requests
uv add --script path/to/script.py "pandas>=2.0,<3"

# 3. Remove a dependency.
uv remove --script path/to/script.py requests

# 4. Run it.
uv run path/to/script.py
```

Use `uv init --script` **even when the script already exists conceptually** and
only needs to be created on disk. It is the only supported way to bootstrap the
PEP 723 header.

If the correct `uv init` / `uv add` / `uv run` flags are unclear, use
`uv help init`, `uv help add`, or `uv help run` rather than guessing.

______________________________________________________________________

## 3. PEP 723 Block Syntax

The block must appear before any code, framed by exact markers:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests>=2.32,<3",
#     "rich>=13.0",
# ]
# ///
```

**Exact rules** (enforced by `uv`, broken by hand-editing):

- The opening line is exactly `# /// script` — no extra text.
- Every line inside the block starts with a hash followed by a space.
- The body is TOML: `dependencies` is a list of PEP 508 specifiers,
  `requires-python` is a version specifier.
- The closing line is exactly `# ///`.

Optional fields:

| Field | Purpose |
| ----- | ------- |
| `requires-python` | Constrain interpreter version (e.g. `">=3.11,<3.12"`) |
| `dependencies` | List of PEP 508 specifiers |
| `tool.uv.*` | uv-specific settings (mirrors `[tool.uv]` in `pyproject.toml`) |

______________________________________________________________________

## 4. Running Scripts

```bash
# Install declared deps and run.
uv run script.py

# Pass arguments to the script.
uv run script.py arg1 --flag value

# Run with a specific Python version (overrides requires-python lower bound
# only if compatible; use an explicit version for arch overrides).
uv run --python 3.11 script.py

# Run from anywhere with uvx (still reads PEP 723 metadata).
uvx /path/to/script.py
```

First run downloads and caches dependencies; subsequent runs are near-instant.

For non-default architectures (e.g. 32-bit Python), see
[uv-python-versions.md](uv-python-versions.md).

______________________________________________________________________

## 5. Locking Scripts for Reproducibility

For full reproducibility, generate a companion lockfile:

```bash
uv lock --script path/to/script.py
```

This writes `path/to/script.py.lock` next to the script. Commit both files when
the script must produce identical output over time. Without a lockfile, `uv`
re-resolves on every run against the latest specifiers.

______________________________________________________________________

## 6. Scripts vs Projects

| Use a standalone script when… | Use a project when… |
| ----------------------------- | ------------------- |
| Single-file utility or automation | Multiple modules / packages |
| Quick data analysis or one-off task | Application with `src/` layout |
| Shareable example that "just runs" | Separate dev/test dependencies |
| CLI that fits in one file | Build/publish a package |

If the task involves a full Python project with `pyproject.toml`, use the
project-oriented workflows in [uv-projects.md](uv-projects.md) instead of the
script commands above. The two modes are mutually exclusive for a given file.

______________________________________________________________________

## 7. Agentic Script Design

Standalone scripts are frequently executed by agents in non-interactive shells.
Apply these rules to any script that may be invoked by an agent:

- **No interactive prompts.** Never block on `input()`, password dialogs, or
  confirmation menus. Accept all input via flags, env vars, or stdin. A script
  that waits for a TTY will hang indefinitely in an agent shell.
- **Provide `--help`.** It is the primary way an agent learns the interface.
  Include a brief description, all flags, and a usage example.
- **Write helpful errors.** `"Error: --format must be one of: json, csv, table. Received: \"xml\""` beats `"invalid input"`.
- **Prefer structured output.** JSON / CSV / TSV on stdout; diagnostics on
  stderr. This makes the script composable in pipelines.
- **Idempotency.** Agents retry. "Create if not exists" beats "create and fail
  on duplicate."
- **Meaningful exit codes.** Distinct codes for distinct failures
  (not found, invalid args, auth failure), documented in `--help`.
- **Predictable output size.** Default to a summary or cap output; offer an
  `--offset`/`--limit` flag or an `--output FILE` option. Agent harnesses
  truncate beyond ~10–30K characters.

______________________________________________________________________

## 8. Working Example

See [`examples/uv_script_32bit.py`](../examples/uv_script_32bit.py) for a complete
standalone script that:

- Declares dependencies and `requires-python` via PEP 723 (created with
  `uv init --script`).
- Targets Python 3.11 specifically (`requires-python = ">=3.11,<3.12"`).
- Documents the workaround for running on a **32-bit** interpreter, which `uv`
  does not ship (see [uv-python-versions.md](uv-python-versions.md)).

______________________________________________________________________

## 9. Troubleshooting

| Symptom | Cause | Fix |
| ------- | ----- | --- |
| `Failed to parse inline script metadata` | Block syntax broken (often by hand-editing) | Regenerate via `uv add --script`; do not hand-patch |
| `Package 'X' not found on PyPI` | Misspelled package name | Verify name on PyPI; re-run `uv add --script` |
| `Unable to resolve dependencies` | Conflicting version specifiers | Loosen specifiers; check PEP 508 syntax |
| `Requires Python >=3.11 but found 3.10` | `requires-python` not satisfied | `uv python install 3.11`, then `uv run --python 3.11 script.py` |
| First run is slow | Network download of dependencies | Expected; subsequent runs use the cache |
| Cache write fails in sandbox | Default cache dir not writable | Set `UV_CACHE_DIR` (see [uv.md §4](uv.md)) |

______________________________________________________________________

## 10. Related References

- [uv.md](uv.md) — execution discipline (`uv run`, never bare `python`)
- [uv-projects.md](uv-projects.md) — project workflow
- [uv-python-versions.md](uv-python-versions.md) — version + architecture management
- [project-setup.md](project-setup.md) — project structure
