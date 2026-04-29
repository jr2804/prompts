"""
Example: Extract Functions to New File

Find and move functions to a separate file with minimal token usage.
"""

import ast
import re
from pathlib import Path


def find_functions(file_path: Path, pattern: str) -> list[dict]:
    """Find function definitions matching regex pattern."""
    content = file_path.read_text()
    tree = ast.parse(content)

    functions = []
    lines = content.splitlines()

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if re.search(pattern, node.name):
                # Get function source lines
                start_line = node.lineno - 1  # AST is 1-indexed
                end_line = node.end_lineno
                functions.append({
                    "name": node.name,
                    "start_line": start_line,
                    "end_line": end_node,
                    "source": "\n".join(lines[start_line:end_line]),
                })

    return functions


def extract_functions_to_new_file(
    source_file: Path,
    target_file: Path,
    pattern: str,
) -> dict:
    """Extract matching functions from source to target file."""
    functions = find_functions(source_file, pattern)
    print(f"Found {len(functions)} functions matching '{pattern}'")

    if not functions:
        return {"functions_extracted": 0}

    # Extract imports from original file
    content = source_file.read_text()
    imports = [
        line
        for line in content.splitlines()
        if line.strip().startswith(("import ", "from "))
    ]

    # Create new file with imports
    target_file.write_text("\n".join(set(imports)) + "\n\n")

    # Append each function
    with target_file.open("a") as f:
        for func in functions:
            print(f"  Moving {func['name']} (lines {func['start_line']+1}-{func['end_line']})")
            f.write(func["source"] + "\n\n")

    # Return summary only
    return {
        "functions_extracted": len(functions),
        "function_names": [f["name"] for f in functions],
    }


# Example usage
if __name__ == "__main__":
    result = extract_functions_to_new_file(
        source_file=Path("app.py"),
        target_file=Path("utils.py"),
        pattern=r".*_util$",
    )
    print(f"\nExtracted {result['functions_extracted']} functions")
    print(f"Functions: {', '.join(result['function_names'])}")
