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

Examples:
    uv run check_path_naming.py output_file
    # Output: is_file

    uv run check_path_naming.py cache_dir
    # Output: is_dir

    uv run check_path_naming.py --check-files src/
    # Output: List of violations in Python files
"""

from __future__ import annotations

import argparse
import enum
import re
import sys
from pathlib import Path


class PathValidity(enum.StrEnum):
    """Validation results for path variable naming."""

    FILE = "is_file"
    DIR = "is_dir"
    PATH = "is_path_exceptional"
    INVALID = "invalid"


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

    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
