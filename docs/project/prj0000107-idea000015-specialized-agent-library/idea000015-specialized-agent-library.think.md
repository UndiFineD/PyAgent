# idea000015-specialized-agent-library - Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-03-30_

## Root Cause Analysis
1. Capability-definition/runtime gap: specialized capabilities are documented in agent definition artifacts, but Python runtime implementation in `src/agents/` is effectively anchored on `BaseAgent.py` with no equivalent specialized Python-agent library layer.
2. Architectural drift risk: repository architecture emphasizes core/agent separation and mixin composition, but there is no current project-level option decision that defines how specialized agents should be represented in runtime code.
3. Governance ambiguity: source idea references `docs/AGENTS.md`, while repository evidence points to `docs/architecture/1agents.md` and `docs/architecture/archive/agents.md`; this mismatch can produce incorrect implementation targeting in @3design/@4plan.

## Discovery Evidence
### Literature Review (Repository)
- `src/agents/BaseAgent.py` shows the baseline Python runtime anchor.
- `docs/architecture/1agents.md` defines roster/process and architecture principles (core/agent separation, mixins, transactions).
- `docs/project/ideas/idea000015-specialized-agent-library.md` states the implementation gap and expected workflow constraints.

### Alternative Enumeration
Three distinct options were explored:
- Option A: Dedicated specialized Python runtime classes.
- Option B: Hybrid manifest-to-runtime adapter over universal shell primitives.
- Option C: Universal-only capability packs with no dedicated specialized classes.

### Prior-Art Search
- `docs/project/prj0000086-universal-agent-shell/universal-agent-shell.project.md`
- `docs/project/prj0000105-idea000016-mixin-architecture-base/idea000016-mixin-architecture-base.project.md`
- `docs/project/prj0000106-idea000080-smart-prompt-routing-system/idea000080-smart-prompt-routing-system.project.md`
- `docs/architecture/archive/agents.md`

### Constraint Mapping
- Must stay in project-doc scope for @2think (no production code edits).
- Must preserve branch gate: expected branch is `prj0000107-idea000015-specialized-agent-library`.
- Must align with naming policy in `docs/project/naming_standards.md` (snake_case files/folders) and conduct policy in `docs/project/code_of_conduct.md`.
- Must respect architecture instruction: agent orchestration thin; domain logic in `*Core` classes; composition via mixins.

### Stakeholder Impact
- @3design: requires an explicit implementation target (class library vs adapters vs shell-only) to draft interfaces and ADR implications.
- @4plan/@5test: need predictable test seams and validation signals per risk area.
- @6code: needs clear file boundaries and migration strategy to avoid broad churn.
- @9git: needs narrow staging policy compliance limited to project artifacts in this phase.

### External Pattern Evidence (Approved Source)
- `https://github.com/humanlayer/12-factor-agents` supports patterns relevant to this decision space:
  - small focused agents,
  - own prompts/context,
  - structured tool outputs,
  - avoid over-framework rewrites when incremental modular integration is viable.

## Options
### Option A - Dedicated Specialized Python Agent Class Library
Build concrete specialized agent classes under a dedicated runtime package (for example, under `src/agents/`), each orchestrating a corresponding `*Core` implementation.

Evidence anchors:
- `src/agents/BaseAgent.py`
- `docs/architecture/1agents.md`
- `docs/project/prj0000105-idea000016-mixin-architecture-base/idea000016-mixin-architecture-base.project.md`

Research coverage:
- Literature review: yes
- Alternative enumeration: yes
- Prior-art search: yes
- Constraint mapping: yes
- Stakeholder impact: yes
- Risk enumeration: yes

Pros:
- Highest explicitness for discoverability and static analysis.
- Clear boundaries for ownership and testing per specialized agent.
- Strong alignment with "small focused agents" principle.

Cons:
- Higher implementation surface and migration overhead.
- Potential class proliferation and maintenance burden.
- More opportunities for naming/structure drift if not strongly governed.

SWOT:
- Strengths: explicit contracts, test isolation, easier onboarding.
- Weaknesses: boilerplate growth, duplicated orchestration logic risk.
- Opportunities: establish canonical specialization template for future agents.
- Threats: scope expansion into broad refactors beyond project boundary.

Security risk analysis with testability mapping:
1. Risk: inconsistent tool permission boundaries across many classes.
	- Likelihood: M | Impact: H
	- Mitigation: shared guardrail mixins and centralized policy contract.
	- Testability signal: policy contract unit tests + negative authorization tests.
2. Risk: prompt/context leakage from per-agent divergence.
	- Likelihood: M | Impact: M
	- Mitigation: central context/prompt templates with schema checks.
	- Testability signal: prompt/context schema validation tests and regression fixtures.
3. Risk: incomplete transaction wrapping in newly added specialized flows.
	- Likelihood: M | Impact: H
	- Mitigation: mandatory transaction interfaces in specialized base abstractions.
	- Testability signal: failure-injection tests asserting rollback behavior.

### Option B - Hybrid Adapter Layer: Manifest-Defined Specializations + Runtime Adapters (Recommended)
Retain universal shell primitives while introducing a typed adapter layer that maps specialized definitions to runtime orchestration contracts, with domain logic still in `*Core` classes.

Evidence anchors:
- `src/core/universal/UniversalAgentShell.py`
- `src/core/universal/UniversalIntentRouter.py`
- `docs/project/prj0000086-universal-agent-shell/universal-agent-shell.project.md`
- `docs/project/prj0000106-idea000080-smart-prompt-routing-system/idea000080-smart-prompt-routing-system.project.md`

Research coverage:
- Literature review: yes
- Alternative enumeration: yes
- Prior-art search: yes
- Constraint mapping: yes
- Stakeholder impact: yes
- Risk enumeration: yes

Pros:
- Best balance between explicit specialization and reuse of existing routing/shell capabilities.
- Lower migration risk than full class-library rollout.
- Supports incremental rollout with compatibility checks.

Cons:
- Requires strong adapter contracts to avoid hidden complexity.
- Risk of half-implemented abstractions if ownership boundaries are unclear.
- Debugging may span manifest, adapter, and shell layers.

SWOT:
- Strengths: incremental adoption, reduced churn, architecture-compatible.
- Weaknesses: added indirection compared with direct classes.
- Opportunities: create a reusable specialization framework with guardrails.
- Threats: adapter sprawl if boundaries and versioning are not enforced.

Security risk analysis with testability mapping:
1. Risk: adapter route injection or malformed manifest mapping.
	- Likelihood: M | Impact: H
	- Mitigation: strict manifest schema validation + allowlisted capability routing.
	- Testability signal: schema-fuzz tests and route-allowlist enforcement tests.
2. Risk: privilege escalation through dynamic capability binding.
	- Likelihood: M | Impact: H
	- Mitigation: capability-to-policy matrix with default deny.
	- Testability signal: permission matrix tests and denied-path integration tests.
3. Risk: observability blind spots across adapter boundaries.
	- Likelihood: M | Impact: M
	- Mitigation: mandatory telemetry envelope and correlation IDs at adapter ingress/egress.
	- Testability signal: telemetry contract tests asserting required fields and continuity.

### Option C - Universal-Only Capability Packs (No Dedicated Specialized Runtime Library)
Avoid adding specialized runtime classes; represent specialization solely via shell/routing policy and capability packs.

Evidence anchors:
- `src/core/universal/UniversalAgentShell.py`
- `src/core/universal/UniversalCoreRegistry.py`
- `docs/architecture/archive/V4_IMPLEMENTATION_DEEP_DIVE.md`

Research coverage:
- Literature review: yes
- Alternative enumeration: yes
- Prior-art search: yes
- Constraint mapping: yes
- Stakeholder impact: yes
- Risk enumeration: yes

Pros:
- Minimal immediate code surface.
- Fastest path to short-term experimentation.
- Centralized control in one orchestration surface.

Cons:
- Weakest alignment with explicit specialized-agent-library objective.
- Reduced clarity for ownership and per-specialization testing.
- Higher risk of monolithic shell complexity over time.

SWOT:
- Strengths: low initial implementation cost.
- Weaknesses: weak semantic alignment with project intent.
- Opportunities: rapid prototyping for capability fit validation.
- Threats: long-term maintainability and auditability degradation.

Security risk analysis with testability mapping:
1. Risk: centralized shell blast radius for defects.
	- Likelihood: M | Impact: H
	- Mitigation: strict feature flags and bounded rollout strategy.
	- Testability signal: canary and regression suite by capability pack.
2. Risk: policy drift between capability metadata and runtime behavior.
	- Likelihood: M | Impact: M
	- Mitigation: metadata/runtime parity validation gate.
	- Testability signal: parity tests comparing declared vs executable capability graph.
3. Risk: weak traceability for specialization-level audits.
	- Likelihood: H | Impact: M
	- Mitigation: per-capability audit tagging and deterministic route logs.
	- Testability signal: audit log completeness tests and trace replay checks.

## Decision Matrix
| Criterion | Option A | Option B | Option C |
|---|---:|---:|---:|
| Alignment to specialized-agent-library objective | 5 | 5 | 2 |
| Reuse of existing repository capabilities | 3 | 5 | 5 |
| Delivery risk (lower is better) | 2 | 4 | 4 |
| Long-term maintainability | 4 | 5 | 2 |
| Security/governance controllability | 4 | 5 | 3 |
| Testability and observability | 4 | 5 | 3 |
| Total | 22 | 29 | 19 |

## Recommendation
**Select Option B (Hybrid Adapter Layer).**

Rationale:
1. Best objective fit without forcing full class proliferation.
2. Reuses proven universal-shell/routing primitives while adding explicit specialization contracts.
3. Lowest combined architecture and migration risk under current project constraints.

Historical prior-art grounding:
- `docs/project/prj0000086-universal-agent-shell/universal-agent-shell.project.md`
- `docs/project/prj0000105-idea000016-mixin-architecture-base/idea000016-mixin-architecture-base.project.md`
- `docs/project/prj0000106-idea000080-smart-prompt-routing-system/idea000080-smart-prompt-routing-system.project.md`

Reject reasons:
- Option A rejected for v1 due to higher churn and larger blast radius before adapter contracts are validated.
- Option C rejected for v1 because it under-serves the explicit specialized-library goal and risks a monolithic shell surface.

## Open Questions (for @3design)
1. What is the minimal adapter contract boundary between specialized definitions and runtime shell calls?
2. Should specialization metadata source-of-truth live adjacent to `.agent.md` files or in a dedicated runtime schema registry?
3. What is the versioning strategy for adapter contracts to prevent routing regressions?
4. Which telemetry fields are mandatory for end-to-end specialization traceability?
5. Is an ADR required in design phase to codify specialization architecture and migration policy?

## Handoff Note
This @2think artifact is complete and in-scope. Recommended lead direction for @3design: **Option B** with explicit adapter contracts, policy-bound capability mapping, and parity-test requirements.