# Consolidate beads issues

Evaluate all issues in the tracker and leave it in a clean, structured state:
stale issues are closed or refreshed, exact and overlapping duplicates are
merged, and every actionable issue lives under an epic as a child item
(sub-epics and deeper sub-items are allowed). Work in that order — merging
before hierarchy, so merged-away issues are not reparented first.

Run read-only passes first (`bd status`, `bd list`, the passes below), decide,
then apply changes. Never call `bd delete`; close or mark duplicates instead.

## 1. Snapshot

```bash
bd status                      # database overview
bd list --all --json -n 0 --brief   # every issue, compact fields
```

## 2. Stale issues

Candidates:

```bash
bd stale --days 30 --json      # no activity for 30+ days (min value: 1)
```

For each stale issue, read `bd show <id>` and judge relevance. Close only
with a reason; never delete.

- **Obsolete or done elsewhere** → `bd close <id> --reason "obsolete: <why>"`
- **Still relevant but forgotten** → refresh: `bd update <id> -p <0-4> --append-notes "<why it still matters>"`; add a clearer title or type if needed
- **Abandoned work-in-progress** → either reclaim it (`bd update <id> --claim`)
  or close it as abandoned; reopening later is cheap

## 3. Exact duplicates

`bd duplicates --json` groups issues with identical content and proposes a
merge target (most referenced, then smallest ID).

```bash
bd duplicates --json           # review groups first
bd duplicates --dry-run        # preview the merge
bd duplicates --auto-merge     # apply (only after reviewing)
```

For a single pair, prefer the explicit form:

```bash
bd duplicate <duplicate-id> --of <canonical-id>
```

This marks the duplicate and closes it with a reference to the canonical
issue. Pick the canonical issue yourself when the proposal is wrong (older,
better described, or more referenced wins).

## 4. Overlapping issues (not byte-identical)

```bash
bd find-duplicates --json --threshold 0.3
```

Default threshold is 0.5; lower it to catch loose overlap, raise it to reduce
noise. Score 1.0 is an exact duplicate, ~0.5 is likely overlap. For each
candidate pair, read both issues and decide:

- **Same work** → merge: append the duplicate's useful details to the
  canonical issue (`bd update <canonical> --append-notes "..."`), then
  `bd duplicate <duplicate-id> --of <canonical-id>`.
- **Related but distinct** → keep both: sharpen the titles so future
  duplicate detection improves, and optionally link them with
  `bd dep relate <id-a> <id-b>`.

## 5. Epic hierarchy

Goal: every actionable (non-epic) issue has a parent, directly or through a
sub-epic or sub-item chain.

```bash
bd list -t epic --json         # existing epics
bd list --no-parent --json     # all unparented issues (epics and orphans)
```

`bd list --no-parent` is the reliable orphan sweep; compound queries like
`bd query 'parent=none'` do not match orphans reliably.

For each unparented non-epic issue:

1. Pick a fitting existing epic, or create one:
   `bd create "<Epic title>" -t epic` (optionally with a sub-epic parent via
   `--parent`).
2. Attach the child: `bd update <id> --parent <epic-id>` — this creates the
   parent-child dependency. Children can have children; prefer a depth of at
   most 2–3 levels (epic → sub-epic/task → sub-item).
3. Order work inside an epic with blocking dependencies where sequencing
   matters: `bd dep add <blocked-id> <blocker-id>`.
4. Keep epics healthy: `bd epic status`, and close finished ones with
   `bd epic close-eligible --dry-run` followed by the real run.

Do not force a parent onto issues that are genuinely standalone; if several
such issues share a theme, that theme is a missing epic — create it.

## 6. Verify and report

```bash
bd dep cycles                       # must report no cycles
bd list --no-parent --json          # only epics should remain here
bd doctor --check=conventions       # advisory hygiene report (see bd lint)
```

Summarize: issues closed (with reasons), duplicates merged (duplicate →
canonical), epics created, issues attached (child → parent), issues
refreshed, and any issues left open deliberately.
