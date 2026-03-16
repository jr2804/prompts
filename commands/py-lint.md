---
name: "py-lint"
description: "Use a Python linter to analyze code for potential errors and style issues"
model: "github-copilot/gpt-5-mini"
---

# pyLint

You have a Python codebase that may contain potential errors, style issues, or code smells. Use Python linter `ruff check <paths> --fix` to analyze the code, identify any issues and let `ruff` fix the easy ones. Include source and test directories in the analysis, typically found in `src/` and `tests/`.

After running the linter, review the output for any remaining issues that were not automatically fixed.

If available, use the skill `python-linter` to assist fixing only the following linter issues: `$ARGUMENTS`

(If no issues were provided in the last statement, only provide an overview of the linter output and do not attempt to fix any issues.)

If the skill is not available, you can still fix these issues manually by following the linter's recommendations.
