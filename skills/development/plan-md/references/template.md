# PLAN.md Template

Copy this template to `PLAN.md` in the **project root**.
Replace all placeholder text and delete the HTML comments before committing.

When complete: archive to `docs/PLAN-<feature-name>-complete.md` or delete.

______________________________________________________________________

# PLAN: <Short action-oriented feature title>

<!-- Goal: 2-3 sentences explaining what the user gains.
     Write from the user's perspective, not the code's.
     State how someone can observe it working.
     Do NOT describe internal code structure ("adds a middleware").
     DO describe behavior ("users can sign in with GitHub and land on /dashboard"). -->

## Goal

<User-visible outcome. What can someone do after this that they could not do before?
How do they observe it working? 2-3 sentences max.>

<!-- Context: MUST BE SELF-CONTAINED for fresh session handoff.
     A new agent session with ONLY this file must be able to implement.
     Include: current state, key files with roles, patterns to follow,
     dependencies, environment setup, and constraints. -->

## Context

- **Current state:** <Brief description of what exists today that this feature builds on or changes>

- **Key files:**
  - `path/to/relevant/file.ts` — <what it does / why it matters / key functions or patterns>
  - `path/to/another/file.py` — <role in this feature / important classes or functions>

- **Patterns to follow:**
  - <Describe the existing pattern to match, e.g., "Error handling uses Result<T, E> pattern">
  - <Include brief code example if non-obvious:>
    ```
    // Example: How errors are currently handled in this codebase
    def process() -> Result[Data, Error]:
        ...
    ```

- **Dependencies:**
  - <Package/module needed>: <how to verify installed, e.g., `pip show <pkg>`>
  - <Any version requirements>

- **Environment:**
  - <Env vars needed, e.g., `DATABASE_URL`>
  - <Config files to create/modify>
  - <Services that must be running>

- **Constraints:** <Locked-in tech choices, compatibility requirements, or explicitly out-of-scope items>

<!-- Phases: Break the work into 2-4 sequential phases.
     Each phase should be independently committable and verifiable.
     Start small: Phase 1 is often just the data model, interface, or simplest path.
     Each phase needs: a name, a Deliverable statement, and checkbox tasks.
     Tasks must be specific: file name + function/class/route to create or modify.
     Add test tasks to each phase (pairs with test-driven-development skill). -->

## Phases

### Phase 1: <Name, e.g. "Data Model" or "Core Interface">

**Deliverable:** <What concretely exists at end of this phase — a passing test suite,
a migrated schema, a working endpoint, a functional CLI command>

- [ ] Create/modify `path/to/file.ts` — add `<ClassName>` with `<method>` that does `<behavior>`
- [ ] Create `path/to/test.ts` — test cases for `<scenario>`
- [ ] <Another specific task with file and function names>

### Phase 2: <Name>

**Deliverable:** <Deliverable>

- [ ] <Specific task with file path and function name>
- [ ] <Test task>

<!-- Add Phase 3 and Phase 4 as needed. Rarely need more than 4 phases.
     If you find yourself writing 5+ phases, consider splitting into two PLAN.md files. -->

<!-- Validation: Observable acceptance criteria.
     MUST include exact commands with working directory.
     Each criterion must be something a human (or automated check) can verify.
     Bad: "authentication works"
     Good: "POST /api/auth/github with a valid code returns 200 and sets a session cookie" -->

## Validation

- [ ] Run `<command>` from `<directory>`, expect `<output or exit code>`
- [ ] Navigate to `<URL>`, observe `<specific behavior or UI state>`
- [ ] Call `<endpoint>` with `<input>`, receive `<exact response shape>`

<!-- Progress: Living checklist. Updated continuously during implementation.
     Add timestamps. NEVER delete entries — mark as done instead.
     Split a partially done task into done + remaining sub-items if needed.
     This is the PRIMARY tracking mechanism — update frequently. -->

## Progress

- [x] (<YYYY-MM-DD HH:MMZ>) Created PLAN.md
- [ ] Phase 1 complete
- [ ] Phase 2 complete
- [ ] All validation criteria met

<!-- Decisions: Record key non-obvious choices as they are made — not after.
     Only decisions that future contributors should understand.
     Include enough context for a fresh reader.
     Format: Decision / Rationale / Date -->

## Decisions

<!-- - Decision: Used JWT over sessions / Rationale: Stateless; simpler in serverless env / Date: 2025-10-01 -->

<!-- Notes: Surprises, blockers, discoveries, lessons learned.
     Add immediately when encountered — do not batch until the end.
     Include evidence (test output, error messages, file paths) when useful. -->

## Notes

<!-- Add notes during implementation as things are discovered. -->
