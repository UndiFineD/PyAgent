# prj0000088-ai-fuzzing-security - Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-03-27_

## Root Cause Analysis
1. The active codebase currently has no first-class fuzzing engine module in `src/`, while prior project artifacts reference legacy fuzzing paths and planned fuzzing capabilities.
2. Existing project direction asks for AI-assisted fuzzing, but a safe v1 must stay deterministic, local, and free of external network calls.
3. The repository already has reusable safety and orchestration primitives (tool registry, process transaction wrapper, branch/scope governance) that can host a minimal fuzzing engine without broad architecture churn.

## Step 1 Research Evidence
| Task Type | Findings | Evidence |
|---|---|---|
| Literature review | Project scope explicitly frames AI fuzzing with learning-based path discovery and local-model-assisted generation, but this phase is options-only and not implementation. | `docs/project/prj0000088-ai-fuzzing-security/prj0000088-ai-fuzzing-security.project.md` |
| Alternative enumeration | Prior 2think work demonstrates a 3-option matrix approach with deterministic-first framing and clear blast-radius analysis. | `docs/project/prj0000085-shadow-mode-replay/prj0000085-shadow-mode-replay.think.md` |
| Prior-art search | Historical architecture notes already identify intended fuzzing integration seams and local model context. | `docs/architecture/archive/overview.md`, `docs/architecture/archive/planner.agent.memory.md` |
| Constraint mapping | One-project-one-branch, project scope boundaries, and discovery-lane governance are mandatory for this artifact. | `docs/project/prj0000088-ai-fuzzing-security/prj0000088-ai-fuzzing-security.project.md`, `docs/project/kanban.md`, `/memories/repo/branch-governance.md` |
| Stakeholder impact | Existing tool dispatch and security/process wrappers show where fuzzing can integrate with low coupling. | `src/tools/tool_registry.py`, `src/core/security_bridge.py`, `src/transactions/ProcessTransactionManager.py` |
| Risk enumeration | Legacy references indicate missing/uncertain fuzzing API assumptions (`fuzz_async`, corpus/seed handling), reinforcing need for minimal deterministic v1 boundaries. | `docs/architecture/archive/tester.agent.memory.md`, `docs/project/prj0000037/prj037-tools-crdt-security.code.md` |

## Constraints (Explicit)
- Must remain in `docs/project/prj0000088-ai-fuzzing-security/` for @2think output; no runtime code changes in this phase.
- Must recommend a v1 that is local and deterministic.
- Must enforce no external network calls for fuzz execution in v1.
- Must fit budget tier M and Discovery scope: option quality over implementation breadth.
- Must define guardrails suitable for downstream @3design to codify.

## Options
### Option A - Deterministic Local Mutation Engine (Rule-Based, No Model Runtime)
**Approach**
- Build a minimal local fuzzing core around seeded corpus + deterministic mutation operators only.
- Mutation strategies in v1:
	- byte_flip (indexed bit/byte flip by seeded PRNG)
	- boundary_splice (insert/remove boundary values and delimiters)
	- structure_stress (depth/length amplification for JSON-like payloads)
	- token_substitution (dictionary-based replacements from local static tables)
- Use seeded run IDs and deterministic mutation scheduling (`seed`, `cycle`, `operator`, `input_index`).
- Enforce hard guardrails: no sockets, no HTTP clients, no subprocess shell strings, bounded exec/time/memory budgets, and explicit allowlist of local targets.

**Research coverage used**
- Literature review: AI fuzzing goals and mutation concepts.
- Constraint mapping: no-external-call and deterministic v1 boundaries.
- Stakeholder impact: low-coupling integration through tool registry and process wrapper.
- Prior-art search: historical fuzzing references and missing API lessons.
- Risk enumeration: safety bypass, determinism drift, and corpus blowup risks.

**Pros**
- Smallest v1 surface and lowest operational risk.
- Strong reproducibility for triage and regression.
- No dependency on local model serving availability.

**Cons**
- Lower semantic mutation quality than model-assisted strategies.
- May miss protocol/stateful edge cases without richer generators.
- Requires careful operator tuning to avoid shallow path coverage.

**Stakeholder impact**
- Low-medium impact: @3design and @4plan define contracts and sequencing.
- Medium impact: @5test creates deterministic fixtures and seed replay checks.
- Low impact: @7exec can validate local-only behavior quickly.

**Failure modes (likelihood/impact)**
1. Guardrail bypass permits unintended external call path (L/H).
2. Seed handling bug causes non-reproducible results (M/H).
3. Mutation corpus growth causes local resource spikes (M/M).

**Workspace evidence**
- `docs/Key/ai_fuzzing.md`
- `src/tools/tool_registry.py`
- `src/transactions/ProcessTransactionManager.py`
- `docs/architecture/archive/tester.agent.memory.md`

### Option B - Deterministic Engine + Local Model Mutator Plug-In (Disabled by Default)
**Approach**
- Keep Option A core, but add a plug-in interface for a local model mutator adapter.
- Adapter can generate structured edge-case candidates from seed payloads, but only when an explicit local-only feature flag is enabled.
- Default mode remains deterministic rule-based operators; model outputs are normalized/canonicalized before scheduling.

**Research coverage used**
- Literature review: local-model-assisted fuzzing direction.
- Alternative enumeration: strict deterministic-only vs extensible local-model architecture.
- Prior-art search: planned Ollama/local-model integration references.
- Constraint mapping: local-only and no external call guarantees still required.
- Stakeholder impact: broader blast radius into model infrastructure.
- Risk enumeration: determinism and adapter complexity risks.

**Pros**
- Better long-term path coverage potential while preserving deterministic default.
- Clear migration path toward AI-assisted mutations without re-architecting core.
- Allows phased rollout under explicit flags.

**Cons**
- Higher v1 complexity than needed for immediate goals.
- Determinism controls become harder once generative outputs are included.
- Additional security review needed for adapter boundaries.

**Stakeholder impact**
- Medium-high impact: @3design must define adapter contracts and policy gates.
- Medium impact: model/platform owners for local adapter lifecycle.
- Medium impact: @5test must support dual-path test matrix.

**Failure modes (likelihood/impact)**
1. Local model output variance weakens deterministic replay expectations (M/H).
2. Adapter path accidentally introduces non-local API behavior (L/H).
3. Feature-flag logic drift causes inconsistent execution mode (M/M).

**Workspace evidence**
- `docs/project/kanban.md`
- `docs/architecture/archive/overview.md`
- `docs/architecture/archive/planner.agent.memory.md`
- `src/core/security_bridge.py`

### Option C - High-Throughput Async Fuzzing Pipeline with Multi-Stage Learning Loop
**Approach**
- Build a larger asynchronous orchestration layer for multi-cycle campaigns with scoring, corpus prioritization, and strategy adaptation each cycle.
- Integrate process isolation, checkpointing, coverage heuristics, and campaign analytics from day one.
- Include a broad plugin ecosystem for mutators and target adapters.

**Research coverage used**
- Alternative enumeration: fully featured campaign architecture path.
- Prior-art search: historical ambitions for multi-cycle and AI fuzzing.
- Constraint mapping: conflicts with Discovery-phase and minimal-v1 expectations.
- Stakeholder impact: high cross-cutting impact on tooling, runtime, and testing.
- Risk enumeration: schedule, complexity, and operational safety risks.

**Pros**
- Highest theoretical coverage and extensibility.
- Rich campaign telemetry and future-proof architecture.
- Better support for advanced fuzzing workflows.

**Cons**
- Over-scoped for v1 and budget M discovery intent.
- Largest blast radius and highest delivery risk.
- Hard to validate safely without significant additional guardrail work.

**Stakeholder impact**
- High impact: @3design through @8ql across multiple subsystems.
- High impact: CI/test infra due to campaign-scale fixture requirements.
- High operational burden for deterministic guarantees.

**Failure modes (likelihood/impact)**
1. Multi-stage scheduler introduces nondeterministic ordering bugs (H/H).
2. Guardrail policy fragmentation across plugins creates safety gaps (M/H).
3. Delivery timeline slips before usable security value is reached (H/M).

**Workspace evidence**
- `docs/architecture/archive/overview.md`
- `docs/architecture/archive/tester.agent.memory.md`
- `docs/architecture/archive/planner.agent.memory.md`
- `docs/project/prj0000088-ai-fuzzing-security/prj0000088-ai-fuzzing-security.project.md`

## Decision Matrix
| Criterion | Option A | Option B | Option C |
|---|---|---|---|
| Scope fit for minimal v1 | High | Medium | Low |
| Determinism strength | High | Medium | Low-Medium |
| Safety/no-external-call clarity | High | Medium | Medium |
| Implementation complexity | Low | Medium | High |
| Time-to-first-value | High | Medium | Low |
| Long-term extensibility | Medium | High | High |
| Overall delivery risk | Low | Medium | High |

## Recommendation
**Option A - Deterministic Local Mutation Engine (Rule-Based, No Model Runtime)**

Rationale:
1. Best alignment with requested outcome: minimal v1, local deterministic behavior, and explicit no-external-call guardrails.
2. Lowest blast radius while still delivering meaningful mutation strategy coverage.
3. Most testable and auditable baseline for downstream design, plan, and security verification.
4. Leaves a clean optional extension seam for local model mutators in a later phase without coupling v1 to model runtime volatility.

## Integration Points
1. `src/tools/tool_registry.py`: register a dedicated fuzzing tool entrypoint for deterministic campaign execution.
2. `src/transactions/ProcessTransactionManager.py`: run target commands under bounded timeout and deterministic capture behavior.
3. `src/core/security_bridge.py`: reuse strict local binary invocation patterns for guarded subprocess interactions.
4. `src/core/base/base_agent.py`: optional agent orchestration hook to schedule deterministic fuzzing runs without direct runtime coupling.
5. `tests/` conventions (pattern from prior projects): add seed replay fixtures and guardrail contract tests in dedicated fuzzing test modules during @5test.
6. Legacy alignment note: prior references to `src-old/tools/security/fuzzing.py` in `docs/project/prj0000037/prj037-tools-crdt-security.code.md` should be treated as historical context, not active path dependency.

## Open Questions
1. Which target classes are in v1 scope: CLI parsers, API payload validators, or file-format handlers?
2. What is the minimum required mutation operator set for acceptance (3 vs 4 vs 5 operators)?
3. Should deterministic campaign IDs be derived from `(seed, target, config)` hash or explicit run metadata?
4. What hard execution budgets should be default in v1 (`max_cases`, per-case timeout, total runtime cap)?
5. Which guardrail enforcement layer is authoritative: tool runner, process transaction wrapper, or both?
6. How should corpus persistence be handled in v1: in-memory only, local file snapshots, or transaction-backed store?
