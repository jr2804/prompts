# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""Common helpers for deterministic officecli XML operations."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import subprocess
from typing import Any


@dataclass
class CliResult:
    args: list[str]
    returncode: int
    stdout: str
    stderr: str


def run_officecli(args: list[str], *, check: bool = True, verbose: bool = False) -> CliResult:
    command = ["officecli", *args]
    proc = subprocess.run(command, capture_output=True, text=True, check=False)
    result = CliResult(command, proc.returncode, proc.stdout, proc.stderr)
    if verbose:
        print("$", " ".join(command))
        if result.stdout.strip():
            print(result.stdout.strip())
        if result.stderr.strip():
            print(result.stderr.strip())
    if check and result.returncode != 0:
        raise RuntimeError(f"officecli failed ({result.returncode}): {result.stderr.strip()}")
    return result


def load_json_spec(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("Spec root must be an object")
    return data


def raw_set(doc_path: str, xpath: str, action: str, xml: str, *, verbose: bool = False) -> CliResult:
    if action not in {"replace", "before", "after"}:
        raise ValueError(f"Unsupported action: {action}")
    if action == "replace" and xml == "":
        raise ValueError("Refusing destructive empty XML replace")
    args = [
        "raw-set",
        doc_path,
        "/document",
        "--xpath",
        xpath,
        "--action",
        action,
        "--xml",
        xml,
    ]
    return run_officecli(args, verbose=verbose)


def validate_doc(doc_path: str, *, verbose: bool = False) -> CliResult:
    return run_officecli(["validate", doc_path], verbose=verbose)
