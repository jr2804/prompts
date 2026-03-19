---
name: "create-skill-from-url"
description: "Generate skills from documentation websites, GitHub repositories, or local paths using Skill Seekers. Use when user wants to create a skill from a URL, GitHub repo, or local codebase."
---

# Create Skill from URL(s)

Generate one or more skills from documentation websites, GitHub repositories, or local paths using [Skill Seekers](https://github.com/yusufkaraaslan/Skill_Seekers).

## Usage

```
/create-skill-from-url <source> [<source> ...]
```

Each argument is treated as a single source. Supported source types:

| Source Pattern | Type | Example |
|---------------|------|---------|
| `https://...` | Documentation URL | `https://docs.python.org/` |
| `owner/repo` | GitHub repository | `facebook/react` |
| `./path` or absolute path | Local directory | `./my-project` |
| `*.pdf` | PDF file | `manual.pdf` |

## Behavior

- **Single source**: Creates one skill directly
- **Multiple sources**: Creates individual skills first, then merges their content into a consolidated skill

## Options

- `--name <skill-name>` - Override the generated skill name
- `--description <desc>` - Override the skill description
- `--output <path>` - Output directory (default: `.agents/skills/`)

## Examples

```
/create-skill-from-url https://docs.python.org/

/create-skill-from-url facebook/react

/create-skill-from-url ./my-local-project

/create-skill-from-url https://docs.django.com/ https://docs.sqlalchemy.org/
```

## How It Works

1. **Single source**: Runs `uvx skill-seekers create <source>` and copies the generated skill to `.agents/skills/`
2. **Multiple sources**:
   - Creates individual skills in temporary directories
   - Merges SKILL.md content and references into one consolidated skill
   - Places the merged skill in `.agents/skills/<merged-name>/`

## Implementation

Use `$ARGUMENTS` as the source list for the skill-seekers command:

```bash
uvx skill-seekers create $ARGUMENTS
```

If multiple sources are provided, implement logic to merge the generated skills into one consolidated skill, ensuring to combine their content and references appropriately.

If no arguments are provided to the current command, return an error message prompting the user to provide at least one source.

## Requirements

- [uv](https://github.com/astral-sh/uv) must be installed
- For GitHub sources: `GITHUB_TOKEN` environment variable (optional, for higher rate limits)
- For AI enhancement: `ANTHROPIC_API_KEY` environment variable

## See Also

- [Skill Creator skill](../skill-creator/SKILL.md) - Guide for creating effective skills
- [Skill Seekers GitHub](https://github.com/yusufkaraaslan/Skill_Seekers) - Full documentation
