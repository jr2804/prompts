# Code Auditing Reference

Comprehensive 6-dimension code audit methodology for codebase analysis.

## Table of Contents

1. [Audit Dimensions](#audit-dimensions)
   - [1. Architecture](#1-architecture)
   - [2. Code Quality](#2-code-quality)
   - [3. Security](#3-security)
   - [4. Performance](#4-performance)
   - [5. Testing](#5-testing)
   - [6. Maintainability](#6-maintainability)
2. [Severity Ratings](#severity-ratings)
3. [Audit Report Format](#audit-report-format)
4. [When to Audit](#when-to-audit)

______________________________________________________________________

## Audit Dimensions

### 1. Architecture

Analyze overall structure and design decisions.

**Check:**

- Overall structure and organization
- Design patterns in use
- Module boundaries and separation of concerns
- Dependency management (depth, circular dependencies)
- Architectural decisions and trade-offs
- Inter-module communication patterns

**Red Flags:**

- God modules with many responsibilities
- Circular dependencies between modules
- Unclear boundaries between layers
- Hidden coupling through global state

______________________________________________________________________

### 2. Code Quality

Assess readability, complexity, and duplication.

**Check:**

- Cyclomatic complexity hotspots
- Code duplication (DRY violations)
- Naming conventions and consistency
- Documentation coverage
- Function length and Single Responsibility Principle
- Dead code and unused imports

**Red Flags:**

- Functions exceeding 50 lines
- Repeated switch/if-else chains
- Inconsistent naming schemes
- Magic numbers or hardcoded values
- Missing docstrings on public APIs

______________________________________________________________________

### 3. Security

Identify vulnerabilities and protection gaps.

**Check:**

- Input validation and sanitization
- Authentication and authorization patterns
- Secrets management (no hardcoded credentials)
- SQL injection and parameterization
- Dependency vulnerabilities (outdated or known-vulnerable packages)
- OWASP Top 10 issues

**Red Flags:**

- User input used in queries or commands without validation
- API keys or passwords in source code
- Missing access control checks
- Unvalidated file paths or content
- Insecure deserialization

______________________________________________________________________

### 4. Performance

Find bottlenecks and resource inefficiencies.

**Check:**

- Algorithmic complexity issues (O(n²) or worse in hot paths)
- Database query optimization (N+1 queries, missing indexes)
- Memory usage patterns (leaks, excessive allocation)
- Caching opportunities
- Resource leaks (unclosed files, connections)
- Unnecessary iterations or copies

**Red Flags:**

- Nested loops processing large datasets
- Loading entire datasets into memory
- Missing pagination or streaming
- Unnecessary object creation in hot paths
- Unclosed resources in error paths

______________________________________________________________________

### 5. Testing

Evaluate test coverage and quality.

**Check:**

- Test coverage percentage and trends
- Test quality and effectiveness
- Missing test scenarios (happy path, edge cases, error paths)
- Test isolation and independence
- Integration vs unit test balance
- Mock and fixture practices

**Red Flags:**

- Coverage below 70%
- Tests that only assert one thing
- Shared mutable state between tests
- Tests depending on execution order
- Missing error condition tests

______________________________________________________________________

### 6. Maintainability

Assess technical debt and long-term health.

**Check:**

- Technical debt assessment
- Module coupling and cohesion
- Ease of future changes
- Onboarding friendliness (code clarity)
- Documentation quality (README, API docs, inline comments)
- Configuration complexity

**Red Flags:**

- Duplicate code across modules
- Complex conditional logic without explanation
- Missing or outdated documentation
- Over-engineered abstractions
- Tight coupling preventing independent changes

______________________________________________________________________

## Severity Ratings

| Rating | Description | Action |
|--------|-------------|--------|
| **Critical** | Exploitable vulnerability or data loss risk | Fix immediately |
| **High** | Significant issue affecting reliability or security | Fix within 1 week |
| **Medium** | Code quality or maintainability concern | Schedule fix |
| **Low** | Improvement opportunity | Address when convenient |

______________________________________________________________________

## Audit Report Format

```markdown
# Code Audit Report

## Executive Summary
- Overall health score: X/10
- Critical issues: N
- High priority issues: N
- Top recommendation

## Findings

### Critical
- [Issue]: [File:Line]
  - Impact: [Description]
  - Fix: [Recommendation]

### High
- [Issue]: [File:Line]
  - Impact: [Description]
  - Fix: [Recommendation]

### Medium
- [Issue]: [File:Line]
  - Impact: [Description]
  - Fix: [Recommendation]

### Low
- [Issue]: [File:Line]
  - Impact: [Description]
  - Fix: [Recommendation]

## Action Plan

1. **Immediate** (< 1 day): [Critical fixes]
2. **Short-term** (1-5 days): [High priority]
3. **Medium-term** (1-2 weeks): [Medium priority]
4. **Backlog**: [Low priority improvements]

## Metrics
- Files analyzed: X
- Lines of code: Y
- Test coverage: Z%
- Complexity hotspots: N
```

______________________________________________________________________

## When to Audit

**Trigger an audit when:**

- Starting a major refactoring effort
- Investigating recurring bugs or incidents
- Onboarding to unfamiliar codebase
- Planning significant feature additions
- Security compliance requirements
- Pre-release quality check
- Post-mortem after production issues

**Audit depth levels:**

- **Quick** (15-30 min): Critical issues only, high-level scan
- **Standard** (30-60 min): Full 6-dimension analysis
- **Deep** (60+ min): Exhaustive with line-by-line review

______________________________________________________________________

## Audit Workflow

1. **Explore** the codebase structure thoroughly
2. **Identify patterns** using Grep and Glob
3. **Read critical files** in detail
4. **Run static analysis** tools if available
5. **Synthesize findings** into actionable report

**Tools:**

- `grep` / `rg` — Pattern matching for code smells
- `glob` — Find files by type or pattern
- `read` — Detailed file analysis
- `bash` — Run linters, complexity analyzers, coverage tools
- LSP diagnostics — IDE-level issue detection
