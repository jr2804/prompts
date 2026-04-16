# Code Audit Checklist

Periodic audits catch semantic duplication and related issues that static analysis misses.

## Pre-Audit Checklist

- [ ] Backup current CODE_INDEX.md
- [ ] Ensure all recent code is committed
- [ ] Have list of files/directories to audit
- [ ] Schedule 1-2 hours for thorough review

## Audit Categories

### Utility Functions

- [ ] Any functions doing similar things? (date formatting, validation, string ops)
- [ ] Multiple ways to fetch same data?
- [ ] Scattered inline validation logic?
- [ ] Repeated error handling patterns?
- [ ] Generic variable names in multiple files? (`data`, `result`, `temp`, `item`)

### Components (React/Vue/etc.)

- [ ] Similar UI components that could merge?
- [ ] Multiple implementations of buttons, cards, modals?
- [ ] Components with almost-identical logic?
- [ ] Prop patterns that could be unified?

### Hooks (React)

- [ ] Custom hooks with overlapping logic?
- [ ] Multiple similar data-fetching hooks?
- [ ] Repeated state management patterns?

### API Clients

- [ ] Multiple API client implementations?
- [ ] Inconsistent error handling across endpoints?
- [ ] Similar request/response transformation logic?

### Classes/Types

- [ ] Similar class hierarchies?
- [ ] Interfaces with overlapping properties?
- [ ] Repeated initialization patterns?

## Audit Output Format

Document findings in a structured report:

```markdown
## Code Duplication Audit - [DATE]

**Scope**: [e.g., "src/ and tests/"]
**Auditor**: [name or agent]
**Result**: [X duplication issues found]

### 🔴 High Priority (Merge These Immediately)

1. **Date formatting** - 3 similar functions found
   - `formatDate()` in utils/dates.ts
   - `displayDate()` in components/Header.tsx
   - `showDate()` in pages/Profile.tsx
   - **Effort**: 30 min merge + refactor
   - **Action**: Consolidate into utils/dates.ts with options
   - **Status**: Pending

2. **Email validation** - Inline logic in 5 files
   - signup.ts:42
   - profile.ts:28
   - invite.ts:15
   - settings.ts:67
   - admin.ts:33
   - **Effort**: 20 min extraction
   - **Action**: Extract to utils/validate.ts::isValidEmail()
   - **Status**: Pending

### 🟡 Medium Priority (Consider Merging)

1. **User fetching** - 2 different patterns
   - `fetchUser()` in api/users.ts (Promise-based)
   - `getUser()` in services/user.ts (async/await wrapper)
   - **Effort**: 15 min unification
   - **Action**: Keep one pattern, deprecate other
   - **Status**: Review owner

2. **Button components** - 3 variants
   - `PrimaryButton` in components/buttons/Primary.tsx
   - `SecondaryButton` in components/buttons/Secondary.tsx
   - `DangerButton` in components/buttons/Danger.tsx
   - **Note**: May be intentional for different use cases
   - **Action**: Verify intent with component owner
   - **Status**: Review needed

### 🟢 Low Priority (Monitor)

1. **Error classes** - 2 custom error types
   - `AppError` in utils/errors.ts
   - `ValidationError` in utils/errors.ts (subclass of AppError)
   - **Note**: Proper inheritance hierarchy
   - **Action**: No change needed

2. **Test utilities** - Similar test helpers
   - `setupUser()` in tests/setup/user.ts
   - `createMockUser()` in tests/mocks/user.ts
   - **Note**: Different purposes (setup vs. mocking)
   - **Action**: Document difference in comments

---

### Summary

| Priority | Count | Effort | Merged? |
|----------|-------|--------|---------|
| 🔴 High | 2 | ~50 min | ⏳ Pending |
| 🟡 Medium | 2 | ~30 min | 🔍 Review |
| 🟢 Low | 2 | None | ✅ OK |

**Next Steps**:
1. Merge high-priority duplications
2. Review medium-priority with team
3. Update CODE_INDEX.md after merges
4. Schedule follow-up audit in 2 weeks
```

## Implementation Process

### Step 1: Run Audit

For each category in the audit checklist:

```bash
# Example: Find similar functions by name pattern
grep -r "function format" src/
grep -r "function validate" src/
grep -r "function fetch" src/

# Look for duplicated patterns
grep -r "const \[.*loading.*\] = useState" src/
grep -r "useEffect(() => {" src/hooks/
```

### Step 2: Document Findings

Create audit report with:

- Exact file locations and line numbers
- Code snippets showing the duplication
- Estimated effort to fix
- Recommended action (merge, extend, keep separate)
- Justification if keeping duplicate

### Step 3: Prioritize

High priority (do immediately):

- Performance impacts (redundant API calls)
- Security issues (inconsistent validation)
- Maintenance burden (scattered logic)

Medium priority (schedule soon):

- Code readability improvements
- Reduced test burden
- Simplified mental model

Low priority (monitor):

- Intentional variants for different use cases
- Code that's unlikely to change
- Areas with clear ownership and docs

### Step 4: Merge/Refactor

For each item being merged:

1. Create branch: `refactor/merge-{function-name}`
2. Consolidate implementations
3. Update all imports
4. Run existing tests to verify behavior
5. Update CODE_INDEX.md
6. Create minimal PR with clear commit message
7. Merge after review

### Step 5: Re-audit

After 2-4 weeks, run audit again to:

- Verify merges stayed merged (no new duplicates)
- Catch new duplication patterns early
- Track team's deduplication discipline

## Red Flags

⚠️ **Warning signs during audit:**

- [ ] Same validation logic in 3+ places
- [ ] Multiple HTTP client implementations
- [ ] More than 2 ways to format dates/times
- [ ] Duplicate error handling in many functions
- [ ] Similar components with different names
- [ ] Repeated state management patterns
- [ ] Multiple implementations of the same algorithm

These indicate weak modularity. Refactor soon.

## Tools & Commands

### Automated Search

```bash
# Find similar function names
grep -r "^export function \|^export const" src/ | awk -F: '{print $NF}' | sort

# Find duplicated imports
grep -r "^import " src/ | grep -i "validate\|format\|fetch" | sort | uniq -d

# Find copy-pasted code (approximate)
# Look for identical multi-line patterns
find src -name "*.ts" -o -name "*.js" | xargs wc -l | sort -n | tail -20
```

### Semi-Automated Detection

For larger codebases, use tools like:

- **AST analyzers** (tree-sitter, babel) for code pattern detection
- **Similarity tools** (git log --all -S "pattern") for finding similar code
- **Metrics tools** (complexity, duplication scores)

But manual review remains essential to understand intent.

## Maintenance Schedule

| Codebase Size | Audit Frequency | Scope |
|---------------|-----------------|-------|
| < 50 files | Monthly | Manual review of recent changes |
| 50-200 files | Bi-weekly | Focused areas + full index sync |
| 200+ files | Weekly | Automated detection + manual validation |
| 500+ files | Continuous | Git hooks + pre-commit checks |

______________________________________________________________________

## Questions to Ask

For each potential duplication, ask:

1. **Same purpose?** Or serving different use cases?
2. **Same behavior?** Or subtle differences?
3. **Same constraints?** Or different performance/security needs?
4. **Intentional variants?** Or accidental duplication?
5. **Cost to merge?** Vs. cost to maintain separately?

If answer to all is "yes to merge," consolidate immediately.
