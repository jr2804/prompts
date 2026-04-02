# Type Checking Reference

## Table of Contents

1. [Rule: Never Use TYPE_CHECKING Guards](#1-rule-never-use-type_checking-guards)
2. [Why TYPE_CHECKING is Problematic](#2-why-type_checking-is-problematic)
3. [Alternative Patterns](#3-alternative-patterns)
   - [Extract Shared Types to Dedicated Modules](#31-extract-shared-types-to-dedicated-modules)
   - [Use Protocols for Structural Typing](#32-use-protocols-for-structural-typing)
   - [Forward References (String Literals)](#33-forward-references-string-literals)
   - [Local Imports (Last Resort)](#34-local-imports-last-resort)
4. [Handling Existing Code with TYPE_CHECKING](#4-handling-existing-code-with-type_checking)

______________________________________________________________________

## 1. Rule: Never Use TYPE_CHECKING Guards

**Never import `TYPE_CHECKING`.**

```python
# WRONG — never do this
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import User, Order
```

**Never wrap imports in `if TYPE_CHECKING:` blocks.**

```python
# WRONG — never do this
if TYPE_CHECKING:
    from .external import HeavyModel

class Service:
    def process(self, data: "HeavyModel") -> None:  # type: ignore
        ...
```

**Prefer normal, top-level imports.** Only use local imports inside functions for genuine runtime concerns (e.g., heavy optional dependencies), never solely for type hints.

______________________________________________________________________

## 2. Why TYPE_CHECKING is Problematic

### Hides Design Problems

When you need `TYPE_CHECKING` guards to avoid circular imports, the real problem is usually that modules depend on each other too directly. Extracting shared types into a dedicated module breaks cycles cleanly and makes the architecture easier to understand.

### Diverges Runtime from Type-Checker Behavior

Code inside `if TYPE_CHECKING:` never runs at runtime, yet type checkers treat it as if it does. This creates two different "views" of a module — one for the interpreter, one for the type checker — which complicates debugging, tooling, and onboarding.

### Adds Import-Time and Cognitive Overhead

Even when used correctly, `TYPE_CHECKING` requires importing the `typing` module and often pulling in additional names only for types. Guarded imports introduce conditional blocks that readers must mentally simulate.

### Modern Python Makes It Unnecessary

Forward references via `"MyClass"` or `from __future__ import annotations` (and default lazy evaluation of annotations in Python 3.10+) drastically reduce the need for type-only imports.

______________________________________________________________________

## 3. Alternative Patterns

### 3.1 Extract Shared Types to Dedicated Modules

**Problem:** Two modules reference each other's classes in type hints.

```python
# user.py
from .order import Order  # causes cycle

class User:
    def last_order(self) -> "Order":
        ...
```

```python
# order.py
from .user import User  # causes cycle

class Order:
    def customer(self) -> User:
        ...
```

**Solution:** Move shared domain types to a third module.

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

- Group closely related domain entities, enums, and dataclasses in one or a few small modules.
- Let feature modules depend on these shared domain modules instead of on each other.

______________________________________________________________________

### 3.2 Use Protocols for Structural Typing

**Problem:** Multiple modules need to refer to each other's behavior without depending on concrete implementations.

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

- `service` and `storage_fs` do not import each other; both depend only on `interfaces`.
- Type checkers verify correctness via protocol definitions.
- Follows clean architecture / hexagonal architecture principles.

______________________________________________________________________

### 3.3 Forward References (String Literals)

**Pattern 1 — Simple string annotations:**

```python
class Node:
    def __init__(self, parent: "Node | None" = None) -> None:
        self.parent = parent
```

**Pattern 2 — Postponed evaluation of annotations:**

```python
from __future__ import annotations

class Node:
    def __init__(self, parent: Node | None = None) -> None:
        self.parent = parent
```

With `from __future__ import annotations`, annotations are not evaluated at function definition time, so they do not force additional imports at definition time.

______________________________________________________________________

### 3.4 Local Imports (Last Resort)

Use local imports inside functions only for **genuine runtime concerns**, not for type hints:

```python
def render_report(data: ReportData) -> str:
    # Local import because the rendering library is heavy and only
    # needed for this function.
    from .renderer import render_to_html

    return render_to_html(data)
```

**Acceptable use cases:**

- Optional heavy dependencies (e.g., large numeric or ML libraries).
- Rarely used code paths in performance-sensitive modules.
- Framework limitations that make re-architecting infeasible.

**Constraints:**

- Do not use solely for type hints.
- Document clearly *why* the local import exists.
- Prefer forward references for types and keep imports runtime-accurate.

______________________________________________________________________

## 4. Handling Existing Code with TYPE_CHECKING

### Minimal Edits

Leave existing `TYPE_CHECKING` guards intact. Do not introduce new guarded imports or extend the pattern into new modules.

### Modernization / Cleanup

When tasked with improving module structure:

1. **Identify why each `TYPE_CHECKING` block exists.** Common reasons: type-only imports to avoid cycles, heavy imports used only in annotations.

2. **Apply the structural patterns above:**

   - Extract shared types into neutral modules (§3.1).
   - Replace concrete cross-dependencies with protocols (§3.2).
   - Use forward references instead of type-only imports (§3.3).

3. **Remove `TYPE_CHECKING` gradually.** Once a guarded import is no longer needed, inline it as a normal top-level import or drop it entirely if only used for typing.

4. **Verify alignment.** After cleanup, no code should be "visible" only to the type checker; all imports should reflect real runtime dependencies. Re-run static type checking and tests after each removal.
