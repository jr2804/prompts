# Design Patterns

Catalog of visual and UX design slop patterns.

## Visual Slop

### Generic Gradient Backgrounds

❌ **Slop: Purple/pink/cyan gradients**

- 45-degree diagonal gradient from purple to pink
- Floating 3D spheres with no purpose
- Every UI element uses the same visual treatment
- Looks like a thousand other AI startup sites

✅ **Better: Intentional visual hierarchy**

- Color palette reflects brand (not trend)
- Backgrounds support content, not distract from it
- Visual weight matches information hierarchy
- Recognize specific design system (Stripe, Apple, Linear)

**Questions to ask:**

- Why this color? Can you justify it beyond "looks modern"?
- Does it contrast enough for readability?
- Does it work for colorblind users?
- Does it support or distract from content?

### Overuse of Visual Effects

❌ **Slop effects**

- Glassmorphism on every card (blurred background, frosted glass look)
- Neumorphism (inset/embossed look) everywhere
- Floating elements with parallax that serves no function
- Excessive shadow layers (shadow on shadow on shadow)
- Blur, glow, and motion just because they're available

✅ **Better: Effects with purpose**

- Glassmorphism only where layering adds clarity
- Shadows indicate hierarchy, not decoration
- Motion guides attention or confirms interaction
- Effects disabled for users who request reduced motion

### Lazy Iconography

❌ **Slop**

- Generic gradient circles as icons
- Stock UI icons unchanged from design system
- Icons that don't match visual style
- 100 icons of equal visual weight

✅ **Better: Intentional icons**

- Custom icons matching brand
- Icon size and weight reflect importance
- Icons support text, not replace it (label buttons)
- Consistent metaphors (download = arrow down, not cloud)

## Layout Slop

### Template-Driven Layouts

❌ **Slop: Content forced into templates**

```
[Hero Section - Large Image]
[Three Equal Cards]
[CTA Button]
[Three More Cards]
[FAQ Section]
[Final CTA]
```

Same structure for every page, regardless of content.

✅ **Better: Content-first layouts**

- Hierarchy determined by importance, not template
- Different sections get different treatments
- Whitespace emphasizes key content
- Layout adapts to actual content length

### Card Addiction

❌ **Slop: Everything in cards**

```
┌─────────┐  ┌─────────┐  ┌─────────┐
│ Item 1  │  │ Item 2  │  │ Item 3  │
└─────────┘  └─────────┘  └─────────┘
```

Every content type (article, person, product) gets the same card treatment.

✅ **Better: Variety based on content type**

- Articles: Text-heavy layout
- People: Avatar + key info
- Products: Large image + details
- Different types get different treatments

### Excessive Centering

❌ **Slop**

```
                    [Centered Heading]
                    [Centered Subtext]
                    [Centered Button]
                    [Centered CTA]
```

Every section centered, no visual breathing room.

✅ **Better: Strategic alignment**

- Center only hero and major CTAs
- Left-align body text (easier to read)
- Align related elements together
- Create visual groups through alignment

## Copy Slop

### Generic Marketing Language

❌ **Slop phrases**

- "Empower your business"
- "Transform your workflow"
- "The future is now"
- "Next-generation solution"
- "Innovative platform"
- "Enterprise-grade reliability"
- "Unlock your potential"

Could be any SaaS product; no specificity.

✅ **Better: Specific value propositions**

❌ "Empower your team" → ✅ "Approve 100 invoices in 5 minutes"\
❌ "Innovative scheduling" → ✅ "Automatically handle timezone conflicts"\
❌ "Enterprise-grade" → ✅ "99.99% uptime with automatic failover"\
❌ "Transform your workflow" → ✅ "Cut data entry time by 80%"

### Vague Headlines

❌ **Slop headings**

- "Welcome to Our Platform"
- "Why Choose Us?"
- "Get Started Today"
- "Introducing Our Solution"

Tell nothing about what the product does.

✅ **Better: Specific headlines**

- "Approve 100 invoices in 5 minutes with AutoPay"
- "Why Finance Teams Switch from Excel"
- "Start free, upgrade when you're ready"
- "Extract line items automatically with AI"

### Weak CTAs

❌ **Slop**

- "Get Started"
- "Sign Up"
- "Click Here"
- "Learn More"

No context about what happens next.

✅ **Better: Clear CTAs**

- "Try free for 14 days" (shows commitment)
- "See 50 invoices auto-processed" (shows value)
- "Watch 3-min demo" (shows what you'll learn)
- "Get API docs" (specific action)

## Component Patterns Slop

### Too Many Variants

❌ **Slop: Button variations**

- PrimaryButton
- SecondaryButton
- TertiaryButton
- DangerButton
- WarningButton
- SuccessButton
- GhostButton
- OutlineButton
- SolidButton
- TextButton

Which one do I use when? Confusion.

✅ **Better: Limited, intentional variants**

```
<Button variant="primary">Submit</Button>    <!-- Main action -->
<Button variant="secondary">Cancel</Button>  <!-- Alternative -->
<Button variant="danger">Delete</Button>     <!-- Destructive -->
<Button variant="ghost">Help</Button>        <!-- Lowest priority -->
```

Four variants, clear rules for each.

### Inconsistent Spacing

❌ **Slop: Random padding/margins**

```
Component 1: 16px padding
Component 2: 20px padding
Component 3: 12px padding
Section gap: 32px
Card gap: 48px
Header margin: 24px
```

No pattern or system.

✅ **Better: Spacing scale**

```
--space-1:  4px   (tight)
--space-2:  8px   (compact)
--space-3: 16px   (default)
--space-4: 24px   (breathing room)
--space-5: 32px   (section separation)
--space-6: 48px   (major sections)
```

Use only scale values. Consistent and predictable.

## Typography Slop

### Font Confusion

❌ **Slop**

- Headlines: 6 different font sizes (28px, 32px, 36px, 40px, 48px, 56px)
- Line heights all different
- 4+ font families

Looks unprofessional and hard to build.

✅ **Better: Typographic scale**

```
Display: 56px, 1.2 line-height (hero headlines)
H1:      40px, 1.3 line-height
H2:      32px, 1.4 line-height
H3:      24px, 1.5 line-height
Body:    16px, 1.6 line-height
Small:   14px, 1.6 line-height
Caption:  12px, 1.5 line-height
```

Limited scale, intentional hierarchy.

### Poor Readability

❌ **Slop**

- Light gray text on white background (< 4.5:1 contrast)
- Long paragraphs with no line breaks (100+ characters per line)
- Small text (< 14px) for body content
- No focus states on interactive elements

Excludes people, hard to read.

✅ **Better: Accessible typography**

- Minimum 4.5:1 contrast ratio (WCAG AA)
- 45-75 characters per line (optimal reading)
- Minimum 16px for body text on mobile
- Clear focus states (ring, underline, or highlight)

## Scoring Design Quality

When reviewing design, ask:

1. **Does it reflect the brand?** Or look generic?
2. **Does hierarchy serve content?** Or just decorative?
3. **Is copy specific?** Or marketing clichés?
4. **Are colors intentional?** Or trendy?
5. **Is it accessible?** Or only works for some users?

High-quality design passes all five.

## Best Practices

**Color:**

- Intentional palette (2-3 primary, 2-3 neutral)
- Sufficient contrast (4.5:1 minimum)
- Accessible to colorblind users
- Consistent across brand touchpoints

**Typography:**

- Limited scale (6-8 sizes max)
- Readable line length (45-75 characters)
- Sufficient line height (1.5-1.8)
- Clear hierarchy

**Layout:**

- Content-driven hierarchy
- Whitespace emphasizes importance
- Consistent spacing system
- Responsive breakpoints intentional

**Copy:**

- Specific over generic
- Benefit over feature
- Action-oriented CTAs
- Consistent voice and tone

**Interaction:**

- Feedback for user actions
- Focus states visible
- Loading states clear
- Error messages helpful
