---
name: tea
description: Command-line tool to interact with Gitea. Use when working with Gitea repositories, issues, pull requests, releases, labels, milestones, organizations, branches, actions, webhooks, or notifications. Provides local helpers like 'tea pr checkout'. Works best in an upstream/fork workflow when the local main branch tracks the upstream repo. Configuration is persisted in $XDG_CONFIG_HOME/tea.
---

# tea - Gitea CLI

A productivity helper for Gitea. Manages most entities on one or multiple Gitea instances and provides local helpers.

## When to Use This Skill

- Managing Gitea repositories (create, fork, migrate, delete)
- Working with issues (list, create, edit, close, reopen)
- Managing pull requests (list, create, checkout, merge, review, approve, reject)
- Managing labels, milestones, and releases
- Tracking time on issues/PRs
- Managing organizations
- Working with branches (list, protect, unprotect)
- Managing GitHub Actions (secrets, variables, runs, workflows)
- Managing webhooks
- Viewing and managing notifications

## Core Concepts

### Authentication

tea uses a login system to manage Gitea server connections. Each login stores:
- Server URL
- Authentication method (token, OAuth, SSH key, or basic auth)
- Optional: client ID, scopes, OTP token

### Context Awareness

tea tries to use context provided by the repository in $PWD if available. Use `--repo` or `--remote` flags to override.

### Output Formats

All commands support `--output` (`-o`) flag with formats: simple, table, csv, tsv, yaml, json

## Commands

### logins - Authentication Management

```bash
# List all logins
tea logins list

# Add a new login with token
tea logins add --url https://gitea.example.com --token YOUR_TOKEN --name myserver

# Add login with SSH key
tea logins add --url https://gitea.example.com --ssh-key /path/to/key --name sshserver

# Add login with OAuth
tea logins add --url https://gitea.example.com --oauth --name oauthserver

# Set default login
tea logins default --name myserver

# Delete a login
tea logins delete --name myserver

# Show current logged in user
tea whoami
```

### issues - Issue Management

```bash
# List issues
tea issues list --state open
tea issues list --labels bug,urgent
tea issues list --assignee username
tea issues list --milestone "v1.0"

# Create an issue
tea issues create --title "Bug in login" --description "Description here"
tea issues create -t "Issue title" -d "Description" --labels bug --assignees user1,user2

# Edit issues
tea issues edit --title "New title" 123
tea issues edit --add-labels feature --remove-labels bug 123

# Close/reopen issues
tea issues close 123
tea issues reopen 123
```

### pulls - Pull Request Management

```bash
# List pull requests
tea pulls list --state open

# Checkout a PR locally
tea pulls checkout 123
tea pulls checkout 123 --branch  # Create local branch if needed

# Create a PR
tea pulls create --title "Feature X" --description "Description" --base main
tea pulls create -t "PR title" -d "PR body" --head feature-branch

# Merge a PR
tea pulls merge 123
tea pulls merge 123 --style squash  # squash, rebase, merge

# Review PRs
tea pulls review 123
tea pulls approve 123
tea pulls reject 123 --message "Needs changes"

# Close/reopen PRs
tea pulls close 123
tea pulls reopen 123

# Clean up closed PR branches
tea pulls clean 123
```

### labels - Label Management

```bash
# List labels
tea labels list

# Create a label
tea labels create --name bug --color "ff0000" --description "Bug label"

# Update a label
tea labels update --id 1 --name "critical bug" --color "ff0000"

# Delete a label
tea labels delete --id 1
```

### milestones - Milestone Management

```bash
# List milestones
tea milestones list --state open

# Create a milestone
tea milestones create --title "v1.0" --description "First release"
tea milestones create -t "v2.0" --deadline 2024-12-31

# Close/delete milestones
tea milestones close 1
tea milestones delete 1
tea milestones reopen 1

# Manage issues in milestone
tea milestones issues --add 1 123  # Add issue 123 to milestone 1
tea milestones issues --remove 1 123
```

### releases - Release Management

```bash
# List releases
tea releases list

# Create a release
tea releases create --title "v1.0.0" --tag v1.0.0 --note "Release notes"
tea releases create -t "v1.0.0" -t v1.0.0 -n "Notes" --draft --prerelease

# Edit a release
tea releases edit --title "New title" 1

# Delete a release
tea releases delete --confirm 1
tea releases delete --confirm --delete-tag 1  # Also delete git tag

# Manage release assets
tea releases assets list 1
tea releases assets create 1 --asset /path/to/file.zip
tea releases assets delete --confirm 1 asset-name
```

### times - Time Tracking

```bash
# List tracked times
tea times list
tea times list --repo owner/repo
tea times list --mine  # Your times across all repos

# Add time to an issue
tea times add 123 --duration 2h30m

# Delete/reset time
tea times delete 1
tea times reset 123
```

### organizations - Organization Management

```bash
# List organizations
tea orgs list

# Create an organization
tea orgs create --name myorg --description "My Organization"

# Delete an organization
tea orgs delete --name myorg
```

### repos - Repository Management

```bash
# List your repositories
tea repos list
tea repos list --owner username
tea repos list --type fork  # fork, mirror, source

# Search repositories
tea repos search --keyword myproject
tea repos search --topic machine-learning

# Create a repository
tea repos create --name myrepo --description "My new repo"
tea repos create -n newrepo --private --init --gitignores Go --license MIT

# Fork a repository
tea repos fork --owner gitea --repo tea

# Migrate a repository
tea repos migrate --clone-url https://github.com/user/repo --service github --issues --labels --milestones

# Delete a repository
tea repos delete --owner username --name reponame --force

# Edit repository
tea repos edit --owner user --repo name --private false
tea repos edit -R owner/repo --description "New description"
```

### branches - Branch Management

```bash
# List branches
tea branches list

# Protect a branch
tea branches protect main

# Unprotect a branch
tea branches unprotect main
```

### actions - GitHub Actions Management

```bash
# Manage secrets
tea actions secrets list
tea actions secrets create --name SECRET_NAME --value value
tea actions secrets create --name NAME --stdin  # Read from stdin
tea actions secrets delete --confirm --name NAME

# Manage variables
tea actions variables list
tea actions variables set --name VAR_NAME --value value
tea actions variables delete --confirm --name NAME

# Manage workflow runs
tea actions runs list
tea actions runs list --status success --branch main
tea actions runs view 123
tea actions runs view 123 --jobs  # Show jobs table
tea actions runs logs 123
tea actions runs logs 123 --follow  # Follow log output
tea actions runs delete --confirm 123

# Manage workflows
tea actions workflows list
```

### webhooks - Webhook Management

```bash
# List webhooks
tea webhooks list
tea webhooks list --repo owner/repo

# Create a webhook
tea webhooks create --url https://example.com/webhook --events push,issues
tea webhooks create -u URL --type slack

# Update a webhook
tea webhooks update --id 1 --url new-url --active

# Delete a webhook
tea webhooks delete --confirm --id 1
```

### comment - Add Comments

```bash
# Add comment to issue/PR
tea comment 123 --body "This is a comment"
tea comment -r owner/repo 123 -d "Comment text"
```

### open - Open in Browser

```bash
# Open repository in browser
tea open
tea open --repo owner/repo

# Open specific items
tea open issues 123
tea open pulls 123
tea open releases 1
```

### notifications - Notifications

```bash
# List notifications
tea notifications list
tea notifications list --states unread,pinned

# All your notifications across repos
tea notifications list --mine
```

## Common Options

- `--login, -l`: Use a different Gitea login
- `--repo, -r`: Override local repository path or gitea slug (e.g., "owner/repo")
- `--remote, -R`: Discover Gitea login from remote
- `--output, -o`: Output format (simple, table, csv, tsv, yaml, json)
- `--limit, --lm`: Items per page (default: 30)
- `--page, -p`: Page number (default: 1)

## Installation

```bash
# Install tea via package manager or download from releases
# https://github.com/gitea/tea/releases

# Or install via Go
go install github.com/gitea/tea@latest
```

## Configuration

Configuration is stored in `$XDG_CONFIG_HOME/tea` (typically `~/.config/tea`).

## Guidelines

1. Always authenticate first using `tea logins add` before running other commands
2. Use `--output json` or `--output yaml` for scriptable output
3. Use `--limit` and `--page` for paginated results
4. Use `--confirm` or `-y` flag when deleting to skip prompts
5. tea works best when run from within a git repository cloned from Gitea

## Gotchas

1. **Authentication required**: Most commands require a login. Run `tea logins add` first.
2. **Repository context**: tea auto-detects the repository from PWD. Use `--repo owner/repo` if not in a git repo.
3. **Output format**: Use `--output json` for programmatic access; table format is default.
4. **Delete confirmation**: Most delete commands require `--confirm` or `-y` flag.
5. **PR checkout**: `tea pulls checkout` creates a local branch but doesn't switch to it automatically; use `git checkout` after.
6. **Time tracking**: Time duration format accepts formats like "2h30m" or "150m".

## Integration

Related skills in this collection:
- skill-creator - For creating and updating skills
- git - For git operations that work well with tea