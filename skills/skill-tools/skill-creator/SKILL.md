---
name: skill-creator
description: Guide for creating, validating, improving, and benchmarking skills. Use when users want to create a skill from scratch, edit or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy.
---

# Skill Creator

A skill for creating new skills and iteratively improving them.

## Overview

At a high level, creating a skill follows this loop:

1. Decide what the skill should do and roughly how it should do it.
2. Write a draft of the skill.
3. Create test prompts and run the agent on them.
4. Evaluate the results qualitatively and, if the runtime supports it, quantitatively.
5. Rewrite the skill based on feedback.
6. Repeat until satisfied.
7. Expand the test set and try again at larger scale.

Your job is to figure out where the user is in this process and help them progress. A user may arrive with just "I want a skill for X" — narrow the scope, write a draft, draft test cases, evaluate, and iterate. Or they may already have a draft — go straight to the eval/iterate step.

## Skill Anatomy

A skill is a directory with at minimum a `SKILL.md`. Optional subdirectories organize supporting files:

```text
skill-name/
├── SKILL.md            (required)  — frontmatter + instructions
├── scripts/            (optional)  — executable code (Python/Bash/etc.)
├── references/        (optional)  — documentation loaded on demand
├── assets/            (optional)  — templates, icons, fonts, static files
├── agents/            (optional)  — sub-agent role definitions for evals
├── eval-viewer/       (optional) — HTML viewer for eval results
└── evals/             (optional)  — test prompts and grading criteria
```

### Frontmatter

```yaml
---
name: skill-name           # required — hyphen-case, ≤64 chars
description: >-            # required — what + when to use, ≤1024 chars
  One paragraph. Use "Use when..." phrasing. Include the trigger
  scenarios (file types, task keywords, user intent) that should
  activate this skill.
---
```

Only these frontmatter fields are valid: `name`, `description`, `license`, `allowed-tools`, `metadata`, `compatibility`.

### scripts/

Executable code for tasks that need deterministic reliability or are written repeatedly. Every script must declare its Python version floor and dependencies via PEP 723 inline metadata — never assume packages are pre-installed:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = ["pypdf", "pillow"]
# ///

import pypdf
from PIL import Image
```

See [PEP 723 inline metadata](https://packaging.python.org/en/latest/specifications/inline-script-metadata/) and the [uv scripts guide](https://docs.astral.sh/uv/guides/scripts/#declaring-script-dependencies).

Run scripts via `uv run scripts/<name>.py …` — never `python …` or `python -m …`.

### references/

Documentation loaded into context as needed. Use these patterns:

**High-level guide with references** — show the summary, link to details:

```markdown
## Quick start
Extract text with pdfplumber: [example]

## Advanced
- **Form filling**: See [references/forms.md](references/forms.md)
- **API reference**: See [references/api.md](references/api.md)
```

**Conditional details** — show basic content, link to advanced:

```markdown
## Creating documents
Use python-docx. For tracked changes see [references/redlining.md](references/redlining.md).
```

**Rules:**

- Keep references one level deep from SKILL.md. Every reference links directly from SKILL.md.
- Files longer than 100 lines should have a table of contents at the top.

### assets/

Static files used in output: templates, icons, fonts, sample data. Every asset must be named or linked in SKILL.md or a reference — orphaned files that nothing references are dead weight.

### agents/

Sub-agent role definitions. Used during evals to spawn specialized grader, analyzer, or comparator agents. Each is a plain `.md` file read by the spawning agent.

## Creating a New Skill

### Step 1 — Understand with concrete examples

Before writing anything, understand how the skill will actually be used. Ask the user for examples: "What would a user actually say to trigger this?" "Can you give me a sample prompt and the expected output?"

Conclude when you have enough examples to write a meaningful draft.

### Step 2 — Plan the contents

Analyze each example: what scripts, references, and assets would eliminate repeated work? List every resource, then assign it to the right subdirectory. If a resource fits in two places, pick one — no duplication.

**When to use scripts:**

- The same code is rewritten repeatedly (e.g., PDF rotation, image conversion).
- Deterministic reliability is needed (file operations, format conversion).

**When to use references:**

- Documentation needs to be loaded only for specific subtasks.
- The skill covers multiple domains or variants and users only need one at a time.

**When to use assets:**

- Static files are inputs or outputs of the skill (templates, icons, fonts, sample data).

### Step 3 — Initialize

Run `uv run scripts/init_skill.py <skill-name> --path <parent-dir>`. This creates the directory structure with a `SKILL.md` template. Edit the template: fill in name, description, and the body.

If the skill already exists, skip to step 4.

### Step 4 — Implement

Write the scripts, references, and assets. Every script gets PEP 723 inline metadata. Every reference and asset gets mentioned in SKILL.md or a reference that SKILL.md links to — nothing lives in a subdirectory without a path to it from the top.

**Structure rules for SKILL.md:**

- Keep it under 300 lines. Move detailed content to `references/`.
- Use imperative voice ("Use when…", not "This skill does…").
- The `description` field in frontmatter is the trigger signal — make it specific. Include file types, task keywords, and user intent.
- Do not name a specific agent runtime ("Claude Code", "Copilot", "Gemini") in instructions or frontmatter.

### Step 5 — Validate

Run `uvx skills-ref validate <skill-path>` to check spec compliance. Also run `uv run scripts/quick_validate.py <skill-path>` for a local check.

### Step 6 — Package

Run `uv run scripts/package_skill.py <skill-path> [output-dir]` to create a distributable `.skill` file.

## Improving an Existing Skill

### The Iteration Loop

```text
draft → test prompts → run → grade → review → rewrite → repeat
```

1. Identify where the current skill falls short.
2. Add or revise the relevant section.
3. Create 2–3 realistic test prompts and run the agent on them.
4. Ask the user to evaluate the results.
5. Rewrite based on feedback.
6. Repeat until the skill is reliable.

If the runtime supports sub-agents, you can also run quantitative evals. See **Quantitative Evaluation** below.

### Writing Good Test Prompts

Test prompts should be realistic — concrete file paths, context about the user's situation, exact task descriptions. Not abstract ("format this data") but specific ("the xlsx is in downloads, it's called Q4 sales FINAL v2.xlsx, add a profit margin column").

Save test prompts to `evals/evals.json`. Include `expectations` — verifiable statements about the expected output, not just "it should look good."

```json
{
  "skill_name": "pdf-editor",
  "evals": [
    {
      "id": 1,
      "prompt": "Rotate the third page of report.pdf by 90 degrees clockwise",
      "expected_output": "A PDF where page 3 is landscape-oriented",
      "files": ["evals/files/report.pdf"],
      "expectations": [
        "The output file is a valid PDF",
        "Page 3 is rotated 90 degrees",
        "Other pages are unchanged"
      ]
    }
  ]
}
```

## Quantitative Evaluation

> Requires a coding-agent runtime that supports sub-agents. If the current runtime does not support this, skip to **Human Review Loop**.

### Step 1 — Run the evals

If the skill has `evals/evals.json`, run the evaluation suite. This typically spawns one sub-agent per test prompt, saves outputs, and produces grading results.

### Step 2 — Grade each run

Spawn a grader sub-agent that reads `agents/grader.md` and evaluates each assertion against the outputs. Save results to `grading.json` in each run directory. The `grading.json` expectations array must use these exact fields: `text`, `passed`, `evidence`.

For assertions checkable programmatically, write a script instead of eyeballing — scripts are faster, more reliable, and reusable across iterations.

### Step 3 — Aggregate into benchmark

Run the aggregation script:

```bash
uv run scripts/aggregate_benchmark.py <workspace>/iteration-N --skill-name <name>
```

This produces `benchmark.json` and `benchmark.md` with pass_rate, time, and tokens for each configuration, with mean ± stddev and delta. See `references/schemas.md` for the exact schema.

### Step 4 — Analyst pass

Read the benchmark data and surface patterns the aggregate stats might hide. See `agents/analyzer.md` — look for non-discriminating assertions (always pass regardless of skill), high-variance evals (possibly flaky), and time/token tradeoffs.

### Step 5 — Launch the viewer

```bash
uv run scripts/generate_review.py <workspace>/iteration-N --skill-name "my-skill" --benchmark <workspace>/iteration-N/benchmark.json
```

For iteration 2+, also pass `--previous-workspace <workspace>/iteration-<N-1>`.

## Description Optimization

The `description` field in SKILL.md frontmatter is the primary trigger signal. After creating or significantly revising a skill, offer to optimize it for better triggering accuracy.

### Step 1 — Generate trigger eval queries

Create 20 eval queries — should-trigger and should-not-trigger cases. Save as JSON:

```json
[
  {"query": "the user prompt", "should_trigger": true},
  {"query": "another prompt", "should_trigger": false}
]
```

Queries must be realistic, concrete, and specific. Include file paths, personal context, company names, URLs, abbreviations, casual speech. Use a mix of lengths. Focus on edge cases.

**Bad:** `"Format this data"`, `"Extract text from PDF"`
**Good:** `"ok so my boss just sent me this xlsx file (its in my downloads, called something like 'Q4 sales final FINAL v2.xlsx') and she wants me to add a column that shows the profit"`

Share the queries with the user and ask for feedback before proceeding.

### Step 2 — Run trigger eval

Use the runtime's eval runner to test each query against the skill's description. If the runtime supports sub-agents and has an automated runner, use it. Otherwise run the prompts manually.

### Step 3 — Improve the description

Pass the eval results to `scripts/improve_description.py` (or equivalent) to generate an improved description.

### Step 4 — Evaluate at scale

Once the description passes on the 20-query set, expand to 100+ queries and repeat. A description that passes 20 queries may still over-trigger or under-trigger at scale.

## Blind Comparison

For situations where you want a rigorous comparison between two versions of a skill, use the blind comparison system. Read `agents/comparator.md` and `agents/analyzer.md`. The basic idea: give two outputs to an independent agent without revealing which is which, and let it judge quality. Then analyze why the winner won.

This is optional, requires sub-agents, and most users won't need it. The human review loop is usually sufficient.

## Advanced: Combining Multiple Source Skills into One Aggregate

When a skill draws from several reference skills, apply these rules to keep the result maintainable and unambiguous:

### No duplication

Each fact, rule, and piece of guidance lives in exactly one place. If two source skills say the same thing in different words, pick the clearer phrasing and drop the other. If two sources disagree, resolve the conflict explicitly — do not keep both versions as alternatives.

### Subdirectory discipline

Use only these subdirectories:

- `scripts/` — executable code
- `references/` — on-demand documentation
- `assets/` — static files used as inputs/outputs
- `agents/` — sub-agent role definitions (for eval workflows)
- `eval-viewer/` — HTML result viewers

Add a subdirectory only when it solves a real organizational problem that these five cannot. When you add one, document why in SKILL.md.

### Every file is reachable from SKILL.md

Nothing lives in a subdirectory without a path from SKILL.md or from a file that SKILL.md links to. A file that cannot be reached from SKILL.md is invisible to the agent and dead weight in the context window. Apply this rule ruthlessly:

- If a script is not called from SKILL.md or a reference, remove it or link to it.
- If a reference is not linked from SKILL.md or a referencing file, either link it or remove it.
- If an asset is not used by any script or referenced in any doc, remove it.

### No agent-specific names or tool references

Instructions and frontmatter must not name a specific agent runtime, CLI, or tool. Write agent-neutrally:

- "Run with `uv run`" is acceptable (it names a tool, not an agent).
- "Use Claude Code to run this" is not acceptable.
- "Run with `python`" is not acceptable — use `uv run`.
- Avoid naming CLI tools that are not universally available. If a tool is needed for a specific workflow, name it in that section's context, not as a global rule.

### Conflict resolution

When source skills conflict on a rule or recommendation, do not keep both. Pick the one that is:

1. More specific to the skill's domain.
2. Backed by a standard, citation, or benchmark.
3. Easier to verify.

State the resolution explicitly: "Source A recommended X but source B recommended Y. We use Y because Z."

## Writing Guidelines

### Imperative form

Prefer imperative voice in instructions: "Use when…" not "This skill does…".

### Explain the why

Theory of mind beats musty MUSTs. Explain why a rule exists rather than just stating it. A skill that explains its reasoning transfers to novel situations; a skill that just lists rules does not.

### Output format definitions

```markdown
## Report structure
ALWAYS use this exact template:
# [Title]
## Executive summary
## Key findings
## Recommendations
```

### Example pattern

```markdown
## Commit message format
**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

### Principle of lack of surprise

Skills must not contain malware, exploit code, or anything that compromises system security. A skill's contents should not surprise the user in intent if described. Do not create misleading skills or skills designed to facilitate unauthorized access, data exfiltration, or other malicious activities. Roleplay scenarios are fine.

## Quick Reference

| Script | What it does |
|--------|-------------|
| `scripts/init_skill.py` | Scaffold a new skill directory |
| `scripts/quick_validate.py` | Spec-compliance check (frontmatter, name, description) |
| `scripts/package_skill.py` | Build a distributable `.skill` zip file |
| `scripts/run_eval.py` | Run trigger eval queries (requires sub-agent runtime) |
| `scripts/run_loop.py` | Run the full eval → improve → repeat loop |
| `scripts/improve_description.py` | Generate an improved description from eval results |
| `scripts/generate_report.py` | Build an HTML report from loop output |
| `scripts/aggregate_benchmark.py` | Aggregate run results into benchmark statistics |
