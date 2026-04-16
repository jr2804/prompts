# Text Patterns

Catalog of natural language slop patterns to identify and eliminate.

## High-Risk Phrases (Remove Immediately)

These phrases are almost always unnecessary and should be deleted or replaced:

| Phrase | Why It's Slop | Replacement | Example |
|--------|--------------|-------------|---------|
| "delve into" | Pretentious filler | "examine", "explore", or delete | ❌ We will delve into the complexities → ✅ We examine practical approaches |
| "navigate the complexities" | Vague hand-waving | "handle", "address", or delete | ❌ Navigate the complexities of modern AI → ✅ Handle the tradeoffs in production AI |
| "in today's fast-paced world" | Generic excuse for urgency | Delete entirely | ❌ In today's fast-paced world, agility matters → ✅ Agility matters. |
| "it's important to note that" | Condescending filler | Delete and state fact directly | ❌ It's important to note that costs matter → ✅ Costs matter. |
| "cutting-edge" | Buzzword without specifics | Name what's actually new | ❌ Our cutting-edge solution → ✅ Our tensor-optimized search |
| "paradigm shift" | Grandiose overstatement | "change", "improvement", be specific | ❌ A paradigm shift in debugging → ✅ Faster debugging using binary search |
| "leverage" | Corporate jargon | "use", "exploit", "apply" | ❌ Leverage our platform → ✅ Use our API |
| "synergistic" | Meaningless buzzword | Delete or describe actual collaboration | ❌ Synergistic partnership → ✅ We coordinate on scheduling |
| "ecosystem" | Overused for any collection | Name what it actually is | ❌ Our ecosystem of tools → ✅ Our three integrated tools |
| "seamless" | Vague positive claim | Describe actual experience | ❌ Seamless integration → ✅ One-click setup, no manual config |
| "empower" | Generic, condescending | Describe actual benefit | ❌ Empower your users → ✅ Let users control their permissions |

## Excessive Buzzwords

Common corporate jargon that signals low-effort writing:

**Replace with concrete terms:**

- "leverage" → "use", "apply", "exploit"
- "synergistic" → (describe the actual relationship)
- "holistic" → "complete", "integrated", or be specific
- "disruptive" → "faster", "cheaper", "more reliable"
- "innovative" → describe what's actually new
- "best-in-class" → cite specific metrics
- "robust" → name what failure modes it handles
- "scalable" → "handles X users" or "scales to Y"
- "dynamic" → "adjusts to conditions" or "changes in real-time"
- "next-generation" → describe what's actually improved

## Meta-Commentary

Phrases that talk ABOUT the text instead of delivering content:

| Pattern | Why It's Slop | Example Fix |
|---------|--------------|------------|
| "In this article, we will discuss..." | Wastes opening, states the obvious | Lead with the actual content |
| "As mentioned above..." | Forces reader to scroll back | Use forward references or restructure |
| "The rest of this document..." | Breaks immersion | Delete meta joiners, let document flow naturally |
| "In conclusion..." | Signals you've finished | Just finish; readers know when they reach the end |
| "To summarize..." | Same as above | State the summary; don't announce it |
| "It goes without saying..." | Then don't say it | Delete this line |

## Excessive Hedging

Qualified language that undermines confidence:

| Pattern | Why It's Slop | Fix |
|---------|--------------|-----|
| "may or may not" | Cowardly non-statement | Commit to one: "likely" or "unlikely" |
| "could potentially" | Same vagueness | Use "might" or "will" depending on likelihood |
| "arguably" | Signals you lack conviction | State your position without qualifying |
| "in some sense" | Filler that admits confusion | Clarify what you actually mean |
| "sort of", "kind of", "somewhat" | Wishy-washy | Use precise language |
| "it seems" | Defer to reader's judgment unnecessarily | Say what you observe |
| "one could argue" | Passive-voice hedging | State your argument directly |

## Redundant Qualifiers

Words that repeat information already implied:

| Redundant | More Direct | Example |
|-----------|------------|---------|
| "very unique" | "unique" | Unique things are already distinct; "very" adds nothing |
| "literally true" | "true" | "Literally" is already implied for factual claims |
| "surprising discovery" | "discovery" | Discoveries are surprising by definition |
| "basic fundamentals" | "fundamentals" | Fundamentals are basic by definition |
| "end result" | "result" | The result is by definition at the end |
| "rarely ever" | "rarely" | "Ever" adds nothing |

## Structural Tics

Overused sentence patterns that signal formulaic writing:

### Em-dash addiction

**Problem:** Using em-dashes to create dramatic pauses

❌ We considered three options—performance, cost, reliability. Each matters—deeply.

✅ We weighed three tradeoffs: performance, cost, reliability. Each matters.

### Rhetorical questions

**Problem:** Using questions as a lazy way to engage readers

❌ What makes a good algorithm? Speed, obviously. Correctness? Even more obvious.

✅ Good algorithms prioritize speed and correctness.

### "It's not X, it's Y" construction

**Problem:** Binary contrasts that pretend nuance doesn't exist

❌ This isn't about innovation—it's about reliability.

✅ We prioritize reliability over novelty.

### Tricolon (three-part lists) abuse

**Problem:** Forcing everything into triplets for rhythm

❌ We build fast, efficient, and scalable systems.

✅ We build fast, efficient systems. [Or: Our systems are fast, efficient, and handle scale.]

### Bold-first bullets

**Problem:** Overemphasizing the label

❌ **Performance**: We measure latency. **Reliability**: Our uptime is 99.99%. **Cost**: We charge per use.

✅ Latency: We measure below 100ms. Uptime: 99.99%. Pricing: Pay per use.

## Tone Issues

### Patronizing analogies

"Think of it as..." often signals you're about to oversimplify:

❌ Think of the database as a library, where tables are shelves.

✅ The database organizes data into tables (similar to spreadsheet sheets).

### Grandiose stakes inflation

Overstating consequences:

❌ This could revolutionize how humans communicate forever.

✅ This reduces latency from 5s to 500ms for most queries.

### Filler intensifiers

Words that add emotional heat but no information:

- "literally" (unless you mean it technically)
- "really", "very", "extremely", "incredibly"
- "basically" (if it's basic, show it)
- "actually" (only use if contradicting prior statement)
- "honestly" (if you're being dishonest elsewhere?)

## Writing Better

### Be Direct

- **Cut preambles**: "In order to understand X, you must first..." → Just start explaining X.
- **Skip meta-commentary**: Don't say what you're about to do; just do it.
- **Lead with point**: Put the main idea first, then details.

### Be Specific

- **Replace vague nouns**: "items", "things", "stuff" → name what they are
- **Use concrete examples**: Instead of "we handle edge cases", show one
- **Name specific improvements**: Instead of "faster", say "3x faster on 1MB files"

### Be Authentic

- **Vary rhythm**: Mix short and long sentences. Start some with verbs, some with nouns.
- **Use active voice**: Prefer "We built this" over "This was built".
- **Match context**: Formal docs need different tone than tutorials.

## Scoring Text

When unsure if text has slop, ask:

1. **Would a 5-year-old understand this?** If not, simplify or explain.
2. **Does every word earn its place?** If not, cut it.
3. **Could I say this in half the words?** If yes, try.
4. **Do I sound like myself?** Or like a template?
5. **Does this make me smarter?** Or does it waste my time?

High-quality text passes all five.
