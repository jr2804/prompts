# PLAN.md Reference Guide

Consolidated reference for creating and maintaining `PLAN.md` — a lightweight living planning document for medium-complexity feature implementations.

______________________________________________________________________

## Table of Contents

1. [When to Use PLAN.md](#when-to-use-planmd)
2. [PLAN.md Structure](#planmd-structure)
3. [Self-Contained for Fresh Sessions](#self-contained-for-fresh-sessions)
4. [Template](#template)
5. [Example: Rate Limiting Feature](#example-rate-limiting-feature)

______________________________________________________________________

## When to Use PLAN.md

Create a PLAN.md when **all** of the following are true:

- The feature requires **more than 2 prompts** to implement
- It touches **multiple files or components**
- It involves **non-trivial decisions** (architecture, data model, API design)

**Scope sweet spot:** 3–15 prompts of work, 3–10 files affected.

Skip PLAN.md when:

- It's a quick fix or single-file edit
- The request is exploratory / throwaway
- A full spec already exists
- You can see the complete solution in your head right now

______________________________________________________________________

## PLAN.md Structure

### Goal

User-visible outcome in 2–3 sentences. State how to observe it working. Avoid internal details — describe behavior.

### Context

**Must be self-contained.** Include:

- Current state in one sentence
- Key files as full repo-relative paths with their roles
- Existing patterns to follow (with brief code examples if non-obvious)
- Dependencies (what packages/modules are needed)
- Environment setup (env vars, config, prerequisites)
- Constraints (locked-in choices, out-of-scope items)

### Phases

Break work into 2–4 sequential phases. Each phase must have:

- A name
- A **Deliverable** statement (what concretely exists at end)
- Checkbox tasks with specific file and function names

Start small — Phase 1 is often the data model, interface, or simplest path.

### Validation Criteria

Observable acceptance criteria. Include exact commands with working directory. Each criterion must be something a human can verify.

### Progress Tracking

Living checklist. Update continuously with timestamps. Never delete entries — mark done instead.

### Decisions Log

Record key non-obvious choices as they are made. Include rationale and date. Future contributors should understand why.

### Notes

Surprises, blockers, discoveries. Add immediately when encountered. Include evidence (test output, error messages, file paths).

______________________________________________________________________

## Self-Contained for Fresh Sessions

A fresh agent session with **only** the PLAN.md file must be able to implement the plan.

Ensure the Context section includes:

- Full paths to all relevant files
- Key patterns/functions to follow (with brief examples if non-obvious)
- Dependencies and how to verify them
- Environment setup needed

Ensure Phases include:

- Specific file and function names to create/modify
- Enough detail to implement without exploration

Ensure Validation includes:

- Exact commands to run
- Expected output or behavior

______________________________________________________________________

## Template

````markdown
# PLAN: <Short action-oriented feature title>

## Goal

<User-visible outcome in 2-3 sentences. How do they observe it working?>

## Context

- **Current state:** <Brief description of existing state>

- **Key files:**
  - `path/to/file.ts` — <what it does / why it matters / key functions>
  - `path/to/another.py` — <role in this feature>

- **Patterns to follow:**
  - <Existing pattern to match, e.g., "Error handling uses Result<T, E>">
  - ```typescript
    // Example: How errors are currently handled
    def process() -> Result[Data, Error]:
        ...
    ```

- **Dependencies:**
  - <Package>: <how to verify, e.g., `pip show <pkg>`>

- **Environment:**
  - <Env vars needed>
  - <Config files to create/modify>

- **Constraints:** <Locked-in choices, out-of-scope items>

## Phases

### Phase 1: <Name>

**Deliverable:** <What concretely exists at end — a passing test, a working endpoint>

- [ ] Create/modify `path/to/file.ts` — add `<Class>` with `<method>`
- [ ] Create `path/to/test.ts` — test cases for `<scenario>`

### Phase 2: <Name>

**Deliverable:** <Deliverable>

- [ ] <Specific task with file path and function name>
- [ ] <Test task>

## Validation

- [ ] Run `<command>` from `<directory>`, expect `<output or exit code>`
- [ ] Navigate to `<URL>`, observe `<specific behavior>`

## Progress

- [x] (<YYYY-MM-DD HH:MMZ>) Created PLAN.md
- [ ] Phase 1 complete
- [ ] Phase 2 complete
- [ ] All validation criteria met

## Decisions

- Decision: <What> / Rationale: <Why> / Date: <YYYY-MM-DD>

## Notes

<!-- Add notes during implementation as things are discovered. -->
````

______________________________________________________________________

## Example: Rate Limiting Feature

````markdown
# PLAN: Rate Limiting for REST API Endpoints

## Goal

After this, all public REST API endpoints enforce per-IP rate limits (100 req/min default,
configurable per route). Clients that exceed the limit receive a `429 Too Many Requests`
response with a `Retry-After` header. Existing tests continue to pass; new integration
tests cover the limit behavior.

## Context

- **Current state:** Express app with ~15 REST endpoints in `src/routes/`. No rate limiting exists.
  All routes registered in `src/app.ts`. Redis already in the stack for session caching.

- **Key files:**
  - `src/app.ts` — main Express app, where middleware is mounted
  - `src/routes/index.ts` — route registration barrel
  - `src/config/index.ts` — env-var based config using dotenv
  - `src/middleware/` — existing middleware (auth.ts, errors.ts)
  - `src/redis.ts` — existing Redis client singleton

- **Patterns to follow:**
  - Config pattern:
    ```typescript
    export const RATE_LIMIT_WINDOW_MS = parseInt(process.env.RATE_LIMIT_WINDOW_MS || '60000', 10);
    ```
  - Middleware pattern:
    ```typescript
    export const authMiddleware: RequestHandler = (req, res, next) => { next(); };
    ```

- **Dependencies:**
  - `express-rate-limit` — already installed
  - `rate-limit-redis` — needs install
  - Redis must be running: `redis-cli ping` → `PONG`

- **Environment:**
  - Redis URL from `REDIS_URL` env var
  - New env vars: `RATE_LIMIT_WINDOW_MS`, `RATE_LIMIT_MAX`

- **Constraints:**
  - Must use existing Redis connection, not spin up a second
  - Rate limit keys must not collide with session keys (use `rl:` prefix)
  - Out of scope: per-user limits, admin bypass

## Phases

### Phase 1: Config and Redis Key Design

**Deliverable:** Config values for rate limiting are defined and validated.

- [ ] Add `RATE_LIMIT_WINDOW_MS` (default: 60000) and `RATE_LIMIT_MAX` (default: 100) to `src/config/index.ts`
- [ ] Add `RATE_LIMIT_PREFIX` constant (`"rl:"`) to `src/redis.ts`
- [ ] Create `tests/unit/config.test.ts` — verify defaults and env-var overrides

### Phase 2: Rate-Limiter Middleware

**Deliverable:** `src/middleware/rateLimiter.ts` is implemented and unit-tested.

- [ ] Install `rate-limit-redis`
- [ ] Create `src/middleware/rateLimiter.ts` — Express middleware using express-rate-limit with Redis store
- [ ] Middleware sets `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `Retry-After` headers
- [ ] Create `tests/unit/rateLimiter.test.ts` — mock Redis, test: first request returns 200; 101st returns 429

### Phase 3: Mount and Integration Tests

**Deliverable:** Rate limiting is active on all routes; integration tests pass.

- [ ] Mount `rateLimiter` middleware in `src/app.ts` before route registration
- [ ] Add `RATE_LIMIT_MAX=3` to `tests/setup.ts`
- [ ] Create `tests/integration/rateLimit.test.ts` — fire 4 requests, 4th returns 429

## Validation

- [ ] Run `npm test` from project root — all tests pass
- [ ] Start server with `RATE_LIMIT_MAX=4` in `.env.local`
- [ ] Run: `for i in $(seq 1 5); do curl -s -o /dev/null -w "%{http_code}\n" http://localhost:3000/api/health; done` — expect: 200, 200, 200, 200, 429
- [ ] Check headers: `curl -I http://localhost:3000/api/health` — expect `X-RateLimit-Limit` and `X-RateLimit-Remaining`

## Progress

- [x] (2025-10-01 09:00Z) Created PLAN.md
- [ ] Phase 1 complete
- [ ] Phase 2 complete
- [ ] Phase 3 complete
- [ ] All validation criteria met

## Decisions

- Decision: Used express-rate-limit with rate-limit-redis (fixed window) / Rationale: Fixed window is simpler and sufficient for current traffic patterns / Date: 2025-10-01
- Decision: Applied rate limit globally rather than per-route / Rationale: Per-route config is out of scope; global is the simplest correct starting point / Date: 2025-10-01

## Notes

<!-- Add surprises, blockers, discoveries during implementation. -->
````
