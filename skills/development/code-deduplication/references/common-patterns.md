# Common Duplication Patterns

Real-world examples of code duplication and how to fix them.

## Pattern 1: Utility Function Reimplementation

**The Problem:** Agent creates `validateEmail()` when `isEmail()` already exists in the codebase.

### ❌ Bad: Reimplementation

```typescript
// Already exists in utils/validate.ts:10
export function isEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// But then you create this anyway:
function validateEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
```

### ✅ Good: Check and reuse

```typescript
// Before writing validateEmail, check CODE_INDEX.md
// Found: isEmail() in utils/validate.ts

import { isEmail } from '@/utils/validate';

if (isEmail(userInput)) {
  // Valid email, continue
}
```

______________________________________________________________________

## Pattern 2: Slightly Different Versions

**The Problem:** Multiple date formatters with slight variations scattered across files.

### ❌ Bad: Scattered implementations

```typescript
// In file A - components/Header.tsx
function formatDate(d: Date) {
  return d.toLocaleDateString();
}

// In file B - pages/Profile.tsx
function displayDate(d: Date) {
  return d.toLocaleDateString('en-US');
}

// In file C - components/DatePicker.tsx
function showDate(d: Date) {
  return d.toLocaleDateString('en-US', { month: 'short' });
}
```

### ✅ Good: One function with options

```typescript
// utils/dates.ts - Single source of truth
export function formatDate(
  d: Date,
  options?: { locale?: string; format?: 'short' | 'long' }
) {
  const locale = options?.locale ?? 'en-US';
  const formatOpts = options?.format === 'short'
    ? { month: 'short', day: 'numeric' }
    : { month: 'long', day: 'numeric', year: 'numeric' };

  return d.toLocaleDateString(locale, formatOpts);
}

// Usage everywhere
import { formatDate } from '@/utils/dates';

formatDate(date)  // Full format
formatDate(date, { format: 'short' })  // Short format
formatDate(date, { locale: 'fr-FR' })  // French locale
```

______________________________________________________________________

## Pattern 3: Inline Logic Scattered Everywhere

**The Problem:** Same validation logic duplicated across files.

### ❌ Bad: Duplicated logic

```typescript
// In signup.ts
if (!email || !email.includes('@') || email.length < 5) {
  throw new Error('Invalid email');
}

// In profile.ts
if (!email || !email.includes('@') || email.length < 5) {
  throw new Error('Invalid email');
}

// In invite.ts
if (!email || !email.includes('@') || email.length < 5) {
  throw new Error('Invalid email');
}

// In settings.ts
if (!email || !email.includes('@') || email.length < 5) {
  throw new Error('Invalid email');
}
```

### ✅ Good: Extract once, import everywhere

```typescript
// utils/validate.ts - Single source
export const isValidEmail = (email: string) =>
  email && email.includes('@') && email.length >= 5;

// signup.ts
import { isValidEmail } from '@/utils/validate';
if (!isValidEmail(email)) {
  throw new Error('Invalid email');
}

// profile.ts
import { isValidEmail } from '@/utils/validate';
if (!isValidEmail(email)) {
  throw new Error('Invalid email');
}

// ... same import in invite.ts, settings.ts, etc.
```

______________________________________________________________________

## Pattern 4: Similar Component Implementations

**The Problem:** Multiple button components doing essentially the same thing.

### ❌ Bad: Multiple button components

```typescript
// components/PrimaryButton.tsx
export function PrimaryButton({ children, onClick }) {
  return (
    <button
      onClick={onClick}
      style={{ background: 'blue', color: 'white', padding: '8px 16px' }}
    >
      {children}
    </button>
  );
}

// components/SecondaryButton.tsx
export function SecondaryButton({ children, onClick }) {
  return (
    <button
      onClick={onClick}
      style={{ background: 'gray', color: 'black', padding: '8px 16px' }}
    >
      {children}
    </button>
  );
}

// components/DangerButton.tsx
export function DangerButton({ children, onClick }) {
  return (
    <button
      onClick={onClick}
      style={{ background: 'red', color: 'white', padding: '8px 16px' }}
    >
      {children}
    </button>
  );
}
```

### ✅ Good: One component with variant prop

```typescript
// components/Button.tsx
interface ButtonProps {
  children: React.ReactNode;
  onClick: () => void;
  variant?: 'primary' | 'secondary' | 'danger';
}

export function Button({ children, onClick, variant = 'primary' }: ButtonProps) {
  const styles = {
    primary: { background: 'blue', color: 'white' },
    secondary: { background: 'gray', color: 'black' },
    danger: { background: 'red', color: 'white' },
  };

  return (
    <button
      onClick={onClick}
      style={{ padding: '8px 16px', ...styles[variant] }}
    >
      {children}
    </button>
  );
}

// Usage
<Button variant="primary">Save</Button>
<Button variant="secondary">Cancel</Button>
<Button variant="danger">Delete</Button>
```

______________________________________________________________________

## Pattern 5: Duplicate Error Handling

**The Problem:** Same try/catch pattern repeated across many functions.

### ❌ Bad: Duplicated error handling

```typescript
// api/users.ts
export async function fetchUser(id: string) {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error('Failed to fetch user:', error);
    throw error;
  }
}

// api/posts.ts
export async function fetchPosts() {
  try {
    const response = await fetch('/api/posts');
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error('Failed to fetch posts:', error);
    throw error;
  }
}
```

### ✅ Good: Extract error handling helper

```typescript
// utils/api.ts
async function fetchJson(url: string) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return await response.json();
}

// api/users.ts
export async function fetchUser(id: string) {
  try {
    return await fetchJson(`/api/users/${id}`);
  } catch (error) {
    console.error('Failed to fetch user:', error);
    throw error;
  }
}

// api/posts.ts
export async function fetchPosts() {
  try {
    return await fetchJson('/api/posts');
  } catch (error) {
    console.error('Failed to fetch posts:', error);
    throw error;
  }
}
```

______________________________________________________________________

## Pattern 6: Duplicate Hook Logic

**The Problem:** Multiple hooks doing similar data fetching.

### ❌ Bad: Similar hooks

```typescript
// hooks/useUser.ts
export function useUser(id: string) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetchUser(id)
      .then(data => { setUser(data); setError(null); })
      .catch(err => setError(err))
      .finally(() => setLoading(false));
  }, [id]);

  return { user, loading, error };
}

// hooks/usePosts.ts
export function usePosts(userId: string) {
  const [posts, setPosts] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetchPosts(userId)
      .then(data => { setPosts(data); setError(null); })
      .catch(err => setError(err))
      .finally(() => setLoading(false));
  }, [userId]);

  return { posts, loading, error };
}
```

### ✅ Good: Generic fetch hook

```typescript
// hooks/useFetch.ts
export function useFetch<T>(fn: (...args: any[]) => Promise<T>, ...args: any[]) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    setLoading(true);
    fn(...args)
      .then(data => { setData(data); setError(null); })
      .catch(err => setError(err))
      .finally(() => setLoading(false));
  }, args);

  return { data, loading, error };
}

// hooks/useUser.ts
export function useUser(id: string) {
  return useFetch(fetchUser, id);
}

// hooks/usePosts.ts
export function usePosts(userId: string) {
  return useFetch(fetchPosts, userId);
}
```

______________________________________________________________________

## The Decision Tree

```
Need new functionality
        │
        ▼
Check CODE_INDEX.md for similar
        │
    ┌───┴──────────────────┐
    │                      │
Found exact match      Found similar
    │                      │
    ▼                      ▼
USE IT              Can it be extended?
                        │
                    ┌───┴──────┐
                    │          │
                  Yes         No
                    │          │
                    ▼          ▼
                Extend it   Create new
              (add params)  (update index)
                    │          │
                    └───┬──────┘
                        │
                Nothing found
                        │
                        ▼
                    Create new
                  (update index)
```

______________________________________________________________________

## Prevention Strategy

**Before writing any new code:**

1. **Describe** what you need in plain English
2. **Check CODE_INDEX.md** for similar capabilities
3. **Search** the codebase for similar patterns
4. **Decide**: Use, extend, or create new?
5. **Update index** if you create something new

**After writing new code:**

1. Update CODE_INDEX.md immediately
2. Add file headers documenting exports
3. Add function docstrings
4. Commit the index update with your code
