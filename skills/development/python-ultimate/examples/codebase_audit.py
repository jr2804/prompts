"""
Example: Comprehensive Codebase Audit

Analyze code quality across entire project with minimal tokens.
"""

import ast
from pathlib import Path


def analyze_file_complexity(file_path: Path) -> dict:
    """Extract complexity metrics from Python file."""
    try:
        tree = ast.parse(file_path.read_text())
    except SyntaxError:
        return {"error": "syntax_error"}

    functions = []
    total_complexity = 0

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Simple complexity: count nested control flow
            nested = sum(
                1
                for n in ast.walk(node)
                if isinstance(n, (ast.If, ast.For, ast.While, ast.With))
            )
            functions.append({"name": node.name, "complexity": nested})
            total_complexity += nested

    lines = len(file_path.read_text().splitlines())

    return {
        "lines": lines,
        "functions": len(functions),
        "total_complexity": total_complexity,
        "avg_complexity": total_complexity / len(functions) if functions else 0,
        "function_details": functions,
    }


def audit_codebase(directory: Path) -> dict:
    """Audit all Python files in directory."""
    files = list(directory.rglob("*.py"))
    print(f"Analyzing {len(files)} files...")

    issues = {
        "high_complexity": [],
        "large_files": [],
    }

    for file in files:
        analysis = analyze_file_complexity(file)

        # Flag high complexity
        if analysis.get("avg_complexity", 0) > 10:
            issues["high_complexity"].append({
                "file": str(file),
                "avg_complexity": analysis["avg_complexity"],
            })

        # Flag large files
        if analysis.get("lines", 0) > 500:
            issues["large_files"].append({
                "file": str(file),
                "lines": analysis["lines"],
            })

    # Return summary only (NOT all the data!)
    return {
        "files_audited": len(files),
        "issues": {
            "high_complexity": len(issues["high_complexity"]),
            "large_files": len(issues["large_files"]),
        },
        "top_complexity": sorted(
            issues["high_complexity"],
            key=lambda x: x["avg_complexity"],
            reverse=True,
        )[:5],  # Only top 5
    }


# Example usage
if __name__ == "__main__":
    result = audit_codebase(Path("src"))
    print(f"\nAudit complete:")
    print(f"  Files audited: {result['files_audited']}")
    print(f"  High complexity files: {result['issues']['high_complexity']}")
    print(f"  Large files (>500 lines): {result['issues']['large_files']}")
