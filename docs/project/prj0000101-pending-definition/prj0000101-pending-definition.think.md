# prj0000101-pending-definition - Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-03-29_

## @1project Handoff Context
- Idea source: `docs/project/ideas/idea000013-backend-health-check-endpoint.md`
- Problem anchor: no visible `/health`, `/readyz`, or `/livez` endpoint in `backend/app.py` for orchestrator health checks.
- Branch constraint: all Discovery analysis must stay on `prj0000101-pending-definition`.
- Scope constraint: keep analysis and references within `docs/project/prj0000101-pending-definition/` plus source references; no implementation edits in this phase.
- Required outcomes for handoff acceptance:
	- Provide option set with trade-offs specific to backend health endpoint strategy.
	- Produce an explicit recommendation and rationale for @3design.
	- Capture open questions and assumptions that affect architecture/design decisions.

## Root Cause Analysis
- Idea-to-code drift: `idea000013` still states probe endpoints are missing, but repository evidence shows `/health`, `/livez`, and `/readyz` already exist in `backend/app.py`.
- Project duplication drift: prior full lifecycle work already exists for the same idea in `docs/project/prj0000098-backend-health-check-endpoint/`, including completed think/design/plan/code artifacts.
- Decision gap for this project: `prj0000101` currently lacks an explicit Discovery decision on whether to:
	- close as duplicate of `prj0000098`,
	- continue as contract-hardening,
	- or pursue a structural refactor.
- Governance root cause: source references and historical prior art were not reconciled before initiating this new project lane, leaving uncertain scope for @3design.

Research coverage used for this analysis (>=4 task types):
- Literature review: `docs/project/ideas/idea000013-backend-health-check-endpoint.md`, `docs/architecture/6interfaces-api.md`.
- Alternative enumeration: options A/B/C below.
- Prior-art search: `docs/project/prj0000098-backend-health-check-endpoint/prj0000098-backend-health-check-endpoint.think.md`, `docs/project/prj0000098-backend-health-check-endpoint/prj0000098-backend-health-check-endpoint.design.md`, `docs/architecture/archive/9operations-observability.md`.
- Constraint mapping: branch/scope constraints from `docs/project/prj0000101-pending-definition/prj0000101-pending-definition.project.md`.
- Stakeholder impact: backend runtime, operations, CI/test owners, and downstream @3design/@4plan agents.
- Risk enumeration: security/operability risks captured per option below.

## Options
### Option A - Contract-First Consolidation (Discovery continuation)
Architecture/implementation direction:
- Treat existing probe endpoints in `backend/app.py` as baseline capability.
- Focus this project on formalizing endpoint contract decisions (payload/status semantics, versioned vs unversioned behavior, readiness degradation semantics) and acceptance criteria for downstream design.
- Avoid structural backend changes during this lane; prioritize explicit contract and testability alignment for @3design.

SWOT:
- Strength: fastest scope-fit with branch boundary and Discovery-only mandate.
- Weakness: does not reduce structural code coupling yet.
- Opportunity: resolves stale idea narrative and prevents duplicate implementation work.
- Threat: if contract remains ambiguous, downstream implementation may diverge.

Security risk analysis:
- Threat vector: accidental leakage of internal state in readiness payload.
	Impact: M. Mitigation: constrain payload schema to non-sensitive fields.
	Testability signal: response-schema and content-allowlist tests.
- Threat vector: endpoint auth/rate-limit regression while refining contract.
	Impact: H. Mitigation: explicit unauthenticated + exemption requirements in design.
	Testability signal: auth-bypass and rate-limit regression tests.
- Threat vector: stale docs causing operator misuse.
	Impact: M. Mitigation: canonical contract docs linked to acceptance tests.
	Testability signal: docs-policy checks plus targeted contract test references.

Stakeholder impact:
- Low blast radius, primarily docs/design/test contract owners and operations consumers.

### Option B - Canonical Path Rationalization (`/v1/*` preferred, legacy alias policy)
Architecture/implementation direction:
- Define canonical probe endpoints under `/v1/health`, `/v1/livez`, `/v1/readyz`.
- Define lifecycle policy for unversioned aliases (`/health`, `/livez`, `/readyz`): keep, deprecate, or remove with migration horizon.
- Carry this as design-level API compatibility decision; implementation deferred.

SWOT:
- Strength: cleaner long-term API surface and explicit compatibility policy.
- Weakness: broader migration and coordination burden.
- Opportunity: align docs/providers around one canonical endpoint family.
- Threat: breaking external probes if alias policy is mishandled.

Security risk analysis:
- Threat vector: alias deprecation without migration coverage causing silent monitoring outage.
	Impact: H. Mitigation: phased policy and compatibility tests.
	Testability signal: dual-path availability tests until cutover.
- Threat vector: inconsistent auth/limiter behavior across old/new paths.
	Impact: H. Mitigation: enforce parity requirements in design contracts.
	Testability signal: matrix tests across all path variants.
- Threat vector: operational drift between docs and runtime.
	Impact: M. Mitigation: contract source-of-truth and CI doc checks.
	Testability signal: docs structure policy + endpoint contract tests.

Stakeholder impact:
- Medium blast radius across operations, integrators, and provider config consumers.

### Option C - Probe Module Refactor (router/service extraction)
Architecture/implementation direction:
- Move probe logic into dedicated health module/router and explicit readiness evaluator service.
- Keep endpoint contracts but isolate responsibilities for future extensibility.
- Position as maintainability-first direction with higher upfront design complexity.

SWOT:
- Strength: best long-term modularity and ownership boundaries.
- Weakness: highest complexity and delivery latency for current Discovery objective.
- Opportunity: enables richer dependency-aware readiness checks later.
- Threat: refactor regressions on existing stable endpoints.

Security risk analysis:
- Threat vector: route wiring regression exposing/misconfiguring health paths.
	Impact: H. Mitigation: route registration validation and integration tests.
	Testability signal: endpoint discovery tests and startup smoke tests.
- Threat vector: readiness evaluator introducing slow/blocking checks.
	Impact: M. Mitigation: local-only bounded checks in first phase.
	Testability signal: latency SLO assertions for probe handlers.
- Threat vector: inconsistent middleware behavior after router split.
	Impact: H. Mitigation: middleware parity requirements in design spec.
	Testability signal: auth/rate-limit middleware regression suite.

Stakeholder impact:
- High blast radius across backend architecture, tests, and operator runbooks.

## Decision Matrix
Scoring: 1 (worst) to 5 (best)

| Criterion | Option A | Option B | Option C |
|---|---:|---:|---:|
| Scope fit | 5 | 3 | 2 |
| Complexity (lower is better score) | 5 | 3 | 2 |
| Risk reduction | 4 | 4 | 3 |
| Delivery speed | 5 | 3 | 2 |
| Operability | 4 | 4 | 3 |
| Total | 23 | 17 | 12 |

Decision notes:
- Option A best matches Discovery constraints and immediate handoff value.
- Option B is viable if @3design prioritizes API canonicalization policy over speed.
- Option C is not preferred for this project stage due to scope/complexity mismatch.

## Recommendation
**Recommend Option A - Contract-First Consolidation** for handoff to @3design.

Rationale:
- It directly addresses the root-cause mismatch (idea says missing endpoints, code shows existing endpoints) without unnecessary re-implementation.
- It keeps work Discovery-level and branch-scope compliant while producing a design-ready contract baseline.
- It reduces duplication risk by explicitly reusing prior art from:
	- `docs/project/prj0000098-backend-health-check-endpoint/prj0000098-backend-health-check-endpoint.think.md`
	- `docs/project/prj0000098-backend-health-check-endpoint/prj0000098-backend-health-check-endpoint.design.md`

Risk-to-testability mapping for the selected option:
- Contract ambiguity risk -> endpoint contract tests for status/body parity (`/health`, `/livez`, `/readyz`, and `/v1/*` where applicable).
- Security exposure risk (payload over-sharing) -> schema/content allowlist tests and negative checks for sensitive fields.
- Operability regression risk (probe accessibility under auth/limiter changes) -> explicit auth-bypass and rate-limit exemption regression tests.
- Governance drift risk -> docs policy validation and traceability links from design acceptance criteria to test targets.

Handoff to @3design:
- Use Option A as baseline.
- Reconcile current live contracts in `backend/app.py` with legacy artifacts from `prj0000098`.
- Produce one explicit interface contract table and acceptance set that disambiguates:
	- readiness degraded semantics,
	- canonical vs alias path policy,
	- and required regression test matrix.

## Open Questions
1. Should `prj0000101` be treated as a continuation/supersession of `prj0000098`, or explicitly marked as duplicate-and-close after design reconciliation?
2. For probe paths, what is the canonical contract policy: dual-path long-term support (`/v1/*` + unversioned) or phased deprecation of aliases?
3. Must `/readyz` degraded responses remain configurable via app state/env controls, and what is the minimum allowed reason schema?
4. What exact non-sensitive payload fields are approved for probe responses to satisfy operations without exposing internals?
5. Which test files are mandatory for contract parity coverage in this lane, and which can remain inherited from prior-art project baselines?
