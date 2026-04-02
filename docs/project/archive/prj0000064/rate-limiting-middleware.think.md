# rate-limiting-middleware — Think

_Owner: @2think | Status: DONE_

## Problem

All FastAPI endpoints are currently unthrottled. A misbehaving client or a denial-of-service attempt can saturate the backend.

## Options

1. **stdlib token-bucket in-process** — simple, no deps, effective for single-node deployments. Reset every window, configurable per-route rate.
2. **slowapi (limits library)** — production-grade, Redis-backed, but adds a dependency.
3. **NGINX/traefik rate limiting** — infrastructure-level, not under PyAgent control.

## Decision

Option 1: in-process token-bucket middleware using only stdlib (`time`, `collections`). Sufficient for single-node; can be replaced with slowapi later for multi-node.

## Key constraints

- `429 Too Many Requests` with `Retry-After` header on breach.
- `/health` is exempt (load-balancers must always reach it).
- Configurable via env vars: `RATE_LIMIT_REQUESTS` (default 60) and `RATE_LIMIT_WINDOW` (default 60 seconds).
- Thread-safe via `asyncio.Lock` per client IP.
