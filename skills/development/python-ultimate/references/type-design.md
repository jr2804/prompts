# Domain Types, Enums, and Structured Data

Use named types to make domain concepts explicit, prevent invalid states, and keep
runtime behavior aligned with static type checking. Treat repeated domain strings
and unstructured `dict[str, Any]` / `dict[str, object]` annotations as design
findings—not as convenient defaults.

## Non-negotiable defaults

- **Do not scatter repeated domain strings.** A finite concept such as a status,
  mode, role, format, or command has one canonical definition. Use a `StrEnum`
  when it is a domain value; a reused standalone fixed string may use a named
  `Final[str]` constant. Import and reuse the definition rather than repeating
  the same meaning in comparisons, dictionary keys, defaults, tests, and call
  sites.
- **Do not use `Literal["..."]` as the domain model for a reusable finite set.**
  Prefer a `StrEnum` and annotate with the enum type. `Literal` is acceptable
  when an API/type-checker construct specifically requires it (for example,
  some overloads), or for a genuinely local type-level constraint that does not
  need a runtime domain type. It is not a substitute for an enum.
- **Do not annotate structured records as `dict[str, Any]` or
  `dict[str, object]` by default.** Use a dataclass for internal records. Use a
  `TypedDict` only when a dictionary-shaped interface is itself required, and
  give each key a precise value type. Use a runtime validator such as Pydantic
  (or a precise parser) for untrusted input: `TypedDict` does not validate data
  at runtime.
- **Avoid `Any` and `object` in annotations whenever a more precise type is
  available.** Treat each occurrence as a finding and replace it with a named
  record, a precise union, a generic, or a `Protocol`. Keep a broad type only
  when the value is genuinely opaque/dynamic and document why narrowing is not
  possible at that boundary. `object` is not a safer substitute for `Any`: it
  still leaves callers without a useful contract and forces narrowing.

## Why `StrEnum` instead of `Literal["..."]`

A `Literal` annotation gives static type checkers a finite set of allowed values
at annotated call sites, which can be useful. At runtime, however, the value is
still an ordinary `str`: `Literal` creates no enum class, member set, iteration,
or parsing/validation. Dynamically received values still need separate runtime
checks, and the same spellings are easy to duplicate across modules.

A `StrEnum` is a real, iterable class with named members and standard runtime
lookup/validation. `Status(raw_value)` returns the corresponding member or raises
`ValueError`; `list(Status)` provides the canonical choices. More precisely,
a member's concrete type is its enum class, not `str`, but `StrEnum` inherits
from `str`, so its members are also string instances:
`isinstance(JobStatus.QUEUED, str) is True`. This supports common string APIs and
interoperability. The canonical wire strings still exist, but are declared once
as enum values instead of being repeated as unrelated literals throughout the
code.

```python
from enum import StrEnum


class JobStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETE = "complete"


def start_job(status: JobStatus) -> None: ...


# Convert and validate once at an external boundary.
raw_status = "queued"
status = JobStatus(raw_status)  # ValueError for an unknown value
start_job(status)

for allowed_status in JobStatus:
    print(allowed_status.value)
```

Avoid stringly typed variants such as:

```python
from typing import Literal


JobStatus = Literal["queued", "running", "complete"]


def start_job(status: JobStatus) -> None: ...


if status == "queued":  # repeated domain spelling; no runtime enum validation
    ...
```

The `Literal` form can catch some incorrect statically visible calls, but it
cannot be iterated or used to validate an arbitrary runtime string. It also
encourages repeating the spellings in control flow and data structures.

### Python version compatibility

`enum.StrEnum` is in the standard library from Python 3.11. If the project must
support Python 3.10, either raise its minimum Python version when appropriate or
use the compatible standard-library form `class JobStatus(str, Enum)` and use
`.value` explicitly at serialization boundaries. Do not add a dependency just
to imitate `StrEnum` without first checking project conventions.

## Do not scatter hard-coded strings

A string literal is not automatically a problem: user-facing prose, a one-off
format string, and a protocol spelling at its boundary can remain literals. The
antipattern is repeating the same **domain meaning** in multiple places or using
raw strings as an implicit type system.

For each candidate repeated value:

1. Identify whether it is a finite domain choice, one immutable constant, or
   genuinely arbitrary text.
2. Use a `StrEnum` for a finite set, or a named `Final[str]` for one standalone
   constant. Keep the definition in the lowest, neutral module that owns the
   concept.
3. Convert untrusted/external strings to the domain type once at the boundary;
   pass the enum or a validated model internally.
4. Serialize to `.value` only where the external representation is needed.

Do not create a constant or enum for every incidental string. Centralize
semantic values; leave one-off prose and local formatting readable.

## Put shared types in a neutral module

When an enum or record is used by multiple modules, define it in a small shared
module owned by the domain/model layer, such as `domain/job_status.py` or a
well-scoped `domain/enums.py`. Feature modules should import the shared type;
the shared module must not import those feature modules. This prevents a
smallest-diff change from placing the new enum in a service/consumer module and
creating a circular import when another module needs it.

Keep a type local when it is genuinely private to one module. Do not create a
miscellaneous `types.py` just to avoid deciding ownership. Choose a module name
that reflects the domain concept, and extract the type plus related parsing or
serialization helpers only as needed.

```python
# domain/job_status.py — neutral source of truth
from enum import StrEnum


class JobStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETE = "complete"
```

```python
# worker.py and api.py both depend inward on the domain module.
from domain.job_status import JobStatus


def run_job(status: JobStatus) -> None: ...
```

If a circular import appears during extraction, review dependency direction and
move the shared contract to a neutral module; do not hide the cycle with
`TYPE_CHECKING`, copied literals, or imports from one feature module into
another. See [type-checking.md](type-checking.md) for shared-type and cycle
refactoring guidance.

## Model records as records, maps as maps

A record has a fixed set of named fields; represent it as a dataclass for
internal data. A map is a collection of homogeneous key/value entries; keep a
mapping type but make both sides precise. Use enum keys when the keys are a
finite domain vocabulary. For a required dictionary-shaped wire/API contract,
`TypedDict` can describe the shape, but it is static typing only—not validation.

```python
from dataclasses import dataclass
from enum import StrEnum


class ArtifactKind(StrEnum):
    TABLE = "table"
    FIGURE = "figure"


@dataclass(frozen=True, slots=True)
class Artifact:
    kind: ArtifactKind
    name: str
    page_number: int


# A genuine lookup map: each key and value still has a precise type.
counts_by_kind: dict[ArtifactKind, int] = {
    ArtifactKind.TABLE: 3,
    ArtifactKind.FIGURE: 2,
}
```

```python
from typing import TypedDict


# A wire shape that must remain dictionary-shaped; validate incoming JSON
# separately before relying on these annotations at runtime.
class RepositoryPayload(TypedDict):
    id: int
    name: str
    full_name: str
```

Do not turn every dictionary into an object: open-ended homogeneous maps are
valid. The rule is to avoid using a string-keyed dictionary as an undocumented
record, and never to silence uncertainty with `Any` or `object` when the shape
can be made explicit.

For module-level lookup tables built from these types — where they should live,
and how to keep them read-only — see [module-state.md](module-state.md).

## TypedDict: runtime and typing boundaries

`TypedDict` is a **structural, type-checker-only** contract over a plain `dict`.
The value remains the original dict: no constructor runs, no copy is made, and
nothing exists at runtime beyond the dict. `isinstance(x, SomeTypedDict)` raises
`TypeError` (there is no runtime class to check against). Do not treat `cast()`
as validation: `cast(Payload, response.json())` only informs the type checker
and proves nothing about the bytes that arrived.

### When `TypedDict` fits

- **Key presence matters (partial updates).** Use `NotRequired` (or `total=False`
  on the whole type, used deliberately) to preserve the distinction between "key
  omitted" and "value is `None`". Branch on `"key" in payload"` rather than on
  attribute defaults that collapse both cases.
- **You already have the dict** and only need the checker to know its shape,
  with no copy or runtime overhead (e.g., a `requests.json()` result or a DB
  row kept dict-shaped).
- **Wire contract vs. parser.** A `TypedDict` can document what the network
  sends; it does not replace runtime validation of untrusted input.

```python
from typing import NotRequired, TypedDict


class UpdateProfile(TypedDict):
    email: NotRequired[str | None]
    phone: NotRequired[str | None]


def apply_update(patch: UpdateProfile) -> None:
    if "email" in patch:
        user.email = patch["email"]  # present and possibly None = explicit clear
    # absent key => leave existing value unchanged
```

### Sharp edges

- **Structural, not nominal.** Unrelated `TypedDict`s with compatible keys/types
  are interchangeable to the checker; the type is the shape, not a brand.
- **Requiredness composition.** Fields are required by default; subclasses add
  required fields unless marked `NotRequired`. Prefer per-field `NotRequired`
  for clarity; use `total=False` only when most fields are optional and that
  intent is obvious.
- **No runtime validation.** Annotations, including `TypedDict` and `StrEnum`
  annotations, do not validate arbitrary external values. Convert/parse once at
  the trust boundary (Pydantic or an explicit parser) before relying on the
  shape.

## Layering wire, parse, and domain (when mixing is warranted)

When external data enters the program, the three modeling tools can play
different roles for the *same* concept without fighting each other:

1. **Wire (contract):** `TypedDict` describes the expected dict shape (static
   only) when keeping the payload dict-shaped is useful.
2. **Parse (trust boundary):** a runtime validator (typically Pydantic) parses
   and validates/coerces untrusted input once, failing loudly on bad data.
3. **Domain (internal):** a `@dataclass` (often `frozen=True, slots=True`) holds
   the values the rest of the program constructs and passes around.

Convert at the boundary (`parse(raw: Wire) -> Domain` via the validator). Build
`Domain` directly in tests and internal code; do not re-run boundary validation
on values your own code just constructed. Keep this layering only where a real
boundary exists—do not add ceremony for purely internal data (see "Don't mix the
two for the same concept" in [coding-standards.md](coding-standards.md) for the
evolution case where a type should simply become a validated model).

## Audit checklist

When writing or reviewing code, check each applicable item:

- [ ] Search for `Literal[...]`; convert reusable finite domain string choices
      to `StrEnum` unless a specific API/type-checking requirement justifies
      `Literal`.
- [ ] Find repeated domain strings in branches, defaults, dict keys, tests, and
      serialization; centralize the semantic value and reuse its named type.
- [ ] Check whether a shared enum/model belongs in a neutral module rather than
      a feature module that can create a cycle.
- [ ] Search for `dict[str, Any]`, `dict[str, object]`, and broad annotations;
      distinguish records (dataclass/validated model) from real maps (precise
      key/value types).
- [ ] Confirm untrusted data is validated at its boundary; a type annotation,
      `TypedDict`, or `StrEnum` annotation alone does not validate arbitrary
      external values until they are explicitly converted/parsed.

Useful starting searches (adapt `src/` to the project layout):

```bash
rg -n 'Literal\s*\[' src/ --glob '*.py'
rg -n 'dict\s*\[\s*str\s*,\s*(Any|object)\s*\]|\bAny\b|\bobject\b' src/ --glob '*.py'
```

Search results need semantic review: `Literal` may be required by a local API,
and `Any`/`object` may occur in a justified dynamic boundary. String duplication
is domain-specific and cannot be reliably classified by a single regex; inspect
repeated values in the changed code and trace them to their owning concept.
