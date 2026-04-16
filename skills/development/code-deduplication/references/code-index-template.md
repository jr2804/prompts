# Code Index Template

A capability index tracks what functions/classes already exist in your codebase, organized by **purpose** rather than file location. This prevents reimplementation.

## Complete Template

```markdown
# Code Index

*Last updated: [timestamp]*
*Regenerate with: `/update-code-index` command*

## Quick Reference

| Category | Count | Primary Location |
|----------|-------|------------------|
| Date/Time | 5 functions | src/utils/dates.ts |
| Validation | 8 functions | src/utils/validate.ts |
| API Clients | 12 functions | src/api/*.ts |
| Auth | 6 functions | src/auth/*.ts |
| String Operations | 4 functions | src/utils/strings.ts |
| Error Handling | 3 classes | src/utils/errors.ts |
| React Hooks | 5 hooks | src/hooks/*.ts |
| Components | 8 components | src/components/*.tsx |

---

## Date/Time Operations

| Function | Location | Does What | Parameters |
|----------|----------|-----------|------------|
| `formatDate()` | utils/dates.ts:15 | Formats Date → "Jan 15, 2024" | `(date: Date, format?: string)` |
| `formatRelative()` | utils/dates.ts:32 | Formats Date → "2 days ago" | `(date: Date)` |
| `parseDate()` | utils/dates.ts:48 | Parses string → Date | `(str: string, format?: string)` |
| `isExpired()` | auth/tokens.ts:22 | Checks if timestamp past now | `(timestamp: number)` |
| `addDays()` | utils/dates.ts:61 | Adds days to date | `(date: Date, days: number)` |

---

## Validation

| Function | Location | Does What | Parameters |
|----------|----------|-----------|------------|
| `isEmail()` | utils/validate.ts:10 | Validates email format | `(email: string)` |
| `isPhone()` | utils/validate.ts:25 | Validates phone with country | `(phone: string, country?: string)` |
| `isURL()` | utils/validate.ts:42 | Validates URL format | `(url: string)` |
| `isUUID()` | utils/validate.ts:55 | Validates UUID v4 | `(id: string)` |
| `sanitizeHTML()` | utils/sanitize.ts:12 | Strips XSS from input | `(html: string)` |
| `sanitizeSQL()` | utils/sanitize.ts:28 | Escapes SQL special chars | `(input: string)` |
| `isValidUsername()` | utils/validate.ts:70 | Checks username rules | `(username: string)` |
| `validatePassword()` | auth/validate.ts:15 | Checks password strength | `(password: string)` |

---

## String Operations

| Function | Location | Does What | Parameters |
|----------|----------|-----------|------------|
| `slugify()` | utils/strings.ts:8 | Converts to URL slug | `(str: string)` |
| `truncate()` | utils/strings.ts:20 | Truncates with ellipsis | `(str: string, len: number)` |
| `capitalize()` | utils/strings.ts:32 | Capitalizes first letter | `(str: string)` |
| `pluralize()` | utils/strings.ts:40 | Adds s/es correctly | `(word: string, count: number)` |

---

## API Clients

| Function | Location | Does What | Returns |
|----------|----------|-----------|---------|
| `fetchUser()` | api/users.ts:15 | GET /users/:id | `Promise<User>` |
| `fetchUsers()` | api/users.ts:28 | GET /users with pagination | `Promise<User[]>` |
| `createUser()` | api/users.ts:45 | POST /users | `Promise<User>` |
| `updateUser()` | api/users.ts:62 | PATCH /users/:id | `Promise<User>` |
| `deleteUser()` | api/users.ts:78 | DELETE /users/:id | `Promise<void>` |
| `fetchPosts()` | api/posts.ts:12 | GET /posts with filtering | `Promise<Post[]>` |
| `createPost()` | api/posts.ts:30 | POST /posts | `Promise<Post>` |
| `updatePost()` | api/posts.ts:45 | PATCH /posts/:id | `Promise<Post>` |
| `deletePost()` | api/posts.ts:60 | DELETE /posts/:id | `Promise<void>` |
| `fetchComments()` | api/comments.ts:10 | GET /posts/:id/comments | `Promise<Comment[]>` |
| `createComment()` | api/comments.ts:25 | POST /posts/:id/comments | `Promise<Comment>` |
| `updateComment()` | api/comments.ts:40 | PATCH /comments/:id | `Promise<Comment>` |

---

## Error Handling

| Class/Function | Location | Does What |
|----------------|----------|-----------|
| `AppError` | utils/errors.ts:5 | Base error class with code |
| `ValidationError` | utils/errors.ts:20 | Input validation failures |
| `NotFoundError` | utils/errors.ts:32 | Resource not found |
| `handleAsync()` | utils/errors.ts:45 | Wraps async route handlers |
| `errorMiddleware()` | middleware/error.ts:10 | Express error handler |

---

## React Hooks

| Hook | Location | Does What |
|------|----------|-----------|
| `useAuth()` | hooks/useAuth.ts | Auth state + login/logout |
| `useUser()` | hooks/useUser.ts | Current user data |
| `useDebounce()` | hooks/useDebounce.ts | Debounces value changes |
| `useLocalStorage()` | hooks/useLocalStorage.ts | Persisted state |
| `useFetch()` | hooks/useFetch.ts | Data fetching with loading/error |

---

## Components (React)

| Component | Location | Does What |
|-----------|----------|-----------|
| `Button` | components/Button.tsx | Styled button with variants |
| `Input` | components/Input.tsx | Form input with validation |
| `Modal` | components/Modal.tsx | Dialog overlay |
| `Toast` | components/Toast.tsx | Notification popup |
| `Spinner` | components/Spinner.tsx | Loading indicator |
| `Card` | components/Card.tsx | Content container |
| `FormField` | components/FormField.tsx | Label + input wrapper |
| `Layout` | components/Layout.tsx | Page structure |
```

______________________________________________________________________

## Guidelines

### 1. Organization

- Group by **purpose/capability**, not by file location
- Use category headers to group related functions
- Include a "Quick Reference" summary table at top
- Update timestamp when changed

### 2. Detail Level

- **Location**: File and line number for quick navigation
- **Does What**: One sentence describing the function's purpose
- **Parameters**: Function signature with types (for easy copy-paste)
- **Returns**: What the function yields (for API functions)

### 3. Maintenance

- Update immediately after adding new code
- Remove entries when code is deleted
- Merge similar functions by moving to one primary location
- Mark deprecated functions with ⚠️ status

### 4. File Header Requirement

Every file should have a header documenting what it exports:

**TypeScript:**

```typescript
/**
 * @file User authentication utilities
 * @description Handles login, logout, session management, token refresh
 *
 * Key exports:
 * - login(email, password) - Authenticates user, returns tokens
 * - logout() - Clears session and tokens
 * - refreshToken() - Gets new access token
 * - validateSession() - Checks if session is valid
 */

import { ... } from '...';
```

**Python:**

```python
"""
User authentication utilities.

Handles login, logout, session management, token refresh.

Key exports:
    - login(email, password) - Authenticates user, returns tokens
    - logout() - Clears session and tokens
    - refresh_token() - Gets new access token
    - validate_session() - Checks if session is valid
"""

from typing import ...
```

### 5. Function Documentation

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

______________________________________________________________________

## When to Update

- ✅ After creating new functions
- ✅ After merging/consolidating functions
- ✅ After deleting deprecated code
- ❌ Don't update for internal refactors (same behavior, different implementation)
