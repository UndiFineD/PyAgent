# rate-limiting-middleware — Design

_Owner: @3design | Status: DONE_

## Selected Design: In-Process Token Bucket Middleware

### `backend/rate_limiter.py`

```python
class TokenBucket:
    """Per-client sliding-window token bucket."""
    def __init__(self, rate: int, window: float): ...
    async def consume(self) -> bool: ...  # True = allowed, False = rate limited

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Starlette middleware wrapping every request through a per-IP token bucket.
    Exempt paths: /health
    On limit: 429 + Retry-After header
    """
```

### Configuration

| Env var | Default | Meaning |
|---|---|---|
| `RATE_LIMIT_REQUESTS` | `60` | Tokens per window |
| `RATE_LIMIT_WINDOW` | `60` | Window size in seconds |

### Response on limit

```
HTTP/1.1 429 Too Many Requests
Retry-After: 60
Content-Type: application/json
{"detail": "Rate limit exceeded. Try again in 60 seconds."}
```

### Ordering

Middleware chain (outermost to innermost):
1. `CORSMiddleware`
2. `RateLimitMiddleware` ← new
3. Route handlers + auth dependency
