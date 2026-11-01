# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

"""Find and safely move matching top-level functions into a new module."""

import argparse
import ast
import re
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FunctionInfo:
    """Source details for a matching function definition."""

    name: str
    start_line: int
    end_line: int
    source: str


@dataclass(frozen=True)
class ExtractionResult:
    """Summary of definitions moved into the target module."""

    functions_extracted: int
    function_names: tuple[str, ...] = ()


def find_functions(file_path: Path, pattern: str) -> list[FunctionInfo]:
    """Find matching module-level function definitions in a UTF-8 Python file."""
    with file_path.open("r", encoding="utf-8", newline="") as source:
        content = source.read()
    return _matching_functions(content, pattern)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_file", type=Path, help="Python module to edit")
    parser.add_argument(
        "target_file", type=Path, help="New module path; it must not exist"
    )
    parser.add_argument(
        "pattern", help="Regular expression matched against top-level function names"
    )
    args = parser.parse_args()

    try:
        result = extract_functions_to_new_file(
            source_file=args.source_file,
            target_file=args.target_file,
            pattern=args.pattern,
        )
    except (OSError, SyntaxError, ValueError, re.error) as error:
        parser.error(str(error))

    if result.functions_extracted == 0:
        print("No functions matched; source and target are unchanged.")
        return

    print(f"\nExtracted {result.functions_extracted} functions")
    print(f"Functions: {', '.join(result.function_names)}")


def extract_functions_to_new_file(
    source_file: Path,
    target_file: Path,
    pattern: str,
) -> ExtractionResult:
    """Move matching top-level defs to a new UTF-8 file without overwriting it.

    The target receives the source module's imports and matching definitions. The
    source definitions (including decorators) are removed only after the target
    has been created and the edited source has been staged successfully. This is a
    mechanical move: review module-level dependencies, callers, and imports because
    this helper does not migrate or rewrite them.
    """
    source_file = source_file.resolve()
    target_file = target_file.resolve()
    if source_file == target_file:
        raise ValueError("Source and target paths must be different")
    if target_file.exists():
        raise FileExistsError(f"Target already exists: {target_file}")

    with source_file.open("r", encoding="utf-8", newline="") as source:
        content = source.read()
    tree = ast.parse(content)
    functions = _matching_functions(content, pattern)
    if not functions:
        return ExtractionResult(functions_extracted=0)

    imports: list[str] = []
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            import_source = ast.get_source_segment(content, node)
            if import_source is None:
                raise ValueError("Could not read an import statement from source")
            imports.append(import_source)

    target_content = (
        "\n\n".join([*imports, *(function.source for function in functions)]) + "\n"
    )

    removed_lines = {
        line
        for function in functions
        for line in range(function.start_line, function.end_line + 1)
    }
    remaining_content = "".join(
        line
        for number, line in enumerate(content.splitlines(keepends=True), start=1)
        if number not in removed_lines
    )

    target_created = False
    staged_source_file: Path | None = None
    try:
        # Exclusive creation protects against a target appearing after the check.
        with target_file.open("x", encoding="utf-8", newline="\n") as target:
            target_created = True
            target.write(target_content)

        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=source_file.parent,
            delete=False,
        ) as staged:
            staged_source_file = Path(staged.name)
            staged.write(remaining_content)

        shutil.copystat(source_file, staged_source_file)
        staged_source_file.replace(source_file)
        staged_source_file = None
    except BaseException:
        # Clean up the partial move on errors and interruptions, then re-raise.
        if staged_source_file is not None:
            staged_source_file.unlink(missing_ok=True)
        if target_created:
            target_file.unlink(missing_ok=True)
        raise

    for function in functions:
        print(
            f"  Moving {function.name} "
            f"(lines {function.start_line}-{function.end_line})"
        )

    return ExtractionResult(
        functions_extracted=len(functions),
        function_names=tuple(function.name for function in functions),
    )


def _matching_functions(content: str, pattern: str) -> list[FunctionInfo]:
    """Return matching module-level functions, including decorators and async defs."""
    matcher = re.compile(pattern)
    tree = ast.parse(content)
    lines = content.splitlines()
    functions: list[FunctionInfo] = []

    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if not matcher.search(node.name):
            continue

        start_line = min(
            (decorator.lineno for decorator in node.decorator_list),
            default=node.lineno,
        )
        end_line = node.end_lineno or node.lineno
        functions.append(
            FunctionInfo(
                name=node.name,
                start_line=start_line,
                end_line=end_line,
                source="\n".join(lines[start_line - 1 : end_line]),
            )
        )

    return functions


if __name__ == "__main__":
    main()
