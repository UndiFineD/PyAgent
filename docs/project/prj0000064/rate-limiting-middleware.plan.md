# rate-limiting-middleware — Plan

_Owner: @4plan | Status: DONE_

## Tasks

1. Create `backend/rate_limiter.py`: `TokenBucket` + `RateLimitMiddleware`.
2. Update `backend/app.py`: add `RateLimitMiddleware` after `CORSMiddleware`.
3. Create `tests/test_rate_limiting.py`: 6 tests.
4. Update `data/projects.json` + `docs/project/kanban.md`.

## Acceptance criteria

- `GET /health` always returns 200 regardless of rate.
- After N requests in window, next request returns 429 with `Retry-After` header.
- Client IP isolated — one IP's bucket doesn't affect another.
- All 6 tests pass.
- No new pip dependencies.
