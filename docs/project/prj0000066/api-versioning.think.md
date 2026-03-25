# api-versioning — Think

_Owner: @2think_

## Problem

All existing endpoints are registered at `/api/<resource>`. Any breaking change would immediately affect all clients. Adding versioning now (at low complexity) provides isolation for future changes.

## Constraints

- Budget S — minimal code change, no new framework
- Must not break existing tests (they use `/api/` paths)
- FastAPI supports `include_router(prefix=...)` natively

## Options considered

| Option | Pros | Cons |
|---|---|---|
| APIRouter prefix `/api/v1/` | Native FastAPI, zero new deps | Need to handle `/api/` aliases |
| URL param `?version=1` | No path changes | Non-standard, hard to route |
| `Accept` header versioning | Clean semantics | Complex middleware, hard to test |
| Sub-application mounting | Full isolation | Over-engineering for P3/S |

## Selected direction

**Add `/api/v1/` prefix via a second `include_router` call.**

- Keep existing `_auth_router` routes registered at `/api/` for backwards compatibility
- Also register same router at `/api/v1/` as the versioned namespace
- Add `Deprecation: true` response header to the unversioned `/api/` variants via middleware or per-endpoint (middleware chosen for zero duplication)
- Default API version in OpenAPI docs set to `/api/v1/`

## Decision

Use a lightweight `DeprecationMiddleware` that adds `Deprecation: true` + `Link: </api/v1/...>; rel="successor-version"` header to any `/api/` response that has a `/api/v1/` counterpart.
