# Standards skills -- gap analysis

Generated: 2026-05-21. 21 skills reviewed across 3 SDOs + common layer.

## Inventory

| Layer | 3GPP | ITU-T | ETSI | Common (sdo-) |
|-------|------|-------|------|---------------|
| **1. Common** | -- | -- | -- | 5 skills |
| **2. Reference** | 8 skills | 3 skills | 2 skills | -- |
| **3. Drafting** | 1 skill | 1 skill | 1 skill | -- |
| **Total** | 9 | 4 | 3 | 5 = **21** |

---

## A. Missing skills (planned, not yet created)

| Skill | SDO | Priority | Why needed |
|-------|-----|----------|-----------|
| `itut-meetings` | ITU-T | **Medium** | Referenced by `itut-drafting` cross-refs. A.1 has detailed meeting scheduling, collective letter timing, cancellation criteria -- currently only summarised in `itut-basics`. |
| `etsi-meetings` | ETSI | **Medium** | Needed for complete ETSI coverage. No meeting structure/procedures skill exists. |
| `etsi-contributions` | ETSI | **Medium** | Contribution submission procedures, templates, TDoc numbering. Neither EDR nor the Guide cover this. |
| `etsi-work-items` | ETSI | **Low** | Work Item lifecycle (creation, approval, tracking). Partially covered in `etsi-basics`. |
| `3gpp-spec-retrieval` | 3GPP | **Low** | Parallel to `etsi-spec`. 3GPP has FTP access patterns in `3gpp-specifications` but no dedicated retrieval script. |
| `itut-spec-retrieval` | ITU-T | **Low** | Parallel to `etsi-spec`. ITU-T Recommendations are accessible via handle.itu.int URLs. |

---

## B. Cross-reference gaps

| Skill | References | Issue |
|-------|-----------|-------|
| `itut-drafting` | `itut-meetings` | Skill does not exist (see missing skills above) |
| `sdo-docx-operations` | `docx-svg` | Valid skill in `skills/documents/`, not `skills/standards/`. OK but noted. |
| `sdo-docx-formatting` | `3gpp-drafting` | Should reference it (already references `etsi-drafting` and `itut-drafting` but missing 3GPP) |

Older Layer 2 skills (`3gpp-*` reference skills) use `@skill-name` format
rather than `\`skill-name\`` -- these are not machine-detectable and should
be updated for consistency with the newer skills.

---

## C. Capability coverage by SDO

| Capability | 3GPP | ITU-T | ETSI |
|-----------|------|-------|------|
| Organisation basics | `3gpp-basics` | `itut-basics` | `etsi-basics` |
| Meeting structure | `3gpp-meetings` | **missing** | **missing** |
| Working groups | `3gpp-working-groups` | *(in basics)* | *(not applicable)* |
| Contributions/submissions | `3gpp-tdocs` (data) | `itut-contributions` | **missing** |
| Change requests | `3gpp-change-request` | *(in basics)* | *(not applicable)* |
| Spec numbering/formats | `3gpp-specifications` | `itut-recommendations` | `etsi-spec` |
| Spec retrieval script | **missing** | **missing** | `etsi-spec` |
| Release structure | `3gpp-releases` | *(in basics)* | *(not applicable)* |
| Portal authentication | `3gpp-portal-auth` | **missing** | **missing** |
| Work items | *(partial, in basics)* | *(in basics)* | **missing** |
| Drafting (.docx) | `3gpp-drafting` | `itut-drafting` | `etsi-drafting` |
| Style-name mapping | table in drafting | table in drafting | table in drafting |
| Drafting template | Tdoc_Template.docx | template.docx | **missing** |
| Project setup | `sdo-project-setup` | `sdo-project-setup` | `sdo-project-setup` |

---

## D. Feature completeness of existing skills

### Common layer (sdo-)

| Skill | Depth | Gaps |
|-------|-------|------|
| `sdo-docx-formatting` | High -- 6 reference files | Missing: `3gpp-drafting` in cross-refs |
| `sdo-docx-operations` | High -- 5 scripts, schemas, 4 references | None significant |
| `sdo-project-setup` | High -- script, 3 references | None |
| `sdo-writing-conventions` | High -- 11-section extract | None; note that ITU-specific parts were generalized |
| `sdo-writing-style` | High -- 14 core rules + checks | None |

### 3GPP layer

| Skill | Depth | Gaps |
|-------|-------|------|
| `3gpp-basics` | High -- comprehensive | Uses `@skill-name` refs (not `\`skill-name\``) |
| `3gpp-working-groups` | High -- TBIDs, hierarchy | Uses `@skill-name` refs |
| `3gpp-meetings` | High -- identifiers, scheduling | Uses `@skill-name` refs |
| `3gpp-tdocs` | High -- patterns, FTP, metadata | Uses `@skill-name` refs |
| `3gpp-releases` | High -- versioning, freeze | Uses `@skill-name` refs |
| `3gpp-specifications` | High -- TS/TR, FTP structure | Uses `@skill-name` refs |
| `3gpp-portal-auth` | High -- EOL, AJAX | Uses `@skill-name` refs |
| `3gpp-change-request` | High -- workflow, status | Has `workflow.md`; uses `@skill-name` refs |
| `3gpp-drafting` | High -- template, metadata, revision, styles | Missing: no reference from `sdo-docx-formatting` back to this skill |

### ITU-T layer

| Skill | Depth | Gaps |
|-------|-------|------|
| `itut-basics` | High -- A.1 extract | None |
| `itut-contributions` | High -- A.1 clause 3 extract | None |
| `itut-recommendations` | High -- Rules extract | None |
| `itut-drafting` | High -- template, styles, equations, batch | References missing `itut-meetings`; uses `\`body-text\`` etc. as internal refs (not skills) |

### ETSI layer

| Skill | Depth | Gaps |
|-------|-------|------|
| `etsi-basics` | High -- Guide + EDR extract | None |
| `etsi-drafting` | High -- EDR extract + style table | Missing: no .docx template asset. Style names based on 3GPP pool (likely correct but unverified). |
| `etsi-spec` | High -- metadata script | None |

---

## E. SDO-specific drafting completeness

### Template availability

| SDO | Template | Location |
|-----|----------|----------|
| 3GPP | Tdoc_Template.docx | `3gpp-drafting/assets/` |
| ITU-T | template.docx | `itut-drafting/assets/` |
| ETSI | **missing** | `etsi-drafting` has no assets/ directory |

### Metadata/property sync

| SDO | Mechanism |
|-----|-----------|
| 3GPP | `sdo-project-setup/scripts/set_docx_props.py` with default (3GPP) `--props` mapping |
| ITU-T | `sdo-project-setup/scripts/set_docx_props.py` with ITU-T `--props` mapping |
| ETSI | Not defined; needs ETSI custom property names |

### Style-name mapping coverage

All 16 abstract names from `sdo-docx-formatting` are mapped in all three
drafting skills. The ETSI mapping is identical to 3GPP for the shared pool
(confirmed by the EDR's reliance on the same style names).

---

## F. Recommendations

### Immediate (fix existing issues)

1. **[Fix] `itut-drafting`** -- remove `itut-meetings` cross-reference or create the skill
2. **[Fix] `sdo-docx-formatting`** -- add `3gpp-drafting` to cross-refs
3. **[Fix] ETSI template** -- locate or create an ETSI deliverable skeleton .docx for `etsi-drafting/assets/`

### Short-term (fill critical gaps)

4. Create `etsi-contributions` -- contribution procedures from ETSI portal/TWP
5. Create `etsi-meetings` -- meeting structure from ETSI Directives

### Medium-term (round out coverage)

6. Create `itut-meetings` -- meeting procedures from A.1
7. Update 3GPP reference skills (`@skill-name` -> `\`skill-name\``) for consistency

### Low priority (nice to have)

8. Create `3gpp-spec-retrieval` with Python script (parallel to `etsi-spec`)
9. Create `itut-spec-retrieval` with Python script
10. Create `etsi-work-items` for Work Item lifecycle detail

### Completed

- **`itut-patents`** -- created 2025-05-22 from Common Patent Policy Guidelines (2022) + ITU patents book Ch.15. Patent policy, IPR disclosure, 3 licensing options, declaration forms, database, neutrality principles.

---

## Overall assessment

**Strengths:**
- All three SDOs have complete Layer 1 (common) + Layer 3 (drafting) coverage
- Style-name mapping is consistent and complete across all drafting skills
- ITU-T has good depth despite having fewer skills than 3GPP
- The 5 common skills are high-quality with scripts, schemas, and reference files

**Weaknesses:**
- ETSI has only 3 skills vs. 9 for 3GPP and 4 for ITU-T
- 3GPP reference skills use inconsistent cross-reference format
- Cross-reference accuracy has minor issues (1 missing, 1 incomplete)
- No spec-retrieval scripts for 3GPP or ITU-T (only ETSI has one)
