---
agent: agent
---
Please analyze the coding guidelines given in `AGENTS.md` and its referenced sub-documents. Then get familiar with the code structure of this project, including:

- if available, use MCP server `memorygraph` for long-term storage of important information and knowledge across projects. Use `recall_memories` from `memorygraph` before any task. Query by project, tech, or task type.
- if available, use the `bd` tool and MCP server `beads-mcp` for issue tracking and improved memory that can be used manually by human operators as well as automated by coding agents. Use `bd ready` to get a list of open issues.
- if available, use the MCP server `chunkhound` index, search and research on source code, documentation and other markdown files. 
- if available, use MCP server `ncp` to discover and get suggestions for available tools.

Based on the memory information, select the most obvious issue to fix and plan the implementation task accordingly. In doubt, ask the user on how to proceed.