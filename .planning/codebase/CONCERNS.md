# Codebase Concerns

**Analysis Date:** 2026-04-02

## Tech Debt

**Massive Code Duplication in OOXML Validation Modules:**
- Issue: The `docx/ooxml/scripts/validation/` and `pptx/ooxml/scripts/validation/` directories contain byte-for-byte identical files. `base.py` (40,841 bytes), `docx.py` (10,249 bytes), `pptx.py` (12,642 bytes), `redlining.py` (11,456 bytes), `validate.py` (2,028 bytes), `__init__.py` (351 bytes), and `pack.py` (~5,800 bytes) are duplicated across both locations.
- Files:
  - `skills/documents/docx/ooxml/scripts/validation/base.py`
  - `skills/documents/pptx/ooxml/scripts/validation/base.py`
  - (all corresponding pairs in these two directories)
- Impact: Bug fixes or feature changes must be applied in two places. Any divergence introduces silent inconsistencies. The `__init__.py` in the pptx directory still says "Validation modules for Word document processing" (copy-paste from docx).
- Fix approach: Extract the shared validation logic into a single shared module (e.g., `skills/documents/_ooxml_shared/` or a package-level import). Both docx and pptx skills should import from the shared location.

**Duplicated pack.py and unpack.py Scripts:**
- Issue: `docx/ooxml/scripts/pack.py` and `pptx/ooxml/scripts/pack.py` are near-identical (~160 lines each). Same for `unpack.py`. The docx version includes inline script metadata (`# /// script`); the pptx version does not.
- Files:
  - `skills/documents/docx/ooxml/scripts/pack.py`
  - `skills/documents/pptx/ooxml/scripts/pack.py`
  - `skills/documents/docx/ooxml/scripts/unpack.py`
  - `skills/documents/pptx/ooxml/scripts/unpack.py`
- Impact: Inconsistent dependency declarations between the two copies.
- Fix approach: Consolidate into a single script or shared module.

**Hardcoded Database Credentials:**
- Issue: `skills/database/sqlmodel/scripts/init_db.py` uses `"postgresql://user:password@localhost:5432/dbname"` as the default fallback for `DATABASE_URL`. This default appears twice (lines 22 and 47).
- Files: `skills/database/sqlmodel/scripts/init_db.py`
- Impact: If a user runs the script without setting `DATABASE_URL`, it attempts to connect with placeholder credentials. The hardcoded `password` string is a security anti-pattern in template/example code.
- Fix approach: Use `None` as default and raise an explicit error if `DATABASE_URL` is not set. Remove the duplicated fallback string.

**Incomplete README.md:**
- Issue: `README.md` contains three `TODO` placeholders (lines 25, 29, 33) for the Commands, Skills, and Agents sections. These sections provide no useful information to users.
- Files: `README.md`
- Impact: New contributors/users have no overview of available content.
- Fix approach: Populate these sections with a listing of available skills, commands, and agent configurations.

**Most Python Scripts Lack Inline Script Metadata:**
- Issue: The `skills/AGENTS.md` requires inline script metadata (`# /// script`) for all skill scripts. Only 2 out of 40+ Python scripts comply (e.g., `docx/ooxml/scripts/pack.py`). The rest have no dependency declarations.
- Files: All `.py` files under `skills/` except `pack.py` in the docx subdirectory.
- Impact: `uv run` cannot auto-resolve dependencies for these scripts, breaking the documented workflow.
- Fix approach: Add `# /// script` metadata blocks to all scripts that import third-party packages.

**skills-lock.json Only Tracks 6 of 50+ Skills:**
- Issue: `skills-lock.json` contains hashes for only 6 skills (`coding-principles`, `python-cli`, `python-linter`, `python-no-type-checking-guard`, `python-standards`, `testing-strategy`). All other skills (3gpp-*, documents/*, mcp-servers/*, etc.) are untracked.
- Files: `skills-lock.json`
- Impact: No integrity verification for the majority of skills. Changes to untracked skills go undetected.
- Fix approach: Either extend the lock file to cover all skills or document which skills are externally managed vs. local.

## Security Considerations

**Hardcoded Credentials in Template Code:**
- Risk: `skills/database/sqlmodel/scripts/init_db.py` contains `"postgresql://user:password@localhost:5432/dbname"` as a default. While this is clearly a placeholder, it teaches users to embed credentials in code.
- Files: `skills/database/sqlmodel/scripts/init_db.py`
- Current mitigation: The function checks `DATABASE_URL` env var first.
- Recommendations: Raise `ValueError("DATABASE_URL environment variable is required")` instead of falling back to a hardcoded string. Add a comment explaining secure credential management.

**Missing .gitignore Patterns:**
- Risk: `.gitignore` only contains `uv.lock` and `__pycache__`. Missing patterns for `.venv/`, `*.pyc`, `.eggs/`, `*.egg-info/`, `.ruff_cache/`, IDE configs (`.idea/`, `.vscode/`), OS files (`.DS_Store`, `Thumbs.db`), and sensitive directories.
- Files: `.gitignore`
- Current mitigation: `.venv/` is present on disk but not explicitly in `.gitignore` (may be covered by a global gitignore).
- Recommendations: Add standard Python `.gitignore` patterns. Explicitly exclude `.venv/`.

## Fragile Areas

**Single Test File for Entire Codebase:**
- Issue: Only one test file exists: `skills/documents/pdf/scripts/check_bounding_boxes_test.py` (247 lines). The file explicitly states: "Currently this is not run automatically in CI; it's just for documentation and manual checking."
- Files: `skills/documents/pdf/scripts/check_bounding_boxes_test.py`
- Impact: All other scripts (database, docx, pptx, validation, skill-creator, etsi-spec) have zero test coverage. Regressions will go undetected.
- Safe modification: Add tests incrementally; use `pytest` as the runner.
- Test coverage: Virtually none. No CI pipeline exists.

**Large Monolithic Files:**
- Issue: Several Python files exceed reasonable size limits:
  - `skills/documents/docx/scripts/document.py` - 51,708 bytes (~1,200+ lines)
  - `skills/documents/docx/ooxml/scripts/validation/base.py` - 40,841 bytes (~951 lines)
  - `skills/documents/pptx/scripts/inventory.py` - 39,138 bytes
  - `skills/documents/pptx/scripts/html2pptx.js` - 38,773 bytes (~979 lines)
- Files: As listed above.
- Why fragile: Large files are harder to review, understand, and safely modify. Any change has higher blast radius.
- Safe modification: Extract logical sections into separate modules before making functional changes.

**Stale Import in docx validation __init__.py:**
- Issue: `skills/documents/docx/ooxml/scripts/validation/__init__.py` imports `PPTXSchemaValidator` (line 7). The pptx validation `__init__.py` has the same import. Both modules export both DOCX and PPTX validators, which may cause confusion about ownership.
- Files:
  - `skills/documents/docx/ooxml/scripts/validation/__init__.py`
  - `skills/documents/pptx/ooxml/scripts/validation/__init__.py`
- Why fragile: Cross-contamination of concerns. A docx skill should not export PPTX validators.
- Safe modification: Remove PPTX exports from docx __init__.py and vice versa.

**Test File Uses Relative Import Without Package Structure:**
- Issue: `check_bounding_boxes_test.py` contains `from check_bounding_boxes import get_bounding_box_messages` (bare import). This only works when the test is run from the same directory. There is no `__init__.py` in the `pdf/scripts/` directory.
- Files: `skills/documents/pdf/scripts/check_bounding_boxes_test.py`
- Why fragile: Test will fail when run from any other directory or via pytest discovery.
- Safe modification: Add proper package structure or use `sys.path` manipulation.

## Missing Critical Features

**No CI/CD Pipeline:**
- Problem: No `.github/workflows/`, no `Makefile`, no `tox.ini`, no CI configuration exists. Tests, linting, and formatting are defined only in `mise` tasks (`.config/mise/config.toml`).
- Blocks: Automated quality gates, PR validation, continuous integration.

**No LICENSE File:**
- Problem: `LICENSE` file is listed in the root directory but its content/validity should be verified.
- Blocks: Legal clarity for external contributors and users.

## Performance Bottlenecks

**No Performance Concerns Detected:**
- This is a collection of prompts, skills, and scripts. No runtime performance bottlenecks apply. The scripts run on-demand (manual invocation) rather than as a service.

## Scaling Limits

**skills-lock.json Hash Validation:**
- Current capacity: Only 6 skills tracked. Adding more requires manual entry.
- Limit: Manual maintenance becomes unsustainable as the skill collection grows.
- Scaling path: Automate hash generation and lock file updates via a script or CI step.

## Dependencies at Risk

**lxml Used Without Inline Metadata:**
- Risk: `skills/documents/*/ooxml/scripts/validation/base.py` imports `lxml.etree`, but none of these scripts declare `lxml` as a dependency via inline script metadata. Running via `uv run` will fail.
- Impact: Validation scripts are broken under the documented workflow (`uv run`).
- Files: All files under `skills/documents/*/ooxml/scripts/validation/`
- Migration plan: Add `# /// script` metadata with `"lxml"` dependency to all affected scripts.

**defusedxml Inconsistency:**
- Risk: `docx/ooxml/scripts/pack.py` declares `defusedxml` as a dependency via inline metadata. `pptx/ooxml/scripts/pack.py` (near-identical file) does not declare it.
- Impact: The pptx pack.py may fail under `uv run` if `defusedxml` is not already installed.
- Files:
  - `skills/documents/docx/ooxml/scripts/pack.py`
  - `skills/documents/pptx/ooxml/scripts/pack.py`
- Migration plan: Either add metadata to pptx version or consolidate the scripts.

---

*Concerns audit: 2026-04-02*
