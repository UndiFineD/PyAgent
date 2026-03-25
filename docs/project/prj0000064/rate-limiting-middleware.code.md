# rate-limiting-middleware — Code Notes

_Owner: @6code | Status: DONE_

## Files changed

- `backend/rate_limiter.py` — NEW
- `backend/app.py` — add `RateLimitMiddleware` import + `app.add_middleware` call

## Key implementation notes

- `TokenBucket.consume()` is async and uses `asyncio.Lock` — safe under FastAPI's async event loop.
- Bucket map keyed by client IP string; each IP gets its own bucket on first request.
- Window reset: when `time.monotonic() - last_refill >= window`, tokens are reset to `rate`.
- `EXEMPT_PATHS = {"/health"}` — no token consumed for these.
- `X-Forwarded-For` checked first for proxy-aware IP extraction; falls back to `request.client.host`.
