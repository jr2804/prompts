# AGENTS.md — skills/

Skill authoring contract for this repository. Skills are modular components
that define specific capabilities or behaviors for AI coding assistants.

## Purpose

Define the binding rules for creating and updating agent skills under
`skills/`. Anything not covered here falls back to the root AGENTS.md and
`.agents/POLICIES.md`.

## Ownership

- Owns: all skill definitions, helper scripts, and per-skill references
  under `skills/**`.
- Does not own: the `skill-creator` tool itself is a skill consumed here,
  but its internal behavior is documented in its own `SKILL.md`.

## Local Contracts

### Spec compliance

Any created or updated skill MUST comply with the
[Agent Skills Specification](https://agentskills.io/specification).

- Skills must be modular and integrate cleanly with other skills.
- Follow best practices for code quality: proper documentation, testing,
  and adherence to coding standards.
- Use version control to manage changes and updates to skills.
- Validate with `uvx skills-ref validate <path-to-skill>`.

### Agent neutrality

**All skills must be agent-agnostic** — designed to work across Claude Code,
Qwen, Gemini, Cursor, and other AI coding assistants.

- **Avoid agent-specific mentions**: do not reference "Claude," "Claude Code,"
  "Gemini CLI," etc. in skill text.
- **Use universal language**: write "when you write code" instead of
  "[Agent] writes code"; "use the MCP server" instead of "use this in
  [Agent]."
- **Tool references must be portable**: if a skill requires an MCP server,
  plugin, or tool, name the capability, not the agent integration path.
- **Examples**: use generic idioms (Python, TypeScript, etc.), not
  agent-specific APIs or imports.

Frontmatter guidance:

- `description`: must indicate when/why to use the skill, not which agent
  it supports.
- `when-to-use`: keep focused on the task, not the agent.

Audit checklist before finalizing a skill:

- [ ] No hardcoded "Claude", "Gemini", "Qwen", "Copilot" references
- [ ] Examples use only standard language/framework idioms
- [ ] Tool/MCP server references describe the capability, not the agent's
      integration method
- [ ] Instructions use "agents", "LLMs", "you" instead of agent names
- [ ] References to external systems (APIs, files, databases) are generic

### Skill creation

When creating a new skill, use the skill in `./skill-creator`. It scaffolds
and implements new agent skills efficiently.

Run skill-creator helper scripts ALWAYS through `uv`:

```bash
uv run ./skills/skill-creator/scripts/<script-name>.py
```

### Skill script metadata

Minimum/maximum Python version and non-stdlib dependencies for skill scripts
MUST be declared as inline script metadata:

- <https://packaging.python.org/en/latest/specifications/inline-script-metadata/#inline-script-metadata>
- <https://docs.astral.sh/uv/guides/scripts/#declaring-script-dependencies>

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

## Work Guidance

- Reuse existing skills/patterns before creating new ones — check the
  catalog in `README.md` and sibling skill folders first.
- Keep skill text concise and operational; link to canonical references
  instead of restating them.

## Verification

```bash
# validate a skill against the Agent Skills spec
uvx skills-ref validate <path-to-skill>

# lint any Python helper scripts
ruff check <path-to-skill> --fix
```

## Child DOX Index

| Path | Covers |
|------|--------|
| `skills/standards/AGENTS.md` | Standards-document skills — `.docx` generation for SDOs (ETSI, 3GPP, ITU-T) |
