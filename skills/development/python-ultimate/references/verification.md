# Verification Reference

## Table of Contents

1. [Iron Law](#iron-law)
2. [Gate Function](#gate-function)
3. [Forbidden Words](#forbidden-words)
4. [Verification Checklist](#verification-checklist)
5. [Common Verification Commands](#common-verification-commands)
6. [When Verification Fails](#when-verification-fails)

______________________________________________________________________

## Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

**Evidence before claims, always.**

If you haven't run the verification command, you cannot claim it passes. Skip any step = lying, not verifying.

______________________________________________________________________

## Gate Function

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY   → What command proves this claim?
2. RUN        → Execute the FULL command (fresh, complete)
3. READ       → Full output, check exit code, count failures
4. VERIFY     → Does output confirm the claim?
               - If NO: State actual status with evidence
               - If YES: State claim WITH evidence
5. ONLY THEN  → Make the claim
```

______________________________________________________________________

## Forbidden Words

Do **not** use these words when stating results:

- **should**
- **probably**
- **might**
- **likely**

These words imply assumption without evidence. State actual results with command output instead.

______________________________________________________________________

## Verification Checklist

Before claiming completion, verify:

- [ ] Tests pass — Run test command, confirm 0 failures
- [ ] Linter clean — Run ruff/mypy, confirm 0 errors
- [ ] Type checks pass — Run mypy, confirm no issues
- [ ] Build succeeds — Run build command, confirm exit 0
- [ ] Original symptom fixed — Reproduce issue, confirm resolved
- [ ] Regression tests work — Red-green cycle verified
- [ ] VCS diff shows intended changes — Review actual changes

______________________________________________________________________

## Common Verification Commands

```bash
# Run tests
pytest
pytest tests/

# Lint
ruff check .
ruff check src/

# Type check
mypy src/
mypy .

# Build
python -m build
uv build
```

______________________________________________________________________

## When Verification Fails

**Do not claim success.**

1. State the actual failure with evidence (command output)
2. Diagnose the root cause
3. Fix the issue
4. Re-run verification
5. Only then claim the fix works

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check |
| Build succeeds | Exit code 0 | Logs look good |
| Bug fixed | Original symptom: passes | Code changed |
| Regression works | Red-green verified | Test passes once |

______________________________________________________________________

**Bottom Line:** Run the command. Read the output. THEN claim the result. This is non-negotiable.
