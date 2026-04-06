---
name: mise
description: >-
  Mise toolchain and task management guide for selecting the right mise options and commands across tools, environments, tasks, and CI. Use when setting up or troubleshooting mise, choosing between mise.toml and mise.local.toml, configuring activation vs shims, selecting backends, or tuning settings like lockfile, auto-install, offline, and task output.
---

# mise

Explain and apply mise options for toolchains, environment variables, tasks, and automation.

## Core Workflow

1. Identify intent first: onboarding, adding a tool, task orchestration, env management, CI hardening, or troubleshooting.
2. Detect current setup before proposing changes.
3. Choose configuration scope and option set.
4. Apply changes with CLI-first commands.
5. Validate with health and behavior checks.

## 1) Identify Intent

Map the request to one of these paths:

- Tool versions and runtimes -> use tools flow.
- Project or shell env vars -> use environments flow.
- Build/test/deploy commands -> use tasks flow.
- Reproducible CI builds -> use lockfile and CI flow.
- "command not found" or PATH mismatch -> use troubleshooting flow.

For detailed decision tables and option references, read [options-by-area](./references/options-by-area.md).

## 2) Detect Current Setup

Inspect config files and trust state before editing:

```bash
ls -la mise.toml .mise.toml mise.local.toml .tool-versions 2>/dev/null
mise config
mise doctor
```

Prefer existing project conventions instead of introducing a new config format.

## 3) Choose Scope and File

- Team-wide, committed defaults: `mise.toml`
- Personal/local overrides (usually gitignored): `mise.local.toml`
- User-wide defaults: `~/.config/mise/config.toml`

Decision rule:

- If the change must be shared with all contributors, use `mise.toml`.
- If the change is personal or machine-specific, use `mise.local.toml` or global config.

## 4) Apply CLI-First Changes

Prefer CLI over manual editing when possible:

```bash
# add or update project tools
mise use node@20

# add global defaults
mise use -g python@3.12

# install tools declared in config
mise install

# one-off execution without full shell activation
mise exec -- node -v

# run tasks with mise context (tools + env)
mise run <task>
```

Use explicit settings for behavior changes that affect automation or security.

## 5) Validate and Troubleshoot

Run a minimal validation set after edits:

```bash
mise doctor
mise ls --current
mise which <tool>
<tool> --version
```

If `mise which <tool>` differs from shell `which`/`where`, diagnose activation or PATH configuration.

## Decision Points

- Activation vs shims:
  Use activation for interactive shells, shims for some CI or IDE contexts where shell init is limited.
- `mise use` vs manual TOML edits:
  Prefer `mise use` for tool additions and version changes.
- `mise exec` usage:
  Use for one-off/CI execution; do not treat it as a permanent workaround for broken activation.
- Locking strategy:
  Use loose versions in config plus lockfile for reproducibility.

## Completion Checks

The workflow is complete when all checks pass:

- Correct config scope selected and documented.
- Tools resolve as expected in current directory.
- Tasks run with expected environment.
- CI-oriented settings (if requested) are explicitly configured and verified.
- No unresolved doctor warnings relevant to the change.

## References

- Option catalog and branching logic: [options-by-area](./references/options-by-area.md)
