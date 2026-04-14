# jwt-refresh-token-support - Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-04-04_

## Overview
Deliver the phase-one backend-managed refresh-session slice defined by Option A, the design artifact, and ADR-0008 without expanding the backend into a broader identity platform. The plan keeps the work inside one bounded backend lane: a file-backed refresh-session store, additive auth routes, stricter backend-issued access-token claims, and focused compatibility coverage for protected HTTP routes and `/ws` handshake auth.

In scope for implementation:
1. `POST /v1/auth/session` bootstrap from `X-API-Key` only.
2. Opaque rotating refresh tokens with hash-at-rest persistence.
3. Short-lived backend-issued access JWTs with explicit claim requirements.
4. Additive `POST /v1/auth/refresh` and `POST /v1/auth/logout` routes.
5. Focused tests for rotation, replay rejection, logout, restart recovery, protected-route compatibility, and WebSocket JWT handshake compatibility.

Out of scope for implementation:
1. User/password login, human-user identity, or service-principal registry work.
2. Exchange of externally minted JWTs for managed refresh sessions.
3. Multi-instance or database-backed session persistence.
4. Mid-connection WebSocket refresh or per-request session-store lookups for active access JWTs.
5. Broader backend model refactors outside the auth/session surface.

## Branch Gate
- Project ID: prj0000122
- Expected branch: prj0000122-jwt-refresh-token-support
- Observed branch: prj0000122-jwt-refresh-token-support
- Result: PASS

## Scope Guardrails
- Planning-scope files updated in this step: this plan file, `docs/project/prj0000122-jwt-refresh-token-support/jwt-refresh-token-support.project.md`, `.github/agents/data/current.4plan.memory.md`, `.github/agents/data/history.4plan.memory.md`, and `.github/agents/data/2026-04-04.4plan.log.md`.
- Downstream implementation ownership is limited to `backend/auth.py`, `backend/app.py`, new `backend/auth_session_store.py`, `tests/test_backend_refresh_sessions.py`, `tests/test_backend_auth.py`, `tests/test_backend_worker.py`, and project handoff artifacts under `docs/project/prj0000122-jwt-refresh-token-support/`.
- `backend/session_manager.py` remains read-only in this slice unless `/ws` handshake proof shows a hard dependency on transport-session changes.
- `backend/models.py` remains out of scope unless route payload sprawl makes inline request/response models unmaintainable.
- If deployment requirements now require multi-process or multi-node shared auth state, stop and return to `@0master` because ADR-0008's file-backed persistence boundary no longer holds.

## Context Map
### Files to Modify
| File | Purpose | Planned change |
|---|---|---|
| `backend/auth.py` | Current API-key and JWT auth entrypoint | Add backend-issued access-token helpers and stricter managed-token claim validation while preserving legacy JWT/API-key acceptance |
| `backend/app.py` | FastAPI route surface and `/ws` endpoint | Add `/v1/auth/session`, `/v1/auth/refresh`, and `/v1/auth/logout` routes; wire the session store and managed-token flow |
| `tests/test_backend_auth.py` | Existing protected-route auth regression suite | Preserve current API-key/direct-JWT behavior and add managed access-token claim/compatibility assertions |
| `tests/test_backend_worker.py` | Existing `/ws` handshake coverage | Prove backend-issued access JWTs work at handshake without changing current dev-mode expectations |

### New Files
| File | Purpose |
|---|---|
| `backend/auth_session_store.py` | File-backed refresh-session persistence with single-process locking and atomic replace writes |
| `tests/test_backend_refresh_sessions.py` | Bootstrap, refresh, replay, logout, and restart-recovery contract tests |

### Dependencies (read-only or reference patterns)
| File | Relationship |
|---|---|
| `backend/memory_store.py` | Reference pattern for JSON persistence, path handling, and single-process locking |
| `backend/session_manager.py` | Confirms WebSocket transport sessions stay separate from auth-session persistence |
| `docs/architecture/adr/0008-backend-managed-refresh-sessions-for-jwt-renewal.md` | Architecture boundary for bootstrap, refresh rotation, and file-backed persistence |

### Test Files
| Test | Coverage |
|---|---|
| `tests/test_backend_refresh_sessions.py` | New red/green contract for bootstrap, rotation, replay rejection, logout, and restart recovery |
| `tests/test_backend_auth.py` | Legacy API-key/direct-JWT compatibility plus managed access-token claim contract |
| `tests/test_backend_worker.py` | `/ws` handshake compatibility with backend-issued access JWTs |

### Reference Patterns
| File | Pattern |
|---|---|
| `backend/memory_store.py` | Atomic JSON file persistence with in-process locking |
| `tests/test_backend_auth.py` | Existing monkeypatch-based auth contract tests |
| `tests/test_backend_worker.py` | Existing WebSocket handshake helpers and encrypted frame test flow |

### Risk Assessment
- Breaking changes to current API-key or direct-JWT callers are high impact and must be caught by focused compatibility selectors.
- Persistence drift is bounded to single-instance deployments only; do not silently broaden to multi-instance semantics.
- Logout only cuts off the refresh path immediately; short access-token TTL is part of the security contract and must remain explicit in tests and review notes.

## AC and Interface Traceability
| Task ID | AC Coverage | Interface Coverage |
|---|---|---|
| T-JRT-001 | AC-JRT-001, AC-JRT-003, AC-JRT-004, AC-JRT-005, AC-JRT-008 | IFACE-JRT-001, IFACE-JRT-003, IFACE-JRT-004, IFACE-JRT-005, IFACE-JRT-006, IFACE-JRT-009 |
| T-JRT-002 | AC-JRT-002, AC-JRT-006 | IFACE-JRT-002, IFACE-JRT-007, IFACE-JRT-009 |
| T-JRT-003 | AC-JRT-007 | IFACE-JRT-008 |
| T-JRT-004 | AC-JRT-001, AC-JRT-002, AC-JRT-003, AC-JRT-004, AC-JRT-005, AC-JRT-006, AC-JRT-007, AC-JRT-008 | IFACE-JRT-001, IFACE-JRT-002, IFACE-JRT-003, IFACE-JRT-004, IFACE-JRT-005, IFACE-JRT-006, IFACE-JRT-007, IFACE-JRT-008, IFACE-JRT-009 |
| T-JRT-005 | AC-JRT-003, AC-JRT-004, AC-JRT-005, AC-JRT-008 | IFACE-JRT-003, IFACE-JRT-004, IFACE-JRT-005, IFACE-JRT-006, IFACE-JRT-009 |
| T-JRT-006 | AC-JRT-001, AC-JRT-002, AC-JRT-005, AC-JRT-006, AC-JRT-007, AC-JRT-008 | IFACE-JRT-001, IFACE-JRT-002, IFACE-JRT-005, IFACE-JRT-006, IFACE-JRT-007, IFACE-JRT-008, IFACE-JRT-009 |
| T-JRT-007 | AC-JRT-001..AC-JRT-008 | IFACE-JRT-001..IFACE-JRT-009 |
| T-JRT-008 | AC-JRT-001..AC-JRT-008 | IFACE-JRT-001..IFACE-JRT-009 |
| T-JRT-009 | AC-JRT-001..AC-JRT-008 | IFACE-JRT-001..IFACE-JRT-009 |

## Chunking Strategy
- Chunk C1 (red contract + implementation lane): T-JRT-001..T-JRT-006.
	- Estimated implementation/test files: 6 (`backend/auth.py`, `backend/app.py`, `backend/auth_session_store.py`, `tests/test_backend_refresh_sessions.py`, `tests/test_backend_auth.py`, `tests/test_backend_worker.py`).
	- Estimated project handoff files: 2 (`jwt-refresh-token-support.test.md`, optional `jwt-refresh-token-support.code.md` evidence later in workflow).
- Chunk C2 (execution, quality, and git closure): T-JRT-007..T-JRT-009.
	- Estimated closure files: 3 (`jwt-refresh-token-support.exec.md`, `jwt-refresh-token-support.ql.md`, `jwt-refresh-token-support.git.md`).

## Task List
| Task ID | Parallel Class | Owner | Objective | Target Files | Acceptance Criteria | Validation Command |
|---|---|---|---|---|---|---|
| T-JRT-001 | parallel-safe | @5test | Author the failing-first refresh-session contract for bootstrap, refresh rotation, replay rejection, logout, and restart recovery using a temp file-backed store path. | `tests/test_backend_refresh_sessions.py`, `docs/project/prj0000122-jwt-refresh-token-support/jwt-refresh-token-support.test.md` | Valid API key returns a managed token pair; invalid API key returns `401`; rotated refresh token becomes unusable on second use; logout revokes the family; restart reloads the store and preserves one active session; persisted store never contains the plaintext refresh token. | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_backend_refresh_sessions.py` |
| T-JRT-002 | parallel-safe | @5test | Extend protected-route auth tests for the backend-issued access-token claim contract while preserving current API-key and direct-JWT compatibility. | `tests/test_backend_auth.py`, `docs/project/prj0000122-jwt-refresh-token-support/jwt-refresh-token-support.test.md` | Managed access-token tests assert required claims (`sub`, `sid`, `jti`, `iat`, `exp`, `typ=access`); existing API-key and legacy direct-JWT selectors stay in place and remain green after implementation. | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_backend_auth.py` |
| T-JRT-003 | parallel-safe | @5test | Add focused `/ws` handshake coverage proving a backend-issued access JWT authenticates through the existing query-parameter token path without introducing mid-connection refresh semantics. | `tests/test_backend_worker.py`, `docs/project/prj0000122-jwt-refresh-token-support/jwt-refresh-token-support.test.md` | `/ws` still supports current dev-mode flow; a managed access JWT is accepted at handshake; no test requires session-store access after the connection is established. | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_backend_worker.py` |
| T-JRT-004 | sequential-only (convergence) | @5test | Merge the parallel red work packages into one deterministic failing-first handoff packet for `@6code`. | `docs/project/prj0000122-jwt-refresh-token-support/jwt-refresh-token-support.test.md` | The test artifact records failing selectors for T-JRT-001..T-JRT-003, fixture strategy for temp session-store paths, and no file-ownership overlap remains unresolved before implementation starts. | `rg -n "T-JRT-001|T-JRT-002|T-JRT-003|failing-first|refresh_sessions" docs/project/prj0000122-jwt-refresh-token-support/jwt-refresh-token-support.test.md` |
| T-JRT-005 | sequential-only | @6code | Implement the dedicated file-backed refresh-session store with atomic replace writes, single-process locking, and hash-at-rest refresh-token storage. | `backend/auth_session_store.py` | The store persists `session_id`, `token_family_id`, hashed refresh-token state, timestamps, and revocation data; rotation invalidates prior tokens immediately; restart recovery works within the single-instance boundary from ADR-0008. | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_backend_refresh_sessions.py -k "bootstrap or refresh or logout or restart"` |
| T-JRT-006 | sequential-only | @6code | Add managed access-token helpers and additive auth routes while keeping legacy protected-route and `/ws` auth behavior intact. | `backend/auth.py`, `backend/app.py` | `/v1/auth/session`, `/v1/auth/refresh`, and `/v1/auth/logout` satisfy the response/failure contracts; managed access JWTs enforce the explicit claim contract; existing API-key/direct-JWT flows keep passing; `/ws` accepts managed access JWTs via the current handshake path only. | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_backend_refresh_sessions.py tests/test_backend_auth.py tests/test_backend_worker.py` |
| T-JRT-007 | sequential-only | @7exec | Run the focused auth-session convergence suite and record execution evidence against the approved file boundary. | `docs/project/prj0000122-jwt-refresh-token-support/jwt-refresh-token-support.exec.md` | Execution evidence captures the focused pytest selectors, any environment setup needed for backend auth tests, and the changed-file list for Chunk C1 only. | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_backend_refresh_sessions.py tests/test_backend_auth.py tests/test_backend_worker.py` |
| T-JRT-008 | sequential-only | @8ql | Review security and quality closure for token hashing, claim enforcement, replay protection, TTL-bounded revocation semantics, and persistence boundary adherence. | `docs/project/prj0000122-jwt-refresh-token-support/jwt-refresh-token-support.ql.md` | Quality review proves refresh tokens are opaque and hashed at rest, managed access JWTs enforce `typ=access` plus required claims, logout cuts off refresh immediately, and no multi-instance assumptions leaked into the implementation. | `rg -n "token_urlsafe|sha|hash|typ|sid|jti|refresh|revok|atomic" backend/auth.py backend/auth_session_store.py backend/app.py tests/test_backend_refresh_sessions.py` |
| T-JRT-009 | sequential-only | @9git | Complete the narrow git handoff with branch validation, scoped staging proof, and links back to this plan and ADR-0008. | `docs/project/prj0000122-jwt-refresh-token-support/jwt-refresh-token-support.git.md` | The git handoff records the expected branch, approved changed files, focused validation commands, and the first red-phase slice lineage from this plan to `jwt-refresh-token-support.test.md`. | `git status --short` |

## Parallelization and Sequencing
- Sequential hard constraints:
	1. T-JRT-001, T-JRT-002, and T-JRT-003 can start together because they own disjoint test files.
	2. T-JRT-004 is the required red-phase sync barrier and must complete before any implementation task starts.
	3. T-JRT-005 must complete before T-JRT-006 because the route/auth layer depends on the session-store contract.
	4. T-JRT-007 waits for T-JRT-006 completion and is the convergence barrier for the implementation lane.
	5. T-JRT-008 waits for T-JRT-007 evidence.
	6. T-JRT-009 waits for T-JRT-008 closure.
- Parallel-safe boundary:
	1. T-JRT-001 owns `tests/test_backend_refresh_sessions.py`.
	2. T-JRT-002 owns `tests/test_backend_auth.py`.
	3. T-JRT-003 owns `tests/test_backend_worker.py`.
	4. Shared updates to `jwt-refresh-token-support.test.md` are deferred to T-JRT-004 only.
- Convergence step:
	1. T-JRT-004 is the mandatory merge decision for the parallel red wave.
	2. `@5test` owns the merge decision and must reject the handoff if the three red packages introduce overlapping file ownership or broaden scope beyond the approved auth/session surfaces.

## File Ownership Map
| Work Package | Owner | Files |
|---|---|---|
| WP1 - Refresh-session red contract | @5test | `tests/test_backend_refresh_sessions.py`, `docs/project/prj0000122-jwt-refresh-token-support/jwt-refresh-token-support.test.md` |
| WP2 - Protected-route auth compatibility red contract | @5test | `tests/test_backend_auth.py` |
| WP3 - WebSocket handshake red contract | @5test | `tests/test_backend_worker.py` |
| WP4 - Red convergence packet | @5test | `docs/project/prj0000122-jwt-refresh-token-support/jwt-refresh-token-support.test.md` |
| WP5 - Session-store implementation | @6code | `backend/auth_session_store.py` |
| WP6 - Auth helper and route integration | @6code | `backend/auth.py`, `backend/app.py` |
| WP7 - Execution evidence | @7exec | `docs/project/prj0000122-jwt-refresh-token-support/jwt-refresh-token-support.exec.md` |
| WP8 - Quality closure | @8ql | `docs/project/prj0000122-jwt-refresh-token-support/jwt-refresh-token-support.ql.md` |
| WP9 - Git handoff | @9git | `docs/project/prj0000122-jwt-refresh-token-support/jwt-refresh-token-support.git.md` |

## Agent Validation Contracts and Evidence Expectations
### @5test Contract
- Deliverables:
	1. `tests/test_backend_refresh_sessions.py` as the primary red-phase contract file.
	2. Managed-token coverage added to `tests/test_backend_auth.py` and `tests/test_backend_worker.py`.
	3. `jwt-refresh-token-support.test.md` documenting failing selectors, fixture strategy, and task-to-AC coverage.
- Required evidence:
	1. One failing-first selector per red work package.
	2. Explicit temp-path strategy for `PYAGENT_AUTH_SESSION_STORE_PATH`.
	3. Proof that no red test introduces multi-instance or per-request session-store assumptions.

### @6code Contract
- Deliverables:
	1. New `backend/auth_session_store.py` with real persistence logic, not placeholders.
	2. Additive route/auth changes in `backend/auth.py` and `backend/app.py` only.
- Required evidence:
	1. Focused selector output for `tests/test_backend_refresh_sessions.py`.
	2. Compatibility selector output for `tests/test_backend_auth.py` and `tests/test_backend_worker.py`.
	3. Proof that plaintext refresh tokens are never written to disk.

### @7exec Contract
- Deliverables:
	1. `jwt-refresh-token-support.exec.md` with focused execution transcript.
- Required evidence:
	1. Focused pytest transcript for the three backend auth test files.
	2. Changed-file list limited to the approved implementation surface and project artifacts.
	3. Docs policy gate transcript after project-artifact updates.

### @8ql Contract
- Deliverables:
	1. `jwt-refresh-token-support.ql.md` with security/quality closure review.
- Required evidence:
	1. Token hashing and claim-contract audit.
	2. Replay/logout behavior audit tied to AC-JRT-005 and AC-JRT-008.
	3. Persistence-boundary audit tied to ADR-0008.

## Milestones
| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | Parallel red contracts authored | T-JRT-001, T-JRT-002, T-JRT-003 | PLANNED |
| M2 | Red convergence packet complete | T-JRT-004 | PLANNED |
| M3 | Session-store and route implementation complete | T-JRT-005, T-JRT-006 | PLANNED |
| M4 | Execution convergence complete | T-JRT-007 | PLANNED |
| M5 | Quality and git closure ready | T-JRT-008, T-JRT-009 | PLANNED |

## Blockers and Dependencies
- `PYAGENT_API_KEY` and `PYAGENT_JWT_SECRET` must remain monkeypatchable or fixture-controlled in tests so the red/green path stays deterministic.
- The implementation needs a new path override `PYAGENT_AUTH_SESSION_STORE_PATH`; if configuration strategy differs, stop and reconcile with the design before code lands.
- The store contract assumes one process owns writes. Any requirement for shared writes across processes is a blocker that invalidates the chosen persistence design.
- `/ws` already authenticates via query parameters after accept. Managed access JWT support must fit that path; changing transport auth semantics is out of scope.

## Validation Commands by Milestone
### M1
```powershell
& c:/Dev/PyAgent/.venv/Scripts/Activate.ps1
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_backend_refresh_sessions.py
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_backend_auth.py
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_backend_worker.py
```

### M2
```powershell
rg -n "T-JRT-001|T-JRT-002|T-JRT-003|failing-first|refresh_sessions" docs/project/prj0000122-jwt-refresh-token-support/jwt-refresh-token-support.test.md
```

### M3
```powershell
& c:/Dev/PyAgent/.venv/Scripts/Activate.ps1
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_backend_refresh_sessions.py -k "bootstrap or refresh or logout or restart"
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_backend_refresh_sessions.py tests/test_backend_auth.py tests/test_backend_worker.py
```

### M4
```powershell
& c:/Dev/PyAgent/.venv/Scripts/Activate.ps1
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_backend_refresh_sessions.py tests/test_backend_auth.py tests/test_backend_worker.py
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
git diff --name-only
```

### M5
```powershell
rg -n "token_urlsafe|sha|hash|typ|sid|jti|refresh|revok|atomic" backend/auth.py backend/auth_session_store.py backend/app.py tests/test_backend_refresh_sessions.py
git branch --show-current
git status --short
```

## Handoff Package to @5test
1. Start with T-JRT-001 only.
2. Keep the first red-phase slice limited to `tests/test_backend_refresh_sessions.py` plus `jwt-refresh-token-support.test.md`.
3. The recommended first slice is: temp store-path fixture, `POST /v1/auth/session` success/401 coverage, one successful `POST /v1/auth/refresh`, one replayed refresh-token `401`, and a disk assertion proving plaintext refresh tokens are never persisted.
4. Defer `tests/test_backend_auth.py` and `tests/test_backend_worker.py` until the refresh-session contract exists as a failing-first baseline.

## Planning Evidence
- Branch gate: `git branch --show-current` -> `prj0000122-jwt-refresh-token-support`
- Design inputs reviewed: project overview, think artifact, design artifact, and ADR-0008 on 2026-04-04
- Docs policy gate: `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `17 passed in 6.41s`
