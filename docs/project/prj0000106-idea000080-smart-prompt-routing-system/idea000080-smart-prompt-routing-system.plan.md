# idea000080-smart-prompt-routing-system - Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-03-30_

## Overview
Deliver the hybrid smart prompt routing system selected in design (Option B) using deterministic guardrail precedence, classifier-assisted ambiguity handling, deterministic tie-break controls, fail-closed fallback, and redacted provenance telemetry.

Execution is split into two implementation chunks sized around ~10 code files and ~10 test files each so @5test and @6code can work incrementally with clear gates.

## Requirements & Constraints
- REQ-SPR-001: Implement `PromptRoutingFacade` async contract that always returns a route decision or explicit fail-closed fallback.
- REQ-SPR-002: Enforce absolute guardrail precedence over classifier and tie-break outcomes.
- REQ-SPR-003: Emit schema-valid classifier results with bounded confidence values.
- REQ-SPR-004: Tie-break resolver must be deterministic and bounded by timeout.
- REQ-SPR-005: Fallback policy must trigger on timeout/schema/provider failures.
- REQ-SPR-006: Shadow and active modes must produce the same route decision for same input+policy version.
- REQ-SPR-007: Telemetry must include required provenance fields and redaction guarantees.
- CON-SPR-001: Branch must remain `prj0000106-idea000080-smart-prompt-routing-system`.
- CON-SPR-002: Naming and docs must comply with `docs/project/naming_standards.md` and `docs/project/code_of_conduct.md`.
- CON-SPR-003: @4plan only produces executable plan artifacts and lifecycle docs/memory updates; no production code or test implementation in this stage.
- GUD-SPR-001: Every task must include objective, target files, acceptance criteria, and at least one validation command.

## Chunk Plan

### Chunk A - Guardrail-First Routing Core (Target: ~10 code files, ~10 test files)

Code file set:
1. `src/core/routing/prompt_routing_facade.py`
2. `src/core/routing/guardrail_policy_engine.py`
3. `src/core/routing/routing_models.py`
4. `src/core/routing/request_normalizer.py`
5. `src/core/routing/routing_policy_loader.py`
6. `src/core/routing/policy_versioning.py`
7. `src/core/universal/UniversalIntentRouter.py`
8. `src/core/workflow/engine.py`
9. `src/core/resilience/CircuitBreakerCore.py`
10. `src/core/observability.py`

Test file set:
1. `tests/core/routing/test_prompt_routing_facade.py`
2. `tests/core/routing/test_guardrail_policy_engine.py`
3. `tests/core/routing/test_request_normalizer.py`
4. `tests/core/routing/test_routing_policy_loader.py`
5. `tests/core/routing/test_policy_versioning.py`
6. `tests/test_UniversalIntentRouter.py`
7. `tests/test_workflow_engine.py`
8. `tests/core/routing/test_guardrail_precedence_contract.py`
9. `tests/core/routing/test_fail_closed_fallback_contract.py`
10. `tests/core/routing/test_shadow_active_contract_scaffold.py`

### Chunk B - Ambiguity Resolution, Fallback, and Telemetry (Target: ~10 code files, ~10 test files)

Code file set:
1. `src/core/routing/prompt_semantic_classifier.py`
2. `src/core/routing/classifier_schema.py`
3. `src/core/routing/confidence_calibration.py`
4. `src/core/routing/tie_break_resolver.py`
5. `src/core/routing/routing_fallback_policy.py`
6. `src/core/routing/fallback_reason_taxonomy.py`
7. `src/core/routing/routing_telemetry_emitter.py`
8. `src/core/routing/shadow_mode_router.py`
9. `src/core/providers/FlmModelProbe.py`
10. `backend/tracing.py`

Test file set:
1. `tests/core/routing/test_prompt_semantic_classifier.py`
2. `tests/core/routing/test_classifier_schema.py`
3. `tests/core/routing/test_confidence_calibration.py`
4. `tests/core/routing/test_tie_break_resolver.py`
5. `tests/core/routing/test_tie_break_timeout.py`
6. `tests/core/routing/test_routing_fallback_policy.py`
7. `tests/core/routing/test_fallback_reason_taxonomy.py`
8. `tests/core/routing/test_routing_telemetry_emitter.py`
9. `tests/core/routing/test_shadow_active_parity.py`
10. `tests/core/routing/test_telemetry_redaction.py`

## AC to Task Phase Mapping
| AC | Requirement | Phase owner | Planned tasks |
|---|---|---|---|
| AC-SPR-001 | Facade returns route decision or safe fallback | @5test -> @6code | T-SPR-001, T-SPR-002 |
| AC-SPR-002 | Guardrail precedence is absolute | @5test -> @6code | T-SPR-003, T-SPR-004 |
| AC-SPR-003 | Classifier schema + confidence bounds | @5test -> @6code | T-SPR-005, T-SPR-006 |
| AC-SPR-004 | Deterministic tie-break | @5test -> @6code | T-SPR-007 |
| AC-SPR-005 | Fail-closed fallback on faults | @5test -> @6code | T-SPR-008 |
| AC-SPR-006 | Shadow-active parity | @5test -> @6code | T-SPR-009 |
| AC-SPR-007 | Tie-break timeout bound + reason telemetry | @5test -> @6code | T-SPR-010 |
| AC-SPR-008 | Provenance telemetry schema + redaction | @5test -> @6code | T-SPR-011 |

## Task List (Executable, Ordered)

### Phase 1 - @5test Red-Phase Contract Coverage
| Task ID | Objective | Target files | Acceptance criteria | Validation command |
|---|---|---|---|---|
| T-SPR-001 | Author facade contract tests for success/fallback envelope behavior | `tests/core/routing/test_prompt_routing_facade.py`, `tests/core/routing/test_fail_closed_fallback_contract.py` | AC-SPR-001 red-phase tests fail for missing/incorrect facade behavior with deterministic assertions | `python -m pytest -q tests/core/routing/test_prompt_routing_facade.py tests/core/routing/test_fail_closed_fallback_contract.py` |
| T-SPR-002 | Add shadow/active parity contract tests with policy-version fixture | `tests/core/routing/test_shadow_active_parity.py`, `tests/core/routing/test_shadow_active_contract_scaffold.py` | AC-SPR-006 parity assertions fail until implementation is present | `python -m pytest -q tests/core/routing/test_shadow_active_parity.py -k parity` |
| T-SPR-003 | Add guardrail precedence adversarial tests | `tests/core/routing/test_guardrail_policy_engine.py`, `tests/core/routing/test_guardrail_precedence_contract.py` | AC-SPR-002 contract proves classifier/tie-break cannot override guardrail route | `python -m pytest -q tests/core/routing/test_guardrail_policy_engine.py tests/core/routing/test_guardrail_precedence_contract.py -k precedence` |
| T-SPR-004 | Add router integration guardrail-first path tests | `tests/test_UniversalIntentRouter.py`, `tests/test_workflow_engine.py` | AC-SPR-001 and AC-SPR-002 route dispatch integration expectations are explicit | `python -m pytest -q tests/test_UniversalIntentRouter.py tests/test_workflow_engine.py` |
| T-SPR-005 | Add classifier schema validation tests | `tests/core/routing/test_prompt_semantic_classifier.py`, `tests/core/routing/test_classifier_schema.py` | AC-SPR-003 schema invalid outputs fail with clear reason taxonomy | `python -m pytest -q tests/core/routing/test_prompt_semantic_classifier.py tests/core/routing/test_classifier_schema.py` |
| T-SPR-006 | Add confidence calibration boundary tests | `tests/core/routing/test_confidence_calibration.py` | AC-SPR-003 confidence values are bounded/calibrated and deterministic | `python -m pytest -q tests/core/routing/test_confidence_calibration.py` |
| T-SPR-007 | Add deterministic replay tests for tie-break resolution | `tests/core/routing/test_tie_break_resolver.py` | AC-SPR-004 route outcome remains identical across repeated deterministic runs | `python -m pytest -q tests/core/routing/test_tie_break_resolver.py -k deterministic` |
| T-SPR-008 | Add fail-closed tests for timeout/schema/provider faults | `tests/core/routing/test_routing_fallback_policy.py`, `tests/core/routing/test_fallback_reason_taxonomy.py` | AC-SPR-005 fallback path triggers with explicit reason code for each injected fault | `python -m pytest -q tests/core/routing/test_routing_fallback_policy.py tests/core/routing/test_fallback_reason_taxonomy.py` |
| T-SPR-010 | Add timeout boundary and telemetry reason assertions | `tests/core/routing/test_tie_break_timeout.py` | AC-SPR-007 tie-break timeout is bounded and timeout reason recorded | `python -m pytest -q tests/core/routing/test_tie_break_timeout.py` |
| T-SPR-011 | Add telemetry schema + redaction tests | `tests/core/routing/test_routing_telemetry_emitter.py`, `tests/core/routing/test_telemetry_redaction.py` | AC-SPR-008 validates required fields, correlation IDs, and redaction of sensitive content | `python -m pytest -q tests/core/routing/test_routing_telemetry_emitter.py tests/core/routing/test_telemetry_redaction.py` |

### Phase 2 - @6code Green-Phase Implementation
| Task ID | Objective | Target files | Acceptance criteria | Validation command |
|---|---|---|---|---|
| T-SPR-012 | Implement facade, request normalization, policy loading, and decision model wiring | `src/core/routing/prompt_routing_facade.py`, `src/core/routing/request_normalizer.py`, `src/core/routing/routing_models.py`, `src/core/routing/routing_policy_loader.py`, `src/core/routing/policy_versioning.py` | AC-SPR-001 and AC-SPR-006 pass for contract and parity fixtures | `python -m pytest -q tests/core/routing/test_prompt_routing_facade.py tests/core/routing/test_shadow_active_parity.py` |
| T-SPR-013 | Implement deterministic guardrail engine and integrate guardrail-first routing path | `src/core/routing/guardrail_policy_engine.py`, `src/core/universal/UniversalIntentRouter.py`, `src/core/workflow/engine.py` | AC-SPR-002 precedence tests pass without regressions in integration routing behavior | `python -m pytest -q tests/core/routing/test_guardrail_precedence_contract.py tests/test_UniversalIntentRouter.py tests/test_workflow_engine.py` |
| T-SPR-014 | Implement classifier, schema validation, and confidence calibration pipeline | `src/core/routing/prompt_semantic_classifier.py`, `src/core/routing/classifier_schema.py`, `src/core/routing/confidence_calibration.py` | AC-SPR-003 schema and confidence tests pass deterministically | `python -m pytest -q tests/core/routing/test_prompt_semantic_classifier.py tests/core/routing/test_classifier_schema.py tests/core/routing/test_confidence_calibration.py` |
| T-SPR-015 | Implement deterministic tie-break resolver with strict timeout controls | `src/core/routing/tie_break_resolver.py`, `src/core/resilience/CircuitBreakerCore.py` | AC-SPR-004 and AC-SPR-007 deterministic replay and timeout boundary tests pass | `python -m pytest -q tests/core/routing/test_tie_break_resolver.py tests/core/routing/test_tie_break_timeout.py` |
| T-SPR-016 | Implement fail-closed fallback policy and reason taxonomy | `src/core/routing/routing_fallback_policy.py`, `src/core/routing/fallback_reason_taxonomy.py` | AC-SPR-005 fault-injection tests pass and reasons are explicit and stable | `python -m pytest -q tests/core/routing/test_routing_fallback_policy.py tests/core/routing/test_fallback_reason_taxonomy.py` |
| T-SPR-017 | Implement telemetry emitter, redaction policy, and trace propagation | `src/core/routing/routing_telemetry_emitter.py`, `src/core/observability.py`, `backend/tracing.py`, `src/core/providers/FlmModelProbe.py` | AC-SPR-008 schema+redaction tests pass and trace IDs are emitted end-to-end | `python -m pytest -q tests/core/routing/test_routing_telemetry_emitter.py tests/core/routing/test_telemetry_redaction.py` |
| T-SPR-018 | Implement shadow-mode router and parity wiring for active-mode path | `src/core/routing/shadow_mode_router.py`, `src/core/routing/prompt_routing_facade.py`, `src/core/workflow/engine.py` | AC-SPR-006 parity and facade contract tests pass together | `python -m pytest -q tests/core/routing/test_shadow_active_parity.py tests/core/routing/test_prompt_routing_facade.py` |

### Phase 3 - @7exec and @8ql Validation Gates
| Task ID | Objective | Target files | Acceptance criteria | Validation command |
|---|---|---|---|---|
| T-SPR-019 | Execute AC-focused deterministic suite and capture runtime evidence | `docs/project/prj0000106-idea000080-smart-prompt-routing-system/idea000080-smart-prompt-routing-system.exec.md` | AC-SPR-001..AC-SPR-008 evidence captured with conclusive pass/fail outcomes | `python -m pytest -q tests/core/routing` |
| T-SPR-020 | Execute quality/security checks for routing changes | `docs/project/prj0000106-idea000080-smart-prompt-routing-system/idea000080-smart-prompt-routing-system.ql.md` | No unresolved security/quality blockers for route/fallback/telemetry paths | `python -m ruff check src/core/routing tests/core/routing; python -m mypy src/core/routing` |

### Phase 4 - @9git Handoff
| Task ID | Objective | Target files | Acceptance criteria | Validation command |
|---|---|---|---|---|
| T-SPR-021 | Prepare narrow-scoped staging and branch-safe handoff artifacts | `docs/project/prj0000106-idea000080-smart-prompt-routing-system/idea000080-smart-prompt-routing-system.git.md` | Staged files are in-scope for project branch and include required evidence links | `git status --short; git diff -- docs/project/prj0000106-idea000080-smart-prompt-routing-system` |

## Dependency Order
1. @5test completes red-phase tasks T-SPR-001..T-SPR-011.
2. @6code implements T-SPR-012..T-SPR-018 to satisfy failing tests.
3. @7exec runs T-SPR-019 runtime validation.
4. @8ql runs T-SPR-020 quality/security closure.
5. @9git executes T-SPR-021 narrow commit/push/PR handoff.

## Milestones
| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | Plan finalized and AC-mapped | T-SPR-001..T-SPR-021 defined | DONE |
| M2 | Red-phase tests authored | T-SPR-001..T-SPR-011 | NOT_STARTED |
| M3 | Green-phase implementation complete | T-SPR-012..T-SPR-018 | NOT_STARTED |
| M4 | Runtime + quality closure | T-SPR-019..T-SPR-020 | NOT_STARTED |
| M5 | Git handoff completion | T-SPR-021 | NOT_STARTED |

## Handoff Notes
- Primary downstream target: @5test.
- @5test starts with T-SPR-001 and must keep test file scope inside listed chunk files.
- @6code must not introduce placeholders; each task must ship working logic meeting assertions.
- If branch mismatch occurs at any downstream step, lifecycle returns to @0master as BLOCKED.

## Validation Commands
```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
python -m pytest -q tests/core/routing
python -m ruff check src/core/routing tests/core/routing
python -m mypy src/core/routing
```

## Validation Evidence (@4plan)
- Docs policy gate: `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py`
- Result: `12 passed in 1.59s` (2026-03-30)
