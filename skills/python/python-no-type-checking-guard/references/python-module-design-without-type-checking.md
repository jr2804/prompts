# Python module design without `TYPE_CHECKING`

This reference document explains *why* this skill forbids
`from typing import TYPE_CHECKING` and shows concrete design patterns that
avoid it while still supporting robust static type checking.

---

## 1. Why avoid `TYPE_CHECKING` in this project?

Python exposes `typing.TYPE_CHECKING` as a constant that static type checkers
understand, and many style guides recommend it for type‑only imports.
This project **intentionally** prohibits that pattern for several reasons:

1. **It hides design problems instead of fixing them.**

   When you need to guard imports just to avoid circular imports from type
   hints, the real problem is usually that modules depend on each other too
   directly. Extracting shared types or interfaces into a dedicated module
   (e.g. `models.py`, `types.py`, `interfaces.py`) breaks cycles cleanly
   and makes the architecture easier to understand.

2. **It diverges runtime behavior from type‑checker behavior.**

   Code inside `if TYPE_CHECKING:` never runs at runtime, yet type checkers
   treat it as if it does. This creates two different "views" of a module —
   one for the interpreter, one for the type checker — which complicates
   debugging, tooling, and onboarding.

3. **It adds import‑time and cognitive overhead.**

   Even when used correctly, `TYPE_CHECKING` still requires importing the
   `typing` module and often pulling in additional names only for types.
   Guarded imports introduce conditional blocks that readers must mentally
   simulate, making modules harder to scan.

4. **Modern Python features make most uses unnecessary.**

   Forward references via `"MyClass"` or `from __future__ import annotations`
   (and default lazy evaluation of annotations in newer Python versions)
   drastically reduce the need for type‑only imports. Combined with better
   module structure, this covers nearly all circular‑import situations.

---

## 2. Core refactoring patterns

### 2.1 Extract common types into dedicated modules

**Problem:** Two modules reference each other's classes in type hints and
import each other directly.

```python
# user.py
from .order import Order

class User:
    def last_order(self) -> "Order":
        ...
```

```python
# order.py
from .user import User

class Order:
    def customer(self) -> User:
        ...
```

**Refactor to — move shared domain types to a third module:**

```python
# domain.py
class User:
    ...

class Order:
    ...
```

```python
# user.py
from .domain import Order, User

class User(User):
    def last_order(self) -> Order:
        ...
```

```python
# order.py
from .domain import Order, User

class Order(Order):
    def customer(self) -> User:
        ...
```

**Guidelines:**

- Group closely related domain entities, enums, and dataclasses in one or a
  few small modules that do **not** depend on high‑level features.
- Let feature modules depend on these shared domain modules instead of on
  each other.

---

### 2.2 Introduce protocols or interfaces to break cycles

**Problem:** Multiple modules need to refer to each other's behavior, but
they should not depend on each other's concrete implementations.

```python
# interfaces.py
from typing import Protocol

class Storage(Protocol):
    def write(self, key: str, data: bytes) -> None: ...
    def read(self, key: str) -> bytes: ...
```

```python
# storage_fs.py
from .interfaces import Storage

class FileSystemStorage(Storage):
    ...
```

```python
# service.py
from .interfaces import Storage

class Service:
    def __init__(self, storage: Storage) -> None:
        self._storage = storage
```

**Benefits:**

- `service` and `storage_fs` do not import each other; both depend only on
  `interfaces`, which is stable and easy to reason about.
- Type checkers can still verify correctness thanks to the protocol
  definitions.
- The dependency structure follows clean architecture / hexagonal ideas.

---

### 2.3 Use forward references instead of type‑only imports

**Pattern 1 — simple string annotations:**

```python
class Node:
    def __init__(self, parent: "Node | None" = None) -> None:
        self.parent = parent
```

**Pattern 2 — postponed evaluation of annotations:**

```python
from __future__ import annotations

class Node:
    def __init__(self, parent: Node | None = None) -> None:
        self.parent = parent
```

With postponed evaluation (and in newer Python versions where annotations
are lazy by default), the annotation is not evaluated at function definition
time, so it does not force additional imports.

---

### 2.4 Local imports as a targeted workaround

Local imports inside functions are acceptable for **genuine runtime
concerns**, not for type hints:

```python
def render_report(data: ReportData) -> str:
    # Local import because the rendering library is heavy and only
    # needed for this function.
    from .renderer import render_to_html

    return render_to_html(data)
```

Acceptable use cases:

- Optional heavy dependencies (e.g. large numeric or ML libraries).
- Rarely used code paths in performance‑sensitive modules.
- Framework limitations that make re‑architecting infeasible.

**Constraints:**

- Do not use this solely for type hints.
- Prefer forward references for types and keep imports runtime‑accurate.
- Document clearly *why* the local import exists.

---

## 3. Step‑by‑step: modernizing existing code

When the task is to modernize, clean up types, or improve module structure
in a codebase that already uses `TYPE_CHECKING`:

1. **Identify why each `TYPE_CHECKING` block exists.**
   Common reasons: type‑only imports to avoid cycles, heavy imports used
   only in annotations.

2. **Apply the structural patterns above.**
   - Extract shared types into neutral modules (§2.1).
   - Replace concrete cross‑dependencies with protocols (§2.2).
   - Use forward references instead of type‑only imports (§2.3).

3. **Remove `TYPE_CHECKING` gradually.**
   Once a guarded import is no longer needed, inline it as a normal
   top‑level import or drop it entirely if only used for typing.
   Re‑run static type checking and tests after each removal.

4. **Verify alignment of runtime and static views.**
   After cleanup, no code should be "visible" only to the type checker;
   all imports should reflect real runtime dependencies.
