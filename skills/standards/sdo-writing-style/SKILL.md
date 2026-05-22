---
name: sdo-writing-style
description: General writing principles for formal standardization documents across SDOs (3GPP, ETSI, ITU-T). Use when drafting or revising prose content for standards contributions, technical reports, or meeting documents. Covers specificity, fact discipline, anti-genericity, register, structure, and revision checks. Does NOT cover .docx formatting -- see sdo-docx-formatting for style rules.
---

# SDO Writing Style

Apply these prose-quality rules to the **textual content** of standards
documents. For .docx formatting (styles, headings, tables, figures), see
`sdo-docx-formatting`.

## Purpose

Write for the actual context. The goal is prose that fits the medium, the
task, and the reader. Standards documents must be precise, verifiable, and
concrete -- vague generalities undermine technical credibility.

## Precedence

When rules conflict:

1. Truth, safety, accessibility, and platform/legal requirements
2. Explicit user instructions
3. Genre and medium norms (standards documents are formal technical writing)
4. Core rules below
5. Optional heuristics

## Core workflow

1. Identify the medium, audience, reader need, and job of the text.
2. If task-oriented, identify the answer or next action that belongs first.
3. If long-form, decide the through-line and one concrete example, moment,
   or case that can carry real weight.
4. Draft to fit that context, not an abstract idea of "good writing."
5. Cut what sounds generic, ceremonial, over-engineered, or too cleanly
   modular.

## Safety rails

- Do not invent typos. Do not break grammar on purpose. Do not inject
  slang, profanity, fake uncertainty, or staged messiness.
- Do not make text less usable or accessible in the name of style.
- The recurring problem is **regularity and mismatch**, not any one feature.
- In standards documents, prefer straight ASCII quotes and apostrophes.
  Avoid curly quotes, smart apostrophes, and single-character ellipses.

---

## Core rules

Rules grouped by concern for incremental application:
- **Content Integrity** (1, 3, 4): anchor to context, be specific, verify facts
- **Style & Voice** (5, 6, 7, 8): plain words, coherent reference, no performance, calibrated stance
- **Structure** (2, 9, 11, 12, 13): fit format, show before generalizing, develop thought, choose shape, avoid catalog prose
- **Revision** (10, 14): watch regularity, re-read and cut

### 1. Anchor to the actual context before drafting

Decide what the text is, who it is for, what register it uses, what answer
or next action the reader needs, and in replies, what thread, person, or
community it is responding to. A contribution that could be pasted into any
meeting on the same topic will read generic even if the prose is clean.

### 2. Fit the format to the medium

Standards documents are formal technical writing. Structure is expected:
headings, lists, tables, equations. Over-structuring a casual discussion
note makes it feel templated; under-structuring a technical contribution
makes it harder to evaluate.

### 3. Prefer concrete specificity over polished generality

Each paragraph of three or more sentences (excluding transitional paragraphs)
should carry at least one concrete anchor:

**What counts:**
- A proper noun the reader could look up (spec name, organization)
- A specific number that is not only a date or version
- A direct quote from a referenced specification
- A named decision, measurement, or test condition
- A checkable detail

**What does not count:**
- `many`, `various`, `several`, `a lot of`
- `in ways that mattered`, `meaningful changes`, `broad implications`
- `the standard approach`, `the usual pattern`, `as is often the case`
- Vague intensifiers: `essentially`, `fundamentally`, `ultimately`

### 4. Specificity must be earned

When writing about real entities, specifications, measurements, or
procedures, prefer fewer verified facts to many guessed ones.

- Do not use specificity theater: invented milestone names, suspiciously
  exact claims, synthetic quotes, or decorative factuality.
- Be especially careful with hidden-mechanism claims: internal logic,
  unseen motives, back-end behavior.
- Do not launder analysis through vague authority. Avoid `experts say`,
  `research suggests`, or `critics argue` unless you can name the source.
- Treat exact quotes, close paraphrases, public metrics, future claims,
  and causal claims as high-fragility facts.
- If you cannot verify a claim, attribute it, soften it, or cut it.

### 5. Use plain words. Allow ordinary repetition. Prefer verbs.

Do not chase synonyms for basic words like `problem`, `change`, `system`,
`work`, or `test`. Repeat the ordinary word when it is the right word.
Prefer `we changed it` to `the implementation of the change`, `latency
dropped` to `a reduction in latency was observed`.

### 6. Cohere through reference, not label spam

Use pronouns and continued reference when the reader can easily track them.
Do not restate the full frame in every paragraph. Treat signpost openers
like `Furthermore`, `Moreover`, `Additionally`, `Importantly`, and
`Notably` as things to justify, not default sentence starters.

### 7. Do not perform

Avoid keynote cadence, mission-statement phrasing, applause-line endings,
and ceremonial wrap-ups. Start where the answer starts. Stop where the
answer stops.

### 8. Calibrate confidence, stance, and voice to genre

Standards documents aim at neutrality and precision. Do not inject first
person or attitude just to make the text feel human. A recommendation is
appropriate when: (a) the document's purpose is to propose or evaluate a
technical choice, (b) evidence supports a specific conclusion, or (c) the
contributing body has asked for a position. In those cases, state the
recommendation clearly with supporting evidence. Otherwise, remain neutral --
do not manufacture a view where none is required.

### 9. Show concrete things before generalizing

Usually the order should be:

1. what was done or observed
2. where the pattern appeared
3. what constraint mattered
4. what failed or changed
5. what that seems to mean

### 10. Watch regularity

Watch for repeated use of the same moves:
- Parallel enumeration and reflexive three-part cadence inside sentences
- Multiple sentences doing hidden list work even without bullets
- Concession-plus-positive rhythm (`not X, but Y`; `may sound X, but Y`)
- Identical paragraph arcs
- One neat claim sentence at the top of every paragraph followed by
  orderly elaboration
- The same punctuation move in every paragraph

### 11. Let the thought develop

Longer pieces should not feel pre-solved. If the prose moves in a perfectly
efficient straight line from claim to conclusion, it can feel rushed. A
concrete example usually does this better than an artificial aside.

### 12. Choose structure consciously

For task pages, procedures, reference docs: the predictable structure is
often the clearest one. For contributions, white papers, technical reports:
choose a through-line instead -- one complaint that stopped mattering, one
constraint that shaped the design, one mismatch between promise and reality.

### 13. Do not turn a piece into catalog prose or system-tour prose

If a paragraph is mainly names, milestones, categories, or spec labels, it
is probably catalog prose. If each paragraph can be summarized with a single
label (`background`, `mechanism`, `impact`), the piece is system-tour prose.

Pick one change and trace its consequence. Cross-wire the piece so
paragraphs depend on each other instead of sitting like labeled boxes.

### 14. Revise by reading and cutting

Re-read as a first-time reader. Cut anything that is auditioning. Cut
sentences whose only job is to announce the next sentence. Collapse
paragraphs that restate each other. Most edits should make the text shorter.

---

## Required checks

For short pieces (up to ~150 words), run checks 1-5, 7, and 10. For longer
pieces, run all checks.

1. **Register fit.** Does the format and level of structure match a formal
   standards document?
2. **Concrete-anchor audit.** For each substantial paragraph, point to one
   concrete anchor.
3. **Fact discipline.** Pick the three most fragile factual claims. If you
   cannot vouch for them, attribute them, soften them, or cut them.
4. **Source-fit check.** Check every exact quote, close paraphrase, public
   metric, planned/future event, and causal claim. Do not keep `X caused Y`
   unless the source supports the relationship.
5. **Regularity tripwire.** Name the single most repeated visible pattern.
   If the same move appears 3+ times, rewrite at least one occurrence.
6. **Repeated-frame check.** If a central metaphor, contrast, or wording
   family appears throughout the piece, decide whether it is a useful
   motif or a too-neat scaffold.
7. **Stance and voice.** Standards documents aim at neutrality: did you
   keep it neutral? If a view is called for, is it backed by evidence?
8. **Developed thought.** For any piece >4 paragraphs, identify one place
   where the prose pauses, doubles back, or notices a concrete detail off
   the main line.
9. **Shape and spine.** State the organizing principle and controlling
   claim. If the shape is `starting state -> changes -> verdict`, or
   paragraphs map one-to-one with named topics, restructure.
10. **Over-correction.** Did you add fake-human moves -- typos, slang,
    forced asides -- just to break a pattern?

These are tripwires, not goals. Use them to catch genericity, visible
regularity, and modular structure, not to manufacture variation.

---

## Useful corrections

| Problem | Better |
|---------|--------|
| Generic -> specific | `The change had broad implications.` -> `The change reduced idle noise by 6 dB in the worst-case configuration.` |
| Puffery -> observable | `The method is robust and efficient.` -> `The method converged for all 47 test conditions within 100 iterations.` |
| Catalog prose -> argument | `First came method A, then method B, then method C.` -> `Methods A and B both failed above 8 kHz; only method C maintained performance across the full band.` |
| Vague attribution | `Research suggests this approach works well.` -> `TS 26.131 defines the requirement as -64 dBm0 for send direction idle noise.` |
| Causal overreach | `The codec drove the noise floor higher.` -> `After encoding, the noise floor increased by 3 dB relative to the PCM input.` |

---

## Cross-references

- `sdo-writing-conventions` -- mechanical writing rules (spelling, hyphens, numbers, capitalization, abbreviations, non-discriminatory language)
- `sdo-docx-formatting` -- .docx style rules, table/figure formatting
- `sdo-docx-operations` -- officecli guardrails for implementing edits
- Per-SDO drafting skills (`3gpp-drafting`, `etsi-drafting`, `itut-drafting`)
