---
name: beads-consolidate
description: Consolidate and evaluate all beads issues - close or refresh stale ones, merge duplicates and overlapping issues, and sort everything under epic issues
---

# beads consolidate

Check tracker availability first, exactly as the `beads` skill requires (CLI
`bd --version`, otherwise the beads MCP server tools). If neither interface
is available or working, state exactly `beads issue tracker not installed.`
and stop.

Run the `beads` skill's **consolidate** command, defined in
`skills/tools/beads/references/consolidate.md`: evaluate all issues in the
tracker, close or refresh stale ones, merge exact and overlapping duplicates
into their canonical issue, and attach every actionable issue as a child
below an epic issue (sub-epics and further sub-items allowed). Verify the
result (`bd dep cycles`, orphan sweep, `bd doctor --check=conventions`) and
report every mutation with its reason. Never delete issues; close or mark
duplicates instead.

Any `$ARGUMENTS` are additional instructions for this run (for example a
different staleness threshold or issues to leave untouched).
