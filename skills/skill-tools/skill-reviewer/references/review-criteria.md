# Review Criteria

Detailed evaluation checklist for skill quality assessment.

## Frontmatter Validation

### Required Fields

| Field | Rules |
|-------|-------|
| `name` | 1-64 chars, lowercase alphanumeric + hyphens only, no leading/trailing/consecutive hyphens, must match parent directory name |
| `description` | 1-1024 chars, no angle brackets (`<` or `>`), describes what AND when to use |

### Optional Fields (verify if present)

- `license`: string, keep short
- `compatibility`: 1-500 chars, system requirements
- `metadata`: key-value map, unique key names
- `allowed-tools`: space-separated string

### Name Format

Valid: `skill-name`, `pdf-processing`, `code-review-2`
Invalid: `PDF-Processing` (uppercase), `-pdf` (leading hyphen), `pdf--processing` (consecutive hyphens)

## Description Quality

### Good Description Checklist

- [ ] **Imperative phrasing**: "Use when..." not "This skill does..."
- [ ] **User intent focus**: Describes what user is trying to achieve
- [ ] **Specific keywords**: Includes domain terms that trigger relevance matching
- [ ] **When-to-use scenarios**: Explicit contexts where skill applies
- [ ] **Even-if mention**: Covers cases where user doesn't name domain explicitly

### Example Transformations

**Poor:**

```yaml
description: Helps with PDFs.
```

**Good:**

```yaml
description: >
  Extract text and tables from PDF files, fill PDF forms, and merge
  multiple PDFs. Use when working with PDF documents or when the user
  mentions PDFs, forms, or document extraction.
```

## Body Structure

### Length Guidelines

- **\<100 lines**: Ideal — concise, context-efficient
- **100-300 lines**: Acceptable — most content in SKILL.md
- **300-500 lines**: Consider splitting — use references/ for details
- **>500 lines**: Problematic — move detailed content to references/

### Progressive Disclosure

SKILL.md should contain:

1. Core workflow / main instructions
2. Essential patterns and examples
3. Key references with clear "see [file] for details" links

Reference files should contain:

- Detailed API documentation
- Extended examples
- Edge case handling
- Large reference tables

### Agent-Agnostic Language

**Prohibited:**

- "Claude", "Claude Code", "Claude.ai"
- "Gemini CLI", "Gemini"
- "Qwen", "Cursor", "Copilot"

**Permitted:**

- "agents", "LLMs", "AI assistants"
- "when you write code", "when processing documents"
- "the agent", "the model"

### Section Requirements

A well-structured skill typically includes:

1. **Overview** — 1-2 sentences on purpose
2. **Core Workflow** — Sequential steps or decision tree
3. **When to Use** — Explicit triggering scenarios
4. **Examples** — Input/output pairs (if applicable)

## Resource Organization

### scripts/

**Use when:**

- Deterministic reliability needed
- Code repeatedly rewritten
- Token efficiency important

**Contents:**

- Python/Bash scripts for automation
- Data processing utilities
- Format conversion tools

**Example:**

```
scripts/
├── extract_text.py    # PDF text extraction
└── validate_pdf.py    # PDF validation
```

### references/

**Use when:**

- Detailed documentation needed
- Claude should load on demand
- Too lengthy for SKILL.md

**Contents:**

- API references
- Workflow guides
- Domain-specific docs
- Schemas and formats

**Example:**

```
references/
├── api-reference.md    # Complete API docs
├── forms.md           # Form handling guide
└── patterns.md        # Common patterns
```

### assets/

**Use when:**

- Files used in output (not documentation)
- Templates to copy
- Images, icons, fonts

**Example:**

```
assets/
├── template.pptx       # PowerPoint template
└── logo.png           # Brand logo
```

## Validation Commands

### skills-ref validate

```bash
uvx skills-ref validate ./path/to/skill
```

Checks:

- Frontmatter YAML syntax
- Required fields present
- Name format valid
- Description length
- File structure

### quick_review.py

```bash
uv run scripts/quick_review.py ./path/to/skill
```

Lightweight validation without external dependencies.
