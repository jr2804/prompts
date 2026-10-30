# /// script
# requires-python = ">=3.10"
# ///

"""Preview or apply a textual Python-identifier rename across a project."""

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

IGNORED_DIRECTORY_NAMES = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "venv",
}


@dataclass(frozen=True, slots=True)
class PlannedChange:
    file_path: Path
    replacement_count: int
    updated_text: str


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--old", required=True, help="Existing identifier")
    parser.add_argument("--new", required=True, help="Replacement identifier")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write the planned replacements (default: preview only)",
    )
    args = parser.parse_args()
    if not args.root.is_dir():
        parser.error(f"Root directory does not exist: {args.root}")

    try:
        changes = plan_identifier_rename(args.root, args.old, args.new)
    except ValueError as error:
        parser.error(str(error))
    replacement_total = sum(change.replacement_count for change in changes)
    for change in changes:
        print(f"{change.file_path}: {change.replacement_count} replacement(s)")

    if not changes:
        print("No matches found.")
        return

    if not args.apply:
        print(
            f"Preview only: {replacement_total} replacement(s) in "
            f"{len(changes)} file(s). Review the scope, then rerun with --apply."
        )
        return

    for change in changes:
        change.file_path.write_text(change.updated_text, encoding="utf-8")
    print(
        f"Applied {replacement_total} replacement(s) in "
        f"{len(changes)} file(s). Run the relevant tests and checks."
    )


def plan_identifier_rename(
    root_dir: Path,
    old_name: str,
    new_name: str,
) -> list[PlannedChange]:
    """Find textual identifier matches without modifying files."""
    if not old_name.isidentifier() or not new_name.isidentifier():
        raise ValueError("Old and new names must be valid Python identifiers")

    pattern = re.compile(rf"\b{re.escape(old_name)}\b")
    changes: list[PlannedChange] = []
    for path in sorted(root_dir.rglob("*.py")):
        if any(part in IGNORED_DIRECTORY_NAMES for part in path.parts):
            continue
        original_text = path.read_text(encoding="utf-8")
        updated_text, replacement_count = pattern.subn(new_name, original_text)
        if replacement_count:
            changes.append(
                PlannedChange(
                    file_path=path,
                    replacement_count=replacement_count,
                    updated_text=updated_text,
                )
            )
    return changes


if __name__ == "__main__":
    main()
