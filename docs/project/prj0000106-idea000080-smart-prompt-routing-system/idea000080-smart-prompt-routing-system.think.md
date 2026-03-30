# idea000080-smart-prompt-routing-system - Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-03-30_

## Branch Plan
Expected branch: prj0000106-idea000080-smart-prompt-routing-system.

## Branch Validation
- PASS: Expected branch recorded in project overview.
- PASS: Observed branch matches expected during initialization.

## Scope Validation
- PASS: Initialization changes constrained to project governance artifacts.

## Failure Disposition
None.

## Root Cause Analysis

1. Prompt/model/agent routing knowledge exists in prior projects, but capability selection is still fragmented across intent handling, provider fallback, and scheduler heuristics.
2. Existing prior-art demonstrates safe dual-path rollout patterns, but there is no current project-level smart routing policy that combines workload classification, context strategy, and resilience controls in one contract.
3. Without a unified routing contract, the system risks suboptimal model selection, cost spikes, and inconsistent behavior under failure.

## Research Coverage (Required Task Types)

### 1) Literature Review
- `docs/project/ideas/idea000080-smart-prompt-routing-system.md`
- `docs/architecture/archive/agents.md`
- `docs/architecture/archive/INFRASTRUCTURE_SERVICES.md`
- `docs/architecture/archive/V4_IMPLEMENTATION_DEEP_DIVE.md`

### 2) Alternative Enumeration
- Option A: Deterministic Rule Router (intent + workload bands)
- Option B: Hybrid Router (rules + lightweight semantic classifier + LLM tie-break)
- Option C: Event-Mediated Router Service (decoupled command bus topology)

### 3) Prior-Art Search
- `docs/project/prj0000086-universal-agent-shell/universal-agent-shell.think.md`
- `docs/project/prj0000086-universal-agent-shell/universal-agent-shell.design.md`
- `docs/project/prj0000083-llm-circuit-breaker/prj0000083-llm-circuit-breaker.think.md`
- `docs/project/prj0000080-cort-reasoning-pipeline/prj0000080.think.md`

### 4) Constraint Mapping
- Branch must match: `prj0000106-idea000080-smart-prompt-routing-system`.
- Keep work in project lifecycle scope for this phase (docs + memory/log updates).
- Downstream architecture must preserve mixin/core separation and async-first patterns.
- Naming and docs decisions must comply with:
	- `docs/project/naming_standards.md`
	- `docs/project/code_of_conduct.md`

### 5) Stakeholder Impact
- `@3design`: needs stable routing contracts and interface boundaries.
- `@4plan`/`@5test`: need deterministic acceptance criteria and validation signals.
- `@6code`: needs low-risk integration points in orchestration layers.
- Runtime stakeholders: provider adapters, observability, and resilience layers.

### 6) Risk Enumeration
- Included per option below with likelihood/impact and explicit risk-to-testability mapping.

## External Pattern Evidence (Approved Domains)
- `github.com/humanlayer/12-factor-agents`: reinforces structured tool-calling, owned context-window policy, and explicit control-flow ownership.
- `learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/event-driven`: informs broker vs mediator tradeoffs, observability/correlation, and reliability implications for decoupled routing.

## Options

### Option A - Deterministic Rule Router (Policy Table in Orchestration Layer)

**Problem statement**
Implement smart routing with deterministic policy rules only (intent/workload/latency budget/tool requirement), minimizing moving parts.

**Proposed approach**
1. Define a static routing matrix mapping `(intent, workload_class, constraints)` to `(model tier, context strategy, tool policy)`.
2. Reuse fallback semantics from prior circuit-breaker patterns for unavailable providers.
3. Emit structured routing telemetry for auditability.

**Research task coverage for this option (4/6+):**
- Literature review: archive and prior project docs.
- Prior-art search: prj0000086 + prj0000083.
- Constraint mapping: scope, branch, naming, async/mixin constraints.
- Stakeholder impact: straightforward for plan/test/code agents.
- Risk enumeration: listed below.

**Workspace evidence**
- `docs/project/prj0000086-universal-agent-shell/universal-agent-shell.design.md`
- `docs/project/prj0000083-llm-circuit-breaker/prj0000083-llm-circuit-breaker.think.md`
- `rust_core/src/inference/scheduler.rs`

**SWOT**
- Strengths: deterministic, easy to test, low operational complexity.
- Weaknesses: poorer adaptability to ambiguous prompts and evolving workloads.
- Opportunities: fast initial rollout with clear governance/audit behavior.
- Threats: policy-table drift and misrouting as task diversity grows.

**Security and reliability risks (with testability mapping)**
| Risk | Likelihood | Impact | Mitigation | Testability signal |
|---|---|---|---|---|
| Rule poisoning/misconfiguration routes sensitive prompts to weak path | M | H | signed policy changes + review gate | policy snapshot tests + approval audit log checks |
| Prompt classification bypass via phrasing edge cases | M | M | explicit deny/unknown fallback route | adversarial prompt regression tests |
| Telemetry leaks prompt content | L | H | field allowlist and redaction | log-schema unit tests + secret scan assertions |

### Option B - Hybrid Router (Rules + Semantic Classifier + LLM Tie-Break) [Leading]

**Problem statement**
Balance deterministic safety with better routing accuracy for ambiguous or multi-intent prompts.

**Proposed approach**
1. Stage-1 deterministic guardrails choose obvious routes and enforce hard constraints.
2. Stage-2 lightweight semantic classifier handles ambiguous prompts.
3. Stage-3 optional low-cost LLM tie-breaker only when confidence is below threshold.
4. Apply resilience fallback policy and emit confidence/decision provenance telemetry.

**Research task coverage for this option (4/6+):**
- Literature review: 12-factor agent control-flow/context principles.
- Prior-art search: universal shell dual-path and circuit-breaker fallback patterns.
- Constraint mapping: in-scope docs phase now; design must preserve mixin/core separation later.
- Stakeholder impact: broader than Option A but still manageable for design/plan/test.
- Risk enumeration: listed below.

**Workspace evidence**
- `docs/project/prj0000086-universal-agent-shell/universal-agent-shell.think.md`
- `docs/project/prj0000080-cort-reasoning-pipeline/prj0000080.think.md`
- `src/context_manager/window.py`

**SWOT**
- Strengths: better routing quality under ambiguity while preserving deterministic boundaries.
- Weaknesses: more components and confidence-threshold tuning complexity.
- Opportunities: supports shadow-mode learning and phased improvement.
- Threats: tie-breaker latency/cost creep if thresholds are mis-tuned.

**Security and reliability risks (with testability mapping)**
| Risk | Likelihood | Impact | Mitigation | Testability signal |
|---|---|---|---|---|
| Classifier confidence manipulation causes expensive or unsafe route | M | H | hard guardrail precedence over classifier | precedence contract tests + fuzzed confidence inputs |
| LLM tie-break prompt injection from untrusted context | M | H | sanitize/partition context and strict schema output | schema-validation tests + injection corpus tests |
| Non-deterministic tie-break creates flaky behavior | M | M | deterministic seed/temperature controls in tie-break path | deterministic replay tests + route consistency metrics |

### Option C - Event-Mediated Router Service (Mediator Topology)

**Problem statement**
Externalize routing into a mediator service on an event bus to maximize decoupling and scaling.

**Proposed approach**
1. Producer emits routing request events with correlation IDs.
2. Mediator resolves route and dispatch commands to specialized consumers.
3. Consumers execute and publish results; orchestrator reconciles responses.

**Research task coverage for this option (4/6+):**
- Literature review: infrastructure archive + Microsoft event-driven mediator guidance.
- Alternative enumeration: broker vs mediator architecture style.
- Constraint mapping: highest blast radius and largest out-of-scope risk for current lifecycle stage.
- Stakeholder impact: affects orchestration, observability, operations, and incident response.
- Risk enumeration: listed below.

**Workspace evidence**
- `docs/architecture/archive/INFRASTRUCTURE_SERVICES.md`
- `docs/architecture/archive/proxima_voyager.md`
- `docs/project/prj0000057/agent-orchestration-graph.design.md`

**SWOT**
- Strengths: high decoupling and scalability; strong long-term extensibility.
- Weaknesses: biggest implementation and operational complexity.
- Opportunities: replayable routing events and richer observability pipelines.
- Threats: consistency/debuggability challenges and mediator bottleneck risk.

**Security and reliability risks (with testability mapping)**
| Risk | Likelihood | Impact | Mitigation | Testability signal |
|---|---|---|---|---|
| Event replay/tampering alters routing outcomes | M | H | signed events + idempotency keys + sequence checks | replay/idempotency integration tests |
| Correlation ID propagation breaks traceability | M | M | mandatory correlation contract at ingestion | end-to-end trace propagation tests |
| Mediator outage becomes centralized failure point | M | H | HA mediator + backpressure + DLQ | chaos/failover scenario tests |

## Project Boundary Constraints Tie-In

1. Current @2think work remains documentation-only and does not alter runtime code.
2. Recommended direction must support phased rollout and fallback, minimizing blast radius.
3. Any downstream design must keep to naming/governance standards and produce deterministic validation artifacts for @4plan/@5test.
4. Option C is feasible long-term but misaligned with near-term project boundary due to operational and integration breadth.

## Decision Matrix
| Criterion | Option A | Option B | Option C |
|---|---|---|---|
| Routing accuracy under ambiguity | Medium | High | High |
| Determinism/auditability | High | High | Medium |
| Initial delivery complexity | Low | Medium | High |
| Reuse of repository prior-art patterns | High | High | Medium |
| Security control surface size | Low | Medium | High |
| Operational overhead | Low | Medium | High |
| Incremental rollout safety | High | High | Medium |
| Long-term extensibility | Medium | High | High |

## Recommendation
**Leading option: Option B (Hybrid Router with deterministic guardrails).**

**Rationale**
1. Preserves deterministic guardrails and fallback safety from proven prior-art while improving route quality for ambiguous prompts.
2. Keeps complexity below event-mediator architecture while avoiding rigid rule-only limitations.
3. Supports phased rollout and shadow evaluation, which aligns with project-boundary risk control.

**Historical prior-art references (required)**
- `docs/project/prj0000086-universal-agent-shell/universal-agent-shell.design.md`
- `docs/project/prj0000083-llm-circuit-breaker/prj0000083-llm-circuit-breaker.think.md`
- `docs/project/prj0000080-cort-reasoning-pipeline/prj0000080.think.md`

**Risk-to-testability mapping for recommended option**
| Key risk | Proposed validation strategy |
|---|---|
| Guardrail precedence regressions | contract tests that assert rule layer always overrides classifier/tie-break |
| Confidence threshold drift | threshold sweep tests plus route distribution monitoring in shadow mode |
| Tie-break instability | deterministic replay tests with fixed seeds and expected route outputs |

## Open Questions
1. Which prompt/workload taxonomy should be canonical in v1, and where is it versioned?
2. What confidence threshold policy should trigger the tie-breaker vs immediate fallback to deterministic route?
3. Which telemetry schema is mandatory for route provenance (rule hit, classifier score, tie-break result, fallback reason)?
4. What are acceptance gates for promoting routes from shadow-mode to active-mode?
5. What is the exact timeout/circuit-break policy boundary between route selection and model execution?
6. Should ambiguous high-risk prompts default to safest model/tool path even at higher cost?
