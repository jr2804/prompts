# AGENTS.md Design Guidelines

**Evidence-Based Best Practices for Repository-Level Context Files**

*Based on arXiv:2602.11988 "Evaluating AGENTS.md" and industry best practices*

---

## Executive Summary

Recent empirical research (arXiv:2602.11988) challenges common assumptions about AGENTS.md files:

| Finding | Impact |
|---------|--------|
| LLM-generated context files **reduce** task success rates | ❌ Avoid auto-generation |
| Context files increase inference costs by **20%+** | ⚠️ Keep minimal |
| Developer-written files show only **~4% success improvement** | 📊 Marginal benefit |
| Agents exhibit **over-exploration** when given broad context | 🎯 Focus on essentials |

**Key Recommendation:** Less is more. Write minimal, high-signal files only when they provide universal value across tasks.

---

## Core Principles

### 1. Universal Applicability Test

**Every line must pass this test:** *"Will this be relevant for MOST tasks the agent performs?"*

**✅ Include:**
- Build/test/run commands used daily
- Critical architectural constraints
- Non-obvious import patterns
- Hard requirements (e.g., "NEVER commit .env")

**❌ Exclude:**
- Feature-specific implementation details
- One-off troubleshooting steps
- Auto-generated file trees
- Exhaustive command references

### 2. Instruction Budget Awareness

Frontier models can follow ~150-200 instructions reliably. Claude Code's system prompt already uses ~50 instructions.

**Target:** AGENTS.md should contain **<50 instructions** (ideally <30)

**Why it matters:** As instruction count increases, compliance decreases **uniformly across all instructions**—not just new ones.

### 3. Progressive Disclosure

Don't stuff everything into root AGENTS.md. Use task-specific files:

```
docs/agent-context/
├── building-the-project.md
├── testing-patterns.md
├── database-schema.md
└── service-architecture.md
```

Root AGENTS.md references these files; agent reads them only when relevant.

**Example:**
```markdown
## Related Documentation

- **Adding new commands?** Read `docs/agent-context/cli-patterns.md`
- **Database changes?** See `docs/agent-context/database-schema.md`
- **Testing requirements?** Check `docs/agent-context/testing-patterns.md`
```

### 4. Pointers Over Copies

**Never duplicate information that exists elsewhere:**

| Instead of... | Do this... |
|---------------|------------|
| Pasting code snippets | Reference `file:line` locations |
| Copying function signatures | Link to source file |
| Maintaining command lists | Point to package.json/pyproject.toml |
| Documenting stable APIs | Reference official docs |

**Rationale:** Copied content becomes stale. Pointers remain accurate.

### 5. No Linters in AGENTS.md

**Don't use AGENTS.md for:**
- Code style rules (use `.editorconfig`, `ruff.toml`)
- Formatting requirements (use Prettier, Biome)
- Type checking rules (use `pyrightconfig.json`)

**Why:** LLMs are expensive, slow linters. Use deterministic tools instead.

**Better approach:** Set up pre-commit hooks or stop-hooks that run formatters automatically.

---

## Structure Template

### Minimal Root AGENTS.md (<60 lines)

```markdown
# Project Name

One-sentence project description.

## Quick Commands

```bash
# Primary development commands
uv run pytest -v          # Run tests
ruff check src/ tests/    # Lint
uv run <app>              # Run application
```

## Critical Constraints

- **NEVER** [most important prohibition]
- **ALWAYS** [most important requirement]
- Use `uv run` for all Python commands

## Project Structure

Brief 2-3 sentence overview of main components.

## Documentation

- **CLI usage:** `docs/cli.md`
- **Architecture:** `docs/architecture.md`
- **Testing:** `tests/AGENTS.md`
```

### Package-Level AGENTS.md (<150 lines)

```markdown
# Package Name

## Purpose

One paragraph describing package responsibility.

## Import Patterns

```python
# Correct imports
from package.submodule import function

# Avoid: circular imports
```

## Key Design Patterns

### Pattern Name

Brief explanation with code example.

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `ENV_VAR` | `value` | Purpose |

## Testing

```bash
uv run pytest tests/package/ -v
```

## Lessons Learned

1. **Insight from refactoring** - Why it matters
2. **Common pitfall** - How to avoid
```

---

## Content Guidelines

### What to Include

| Category | Examples | Priority |
|----------|----------|----------|
| **Build/Test Commands** | `uv run pytest`, `npm test` | High |
| **Critical Constraints** | "NEVER commit .env", "Always use uv run" | High |
| **Non-Obvious Patterns** | Import paths, caching requirements | Medium |
| **Architecture Overview** | 2-3 sentence component map | Medium |
| **Lessons Learned** | Refactoring insights, pitfalls | Low |

### What to Exclude

| Category | Why Exclude |
|----------|-------------|
| Auto-generated file trees | Changes constantly, adds noise |
| Exhaustive command lists | Rarely relevant, bloats context |
| Code style rules | Use linters instead |
| Step-by-step tutorials | Belongs in docs/, not AGENTS.md |
| TODO lists | Use issue tracker |
| Temporary debugging notes | Delete after use |
| Checklists of completed items | Git history handles this |

---

## Writing Style

### Tone

**Prescriptive for constraints:**
- "NEVER suppress linter issues with `# noqa`"
- "MUST use `uv run` for all Python commands"

**Descriptive for patterns:**
- "Domain packages do not re-export operations"
- "Working group is derived from meeting via JOIN"

### Formatting

- **Bold** for emphasis on critical rules
- `Code blocks` for commands and imports
- Tables for configuration/options
- Bullet lists for related items

### Length Targets

| File Type | Target | Maximum |
|-----------|--------|---------|
| Root AGENTS.md | <60 lines | 100 lines |
| Package AGENTS.md | <100 lines | 150 lines |
| Task-specific docs | <50 lines | 75 lines |

---

## Anti-Patterns (from arXiv:2602.11988)

### ❌ Auto-Generated AGENTS.md

**Problem:** LLM-generated files reduce success rates and increase costs 20%+.

**Symptoms:**
- Generic advice ("write clean code")
- Obvious statements ("use Python for Python files")
- No project-specific insights

**Solution:** Write manually, review every line.

### ❌ Over-Exploration Triggers

**Problem:** Broad architectural overviews encourage unfocused exploration.

**Example:**
```markdown
# Full Module Documentation

## src/module_a/
This module handles...

## src/module_b/
This module is responsible for...

## src/module_c/
This module manages...
```

**Better:**
```markdown
## Key Modules

- **`module_a/`** - Primary entry point (start here)
- **`module_b/`** - Database operations
- **`module_c/`** - External API client
```

### ❌ Instruction Bloat

**Problem:** Each additional instruction reduces compliance with all instructions.

**Before (25 instructions):**
```markdown
- Always use type hints
- Never use Optional, use T | None
- Use is/not for None comparisons
- Keep modules under 250 lines
- Keep functions under 75 lines
- Use logging not print()
- Explain WHY not WHAT
- Don't use numbered steps
- Don't use decorative headings
- Don't use emojis in comments
... (15 more)
```

**After (8 instructions):**
```markdown
## Code Style

Follow project conventions (see `ruff.toml`). Key rules:
- Type hints mandatory (`T | None` not `Optional[T]`)
- `is`/`is not` for None comparisons
- `logging` over `print()`
```

---

## Maintenance

### When to Update

- ✅ After major refactoring with architectural insights
- ✅ When discovering repeated anti-patterns
- ✅ After adding new critical constraints
- ❌ After every small change
- ❌ To add temporary troubleshooting steps

### Review Checklist

Before adding content, ask:

1. **Universal?** Relevant for 80%+ of tasks?
2. **Non-obvious?** Would agent discover this from code?
3. **Stable?** Will this be true in 6 months?
4. **Actionable?** Can agent act on this immediately?
5. **Unique?** Already documented elsewhere?

**If any answer is "no" → Don't add it.**

### Deprecation

Remove content when:

- Feature it describes was removed
- Pattern it enforces is now automated
- Information moved to dedicated docs/
- Instruction is no longer universally applicable

---

## Validation

### Quick Health Check

```bash
# Count lines
wc -l AGENTS.md

# Count instructions (rough)
grep -c "^[*-]" AGENTS.md
```

**Targets:**
- Root AGENTS.md: <100 lines, <30 instructions
- Package AGENTS.md: <150 lines, <50 instructions

### Agent Feedback Loop

After major changes, observe:

1. Does agent follow the instructions?
2. Does it improve task completion?
3. Does it reduce unnecessary exploration?

If not → simplify or remove.

---

## Examples from This Project

### ✅ Good Patterns

**Root AGENTS.md (163 lines):**
- Clear command section with `uv run` emphasis
- Explicit linter prohibitions (PLC0415, ANN001)
- Git constraints (never commit .env)
- Skills reference table
- Package overview table

**Package AGENTS.md (tdoc_crawler, 168 lines):**
- Import patterns with correct/incorrect examples
- HTTP caching requirement with code example
- TDoc data sources comparison table
- Database schema overview
- Circular import prevention strategy

**CLI Submodule (68 lines):**
- Clear separation: CLI vs library code
- Classification rules with examples
- Module responsibility table
- Lessons learned from refactoring

### ⚠️ Areas for Improvement

**convert-lo AGENTS.md (271 lines):**
- Too long (exceeds 150-line target)
- Extensive usage examples belong in docs/
- Performance benchmarks belong in README
- **Action:** Move usage patterns to `docs/convert-lo-usage.md`, keep only critical constraints

**tdoc-ai AGENTS.md (136 lines):**
- Good length but could be more minimal
- Factory pattern explanation could reference source
- **Action:** Replace code examples with file references

---

## References

### Research

- **arXiv:2602.11988** - "Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?" (ETH Zurich, 2026)
  - [Paper](https://arxiv.org/abs/2602.11988)
  - [AgentBench Dataset](https://github.com/eth-sri/agentbench)

### Industry Best Practices

- **HumanLayer** - "Writing a good CLAUDE.md"
  - [Blog Post](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
  - Key insight: <60 lines for root file

- **Anthropic** - Claude Code Documentation
  - [Official Docs](https://code.claude.com/docs/en/agents)

### Related Patterns

- **Progressive Disclosure** - Show context only when needed
- **12-Factor Agents** - Context engineering best practices
- **Context Compression** - Summarize vs. copy

---

## Appendix: Decision Tree

```
Should I add this to AGENTS.md?
│
├─ Is it universally applicable? ─No─→ Put in task-specific doc
│       │
│      Yes
│       │
├─ Is it non-obvious from code? ─No─→ Don't add (redundant)
│       │
│      Yes
│       │
├─ Is it stable (6+ months)? ─No─→ Don't add (temporary)
│       │
│      Yes
│       │
├─ Is it already documented? ─Yes─→ Add pointer, not copy
│       │
│       No
│       │
├─ Can it be automated? ─Yes─→ Use linter/hook instead
│       │
│       No
│       │
└─→ ADD TO AGENTS.md
```

---

*Last updated: March 2026*
*Based on empirical research + project-specific learnings*
