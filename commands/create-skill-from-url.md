---
name: "create-skill-from-url"
description: "Generate skills from documentation websites, GitHub repositories, or local paths using Skill Seekers. Use when user wants to create a skill from a URL, GitHub repo, or local codebase. Usage: /create-skill-from-url name=<name> source=<source> output-dir=<output-dir> description="<description>"
---

# Create Skill from any source (URL, PDF, Word Docx, HTML, etc.)

Generate one or more skills from documentation websites, GitHub repositories, or local file paths using [Skill Seekers](https://github.com/yusufkaraaslan/Skill_Seekers).

## Usage

1) Parse the command arguments to extract the skill `name`, `source`, `output-dir`, and `description`: `$ARGUMENTS`
2) If `name` is not provided or cannot be determined, return an error message prompting the user to provide a skill name.
3) If `source` is not provided or cannot be determined, return an error message prompting the user to provide at least one source (URL, GitHub repo, or local path).
4) If `description` is not provided or cannot be determined, use a dummy placeholder (e.g.,  "to be updated"). The description will be generated and  updated based on the generated skill main text, considering also the `skill-creator` skill.
5) Create a new skill named `name` in the output directory `output-dir` (if `output-dir` is an empty string, use `.agents/skills/name`) using the provided source `source` as follows:

```shell
uvx skill-seekers create <source> --name <name> --output "<output-dir>" --description "<description>"
```

Use the skill `skill-creator` to enhance the generated skill and possible attachments (scripts, references, etc.).


## Requirements

- [uv](https://github.com/astral-sh/uv) must be installed
- For GitHub sources: `GITHUB_TOKEN` environment variable (optional, for higher rate limits)
- For AI enhancement: `ANTHROPIC_API_KEY` environment variable

## See Also

- [Skill Creator skill](../skill-creator/SKILL.md) - Guide for creating effective skills
- [Skill Seekers GitHub](https://github.com/yusufkaraaslan/Skill_Seekers) - Full documentation
