# Example PLAN.md

A complete, realistic PLAN.md for a medium-complexity feature: adding API rate limiting
to an existing Express + TypeScript REST API using Redis. This touches config, middleware,
route registration, tests, and docs — approximately 8-12 tasks across 3 phases.

Note: This example demonstrates a self-contained plan that a fresh agent session
could implement with only this file.

______________________________________________________________________

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
  - `src/app.ts` — main Express app, where middleware is mounted. Imports routes from `./routes`
  - `src/routes/index.ts` — route registration barrel, exports `Router` instance
  - `src/config/index.ts` — env-var based config using dotenv. Pattern: `export const FOO = process.env.FOO || 'default'`
  - `src/middleware/` — existing middleware (auth.ts, errors.ts); new rate-limiter.ts goes here
  - `src/redis.ts` — existing Redis client singleton. Exports `redis` client instance
  - `tests/integration/` — existing integration tests using supertest

- **Patterns to follow:**
  - Config pattern (from `src/config/index.ts`):
    ```typescript
    export const RATE_LIMIT_WINDOW_MS = parseInt(process.env.RATE_LIMIT_WINDOW_MS || '60000', 10);
    export const RATE_LIMIT_MAX = parseInt(process.env.RATE_LIMIT_MAX || '100', 10);
    ```
  - Middleware pattern (from `src/middleware/auth.ts`):
    ```typescript
    export const authMiddleware: RequestHandler = (req, res, next) => {
      // logic here
      next();
    };
    ```
  - Test pattern (from `tests/integration/`): uses supertest with `request(app)` helper

- **Dependencies:**
  - `express-rate-limit` — already installed, verify with `npm ls express-rate-limit`
  - `rate-limit-redis` — needs install: `npm install rate-limit-redis`
  - Redis must be running: verify with `redis-cli ping` → expect `PONG`

- **Environment:**
  - Redis URL from `REDIS_URL` env var (already configured)
  - New env vars to add: `RATE_LIMIT_WINDOW_MS`, `RATE_LIMIT_MAX` (with defaults)

- **Constraints:**
  - Must use existing Redis connection (`src/redis.ts`), not spin up a second
  - Rate limit keys must not collide with session keys (use `rl:` prefix)
  - Out of scope: per-user limits, admin bypass, rate limit dashboards

## Phases

### Phase 1: Config and Redis Key Design

**Deliverable:** Config values for rate limiting are defined and validated; key naming
convention is documented and unit-tested.

- [ ] Add `RATE_LIMIT_WINDOW_MS` (default: 60000) and `RATE_LIMIT_MAX` (default: 100) to `src/config/index.ts`
- [ ] Add `RATE_LIMIT_PREFIX` constant (`"rl:"`) to `src/redis.ts` after the client creation
- [ ] Create `tests/unit/config.test.ts` — verify defaults and env-var overrides for new config values

### Phase 2: Rate-Limiter Middleware

**Deliverable:** `src/middleware/rateLimiter.ts` is implemented and unit-tested with a mocked
Redis client; middleware correctly increments counters and returns 429 on breach.

- [ ] Install `rate-limit-redis`: `npm install rate-limit-redis`
- [ ] Create `src/middleware/rateLimiter.ts` — Express middleware using express-rate-limit with Redis store
- [ ] Middleware sets `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `Retry-After` headers
- [ ] Create `tests/unit/rateLimiter.test.ts` — mock Redis client, test: first request returns 200 with correct headers; 101st request returns 429

### Phase 3: Mount and Integration Tests

**Deliverable:** Rate limiting is active on all routes; integration tests demonstrate
the limit end-to-end against a real (test) Redis instance.

- [ ] Mount `rateLimiter` middleware in `src/app.ts` before route registration
- [ ] Add `RATE_LIMIT_MAX=3` to `tests/setup.ts` environment setup
- [ ] Create `tests/integration/rateLimit.test.ts` — fire 4 requests with supertest, assert first 3 return underlying route status, 4th returns 429
- [ ] Verify `Retry-After` header value matches configured window

## Validation

- [ ] Run `npm test` from project root — all tests pass (existing + new)
- [ ] Start server: `npm run dev` with `RATE_LIMIT_MAX=4` in `.env.local`
- [ ] Run: `for i in $(seq 1 5); do curl -s -o /dev/null -w "%{http_code}\n" http://localhost:3000/api/health; done` — expect: 200, 200, 200, 200, 429
- [ ] Check headers: `curl -I http://localhost:3000/api/health` — expect `X-RateLimit-Limit` and `X-RateLimit-Remaining` headers

## Progress

- [x] (2025-10-01 09:00Z) Created PLAN.md
- [x] (2025-10-01 09:15Z) Phase 1: Added config vars and RATE_LIMIT_PREFIX constant
- [x] (2025-10-01 09:30Z) Phase 1: Unit tests written and passing
- [x] (2025-10-01 10:00Z) Phase 2: Installed rate-limit-redis, created rateLimiter.ts
- [x] (2025-10-01 10:45Z) Phase 2: Unit tests passing (mocked Redis)
- [x] (2025-10-01 11:30Z) Phase 3: Middleware mounted; integration tests passing
- [x] (2025-10-01 11:45Z) All validation criteria verified manually

## Decisions

- Decision: Used express-rate-limit with rate-limit-redis (fixed window) instead of sliding window / Rationale: Fixed window is simpler and sufficient for current traffic patterns; sliding window adds complexity without clear benefit at this scale / Date: 2025-10-01
- Decision: Applied rate limit globally (all routes) rather than per-route config / Rationale: Per-route config is out of scope per constraints; global is the simplest correct starting point / Date: 2025-10-01

## Notes

- Discovered that `src/redis.ts` did not export the client type — added `export type RedisClient` to allow proper mocking in unit tests. Small change, low risk.
- Evidence: `npm test` output — 47 tests passed, 0 failed after adding the type export.
