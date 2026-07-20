# /// script
# requires-python = ">=3.11,<3.12"
# dependencies = [
#     "rich>=13.7,<15",
# ]
# ///

"""Demonstrate a PEP 723 standalone script targeting 32-bit Python 3.11.

This file is a companion to
``skills/development/python-ultimate/references/uv-python-versions.md`` and
``references/uv-scripts.md``.

Why this script exists
----------------------
``uv`` does not ship 32-bit CPython (Astral's python-build-standalone builds are
x86_64 only on Windows). To run a PEP 723 script under a 32-bit interpreter you
must point ``uv`` at a system-installed 32-bit Python via the ``--python`` flag.

The PEP 723 header above was created and must be maintained with::

    uv init --script examples/uv_script_32bit.py
    uv add --script examples/uv_script_32bit.py "rich>=13.7,<15"

Never edit the ``# /// script ... # ///`` block by hand.

Running on a 32-bit interpreter (Windows example)
-------------------------------------------------
1. Install Python 3.11 (32-bit) from https://www.python.org/downloads/windows/
   - Choose the "Windows installer (32-bit)" download.
   - Default install path (per-user):
       C:\\Users\\<user>\\AppData\\Local\\Programs\\Python\\Python311-32\\python.exe
   - All-users install path:
       C:\\Program Files (x86)\\Python311-32\\python.exe

2. Point ``uv`` at that interpreter explicitly::

       uv run --python "C:\\Program Files (x86)\\Python311-32\\python.exe" examples/uv_script_32bit.py

3. Or, if you have already pinned the version with ``uv python pin 3.11`` and the
   only 3.11 interpreter on the machine is the 32-bit one, plain ``uv run`` will
   pick it up::

       uv run examples/uv_script_32bit.py

Running on a 64-bit interpreter
-------------------------------
This script also runs under 64-bit Python 3.11 — the inline metadata only
constrains the minor version, not the architecture::

    uv run examples/uv_script_32bit.py

Verifying the architecture
--------------------------
The script prints ``platform.architecture()`` and the pointer size so you can
confirm which build is actually running.
"""

from __future__ import annotations

import platform
import struct
import sys


def main() -> None:
    """Print interpreter metadata using a declared dependency (rich)."""
    try:
        from rich.console import Console
        from rich.table import Table
    except ImportError as exc:  # pragma: no cover - defensive
        msg = (
            "rich is not installed. Run via `uv run` so PEP 723 deps resolve:\n"
            "  uv run --python <path-to-32bit-python> "
            "examples/uv_script_32bit.py"
        )
        raise SystemExit(msg) from exc

    console = Console()
    bits = struct.calcsize("P") * 8
    arch_label, _binary = platform.architecture()

    table = Table(title="Interpreter Report", show_header=True)
    table.add_column("Property", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")
    table.add_row("Python version", sys.version)
    table.add_row("Executable", sys.executable)
    table.add_row("platform.architecture()", arch_label)
    table.add_row("Pointer width", f"{bits} bit")
    table.add_row("Implementation", platform.python_implementation())
    table.add_row("GIL enabled", str(getattr(sys, "_is_gil_enabled", lambda: True)()))
    console.print(table)

    if bits == 32:
        console.print("[green]Running under a 32-bit interpreter.[/green]")
    else:
        console.print(
            "[yellow]Not 32-bit. To force 32-bit, pass "
            "--python <path-to-32bit-python>.[/yellow]"
        )


if __name__ == "__main__":
    main()
