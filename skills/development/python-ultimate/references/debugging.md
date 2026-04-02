# Systematic Debugging Reference

## Table of Contents

1. [Iron Law](#iron-law)
2. [4-Phase Process](#4-phase-process)
   - [Phase 1: Root Cause Analysis](#phase-1-root-cause-analysis)
   - [Phase 2: Pattern Analysis](#phase-2-pattern-analysis)
   - [Phase 3: Hypothesis Formation](#phase-3-hypothesis-formation)
   - [Phase 4: Implementation](#phase-4-implementation)
3. [Red Flags](#red-flags)
4. [Common Rationalizations to Avoid](#common-rationalizations-to-avoid)
5. [Debugging Tools and Techniques](#debugging-tools-and-techniques)
6. [When to Stop and Reassess](#when-to-stop-and-reassess)

______________________________________________________________________

## Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

**Violating the letter of this process is violating the spirit of debugging.**

If you haven't completed Phase 1, you cannot propose fixes.

______________________________________________________________________

## 4-Phase Process

Complete each phase before proceeding to the next.

### Phase 1: Root Cause Analysis

**Before attempting ANY fix:**

1. **Read Error Messages Carefully**

   - Don't skip past errors or warnings
   - Read stack traces completely
   - Note line numbers, file paths, error codes

2. **Reproduce Consistently**

   - Can you trigger it reliably?
   - What are the exact steps?
   - Does it happen every time?
   - If not reproducible → gather more data, don't guess

3. **Check Recent Changes**

   - What changed that could cause this?
   - Git diff, recent commits
   - New dependencies, config changes

4. **Trace Data Flow** (for errors deep in call stack)

   - Where does bad value originate?
   - What called this with bad value?
   - Trace up until you find the source
   - Fix at source, not at symptom

5. **Gather Evidence in Multi-Component Systems**
   For each component boundary:

   - Log what data enters component
   - Log what data exits component
   - Verify environment/config propagation
   - Check state at each layer

### Phase 2: Pattern Analysis

1. **Find Working Examples**

   - Locate similar working code in same codebase
   - What works that's similar to what's broken?

2. **Compare Against References**

   - If implementing a pattern, read reference implementation COMPLETELY
   - Don't skim - read every line

3. **Identify Differences**

   - What's different between working and broken?
   - List every difference, however small
   - Don't assume "that can't matter"

4. **Understand Dependencies**

   - What other components does this need?
   - What settings, config, environment?

### Phase 3: Hypothesis Formation

**Apply the scientific method:**

1. **Form Single Hypothesis**

   - State clearly: "I think X is the root cause because Y"
   - Write it down
   - Be specific, not vague

2. **Test Minimally**

   - Make the SMALLEST possible change to test hypothesis
   - One variable at a time
   - Don't fix multiple things at once

3. **Verify Before Continuing**

   - Did it work? Yes → Phase 4
   - Didn't work? Form NEW hypothesis
   - DON'T add more fixes on top

### Phase 4: Implementation

1. **Create Failing Test Case First**

   - Simplest possible reproduction
   - Automated test if possible
   - MUST exist before fixing

2. **Implement Single Fix**

   - Address the root cause identified
   - ONE change at a time
   - No "while I'm here" improvements

3. **Verify Fix**

   - Test passes now?
   - No other tests broken?
   - Issue actually resolved?

______________________________________________________________________

## Red Flags

**STOP and return to Phase 1 if you catch yourself thinking:**

- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- Proposing solutions before tracing data flow
- **"One more fix attempt" (when already tried 2+)**
- **Each fix reveals new problem in different place**

______________________________________________________________________

## Common Rationalizations to Avoid

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from start |
| "I'll write test after confirming fix works" | Untested fixes don't stick. Test first proves it |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs |
| "Reference too long, I'll adapt the pattern" | Partial understanding guarantees bugs |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem |

______________________________________________________________________

## Debugging Tools and Techniques

1. **Instrumentation at Boundaries**

   - Log data entering and exiting each component
   - Verify environment/config propagation
   - Check state at each layer

2. **Backward Tracing**

   - Start from where error manifests
   - Trace data flow backward to origin
   - Fix at source, not symptom

3. **Minimal Test Cases**

   - Isolate the smallest possible reproduction
   - One variable at a time

4. **Compare Against Working State**

   - Git diff between known good state
   - Compare configurations
   - Check environmental differences

______________________________________________________________________

## When to Stop and Reassess

**If 3+ fixes failed, question the architecture:**

Signs of architectural problems:

- Each fix reveals new shared state/coupling/problem in different place
- Fixes require "massive refactoring" to implement
- Each fix creates new symptoms elsewhere

**STOP and question fundamentals:**

- Is this pattern fundamentally sound?
- Should we refactor architecture vs. continue fixing symptoms?
- Discuss with your human partner before attempting more fixes

**When process reveals "no root cause":**
If systematic investigation reveals issue is truly environmental, timing-dependent, or external:

1. Document what you investigated
2. Implement appropriate handling (retry, timeout, error message)
3. Add monitoring/logging for future investigation

**Remember:** 95% of "no root cause" cases are incomplete investigation.
