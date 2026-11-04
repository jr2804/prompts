# Forbidden Scan Fixtures: Expected Output

Use these fixtures to validate `--check-forbidden` behavior from
`skills/development/python-ultimate/assets/check_path_naming.py`. Run the command
below from the repository root.

## Command

```bash
uv run skills/development/python-ultimate/assets/check_path_naming.py --check-forbidden skills/development/python-ultimate/assets/examples/
```

## Expected Matches by File

### fixture_type_and_imports.py

Expected pattern classes:

- `TYPE_CHECKING guard` (the import line, the `if` guard, and the inner guard)
- `Optional[T]`

Expected count:

- 4 matches

These fixtures are deliberately non-compliant, so `assets/examples/.ruff.toml`
excludes them from `ruff check --fix --unsafe-fixes`. Without that exclusion the
repository lint task rewrites `Optional[str]` to `str | None` and drops the
`TYPE_CHECKING` block, leaving the fixture with nothing to detect.

### fixture_paths_and_noqa.py

Expected pattern classes:

- `os.path usage`
- `sys.path manipulation`
- `noqa suppression`

Expected count:

- 4 matches

### fixture_defensive_import.py

Expected pattern classes:

- `defensive required import`

Expected count:

- 1 match

## Expected Aggregate

- Total matches: 9
- Exit code: 1 (findings present)

The scanner prints file paths, line numbers, pattern class labels, and a short remediation reason for each match.

## Vacuous-scan safety

Both scanners refuse to report success when they scanned nothing, or when a file
could not be read or parsed. An empty directory or a syntax error exits `2`:

```bash
uv run skills/development/python-ultimate/assets/check_path_naming.py --check-forbidden /empty/dir
# ERROR: no Python files found under /empty/dir - refusing to report success
```
