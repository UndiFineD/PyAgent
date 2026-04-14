# jwt-refresh-token-support - Design

_Status: DONE_
_Designer: @3design | Updated: 2026-04-04_

## Selected Option
Option A: backend-managed refresh sessions with API-key bootstrap, opaque rotating refresh tokens, and short-lived access JWTs.

This design keeps phase one intentionally narrow and implementation-ready:
- the backend gains one first-party session family for clients that already hold the existing shared API key.
- the backend issues its own short-lived access JWTs and rotates opaque refresh tokens on every successful refresh.
- refresh-session state is persisted in a dedicated file-backed store so restart recovery works without introducing a database migration in phase one.
- existing direct API-key and externally minted JWT authentication paths remain intact for backward compatibility.

## Problem Statement and Goals
The current backend can validate API keys and externally minted JWTs, but it cannot create, rotate, revoke, or persist auth sessions. The design goal is to add a backend-owned refresh-token path without expanding this project into a full identity platform.

Phase-one goals:
- add a deterministic bootstrap flow for creating a managed auth session
- persist refresh-session state across process restarts in the current single-node deployment model
- issue short-lived backend JWT access tokens with explicit claim contracts
- issue opaque single-use refresh tokens and rotate them on each refresh
- keep WebSocket behavior compatible with the current access-token-at-handshake model
- keep the design small enough for @4plan to decompose into one bounded backend slice

## Architecture
### High-Level Flow
1. A client calls `POST /v1/auth/session` with `X-API-Key`.
2. The backend validates the API key using the existing trust model and creates a new auth session record with a server-generated `session_id` and `token_family_id`.
3. The backend issues:
	- an access JWT signed with `PYAGENT_JWT_SECRET`
	- an opaque refresh token generated with cryptographically secure randomness
4. The backend stores only the hash of the refresh token plus session metadata in a dedicated file-backed session store.
5. Protected HTTP routes continue to accept API key or JWT. Backend-issued access JWTs use the existing bearer path with stricter claim requirements.
6. The client calls `POST /v1/auth/refresh` with the refresh token. The backend validates the stored hash, rotates the refresh token, updates the record atomically, and returns a new access JWT plus new refresh token.
7. The client can call `POST /v1/auth/logout` with the refresh token to revoke the session family. After logout, refresh attempts fail immediately. Already-issued access JWTs remain valid only until their short TTL expires.

### Bootstrap and Subject Model
Phase-one bootstrap is resolved as API-key exchange only.

Rationale:
- the repository already has a trusted machine credential: `PYAGENT_API_KEY`
- there is no user directory, password flow, or service-principal registry to support a richer subject bootstrap safely in this project
- binding the first refresh-session slice to the API-key path keeps implementation bounded and testable

Phase-one principal mapping:
- API-key bootstrap creates a machine subject with the fixed subject value `service:api_key`
- the subject is intentionally coarse in phase one; uniqueness is provided by `session_id`, not by a new identity layer
- exchanging externally minted JWTs for backend-managed refresh sessions is deferred to a follow-on project

### Persistence Decision
Phase-one session state is resolved as file-backed JSON persistence, not in-memory and not database-backed.

Chosen persistence contract:
- store path default: `data/auth/refresh_sessions.json`
- optional override: `PYAGENT_AUTH_SESSION_STORE_PATH`
- concurrency model: single-process async lock around store mutations
- durability model: whole-file read/modify/write with atomic replace semantics

Why this is the right phase-one choice:
- in-memory state would lose logout and replay protection on restart, which is too weak for refresh-token support
- SQLite or Postgres would introduce new infrastructure and migration scope that the current project brief does not justify
- a dedicated file-backed store matches existing repository patterns and preserves restart recovery in the current deployment shape

Explicit limitation:
- this persistence model is single-instance only; multi-process or multi-node deployment is out of scope for phase one

### Session Record Shape
Each persisted session record must contain enough information to support rotation, replay rejection, expiry, and revocation.

Minimum record fields:
- `session_id`
- `subject`
- `token_family_id`
- `current_refresh_token_hash`
- `current_refresh_token_jti`
- `created_at`
- `last_rotated_at`
- `access_expires_in_seconds`
- `refresh_expires_at`
- `revoked_at`
- `revocation_reason`

### Token Contracts
Access JWT contract:
- signing secret: `PYAGENT_JWT_SECRET`
- algorithm: `HS256`
- default TTL: 900 seconds
- required claims: `sub`, `sid`, `jti`, `iat`, `exp`, `typ`
- `typ` value: `access`

Refresh-token contract:
- opaque value only; not a JWT
- generated with `secrets.token_urlsafe(...)`
- default TTL: 604800 seconds
- only the token hash is persisted server-side
- every successful refresh invalidates the previously active refresh token immediately

### Compatibility Rules
HTTP compatibility:
- existing `X-API-Key` access to protected routes remains unchanged
- existing direct bearer JWT validation remains available for already-integrated callers
- backend-managed access JWTs use the same bearer header path as legacy JWT callers

WebSocket compatibility:
- `/ws` keeps its current handshake behavior
- clients can continue to connect using API key, dev mode, or access JWT query parameters
- backend-managed access JWTs are accepted at handshake through the existing JWT path
- no mid-connection refresh or re-authentication is added in phase one
- a WebSocket authenticated before access-token expiry is allowed to continue until disconnect, matching current transport behavior

### Component Responsibilities
| Component | Responsibility | Phase-one rule |
|---|---|---|
| `backend/auth.py` | issue/verify backend access JWTs, validate bootstrap credentials, define auth helpers | remains the auth logic entrypoint |
| `backend/auth_session_store.py` | persist refresh-session metadata, rotation state, and revocation | new file-backed store, single-process only |
| `backend/app.py` | expose session/bootstrap/refresh/logout routes and wire dependencies | additive route family only |
| `tests/test_backend_auth.py` | preserve current auth-path compatibility | existing API-key and direct-JWT behavior must stay green |
| `tests/test_backend_refresh_sessions.py` | validate bootstrap, refresh, replay rejection, logout, and restart recovery | new focused auth-session contract tests |
| `tests/test_backend_worker.py` | preserve current WebSocket handshake behavior | no mid-socket refresh introduced |

## API Contracts
### `POST /v1/auth/session`
Purpose:
- bootstrap a backend-managed auth session from the existing shared API key

Request:
- header: `X-API-Key: <key>`
- body: empty in phase one

Success response `200`:
- `access_token`
- `token_type` = `Bearer`
- `expires_in`
- `refresh_token`
- `refresh_expires_in`
- `session_id`
- `subject`

Failure modes:
- `401` when API key is missing or invalid
- `503` only if the session store cannot persist the new session

### `POST /v1/auth/refresh`
Purpose:
- exchange one active refresh token for a new access JWT and a new refresh token

Request body:
- `refresh_token`

Success response `200`:
- `access_token`
- `token_type` = `Bearer`
- `expires_in`
- `refresh_token`
- `refresh_expires_in`
- `session_id`
- `subject`

Failure modes:
- `401` for missing, expired, revoked, or replayed refresh token
- `409` is not used in phase one; replay and revoked states are normalized to `401` to keep the client contract small

### `POST /v1/auth/logout`
Purpose:
- revoke the current refresh-session family

Request body:
- `refresh_token`

Success response `200`:
- `status` = `revoked`
- `session_id`

Failure modes:
- `401` when the token is missing, unknown, expired, or already revoked

## Interfaces & Contracts
| Interface ID | Contract | Planned implementation anchor |
|---|---|---|
| `IFACE-JRT-001` | `POST /v1/auth/session` accepts only `X-API-Key` bootstrap in phase one and returns a backend-managed token pair. | `PT-JRT-001` |
| `IFACE-JRT-002` | backend-issued access JWTs always contain `sub`, `sid`, `jti`, `iat`, `exp`, and `typ=access`. | `PT-JRT-002` |
| `IFACE-JRT-003` | refresh tokens are opaque, single-use, server-hashed values and never stored in plaintext. | `PT-JRT-002`, `PT-JRT-003` |
| `IFACE-JRT-004` | refresh-session persistence uses a dedicated file-backed store at `data/auth/refresh_sessions.json` with atomic replace writes and single-process locking. | `PT-JRT-003` |
| `IFACE-JRT-005` | `POST /v1/auth/refresh` rotates the refresh token atomically and invalidates the prior token immediately. | `PT-JRT-004` |
| `IFACE-JRT-006` | `POST /v1/auth/logout` revokes the session family so subsequent refresh attempts fail immediately. | `PT-JRT-004` |
| `IFACE-JRT-007` | protected HTTP routes retain legacy API-key and direct-JWT compatibility while accepting backend-issued access JWTs through the existing bearer path. | `PT-JRT-002`, `PT-JRT-005` |
| `IFACE-JRT-008` | `/ws` remains handshake-only for auth; backend-issued access JWTs are accepted, and no mid-connection refresh is added. | `PT-JRT-005`, `PT-JRT-006` |
| `IFACE-JRT-009` | revocation does not require store lookup on every protected HTTP request; already-issued access JWTs expire naturally within the short TTL window. | `PT-JRT-002`, `PT-JRT-004` |

## Acceptance Criteria
| AC ID | Requirement | Verification signal | Interface linkage |
|---|---|---|---|
| `AC-JRT-001` | The backend exposes a phase-one bootstrap endpoint that creates a refresh-managed session from the existing shared API key. | `POST /v1/auth/session` returns `200` with token pair and session metadata for a valid API key and `401` for an invalid one. | `IFACE-JRT-001` |
| `AC-JRT-002` | Backend-issued access tokens follow one explicit claim contract and short TTL policy. | Focused tests verify `typ=access`, required claims, signature validity, and expiration behavior. | `IFACE-JRT-002`, `IFACE-JRT-007`, `IFACE-JRT-009` |
| `AC-JRT-003` | Refresh tokens are opaque, server-hashed, and single-use. | Store tests verify no plaintext refresh token is persisted and prior tokens are rejected after rotation. | `IFACE-JRT-003`, `IFACE-JRT-005` |
| `AC-JRT-004` | Refresh-session state survives a process restart in the current single-node deployment model. | Restart-oriented tests reload the store from disk and confirm an unrevoked refresh token still works after process reinitialization. | `IFACE-JRT-004` |
| `AC-JRT-005` | Replay and logout are enforced on the refresh path. | Second use of an already-rotated token returns `401`, and logout causes subsequent refresh to return `401`. | `IFACE-JRT-005`, `IFACE-JRT-006` |
| `AC-JRT-006` | Existing protected-route compatibility is preserved. | Existing `tests/test_backend_auth.py` scenarios for API key and direct JWT paths remain green after the new route family lands. | `IFACE-JRT-007` |
| `AC-JRT-007` | WebSocket authentication remains compatible with current behavior. | Existing `tests/test_backend_worker.py` WebSocket handshake scenarios remain green, and a focused test proves a backend-issued access JWT can authenticate at `/ws`. | `IFACE-JRT-008` |
| `AC-JRT-008` | Revoked sessions stop refreshing immediately, and HTTP access naturally ends within the configured access-token TTL window. | Contract tests prove refresh fails immediately after revocation and document that no per-request session-store check is required for active access JWTs. | `IFACE-JRT-006`, `IFACE-JRT-009` |
| `AC-JRT-009` | The design remains bounded and implementation-ready for downstream planning. | Canonical design includes resolved bootstrap/persistence decisions, interface contracts, AC table, file scope, non-goals, and ADR impact. | all |

## Interface-to-Task Traceability
This block defines the minimum implementation anchors that `@4plan` must refine into executable tasks.

| Planned task ID | Expected implementation focus | Interfaces covered |
|---|---|---|
| `PT-JRT-001` | add `POST /v1/auth/session` bootstrap route and response contract | `IFACE-JRT-001` |
| `PT-JRT-002` | extend auth helpers for backend-issued access JWT creation and validation contract | `IFACE-JRT-002`, `IFACE-JRT-003`, `IFACE-JRT-007`, `IFACE-JRT-009` |
| `PT-JRT-003` | add file-backed `backend/auth_session_store.py` with atomic persistence behavior | `IFACE-JRT-003`, `IFACE-JRT-004` |
| `PT-JRT-004` | add refresh rotation and logout revocation route behavior | `IFACE-JRT-005`, `IFACE-JRT-006`, `IFACE-JRT-009` |
| `PT-JRT-005` | preserve legacy protected-route behavior while accepting backend-issued access JWTs | `IFACE-JRT-007`, `IFACE-JRT-008` |
| `PT-JRT-006` | add focused WebSocket compatibility coverage for backend-issued access JWTs | `IFACE-JRT-008` |
| `PT-JRT-007` | add focused restart/replay/revocation tests and fixture support | `IFACE-JRT-003`, `IFACE-JRT-004`, `IFACE-JRT-005`, `IFACE-JRT-006` |

## Phase-One File Scope
### Files to modify
| File | Reason |
|---|---|
| `backend/auth.py` | add bootstrap helper logic, backend-issued access-token helpers, and stricter claim verification |
| `backend/app.py` | add `/v1/auth/session`, `/v1/auth/refresh`, and `/v1/auth/logout` routes |
| `tests/test_backend_auth.py` | preserve and extend existing auth compatibility coverage |
| `tests/test_backend_worker.py` | preserve WebSocket compatibility and add backend-issued access-JWT handshake coverage |

### New files
| File | Reason |
|---|---|
| `backend/auth_session_store.py` | dedicated file-backed refresh-session persistence and rotation logic |
| `tests/test_backend_refresh_sessions.py` | focused bootstrap, refresh, replay, logout, and restart-recovery tests |

### Runtime artifacts not committed to Git
| Path | Purpose |
|---|---|
| `data/auth/refresh_sessions.json` | file-backed refresh-session store |

### Explicitly out of phase-one file scope
| File | Why excluded |
|---|---|
| `backend/session_manager.py` | WebSocket transport session registry remains separate from auth-session persistence |
| `backend/models.py` | request/response models can stay local to `backend/app.py` in phase one to avoid unnecessary file spread |

## Non-Goals and Deferred Items
Excluded from phase one:
- password login, user registration, or human-user identity modeling
- API-key-derived per-client subject catalogs or client management UI
- exchanging externally minted JWTs for backend-managed refresh sessions
- per-request session-store lookups for every protected HTTP route
- multi-instance or distributed refresh-session persistence
- mid-connection WebSocket token refresh or forced disconnect-on-expiry
- session introspection or administrative session listing endpoints

Deferred follow-on items:
- SQLite or Postgres-backed auth session persistence for multi-instance deployments
- external JWT-to-session exchange
- richer subject mapping and audit trails for multiple client identities

## Non-Functional Requirements
- Performance: normal protected HTTP requests must remain bearer-signature-only in phase one; session-store I/O occurs only on bootstrap, refresh, and logout.
- Security: refresh tokens must be opaque, single-use, hashed at rest, and rejected after rotation or revocation.
- Reliability: auth-session state must survive process restart through the file-backed store in the current deployment shape.
- Testability: rotation, replay, logout, restart recovery, compatibility, and WebSocket handshake behavior must all be verifiable with deterministic focused pytest selectors.
- Maintainability: implementation stays bounded to one new backend store module, additive auth routes, and focused tests.

## Risks and Rollback
| Risk | Impact | Mitigation | Rollback trigger |
|---|---|---|---|
| file-backed store semantics are insufficient for actual deployment topology | high | explicitly scope phase one to single-instance deployments and document database persistence as deferred | operators confirm multi-instance auth state is required before implementation starts |
| short-lived access JWTs remain usable until expiry after logout | medium | keep access TTL short and make immediate revocation apply to refresh path only in phase one | security review rejects bounded-TTL revocation semantics for this backend |
| compatibility regressions in direct API-key or direct-JWT paths | high | preserve current route behavior and keep focused compatibility tests green | existing auth tests fail or downstream consumers require breaking contract changes |

Rollback posture:
- remove the additive session/refresh/logout routes and dedicated session store if the backend-managed refresh slice proves too large for the current project
- preserve the legacy API-key and direct-JWT validation paths regardless of rollback

## ADR Impact
This design introduces an architecture decision and requires ADR coverage.

- ADR file: `docs/architecture/adr/0008-backend-managed-refresh-sessions-for-jwt-renewal.md`
- ADR scope: phase-one bootstrap credential choice, backend-issued access JWT contract, opaque rotating refresh-token policy, and file-backed single-instance persistence boundary

## Blockers and Open Questions
No blocking open questions remain for phase-one planning.

Conditional blocker to carry forward explicitly:
- if deployment requirements now include multiple backend instances or shared auth state across processes, phase-one persistence must be re-scoped to SQLite or Postgres before implementation starts
