# AGENTS.md — HISTORY

Recorded decisions with git references. Read when relevant to current task.
Acts as simple long-term memory for the project.

## Format

| Date | Decision | Rationale | Git ref |
|------|----------|-----------|---------|
| YYYY-MM-DD | [description] | [why] | [commit hash/tag] |
| 2026-11-04 | Consolidated Python antipattern scanning into one `skills/development/python-ultimate/assets/check_antipatterns.py` holding only `IMPORT-ERROR-GUARD` and a configurable `BANNED-NOQA`; added a rule-to-tool ownership table to `references/linter-rules.md`. Both scanners now exit `2` when a scan is vacuous or a file cannot be parsed. | A linter already owns `PLW0603`, `PGH004`, `RUF100`, `PTH`, `UP045`, `PLC0415` and `TCH`; re-implementing them in scripts produced gates that could not be trusted. Only the two rules needing project dependency context lack a Ruff equivalent. The exit-`2` contract exists because `check_path_naming.py` used to report success on an empty directory and on unparseable files. | 7a910f4 |
| 2026-11-04 | Guarded `assets/examples/` with a nested `.ruff.toml` (`exclude = ["*"]`) and restored the deliberately non-compliant fixture content. | The repo `mise lint` task runs `ruff check --fix --unsafe-fixes`; it silently rewrote `fixture_type_and_imports.py` in `08ac78f`, deleting the very patterns the fixture exists to detect. Any future autofix run must not reach the fixtures. | 7a910f4 |
| 2026-11-04 | Classified scanner lookup tables by how a wrong entry fails, in `skills/development/python-ultimate/references/linter-rules.md`: container (`KeyError`), narrows (silent), widens (loud), and unclassified (no reader). Added `assets/test_check_antipatterns.py` `ModuleConstantTest` to flag module-level names never read in their own file. | Measured rather than reasoned: a wrong `_ALIAS_HINTS` entry is silent in a PEP 723 script but loud when the entry is missing, the inverse of what the code comment claimed; and a partial `SKIP_DIRS` entry leaves a non-empty scan that reports a quiet `0`, so the exit-`2` coverage check makes *total* narrowing safe, not narrowing. The no-reader class was found in a sibling project after `scan_global_usage` was deleted while its allowlist constant and comment stayed behind — coverage, guess-direction, and table checks all pass by absence. | a756a48 |
| 2026-11-02 | Added `tools/beads` skill: consolidate (close/refresh stale, merge duplicates, epic hierarchy) and start-work (most urgent release-relevant issue, close-out loop) commands, guarded by exact `beads issue tracker not installed.` message when neither `bd` CLI nor beads MCP tools respond; exposed as slash-commands `commands/beads-consolidate.md` and `commands/beads-start-work.md`. | bd command semantics were verified in a sandbox (notably: `bd list --no-parent` is the reliable orphan sweep while `bd query 'parent=none'` misses orphans); one skill with judgment-driven workflows fits the repo better than deterministic mise tasks. | TBD |
| 2026-10-30 | Migrated Python structural sorting from csort/Clean-sort to pyreorder. | Keeps the prior section, strategy, method-order and enabled-transform settings while using the successor CLI/config; explicitly disables pyreorder's new main-guard import hoist to avoid an unrequested import-timing change. | 45c39c5 |
| 2026-10-30 | Added a `mise typecheck` task, completed PEP 723 metadata for runnable scripts, and configured Ty for consumer-managed skill imports. | The repository contains standalone skill assets, not one Python application environment. Ty ignores unresolved imports while retaining all other type rules; revisit if application code is added. | 23d7e95 |
| 2026-08-18 | Retired `.planning/codebase/` snapshots; uplifted `.gitignore` with `.agents/history/`+`plans/` patterns from agents-scaffold `INSTALL.md`. | `.planning/codebase/*` (April-2026) was stale: dual-location skill model gone, OOXML paths gone, `saddle-cli` integrations shrunk. The same structural intent already lives in `AGENTS.md` + `.agents/*.md`, so deleting avoids drift. `.agents/plans/`/`history/` are forward-declared per template. | TBD |

## Guidance

- Record decisions that would be costly to rediscover.
- Note false turns and why they were rejected.
- Link to relevant commits.
- Keep entries brief — enough to reconstruct reasoning.
