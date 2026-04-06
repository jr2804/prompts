# mise Options by Area

Use this file when the user asks for concrete options, defaults, tradeoffs, or command-level recommendations.

## 1) Toolchain Management Options

Primary commands:

- `mise use [tool@version]` adds/updates tool declarations.
- `mise install` installs declared tools.
- `mise exec -- <cmd>` runs a command in mise context.

Version strategy:

- Prefer major or channel pins (for example `node@20`, `node@lts`) in config.
- Use lockfiles for exact reproducibility rather than hard-pinning every patch version.

Important settings:

- `pin` (default false): makes `mise use` pin exact versions by default.
- `lockfile` (default enabled when unset): read/write lockfiles.
- `locked` (default false): fail install if lockfile lacks pre-resolved URLs for platform.
- `auto_install` (default true): global gate for automatic installs.
- `exec_auto_install` (default true): auto-install behavior for `mise exec`.
- `not_found_auto_install` (default true): shell "command not found" auto-install handler.

When to recommend:

- Team reproducibility or CI determinism: enable lockfile workflow and consider `locked = true` in CI.
- Strict release-age controls: use `install_before` to avoid just-published versions.

## 2) Backends and Source Selection

Common backends:

- Core tools (runtime-native support).
- `aqua:` ecosystem.
- `github:` release assets.
- `npm:` packages.
- `pipx:` Python CLI apps.

Use backend prefixes when explicit source control is needed, for example:

- `mise use npm:prettier@latest`
- `mise use pipx:black@latest`
- `mise use github:BurntSushi/ripgrep@latest`

Relevant settings:

- `disable_backends`: block selected backends globally.
- `disable_default_registry`: disable shorthand resolution for some backend families.
- `shorthands_file`: provide organization-specific shorthand mappings.

## 3) Activation, PATH, and Shell Behavior

Choose one strategy per context:

- Interactive local dev: `mise activate <shell>`.
- Non-interactive contexts and some IDE/CI cases: shims and explicit `mise exec` / `mise run`.

High-impact settings:

- `activate_aggressive`: move mise paths ahead of later PATH edits.
- `windows_shim_mode`: choose shim implementation (`exe`, `file`, `hardlink`, `symlink`).
- `terminal_progress`: progress integration in supported terminals.

Troubleshooting sequence:

1. `mise doctor`
2. `mise ls --current`
3. Compare shell resolution with `mise which <tool>`.
4. If mismatch persists, fix activation or shim mode.

## 4) Configuration Discovery and File Selection

Common files and intent:

- `mise.toml`: shared project configuration.
- `mise.local.toml`: local personal overrides, normally gitignored.
- `.tool-versions`: asdf-compatible legacy format.
- `~/.config/mise/config.toml`: global user defaults.

Early-init settings (must be env var, CLI flag, or early config such as `.miserc.toml`):

- `ceiling_paths`
- `env`
- `ignored_config_paths`
- `override_config_filenames`
- `override_tool_versions_filenames`

Recommend these only when the user needs custom discovery boundaries or alternate naming conventions.

## 5) Environment Variable Management

Core patterns:

- `[env]` for straightforward key-value env vars.
- `_.file`, `_.path`, `_.source` directives for loading env files, extending PATH, and sourcing scripts.
- `required = true` (or help text) for mandatory variables.
- `redact = true` or `redactions` patterns for sensitive output masking.

Useful settings:

- `env_shell_expand`: enable shell-style expansion like `$VAR` and `${VAR:-default}`.
- `env_cache` and `env_cache_ttl`: speed repeated env resolution.
- `env_file`: implicit env file loading path.
- `no_env`: disable env loading from config.

## 6) Task Runner Options

Task definitions:

- TOML tasks in `[tasks]`.
- File-based tasks in `mise-tasks/` (executable scripts).

Key task settings:

- `task.output`: `prefix`, `interleave`, `keep-order`, `replacing`, `timed`, `quiet`, `silent`.
- `task.run_auto_install`: install missing tools before running tasks.
- `task.timeout`: default task timeout.
- `task.monorepo_depth`, `task.monorepo_exclude_dirs`, `task.monorepo_respect_gitignore` for monorepo discovery.
- `task.skip` and `task.skip_depends` for selective execution.

Recommend `task.output = "prefix"` in CI when readable logs are required.

## 7) CI and Offline Controls

For reproducible and resilient automation:

- Use lockfile workflow (`lockfile`, `locked`, `mise lock`).
- Provide GitHub authentication to avoid API rate limits.
- Use `offline` for fully disconnected mode.
- Use `prefer_offline` to minimize network calls while allowing fallback.
- Consider `http_timeout`, `http_retries`, and mirrors for unreliable networks.

## 8) Security and Supply Chain Options

Global verification controls:

- `slsa` and `github_attestations`.
- Backend-specific variants where supported (for example `aqua.*`, `github.*`).
- `paranoid` for extra-secure behavior.
- `install_before` to require release age before fuzzy version resolution.

Recommend these when users ask for hardened toolchain posture or controlled rollout risk.

## 9) Quick Decision Matrix

- User wants stable team toolchain: project `mise.toml` + lockfile.
- User wants personal overrides: `mise.local.toml` (or global config).
- User sees "command not found": run doctor and activation diagnostics before recommending workarounds.
- User asks for one command without changing shell setup: `mise exec -- ...`.
- User needs CI repeatability: lockfile + `locked`, explicit auth, deterministic task output.

## 10) Canonical Sources

- <https://mise.jdx.dev/>
- <https://mise.jdx.dev/getting-started.html>
- <https://mise.jdx.dev/dev-tools/>
- <https://mise.jdx.dev/environments/>
- <https://mise.jdx.dev/tasks/>
- <https://mise.jdx.dev/configuration/settings.html>
