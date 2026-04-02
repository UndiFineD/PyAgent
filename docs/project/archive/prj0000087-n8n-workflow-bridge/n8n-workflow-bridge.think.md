# n8n-workflow-bridge - Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-03-27_

## Root Cause Analysis

1. The project has a strategic n8n requirement but no concrete integration contract for event payloads, retries,
	or auth boundaries.
2. Existing backend security patterns already support optional API-key/JWT auth, but there is no n8n-specific
	adapter layer to reuse these controls safely.
3. A minimal safe v1 must avoid new dependencies and large architecture changes while still enabling both
	outbound workflow triggering and inbound decision callbacks.
4. Without a canonical adapter boundary, integration logic will fragment across endpoints and tools, increasing
	regression and security risk.

## Research Evidence (Task-Type Coverage)

| Task type | Evidence paths |
|---|---|
| Literature review | `docs/architecture/archive/improvement_requirements.md`, `docs/architecture/2workflow.md`, `docs/project/kanban.md` |
| Alternative enumeration | `docs/project/prj0000087-n8n-workflow-bridge/n8n-workflow-bridge.think.md` (this artifact) |
| Prior-art search | `docs/project/prj0000053/hmac-webhook-verification.think.md`, `docs/project/prj0000083-llm-circuit-breaker/prj0000083-llm-circuit-breaker.think.md`, `docs/project/prj0000084-immutable-audit-trail/prj0000084-immutable-audit-trail.think.md` |
| Constraint mapping | `docs/project/prj0000087-n8n-workflow-bridge/n8n-workflow-bridge.project.md`, `docs/architecture/2workflow.md`, `docs/project/kanban.md` |
| Stakeholder impact | `backend/app.py`, `backend/auth.py`, `src/github_app.py`, `docs/project/prj0000087-n8n-workflow-bridge/n8n-workflow-bridge.design.md` |
| Risk enumeration | `docs/project/prj0000053/hmac-webhook-verification.think.md`, `docs/project/prj0000083-llm-circuit-breaker/prj0000083-llm-circuit-breaker.think.md` |

## Options

### Option A - Inbound-Only Webhook Decision Node (Minimalest)

**Approach**
- Add only an inbound endpoint that n8n calls (`POST /api/v1/n8n/events`).
- Validate request shape and map event types directly to existing agent entrypoints.
- Optional API-key check via existing `require_auth` dependency.
- No outbound HTTP client layer in v1.

**Pros**
- Smallest immediate change and lowest implementation time.
- Reuses existing auth/rate-limit middleware in backend.
- Limits blast radius to one route and one adapter function.

**Cons**
- Fails bi-directional goal (agents cannot trigger n8n workflows).
- Pushes outbound design debt to v2 and can force breaking contract changes later.
- Increases risk of ad-hoc outbound calls added in unrelated modules.

**Workspace evidence**
- `docs/architecture/archive/improvement_requirements.md`
- `backend/app.py`
- `backend/auth.py`
- `docs/project/prj0000087-n8n-workflow-bridge/n8n-workflow-bridge.project.md`

**Risk enumeration**

| Failure mode | Likelihood | Impact |
|---|---|---|
| V1 seen as complete despite missing outbound path | M | H |
| Contract churn when outbound support is added later | H | M |
| Inbound payload mapping grows coupled to agent internals | M | M |

**Task-type coverage for Option A**
- Literature review, constraint mapping, stakeholder impact, risk enumeration.

### Option B - Stdlib-Only HTTP Integration Layer + Event Adapter (Recommended)

**Approach**
- Introduce a small stdlib-only integration layer for outbound calls (`urllib.request` + `json` + `hmac`).
- Introduce a dedicated event adapter that normalizes inbound/outbound payloads between PyAgent and n8n.
- Support optional API-key auth for inbound requests and optional outbound header signing.
- Keep persistence out of scope: in-memory idempotency key cache only for minimal safety.

**Pros**
- Satisfies bi-directional requirement with minimal safe v1 scope.
- Aligns with existing project precedent favoring stdlib-first, dependency-light implementations.
- Keeps integration logic in a single boundary layer, reducing coupling and easing future retries/queueing.
- Reuses current backend auth behavior (dev mode + API-key/JWT), preserving compatibility.

**Cons**
- Requires defining explicit payload contracts now (slightly more design effort than Option A).
- No durable retry queue in v1; transient outbound failures are handled only via bounded retry/backoff.

**Workspace evidence**
- `docs/architecture/archive/improvement_requirements.md`
- `backend/auth.py`
- `backend/app.py`
- `src/github_app.py`
- `docs/project/prj0000053/hmac-webhook-verification.think.md`
- `docs/project/prj0000083-llm-circuit-breaker/prj0000083-llm-circuit-breaker.think.md`

**Risk enumeration**

| Failure mode | Likelihood | Impact |
|---|---|---|
| Replay/duplicate events without durable dedupe store | M | M |
| Misconfigured API key leads to accidental open endpoint in prod | M | H |
| Outbound timeout tuning too low/high causes flaky orchestration | M | M |

**Task-type coverage for Option B**
- Literature review, prior-art search, constraint mapping, stakeholder impact, risk enumeration,
  alternative enumeration.

### Option C - Durable Queue Bridge with Worker and Signed Callbacks

**Approach**
- Add a queue-backed bridge (SQLite or Redis-style abstraction) with worker polling,
  durable retries, dead-letter handling, and callback signature verification.
- Keep bidirectional adapter but include persistence and replay tooling in v1.

**Pros**
- Highest operational resilience and traceability.
- Better at handling burst traffic and temporary n8n outages.

**Cons**
- Exceeds minimal safe v1 scope and complexity budget.
- Adds operational surface area (queue lifecycle, migration, worker supervision).
- Increases time-to-first-value and design/testing burden.

**Workspace evidence**
- `docs/project/kanban.md`
- `docs/architecture/2workflow.md`
- `docs/project/prj0000087-n8n-workflow-bridge/n8n-workflow-bridge.project.md`
- `docs/project/prj0000084-immutable-audit-trail/prj0000084-immutable-audit-trail.think.md`

**Risk enumeration**

| Failure mode | Likelihood | Impact |
|---|---|---|
| Overbuild delays delivery and stalls downstream phases | H | H |
| Worker/queue failure modes introduce new incident class | M | H |
| Scope creep breaks branch-boundary and sprint expectations | M | M |

**Task-type coverage for Option C**
- Literature review, prior-art search, constraint mapping, stakeholder impact, risk enumeration,
  alternative enumeration.

## Decision Matrix

| Criterion | Option A | Option B | Option C |
|---|---|---|---|
| Meets bi-directional n8n goal | No | Yes | Yes |
| Minimal safe v1 fit | High | High | Low |
| Dependency footprint | Lowest | Low (stdlib-only) | Medium/High |
| Security alignment with existing auth | Medium | High | High |
| Delivery speed | Fastest | Fast | Slow |
| Operational resilience | Low | Medium | High |
| Architecture coupling risk | Medium/High | Low | Medium |
| Overall recommendation score | 2/5 | 5/5 | 3/5 |

## Recommendation

**Option B — stdlib-only HTTP integration layer + event adapter with optional API-key auth**

Rationale:
- It is the only option that balances minimal safe v1 delivery with the required bi-directional bridge behavior.
- It aligns with established repo precedent for stdlib-first security-sensitive v1 implementations.
- It reuses existing auth and middleware patterns instead of introducing a new trust model.
- It creates a clean adapter boundary that @3design can extend later with durable queues without breaking contracts.

## Open Questions

1. Inbound auth mode: should n8n endpoints accept only API key in v1, or both API key and JWT for parity with
	existing protected routes?
2. Outbound signing: do we require HMAC signing for agent-to-n8n requests in v1, or treat API key as sufficient
	with HMAC deferred to v1.1?
3. Idempotency window: what TTL should in-memory dedupe keys use (for example 5m vs 15m)?
4. Failure semantics: for outbound workflow trigger failures, should the adapter return synchronous error details,
	or enqueue a retry token for later manual replay endpoint in v1?
5. Contract versioning: should payloads include `schema_version` now to avoid future incompatibility?

## Integration Points for @3design

- `backend/app.py`: add versioned n8n endpoints under existing `/api/v1/` routing style and protected router usage.
- `backend/auth.py`: reuse `require_auth` for optional API-key/JWT enforcement; keep dev-mode behavior unchanged.
- `backend/rate_limiter.py`: apply existing limiter to n8n ingress endpoints to reduce abuse risk.
- `backend/logging_config.py`: emit structured correlation IDs for bridge requests and callback responses.
- `src/github_app.py`: reference signature verification pattern (`hmac.compare_digest`, raw-body verification) for
  optional outbound/inbound signing parity.
- `docs/project/prj0000087-n8n-workflow-bridge/n8n-workflow-bridge.design.md`: define canonical event schema,
  adapter interface, timeout/retry bounds, and auth policy as binding decisions.
