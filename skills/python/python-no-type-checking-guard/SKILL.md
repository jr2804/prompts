---
name: python-no-type-checking-guard
description: >
  Enforces a Python typing style that forbids `from typing import TYPE_CHECKING`
  and `if TYPE_CHECKING:` guards. Use when generating, refactoring, or reviewing
  Python code with type hints; when asked to fix circular-import problems related
  to type hints; when optimizing imports or cleaning up typing / mypy / pyright
  issues; or when modernizing existing code that uses TYPE_CHECKING guards.
  This skill is global in scope for Python code — follow it even if other skills
  suggest TYPE_CHECKING as a convenience.
---

# Python typing without `TYPE_CHECKING`

This skill defines hard rules and preferred patterns for writing typed Python
code **without ever using** `from typing import TYPE_CHECKING` or
`if TYPE_CHECKING:` blocks. It applies to all Python code the agent creates
or edits unless the user explicitly overrides this style for a specific file.

For detailed examples and design rationale, consult the bundled reference
`references/python-module-design-without-type-checking.md`.

## Non‑negotiable rules

Follow these rules strictly unless the user explicitly instructs otherwise.

1. **Never import `TYPE_CHECKING`.**
   - Do **not** write `from typing import TYPE_CHECKING`.
   - Do **not** rely on `typing.TYPE_CHECKING` or any alias of it.
   - Do **not** introduce `TYPE_CHECKING = False` or similar "shadow"
     variables as an alternative.

2. **Never wrap imports in `if TYPE_CHECKING:`.**
   - Do **not** use `if TYPE_CHECKING:` blocks to guard imports, even if
     other style guides or examples recommend this pattern.
   - Do **not** move imports into `if TYPE_CHECKING:` solely to break
     circular imports or to "speed up" imports.

3. **Prefer normal, top‑level imports.**
   - Place imports at module top level in the usual way.
   - Only move imports inside functions/methods as a last resort for
     unavoidable runtime concerns (e.g. optional heavy dependencies),
     **not** for typing convenience.

4. **Do not increase divergence between runtime and type‑checking behavior.**
   - Generated code should behave the same under the Python interpreter and
     under static type checkers.
   - Avoid any pattern whose sole purpose is to hide imports from runtime
     while exposing them only to the type checker.

5. **Existing `TYPE_CHECKING` blocks: do not extend; prefer to remove.**
   - If a file already contains `TYPE_CHECKING` guards:
     - You **may leave them as‑is** when doing a minimal change and the
       user did not ask for structural refactoring.
     - **Do not add new guarded imports** or propagate this pattern into
       new modules.
     - When refactoring, prefer to replace such guards with cleaner
       designs described in this skill.

## How to avoid circular imports without `TYPE_CHECKING`

When tempted to use `TYPE_CHECKING` to "solve" a circular import, apply these
patterns instead. See the reference file for full examples and code snippets.

### 1. Extract shared types into a dedicated module

If two modules import each other only for types, extract the shared types
(`dataclass`, `Protocol`, `TypedDict`, enums, etc.) into a third module
(e.g. `models.py`, `types.py`, `domain.py`) and let both depend on that.
This keeps the dependency graph acyclic by design.

### 2. Depend on protocols or interfaces, not concrete classes

If several modules mutually depend on concrete implementations, introduce
`Protocol` or abstract base types in a separate `interfaces.py` / `ports.py`
module. Feature modules then depend only on the interface, breaking cycles
through dependency inversion.

### 3. Use forward references instead of guarded imports

Prefer string annotations (`"MyClass"`) or `from __future__ import annotations`
for forward references, rather than importing symbols into guarded blocks
purely for annotations. In newer Python versions, lazy evaluation of
annotations removes most needs for type‑only imports.

### 4. Local imports as a targeted workaround

Local imports inside functions are acceptable for **genuine runtime concerns**
(heavy optional dependencies, rarely‑used code paths, framework limitations),
but **never** solely for type hints. Document clearly _why_ the local import
exists.

## Handling existing code that uses `TYPE_CHECKING`

- **Minimal edits:** Leave existing guards intact. Do not introduce new
  guarded imports or extend the pattern into new modules.
- **Modernization / cleanup:** Identify why each `TYPE_CHECKING` block exists,
  then apply the patterns above (extract types, introduce protocols, use
  forward references) to gradually remove them. Re-run type checking and
  tests after each removal.
