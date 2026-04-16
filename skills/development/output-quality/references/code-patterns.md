# Code Patterns

Catalog of code slop patterns to identify and eliminate.

## Variable Naming Slop

### Generic Names That Hide Intent

| Generic | Better | Example |
|---------|--------|---------|
| `data` | What data? | `userData`, `transactionHistory`, `searchResults` |
| `result` | What's the result? | `parsedDocument`, `filteredItems`, `validationError` |
| `temp` | Why temporary? | `validatedEmail`, `trimmedInput`, `normalizedPath` |
| `item` | Item of what? | `cartItem`, `menuOption`, `processedRecord` |
| `obj` | Object of what? | `userProfile`, `configObject`, `responseData` |
| `val` | What value? | `userAge`, `discountPercentage`, `timeoutMs` |
| `x`, `y`, `z` | Only acceptable in math | Use meaningful names everywhere else |
| `arr`, `list` | Array of what? | `userNames`, `activeConnections`, `sortedScores` |
| `fn`, `func`, `f` | What does it do? | `calculateTotal`, `validateEmail`, `formatDate` |
| `tmp1`, `tmp2` | Why multiple temps? | Rethink the algorithm |

### Bad Function Names

| Generic | Better | Why |
|---------|--------|-----|
| `handleData()` | What are you handling? | `processUserInput()`, `parseCSVData()`, `validateFormFields()` |
| `processItems()` | What processing? | `filterInactiveUsers()`, `calculateTotalCost()`, `sortByDate()` |
| `manageUsers()` | What management action? | `activateUser()`, `reassignTeam()`, `sendReminder()` |
| `doSomething()` | Way too vague | Any specific action |
| `fix()` | Fix what? | `retryFailedRequest()`, `sanitizeHTMLInput()` |
| `check()` | Check what? | `validateEmail()`, `isUserActive()`, `hasPermission()` |
| `update()` | Update what? | `refreshUserCache()`, `recalculateTotals()`, `syncDatabase()` |
| `make()` | Make what? | `createUser()`, `generateToken()`, `buildQueryString()` |

## Comment Slop

### Obvious Comments

Comments that restate the code should be deleted:

❌ **Bad: Restates code**

```python
# Create a user
user = User()

# Check if email is valid
if '@' in email:

# Loop through items
for item in items:
    # Add item to list
    result.append(item)
```

✅ **Good: Omitted or explains why**

```python
user = User()

if '@' in email:  # Basic validation; more thorough checks in validate_email()

result = [item for item in items]  # List comprehension is equivalent
```

### Comments That Confuse

❌ **Vague or outdated comments**

```python
def calculate_score(data):
    # Magic number 0.5 for weighting
    return data * 0.5

# TODO: fix this later
# HACK: probably works
# This is weird but necessary (why?)
```

✅ **Clear, explanatory comments**

```python
def calculate_score(data):
    # Weight by 50% to normalize against historical max of 200
    NORMALIZED_WEIGHT = 0.5
    return data * NORMALIZED_WEIGHT

# Known limitation: doesn't handle timezone offsets yet (bug #345)
# Workaround for Node.js quirk where Promise.all({...}) fails on objects
```

## Structural Slop

### Over-Engineering

❌ **Unnecessary abstraction layers**

```python
class DataProcessor:
    def process(self, data):
        return self._internal_process(data)

    def _internal_process(self, data):
        return self._actual_process(data)

    def _actual_process(self, data):
        return [x * 2 for x in data]
```

✅ **Direct, simple implementation**

```python
def process_data(data):
    return [x * 2 for x in data]
```

### Design Patterns Without Purpose

❌ **Using patterns before they're needed**

```python
# Singleton pattern for a class used only once
class Logger(metaclass=Singleton):
    pass

# Observer pattern for a single event type
class EventEmitter:
    def __init__(self):
        self.observers = {}
    # 50 lines of boilerplate
```

✅ **Simple approach until complexity is needed**

```python
logger = Logger()

def on_event(callback):
    callbacks.append(callback)

def emit(event):
    for cb in callbacks:
        cb(event)
```

## Implementation Slop

### Complex Solution to Simple Problem

❌ **Overengineered email validation**

```python
import re
from typing import Pattern

EMAIL_REGEX: Pattern = re.compile(
    r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
)

def validate_email(email: str) -> bool:
    """Validate email using RFC 5322 standard."""
    if not email:
        return False
    if len(email) > 254:
        return False
    return EMAIL_REGEX.match(email) is not None
```

✅ **Simple, sufficient approach**

```python
def is_valid_email(email: str) -> bool:
    return email and '@' in email
```

### Premature Optimization

❌ **Over-optimized for theoretical scalability**

```python
from functools import lru_cache
import asyncio
from multiprocessing import Pool

@lru_cache(maxsize=10000)
async def fetch_user_async(user_id):
    with Pool(4) as p:
        return p.apply_async(fetch_from_db, (user_id,)).get()
```

✅ **Simple solution, optimize later if needed**

```python
def get_user(user_id):
    return db.query(User).filter_by(id=user_id).first()
```

## Testing Slop

### No Tests or Insufficient Tests

❌ **No verification**

```python
def calculate_discount(price, percent):
    return price * (1 - percent / 100)  # Hope this is right?
```

✅ **With test verification**

```python
def calculate_discount(price, percent):
    """Calculate price after discount. Percent is 0-100."""
    return price * (1 - percent / 100)

def test_discount():
    assert calculate_discount(100, 10) == 90
    assert calculate_discount(100, 0) == 100
    assert calculate_discount(100, 100) == 0
```

### Tests That Don't Test

❌ **Ineffective tests**

```python
def test_user_creation():
    user = create_user("john@example.com")
    assert user is not None  # Too weak; always passes
```

✅ **Effective tests**

```python
def test_user_creation():
    user = create_user("john@example.com", "password123")
    assert user.email == "john@example.com"
    assert user.password != "password123"  # Verify it's hashed
    assert user.created_at is not None
```

## Documentation Slop

### Missing Documentation

❌ **No context for public API**

```python
def process(x, y, z):
    return x + (y * z)
```

✅ **Clear documentation**

```python
def calculate_total_cost(base_price, quantity, tax_rate):
    """Calculate cost including tax.

    Args:
        base_price: Price per unit in cents
        quantity: Number of units
        tax_rate: Tax as decimal (e.g., 0.08 for 8%)

    Returns:
        Total cost in cents

    Example:
        calculate_total_cost(1000, 5, 0.08) == 5400  # $54
    """
    return base_price * quantity * (1 + tax_rate)
```

### Outdated Documentation

⚠️ **Comments that don't match code**

```python
# This function returns the user's age
def get_user_info(user_id):
    user = db.get(user_id)
    return {"name": user.name, "email": user.email}  # Wait, no age?
```

## Scoring Code Quality

When reviewing code, ask:

1. **Is every name clear?** Or do names need explanation?
2. **Are variables reused too many times?** Or is scope too broad?
3. **Is there unnecessary nesting?** Or deep indentation levels (>3)?
4. **Are tests present and meaningful?** Or missing/weak?
5. **Would a junior engineer understand this?** Or only the author?

High-quality code passes all five.

## Best Practices

**Names:**

- Variable names describe content, not type
- Function names describe action + object
- Class names describe responsibility
- File names match main export

**Comments:**

- Explain WHY, not WHAT (code shows what)
- Document non-obvious decisions
- Update when code changes
- Delete outdated comments

**Structure:**

- Keep functions under 50 lines
- Keep classes under 200 lines
- Single responsibility per function
- Avoid deep nesting (max 3 levels)

**Testing:**

- Test behavior, not implementation
- Include edge cases and error conditions
- Test is documentation
