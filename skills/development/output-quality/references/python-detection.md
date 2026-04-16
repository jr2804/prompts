# Python Detection & Cleanup Tools

Optional scripts for automated detection and cleanup of text slop patterns.

## Overview

Python scripts can help identify slop patterns in text files (markdown, documentation, etc.). These are **optional supplements** to manual review—use them for initial scanning on large documents.

- `detect_slop.py` — Analyzes text and scores slop patterns
- `clean_slop.py` — Automatically removes/replaces common patterns (preview + save modes)

## Setup

Both scripts are standalone (no external dependencies beyond Python 3.6+).

### Option 1: Place in project

```bash
cp detect_slop.py your_project/scripts/
cp clean_slop.py your_project/scripts/

# Run from project root
python scripts/detect_slop.py your_file.md --verbose
python scripts/clean_slop.py your_file.md
```

### Option 2: Run directly

```bash
python detect_slop.py path/to/file.txt
```

## Using detect_slop.py

### Basic Usage

```bash
python detect_slop.py article.md
```

**Output:**

```
Overall Slop Score: 62/100
Assessment: 🟠 Moderate to high slop (40-60 range typical for AI-generated content)

🔴 HIGH-RISK PHRASES (6 found):
  Line 1: 'delve into' in: "In this article, we will delve into..."
  Line 3: 'navigate the complexities' in: "Navigate the complexities of AI"
  ...

📢 BUZZWORDS (12 found):
  leverage (3x), innovative (2x), empower, paradigm shift, synergistic, ...

💡 RECOMMENDATIONS:
  1. Remove "In this article, we will..." preamble
  2. Replace "navigate the complexities" with specific description
  3. Remove buzzwords: "leverage" → "use", "empower" → "enable"
```

### Verbose Mode

```bash
python detect_slop.py article.md --verbose
```

Shows line-by-line analysis and pattern categories.

### Scoring

| Score | Assessment | Action |
|-------|-----------|--------|
| 0-20 | ✅ Low slop | Publish as-is |
| 20-40 | 🟡 Moderate | Minor cleanup recommended |
| 40-60 | 🟠 High | Significant revision needed |
| 60+ | 🔴 Severe | Substantial rewrite recommended |

## Using clean_slop.py

### Preview Changes (Safe)

```bash
python clean_slop.py article.md
```

Shows what would change WITHOUT modifying the file.

**Output:**

```
Analyzing: article.md

🔄 REPLACEMENTS (8 suggested):

1. Line 1: "In this article, we will delve into"
   → DELETE (preamble)

2. Line 3: "navigate the complexities of modern AI"
   → "handle the tradeoffs in AI"

3. Line 5: "leverage cutting-edge solutions"
   → "use modern solutions"

...

Preview complete. No changes made. Run with --save to apply.
```

### Apply Changes

```bash
python clean_slop.py article.md --save
```

- Creates `article.md.backup` (for safety)
- Applies suggested replacements to `article.md`
- Shows summary of changes

### Custom Output File

```bash
python clean_slop.py article.md --output cleaned_article.md
```

Saves cleaned version to new file; leaves original untouched.

### Aggressive Mode

```bash
python clean_slop.py article.md --save --aggressive
```

Applies more aggressive rewrites (may slightly change meaning). **Review carefully before accepting.**

### Options Summary

| Option | Effect |
|--------|--------|
| (none) | Preview mode—show changes without saving |
| `--save` | Apply changes, create .backup |
| `--output FILE` | Save to new file instead of overwriting |
| `--aggressive` | More aggressive replacements (may change meaning) |
| `--verbose` | Show detailed analysis |

## What Gets Detected

### High-Risk Phrases (Always remove)

- "delve into"
- "navigate the complexities"
- "in today's fast-paced world"
- "it's important to note that"
- And 20+ others (see text-patterns.md)

### Buzzwords (Replace with specifics)

- "leverage" → "use"
- "empower" → "enable"
- "innovative" → [specific improvement]
- "cutting-edge" → [specific technology]
- And 15+ others

### Meta-Commentary (Remove)

- "In this article, we will..."
- "As mentioned above..."
- "In conclusion..."
- "To summarize..."

### Excessive Hedging (Reduce)

- "may or may not" → commit to one
- "arguably" → remove qualifier
- "could potentially" → "might" or "will"
- "sort of", "kind of" → remove

## What Doesn't Get Detected

**Limitations:**

- **Context sensitivity**: Scripts can't understand domain-specific terminology that might be appropriate
- **Code slop**: These scripts are text-only; use code-patterns.md for code review
- **Design slop**: Not applicable to code; use design-patterns.md manually
- **Subtle issues**: Things like patronizing tone or overcomplicated structure require human judgment

## Recommended Workflow

1. **Scan with detect_slop.py** for overview and confidence score
2. **Review detect_slop output** for patterns you agree with
3. **Preview with clean_slop.py --verbose** before making changes
4. **Apply with clean_slop.py --save** for confirmed patterns
5. **Manual review** for context-dependent changes
6. **Verify meaning** hasn't changed in important places

## Example Session

```bash
# 1. Analyze
python detect_slop.py README.md
# Score: 68/100 (High slop)

# 2. Preview changes
python clean_slop.py README.md --verbose
# Shows 12 suggested replacements

# 3. Apply changes
python clean_slop.py README.md --save
# README.md.backup created, changes applied

# 4. Verify
# Open README.md, review changes
# Check that meaning is preserved

# 5. Re-scan
python detect_slop.py README.md
# Score: 22/100 (Much better!)
```

## Integration with CI/CD

Optional: Add slop detection to your build pipeline:

```yaml
# .github/workflows/quality-check.yml
- name: Check for slop
  run: |
    python scripts/detect_slop.py docs/*.md --verbose
    # Fail if score > 50
    score=$(python scripts/detect_slop.py docs/*.md | grep "Score:")
    if [ "$score" -gt 50 ]; then
      exit 1
    fi
```

Or as a pre-commit hook:

```bash
#!/bin/bash
# .git/hooks/pre-commit
python scripts/detect_slop.py README.md --threshold 30 || exit 1
```

## Important Notes

- **Always review before accepting automated changes** — machines can't understand context
- **Keep originals** — clean_slop.py creates backups, but verify they're safe
- **These are suggestions, not law** — Use judgment about what to accept
- **For important docs**, manual review is essential
- **Pattern detection isn't perfect** — False positives/negatives are possible

## Advanced: Creating Custom Patterns

If you want to add domain-specific slop detection:

1. Add patterns to the script (see source)
2. Run with `--custom-patterns` option
3. Or modify the script directly for your use case

(Detailed customization instructions available in script source code.)

______________________________________________________________________

**Bottom line**: Use these scripts as a first-pass filter for obvious patterns. Don't rely on them for final judgment.
