---
agent: agent
---
Please analyze the coding guidelines given in `AGENTS.md` and its referenced sub-documents - use the `mgrep` MCP server to parse documentation/markdown files, if available. Then get familiar with the code structure of this project, including:

- use MCP server `ncp` to discover and get suggestions for available tools.
- the use of the MCP server `memorygraph` for long-term storage of important information and knowledge across projects. 
- the use of the `bd` tool that is intended to be used by coding agents for issue tracking and improved memory.


Then perform the following steps to get the next implementation task:

- use `recall_memories` from `memorygraph` before any task. Query by project, tech, or task type.
- use `bd ready` to get a list of open issues.
- based on the memory information, select the most obvious issue to fix and plan the task accordingly. In doubt, ask the user on how to proceed.