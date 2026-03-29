# prj0000101-pending-definition - Design

_Status: DONE_
_Designer: @3design | Updated: 2026-03-29_

## Selected Option
Option A - Contract-First Consolidation (Discovery continuation).

Rationale:
- Preserve existing backend capability already present in `backend/app.py` while removing contract ambiguity left by idea000013.
- Reuse prior-art structure from prj0000098 and update it to reflect current runtime behavior and canonical path policy.
- Produce explicit, testable contracts for @4plan without broad backend refactor in this project stage.

Prior-art reused from prj0000098:
- Endpoint contract table format and AC-style traceability.
- Probe principles: unauthenticated access, rate-limit exemption, low-latency local checks.

## Architecture
### High-level architecture
- Keep probe endpoints implemented directly on the FastAPI app in `backend/app.py`.
- Treat canonical paths as `/v1/health`, `/v1/livez`, `/v1/readyz`.
- Keep unversioned aliases `/health`, `/livez`, `/readyz` as supported compatibility paths (no deprecation in this project scope).
- Keep probes outside authenticated API router and outside rate limiting.

### Readiness/Liveness model
- Liveness (`/livez`, `/v1/livez`): process responsiveness probe only.
- Readiness (`/readyz`, `/v1/readyz`): service acceptance probe that can degrade when local readiness signals indicate non-ready state.
- Health (`/health`, `/v1/health`): minimal broad health signal for legacy and orchestrator compatibility.

### Data flow
1. Request targets canonical path or alias.
2. Middleware applies correlation/version headers; probe bypasses auth and limiter.
3. Probe handler evaluates local state only.
4. Handler returns contract-defined status code and JSON payload.

## Interfaces & Contracts
### Canonical and alias path policy
- Canonical paths: `/v1/health`, `/v1/livez`, `/v1/readyz`.
- Supported aliases: `/health`, `/livez`, `/readyz`.
- Contract requirement: canonical and alias pairs are behaviorally identical (same status code and payload schema for same underlying state).

### Endpoint contracts

| Interface ID | Endpoint(s) | Method | Success Status | Degraded/Failure Status | Response Contract | Semantics | Auth | Rate Limit |
|---|---|---|---|---|---|---|---|---|
| IFC-HC-101 | `/v1/health`, `/health` | GET | 200 | N/A | `{"status": "ok"}` | Legacy-compatible general health | Not required | Exempt |
| IFC-HC-102 | `/v1/livez`, `/livez` | GET | 200 | N/A | `{"status": "alive"}` | Liveness only; no dependency readiness checks | Not required | Exempt |
| IFC-HC-103 | `/v1/readyz`, `/readyz` | GET | 200 | 503 | 200: `{"status": "ready"}`; 503: `{"status": "degraded", "ready": false, "reason": "<machine_readable_reason>"}` | Readiness gate for traffic admission | Not required | Exempt |

### Readiness decision contract
- Return 503 when either condition is true:
	- `app.state.readyz_degraded_reason` exists and is a non-empty string.
	- `PYAGENT_READYZ_FORCE_DEGRADED` is truthy (`1|true|yes|on`, case-insensitive).
- Return 200 otherwise.
- `reason` field is required on 503 responses and must be machine-readable, non-sensitive, and bounded-length text.

### Status code policy
- 200 for healthy/ready states on all probe endpoints.
- 503 only for readiness degradation on readyz endpoints.
- No 401/403/429 for probe endpoints.

## Acceptance Criteria

| AC ID | Requirement | Evidence Target |
|---|---|---|
| AC-101 | Canonical and alias endpoint pairs are both available for health, liveness, and readiness. | Probe route contract tests |
| AC-102 | `/v1/health` and `/health` return HTTP 200 with `{"status":"ok"}` and identical schemas. | Health parity tests |
| AC-103 | `/v1/livez` and `/livez` return HTTP 200 with `{"status":"alive"}` and identical schemas. | Liveness parity tests |
| AC-104 | `/v1/readyz` and `/readyz` return HTTP 200 with `{"status":"ready"}` when no degraded signal is set. | Readiness happy-path tests |
| AC-105 | `/v1/readyz` and `/readyz` return HTTP 503 with required fields `status`, `ready=false`, and `reason` when degraded signal is set. | Readiness degraded-path tests |
| AC-106 | Probe endpoints are unauthenticated and never require credentials under auth-enabled runtime. | Auth bypass tests |
| AC-107 | Probe endpoints are exempt from rate limiting and do not return 429 under probe burst traffic. | Rate-limit exemption tests |
| AC-108 | 503 readiness payload never exposes secrets, stack traces, or internal identifiers. | Payload allowlist/negative-field tests |

## Interface-to-Task Traceability

| Interface ID | Contract Focus | Planned Task ID for @4plan | Target Files for Planning |
|---|---|---|---|
| IFC-HC-101 | Health canonical+alias parity and payload stability | T-101 | `backend/app.py`, probe contract tests |
| IFC-HC-102 | Liveness canonical+alias parity and semantics | T-102 | `backend/app.py`, probe contract tests |
| IFC-HC-103 | Readiness 200/503 semantics with required reason field | T-103 | `backend/app.py`, readiness contract tests |
| IFC-HC-101, IFC-HC-102, IFC-HC-103 | Unauthenticated probe accessibility | T-104 | auth-related backend tests |
| IFC-HC-101, IFC-HC-102, IFC-HC-103 | Rate-limit exemption on canonical and alias paths | T-105 | rate-limiter tests |
| IFC-HC-103 | Degraded payload safety allowlist enforcement | T-106 | readiness negative tests |

## Non-Functional Requirements
- Performance:
	- Probe handlers remain local and constant-time with no outbound I/O.
	- Target probe latency: p95 < 20ms in local test environment.
- Security:
	- Probe payloads contain only operational status fields defined in contracts.
	- Readiness `reason` must not contain secrets, credentials, file paths, or stack traces.
- Testability:
	- Every AC ID maps to executable endpoint/auth/rate-limit tests in @4plan output.
	- Canonical-vs-alias parity is mandatory test coverage, not implied behavior.
- Reliability:
	- `/health` and `/livez` remain stable 200 signals unless process is unavailable.
	- `/readyz` degradation is deterministic from explicit local signals only.

## Open Questions
1. Should an explicit JSON schema artifact for probe responses be added in this project or deferred to the next contract-hardening lane?
2. Should `reason` values for degraded readiness be constrained to an enum now, or remain free-form machine-readable strings with allowlist constraints?
3. Should alias paths remain indefinitely supported or receive a future deprecation policy in a separate project after consumer inventory is complete?
