# jwt-refresh-token-support - Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-04-04_

## Root Cause Analysis
- The current backend authentication layer solved request validation only. It does not own token lifecycle management.
- `backend/auth.py` validates API keys and stateless HS256 bearer JWTs, but it exposes no token issuance, refresh, logout, revocation, rotation, session binding, or token-family handling.
- `backend/app.py` wires `require_auth` onto protected REST routers and `websocket_auth` onto `/ws`, but there is no `/auth/login`, `/auth/session`, `/auth/refresh`, or `/auth/logout` route family.
- `backend/session_manager.py` creates transport-local WebSocket session IDs only. Those IDs are unrelated to JWT claims and provide no reusable server-side auth session record.
- `tests/test_backend_auth.py` mints JWTs directly with `jwt.encode(...)`, which confirms the backend currently expects externally created access tokens rather than issuing its own.
- Persistence patterns exist, but not for auth sessions: `backend/memory_store.py` is JSON-file-backed per-agent memory, while `backend/automem_benchmark_store.py` is optional PostgreSQL storage for benchmark data only.
- Result: refresh token support is absent rather than framework-blocked. The real phase-one design work is defining an initial issuance/bootstrap contract and a server-side session record that can support secure rotation.

Policy gate check:
- `docs/project/code_of_conduct.md`: no policy conflict for this discovery scope.
- `docs/project/naming_standards.md`: proposed file/module naming can remain snake_case-compatible.

Branch gate check:
- Expected branch from project overview: `prj0000122-jwt-refresh-token-support`.
- Observed branch: `prj0000122-jwt-refresh-token-support`.
- Result: PASS.

## Current-State Evidence
- `backend/auth.py`
	- `verify_jwt()` only calls `jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])` and returns the payload or `None`.
	- No claim policy beyond PyJWT default expiration handling: no `typ`, `jti`, `sid`, `iss`, `aud`, token family, or revocation check.
	- Module configuration is read once at import time from `PYAGENT_API_KEY` and `PYAGENT_JWT_SECRET`, which keeps auth simple but means refresh/session state is not modeled anywhere.
- `backend/app.py`
	- Protected endpoints are grouped under `_auth_router = APIRouter(dependencies=[Depends(require_auth)])` and mounted under `/api`, `/api/v1`, and `/v1/api`.
	- The WebSocket endpoint calls `await websocket.accept()` and then `websocket_auth(websocket)`, which reads `?api_key=` or `?token=` query parameters and closes with `4401` on failure.
	- There is no auth bootstrap or refresh route; all JWT usage is consumption-only.
- `backend/session_manager.py`
	- Maintains a simple in-memory `dict[str, WebSocket]` keyed by random UUIDs returned from `connect()`.
	- No subject binding, no expiry, no rotation state, no persistence, and no revocation behavior.
- `tests/test_backend_auth.py`
	- Verifies access with API keys or externally minted JWTs.
	- Does not test refresh endpoints, token rotation, logout, replay rejection, or revocation.
- `tests/test_backend_worker.py`
	- Opens `/ws` without credentials, relying on current dev-mode behavior.
	- Phase one must preserve this developer path or make test/bootstrap behavior explicit.
- Persistence options already present in-repo
	- `backend/memory_store.py` demonstrates lightweight JSON-file persistence with per-key locks.
	- `backend/automem_benchmark_store.py` demonstrates optional Postgres-backed persistence, but that storage is benchmark-specific and not a reusable auth subsystem yet.

## Research Coverage
Task types covered across options:
- Literature review
- Alternative enumeration
- Prior-art search
- Constraint mapping
- Stakeholder impact
- Risk enumeration

Core evidence references:
- `backend/auth.py`
- `backend/app.py`
- `backend/session_manager.py`
- `backend/memory_store.py`
- `backend/automem_benchmark_store.py`
- `tests/test_backend_auth.py`
- `tests/test_backend_worker.py`
- `docs/project/archive/prj0000054/backend-authentication.design.md`
- `docs/project/archive/prj0000054/backend-authentication.think.md`
- `docs/project/archive/prj0000087-n8n-workflow-bridge/n8n-workflow-bridge.think.md`
- `docs/project/archive/prj0000098-backend-health-check-endpoint/prj0000098-backend-health-check-endpoint.think.md`
- `https://docs.python.org/3/library/secrets.html`
- `https://github.com/jpadilla/pyjwt/blob/master/README.rst`

## Constraints and Stakeholder Impact
### Constraints
- There is no user directory, password flow, or identity provider integration in the current backend. A phase-one design must define how the backend obtains an authenticated subject before it can mint refresh tokens.
- Existing production auth supports two inputs only: static API key or externally signed JWT. Any design that issues refresh tokens must either extend that trust model or replace one path explicitly.
- WebSocket auth happens at handshake/query-param time only. Mid-connection refresh is not part of the current transport contract.
- Dev mode is intentional and heavily exercised by tests. Tightening defaults without a test/bootstrap strategy will create broad regression risk.
- The repo currently has no general-purpose auth/session database. The realistic in-repo starting points are a new file-backed store patterned after `backend/memory_store.py` or a newly introduced durable store.
- Project scope is backend JWT refresh/session security, not a broad IAM platform or third-party SSO rollout.

### Stakeholder Impact
- Backend REST clients: would gain short-lived access JWTs and explicit refresh/logout semantics.
- WebSocket clients: would likely keep access-token-only handshake auth, but need compatibility rules when access tokens become short-lived.
- Test suite owners: `tests/test_backend_auth.py` and `tests/test_backend_worker.py` are directly affected; additional protected endpoint tests may need fixture updates if bootstrap behavior changes.
- Operators/security: gain revocation and rotation leverage, but only if persistence and audit visibility are explicit.
- Future design agent (`@3design`): must choose subject bootstrap and persistence durability early because those decisions drive every downstream API and test contract.

## Options
### Option A - Backend-owned session store with opaque rotating refresh tokens
Approach:
- Add first-party auth session endpoints in the backend for a minimal machine-oriented bootstrap flow.
- Issue short-lived access JWTs and long-lived opaque refresh tokens.
- Store hashed refresh-token records server-side with session metadata (`subject`, `session_id`, `token_family_id`, `expires_at`, `rotated_at`, `revoked_at`).
- Rotate the refresh token on every successful refresh and immediately invalidate the previous refresh token.
- Keep WebSocket auth on access JWT at handshake only for phase one; do not add mid-socket refresh yet.
- Prefer a dedicated store module with a file-backed default patterned after `backend/memory_store.py`, unless durability requirements force SQLite/Postgres in design.

Task-type evidence:
- Literature review: current auth/router structure in `backend/auth.py` and `backend/app.py` supports additive auth endpoints without replacing the framework.
- Prior art: `docs/project/archive/prj0000054/backend-authentication.design.md` and `.think.md` show the backend deliberately centralized auth logic in `backend/auth.py` for extension.
- Constraint mapping: there is no existing auth persistence or identity system, so the first slice must define both.
- Stakeholder impact: contains blast radius mostly to backend auth routes/tests instead of all protected endpoints.
- Risk enumeration: supports replay detection and explicit revocation, which stateless designs cannot do well.

SWOT:
- Strengths: strongest security posture inside current repo boundaries; enables true rotation/revocation; matches backend-owned goal.
- Weaknesses: introduces new server-side state and bootstrap contract.
- Opportunities: creates a clean seam for later audit logging, session introspection, and stronger claim validation.
- Threats: weak persistence/durability choices could undercut security claims if multiple processes or restarts are expected.

Security risks and testability mapping:
| Risk | Likelihood | Impact | Mitigation | Validation signal |
|---|---|---|---|---|
| Stolen refresh token replay before rotation is recorded | M | H | Hash stored refresh tokens, rotate on use, invalidate previous token immediately | Contract test: second use of prior refresh token returns unauthorized/revoked |
| File-backed store corruption or race conditions invalidate session state | M | M | Single-writer/lock discipline and atomic write strategy in dedicated store module | Concurrency/unit tests around rotate + revoke + restart recovery |
| Access JWT accepted after session revocation | M | H | Embed `sid`/`jti` and check session status on sensitive flows or keep access TTL aggressively short | Revocation test asserting refresh denied and subsequent protected call fails after expiry window |

Rollback:
- Remove new auth-session routes/store and revert to current validation-only JWT/API-key behavior.

### Option B - Stateless dual-JWT model (refresh token is also a JWT)
Approach:
- Add auth endpoints that issue both access and refresh tokens as signed JWTs.
- Distinguish token purpose by claim (`typ=access` / `typ=refresh`) and expiration windows.
- Avoid server-side session persistence except for optional process-local denylist logic.

Task-type evidence:
- Literature review: current `verify_jwt()` is already stateless and would be easiest to extend mechanically.
- Alternative enumeration: minimal-code path if repo optimizes for speed over security depth.
- Constraint mapping: no current session store means this option avoids introducing one.
- Risk enumeration: inability to enforce single-use refresh rotation is the central weakness.

SWOT:
- Strengths: smallest code footprint and least new infrastructure.
- Weaknesses: weak revocation story; rotation is mostly ceremonial without persistent token-family state.
- Opportunities: easy migration path if backend later delegates auth to an external issuer.
- Threats: refresh-token theft becomes hard to contain because the server has little or no memory of token lineage.

Security risks and testability mapping:
| Risk | Likelihood | Impact | Mitigation | Validation signal |
|---|---|---|---|---|
| Replayed refresh JWT remains valid until expiry | H | H | Reduce refresh TTL and optionally add denylist, but this weakly addresses replay | Replay test will demonstrate inability to reject previously used refresh tokens without extra state |
| Secret compromise invalidates trust for both access and refresh tokens | M | H | Separate secrets and secret-rotation policy | Unit tests for secret separation; operational rotation drill |
| Per-session logout/revocation is ineffective | H | M | Add blacklist state, which erodes the “stateless” premise | Revocation test either fails or forces stateful exception path |

Rollback:
- Revert new issuance endpoints and claims policy, returning to validator-only JWT support.

### Option C - External issuer / gateway owns refresh lifecycle
Approach:
- Keep the backend as a JWT/API-key validator only.
- Define stronger access-token claim requirements (`iss`, `aud`, `typ`, `sid`) and move refresh/login responsibilities to an external auth gateway or upstream service.
- Phase-one backend work becomes validation hardening and documentation, not first-party refresh-token issuance.

Task-type evidence:
- Prior-art search: current backend already consumes externally minted JWTs in tests and has no local identity model.
- Constraint mapping: avoids introducing a local auth database or bootstrap flow.
- Stakeholder impact: pushes operational/auth burden outside this repository.
- Risk enumeration: depends on infrastructure the project brief does not currently define.

SWOT:
- Strengths: lowest in-repo auth complexity; scales better if a real identity provider already exists.
- Weaknesses: does not actually deliver backend-owned refresh support.
- Opportunities: good long-term fit if PyAgent is later fronted by a dedicated auth service.
- Threats: immediate project goal slips because success depends on unavailable upstream infrastructure.

Security risks and testability mapping:
| Risk | Likelihood | Impact | Mitigation | Validation signal |
|---|---|---|---|---|
| Claim contract mismatch between gateway and backend causes widespread auth failures | M | H | Explicit issuer/audience/claim contract and contract tests | Integration tests with representative gateway-minted tokens |
| External refresh outage blocks session renewal while backend remains healthy | M | M | Retry/backoff and graceful error contract | End-to-end failure-mode tests against mocked gateway responses |
| Project delivers validation hardening only, leaving refresh-token gap unresolved | H | H | Re-scope project or explicitly defer backend-owned refresh support | Acceptance criteria review will show goal mismatch |

Rollback:
- No major rollback needed in backend code, but the project would effectively defer the core feature.

## Decision Matrix
| Criterion | Option A | Option B | Option C |
|---|---|---|---|
| Backend-owned refresh support | High | Medium | Low |
| Session rotation / revocation fidelity | High | Low | Medium |
| Delivery speed | Medium | High | Low |
| New infrastructure required | Medium | Low | High |
| Fit with current repo capabilities | High | Medium | Low |
| Security posture improvement | High | Medium-Low | Medium |
| Fit for phase-one scope | High | Medium | Low |

## Recommendation
**Selected: Option A - Backend-owned session store with opaque rotating refresh tokens.**

Why this option:
- It is the only option that materially improves security posture while still satisfying the project goal of backend JWT refresh support.
- It fits the existing architecture extension seam created in `prj0000054`: auth logic is already isolated in `backend/auth.py`, and additive route/store work can stay bounded to the backend surface.
- It gives `@3design` a realistic phase-one boundary: short-lived access JWTs, opaque single-use refresh tokens, server-side session records, and WebSocket compatibility via access-token-only handshake.
- It aligns with repository reality: there is no current auth database, so a dedicated session store must be introduced deliberately rather than hidden inside stateless JWT logic.

Recommended phase-one boundary for `@3design`:
1. Add a minimal backend bootstrap/session endpoint that exchanges an already trusted backend credential for an auth session.
2. Issue short-lived access JWTs containing `sub`, `sid`, `jti`, `iat`, `exp`, and `typ=access`.
3. Issue opaque refresh tokens generated with cryptographically secure randomness and store only hashed refresh-token material server-side.
4. Rotate refresh tokens on every refresh; revoke the old token immediately.
5. Keep WebSocket authentication on access JWT only during the opening handshake.
6. Defer cross-process auth scaling and mid-connection WebSocket refresh unless phase-one durability requirements force them.

Prior-art references supporting recommendation:
- `docs/project/archive/prj0000054/backend-authentication.design.md`
- `docs/project/archive/prj0000054/backend-authentication.think.md`
- `docs/project/archive/prj0000087-n8n-workflow-bridge/n8n-workflow-bridge.think.md`
- `docs/project/archive/prj0000098-backend-health-check-endpoint/prj0000098-backend-health-check-endpoint.think.md`

## Likely Phase-One File Scope
### Files to modify
| File | Purpose | Why it is likely in scope |
|---|---|---|
| `backend/auth.py` | Auth helpers and claim validation | Current home of JWT/API-key logic; natural place for access/refresh helpers |
| `backend/app.py` | Route wiring | Will need session/bootstrap/refresh/logout endpoints and protected-route integration |
| `backend/session_manager.py` | WebSocket session binding (conditional) | Only if design ties WS transport sessions to auth session IDs |
| `tests/test_backend_auth.py` | REST auth coverage | Existing auth contract tests should expand to issuance/refresh/revocation coverage |
| `tests/test_backend_worker.py` | WebSocket auth compatibility | Existing WS handshake tests must remain valid when access tokens become short-lived |

### Likely new files
| File | Purpose |
|---|---|
| `backend/auth_session_store.py` or similar | Persist refresh-session metadata and token-family rotation state |
| `tests/test_backend_refresh_sessions.py` or similar | Focused rotation/replay/logout contract tests |

### Reference patterns
| File | Pattern |
|---|---|
| `backend/memory_store.py` | File-backed async persistence with per-key locking |
| `docs/project/archive/prj0000054/backend-authentication.design.md` | Current backend auth extension seam |

## Open Questions
1. What is the phase-one bootstrap credential flow for obtaining the initial auth session: API-key exchange, service principal secret, or another machine-identity contract?
2. Must refresh-session state survive process restarts and multi-instance deployments in phase one, or is single-process persistence acceptable for the first slice?
