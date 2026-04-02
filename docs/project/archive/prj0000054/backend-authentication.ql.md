# backend-authentication — Security / QL Review

_Owner: @8ql | Status: CLEARED_

## OWASP Top 10 Review

### Cryptographic Failures (A02)
- `hmac.compare_digest` used for API key — timing-safe. Must not be changed to `==`.
- HS256 with PyJWT — standard algorithm. Secret must be ≥ 32 bytes in production.
- JWT secret read from env, never hardcoded.

### Identification and Authentication Failures (A07)
- `DEV_MODE`: when neither secret is set, all requests pass. This is intentional for
  backward compatibility. Production **must** set at least one env var.
- 401 detail message: generic string, does not reveal secret values or computed hashes.
- WebSocket closes with code 4401 on auth failure — no data leakage.

### Broken Access Control (A01)
- `/health` is deliberately unauthenticated — safe for load-balancers.
- All other REST endpoints protected via `APIRouter(dependencies=[Depends(require_auth)])`.
- No route bypasses the router.

### Security Misconfiguration (A05)
- Warning logged at module import when dev mode is active.
- `PYAGENT_API_KEY` and `PYAGENT_JWT_SECRET` documented as required for production.

### Injection (A03)
- No SQL, shell, or template injection surfaces introduced.
- JWT decode does not execute untrusted code.

## Checklist

- [x] `hmac.compare_digest` used for API key (timing-safe)
- [x] JWT secret from env, not hardcoded
- [x] 401 detail does not leak secret or hash
- [x] Warning logged in dev mode
- [x] No new injection surfaces
- [x] `/health` remains open (intentional)
- [x] WS closes with 4401 on failure (no data leakage)
