# tea CLI Reference

Complete command-line reference for tea. See the main SKILL.md for usage examples and common workflows.

## Official Documentation

- Main docs: <https://gitea.com/gitea/tea/src/branch/main/docs/CLI.md>
- GitHub: <https://github.com/gitea/tea>
- Releases: <https://github.com/gitea/tea/releases>

## Installation

```bash
# Via Go
go install github.com/gitea/tea@latest

# Via Homebrew
brew install tea

# Download binary from releases
curl -sL https://github.com/gitea/tea/releases/download/v0.9.0/tea-0.9.0-linux-amd64 -o tea
chmod +x tea
```

## Global Options

- `--help, -h`: Show help
- `--version`: Show version
- `--config`: Config directory (default: ~/.config/tea)

## Command Hierarchy

```text
tea
├── logins (login)
│   ├── list (ls)
│   ├── add
│   ├── edit (e)
│   ├── delete (rm)
│   ├── default
│   └── oauth-refresh
├── logout
├── whoami
├── issues (issue, i)
│   ├── list (ls)
│   ├── create (c)
│   ├── edit (e)
│   ├── reopen (open)
│   └── close
├── pulls (pull, pr)
│   ├── list (ls)
│   ├── checkout (co)
│   ├── clean
│   ├── create (c)
│   ├── close
│   ├── reopen (open)
│   ├── review
│   ├── approve (lgtm, a)
│   ├── reject
│   └── merge (m)
├── labels (label)
│   ├── list (ls)
│   ├── create (c)
│   ├── update
│   └── delete (rm)
├── milestones (milestone, ms)
│   ├── list (ls)
│   ├── create (c)
│   ├── close
│   ├── delete (rm)
│   ├── reopen (open)
│   └── issues (i)
│       ├── add (a)
│       └── remove (r)
├── releases (release, r)
│   ├── list (ls)
│   ├── create (c)
│   ├── delete (rm)
│   ├── edit (e)
│   └── assets (asset, a)
│       ├── list (ls)
│       ├── create (c)
│       └── delete (rm)
├── times (time, t)
│   ├── add (a)
│   ├── delete (rm)
│   ├── reset
│   └── list (ls)
├── organizations (organization, org)
│   ├── list (ls)
│   ├── create (c)
│   └── delete (rm)
├── repos (repo)
│   ├── list (ls)
│   ├── search (s)
│   ├── create (c)
│   ├── create-from-template (ct)
│   ├── fork (f)
│   ├── migrate (m)
│   ├── delete (rm)
│   └── edit (e)
├── branches (branch, b)
│   ├── list (ls)
│   ├── protect (P)
│   └── unprotect (U)
├── actions (action)
│   ├── secrets (secret)
│   │   ├── list (ls)
│   │   ├── create (add, set)
│   │   └── delete (remove, rm)
│   ├── variables (variable, vars, var)
│   │   ├── list (ls)
│   │   ├── set (create, update)
│   │   └── delete (remove, rm)
│   ├── runs (run)
│   │   ├── list (ls)
│   │   ├── view (show, get)
│   │   ├── delete (remove, rm, cancel)
│   │   └── logs (log)
│   └── workflows (workflow)
│       └── list (ls)
├── webhooks (webhook, hooks, hook)
│   ├── list (ls)
│   ├── create (c)
│   ├── delete (rm)
│   └── update (edit, u)
├── comment (c)
├── open (o)
└── notifications (notification, n)
```

## Output Format Details

| Format | Use Case |
|--------|----------|
| simple | Single line per item |
| table | Human-readable table |
| csv | CSV export |
| tsv | TSV export |
| yaml | YAML output |
| json | JSON output |

## Environment Variables

- `TEA_CONFIG`: Config directory path
- `TEA_LOGIN`: Default login to use
- `TEA_OUTPUT`: Default output format

## Configuration File

Location: `~/.config/tea/config.yml`

```yaml
logins:
  - name: gitea.com
    url: https://gitea.com
    token: your-token-here
  - name: self-hosted
    url: https://gitea.example.com
    token: another-token
    insecure: true

defaults:
  login: gitea.com
  output: table
```

## Common Workflows

### First Time Setup

```bash
# 1. Add a login
tea logins add --url https://gitea.com --token YOUR_TOKEN --name gitea

# 2. Verify authentication
tea whoami

# 3. List your repos
tea repos list
```

### Issue Workflow

```bash
# List open issues
tea issues list --state open

# Create new issue
tea issues create --title "Bug: Login fails" --description "Steps to reproduce..."

# Add labels
tea issues edit --add-labels bug 123
```

### PR Workflow

```bash
# List open PRs
tea pulls list --state open

# Checkout PR locally
tea pulls checkout 123

# After making changes, create PR
tea pulls create --title "Fix login bug" --base main

# Approve a PR
tea pulls approve 456
```

### Release Workflow

```bash
# Create release
tea releases create --title "v1.0.0" --tag v1.0.0 --note "Release notes"

# Add assets
tea releases assets create 1 --asset ./binary-linux-amd64
```

### Actions Workflow

```bash
# List workflow runs
tea actions runs list --status failure

# View run details
tea actions runs view 123

# View logs
tea actions runs logs 123 --follow
```
