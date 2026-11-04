# Module State, Globals, and Module-Level Constants

Module-level state is seductive because it is the shortest way to make a value
available everywhere. That convenience is exactly the problem: it removes the
need to pass data, and with it the record of who uses and mutates what. This
reference covers the forbidden patterns (global variables, the `global`
statement), the read-only replacement (`functools.cache` getter), and how to
keep module-level constant tables from becoming an unmaintainable, mutable
module header.

## Non-negotiable defaults

- **Never declare a module-level variable that is mutated at runtime.** Pass
  state as parameters, hold it on an object, or return it from a function.
- **Never use the `global` statement.** Ruff flags it as **PLW0603**
  (`global-statement`). Treat that finding as a hard error: **never add
  `# noqa: PLW0603`, never disable the rule**, and never "fix" it by moving
  the mutation into a `dict`, a list, or an attribute on a module object.
- **A value that is expensive to compute and constant for the process lifetime
  is read-only module state — model it as a cached getter**, not as an
  assignable module variable. See [cached getter](#read-only-module-state-use-a-cached-getter).
- **Module-level constant tables are allowed, but must be immutable-looking and
  out of the module header when long.** Large lookup structures live in their
  own module; shared mutable containers are exposed through read-only views.

## Why global variables and `global` are forbidden

The reasons are not stylistic. Each is a concrete failure mode that shows up in
review or in production:

1. **Action at a distance / hidden coupling.** A module variable can be written
   by any function in the process. Reading a function no longer tells you what
   it depends on or what it changes, so a change in one place silently alters
   behavior in another. This is the single biggest source of "why did this
   suddenly break?" bugs, and no type checker can see it.
2. **Import-order and lifecycle dependence.** Module state is initialized during
   import and lives for the whole process. Behavior therefore depends on which
   module is imported first, on import-time side effects, and on values left
   over from earlier calls. Clean teardown is impossible, and "works when run
   alone" differs from "works in the suite/process".
3. **Untestable without monkeypatching.** Injection requires overwriting module
   attributes; leaks between tests make results order-dependent and flaky.
   Concurrent tests cannot isolate it at all.
4. **Not safe under threads, async, or reentrancy.** Two tasks mutating shared
   module state produce races, lost updates, and interleaved partial states.
   `global` also defeats local reasoning: a function that mutates a global is
   not a pure transformation, so it cannot be composed, retried, or run in
   parallel safely.

Global state is also the reason `global`-based singletons, counters, caches, and
"current context" variables keep needing locks, resets, and defensive copies.
Passing the value (or an object that owns it) is almost always shorter in the
end.

## Read-only module state: use a cached getter

For configuration, resolved paths, parsed data files, and other values that are
computed once and then never change, use a zero-argument getter decorated with
[`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache).
This is effectively a **read-only global variable** whose initializer runs
cleanly on first use:

```python
# WRONG — mutable module state, import-time side effects, hidden coupling
import json
from pathlib import Path

CONFIG: dict[str, object] = json.loads(
    Path("config.json").read_text(encoding="utf-8")
)
DEBUG: bool = False


def set_debug(enabled: bool) -> None:
    global DEBUG  # PLW0603 — never do this
    DEBUG = enabled
```

```python
# CORRECT — lazy, read-only, resettable, no `global`
import json
from dataclasses import dataclass
from functools import cache
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Settings:
    debug: bool
    database_url: str


@cache
def get_settings() -> Settings:
    raw = json.loads(Path("config.json").read_text(encoding="utf-8"))
    return Settings(debug=bool(raw["debug"]), database_url=str(raw["database_url"]))


def is_debug() -> bool:
    return get_settings().debug
```

Why this is strictly better than an assignable module variable:

- **Frozen after construction.** `Settings` is a frozen dataclass, so there is
  no API to change it; the only writer is the initializer.
- **Lazy and side-effect free at import.** The file is read on first call, not
  at import time; import order stops affecting behavior.
- **Resettable for tests.** `get_settings.cache_clear()` restores a clean slate
  without touching production code.
- **Initializer code is allowed to be real code.** Validation, environment
  lookup, parsing, and failure with a clear exception all belong inside the
  getter.

Rules for the pattern:

- Use `@cache` for a **zero-argument** getter, or for arguments with a small,
  bounded set of hashable values. `@cache` is `lru_cache(maxsize=None)`:
  unbounded growth for unbounded inputs. Use
  `functools.lru_cache(maxsize=...)` when the inputs can vary widely.
- Arguments must be hashable; if a call site needs an unhashable argument, the
  cache belongs on a helper taking the hashable key, not on the public function.
- Return an immutable value (`frozen=True` dataclass, tuple, `MappingProxyType`)
  or a defensive copy. Returning a shared mutable dict reintroduces the mutation
  problem through the back door.
- Make the initializer idempotent and thread-tolerant: under concurrency the
  cached function may run twice before the first result is stored. Two identical
  builds are fine; two conflicting side effects are not.
- Provide `get_settings.cache_clear()` in test fixtures when tests need
  different configurations (`monkeypatch.setenv(...)` then `cache_clear()`).
- For per-instance laziness use `functools.cached_property` on a class instead;
  module state is then unnecessary altogether.
- Do not wrap a `cache` getter around something that genuinely changes during
  the process (feature flags, live connections, counters). That is state with a
  lifecycle — model it as an object you create and pass, not as module state.

## Module-level constant tables

A module-level mapping such as

```python
CONSTANTS1_VS_CONSTANTS2: dict[str, dict[str, str]] = {
    "alpha": {"label": "Alpha", "unit": "m"},
    "beta": {"label": "Beta", "unit": "kg"},
}
```

is acceptable when it is genuinely a fixed lookup table. Two problems make it
degrade over time:

1. **It pollutes the module header.** Lookup tables grow; a 200-line literal
   between the docstring and the first function hides the actual logic of the
   module and breaks the canonical section order (constants → enums → classes →
   functions).
2. **It is error-prone regarding modification.** The table is one shared mutable
   object: any importer can write into it, and a `.get`-and-mutate pattern turns
   a "constant" into hidden global state. A wrong nested level or a missing key
   is also invisible to the type checker once values are plain `str`.

Apply these rules:

- **Move long tables out of the header.** Put them in a dedicated data module
  (`data/asset_prefixes.py`, `domain/units.py`) and import the name. Keep the
  consuming module readable; keep the data next to the concept it belongs to,
  not in a miscellaneous `constants.py` dump.
- **Make it read-only at runtime.** `Final` only prevents rebinding the name,
  not mutation of the object. Expose a read-only view:
  `MappingProxyType({...})` for mappings, `frozenset`/`tuple` instead of
  `set`/`list`, and frozen dataclasses for records. Type it
  `Final[Mapping[str, Mapping[str, str]]]` so callers see no mutating API.
- **Use domain types for keys and values.** `StrEnum` keys and dataclass values
  (instead of nested `dict[str, str]`) remove the hard-coded strings, make
  structure visible, and let the type checker catch a bad key or missing field.
  See [type-design.md](type-design.md).
- **Prefer one record type over nested dicts.** `dict[str, dict[str, str]]`
  encodes a record as a map. A frozen dataclass `Unit(label=..., symbol=...)`
  held in `Mapping[UnitKind, Unit]` is the same data with a real contract.
- **If the table is derived, derive it at definition time** from the single
  source of truth (e.g. build the mapping from the enum members) instead of
  maintaining a parallel hand-written copy that can drift.
- **Small, truly local constants stay inline.** `MAX_RETRY_COUNT = 3` at the top
  of the module that uses it is good style; the problem is size, mutability, and
  duplicated meaning — not the constant itself.

## Decision table

| Situation | Preferred |
| --- | --- |
| Value computed once per process (settings, resolved path, parsed data) | `@functools.cache` getter returning a frozen value |
| Value that changes during the process (counter, current session, flags) | Object created and passed explicitly; no module state |
| Function needs to record progress | Return the new value / result object; do not mutate module state |
| Small local constant | `MAX_RETRY_COUNT = 3` in the owning module |
| Long fixed lookup table | Dedicated data module, `MappingProxyType`, precise key/value types |
| Table keyed by a finite domain vocabulary | `StrEnum` keys + frozen dataclass values |
| Per-instance lazy value | `functools.cached_property` |
| Temporary "context" for a call chain | Explicit parameter or context object (dataclass), not a module variable |

## Audit checklist

- [ ] Search for `global` statements and module-level assignments outside the
      constant section; both are findings.
- [ ] Confirm **PLW0603** is enabled and never suppressed — no
      `# noqa: PLW0603`, no rule disabled in configuration. It belongs to the
      Pylint group (`PL`), which Ruff does not enable by default; select it
      explicitly in the project lint configuration.
- [ ] Check every module-level mutable container (`dict`, `list`, `set`,
      `bytearray`, object instances): is it ever mutated after definition? If
      yes, it is global state — refactor it into a parameter, an object, or a
      cached getter.
- [ ] Check "constants" for mutation via `.update`, `.append`, item assignment,
      or `.pop` at any call site.
- [ ] Confirm long lookup tables live outside the logic module and are exposed
      through read-only views with precise types.
- [ ] Confirm cached getters return immutable values and have a documented
      reset path for tests.

Useful starting searches (adapt paths to the project layout):

```bash
rg -n '^\s*global\s+\w+' --glob '*.py'
rg -n 'noqa:\s*PLW0603|PLW0603' --glob '*.py' --glob '*.toml'
rg -n '^[A-Z_][A-Z0-9_]*\s*:\s*(Final\[)?(dict|list|set)\b' --glob '*.py'
rg -n '^[A-Z_][A-Z0-9_]*\s*=' --glob '*.py'             # module-level assignments
```

Semantic review is required: a module-level name assigned once in a constant
section and never mutated is fine; the same name reassigned or mutated from a
function is the antipattern the searches are meant to surface.
