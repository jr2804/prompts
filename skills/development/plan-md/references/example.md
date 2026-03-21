# Example PLAN.md

A complete, realistic PLAN.md for a medium-complexity feature: adding API rate limiting
to an existing Express + TypeScript REST API using Redis. This touches config, middleware,
route registration, tests, and docs — approximately 8-12 tasks across 3 phases.

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
  - `src/app.ts` — main Express app, where middleware is mounted
  - `src/routes/index.ts` — route registration barrel
  - `src/config/index.ts` — env-var based config (add `RATE_LIMIT_*` vars here)
  - `src/middleware/` — existing middleware (auth, errors); new rate-limiter goes here
  - `src/redis.ts` — existing Redis client singleton used for sessions
  - `tests/integration/` — existing integration tests using supertest
- **Constraints:** Must use existing Redis connection (`src/redis.ts`), not spin up a second.
  Rate limit keys must not collide with session keys (use `rl:` prefix).
  Out of scope: per-user limits, admin bypass, rate limit dashboards.

## Phases

### Phase 1: Config and Redis Key Design

**Deliverable:** Config values for rate limiting are defined and validated; key naming
convention is documented and unit-tested.

- [ ] Add `RATE_LIMIT_WINDOW_MS` (default: 60000) and `RATE_LIMIT_MAX` (default: 100) to `src/config/index.ts`
- [ ] Add `RATE_LIMIT_PREFIX` constant (`"rl:"`) to `src/redis.ts`
- [ ] Write unit tests in `tests/unit/config.test.ts` verifying defaults and env-var overrides

### Phase 2: Rate-Limiter Middleware

**Deliverable:** `src/middleware/rateLimiter.ts` is implemented and unit-tested with a mocked
Redis client; middleware correctly increments counters and returns 429 on breach.

- [ ] Create `src/middleware/rateLimiter.ts` — Express middleware using Redis INCR + EXPIRE
- [ ] Middleware sets `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `Retry-After` headers
- [ ] Write unit tests in `tests/unit/rateLimiter.test.ts` using a mock for the Redis client
- [ ] Test: first request returns 200 with correct headers; 101st request returns 429

### Phase 3: Mount and Integration Tests

**Deliverable:** Rate limiting is active on all routes; integration tests demonstrate
the limit end-to-end against a real (test) Redis instance.

- [ ] Mount `rateLimiter` middleware in `src/app.ts` before route registration
- [ ] Add `RATE_LIMIT_MAX=3` override to test environment setup in `tests/setup.ts`
- [ ] Write integration test in `tests/integration/rateLimit.test.ts`: fire 4 requests, assert first 3 return status of underlying route, 4th returns 429
- [ ] Verify `Retry-After` header value matches configured window

## Validation

- [ ] Run `npm test` from project root — all existing tests pass, new tests pass (no regressions)
- [ ] Start server locally (`npm run dev`) and run `for i in $(seq 1 5); do curl -s -o /dev/null -w "%{http_code}\n" http://localhost:3000/api/health; done` with `RATE_LIMIT_MAX=4` in `.env.local` — first outputs `200`, last outputs `429`
- [ ] Check response headers on the 429: `Retry-After` header is present and numeric

## Progress

- [x] (2025-10-01 09:00Z) Created PLAN.md
- [x] (2025-10-01 09:15Z) Phase 1: Added config vars and RATE_LIMIT_PREFIX constant
- [x] (2025-10-01 09:30Z) Phase 1: Unit tests written and passing
- [x] (2025-10-01 10:00Z) Phase 2: rateLimiter.ts implemented
- [x] (2025-10-01 10:45Z) Phase 2: Unit tests passing (mocked Redis)
- [x] (2025-10-01 11:30Z) Phase 3: Middleware mounted; integration tests passing
- [x] (2025-10-01 11:45Z) All validation criteria verified manually

## Decisions

- Decision: Used Redis INCR + EXPIRE instead of a sliding window / Rationale: Fixed window is
  simpler and sufficient for the current traffic patterns; sliding window adds complexity without
  clear benefit at this scale / Date: 2025-10-01
- Decision: Applied rate limit globally (all routes) rather than per-route config / Rationale:
  Per-route config is out of scope per constraints; global is the simplest correct starting point /
  Date: 2025-10-01

## Notes

- Discovered that `redis.ts` did not export the client type — added `export type RedisClient`
  to allow proper mocking in unit tests. Small change, low risk.
- Evidence: `npm test` output — 47 tests passed, 0 failed after adding the type export.
