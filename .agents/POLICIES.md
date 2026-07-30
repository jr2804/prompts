# AGENTS.md — POLICIES

Always applicable. Boundaries, priorities, verification, checklist.

## Priorities

1. Correctness
2. Evidence
3. Safety
4. Minimal changes
5. Consistency
6. Performance

## Boundaries

- NEVER fabricate paths, commits, APIs, config keys, env vars, test results, or benchmark numbers. If you don't know, say so.
- NEVER guess at command names, flags, or paths. Read source or run `--help`.
- NEVER add secrets, API keys, or tokens to files. Use env vars.
- NEVER run destructive commands (`rm -rf`, `git reset --hard`, `git push --force`) without explicit confirmation.
- NEVER delete or move files without explicit instruction.
- NEVER create temp files in project root. Use dedicated temp dir.

## Change constraints

- Minimal, surgical edits. Preserve existing style. No unrelated refactoring while fixing a bug.
- No new dependencies without explicit instruction.
- When changing tests, update only directly affected tests.

## Code quality

Universal defaults. Project-specific standards live in child AGENTS.md.

- **SRP** — one reason to change per module/function; if a name needs "and", split it.
- **DRY** — check before adding; extract on the _third_ occurrence (Rule of Three).
- **Redundant code** — remove dead branches, unreachable conditions, unused params/imports before finishing.
- Prefer a little duplication over the wrong premature abstraction.
- No new code-quality tooling, patterns, or value-object rules by default — opt in per project.

## Completion checklist

- Change solves the stated problem
- Relevant validation ran (or gaps explicitly stated)
- No unintended side effects introduced
- No secrets added or exposed

## DOX authoring (keep AGENTS.md lean)

AGENTS.md and `.agents/` files share limited context. Bloat and duplication
are the failure mode — they waste context on every entry to a subtree and
drift apart as rules change.

### Where a rule lives

Answer one question: **what is the highest (most general) tier that fully
applies?** Put the rule there and nowhere else.

- Applies to **all code in the project**, not one subtree →
  `.agents/POLICIES.md`. This is the default. When unsure, it goes here.
- Meaningful **only inside one subtree** (e.g. framework-specific template
  rules) → that subtree's `AGENTS.md`.
- Just helps navigation → the parent's Child DOX Index, nothing else.

`.agents/POLICIES.md` is the gravity well for universal rules. A subtree
AGENTS.md only contains rules that are meaningless outside that subtree.

### Reference, don't restate

A rule appears in **exactly one file**. Every other file that touches it
uses a **pointer line**: `<topic> — see <file>`. Never copy the rule, the
rationale, or the code example into the second file. If the canonical home
needs a code example, it lives there once — linked to, never duplicated.

### Rule first, rationale second, never third

A DOX line is the rule. If a rationale is costly to rediscover, add one
short clause. Never multi-paragraph explanations or more than one
❌/✅ code pair per rule — those belong in a skill or a `docs/` page, linked
once.

### Content rules

- **No tree views.** Generate on demand with `rg --files | tree-cli --fromfile`.
- **No history.** Git log has it. Record only decisions costly to rediscover
  (in `.agents/HISTORY.md` with commit refs).
- **No TODO lists.** Use issue trackers or beads.

### Size budget

- `.agents/` files: ≤ **120 lines**. They are always-injected context.
- Subtree `AGENTS.md`: ≤ **250 lines**. Loaded cumulatively with every
  parent on entry — the deep-path cost adds up fast.

Exceeding the budget signals the doc is restating instead of pointing, or
hoarding rationale. Cut first; split the subtree only as a last resort.

## Verification

```bash
# lint Python code
ruff check <paths> --fix

# run tests
uv run pytest <paths> -v --tb=short

# validate a skill against the Agent Skills spec
uvx skills-ref validate <path-to-skill>
```

## Response format

Concise and specific. No filler, intros, or restated requirements.
Answer direct questions directly.

For review/debugging/analysis: findings with references, conclusion,
approach. Mention caveats.

## Closeout

1. Run verification
2. Report docs intentionally left unchanged and why
