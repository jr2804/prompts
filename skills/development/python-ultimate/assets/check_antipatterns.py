# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

"""Scan Python files for antipatterns that linters cannot express.

Only rules that have no equivalent Ruff or type-checker diagnostics live here.
Everything a configured linter already reports (``PLW0603`` for ``global``,
``PGH004``/``RUF100`` for ``# noqa``, ``PTH`` for ``os.path``, ``UP045`` for
``Optional[T]``, ``PLC0415`` for inline imports) is deliberately absent:
duplicating it in a custom scanner produces a second, drifting source of truth.
See ``references/linter-rules.md`` for the rule-to-tool mapping.

Rules
-----

``IMPORT-ERROR-GUARD``
    A ``try: import x`` / ``except ImportError`` block guarding a *required*
    dependency. Optional dependencies may be probed; required ones must be
    imported at module level so a missing install fails immediately and
    loudly. Optionality is resolved against, in order:

    1. the scanned file's own PEP 723 ``dependencies`` (all required);
    2. the project ``pyproject.toml`` ``[project.optional-dependencies]``;
    3. ``importlib.metadata.packages_distributions()`` to map an imported
       top-level module (``PIL``) to its distribution (``Pillow``).

    A module that is only in an optional group is allowed. A module that is
    also a required dependency, or that is not declared at all, is a finding:
    an undeclared guard hides a missing dependency instead of expressing an
    optional one. When step 3 returns nothing (no distributions visible, e.g.
    ``python -I -S``) an unmatched module is *unknown* rather than undeclared:
    the scan exits ``2`` naming the module instead of inventing a finding.

``BANNED-NOQA``
    A ``# noqa: CODE`` comment naming a rule the project forbids suppressing.
    Ruff's ``PGH004`` catches blanket ``# noqa`` and ``RUF100`` catches unused
    ones, but neither can express "this specific code must never be
    suppressed". Supply the banned codes per project with ``--ban-noqa``.

Every violation prints ``file:line:col  rule  message`` and the script exits
non-zero on any violation. Exit codes: ``0`` clean, ``1`` violations found,
``2`` the scan itself was invalid (nothing scanned, or a file could not be
parsed). A scan that covers nothing never reports success.

Usage::

    uv run check_antipatterns.py .
    uv run check_antipatterns.py src tests --ban-noqa PLC0415 --ban-noqa E402
    uv run check_antipatterns.py . --json
"""

from __future__ import annotations

import argparse
import ast
import fnmatch
import io
import json
import re
import subprocess
import sys
import tokenize
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

try:  # Python 3.11+
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 fallback
    tomllib = None  # type: ignore[assignment]

__all__ = ["Violation", "main", "scan_file"]

#: Directories never worth walking into.
SKIP_DIRS: frozenset[str] = frozenset(
    {
        ".git",
        ".hg",
        ".svn",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".tox",
        ".venv",
        "__pycache__",
        "build",
        "dist",
        "node_modules",
        "venv",
    }
)

#: A directive comment starts with the code, e.g. the literal text below. Anchored
#: matching is deliberate: prose that merely mentions the directive name is not a
#: suppression, and Ruff likewise refuses to honour one that is not at the start
#: of the comment.
_NOQA_RE = re.compile(
    r"#+\s*noqa(?::\s*(?P<codes>[A-Z]+[0-9]+(?:[,\s]+[A-Z]+[0-9]+)*))?", re.IGNORECASE
)

#: Standard-library module names. A guard around one of these is dead code, but
#: it is not a dependency-declaration problem, so it is out of scope here.
_STDLIB_MODULES: frozenset[str] = frozenset(getattr(sys, "stdlib_module_names", ()))
#: Names that are always present regardless of interpreter build.
_STDLIB_ALWAYS: frozenset[str] = frozenset({"__future__", "builtins"})

#: Asking Ruff for its rule list is a local call; a long timeout would only hide
#: a broken install, so fail fast and treat `None` as "cannot verify".
_RUFF_TIMEOUT_SECONDS = 30

#: Opening marker of a PEP 723 inline-metadata block.
_SCRIPT_MARKER = "# /// script"


@dataclass(frozen=True)
class Violation:
    """One antipattern finding."""

    file: Path
    line: int
    col: int
    rule: str
    message: str

    def format(self, root: Path) -> str:
        try:
            shown = self.file.relative_to(root)
        except ValueError:
            shown = self.file
        return f"{shown}:{self.line}:{self.col}  {self.rule}  {self.message}"

    def as_dict(self, root: Path) -> dict[str, object]:
        try:
            shown = self.file.relative_to(root)
        except ValueError:
            shown = self.file
        return {
            "file": shown.as_posix(),
            "line": self.line,
            "col": self.col,
            "rule": self.rule,
            "message": self.message,
        }


@dataclass(frozen=True)
class DependencyFacts:
    """What the project declares, so optionality can be decided."""

    required: frozenset[str]
    optional: frozenset[str]
    module_to_distribution: dict[str, frozenset[str]]

    def is_optional_only(self, module: str) -> bool:
        """True when *module* is declared optional and never required."""
        names = self._candidate_names(module)
        if names & self.required:
            return False
        return bool(names & self.optional)

    def is_declared(self, module: str) -> bool:
        names = self._candidate_names(module)
        return bool(names & (self.required | self.optional))

    def has_resolver(self) -> bool:
        """True when installed distributions are visible, so aliases can be mapped.

        With no resolver, ``import PIL`` cannot be matched against the ``Pillow``
        distribution. That makes the dependency status of such a module
        *unknown* rather than undeclared, and reporting it would be a false
        positive produced by a missing fact rather than by the code under scan.
        Literal matches still work: ``import requests`` resolves against a
        declared ``requests`` without needing the map at all.
        """
        return bool(self.module_to_distribution)

    def _candidate_names(self, module: str) -> set[str]:
        """Normalized names that could identify *module* as a dependency.

        ``import PIL`` must match the ``Pillow`` distribution, so the
        module-to-distribution map contributes extra candidates.
        """
        names = {_normalize(module)}
        for distribution_name in self.module_to_distribution.get(module, frozenset()):
            names.add(_normalize(distribution_name))
        return names

    def declared_in_script(self, module: str, script_required: frozenset[str]) -> bool:
        """True when *module* is one of the script's own PEP 723 dependencies."""
        return bool(self._candidate_names(module) & script_required)


def _normalize(name: str) -> str:
    """Normalize a distribution or module name for comparison (PEP 503)."""
    return re.sub(r"[-_.]+", "-", name).lower()


def _requirement_name(spec: str) -> str:
    """Extract the bare distribution name from a PEP 508 requirement string."""
    return re.split(r"[\s<>=!~;\[(@]", spec.strip(), maxsplit=1)[0]


def _read_script_dependencies(source: str) -> tuple[frozenset[str], str | None]:
    """Return ``(declared distributions, error)`` for a PEP 723 ``dependencies`` block.

    An unreadable block is an error, not an empty set. ``frozenset()`` means "this
    script declares nothing", which silently exempts every guarded import in the
    file; a malformed block would therefore turn the rule off for that script
    while still reporting a clean scan.
    """
    lines = source.splitlines()
    if not any(line.strip().startswith(_SCRIPT_MARKER) for line in lines):
        return frozenset(), None
    collected: list[str] = []
    inside = False
    for line in lines:
        stripped = line.strip()
        if stripped == _SCRIPT_MARKER:
            inside = True
            continue
        if inside and stripped == "# ///":
            break
        if inside and stripped.startswith("#"):
            collected.append(stripped[1:].lstrip())
    if not collected:
        return frozenset(), None
    if tomllib is None:  # pragma: no cover - 3.11+ is the declared floor
        return frozenset(), "tomllib unavailable, cannot read the PEP 723 block"
    try:
        data = tomllib.loads("\n".join(collected))
    except (tomllib.TOMLDecodeError, ValueError) as error:
        return frozenset(), f"unparseable PEP 723 block ({error})"
    declared = data.get("dependencies", [])
    if not isinstance(declared, list):
        return frozenset(), "PEP 723 `dependencies` is not a list"
    return frozenset(
        _normalize(_requirement_name(str(item))) for item in declared
    ), None


def _read_pyproject(root: Path) -> tuple[frozenset[str], frozenset[str], str | None]:
    """Return ``(required, optional, error)`` distribution names from *root*.

    A present-but-unreadable ``pyproject.toml`` is an error: an empty dependency
    set makes every guarded import look undeclared, and the scan would then
    report findings (or a clean run) against facts it never established.

    The same applies to a ``pyproject.toml`` with no ``[project]`` table. That is
    a legitimate shape for a workspace root, but it declares no dependencies, so
    judging guards against it invents facts. A bare ``[project]`` with an empty
    ``dependencies`` list is different and honest: the project really has none.
    """
    pyproject = root / "pyproject.toml"
    if not pyproject.is_file():
        return frozenset(), frozenset(), None
    if tomllib is None:  # pragma: no cover - 3.11+ is the declared floor
        return frozenset(), frozenset(), f"tomllib unavailable, cannot read {pyproject}"
    try:
        data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError, ValueError) as error:
        return frozenset(), frozenset(), f"cannot read {pyproject} ({error})"

    project = data.get("project")
    if not isinstance(project, dict):
        return (
            frozenset(),
            frozenset(),
            (
                f"{pyproject} has no [project] table, so it declares no "
                "dependencies. That is a normal shape for a virtual workspace "
                "root, but the guards cannot be judged against it.\nFix: point "
                "--project-root at the member package that declares the "
                "dependencies."
            ),
        )
    declared = project.get("dependencies", [])
    required = frozenset(
        _normalize(_requirement_name(str(spec)))
        for spec in declared
        if str(spec).strip()
    )
    optional: set[str] = set()
    for group in project.get("optional-dependencies", {}).values():
        optional.update(
            _normalize(_requirement_name(str(spec)))
            for spec in group
            if str(spec).strip()
        )
    return required, frozenset(optional), None


def _module_distribution_map() -> dict[str, frozenset[str]]:
    """Map top-level import names to distributions, for alias resolution.

    ``import PIL`` is satisfied by the ``Pillow`` distribution; without this
    map every such guard would look undeclared and be flagged.
    """
    try:
        from importlib.metadata import PackageNotFoundError, packages_distributions
    except ImportError:  # pragma: no cover - always present on 3.10+
        return {}
    try:
        mapping = packages_distributions()
    except (PackageNotFoundError, OSError):  # pragma: no cover - broken environment
        return {}
    return {
        module: frozenset(distributions)
        for module, distributions in mapping.items()
        if distributions
    }


def discover_python_files(
    roots: Iterable[Path], errors: list[str], exclude: Iterable[str] = ()
) -> list[Path]:
    """Recursively collect Python files under *roots*, skipping vendored dirs.

    *exclude* entries are matched against directory names and against paths
    relative to the scan root, so ``--exclude examples`` drops every ``examples``
    directory and ``--exclude */fixtures`` drops just those.

    *errors* collects roots that do not exist. A missing root must not narrow
    the scan silently: what remains would look clean, so a typo in a repeated
    path argument would read as a pass.
    """
    patterns = [pattern.strip("/") for pattern in exclude if pattern.strip("/")]
    found: list[Path] = []
    for root in roots:
        if root.is_file():
            if root.suffix == ".py":
                found.append(root)
            continue
        if not root.is_dir():
            errors.append(
                f"{root}: no such file or directory - refusing to scan. "
                "Check the path for a typo."
            )
            continue
        for path in root.rglob("*.py"):
            if SKIP_DIRS.intersection(path.parts):
                continue
            if patterns and _is_excluded(path, root, patterns):
                continue
            found.append(path)
    return sorted(set(found))


def _is_excluded(path: Path, root: Path, patterns: list[str]) -> bool:
    """True when *path* matches any exclusion pattern relative to *root*."""
    try:
        relative = path.relative_to(root)
    except ValueError:
        relative = path
    candidates = {part for part in relative.parts[:-1]}
    as_posix = relative.as_posix()
    for pattern in patterns:
        if pattern in candidates:
            return True
        if fnmatch.fnmatch(as_posix, pattern) or fnmatch.fnmatch(
            as_posix, f"{pattern}/*"
        ):
            return True
    return False


def _imported_modules(node: ast.Try) -> list[tuple[str, int]]:
    """Top-level module names imported inside a ``try`` body, with line numbers."""
    modules: list[tuple[str, int]] = []
    for statement in node.body:
        for child in ast.walk(statement):
            if isinstance(child, ast.Import):
                modules.extend(
                    (alias.name.split(".")[0], child.lineno) for alias in child.names
                )
            elif (
                isinstance(child, ast.ImportFrom) and child.module and child.level == 0
            ):
                modules.append((child.module.split(".")[0], child.lineno))
    return modules


def scan_import_error_guards(
    path: Path,
    tree: ast.Module,
    facts: DependencyFacts,
    script_required: frozenset[str],
) -> tuple[list[Violation], list[str]]:
    """Flag ``try: import x / except ImportError`` around required dependencies.

    Returns ``(violations, unresolved_modules)``. A module whose dependency
    status could not be established is returned in the second list instead of
    being reported: with no visible distributions, an import name that differs
    from its distribution name cannot be matched, so the honest answer is "I do
    not know" and the caller turns that into a failed scan.

    Project files are judged against ``pyproject.toml``: optional-only modules
    may be probed, required ones may not.

    PEP 723 scripts are judged against their own ``dependencies`` block, which
    ``uv run`` always installs in full. A guard around a declared dependency is
    therefore dead weight and reported. A guard around an *undeclared* module in
    a script is a legitimate optional probe (accelerators such as ``orjson``)
    and is left alone - so scripts never need the distribution map.
    """
    violations: list[Violation] = []
    unresolved: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Try):
            continue
        if not any(
            isinstance(handler.type, ast.Name) and handler.type.id == "ImportError"
            for handler in node.handlers
        ):
            continue
        for module, line in _imported_modules(node):
            if module in _STDLIB_MODULES or module in _STDLIB_ALWAYS:
                continue  # stdlib needs no declaration; guarding it is merely dead code
            if script_required:
                if not facts.declared_in_script(module, script_required):
                    continue  # script probe of an undeclared (optional) module
                reason = (
                    "is declared as a script dependency, so `uv run` always installs it"
                )
            elif facts.is_optional_only(module):
                continue  # probing an optional project dependency is the legitimate use
            elif facts.is_declared(module):
                reason = "is a required project dependency"
            elif not facts.has_resolver():
                unresolved.append(module)
                continue
            else:
                reason = "is not declared as an optional dependency"
            violations.append(
                Violation(
                    file=path,
                    line=line,
                    col=1,
                    rule="IMPORT-ERROR-GUARD",
                    message=(
                        f"try/except ImportError guards `{module}`, which {reason}. "
                        "Import required dependencies at module level; reserve the guard for "
                        "packages declared in [project.optional-dependencies]."
                    ),
                )
            )
    return violations, sorted(set(unresolved))


def _describe_token_error(error: BaseException) -> str:
    """Render a ``tokenize`` failure as ``message at line:col`` when available."""
    if isinstance(error, tokenize.TokenError) and error.args:
        message = str(error.args[0])
        position = error.args[1] if len(error.args) > 1 else None
        if isinstance(position, tuple) and len(position) == 2:
            return f"{message} at {position[0]}:{position[1]}"
        return message
    return str(error) or type(error).__name__


def scan_banned_noqa(
    path: Path, source: str, banned: frozenset[str]
) -> tuple[list[Violation], str | None]:
    """Flag real ``# noqa`` directives that suppress a banned rule code.

    Comment tokens are tokenized rather than string-searched, so a ``# noqa``
    inside a string literal or docstring is never a finding. A bare ``# noqa``
    yields no codes and is left to ``PGH004``.

    Returns ``(violations, error)``. A file the tokenizer rejects is reported as
    an error rather than an empty result: silently skipping it would let a
    banned suppression pass unobserved in the one file we could not read.
    """
    if not banned:
        return [], None
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(source).readline))
    except (tokenize.TokenError, IndentationError) as error:
        return [], (
            f"{path}: cannot tokenize ({_describe_token_error(error)}). "
            "Banned `# noqa` suppressions in this file cannot be checked."
        )
    violations: list[Violation] = []
    for token in tokens:
        if token.type != tokenize.COMMENT:
            continue
        match = _NOQA_RE.match(token.string)
        if match is None:
            continue
        codes = {
            code.upper()
            for code in re.split(r"[,\s]+", match.group("codes") or "")
            if code
        }
        for code in sorted(codes & banned):
            violations.append(
                Violation(
                    file=path,
                    line=token.start[0],
                    col=token.start[1] + 1,
                    rule="BANNED-NOQA",
                    message=(
                        f"`# noqa: {code}` suppresses a rule this project forbids silencing. "
                        "Fix the root cause instead of suppressing the diagnostic."
                    ),
                )
            )
    return violations, None


def scan_file(
    path: Path, facts: DependencyFacts, banned: frozenset[str]
) -> tuple[list[Violation], str | None]:
    """Scan one file. Returns (violations, parse_error)."""
    try:
        source = path.read_text(encoding="utf-8", errors="replace")
    except OSError as error:
        return [], f"{path}: cannot read ({error}). Check the file permissions or path."

    violations, noqa_error = scan_banned_noqa(path, source, banned)
    if noqa_error is not None:
        return violations, noqa_error

    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as error:
        return violations, (
            f"{path}:{error.lineno}: cannot parse ({error.msg}). "
            "Fix the syntax first; rules that need the AST cannot be judged."
        )

    script_required, block_error = _read_script_dependencies(source)
    if block_error is not None:
        return violations, f"{path}: {block_error}"
    guard_violations, unresolved = scan_import_error_guards(
        path, tree, facts, script_required
    )
    violations.extend(guard_violations)
    violations.sort(
        key=lambda violation: (violation.line, violation.col, violation.rule)
    )
    if unresolved:
        return violations, (
            f"{path}: cannot judge the guard(s) on "
            + ", ".join(f"`{module}`" for module in unresolved)
            + ": no installed distributions are visible, so an import name that "
            "differs from its distribution name (PIL/Pillow) cannot be matched "
            "and reporting it as undeclared would be a false positive.\n"
            "Fix: run this in the project environment, e.g.\n"
            "  uv run assets/check_antipatterns.py <paths>\n"
            "or install the dependencies first with `uv sync`."
        )
    return violations, None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Scan Python files for antipatterns that linters cannot express.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Only rules without a Ruff equivalent live here. For `global` (PLW0603),\n"
            "`# noqa` (PGH004/RUF100), `os.path` (PTH), `Optional[T]` (UP045) and inline\n"
            "imports (PLC0415) configure the linter instead of adding a scanner."
        ),
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=[Path(".")],
        help="Files or directories to scan.",
    )
    parser.add_argument(
        "--ban-noqa",
        action="append",
        default=[],
        metavar="CODE",
        help="Rule code that must never appear in a `# noqa` comment (repeatable).",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=None,
        help="Directory holding pyproject.toml. Default: nearest marker above the first path.",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        metavar="GLOB",
        help=(
            "Directory-name or glob to skip (repeatable). Use for deliberately "
            "non-compliant fixtures, e.g. --exclude examples."
        ),
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON output.")
    args = parser.parse_args(argv)

    targets = [path.resolve() for path in args.paths]
    if args.project_root is not None:
        explicit_root = args.project_root.resolve()
        if not explicit_root.is_dir():
            print(
                f"ERROR: --project-root {explicit_root} is not a directory - "
                "refusing to guess dependency facts. Fix the path.",
                file=sys.stderr,
            )
            return 2
        if not (explicit_root / "pyproject.toml").is_file():
            print(
                f"ERROR: --project-root {explicit_root} holds no pyproject.toml - "
                "every guarded import would look undeclared and be reported.\n"
                "Fix: point --project-root at the directory containing it, or "
                "omit the flag to auto-detect.",
                file=sys.stderr,
            )
            return 2
        root = explicit_root
    else:
        detected = _project_root(targets[0])
        if detected is None:
            print(
                "ERROR: no pyproject.toml found at or above "
                f"{targets[0]}, so the dependency facts that `IMPORT-ERROR-GUARD` "
                "judges against do not exist.\n"
                "Fix: pass --project-root <dir-with-pyproject.toml>. Refusing to "
                "fall back to the working directory, which would judge these "
                "files against an unrelated project's dependencies.",
                file=sys.stderr,
            )
            return 2
        root = detected.resolve()

    discovery_errors: list[str] = []
    files = discover_python_files(targets, discovery_errors, args.exclude)
    if discovery_errors:
        for message in discovery_errors:
            print(f"ERROR: {message}", file=sys.stderr)
        return 2
    if not files:
        print(
            "ERROR: no Python files scanned under "
            + ", ".join(str(target) for target in targets)
            + " - refusing to report success.\n"
            "Fix: check the path, or pass --exclude for directories that only "
            "hold non-Python files.",
            file=sys.stderr,
        )
        return 2

    required, optional, pyproject_error = _read_pyproject(root)
    if pyproject_error is not None:
        print(f"ERROR: {pyproject_error}", file=sys.stderr)
        return 2
    # An empty distribution map is not fatal by itself: literal matches still
    # work and PEP 723 scripts never need it. It only becomes a failed scan when
    # a guard actually needs an alias resolved, which scan_file reports.
    facts = DependencyFacts(
        required=required,
        optional=optional,
        module_to_distribution=_module_distribution_map(),
    )
    banned = frozenset(code.upper() for code in args.ban_noqa)
    if banned:
        known = _known_ruff_codes()
        if known is None:
            print(
                "NOTE: cannot verify --ban-noqa codes (Ruff not runnable here), so "
                "a mistyped code would silently never match. Install Ruff in the "
                "environment to check them.",
                file=sys.stderr,
            )
        else:
            unknown = sorted(code for code in banned if code not in known)
            if unknown:
                print(
                    "ERROR: --ban-noqa names "
                    + ", ".join(unknown)
                    + " which Ruff does not define, so it can never match a "
                    "directive Ruff honours and the ban silently does nothing.\n"
                    "Fix: use the rule code you meant, e.g. PLC0415 or B008.",
                    file=sys.stderr,
                )
                return 2

    violations: list[Violation] = []
    parse_errors: list[str] = []
    for path in files:
        found, error = scan_file(path, facts, banned)
        violations.extend(found)
        if error is not None:
            parse_errors.append(error)

    if args.json:
        print(
            json.dumps(
                {
                    "violations": [violation.as_dict(root) for violation in violations],
                    "parse_errors": parse_errors,
                    "summary": _summarize(violations),
                    "total": len(violations),
                    "files_scanned": len(files),
                },
                indent=2,
            )
        )
    else:
        _report(violations, parse_errors, root, files)
    return 2 if parse_errors else (1 if violations else 0)


def _project_root(start: Path) -> Path | None:
    """Nearest ancestor of *start* holding a ``pyproject.toml`` marker.

    Returns ``None`` rather than falling back to the working directory. A cwd
    fallback silently substitutes an unrelated project's dependencies: a guard
    around a module that *that* project declares optional is then exempted,
    which is a false negative produced entirely by the wrong file.
    """
    origin = start if start.is_dir() else start.parent
    for candidate in (origin, *origin.parents):
        if (candidate / "pyproject.toml").is_file():
            return candidate
    return None


def _known_ruff_codes() -> frozenset[str] | None:
    """Rule codes Ruff defines, or ``None`` when Ruff cannot be asked.

    Asking the installed Ruff means ``--ban-noqa ZZZ999`` is an error instead of
    a rule that can never match. Returning ``None`` (Ruff absent, or its output
    unparseable) keeps the scanner usable without Ruff; the ban still works, it
    is just unverified.

    ``ruff rule --all`` is the command that enumerates rule codes;
    ``ruff linter`` lists the 59 linter *plugins* and would reject every real
    code such as ``PLC0415``.
    """
    try:
        result = subprocess.run(
            ["ruff", "rule", "--all", "--output-format", "json"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=_RUFF_TIMEOUT_SECONDS,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0 or not (result.stdout or "").strip():
        return None
    try:
        rules = json.loads(result.stdout)
    except json.JSONDecodeError:
        return None
    codes = {
        str(rule["code"]).upper()
        for rule in rules
        if isinstance(rule, dict) and rule.get("code")
    }
    return frozenset(codes) or None


def _summarize(violations: list[Violation]) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for violation in violations:
        counts[violation.rule] += 1
    return dict(sorted(counts.items()))


def _report(
    violations: list[Violation], parse_errors: list[str], root: Path, files: list[Path]
) -> None:
    by_rule = _summarize(violations)
    touched = len({violation.file for violation in violations})
    print(
        f"check-antipatterns: {len(violations)} violation(s) in {touched} file(s) "
        f"with findings, {len(files)} file(s) scanned"
    )
    if parse_errors:
        # The counts above exclude every file below: without this line a run that
        # judged nothing reads exactly like a clean one.
        print(
            f"  INCOMPLETE: {len(parse_errors)} file(s) could not be judged, so "
            "the counts above are not a clean result."
        )
    if by_rule:
        print("  by rule:")
        for rule, count in by_rule.items():
            print(f"    {rule}: {count}")
    if violations:
        print()
        for violation in violations:
            print(f"  {violation.format(root)}")
    for error in parse_errors:
        print(f"ERROR: {error}", file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main())
