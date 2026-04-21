---
name: skill-reviewer
description: Review existing skills and suggest improvements. Use when asked to review, audit, or improve a skill — validates against Agent Skills spec and best practices. Also triggers when drafting or creating a new skill. Run `uvx skills-ref validate` to check spec compliance.
allowed-tools:
  - Bash(skills-ref:*) Bash(uvx:*) Read Edit Write Glob Grep
---

# Skill Reviewer

Review existing skills and generate actionable improvement suggestions using both **inline patch/diff format** and **structured JSON** output.

## When to Use

- User explicitly requests review of a skill at a specific path
- User is drafting or creating a new skill (auto-trigger)
- After running `uvx skills-ref validate` to understand spec violations

## Core Workflow

### 1. Load & Parse

Identify the skill path to review:

- **Explicit**: User provides skill path directly
- **Auto-trigger**: User mentions "new skill", "create skill", "draft skill" → review the SKILL.md being created

Read the target skill's `SKILL.md`:

- Extract YAML frontmatter (name, description, optional fields)
- Parse body content for structural analysis

### 2. Validate with skills-ref

Run the Agent Skills validation CLI:

```bash
uvx skills-ref validate ./path/to/skill
```

This catches:

- Invalid frontmatter YAML syntax
- Missing required fields (name, description)
- Name format violations (must be hyphen-case, max 64 chars)
- Description over 1024 characters
- Unexpected frontmatter fields

### 3. Review Against Criteria

Evaluate the skill using the criteria in [references/review-criteria.md](references/review-criteria.md):

**Frontmatter Checks**

- [ ] `name` field present and valid (hyphen-case, ≤64 chars)
- [ ] `description` field present (≤1024 chars, no angle brackets)
- [ ] No unexpected fields (only: name, description, license, metadata, compatibility, allowed-tools)

**Description Quality**

- [ ] Imperative phrasing ("Use when..." not "This skill does...")
- [ ] Focus on user intent, not implementation
- [ ] Specific keywords for triggering
- [ ] Clear when-to-use scenarios

**Body Structure**

- [ ] Concise instructions (\<500 lines preferred)
- [ ] Progressive disclosure (main points in SKILL.md, details in references/)
- [ ] No agent-specific references ("Claude", "Gemini", etc.)
- [ ] Examples where helpful

**Resource Organization**

- [ ] Scripts in `scripts/` if needed
- [ ] Reference docs in `references/` if needed
- [ ] Assets in `assets/` if needed

### 4. Generate Improvements

Produce **two output formats**:

#### Inline Patch/Diff

Use filepath comments for "Apply to file" functionality:

````markdown
// filepath: skill/SKILL.md
// ...existing code...

```yaml
---
name: my-skill
description: Use when working with CSV files for analysis and visualization.
---
```

// ...existing code...
````

#### Structured JSON

For programmatic consumption:

```json
{
  "skill_path": "/path/to/skill",
  "issues": [
    {
      "severity": "critical",
      "file": "SKILL.md",
      "line": 1,
      "text": "Missing required 'name' field in frontmatter",
      "fix": "Add `name: my-skill` to frontmatter"
    },
    {
      "severity": "major",
      "file": "SKILL.md",
      "line": 3,
      "text": "Description uses second person ('you should use') instead of imperative",
      "fix": "Rewrite as 'Use when...' imperative phrasing"
    }
  ],
  "summary": {
    "critical": 1,
    "major": 2,
    "minor": 0
  }
}
```

### 5. Issue Categorization

Group issues by severity (from skill-improver methodology):

**Critical** — MUST fix immediately

- Missing required frontmatter fields (name, description)
- Invalid YAML syntax
- Referenced files that don't exist

**Major** — MUST fix

- Weak or vague trigger descriptions
- Wrong voice (second person instead of imperative)
- SKILL.md exceeds 500 lines without using references/
- Missing "When to Use" section
- Description doesn't specify when to trigger

**Minor** — Evaluate before fixing

- Subjective style preferences
- Optional enhancements
- Formatting suggestions

### 6. Iterate (Improver Loop)

For skill improvement workflows:

1. Present issues with inline patches
2. User applies fixes
3. Re-validate with `uvx skills-ref validate`
4. Re-review remaining issues
5. Continue until no critical/major issues remain

Output completion marker when done:

```
<skill-review-complete>
```

## Resources

- [Review Criteria](references/review-criteria.md) — Detailed evaluation checklist
- [Improvement Patterns](references/improvement-patterns.md) — Common issues and fixes
- [quick_review.py](scripts/quick_review.py) — Lightweight validation script
