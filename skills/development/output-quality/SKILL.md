---
name: output-quality
description: Detect and eliminate generic, low-quality "AI slop" patterns in natural language, code, and design. Use when REVIEWING existing content (text, code, or visual designs) for quality issues, cleaning up generic patterns, or establishing quality standards. Focuses on pattern detection—not content creation.
---

# Output Quality

Identify and remove telltale patterns that signal low-quality, generic content across text, code, and design.

## What is "Slop"?

"Output slop" refers to predictable patterns that signal generic, low-effort AI-generated content:

**Text slop:** Overused phrases ("delve into," "navigate the complexities"), excessive buzzwords, meta-commentary ("In this article, we will discuss..."), vague hedging

**Code slop:** Generic variable names (`data`, `result`, `temp`), obvious comments that restate code, unnecessary abstraction layers, over-engineered solutions

**Design slop:** Cookie-cutter layouts, generic gradient backgrounds, overused visual patterns, vague marketing copy ("Empower Your Business")

## When to Use This Skill

Apply output-quality techniques when:

- Reviewing AI-generated content before delivery
- Creating original content and want to avoid generic patterns
- Cleaning up existing content that feels generic or low-effort
- Establishing quality standards for a project or team
- Content has telltale signs of lazy, templated generation

## Core Workflow

### 1. Detect Slop

**For text files:**

Read the appropriate reference guide for detailed patterns:

- [text-patterns.md](references/text-patterns.md) — Natural language slop patterns
- [code-patterns.md](references/code-patterns.md) — Programming slop patterns
- [design-patterns.md](references/design-patterns.md) — Visual/UX design slop patterns

### 2. Clean Slop

**Manual cleanup** (recommended):
Apply strategies from the reference files based on detected patterns.

**Text-specific automated tools** (optional):
Python scripts in references can help analyze and suggest cleanup:

- See [python-detection.md](references/python-detection.md) for setup and usage

## Text Quality Principles

### Be Direct

- Skip preambles and meta-commentary
- Lead with the actual point
- Cut transition words that don't add meaning
- Remove "In this article, we will..." throat-clearing

### Be Specific

- Replace generic terms with concrete examples
- Name specific things instead of "items," "things," "data"
- Use precise verbs instead of vague action words
- Avoid lazy extremes ("every," "always," "never") doing vague work

### Be Authentic

- Vary sentence structure and length
- Use active voice predominantly
- Write in a voice appropriate to context, not corporate-generic
- Trust readers to understand without hand-holding

## Code Quality Principles

### Meaningful Names

- Variables should describe their content, not their type
- Function names should describe action + object
- Avoid single-letter names or `temp`, `data`, `result`, `item`

### Appropriate Documentation

- Document why, not what (code should be self-evident)
- Skip documentation for obvious code
- Focus documentation on public APIs and complex logic
- Don't restate what the code does

### Simplicity Over Cleverness

- Write code that's easy to understand
- Optimize only when profiling shows need
- Prefer simple solutions to complex ones
- Avoid unnecessary abstraction layers

## Design Quality Principles

### Content-First Design

- Design around actual content needs
- Create hierarchy based on importance, not templates
- Let content determine layout, not vice versa

### Intentional Choices

- Every design decision should be justifiable
- Use patterns because they serve users, not because they're trendy
- Vary visual treatment based on element importance

### Authentic Voice

- Copy should reflect brand personality
- Avoid generic marketing speak
- Be specific about value proposition

## Common High-Priority Targets

**Text:**

- "delve into" → delete or replace with "examine"
- "navigate the complexities" → "handle" or delete
- "in today's fast-paced world" → delete entirely
- Meta-commentary and preambles → cut to the point

**Code:**

- Generic names: `data` → name what data it represents
- Obvious comments: `// Create a user` before `user = User()` → delete
- Over-engineering: Unnecessary design patterns, multiple abstraction layers
- One-off utilities: Extract only when genuinely reused

**Design:**

- Purple/pink/cyan gradient backgrounds → use intentional color palette
- Floating 3D shapes without purpose → remove
- "Empower Your Business" type headlines → be specific about value
- Generic layouts → design for actual content

## Integration with Code-Deduplication and Coding-Discipline

These three skills work together:

- **output-quality** catches style and pattern smells in finished code
- **code-deduplication** prevents reimplementation of existing logic
- **coding-discipline** guides the writing process to avoid overcomplication from the start

Use output-quality for cleanup and review; use the other two to prevent problems from the start.

## Examples

For detailed before/after examples in text, code, and design, see [examples.md](references/examples.md).
