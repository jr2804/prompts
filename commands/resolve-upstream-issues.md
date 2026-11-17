---
name: resolve-upstream-issues
description: >-
  Check upstream repositories for open issues and triage/resolve them.
  Detects provider (GitHub, GitLab, Forgejo/Codeberg, Gitea, …) and uses the
  matching CLI (gh, glab, fj, …) to read and write issues. Goal: close all
  open issues — close when confident, reply for feedback when not. Also
  checks replies on already-handled issues. If no upstream repo or the host
  does not support issues, stop with a single-sentence notice.
---

# resolve upstream issues

Process all open issues on the upstream repository until every one is resolved
or pending human feedback. Prefer the provider-native CLI for all read/write
operations.

## CLI selection

Detect the upstream host from the git remote(s) (`git remote -v`) and pick the
matching CLI:

| Host / family | CLI | Example URL |
|---|---|---|
| GitHub | `gh` | `github.com/…` |
| GitLab | `glab` | `gitlab.com/…`, self-hosted GitLab |
| Forgejo / Codeberg / Gitea | `fj` | `codeberg.org/…`, `gitea.org/…`, self-hosted Gitea/Forgejo |
| Other / unknown | — | — |

If no remote points at a known issue-tracking host, or the host is not one of
the above, state exactly:

`No supported issue tracker detected on the upstream remote(s).`

… and stop.

## Workflow

1. **Enumerate upstream repos** — run `git remote -v`. For every remote that
   maps to a supported provider, note the host and owner/repo. If multiple
   providers are configured, process each one in turn (see "Multi-repo" below).

2. **Detect provider & verify CLI** — for each repo, identify the provider and
   confirm the CLI is available (`gh --version`, `glab --version`, `fj --version`).
   If the CLI is missing, state which CLI is missing and stop for that repo.

3. **List open issues** — use the provider CLI to list all open issues
   (include labels if useful for triage). Record issue number, title, and
   state (open / closed).

4. **Check replies on previously-handled issues** — for any issue that was
   already worked on in a prior run, pull the comment thread (or check for new
   reactions/assignments since the last interaction). Summarise new input and
   incorporate it into the next step.

5. **Work on each open issue** — for every open issue that has not yet been
   closed this session:
   - Read the issue body and all comments.
   - Diagnose the root cause in the local codebase.
   - Implement the fix, following repository conventions.
   - Verify the fix (run relevant tests, linters, or manual checks).
   - If the issue is fully resolved, prepare to close it (see step 6).
   - If you are **not confident** the fix is complete or correct, leave the
     issue open and post a reply with:
     - what you did and why
     - what remains uncertain
     - a concrete request for feedback or a minimal reproduction / test case
   - If the issue is **invalid / out of scope / duplicate**, post a reply
     explaining the decision and close it.

6. **Close or request feedback** — for each issue handled this session:
   - **Close** (via CLI: `gh issue close`, `glab issue close`, `fj issue close`)
     when you are confident the fix is correct and verified. Add a closing
     comment that documents:
     - root cause
     - what was changed (files / functions / commit, if a commit exists)
     - how to verify (test command, expected behaviour)
   - **Do not close** when confidence is below threshold; instead post a
     reply requesting feedback as described in step 5.

7. **Multi-repo** — if step 1 found multiple upstream repos, repeat steps 2–6
   for each. After all repos are processed, summarise per repo:
   - number of open issues found
   - number closed
   - number left open awaiting feedback (with issue URLs)
   - any repos skipped because the CLI was unavailable

8. **Final report** — end with a concise summary table:

   | Repo | Provider | CLI | Open found | Closed | Awaiting feedback |
   |------|----------|-----|------------|--------|-------------------|

   followed by one line per skipped repo, if any.

## Notes

- `$ARGUMENTS` can narrow the scope: e.g. `only issue #42` or `repo foo/bar`.
  Without arguments, process all open issues on all detected upstream repos.
- Never force-close an issue you are not confident about; prefer a feedback
  request.
- Keep replies short, specific, and actionable. Reference exact file paths,
  functions, and verification commands.
