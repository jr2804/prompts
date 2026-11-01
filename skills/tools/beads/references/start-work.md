# Start work on beads issues

Begin work on a specific issue or on the most urgent one, judged by the
question: "what needs to be fixed/closed before we can make a new
release/push?" Afterwards, keep the tracker accurate — an issue that was
handled but left open is the most common failure mode here.

## 1. Select the issue(s)

**Specific issue given** → skip selection. Confirm it exists and is open:

```bash
bd show <id>
```

If it is closed but needs renewed work, `bd reopen <id>` first.

**No issue given** → pick the most urgent work:

List candidates that are actually actionable now:

```bash
bd ready --json -n 25      # open, unblocked, priority-sorted (0 = highest)
bd blocked --json          # blocked work — a blocker here may itself be urgent
bd list -t epic --json     # epics reveal release-readiness themes
```

1. Judge release relevance from titles, descriptions, epic membership, and
   priority: ask for each candidate "does this block a release or push?"
   Prefer work that unblocks other issues (check `bd dep tree <id>`).
2. Pick the minimal set of issues that unblocks the release. Announce the
   choice and the reason in one or two sentences before starting. Ask the
   user only when the choice is genuinely ambiguous.

## 2. Claim it

```bash
bd update <id> --claim       # sets assignee and status to in_progress
```

`bd ready --claim` combines listing and claiming when working from the
candidate list. Work only on issues you claimed; keep the count small
(one or two at a time).

## 3. Do the work

Implement, test, and commit following the repository's own conventions —
this skill governs the tracker, not the code. If the work uncovers new
defects or ideas, capture them immediately so they are not lost:

```bash
bd create "<Title>" -t bug --deps discovered-from:<id> --silent
```

Record non-trivial findings on the issue itself:

```bash
bd update <id> --append-notes "<finding>"
```

## 4. Close the loop (never skip)

Handling an issue includes updating the tracker. After finishing:

- **Fixed / resolved** → `bd close <id> --reason "<what was done>"`
- **Partially done** → `bd update <id> --append-notes "<progress, what remains>"`,
  keep it `in_progress`, or set it back to `open` with updated priority
- **Rejected / obsolete** → close it with that reason instead of leaving it

Then keep the structure current:

- When all children of an epic are done:
  `bd epic close-eligible --dry-run`, then the real run.
- To continue with the next most urgent issue, `bd close --suggest-next`
  shows newly unblocked candidates; otherwise report the state and stop.

## 5. Report

End with: issue(s) claimed and their outcome (closed / still open with
remaining work), commits or changes made, new issues created, and epics
affected.
