# Code Review Reception

## Table of Contents

1. [Workflow](#workflow)
2. [No Performative Agreement](#no-performative-agreement)
3. [Push Back with Technical Reasoning](#push-back-with-technical-reasoning)
4. [Evaluating Feedback Quality](#evaluating-feedback-quality)
5. [When to Implement vs When to Push Back](#when-to-implement-vs-when-to-push-back)
6. [Responding to Unclear Feedback](#responding-to-unclear-feedback)

______________________________________________________________________

## Workflow

```
READ → UNDERSTAND → VERIFY → EVALUATE → RESPOND → IMPLEMENT
```

1. **READ** – Complete feedback without reacting
2. **UNDERSTAND** – Restate requirement in own words (or ask)
3. **VERIFY** – Check against codebase reality
4. **EVALUATE** – Technically sound for THIS codebase?
5. **RESPOND** – Technical acknowledgment or reasoned pushback
6. **IMPLEMENT** – One item at a time, test each

**Implementation order for multi-item feedback:**

- Blocking issues (breaks, security)
- Simple fixes (typos, imports)
- Complex fixes (refactoring, logic)

______________________________________________________________________

## No Performative Agreement

**NEVER:**

- "You're absolutely right!"
- "Great point!" / "Excellent feedback!"
- "Thanks for catching that!"
- Any gratitude expression

**INSTEAD:**

- Restate the technical requirement
- Ask clarifying questions
- Push back with technical reasoning if wrong
- Just start working (actions > words)

**Why:** Actions speak. Just fix it. The code itself shows you heard the feedback.

______________________________________________________________________

## Push Back with Technical Reasoning

Push back when:

- Suggestion breaks existing functionality
- Reviewer lacks full context
- Violates YAGNI (unused feature)
- Technically incorrect for this stack
- Legacy/compatibility reasons exist
- Conflicts with architectural decisions

**How to push back:**

- Use technical reasoning, not defensiveness
- Ask specific questions
- Reference working tests/code
- Escalate to decision-maker if architectural

**Signal if uncomfortable pushing back:** "Strange things are afoot at the Circle K"

______________________________________________________________________

## Evaluating Feedback Quality

Before implementing external feedback:

1. Technically correct for THIS codebase?
2. Breaks existing functionality?
3. Reason for current implementation?
4. Works on all platforms/versions?
5. Does reviewer understand full context?

**YAGNI Check:**

```
IF reviewer suggests unused feature:
  grep codebase for actual usage
  IF unused: "This endpoint isn't called. Remove it (YAGNI)?"
```

______________________________________________________________________

## When to Implement vs When to Push Back

| Situation | Action |
|-----------|--------|
| Feedback is correct | State fix briefly, implement |
| Suggestion breaks things | Push back with evidence |
| Unused feature requested | Push back with YAGNI |
| Conflicts with architecture | Escalate to decision-maker |
| Can't verify suggestion | State limitation, ask for direction |

**Acknowledging correct feedback:**

```
✅ "Fixed. [Brief description]"
✅ "Good catch - [specific issue]. Fixed in [location]."
✅ [Just fix it and show the code]
```

**If you were wrong:**

```
✅ "You were right - I checked [X] and it does [Y]. Implementing now."
✅ "Verified, you're correct. My initial understanding was wrong because [reason]. Fixing."
```

______________________________________________________________________

## Responding to Unclear Feedback

```
IF any item is unclear:
  STOP – do not implement anything yet
  ASK for clarification on unclear items
```

**Why:** Items may be related. Partial understanding = wrong implementation.

**Example:**

```
Partner: "Fix items 1-6"
You understand 1,2,3,6. Unclear on 4,5.

❌ WRONG: Implement 1,2,3,6 now, ask about 4,5 later
✅ RIGHT: "I understand items 1,2,3,6. Need clarification on 4 and 5 before proceeding."
```

**When can't verify:**

```
"I can't verify this without [X]. Should I [investigate/ask/proceed]?"
```

______________________________________________________________________

## GitHub Thread Replies

Reply in the comment thread (`gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies`), not as a top-level PR comment.

______________________________________________________________________

## The Bottom Line

**External feedback = suggestions to evaluate, not orders to follow.**

Verify. Question. Then implement.

No performative agreement. Technical rigor always.
