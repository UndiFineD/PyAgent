# ADR-0008 - Backend-Managed Refresh Sessions for JWT Renewal

## Status

- Accepted

## Date

- 2026-04-04

## Owners

- @3design
- Reviewers: @4plan, @8ql

## Context

The backend currently validates API keys and externally minted JWTs but does not create or manage auth sessions. Project `prj0000122-jwt-refresh-token-support` needs backend-owned refresh-token support with rotation and revocation, while staying inside a narrow first slice that fits the current repository and deployment model.

Two design-critical questions had to be resolved before planning could begin:
- how a client creates the initial managed session when there is no user directory or login subsystem
- whether refresh-session state should be in-memory, file-backed, or database-backed in phase one

The repository already trusts one machine credential, `PYAGENT_API_KEY`, and already contains lightweight file-backed persistence patterns. It does not contain an auth database, a user catalog, or a distributed session layer.

## Decision

Adopt a backend-managed refresh-session architecture for phase one with the following boundaries:
- `POST /v1/auth/session` uses `X-API-Key` bootstrap only.
- the backend issues short-lived access JWTs signed with `PYAGENT_JWT_SECRET`.
- the backend issues opaque refresh tokens, stores only their hashes, and rotates them on every successful refresh.
- refresh-session state is persisted in a dedicated file-backed JSON store at `data/auth/refresh_sessions.json` with single-process locking and atomic replace writes.
- logout and replay protection apply immediately to the refresh path.
- already-issued access JWTs are not back-checked against the session store on every protected request; they expire naturally within a short TTL window.
- existing direct API-key and direct bearer-JWT validation paths remain available for backward compatibility.

## Alternatives considered

### Alternative A - In-memory refresh-session store

- Summary: keep refresh-session state only in process memory.
- Why not chosen: restart would drop revocation and replay state, which makes refresh-token support too weak even for phase one.

### Alternative B - Stateless refresh JWTs

- Summary: use a second JWT as the refresh token and avoid server-side state.
- Why not chosen: single-use rotation, replay rejection, and targeted revocation are not credible without server-managed state.

### Alternative C - Database-backed session persistence in phase one

- Summary: introduce SQLite or Postgres for refresh-session storage immediately.
- Why not chosen: it expands infrastructure, migration, and operational scope beyond the narrow backend slice justified by this project.

## Consequences

### Positive

- The backend gains real refresh-token rotation and revocation semantics.
- Restart recovery works without requiring a database migration in phase one.
- The bootstrap problem is solved with an already-trusted credential instead of inventing a new login system.
- The project stays additive and compatible with existing API-key and direct-JWT consumers.

### Negative / Trade-offs

- The phase-one subject model is coarse and machine-oriented (`service:api_key`).
- The file-backed store is appropriate only for single-instance deployment.
- Logout does not instantly invalidate already-issued access JWTs; it stops refresh immediately and relies on short access-token TTL.
- Externally minted JWTs are not exchangeable for backend-managed refresh sessions in phase one.

## Implementation impact

- Affected components: `backend/auth.py`, `backend/app.py`, new `backend/auth_session_store.py`, `tests/test_backend_auth.py`, new `tests/test_backend_refresh_sessions.py`, and `tests/test_backend_worker.py`.
- Migration/rollout notes: add session store and auth routes first, keep legacy auth paths intact, then layer focused replay/restart/logout tests.
- Backward compatibility notes: protected HTTP and WebSocket flows continue to accept the existing API-key and direct-JWT paths.

## Validation and monitoring

- Tests or checks required: docs policy pytest selector, architecture governance validation, focused auth-session tests for bootstrap/rotation/logout/restart recovery, and compatibility coverage for protected HTTP and WebSocket paths.
- Runtime signals or metrics to monitor: auth-session creation failures, refresh rotation failures, and store write/read errors once implementation exists.
- Rollback triggers: confirmed multi-instance deployment requirement before implementation, unacceptable bounded-TTL revocation semantics, or compatibility breakage in current auth consumers.

## Related links

- Related project artifact(s): `docs/project/prj0000122-jwt-refresh-token-support/jwt-refresh-token-support.think.md`, `docs/project/prj0000122-jwt-refresh-token-support/jwt-refresh-token-support.design.md`
- Related architecture docs: `docs/architecture/adr/0001-architecture-decision-record-template.md`, `docs/project/archive/prj0000054/backend-authentication.design.md`
- Supersedes/Superseded-by (if any): none