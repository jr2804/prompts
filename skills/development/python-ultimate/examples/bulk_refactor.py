"""
Example: Bulk Refactoring Across Entire Codebase

Rename identifiers across Python files using standard library.
"""

from pathlib import Path
import re


def rename_identifier(
    directory: Path,
    old_name: str,
    new_name: str,
    pattern: str = "*.py",
) -> dict:
    """Rename identifier across all matching files."""
    files_modified = 0
    total_replacements = 0

    for file_path in directory.rglob(pattern):
        content = file_path.read_text()
        new_content, replacements = re.subn(
            rf"\b{re.escape(old_name)}\b",
            new_name,
            content,
        )
        if replacements > 0:
            file_path.write_text(new_content)
            files_modified += 1
            total_replacements += replacements

    return {
        "files_modified": files_modified,
        "total_replacements": total_replacements,
    }


# Example usage
if __name__ == "__main__":
    result = rename_identifier(
        directory=Path("."),
        old_name="getUserData",
        new_name="fetchUserData",
    )
    print(f"Modified {result['files_modified']} files")
    print(f"Total replacements: {result['total_replacements']}")

    # Token-efficient: Only returns summary, not file contents
