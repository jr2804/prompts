---
name: beads-start-work
description: Start work on a specific beads issue or the most urgent one - what needs to be fixed/closed before the next release or push - and keep the tracker accurate afterwards
---

# beads start work

Check tracker availability first, exactly as the `beads` skill requires (CLI
`bd --version`, otherwise the beads MCP server tools). If neither interface
is available or working, state exactly `beads issue tracker not installed.`
and stop.

Parse `$ARGUMENTS`: issue IDs select the work; everything else is an
additional instruction for this run.

Run the `beads` skill's **start work** command, defined in
`skills/tools/beads/references/start-work.md`:

- With issue IDs → start work on those issues (reopen if closed).
- Without → pick the most urgent issue(s) yourself, judged by "what needs to
  be fixed/closed before we can make a new release/push?", and announce the
  choice with its reason before starting.

Claim the issue (`bd update <id> --claim`), do the work following the
repository's own conventions, and always close the loop on the tracker:
close with a reason, record partial progress and findings (new issues via
`--deps discovered-from:<id>`), and complete epics when all their children
are done.
