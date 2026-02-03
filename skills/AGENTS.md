# Instructions for creating and updating agent skills

This document provides guidelines for creating and updating agent skills in our system. Agent skills are modular components that define specific capabilities or behaviors for agents.

## General Guidelines

Any created or updated skill shall comply with the [Agent Skills Specification](https://agentskills.io/specification).

- Ensure that the skill is modular and can be easily integrated with other skills.
- Follow best practices for code quality, including proper documentation, testing, and adherence to coding standards.
- Use version control to manage changes and updates to the skill.

## Skill Creation

When creating a new skill, use the skill provided in `./skill-creator`. This skill is designed to help you scaffold and implement new agent skills efficiently.

To run the helper scripts of the skill creator, always use `uv` to run the scripts. For example:

```bash
uv run ./skills/skill-creator/scripts/<script-name>.py
```
## Creating skill scripts

Minimum/maximum Python version and dependencies beyond standard library for skill scripts must be declared as inline script metadata, see:
- https://packaging.python.org/en/latest/specifications/inline-script-metadata/#inline-script-metadata
- https://docs.astral.sh/uv/guides/scripts/#declaring-script-dependencies

Example:
```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests<3",
#   "rich",
# ]
# ///

import requests
from rich.pretty import pprint

resp = requests.get("https://peps.python.org/api/peps.json")
data = resp.json()
pprint([(k, v["title"]) for k, v in data.items()][:10])
```
