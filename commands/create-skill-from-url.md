______________________________________________________________________

## name: "create-skill-from-url" description: "Generate skills from documentation websites, GitHub repositories, PDFs, or local codebases using Skill Seekers. Use when user wants to create a skill from a URL, GitHub repo, or local path. Triggers: 'create skill from URL', 'generate skill from docs', 'make skill from GitHub repo'."

# Create Skill from URL

Generate skills from documentation websites, GitHub repositories, or local paths using [Skill Seekers](https://github.com/yusufkaraaslan/Skill_Seekers).

## Workflow

1. **Parse arguments** from `$ARGUMENTS`:

   - `name`: Skill name (required)
   - `source`: URL, GitHub repo, or local path (required)
   - `output-dir`: Output directory (default: `.agents/skills/<name>`). Auto-join `name` to directory if not specified.
   - `description`: Skill description (default: "to be updated")

1. **Validate**: Return error if `name` or `source` missing. Ensure that `name` is the trailing part of the output directory. Proceed immediately if validation passes, otherwise, if in doubt, ask for user feedback on inputs.

1. **Execute**:

   ```shell
   uvx skill-seekers create <source> --name <name> --output "<output-dir>" --description "<description>"
   ```

1. **Enhance**: Apply skill-creator guidelines to improve generated skill

1. **Update description**: Modify the skill description if necessary based on enhancement results

1. **Return**: Output success message with skill details or error if creation fails

## Requirements

- [uv](https://github.com/astral-sh/uv) installed
- `GITHUB_TOKEN` for GitHub sources (optional, higher rate limits)
- `ANTHROPIC_API_KEY` for AI enhancement
