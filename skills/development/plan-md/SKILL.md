______________________________________________________________________

## name: plan-md description: Create and maintain a PLAN.md living document for feature implementations that require more than 1-2 prompts but are not full project specs. Use when a feature spans multiple files or components, involves architectural decisions, or needs more than 2 conversation turns to implement. Produces a lightweight markdown planning document placed at docs/PLAN-<feature-name>.md before coding begins, then updated throughout execution with progress, decisions, and discoveries.

# Plan-MD: Feature Implementation Planning

Guide for creating and maintaining a `PLAN.md` — a lightweight living planning document for medium-complexity features.

## When to Use

Create a PLAN.md when **all** of the following are true:

- The feature requires **more than 2 prompts** to implement
- It touches **multiple files or components**
- It involves **non-trivial decisions** (architecture, data model, API design)

Skip PLAN.md when:

- It's a quick fix or single-file edit
- The request is exploratory / throwaway
- A full spec already exists (use a dedicated spec tool instead)
- You can see the complete solution in your head right now

**Scope sweet spot:** 3–15 prompts of work, 3–10 files affected.

## Creating a PLAN.md

### Step 1: Research first

Before writing a single plan line, explore the codebase:

- Identify the key files that will be touched (full repo-relative paths)
- Understand the existing patterns to follow
- Note any constraints or dependencies

### Step 2: Write the plan

Follow the section guide below and the annotated template in [`references/template.md`](references/template.md). Keep it concise — aim for 50–100 lines, not 500.

**Core structure:**

1. **Goal** — What the user gains (2–3 sentences, user perspective, observable)
1. **Context** — Current state, key files, constraints (bullets, full paths)
1. **Phases** — 2–4 phases, each with a deliverable + checkbox tasks
1. **Validation** — Observable acceptance criteria (exact commands or UI actions)
1. **Progress** — Living checklist, updated with timestamps
1. **Decisions** — Key choices + rationale, recorded as made
1. **Notes** — Surprises, blockers, discoveries (added during implementation)

### Step 3: Place and commit

Save to `docs/PLAN-<feature-name>.md` in the project. Commit before writing any code:

```
git add docs/PLAN-<feature-name>.md
git commit -m "plan: add PLAN.md for <feature-name>"
```

### Step 4: Execute phase by phase

Implement one phase at a time. After each phase, update Progress and commit.

## Maintaining the Plan (Living Document)

The PLAN.md is a living document — update it as you work:

**After each stopping point:**

- Check off completed tasks in Progress with a timestamp: `- [x] (2025-10-01 14:00Z) Task done`
- If a task split mid-way, add sub-items before checking the parent off

**When making a non-obvious decision:**

- Add to Decisions: `- Decision: [what] / Rationale: [why] / Date: [date]`

**When hitting surprises or blockers:**

- Add to Notes immediately; don't batch until the end

**At phase completion:**

- Mark phase tasks complete in both the Phases section and Progress
- Verify the deliverable actually exists before moving to the next phase

**At implementation end:**

- Ensure all Validation criteria are checked off
- Add a brief retrospective in Notes if lessons learned are worth capturing

## PLAN.md Section Guide

See [`references/template.md`](references/template.md) for the full annotated template and [`references/example.md`](references/example.md) for a complete realistic example.

**Goal:** User-visible outcome in 2–3 sentences. Start with "After this:" or "This enables:". State how to observe it working. Avoid internal details ("adds a middleware") — describe behavior ("users can log in with GitHub OAuth").

**Context:** Bullets only. Current state in one sentence. Key files as full repo-relative paths. Any locked-in constraints or out-of-scope items.

**Phases:** 2–4 phases. Each phase must have: a name, a Deliverable statement (what concretely exists at end), and checkbox tasks. All tasks that could produce a commit should be a separate task.

**Validation:** Each criterion phrased as observable behavior — "Run `X`, expect `Y`" or "Navigate to Z, see W." Not internal ("code compiles") — something a human can verify.

**Progress:** The one section updated continuously. Start with `- [x] (timestamp) Created PLAN.md`. Add new items freely; never delete old ones — mark done instead.

**Decisions:** Add as decisions are made, not after. Format: `- Decision: ... / Rationale: ... / Date: ...`

**Notes:** Anything unexpected. Include evidence (test output, commands) where it proves the observation.

## Integration with Other Skills

- **test-driven-development**: Add test tasks to each phase — write tests before the implementation task
- **subagent-driven-development**: Dispatch one subagent per phase for cleaner context isolation
