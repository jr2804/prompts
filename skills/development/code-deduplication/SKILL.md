---
name: code-deduplication
description: Pre-write workflow to prevent semantic code duplication. Use BEFORE creating new utility functions, shared modules, or helper code to verify equivalent capabilities don't already exist in the codebase. Requires maintaining CODE_INDEX.md as a capability index organized by purpose (not file location).
---

# Code Deduplication

Prevent semantic duplication and code bloat through capability indexing and pre-write checks.

## Core Philosophy

**Check before you write.** Agents tend to reimplement rather than reuse. The problem isn't duplicate code—it's duplicate purpose.

**Goal:** Know what exists before writing anything new.

## Quick Workflow

1. **Maintain CODE_INDEX.md** in project root—a capability index organized by purpose, not file location
2. **Before writing any new function**, check the index for similar capabilities
3. **After writing new code**, update the index immediately
4. **Periodically audit** for overlapping implementations

## CODE_INDEX.md Structure

Organize by **capability** (what it does), not by file location:

```markdown
# Code Index

_Last updated: [timestamp]_

## Quick Reference

| Category   | Count       | Location              |
| ---------- | ----------- | --------------------- |
| Date/Time  | 5 functions | src/utils/dates.ts    |
| Validation | 8 functions | src/utils/validate.ts |

## Date/Time Operations

| Function           | Location          | Does What                     | Params                          |
| ------------------ | ----------------- | ----------------------------- | ------------------------------- |
| `formatDate()`     | utils/dates.ts:15 | Formats Date → "Jan 15, 2024" | `(date: Date, format?: string)` |
| `formatRelative()` | utils/dates.ts:32 | Formats Date → "2 days ago"   | `(date: Date)`                  |
```

See [code-index-template.md](references/code-index-template.md) for a complete template.

## Before Creating ANY New Function

```
┌─────────────────────────────────────────┐
│ 1. DESCRIBE what you need in plain English
│ 2. CHECK CODE_INDEX.md for similar
│ 3. EVALUATE if existing works
│    ├─ Does it do what I need? → USE IT
│    ├─ Close but not quite? → EXTEND IT
│    └─ Nothing suitable? → CREATE NEW
│ 4. If extending, check for breaking changes
└─────────────────────────────────────────┘
```

## Common Duplication Patterns

### Pattern 1: Utility Function Reimplementation

❌ **Bad:** Creating `validateEmail()` when `isEmail()` exists

✅ **Good:** Check index first, use existing

### Pattern 2: Slightly Different Versions

❌ **Bad:** Multiple date formatters with slight variations scattered across files

✅ **Good:** One function with optional parameters

### Pattern 3: Inline Logic Scattered Everywhere

❌ **Bad:** Same validation logic duplicated in 5 files

✅ **Good:** Extract once, import everywhere

See [common-patterns.md](references/common-patterns.md) for detailed before/after examples.

## Maintaining the Index

### File Header Template

Every file should document what it exports:

```typescript
/**
 * @file User authentication utilities
 * @description Handles login, logout, session management, token refresh
 *
 * Key exports:
 * - login(email, password) - Authenticates user, returns tokens
 * - logout() - Clears session and tokens
 * - refreshToken() - Gets new access token
 */
```

### Function Documentation

Every function needs a one-line summary:

```typescript
/**
 * Validates email format and checks for disposable domains.
 * Returns true for valid non-disposable emails.
 */
export function isValidEmail(email: string): boolean {
  // ...
}
```

### Update Index After Writing

When you create new code:

1. Add file header documenting exports
2. Add function docstrings
3. **Immediately update CODE_INDEX.md** with new capabilities
4. Commit index update with the code

## Periodic Audits

Run `/audit-duplicates` command periodically to catch semantic overlap:

```markdown
## Duplicate Audit - [DATE]

### 🔴 High Priority (Merge These)

1. **Date formatting** - 3 similar functions found
   - formatDate() in utils/dates.ts
   - displayDate() in components/Header.tsx
   - showDate() in pages/Profile.tsx
   - **Action:** Consolidate into utils/dates.ts

### 🟡 Medium Priority (Consider Merging)

1. **User fetching** - 2 different patterns
   - fetchUser() in api/users.ts
   - getUser() in services/user.ts
   - **Action:** Decide on one pattern
```

See [audit-checklist.md](references/audit-checklist.md) for the full process.

## When Context Sensitivity Matters

Not all duplication is bad:

- **Academic writing** may need more hedging
- **Legal documents** require specific phrasing
- **Different domains** may legitimately have separate implementations

Always ask: "Does this serve a function, or is it just repeated?"
