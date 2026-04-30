# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

"""Validate file/directory variable naming conventions.

This script checks if a given variable name follows the python-ultimate
naming conventions for files, directories, and paths.

Usage:
    uv run check_path_naming.py <name>
    uv run check_path_naming.py --check-files <python-file-or-directory>
    uv run check_path_naming.py --check-forbidden <python-file-or-directory>

Examples:
    uv run check_path_naming.py output_file
    # Output: is_file

    uv run check_path_naming.py cache_dir
    # Output: is_dir

    uv run check_path_naming.py --check-files src/
    # Output: List of violations in Python files

    uv run check_path_naming.py --check-forbidden src/
    # Output: List of forbidden pattern matches in Python files
"""

from __future__ import annotations

import argparse
import ast
import enum
import io
import re
import sys
import tokenize
from pathlib import Path


class PathValidity(enum.StrEnum):
    """Validation results for path variable naming."""

    FILE = "is_file"
    DIR = "is_dir"
    PATH = "is_path_exceptional"
    INVALID = "invalid"


FORBIDDEN_REASON: dict[str, str] = {
    "TYPE_CHECKING guard": "Avoid TYPE_CHECKING guards. Refactor imports/types as described in references/type-checking.md.",
    "Optional[T]": "Use pipe syntax (T | None) instead of Optional[T].",
    "os.path usage": "Use pathlib.Path instead of os.path.",
    "noqa suppression": "Fix the underlying lint issue instead of suppressing with # noqa.",
    "sys.path manipulation": "Avoid sys.path manipulation. Use proper package/module layout and imports.",
    "defensive required import": "Check whether this ImportError guard is wrapping a required dependency import.",
}


def check_path_naming(name: str | Path) -> PathValidity:
    """Check if a variable name follows file/directory naming conventions.

    Naming conventions:
    - Variables for files must end with "_file" suffix
    - Variables for directories must end with "_dir" suffix
    - "_path" suffix is only allowed in exceptional cases when
      the type cannot be clearly determined
    - Anti-patterns like "path", "dir_output", "file_output" are invalid
    - Bare generic names (path, file, folder, dir, directory, etc.) are invalid
      when they represent file system paths

    Args:
        name: Variable name to check (string or Path object)

    Returns:
        PathValidity enum indicating the naming validity

    Examples:
        >>> check_path_naming("output_file")
        <PathValidity.FILE: 'is_file'>
        >>> check_path_naming("cache_dir")
        <PathValidity.DIR: 'is_dir'>
        >>> check_path_naming("data_path")
        <PathValidity.PATH: 'is_path_exceptional'>
        >>> check_path_naming("path")
        <PathValidity.INVALID: 'invalid'>
        >>> check_path_naming("folder")
        <PathValidity.INVALID: 'invalid'>
    """
    # Convert Path to string if needed
    var_name = str(name)

    # Strip any Path parent components, get just the name
    var_name = Path(var_name).name if "/" in var_name or "\\" in var_name else var_name

    # Anti-patterns - bare generic names for path-related variables
    # These are always invalid when representing file system paths
    generic_path_names = {
        "path",
        "file",
        "folder",
        "dir",
        "directory",
        "output",
        "input",
        "source",
        "target",
        "dest",
        "destination",
    }
    if var_name in generic_path_names:
        return PathValidity.INVALID

    # "dir" or "file" as prefix instead of suffix
    if var_name.startswith("dir_") or var_name.startswith("file_"):
        return PathValidity.INVALID

    # Check for valid suffixes (in order of specificity)
    if var_name.endswith("_file"):
        return PathValidity.FILE

    if var_name.endswith("_dir"):
        return PathValidity.DIR

    if var_name.endswith("_path"):
        return PathValidity.PATH

    # No valid suffix found
    return PathValidity.INVALID


def get_violation_reason(name: str, validity: PathValidity) -> str | None:
    """Get human-readable explanation for invalid naming.

    Args:
        name: The variable name that was checked
        validity: The validation result

    Returns:
        Explanation string if invalid, None if valid
    """
    if validity == PathValidity.FILE:
        return None
    if validity == PathValidity.DIR:
        return None
    if validity == PathValidity.PATH:
        return None

    # Generic bare names for path-related variables
    generic_path_names = {
        "path",
        "file",
        "folder",
        "dir",
        "directory",
        "output",
        "input",
        "source",
        "target",
        "dest",
        "destination",
    }
    if name in generic_path_names:
        return (
            f"'{name}' is a bare generic name - too ambiguous for path variables. "
            f"Use descriptive names like '{name}_file' or '{name}_dir' "
            f"(e.g., 'input_file', 'output_dir', 'source_dir')"
        )

    # Invalid cases
    if name.startswith("dir_"):
        return f"'{name}' uses 'dir_' as prefix - use '_dir' suffix instead (e.g., '{name[4:]}_dir')"

    if name.startswith("file_"):
        return f"'{name}' uses 'file_' as prefix - use '_file' suffix instead (e.g., '{name[5:]}_file')"

    if name.endswith("_path"):
        return f"'{name}' ends with '_path' - only use for exceptional cases when type is unknown"

    return f"'{name}' missing required suffix - use '_file' for files, '_dir' for directories"


def scan_python_file(file_path: Path) -> list[tuple[int, str, str]]:
    """Scan a Python file for path variable naming violations.

    Args:
        file_path: Path to Python file to scan

    Returns:
        List of (line_number, variable_name, reason) tuples for violations
    """
    violations: list[tuple[int, str, str]] = []

    # Pattern to match variable assignments with Path or path-like values
    # Matches: var_name = Path(...), var_name = some/path, etc.
    assignment_patterns = [
        # Direct Path assignments: name = Path(
        re.compile(r"(\w+)\s*=\s*Path\("),
        # Path with method calls: name = Path.home(), name = Path.cwd()
        re.compile(r"(\w+)\s*=\s*Path\.\w+"),
        # String paths that look like files: name = "..." with path indicators
        re.compile(r"(\w+)\s*=\s*['\"].*[/\\\\].*\.\w+['\"]"),
        # String paths that look like dirs: name = ".../dir" or name = ".../dir/"
        re.compile(r"(\w+)\s*=\s*['\"].*[/\\\\]\w+/?['\"]$"),
    ]

    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception:
        return violations

    for line_num, line in enumerate(content.splitlines(), 1):
        # Skip comments and docstrings
        stripped = line.strip()
        if (
            stripped.startswith("#")
            or stripped.startswith('"""')
            or stripped.startswith("'''")
        ):
            continue

        for pattern in assignment_patterns:
            match = pattern.search(line)
            if match:
                var_name = match.group(1)
                validity = check_path_naming(var_name)

                if validity == PathValidity.INVALID:
                    reason = get_violation_reason(var_name, validity)
                    if reason:
                        violations.append((line_num, var_name, reason))
                break  # Only report first match per line

    return violations


def scan_directory(directory: Path) -> dict[Path, list[tuple[int, str, str]]]:
    """Recursively scan directory for Python files with violations.

    Args:
        directory: Directory to scan

    Returns:
        Dictionary mapping file paths to their violation lists
    """
    all_violations: dict[Path, list[tuple[int, str, str]]] = {}

    for py_file in directory.rglob("*.py"):
        violations = scan_python_file(py_file)
        if violations:
            all_violations[py_file] = violations

    return all_violations


def scan_forbidden_patterns(file_path: Path) -> list[tuple[int, str, str]]:
    """Scan a Python file for forbidden-style patterns.

    Args:
        file_path: Path to Python file to scan

    Returns:
        List of (line_number, pattern_name, reason) tuples for matches
    """
    matches: list[tuple[int, str, str]] = []

    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception:
        return matches

    found: set[tuple[int, str]] = set()

    try:
        tree = ast.parse(content)
    except SyntaxError:
        return matches

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "typing":
            if any(alias.name == "TYPE_CHECKING" for alias in node.names):
                found.add((node.lineno, "TYPE_CHECKING guard"))

        if isinstance(node, ast.If):
            if isinstance(node.test, ast.Name) and node.test.id == "TYPE_CHECKING":
                found.add((node.lineno, "TYPE_CHECKING guard"))

        if isinstance(node, ast.Subscript):
            value = node.value
            if isinstance(value, ast.Name) and value.id == "Optional":
                found.add((node.lineno, "Optional[T]"))
            if (
                isinstance(value, ast.Attribute)
                and isinstance(value.value, ast.Name)
                and value.value.id == "typing"
                and value.attr == "Optional"
            ):
                found.add((node.lineno, "Optional[T]"))

        if isinstance(node, ast.Import):
            if any(alias.name == "os.path" for alias in node.names):
                found.add((node.lineno, "os.path usage"))

        if isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name):
                if node.value.id == "os" and node.attr == "path":
                    found.add((node.lineno, "os.path usage"))
                if node.value.id == "sys" and node.attr == "path":
                    found.add((node.lineno, "sys.path manipulation"))

        if isinstance(node, ast.ExceptHandler) and node.type is not None:
            if isinstance(node.type, ast.Name) and node.type.id == "ImportError":
                found.add((node.lineno, "defensive required import"))

    token_stream = tokenize.generate_tokens(io.StringIO(content).readline)
    for token in token_stream:
        if token.type == tokenize.COMMENT and re.search(r"#\s*noqa\b", token.string, re.IGNORECASE):
            found.add((token.start[0], "noqa suppression"))

    for line_num, pattern_name in sorted(found):
        matches.append((line_num, pattern_name, FORBIDDEN_REASON[pattern_name]))

    return matches


def scan_directory_forbidden(directory: Path) -> dict[Path, list[tuple[int, str, str]]]:
    """Recursively scan directory for forbidden-style pattern matches.

    Args:
        directory: Directory to scan

    Returns:
        Dictionary mapping file paths to their forbidden-style matches
    """
    all_matches: dict[Path, list[tuple[int, str, str]]] = {}

    for py_file in directory.rglob("*.py"):
        file_matches = scan_forbidden_patterns(py_file)
        if file_matches:
            all_matches[py_file] = file_matches

    return all_matches


def main() -> int:
    """Main entry point for CLI usage."""
    parser = argparse.ArgumentParser(
        description="Validate file/directory variable naming conventions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run %(prog)s output_file           # Check single name
  uv run %(prog)s cache_dir             # Returns: is_dir
  uv run %(prog)s --check-files src/    # Scan directory for violations
    uv run %(prog)s --check-forbidden src/  # Scan directory for forbidden patterns
        """,
    )

    parser.add_argument(
        "name",
        nargs="?",
        help="Variable name to check (e.g., 'output_file', 'cache_dir')",
    )

    parser.add_argument(
        "--check-files",
        metavar="PATH",
        help="Scan Python file or directory for naming violations",
    )

    parser.add_argument(
        "--check-forbidden",
        metavar="PATH",
        help="Scan Python file or directory for forbidden-style patterns",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed output with explanations",
    )

    args = parser.parse_args()

    # Check single name
    if args.name:
        validity = check_path_naming(args.name)
        print(validity)

        if args.verbose and validity == PathValidity.INVALID:
            reason = get_violation_reason(args.name, validity)
            if reason:
                print(f"Reason: {reason}", file=sys.stderr)

        return 0 if validity != PathValidity.INVALID else 1

    # Check files
    if args.check_files:
        check_path = Path(args.check_files)

        if not check_path.exists():
            print(f"Error: Path not found: {check_path}", file=sys.stderr)
            return 2

        if check_path.is_file():
            violations = scan_python_file(check_path)
            if violations:
                print(f"\nFound {len(violations)} violation(s) in {check_path}:")
                for line_num, var_name, reason in violations:
                    print(f"  Line {line_num}: {reason}")
                return 1
            else:
                print(f"No violations found in {check_path}")
                return 0

        elif check_path.is_dir():
            violations = scan_directory(check_path)
            total = sum(len(v) for v in violations.values())

            if violations:
                print(f"\nFound {total} violation(s) in {len(violations)} file(s):\n")
                for file_path, file_violations in violations.items():
                    print(f"{file_path}:")
                    for line_num, var_name, reason in file_violations:
                        print(f"  Line {line_num}: {reason}")
                    print()
                return 1
            else:
                print(f"No violations found in {check_path}")
                return 0

    # Check forbidden-style patterns
    if args.check_forbidden:
        check_path = Path(args.check_forbidden)

        if not check_path.exists():
            print(f"Error: Path not found: {check_path}", file=sys.stderr)
            return 2

        if check_path.is_file():
            matches = scan_forbidden_patterns(check_path)
            if matches:
                print(f"\nFound {len(matches)} forbidden pattern match(es) in {check_path}:")
                for line_num, pattern_name, reason in matches:
                    print(f"  Line {line_num}: [{pattern_name}] {reason}")
                return 1
            else:
                print(f"No forbidden pattern matches found in {check_path}")
                return 0

        if check_path.is_dir():
            matches = scan_directory_forbidden(check_path)
            total = sum(len(v) for v in matches.values())

            if matches:
                print(f"\nFound {total} forbidden pattern match(es) in {len(matches)} file(s):\n")
                for file_path, file_matches in matches.items():
                    print(f"{file_path}:")
                    for line_num, pattern_name, reason in file_matches:
                        print(f"  Line {line_num}: [{pattern_name}] {reason}")
                    print()
                return 1

            print(f"No forbidden pattern matches found in {check_path}")
            return 0

    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
