# Forbidden Scan Fixtures: Expected Output

Use these fixtures to validate `--check-forbidden` behavior from `assets/check_path_naming.py`.

## Command

```bash
uv run assets/check_path_naming.py --check-forbidden assets/examples/
```

## Expected Matches by File

### fixture_type_and_imports.py

Expected pattern classes:

- `TYPE_CHECKING guard` (import and conditional guard)
- `Optional[T]`

Expected count:

- 3 matches

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

- Total matches: 8
- Exit code: 1 (findings present)

The scanner prints file paths, line numbers, pattern class labels, and a short remediation reason for each match.
