______________________________________________________________________

## name: "create-plan-md" description: "Create a PLAN.md in the project root for medium-complexity features by collecting required inputs first, then using the plan-md skill. Trigger phrases: 'create plan.md', 'plan this feature', 'start implementation plan'."

# createPlanMd

Create a high-quality `PLAN.md` as a living implementation plan.

## Workflow

1. **Trigger the skill immediately**

   - Use skill `plan-md` for structure, guardrails, and maintenance rules.

1. **Handle existing PLAN.md**

   - If `PLAN.md` already exists in the project root:
     - Read and analyze the existing file
     - Extract the feature title from the `# PLAN:` heading
     - Rename to `PLAN-<feature-title>.md` (slugify the title, lowercase, replace spaces with hyphens)
     - Inform user: "Existing plan archived as PLAN-<feature-title>.md"
   - If no feature title found, rename to `PLAN-archived-<timestamp>.md`

1. **Collect required inputs before writing the plan**

   - If `$ARGUMENTS` is missing or incomplete, ask for the following in one concise questionnaire:
     - Feature title (short, action-oriented)
     - User-visible goal (what users can do after the change)
     - In scope / out of scope
     - Key files or modules likely affected
     - Technical constraints (libraries, APIs, compatibility, performance)
     - Validation criteria (commands, observable behavior, acceptance checks)
     - Risks and unknowns
     - Preferred rollout order or milestones
   - If `$ARGUMENTS` is present, parse it and only ask follow-up questions for missing fields.

1. **Research code context**

   - Inspect the repository areas related to the feature.
   - Confirm or refine the key files list with full repo-relative paths.
   - Identify existing implementation patterns to follow.
   - **Read key files** to capture patterns, dependencies, and context needed for self-contained plan.

1. **Generate the plan file**

   - Create `PLAN.md` in the **project root** using the `plan-md` skill template.
   - Ensure sections are complete and **self-contained**:
     - Goal (user-visible outcome)
     - Context (files, patterns, dependencies, environment setup)
     - Phases (specific files and functions to create/modify)
     - Validation (exact commands with working directory)
     - Progress (initial entry)
     - Decisions (empty, to be filled as decisions are made)
     - Notes (empty, to be filled during implementation)
   - Add the initial progress entry:
     - `- [x] (<timestamp>) Created PLAN.md`

1. **Quality gate before finishing**

   - Verify the plan is:
     - **Self-contained**: A fresh session could implement with only this file
     - Specific and observable (not vague)
     - Phase-based (2-4 phases with deliverables)
     - Grounded in real file paths
     - Explicit about validation commands/behaviors
     - Ready for implementation without further planning

1. **Return a concise summary**

   - Report file path (`PLAN.md`), feature name, and any remaining open questions (if any).
   - Remind user: "A fresh agent session can implement by reading @PLAN.md"

## Notes

- Use this command for features that require more than 1-2 prompts and touch multiple files/components.
- Skip this command for trivial one-file fixes or quick edits.
- The resulting plan is a living document and must be updated during implementation.
- **Existing PLAN.md is preserved**: automatically renamed to `PLAN-<feature-title>.md` before creating new plan.
- When complete: archive to `docs/PLAN-<feature-name>-complete.md` or delete.
