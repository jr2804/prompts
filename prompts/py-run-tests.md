---
name: "py-run-tests"
description: "Run Python tests using pytest and report the results"
---

# pyRunTests

You have a Python codebase with tests that need to be executed to ensure the code is functioning correctly. Use the following command to run the tests, where `<paths>` typically include the test directories (e.g., `tests/`) or more specific test files or sub-directories.

!`uv run pytest <paths> -v --tb=short`

Run the command above only for the following test directories/files: `$ARGUMENTS`
(If no specific arguments were provided in the last statement, run the tests without a test directory, i.e., for all tests and only provide an overview of the test results, but do not attempt to fix any issues.)

After running the tests and if there are any failures, review the output for any failed tests, errors, or warnings. Pay attention to the test names, error messages, and stack traces to understand the issues. Fix low-to-medium complexity issues immediately, if possible. For larger refactorings/redesigns/longer/higher effort tasks, propose suggestions and ask the user how to proceed.
