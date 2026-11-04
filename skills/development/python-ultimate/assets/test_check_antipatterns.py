# /// script
# requires-python = ">=3.10"
# dependencies = ["ruff", "pyyaml"]
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

import ast
import shutil
import subprocess
import sys
import tempfile
import types
import unittest
from importlib.metadata import packages_distributions
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

scanner_file = Path(__file__).with_name("check_antipatterns.py")


def _load_scanner_module() -> types.ModuleType:
    """Import the sibling scanner by path, without touching ``sys.path``.

    This file runs as a standalone PEP 723 script, so there is no package to
    import a sibling from. Loading it by path keeps the table under test and the
    table the scanner uses the *same object* - a copy in this file would go stale
    without anything failing.

    Done this way rather than with ``sys.path.insert``: the skill's antipattern
    index forbids ``sys.path`` manipulation, and a test that breaks the rule it
    is testing invites a reader to assume the rule has exceptions it does not
    have.
    """
    spec = spec_from_file_location("check_antipatterns_under_test", scanner_file)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {scanner_file} for the table tests")
    module = module_from_spec(spec)
    # Register before executing: ``@dataclass`` resolves each class through
    # ``sys.modules[cls.__module__]``, so an unregistered module raises
    # ``AttributeError: 'NoneType' object has no attribute '__dict__'`` at the
    # first dataclass in the file, far from the line that caused it.
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_scanner = _load_scanner_module()
_ALIAS_HINTS: dict[str, str] = _scanner._ALIAS_HINTS
_normalize = _scanner._normalize

PROJECT_WITH_REQUESTS = """\
[project]
name = "demo"
version = "0.1.0"
dependencies = ["requests"]
"""

PROJECT_WITH_PILLOW = """\
[project]
name = "demo"
version = "0.1.0"
dependencies = ["pillow"]
"""

PROJECT_WITH_PYYAML = """\
[project]
name = "demo"
version = "0.1.0"
dependencies = ["pyyaml"]
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
        self,
        *args: str | Path,
        isolated: bool = False,
        scanner: Path | None = None,
    ) -> subprocess.CompletedProcess[str]:
        """Run the scanner and return the completed process.

        *isolated* hides installed distributions, which is how the empty
        import-to-distribution map is reproduced without uninstalling anything.

        *scanner* overrides the script under test, so a test can run a copy with
        one fact deliberately removed and prove that the fact is load-bearing.
        """
        command = [sys.executable]
        if isolated:
            command += ["-I", "-S"]
        command += [str(scanner or scanner_file), *[str(argument) for argument in args]]
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

    def test_alias_resolves_without_the_distribution_map(self) -> None:
        """A hinted alias is decidable even when its distribution is absent.

        This test used to assert exit ``2`` here, on the reasoning that with no
        map entry for ``PIL`` the alias could not be resolved. That reasoning was
        wrong in the direction that matters: the hint table already says ``PIL``
        is ``pillow``, and a declared ``pillow`` guarded by an ``ImportError``
        handler is a finding. Declining the question produced an error where the
        scan had the answer.

        The undecidable case is a declaration with *no* hint, covered by
        ``test_unhinted_absent_declaration_makes_the_verdict_undecidable``.
        """
        self.guarded_dependency(PROJECT_WITH_PILLOW, "PIL")
        process = self.run_scanner(self.root_dir / "module.py", isolated=True)
        self.assertIn("PIL", process.stdout)
        self.assertExit(process, 1)

    def test_alias_hint_resolves_the_declaration_instead_of_bailing_out(self) -> None:
        """A hint exists so the alias can be *resolved*, not so the scan can give up.

        With ``pyyaml`` declared and absent from the environment, a guard on
        ``yaml`` is a guard around a declared dependency - dead weight, exit
        ``1``. The hint table is what makes that provable when
        ``importlib.metadata`` has no entry for an uninstalled distribution.

        An earlier version consulted the hints only to *raise* exit ``2``, so the
        scan had the fact that answers the question and chose an error over it.
        Knowledge that resolves an alias must resolve it.
        """
        self.guarded_dependency(PROJECT_WITH_PYYAML, "yaml")
        process = self.run_scanner(self.root_dir / "module.py", isolated=True)
        self.assertIn("yaml", process.stdout)
        self.assertExit(process, 1)

    def test_a_hinted_declaration_does_not_block_an_unrelated_probe(self) -> None:
        """Only declarations with *unknown* import names may block a verdict.

        ``pyyaml`` is declared, absent and hinted: nothing about it is unknown, and
        the hint names ``yaml``, not ``orjson``. So the probe of ``orjson`` is a
        genuine finding (exit ``1``) rather than an undecidable case.

        This is the sharpening that separates the per-item rule from a
        collection-wide one. Asking "is any declared dependency missing?" would
        answer yes here and bail out with exit ``2``, saying nothing about
        ``orjson``.
        """
        self.write("pyproject.toml", PROJECT_WITH_PYYAML)
        self.write(
            "module.py",
            "try:\n    import orjson\nexcept ImportError:\n    orjson = None\n",
        )
        process = self.run_scanner(self.root_dir / "module.py", isolated=True)
        self.assertIn("orjson", process.stdout)
        self.assertExit(process, 1)

    def test_unhinted_absent_declaration_makes_the_verdict_undecidable(self) -> None:
        """An absent declaration with no hint could own any import name.

        ``requests`` is declared and absent from a bare environment, and nothing
        says which import names it provides. Guarding ``orjson`` might be an
        honest probe of an undeclared accelerator, or it might be ``requests``
        imported under a name only ``importlib.metadata`` could confirm - and the
        distribution is not installed, so there is nothing to read.

        Either verdict would be invented, so the scan fails (exit ``2``). In a
        real project environment ``requests`` is installed, its import names are
        in the map, and this same file becomes a plain finding.
        """
        self.guarded_dependency(PROJECT_WITH_REQUESTS, "orjson")
        process = self.run_scanner(self.root_dir / "module.py", isolated=True)
        self.assertIn("orjson", process.stderr)
        self.assertExit(process, 2)

    def test_unrelated_missing_declaration_still_yields_a_finding(self) -> None:
        """A decidable declaration must not turn another module's probe into noise.

        Both declarations are hinted and absent, so nothing about either is
        unknown: ``pyyaml`` is ``yaml``, ``python-dateutil`` is ``dateutil``, and
        neither is ``orjson``. The probe is therefore a finding, exit ``1``.

        The version of this scan that asked "is any declared dependency
        missing?" answered yes, bailed out with exit ``2`` and said nothing about
        ``orjson`` - a collection statistic standing in for a per-item question.
        """
        self.write(
            "pyproject.toml",
            '[project]\nname = "demo"\nversion = "0.1.0"\n'
            'dependencies = ["pyyaml", "python-dateutil"]\n',
        )
        self.write(
            "module.py",
            "try:\n    import orjson\nexcept ImportError:\n    orjson = None\n",
        )
        process = self.run_scanner(self.root_dir / "module.py", isolated=True)
        self.assertIn("orjson", process.stdout)
        self.assertExit(process, 1)

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

    def test_a_missing_alias_hint_is_loud_rather_than_a_quiet_pass(self) -> None:
        """Omission beats a guess, and this test is what makes the ordering real.

        ``pyyaml`` is declared and absent, so only the hint table can say which
        import names it owns. Drop the entry and the names become *unknowable*,
        which must fail the scan (exit ``2``) - in a script too, where a missing
        hint would otherwise leave the guard looking like a legitimate probe.

        A **wrong** entry is the direction that stays silent: a guard on a name
        the table assigns to another distribution is a genuine probe by every
        available fact, so the script exits ``0``. That asymmetry is why the
        table's comment says prefer omission over guessing; it cannot be caught
        by a test, only by not guessing, so only the loud half is pinned here.
        """
        script = self.write(
            "hinted.py",
            pep723_script(
                '"pyyaml"',
                "try:\n    import yaml\nexcept ImportError:\n    yaml = None",
            ),
        )
        self.assertExit(self.run_scanner(script, isolated=True), 1)

        scanner_without_hint = self.write(
            "scanner_without_hint.py",
            scanner_file.read_text(encoding="utf-8").replace(
                '    "pyyaml": "yaml",\n', ""
            ),
        )
        process = self.run_scanner(script, isolated=True, scanner=scanner_without_hint)
        self.assertExit(process, 2)
        self.assertIn("yaml", process.stderr)

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


class AliasHintTableTest(unittest.TestCase):
    """The hint table is the one fact in the scanner nothing can verify.

    A wrong entry is silent in the PEP 723 branch: the guard looks like an honest
    probe and exits ``0``. No runtime check distinguishes that from a correct
    entry whose dependency has a genuinely different import name, so the table is
    protected only by being short, explicit and reasoned about.

    These tests pin the parts that *are* checkable. They cannot prove an entry
    correct, and saying so is the point: a test that claimed to would be the
    circular-evidence failure again.
    """

    def test_every_installed_hint_matches_the_real_import_name(self) -> None:
        """Verify each hint whose distribution happens to be installed here.

        This is a **partial** check and must stay honest about that. ``pyyaml`` is
        a declared dependency of this test script so at least one entry is always
        checkable; the rest depend on the environment, and a hint whose
        distribution is absent stays unverified rather than being assumed
        correct. The assertion below forbids the degenerate case where the loop
        verified nothing and reported success.
        """
        reverse: dict[str, set[str]] = {}
        for module, distributions in packages_distributions().items():
            for distribution in distributions:
                reverse.setdefault(_normalize(distribution), set()).add(module)

        checked = 0
        for distribution, hint in _ALIAS_HINTS.items():
            modules = reverse.get(_normalize(distribution))
            if modules is None:
                continue  # not installed here: unknowable, not wrong
            checked += 1
            self.assertIn(
                hint,
                modules,
                f"hint says {distribution} provides {hint!r}, but the installed "
                f"distribution provides {sorted(modules)}",
            )

        self.assertGreater(
            checked,
            0,
            "no hinted distribution is installed, so the hints were never "
            "verified. Run this with at least one present; a check that reads "
            "nothing is not a pass.",
        )

    def test_hint_targets_are_not_also_distribution_names(self) -> None:
        """A hint whose target is already a distribution name is dead weight.

        ``_candidate_names`` adds the module name itself and the reverse hint
        lookup. If the hint target equals a real distribution name, that name is
        already a candidate and the entry cannot change any verdict - so it is
        an entry that was added for a reason nobody can name. Cheap to check, and
        the only structural property the table has.
        """
        normalized_hints = {_normalize(hint) for hint in _ALIAS_HINTS.values()}
        overlap = normalized_hints & {_normalize(name) for name in _ALIAS_HINTS}
        self.assertEqual(
            overlap,
            set(),
            f"hint target(s) {sorted(overlap)} equal a distribution name, so the "
            "entry cannot affect any verdict",
        )


class ModuleConstantTest(unittest.TestCase):
    """A table nobody reads passes every check the other classes need.

    Coverage checks, guess-direction and table verification all assume something
    consumes the value. When the consuming function is deleted and the constant
    stays behind with its explanatory comment, every one of them is satisfied by
    absence - there is no narrow verdict and no wide one, there is no verdict at
    all. This is the fourth class, and it is reachable only by asking whether
    the name is still read.

    The check is deliberately crude: a module-level assignment whose name never
    appears in a load context anywhere in the same file. That catches the real
    shape (orphaned constant) without needing cross-module analysis, and cannot
    report a false positive from a value used only in a type position, because a
    type-only use is still a load.
    """

    def test_every_module_constant_is_read_somewhere(self) -> None:
        """No dead module-level names in either scanner.

        ``__all__`` and dunder entries are skipped: re-exports are read by other
        modules, which this single-file check cannot see, and saying so beats
        guessing at them.
        """
        dead: list[str] = []
        scanners = (
            scanner_file,
            scanner_file.with_name("check_path_naming.py"),
        )
        for scanner in scanners:
            tree = ast.parse(scanner.read_text(encoding="utf-8"))
            assigned: set[str] = set()
            for node in tree.body:
                if isinstance(node, ast.Assign):
                    assigned.update(
                        target.id
                        for target in node.targets
                        if isinstance(target, ast.Name)
                    )
                elif isinstance(node, ast.AnnAssign) and isinstance(
                    node.target, ast.Name
                ):
                    assigned.add(node.target.id)
            loads = {
                node.id
                for node in ast.walk(tree)
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
            }
            for name in sorted(assigned - loads):
                if name.startswith("__"):
                    continue
                dead.append(f"{scanner.name}:{name}")

        self.assertEqual(
            dead,
            [],
            "module-level name(s) never read in their own file, so nothing "
            f"consumes them: {dead}. Delete the constant or its reader is "
            "missing - either way the table is unclassified, not narrow.",
        )


if __name__ == "__main__":
    unittest.main()
