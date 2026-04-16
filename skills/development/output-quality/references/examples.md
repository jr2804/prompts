# Output Quality Examples

Before/after examples demonstrating quality improvements across text, code, and design domains.

## Text Examples

### Example 1: Generic Article Opening

**Before (Score: 78/100 — High Slop)**

```
In today's fast-paced world, artificial intelligence has become increasingly important.
Many organizations are looking to leverage cutting-edge AI technologies to empower their
teams and unlock new opportunities. In this article, we will delve into the complexities
of modern AI systems and explore how businesses can navigate these challenges effectively.
```

**Issues:**

- "In today's fast-paced world" — generic, delete
- "leverage", "empower", "unlock" — buzzwords
- "In this article, we will delve" — meta-commentary throat-clearing
- "navigate the complexities" — vague hand-waving
- Multiple clichés in 4 sentences

**After (Score: 15/100 — Clean)**

```
Companies deploying AI face three concrete problems: managing model costs, handling failures
gracefully, and explaining decisions to users. This article examines practical solutions from
five companies that process millions of predictions daily.
```

**Changes:**

- Lead with specific problems (not generic importance)
- Replace buzzwords with concrete actions
- Skip meta-commentary
- Promise specific examples (five companies)

______________________________________________________________________

### Example 2: Documentation Slop

**Before (Score: 82/100)**

```
## Overview

Our API is a powerful and flexible platform that empowers developers to build innovative
applications. It provides a robust set of endpoints that enable you to manage your data
effectively.

### Getting Started

To get started, you'll want to create an account and generate an API key. It's important
to note that API keys should be kept secure at all times.
```

**Issues:**

- "powerful", "flexible", "innovative", "robust" — buzzwords
- "empowers developers" — condescending
- "you'll want to" — wishy-washy
- "it's important to note" — patronizing

**After (Score: 10/100)**

```
## Overview

The API manages your invoices, payments, and reconciliation. Start with the /invoices endpoint
to list or create invoices.

### Getting Started

1. Create an account at api.example.com/signup
2. Generate an API key: Settings → API Keys → Create
3. Keep your key secret—it grants full access to your account
```

**Changes:**

- Specific about what it does
- Action-first structure
- No hedging or buzzwords
- Clear security requirement

______________________________________________________________________

## Code Examples

### Example 1: Generic Data Handler

**Before: Overengineered (80/100 slop)**

```python
class DataProcessor:
    """Processes and transforms data."""

    def __init__(self):
        self.data = None

    def process(self, input_data):
        """Process the input data."""
        self.data = self._validate_and_transform(input_data)
        return self._finalize()

    def _validate_and_transform(self, data):
        """Internal validation and transformation."""
        result = []
        for item in data:
            # Process item
            processed = self._process_item(item)
            result.append(processed)
        return result

    def _process_item(self, item):
        """Process individual item."""
        return item * 2  # Apply transformation

    def _finalize(self):
        """Finalize processing."""
        return self.data

# Usage:
processor = DataProcessor()
result = processor.process([1, 2, 3])
```

**Issues:**

- Multiple abstraction layers (why?)
- Comments restate code
- "data", "item", "result" — generic names
- Single responsibility violated

**After: Simple (10/100 slop)**

```python
def double_values(numbers):
    """Return each value doubled."""
    return [x * 2 for x in numbers]

# Usage:
result = double_values([1, 2, 3])
```

**Changes:**

- Direct implementation
- Clear naming (function and variables)
- No unnecessary classes
- Comments removed (code is self-explanatory)

______________________________________________________________________

### Example 2: Validation Mess

**Before: Scattered (85/100)**

```python
# validate_email.py
def validate_email(email):
    return '@' in email and '.' in email

# forms/user.py
def validate_user_form(data):
    if not data.get('email'):
        raise ValueError('Email required')
    if '@' not in data['email'] or '.' not in data['email']:
        raise ValueError('Invalid email')
    return True

# api/users.py
def create_user(email):
    if not email or '@' not in email:
        return {"error": "Invalid email"}
    # ...

# profile/settings.py
if '@' in user_email and '.' in user_email:
    # Update email
```

**Issues:**

- Same validation logic in 4 places
- Inconsistent error handling
- Multiple implementations

**After: Single source (15/100)**

```python
# utils/validate.py
def is_valid_email(email: str) -> bool:
    """Validate email format. Requires @ and domain."""
    return email and '@' in email and '.' in email.split('@')[1]

# Update CODE_INDEX.md:
# | isValidEmail() | utils/validate.py:5 | Validates email format | (email: str) |

# All callers:
from utils.validate import is_valid_email

# forms/user.py
if not is_valid_email(data.get('email')):
    raise ValueError('Invalid email')

# api/users.py
if not is_valid_email(email):
    return {"error": "Invalid email"}

# profile/settings.py
if is_valid_email(user_email):
    update_email(user_email)
```

**Changes:**

- Single validation function
- Updated CODE_INDEX.md so no one reimplements
- Consistent across codebase

______________________________________________________________________

## Design Examples

### Example 1: Generic Landing Page

**Before (Slop indicators)**

```
Hero: Purple-to-pink gradient background
      Centered "Empower Your Business" headline
      Generic floating 3D spheres

Section 2: Three equal white cards
          "Innovative Solutions", "Enterprise-Grade", "Next-Generation"
          No real differentiation

Section 3: FAQ (5 generic questions)

Footer: Five blue buttons (Sign Up, Learn More, Documentation, Contact, Blog)
```

**Issues:**

- Cookie-cutter layout
- Generic purple/pink gradient
- Floating elements serve no purpose
- Buzzwords, no specifics
- Too many buttons

**After (Quality indicators)**

```
Hero: Brand-color background (e.g., dark blue)
      Specific headline: "Auto-Process 100 Invoices in 5 Minutes"
      Screenshot of actual product (not generic)
      Clear CTA: "Try free for 14 days"

Section 2: Three benefits with different layouts
          - "Approval Workflow" with workflow diagram
          - "API Integration" with code example
          - "Real-time Sync" with status indicator
          Each highlights actual value

Section 3: Three customer results
          "Accounting Team processes 3x faster"
          "Reduced errors from 2% to 0.1%"
          "Cut month-end reconciliation from 3 days to 1 day"

Footer: Single CTA button "Start your free trial"
        Plus: Documentation, Status, Blog links (secondary)
```

**Changes:**

- Specific value proposition
- Real product screenshots vs. generic graphics
- Benefit-focused copy
- Variety in layout and content type
- Single clear primary action

______________________________________________________________________

### Example 2: Component Visual Regression

**Before: Inconsistent**

```
Button variants: 8 different styles
  - PrimaryButton (blue, rounded, 12px padding)
  - SecondaryButton (gray, rounded, 12px padding)
  - DangerButton (red, sharp corners, 16px padding)
  - OutlineButton (white, blue border, 12px padding)
  - TextButton (no background, 4px padding)
  - IconButton (circular, 8px)
  - LinkButton (looks like text)
  - GhostButton (barely visible)

Which one do I use for the main action?
Which for a destructive action?
No clear pattern.
```

**After: Clear hierarchy**

```
Primary: Blue, rounded, 16px padding
  → Main action on every page
  → "Save", "Create", "Submit"

Secondary: Gray, rounded, 16px padding
  → Alternative action
  → "Cancel", "Skip", "Maybe Later"

Danger: Red, rounded, 16px padding
  → Destructive action requiring confirmation
  → "Delete", "Remove", "Close Account"

Ghost: White/transparent, blue text, 12px padding
  → Lowest priority
  → "Help", "Feedback", "Settings"

Rules:
- Every page has exactly one Primary button
- Danger only used for destructive actions
- Ghost for optional/secondary actions
```

**Changes:**

- Limited to 4 clear variants
- Each variant has clear use case
- Visual hierarchy matches importance
- Easier to design, build, and understand

______________________________________________________________________

## The Common Thread

Whether text, code, or design—quality comes from:

1. **Specificity** over generality
2. **Purpose** over appearance
3. **Consistency** over variety
4. **Clarity** over cleverness
5. **Utility** over trends

Generic AI outputs fail on all five. Quality requires intention.
