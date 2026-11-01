# AGENTS.md — HISTORY

Recorded decisions with git references. Read when relevant to current task.
Acts as simple long-term memory for the project.

## Format

| Date | Decision | Rationale | Git ref |
|------|----------|-----------|---------|
| YYYY-MM-DD | [description] | [why] | [commit hash/tag] |
| 2026-10-30 | Migrated Python structural sorting from csort/Clean-sort to pyreorder. | Keeps the prior section, strategy, method-order and enabled-transform settings while using the successor CLI/config; explicitly disables pyreorder's new main-guard import hoist to avoid an unrequested import-timing change. | TBD |
| 2026-10-30 | Added a `mise typecheck` task, completed PEP 723 metadata for runnable scripts, and configured Ty for consumer-managed skill imports. | The repository contains standalone skill assets, not one Python application environment. Ty ignores unresolved imports while retaining all other type rules; revisit if application code is added. | TBD |
| 2026-08-18 | Retired `.planning/codebase/` snapshots; uplifted `.gitignore` with `.agents/history/`+`plans/` patterns from agents-scaffold `INSTALL.md`. | `.planning/codebase/*` (April-2026) was stale: dual-location skill model gone, OOXML paths gone, `saddle-cli` integrations shrunk. The same structural intent already lives in `AGENTS.md` + `.agents/*.md`, so deleting avoids drift. `.agents/plans/`/`history/` are forward-declared per template. | TBD |

## Guidance

- Record decisions that would be costly to rediscover.
- Note false turns and why they were rejected.
- Link to relevant commits.
- Keep entries brief — enough to reconstruct reasoning.
