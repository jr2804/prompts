---
name: agentic-coding
description: Skill family for agent-assisted software development workflows. Includes workspace isolation (git-worktrees), parallel debugging (dispatching-parallel-agents), structured multi-task development (subagent-driven-development), and lightweight code review (requesting-code-review). Install individual skills based on workflow needs.
license: MIT
---

# Agentic Coding

A modular skill family for agent-assisted software development workflows. Each skill addresses a distinct phase or pattern—install only what you need.

## Skill Family Members

| Skill                           | Purpose             | When to Use                                                 |
| ------------------------------- | ------------------- | ----------------------------------------------------------- |
| **using-git-worktrees**         | Workspace isolation | Starting feature work that needs clean branch environment   |
| **dispatching-parallel-agents** | Parallel debugging  | 2+ completely independent failures across different domains |
| **subagent-driven-development** | Structured workflow | Multi-task implementation with integrated two-stage review  |
| **requesting-code-review**      | Standalone review   | Ad-hoc reviews outside structured workflows                 |

## Common Patterns

### Full Feature Development

```
using-git-worktrees → subagent-driven-development
     ↓                        ↓
Create isolated          Execute plan with
feature branch           per-task subagents
                         + integrated review
```

### Parallel Bug Investigation

```
dispatching-parallel-agents
     ↓
Multiple subagents
investigate unrelated
failures simultaneously
```

### Quick Post-Task Review

```
requesting-code-review
     ↓
Lightweight review
after single task
or before merge
```

## Installation

Install individual skills based on your workflow:

```bash
# Need workspace isolation?
saddle-cli install agentic-coding/using-git-worktrees

# Need parallel debugging?
saddle-cli install agentic-coding/dispatching-parallel-agents

# Need structured development workflow?
saddle-cli install agentic-coding/subagent-driven-development

# Need standalone code review?
saddle-cli install agentic-coding/requesting-code-review
```

## Relationship to Other Skills

- **coding-discipline**: Apply behavioral discipline within any agentic workflow
- **python-ultimate**: Technical standards for Python implementation
- **output-quality**: Review final output for anti-patterns

## Decision Flowchart

```dot
digraph which_skill {
    "Starting feature work?" [shape=diamond];
    "Need clean workspace?" [shape=diamond];
    "using-git-worktrees" [shape=box];
    "Multiple failures?" [shape=diamond];
    "Independent domains?" [shape=diamond];
    "dispatching-parallel-agents" [shape=box];
    "Single failure path" [shape=box];
    "Have implementation plan?" [shape=diamond];
    "Multi-task plan?" [shape=diamond];
    "subagent-driven-development" [shape=box];
    "requesting-code-review" [shape=box];

    "Starting feature work?" -> "Need clean workspace?" [label="yes"];
    "Starting feature work?" -> "Have implementation plan?" [label="no"];
    "Need clean workspace?" -> "using-git-worktrees" [label="yes"];
    "Need clean workspace?" -> "Have implementation plan?" [label="no"];
    "Have implementation plan?" -> "Multi-task plan?" [label="yes"];
    "Have implementation plan?" -> "Multiple failures?" [label="no"];
    "Multi-task plan?" -> "subagent-driven-development" [label="yes"];
    "Multi-task plan?" -> "requesting-code-review" [label="no"];
    "Multiple failures?" -> "Independent domains?" [label="yes"];
    "Multiple failures?" -> "Single failure path" [label="no"];
    "Independent domains?" -> "dispatching-parallel-agents" [label="yes"];
    "Independent domains?" -> "Single failure path" [label="no"];
}
```
