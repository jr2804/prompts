# Ruff Linter Rules Reference

## Table of Contents

- [Overview](#overview)
- [Which Tool Enforces What](#which-tool-enforces-what)
- [Gate design](#gate-design)
  - [Make the vacuous pass unrepresentable](#make-the-vacuous-pass-unrepresentable)
  - [A passing verdict is not evidence of a scan](#a-passing-verdict-is-not-evidence-of-a-scan)
  - [Level 0: who decides where the facts come from](#level-0-who-decides-where-the-facts-come-from)
  - [When zero is an honest answer](#when-zero-is-an-honest-answer)
  - [Facts from different places need different lifetimes](#facts-from-different-places-need-different-lifetimes)
    - ["Can I resolve this?" is per item, not per map](#can-i-resolve-this-is-per-item-not-per-map)
  - [Prose is not enforcement](#prose-is-not-enforcement)
    - [A guard that cannot fail for the reason it names](#a-guard-that-cannot-fail-for-the-reason-it-names)
  - [Fatal at the right scope, not the earliest scope](#fatal-at-the-right-scope-not-the-earliest-scope)
    - [The precondition must match the subject set](#the-precondition-must-match-the-subject-set)
- [E402: Module Level Import Not at Top of File](#e402-module-level-import-not-at-top-of-file)
- [B007: Loop Control Variable Not Used](#b007-loop-control-variable-not-used)
- [B008: Function Call in Default Argument](#b008-function-call-in-default-argument)
- [S108: Hardcoded Temp File](#s108-hardcoded-temp-file)
- [PLC0415: Import Outside Top-Level](#plc0415-import-outside-top-level)
- [PLW0603: Global Statement](#plw0603-global-statement)
- [NPY002: Legacy NumPy Random Generation](#npy002-legacy-numpy-random-generation)
- [S311: Suspicious Non-Cryptographic Random Usage](#s311-suspicious-non-cryptographic-random-usage)
- [Typer CLI Exception for B008](#typer-cli-exception-for-b008)
- [General Fix Strategy](#general-fix-strategy)

______________________________________________________________________

## Overview

Ruff is a fast Python linter written in Rust that identifies issues following PEP 8 and other best practices. It provides context-aware fixes that distinguish between production code, test code, and CLI frameworks.

When fixing linter errors:

1. Identify the rule code from the linter output
2. Select the appropriate fix pattern based on your code's context
3. Apply the fix and verify it resolves the issue without introducing new problems

______________________________________________________________________

## Which Tool Enforces What

Do not write a custom checker for something a configured linter already
reports. Every rule below has a native owner; enable that rule instead of adding
a script that re-implements it.

| Rule | Enforced by | Configure instead of scanning |
| --- | --- | --- |
| `global` statement | `PLW0603` | Yes |
| Blanket `# noqa` | `PGH004` | Yes |
| Unused `# noqa` | `RUF100` | Yes |
| `os.path` usage | `PTH` | Yes |
| `Optional[T]` | `UP045` | Yes |
| Inline / function-level imports | `PLC0415` | Yes |
| `TYPE_CHECKING` guards | `TCH` (flake8-type-checking) | Yes |
| Bare `python` invocations | `S603`/`S607` partially; review manually | No |
| `sys.path` manipulation | — | Manual review |

Two rules have no honest linter equivalent and live in a shipped scanner instead:

| Rule | Why a linter cannot express it | Scanner |
| --- | --- | --- |
| `IMPORT-ERROR-GUARD` | Needs the dependency declaration (PEP 723 block or `pyproject.toml`) to decide whether the guard is dead weight or a legitimate optional probe | `assets/check_antipatterns.py` |
| `BANNED-NOQA` | A project may ban specific suppression codes (`# noqa: PLW0603`) while allowing others; Ruff only reports unused or blanket noqa | `assets/check_antipatterns.py --ban-noqa CODE` |

```bash
# Everything a linter covers: let the linter do it.
uvx ruff check --select PLW0603,PGH004,RUF100,PTH,UP045,PLC0415,TCH .

# Only the two rules a linter cannot express:
uv run assets/check_antipatterns.py src --ban-noqa PLW0603
```

The scanner exits `0` clean, `1` on findings, and `2` when the scan itself was
invalid. Exit `2` is not a pass — it means the tool could not establish the facts
the rules depend on:

- no Python files were discovered under the given paths
- a path argument does not exist, or `--project-root` names a directory with no
  `pyproject.toml` — skipping either would silently narrow the scan
- a file could not be read, parsed, or tokenized
- a PEP 723 `dependencies` block, or the project's `pyproject.toml`, could not be
  parsed (an unreadable block would silently exempt every guard in that file)
- a `pyproject.toml` has no `[project]` table, so it declares no dependencies at
  all (a workspace root is a normal shape; judging guards against it invents
  facts). An empty `dependencies = []` list is different and honest
- a guard imports a module whose dependency status could not be established
  because `importlib.metadata` returned no import→distribution map, so an alias
  (`PIL` → `Pillow`) cannot be matched. Scoped per module, not per scan: literal
  matches still work and PEP 723 scripts never need the map, so making an empty
  map fatal everywhere would reject honest runs
- `--ban-noqa` names a code Ruff does not define, so the ban could never match

A gate that read nothing and a gate that read everything and found nothing look
identical in the exit code. Whenever a scanner gains an input layer, it must
assert that the layer was actually read.

## Gate design

The rules in this section apply to any script whose exit code is a verdict: a
validator, a scanner, a consistency check, a parity gate. Each was found the
hard way — a gate that exited `0` while judging nothing, or exited `2` while
rejecting honest input.

### Make the vacuous pass unrepresentable

Exit `2` is a runtime contract; the stronger fix is to make the mistake
impossible to express. Empty is a *valid* value for a findings list and also the
value a failure path wants to return, so `except ...: return []` reads like
robustness while switching the rule off. Prefer these shapes, in order:

1. **Required coverage sink.** `scan_file(path, errors: list[str])` — no default
   for the parameter that carries failures. A caller who forgets it gets a type
   error (`missing-argument`), not a vacuous pass. An `errors: list[str] | None
   = None` default is the bug: it is the option to drop coverage, and some call
   site will take it.
2. **One implementation, plain accessor delegates.** When a gate needs both a
   result and a result-with-coverage, `scan(x)` should be
   `return scan_with_coverage(x).violations`. Never let the two be siblings —
   duplicated coverage plumbing is exactly what rots. Prefer this over widening
   the old return type, because existing assertions written as `== []` compare a
   dataclass to a list, evaluate to `False`, and go on passing silently.
3. **Explicit failure value.** Return `tuple[list[Violation], str | None]` and
   let the caller turn a non-`None` error into exit `2`, rather than raising
   through a loop that also collects real findings. This is a concession, not an
   equal option: the caller can still ignore the error, so it only holds while
   you can point at the `if error is not None: return 2` at every call site.
   Prefer an exception where it fits — the type checker then does the work — and
   reach for this shape only when partial results must be yielded before a
   failure, which a raised exception cannot express.

The narrow entry point should have no failure channel at all where possible. If
its only caller needing coverage calls the covered variant directly, the failure
channel exists exactly once, on the one path that checks it.

Coverage has three faces, and each needs its own exit `2`: **input** (nothing
was scanned), **facts** (a config or source file that grounds the rules could
not be read), **errors** (a file failed mid-scan).

There is a fourth face that is easier to miss: **derived facts**. The input files
read fine, but what the gate *derived* from them came back empty — a dependency
set from a `pyproject.toml` with no `[project]` table, a glob that matched
nothing, a query that returned no rows. No exception is involved, so there is
nothing to swallow and nothing for a grep to find. Every such gate needs
`require_facts(count, what, remedy)` next to its `require_scanned(...)`.

A fifth face is **fabricated facts**: a default substituted for an absent fact
becomes an asserted fact, and the assertions built on it are wrong rather than
missing. This one exits `0` with a confident report, so neither counting nor
emptiness checks catch it. See [Facts from different places need different
lifetimes](#facts-from-different-places-need-different-lifetimes).

The optionality does not have to live in a parameter default. A silent guard is
the same defect wearing different clothes:

```python
if not root.is_dir():
    continue        # a typo in one --src silently narrows the scan
```

Anything that reduces coverage without raising is the bug, whether that is a
keyword argument that defaults to `None` or an `if` that quietly skips a path.
Grep for `errors.*\| None` finds the first kind; the second needs the question
below.

A grep audit finds only the first shape — swallowed errors. It cannot find a
vacuous pass caused by a migration that emptied the input, because there is no
error to swallow. Ask instead: *what does this gate read, and can that set be
empty in a healthy repo?*

### A passing verdict is not evidence of a scan

Three failure modes reach exit `0` while judging nothing, and all three are
cheap to test because each is one input made empty:

| Empty this | And the gate concludes |
| --- | --- |
| the file set | everything it found is clean |
| the derived facts | every rule has nothing to contradict |
| the comparison set | parity, completeness, no gaps |

The third is the quietest. A parity check that compares an empty CLI surface
against an empty tool list prints **"Full Parity achieved!"** — a phrase that
reads as a result rather than as the absence of one. And the counts that would
betray it are usually printed: `0 config defaults`, `0 enum(s) reachable`. A
summary line is part of the gate's contract, so if a count can legitimately be
zero, the gate must decide what zero *means* instead of leaving that to the
reader. `0 violation(s) in 0 file(s), 91 scanned` makes a clean run look like a
scan that read nothing, because two different zeros sit side by side without
saying which is which — name them (`0 file(s) with findings, 91 file(s)
scanned`).

A documented post-mortem does not close the class. A parity gate can carry a
comment describing an earlier vacuous pass and still have one, because the
lesson learned was "use the public API" rather than "assert you got something".
Fix the instance *and* add the assertion.

### Level 0: who decides where the facts come from

Absence failures are testable by emptying an input. Identity failures are not:
the gate returns something *confident and wrong*. The question is not "which
project am I looking at" but **who decides** — the caller (`cwd`, environment
variables, a config path) or the scanner itself (its own `__file__`, its own
package).

- A **caller-derived** fact source needs a `None`-and-exit. A fallback such as
  `return Path.cwd()` in a project-root lookup converts "I do not know" into a
  confident wrong answer, and the verdict then changes depending on where you
  ran it from.
- A **self-derived** source is safe by construction, because `cd` cannot relocate
  it.

So prefer identity derived from what the scanner owns. Test it by running the
scanner from an unrelated directory and asserting that the verdict does *not*
change for an absolute target — and that a tree with no facts still exits `2`
rather than borrowing the caller's.

### When zero is an honest answer

Zero dependencies can be a legitimate result or a broken scan, and only the
input's shape tells you which:

- `[project]` with `dependencies = []` — honest: the project really declares
  none, so a guard around a third-party module is genuinely undeclared.
- `[build-system]` only, no `[project]` table — a normal *virtual* workspace root
  (`[tool.uv.workspace]` with members, no package of its own) that declares no
  dependencies because the question does not apply there. Treating this as
  "zero facts established" is wrong in the other direction.

A `require_facts` guard that only counts will reject the second case. Check the
shape first, then count.

### Facts from different places need different lifetimes

A bug I shipped and then found twice in the same file: one optional object
holding facts with **different provenance**. `DependencyFacts` bundled project
declarations (from `pyproject.toml`, may be absent) with the import-to-distribution
index (from the installed environment, always available). When the project half
was absent the caller passed `facts or DependencyFacts(frozenset(), frozenset(), {})`
— which emptied the environment half too, because `{}` was not a placeholder, it
was a fact.

The symptom was a false *negative*: with no `pyproject.toml`, `from PIL import
Image` could not be matched to a declared `pillow`, so the guard looked like an
undeclared optional probe and was exempted. Exit `0`, clean report, real finding
dropped. The same empty map had already caused a false *positive* one commit
earlier, where it was treated as fatal per file. One fabricated fact, both
directions of wrong.

The fix is not a better default — it is to stop sharing the lifetime. The
resolver is built unconditionally and passed separately from the optional
project facts.

Generalise: if two facts have different sources, they have different failure
modes, and combining them into one optional value makes the available fact
inherit the absent one's absence. Pass them separately, and let each be
optional only where it genuinely can be.

#### "Can I resolve this?" is per item, not per map

Second-order version of the same error, in the guard that replaced it.
`has_resolver()` asked whether *any* distributions were visible. A test
environment with `ruff` installed and `pillow` absent therefore answered "yes"
— and `PIL` was silently exempted again, because a non-empty map was offered as
proof that one particular name was mappable.

The sharper question is whether an alias could be hiding *this* module, and the
evidence decides it: if every declared dependency is present among the installed
distributions, then no declared dependency can be behind an unmapped import name,
so the guard is a genuine probe. Only a declaration that is itself missing from
the environment leaves the alias unprovable.

That distinction is what keeps a bare CI environment from flagging honest probes
of undeclared accelerators such as `orjson`. A blunter "is the map empty?" test
failed in one direction or the other on every attempt.

### Prose is not enforcement

The rules above are documentation, and documentation does not fail a build. A
future edit can move a guard back to `main()`, widen a coverage parameter to
`| None`, or let an unreadable file count as clean, and every existing check
still passes.

Pin the contract with a test that asserts both halves:

- every documented exit-`2` cause really exits `2` — a cause that regresses to
  `0` is a vacuous pass again;
- **honest runs still pass** — this is the half that is usually missing, and it
  is the only thing that catches over-guarding. Absence is easy to test by
  emptying an input; the damage a fix does to correct runs is only visible by
  asserting the complementary case for every fact your guard can declare
  missing.

A guard whose contract is checked in only one direction is half-tested, and the
untested direction is the one where a *fix* introduces the next bug. A suite of
only failure cases is satisfied by a gate that always fails; a suite of only
success cases is satisfied by one that always passes. Each half is what makes
the other mean anything.

Check the guard's *coverage* in both directions too, against the call sites
rather than against a list someone maintains:

| Direction | Registers as |
| --- | --- |
| a case missing for an existing call site | missing |
| a case naming a call site that no longer exists | stale |

#### A guard that cannot fail for the reason it names

The subtlest form, because it passes review: a coverage test asserting each
call site is *imported* by some test. That holds when the import is used only to
call `main()` against real facts, so the test cannot fail for emptiness — the
very defect it was written to prevent. Before trusting a new guard, ask what
input makes it fail, and confirm that input actually reaches it.

### Fatal at the right scope, not the earliest scope

The reflex after finding an empty fact set is to guard it as early as possible,
so the failure cannot be missed. Wrong axis. A guard may only be scoped to the
set of **judgments that consume its fact** — not to the run that contains them.

One rule, three incidents, each caught separately before the rule was named:

| Guard | Placed at | Subject set it wrongly covered |
| --- | --- | --- |
| alias map required (exit 2) | `main()` | files that resolve an import literally, and PEP 723 scripts |
| project facts required (exit 2) | `main()` | PEP 723 scripts, which read their own `dependencies` |
| fact-may-not-be-empty | a call site whose fact can honestly be empty | the call site itself |

Guarding "the run" is tempting because `main()` is where errors are easy to
raise, and because an empty dependency map *feels* like a global input. It is
not: the fact's scope is a property of each rule, not of the scanner. Ask which
judgments read the fact, and fail inside those.

A missing fact should fail the judgments that depend on it, and a scan whose
judgments never touch it should pass. Early guarding is only safer when the fact
really is global input.

#### The precondition must match the subject set

The precise version, because it names the bug rather than the symptom: a guard
attached to a subject set containing members the precondition does not apply to
will reject those members. ``main()``'s subject set is "everything in this run",
and a scripts-only tree contains no member for which project dependency facts
are needed — so a guard there rejects valid input instead of protecting it.

When a precondition becomes true of only *some* subjects, scope it to the
predicate that selects them, not to the scope that happens to be convenient.

______________________________________________________________________

## E402: Module Level Import Not at Top of File

**Rule Code:** E402

**Description:** An import statement appears after code that is not an import, comment, or docstring.

**Problem Pattern:** Imports placed after executable code in a module.

**Fix Pattern:** Keep module-level imports at the top by default, grouped by standard library, third-party, then local imports. Follow [canonical import guidance](imports-optional-dependencies.md) for justified local imports.

**Example:**

```python
# BEFORE (linter error)
def get_platform():
    import platform  # Error: import after code

    return platform.system()


# AFTER (fixed)
import platform


def get_platform():
    return platform.system()
```

______________________________________________________________________

## B007: Loop Control Variable Not Used

**Rule Code:** B007

**Description:** A variable defined in a `for` loop is never used within the loop body.

**Problem Pattern:** Loop variables that are never referenced after assignment.

**Fix Pattern:** Prefix unused loop variables with an underscore (`_`) to indicate intentional non-use. See [naming-conventions.md](naming-conventions.md) for complete guidelines.

**Example:**

```python
# BEFORE (linter error)
for item in items:
    process_items()  # 'item' never used

# AFTER (fixed)
for _ in items:
    process_items()
```

______________________________________________________________________

## B008: Function Call in Default Argument

**Rule Code:** B008

**Description:** A function call is used as a default argument value, evaluated only once at function definition time.

**Problem Pattern:** Mutable or dynamic return values captured at module load time instead of call time.

**Fix Pattern:** Use `None` as default and initialize inside the function body.

**Example:**

```python
# BEFORE (linter error)
def create_list():
    return [1, 2, 3]


def process_data(items: list[int] = create_list()):
    items.append(4)
    return items


# AFTER (fixed)
def process_data(items: list[int] | None = None):
    if items is None:
        items = create_list()
    items.append(4)
    return items
```

______________________________________________________________________

## S108: Hardcoded Temp File

**Rule Code:** S108

**Description:** Hardcoded paths like `/tmp/`, `/var/tmp/`, or `C:\Temp\` for temporary files.

**Problem Pattern:** Using predictable temporary file paths instead of secure, platform-appropriate alternatives.

**Fix Pattern (Production):** Use `tempfile.NamedTemporaryFile` with `delete=False`.

**Fix Pattern (Test):** Use pytest's `tmp_path` fixture.

**Example - Production:**

```python
# BEFORE (linter error)
with open("/tmp/data.txt", "w") as f:
    f.write(data)

# AFTER (fixed)
import tempfile

with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
    f.write(data)
    temp_path = f.name
```

**Example - Test:**

```python
# BEFORE (linter error)
def test_file_processing():
    test_file = "/tmp/test_data.txt"
    with open(test_file, "w") as f:
        f.write("test")


# AFTER (fixed)
def test_file_processing(tmp_path: Path):
    test_file = tmp_path / "test_data.txt"
    test_file.write_text("test")
```

______________________________________________________________________

## PLC0415: Import Outside Top-Level

**Rule Code:** PLC0415

**Description:** Import statements placed inside functions, methods, or class definitions instead of at module level.

**Problem Pattern:** Imports buried within function bodies, making dependencies unclear.

**Fix Pattern:** Prefer module-level imports; see [canonical import guidance](imports-optional-dependencies.md) for justified local imports.

**Example:**

```python
# BEFORE (linter error)
def print_version():
    import platform

    print(platform.python_version())


# AFTER (fixed)
import platform


def print_version():
    print(platform.python_version())
```

**Standard Import Organization:**

```python
# 1. Standard library imports
import os
import sys
from pathlib import Path

# 2. Third-party imports
import typer
from rich.console import Console

# 3. Local application imports
from .utils import helpers
from .core import processors
```

______________________________________________________________________

## PLW0603: Global Statement

**Rule Code:** PLW0603 (`global-statement`)

**Description:** A function uses the `global` statement to rebind a
module-level name.

**Problem Pattern:** Treating a module-level variable as mutable shared state.

**Fix Pattern:** **Never fix this by suppressing it.** `# noqa: PLW0603` and
disabling the rule are both forbidden — the finding always indicates a design
problem. Replace the shared variable with explicit state:

- **Changing value** → return the new value, or hold it on an object that is
  passed in (`self._next += 1`).
- **Read-only value computed once** → a `@functools.cache` getter returning a
  frozen value.
- **Temporary context** → an explicit parameter or a small dataclass passed
  through the call chain.

**Example:**

```python
# WRONG
_cache: dict[str, str] = {}


def load(name: str) -> str:
    global _cache  # PLW0603
    if name not in _cache:
        _cache[name] = name.upper()
    return _cache[name]


# RIGHT — module variable becomes a cached getter result
from functools import cache


@cache
def load(name: str) -> str:
    return name.upper()
```

**Related:** [Module State and Globals](module-state.md) covers the full
rationale, mutability checks for module-level containers, and the
module-constant-table rules.

______________________________________________________________________

## NPY002: Legacy NumPy Random Generation

**Rule Code:** NPY002

**Description:** Usage of legacy `numpy.random` functions (`np.random.seed`, `np.random.normal`) instead of the modern `Generator` API.

**Problem Pattern:** Using frozen `RandomState` methods with global state and poorer statistical properties.

**Fix Pattern:** Use `numpy.random.default_rng()` for the modern `Generator` API.

**Example:**

```python
# BEFORE (linter error)
import numpy as np

np.random.seed(1337)
data = np.random.normal(size=100)

# AFTER (fixed)
import numpy as np

rng = np.random.default_rng(1337)
data = rng.normal(size=100)
```

______________________________________________________________________

## S311: Suspicious Non-Cryptographic Random Usage

**Rule Code:** S311

**Description:** Standard `random` module used in potentially sensitive contexts where cryptographic security is needed.

**Problem Pattern:** Using predictable pseudo-random generators for security-sensitive values.

**Fix Pattern (Security Context):** Use `secrets` module for tokens, passwords, or authentication.\
**Fix Pattern (Non-Security Context):** Use NumPy's `default_rng()` for better performance.

**Example - Security Context:**

```python
# BEFORE (security risk)
import random

token = random.randrange(1000000)

# AFTER (secure)
import secrets

token = secrets.randbelow(1000000)
```

**Example - Non-Security Context:**

```python
# Use NumPy for simulation/data analysis
import numpy as np

rng = np.random.default_rng()
data = rng.random(100)
```

______________________________________________________________________

## Typer CLI Exception for B008

When using `typer.Option()` or `typer.Argument()`, function calls in defaults are **intentional and required**. Apply this special annotation pattern instead of fixing B008:

```python
from typing import Annotated
import typer


def main(
    config: Annotated[
        str, typer.Option(help="Configuration file path")
    ] = "config.yaml",
) -> None:
    """CLI command with proper Typer annotations."""
    ...
```

**Key Pattern:** Use `Annotated` with `typer.Option`/`typer.Argument`, keeping the default value on the parameter itself.

______________________________________________________________________

## General Fix Strategy

| Context | Recommended Approach |
|---------|---------------------|
| **Production Code** | Use `tempfile` module for temp files, `secrets` for security |
| **Test Code** | Use pytest fixtures (`tmp_path`) for temp files |
| **CLI (Typer)** | Use `Annotated` pattern, do not fix B008 |
| **Data Science** | Prefer NumPy `default_rng()` over standard `random` |
| **Imports** | Module level by default; see [canonical import guidance](imports-optional-dependencies.md) for exceptions |
| **Global State** | Never suppress PLW0603; use explicit state or a `@cache` getter ([module state](module-state.md)) |

**When in doubt:**

1. Production vs Test: Choose based on module location and purpose
2. Security vs Non-Security: Default to `secrets` for any token, password, or key generation
3. Typer B008: Preserve the pattern, do not apply standard B008 fix
4. NumPy Random: Always prefer `default_rng()` for new code

**Reference:** [Ruff Full Rule Index](https://docs.astral.sh/ruff/rules/)
