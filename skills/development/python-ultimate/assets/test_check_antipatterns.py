# /// script
# requires-python = ">=3.10"
# dependencies = ["ruff"]
# ///

"""Pin the exit-code contract documented in ``references/linter-rules.md``.

The rules below are prose in a reference file, and prose is not enforcement. A
future edit can move a guard back to ``main()``, widen a parameter to
``| None``, or let a scanner treat an unreadable file as clean, and every
existing check still passes. This file is the check that fails.

Two halves, and the second is the one usually missing:

1. **Every documented exit-2 cause really exits 2.** The reference file lists
   them; a cause that stops working is silently a pass again.
2. **Honest runs still pass.** Guarding a missing fact too early makes scans
   fail that established everything they needed. Absence is easy to test by
   emptying an input; over-guarding is only visible by asserting the
   complementary case, so each "cannot derive" case is paired with a run that
   must NOT fail for the same reason.

Run with ``uv run assets/test_check_antipatterns.py`` from the skill directory.
"""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

scanner_file = Path(__file__).with_name("check_antipatterns.py")

PROJECT_WITH_REQUESTS = """\
[project]
name = "demo"
version = "0.1.0"
dependencies = ["requests"]
"""

BUILD_SYSTEM_ONLY = """\
[build-system]
requires = ["hatchling"]
"""

# Triple-quoted rather than one escaped line: the scanner's own naming rules
# treat a long escaped literal with slashes as a path-like value.
# ``uv`` scans the entire file for the PEP 723 start marker, so it must not
# appear literally here twice — this file is itself a PEP 723 script. Assembling
# the marker from pieces keeps the fixtures intact and the file runnable.
_START_MARKER = "# " + "/// script"
_END_MARKER = "# " + "///"


def pep723_script(dependencies: str, body: str) -> str:
    """Build a synthetic PEP 723 script for the fixtures below."""
    metadata = [
        _START_MARKER,
        '# requires-python = ">=3.10"',
        f"# dependencies = [{dependencies}]",
        _END_MARKER,
    ]
    return "\n".join([*metadata, body, ""])


SCRIPT_WITH_REQUESTS = pep723_script(
    '"requests"',
    "try:\n    import requests\nexcept ImportError:\n    requests = None",
)


class ScannerContractTest(unittest.TestCase):
    """Assert the documented exit codes, both the failures and the successes."""

    def setUp(self) -> None:
        self._temp = tempfile.TemporaryDirectory()
        self.root_dir = Path(self._temp.name)
        self.addCleanup(self._temp.cleanup)

    def write(self, relative: str, content: str, base: Path | None = None) -> Path:
        """Create a file under the temp root and return its path."""
        path = (base or self.root_dir) / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def run_scanner(
        self, *args: str | Path, isolated: bool = False
    ) -> subprocess.CompletedProcess[str]:
        """Run the scanner and return the completed process.

        *isolated* hides installed distributions, which is how the empty
        import-to-distribution map is reproduced without uninstalling anything.
        """
        command = [sys.executable]
        if isolated:
            command += ["-I", "-S"]
        command += [str(scanner_file), *[str(argument) for argument in args]]
        return subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

    def assertExit(self, process: subprocess.CompletedProcess[str], expected: int):
        """Assert the exit code, showing the output when it differs."""
        self.assertEqual(
            process.returncode,
            expected,
            msg=(
                f"expected exit {expected}, got {process.returncode}\n"
                f"stdout:\n{process.stdout}\nstderr:\n{process.stderr}"
            ),
        )

    def guarded_dependency(self, project: str, module: str) -> Path:
        """Build a project whose single file guards *module*, and return the root."""
        self.write("pyproject.toml", project)
        self.write(
            "module.py",
            f"try:\n    import {module}\nexcept ImportError:\n    {module} = None\n",
        )
        return self.root_dir

    # Each documented "could not establish the facts" cause must exit 2.
    # A cause that regresses to exit 0 is a vacuous pass, which is the whole
    # point of the contract.

    def test_empty_directory_exits_2(self) -> None:
        empty = self.root_dir / "empty"
        empty.mkdir()
        self.assertExit(self.run_scanner(empty), 2)

    def test_nonexistent_path_exits_2(self) -> None:
        """A typo must not silently narrow the scan to the paths that exist."""
        self.guarded_dependency(PROJECT_WITH_REQUESTS, "requests")
        self.assertExit(self.run_scanner(self.root_dir, self.root_dir / "typo"), 2)

    def test_project_root_without_pyproject_exits_2(self) -> None:
        self.guarded_dependency(PROJECT_WITH_REQUESTS, "requests")
        bare = self.root_dir / "bare"
        bare.mkdir()
        self.assertExit(self.run_scanner(self.root_dir, "--project-root", bare), 2)

    def test_no_discoverable_pyproject_exits_2(self) -> None:
        """Refuse the cwd fallback rather than judging against an unrelated project."""
        lonely = self.root_dir / "lonely"
        lonely.mkdir()
        self.write(
            "module.py",
            "try:\n    import orjson\nexcept ImportError:\n    orjson = None\n",
            base=lonely,
        )
        self.assertExit(self.run_scanner(lonely), 2)

    def test_build_system_only_root_exits_2(self) -> None:
        """A virtual workspace root declares nothing, so it cannot judge guards."""
        orphan = self.root_dir / "orphan"
        orphan.mkdir()
        self.write("pyproject.toml", BUILD_SYSTEM_ONLY, base=orphan)
        self.write(
            "module.py",
            "try:\n    import orjson\nexcept ImportError:\n    orjson = None\n",
            base=orphan,
        )
        self.assertExit(self.run_scanner(orphan), 2)

    def test_unparseable_file_exits_2(self) -> None:
        self.guarded_dependency(PROJECT_WITH_REQUESTS, "requests")
        self.write("broken.py", "def broken(:\n")
        self.assertExit(self.run_scanner(self.root_dir), 2)

    def test_malformed_pep723_block_exits_2(self) -> None:
        """An unreadable block must not read as 'declares nothing'.

        An empty dependency set exempts every guard in the file, so a malformed
        block would switch the rule off while reporting a clean scan.
        """
        self.guarded_dependency(PROJECT_WITH_REQUESTS, "requests")
        self.write(
            "bad_metadata.py",
            pep723_script(
                '"requests",,,',
                "try:\n    import requests\nexcept ImportError:\n    requests = None",
            ),
        )
        self.assertExit(self.run_scanner(self.root_dir / "bad_metadata.py"), 2)

    @unittest.skipUnless(shutil.which("ruff"), "Ruff is needed to validate codes")
    def test_unknown_ban_noqa_code_exits_2(self) -> None:
        """A ban on a code Ruff does not define can never match."""
        self.guarded_dependency(PROJECT_WITH_REQUESTS, "requests")
        self.assertExit(
            self.run_scanner(self.root_dir, "--ban-noqa", "NOTAREALCODE"), 2
        )

    # The complementary half: facts that were established must not be treated
    # as missing. These are the cases an over-eager guard breaks.

    def test_clean_file_exits_0(self) -> None:
        """A guard on an optional-declared module is the legitimate use."""
        self.write(
            "pyproject.toml",
            PROJECT_WITH_REQUESTS
            + '\n[project.optional-dependencies]\nfast = ["orjson"]\n',
        )
        self.write(
            "clean.py",
            "try:\n    import orjson\nexcept ImportError:\n    orjson = None\n",
        )
        self.assertExit(self.run_scanner(self.root_dir / "clean.py"), 0)

    def test_literal_dependency_needs_no_distribution_map(self) -> None:
        """``requests`` matches a declared ``requests`` without alias resolution.

        The distribution map resolves ``PIL`` to ``Pillow``. A literal name needs
        none of that, so an empty map must not fail the scan.
        """
        self.guarded_dependency(PROJECT_WITH_REQUESTS, "requests")
        self.assertExit(
            self.run_scanner(self.root_dir / "module.py", isolated=True),
            1,
        )

    def test_alias_needs_the_distribution_map_or_fails_loudly(self) -> None:
        """Without the map an alias is *unknown*, not undeclared.

        Reporting it as undeclared would invent a finding; passing it silently
        would hide one. Neither is acceptable, so the scan fails instead.
        """
        self.guarded_dependency(PROJECT_WITH_REQUESTS, "PIL")
        process = self.run_scanner(self.root_dir / "module.py", isolated=True)
        self.assertExit(process, 2)
        self.assertIn("PIL", process.stderr)

    def test_pep723_script_never_consults_the_map(self) -> None:
        """Script dependencies come from the block, so an empty map is harmless."""
        script_file = self.write("script.py", SCRIPT_WITH_REQUESTS)
        self.assertExit(self.run_scanner(script_file, isolated=True), 1)

    def test_script_only_tree_never_silently_exempts_aliases(self) -> None:
        """No ``pyproject.toml`` must not empty the environment-derived map.

        The project facts and the import-to-distribution index have different
        provenance. Folding them into one optional object meant a script-only
        tree got an empty resolver, so ``PIL`` could not match a declared
        ``pillow`` and the guard was silently exempted as an undeclared probe -
        a false negative produced by a missing project file the script never
        reads.

        The exit code depends on whether ``pillow`` is installed here, which the
        test cannot control, so it asserts the property that holds either way:
        the guard is never silently dropped. Installed, the alias resolves and
        the guard is reported; absent, the alias is unprovable and the scan
        fails. Before the fix both cases exited 0.
        """
        script = self.write(
            "alias_script.py",
            pep723_script(
                '"pillow"',
                "try:\n    from PIL import Image\nexcept ImportError:\n    Image = None",
            ),
        )
        process = self.run_scanner(script)
        combined = process.stdout + process.stderr
        self.assertIn("PIL", combined)
        self.assertIn(
            process.returncode, (1, 2), f"guard was silently dropped:\n{combined}"
        )

    def test_script_with_no_declarations_needs_no_resolver(self) -> None:
        """An alias question is vacuous when there is nothing it could match.

        This is the complementary half of the test above: requiring a resolver
        unconditionally would turn an honest pass into a failed scan whenever a
        script declares nothing at all.
        """
        script = self.write(
            "optional_probe.py",
            pep723_script(
                "",
                "try:\n    import orjson\nexcept ImportError:\n    orjson = None",
            ),
        )
        self.assertExit(self.run_scanner(script, isolated=True), 0)


if __name__ == "__main__":
    unittest.main()
