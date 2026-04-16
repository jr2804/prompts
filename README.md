# prompts (and more)

Prompts, instructions, skills, templates, etc. for AI-based coding assistants. Can be used as a source for [saddle-cli](https://saddle.sh/).

## Install

Use `mise` to install the repository. If you don't have `mise` installed, you can install it with:

```bash
curl -fsSL https://mise.sh/install | sh
```

...or on Windows:

```powershell
iwr -useb https://mise.sh/install | iex
```

Run `bunx saddle-cli`, then follow the instructions to install the repository.

## Content

### Commands

TODO

### Skills

TODO

### Agents

TODO

## Useful MCP Servers & CLI tools

A list of MCP servers and CLI tools with similar functionality that are useful for testing and development:

- [CytoScnPy](https://github.com/djinn-soul/CytoScnPy)
- [Debug Skill + CLI](https://github.com/AlmogBaku/debug-skill)
- [grepai](https://github.com/yoanbernabeu/grepai)
- [beads issue tracker](https://github.com/steveyegge/beads)
- [SkillKit](https://github.com/rohitg00/skillkit)
- [Skillz](https://github.com/intellectronica/skillz)
- [AutoSkills](https://github.com/midudev/autoskills)
- *To be continued...*

Related tools:

- [any-cli-mcp-server](https://github.com/eirikb/any-cli-mcp-server)
- [OpenCLI](https://github.com/jackwener/opencli)
- *To be continued...*

## Skills & Agents

### Collections

- [Awesome Claude Skills](https://github.com/BehiSecc/awesome-claude-skills)
- [Awesome Copilot](https://github.com/github/awesome-copilot)
- [Claude Code Ultimate Guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/tree/main/examples/skills)
- *To be continued...*

### Indivial skills and agents

- [caveman](https://github.com/JuliusBrussee/caveman) - Token saving skill for code generation.
- [markdown-viewer](https://github.com/markdown-viewer/skills)

## Upcoming skills/ideas

### Quality & Discipline Skills Family

Organized as a modular family addressing complementary concerns:

**1. output-quality** — Detect and eliminate generic, low-quality patterns in prose, code, and design
*Consolidates*: [deslopify](https://github.com/glaforge/deslopify), [cc-polymath anti-slop](https://github.com/rand/cc-polymath/tree/main/skills/anti-slop)
*Includes*: Text/design anti-slop patterns, code style smells, optional Python detection/cleanup scripts
*Agent-agnostic*: Works across Claude, Qwen, Gemini, Cursor, etc.

**2. coding-discipline** — Behavioral protocol for writing better code first time
*Source*: [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) on LLM coding pitfalls
*Covers*: Surface assumptions, simplicity-first, surgical changes, goal-driven execution
*Integration*: Full EXAMPLES.md as first-class references in SKILL.md
*Agent-neutral*: Discipline principles apply to all code-writing agents

**3. code-deduplication** — Pre-write capability index and check-before-write workflow
*Source*: [claude-bootstrap](https://github.com/alinaqi/claude-bootstrap/tree/main/skills/code-deduplication)
*Includes*: CODE_INDEX.md template, audit utilities, duplicate detection heuristics
*Use with*: coding-discipline for comprehensive implementation rigor

**Rationale:** These three skills address different problem classes (output quality, execution discipline, codebase hygiene) and work best as linked companions rather than one monolithic skill. Each can be invoked independently or in combination.

## References

[Writing a Good AGENTS.md](https://www.philschmid.de/writing-good-agents#the-data-says-less-is-more)
[Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?](https://arxiv.org/pdf/2602.11988)
