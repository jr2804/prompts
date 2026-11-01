---
name: beads
description: >-
  Work with the beads issue tracker through the bd CLI or the beads MCP
  server. Covers consolidating and evaluating issues — closing stale ones,
  merging exact and overlapping duplicates, and organizing every issue under
  epics via parent-child dependencies — and starting work on a specific or
  the most urgent issue, such as what must be fixed before the next release
  or push. Use when the user mentions beads, bd, issue triage, duplicate
  issues, epic hierarchy, release blockers, or asks what to work on next.
---

# beads

Issue-tracker workflows for [beads](https://github.com/gastownhall/beads)
("issues chained together like beads"). Two commands:

1. **Consolidate** — evaluate all issues: close or refresh stale ones, merge
   duplicates and high-overlap issues, and sort everything as child items
   below epic issues (including further sub-items).
   Follow [references/consolidate.md](references/consolidate.md).
2. **Start work** — begin work on a specific issue, or on the most urgent
   one, judged by "what needs to be fixed/closed before we can make a new
   release/push?" — and keep the tracker accurate afterwards.
   Follow [references/start-work.md](references/start-work.md).

## Availability check (always first)

Before any workflow step, verify the tracker is usable:

1. **CLI**: run `bd --version`. A zero exit with a version string means the
   CLI works.
2. **MCP**: if the CLI is unavailable, check whether the beads MCP server
   tools are available in this session.

If neither interface is available or working, state exactly:

```text
beads issue tracker not installed.
```

and stop. Do not attempt either workflow.

If the CLI works but the project has no beads database (commands fail with a
"not initialized" or missing `.beads/` error), beads is installed but not set
up for this project. Report that and ask before running `bd init` —
initialization creates `.beads/`, picks an issue prefix, writes agent-file
snippets, and may install git hooks.

## Interface selection

- **Prefer the CLI** (`bd ...`) when available: it is scriptable, requires
  explicit issue IDs in non-interactive sessions, and supports `--json` on
  every command for reliable parsing.
- **Use the beads MCP server tools** when the CLI is unavailable: map each
  step to the closest tool (list/show, create, update, close, duplicate,
  dependency operations). Steps that read `--json` output translate to the
  tools' structured results.
- Both interfaces operate on the same database; do not interleave them
  within a single logical change.

## Project conventions

Run `bd prime` once at the start of a work session. It prints the project's
canonical beads workflow context and persistent memories (a project can
customize it via `.beads/PRIME.md`). Follow it wherever it adds project-specific
rules; this skill defines the two commands themselves.

## Rules that apply to both commands

- **Explicit IDs everywhere.** In scripts and agent sessions, `bd update`
  and `bd close` refuse to act on a "last touched" issue. Never build a
  command from an empty variable; always name the target issue.
- **Close-out is part of done.** After handling an issue — fixing,
  rejecting, or superseding it — update or close it in the same session.
  An agent that finishes work but leaves the issue open creates exactly the
  stale backlog this skill exists to clean up.
- **Prefer reversible states over deletion.** Close, mark duplicates, or
  supersede instead of `bd delete`. Deletion loses history and references.
- **Parse with `--json`.** Human-readable output is for reports; decisions
  should read structured JSON fields (`status`, `priority`, `parent`,
  `issue_type`, `updated_at`).
- **Report every mutation.** End with a short summary of what was closed,
  merged, created, attached, or claimed, each with its one-line reason.
