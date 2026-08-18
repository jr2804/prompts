# AGENTS.md — HISTORY

Recorded decisions with git references. Read when relevant to current task.
Acts as simple long-term memory for the project.

## Format

| Date | Decision | Rationale | Git ref |
|------|----------|-----------|---------|
| YYYY-MM-DD | [description] | [why] | [commit hash/tag] |
| 2026-08-18 | Retired `.planning/codebase/` snapshots; uplifted `.gitignore` with `.agents/history/`+`plans/` patterns from agents-scaffold `INSTALL.md`. | `.planning/codebase/*` (April-2026) was stale: dual-location skill model gone, OOXML paths gone, `saddle-cli` integrations shrunk. The same structural intent already lives in `AGENTS.md` + `.agents/*.md`, so deleting avoids drift. `.agents/plans/`/`history/` are forward-declared per template. | TBD |

## Guidance

- Record decisions that would be costly to rediscover.
- Note false turns and why they were rejected.
- Link to relevant commits.
- Keep entries brief — enough to reconstruct reasoning.
