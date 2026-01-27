# General instructions

Avoid making assumptions. If you need additional context to accurately answer the user, ask the user for the missing information. Be specific about which context you need.

Always break code up into modules and components so that it can be easily reused across the project.

If your response contains code examples, always provide the name of the file it would go in,so the user knows where the code goes.


Separate the task to implement the project into sub-tasks/milestones. After each milestone:
- Remember the key features and approaches used via the built-in ´/memory´ command.
- Clean-up clutter files like e.g., temporary files, ad-hoc test scripts (that are not actual unit tests/pytest scripts).
- Update documentation and comments to reflect any changes made during the milestone.
- Review and refactor code for improved readability and maintainability.
- Implement automated tests to cover new features and ensure existing functionality is not broken.
- Ensure proper logging and error handling throughout the codebase.
- Update examples in general documentation like e.g., README.md or docs/index.md.
- document new features in the folder /docs of the repository. Update README.md in the root directory of the project, if necessary.

# Project management

- Use pyproject.toml instead of requirements.txt, setup.cfg, setup.py, etc.!
- If not specified in pyproject.toml, generating any code may assume at least Python 3.12 as the minimum version.
- Unless instructed otherwise, always use `uv` to manage environment, adding required/removing ununsed packages and to build the project.
  - `uv run ...` for running a python script.
  - `uv run -m pytest ...` for running a pytest script.
  - `uvx ...` for running program directly from a PyPI package.
  - `uv add/remove/... ...` for managing environments, installing packages, etc.
  - `uv build ...` for building the project.
   
# Coding instructions

- All Python code must be PEP 8 compliant.
- If needed, install standard libraries/packages used in computer science domain like e.g., numpy, scipy, pandas, matplotlib
- If applicable, instead of generating unnecessary code, use existing and widely adopted packages/framesworks.
- for all important functions, add unit tests based on pytest framework. For each functionality, at least three reasonable tests shall be created.
- Never use ´print´ to debug code. Instead, use logging with appropriate log levels (e.g., debug, info, warning, error).
- Never use the deprecated idiom ´from __future__ import annotations´.
- Please apply the following ruff rules / apply recommended style corrections:
	- I001
	- SIM108
	- UP004
	- UP035
	- PTH100 to PTH999
