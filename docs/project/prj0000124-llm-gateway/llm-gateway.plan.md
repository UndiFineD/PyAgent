# llm-gateway - Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-04-04_

## Overview
Execution-ready roadmap for the hybrid split-plane LLM Gateway defined in:
- `docs/project/prj0000124-llm-gateway/llm-gateway.think.md`
- `docs/project/prj0000124-llm-gateway/llm-gateway.design.md`
- `docs/architecture/adr/0009-llm-gateway-hybrid-split-plane.md`

Plan objective: deliver phased implementation and verification steps across all 10 gateway capability pillars while preserving fail-closed governance and branch/scope discipline.

## Capability Pillar Mapping
| Pillar | Capability | Primary Tasks |
|---|---|---|
| P1 | Routing and load balancing | T-LGW-003, T-LGW-007, T-LGW-013 |
| P2 | Authentication and access control | T-LGW-002, T-LGW-014 |
| P3 | Token budgeting | T-LGW-005, T-LGW-012 |
| P4 | Guardrails and policy enforcement | T-LGW-002, T-LGW-008, T-LGW-014 |
| P5 | Semantic cache | T-LGW-006, T-LGW-012 |
| P6 | Model fallback | T-LGW-007, T-LGW-013 |
| P7 | Observability | T-LGW-009, T-LGW-015 |
| P8 | Context management | T-LGW-001, T-LGW-004 |
| P9 | Memory integration | T-LGW-010, T-LGW-012 |
| P10 | Tool and skill catchers | T-LGW-008, T-LGW-014 |

## Phase Plan
### Phase 1 - MVP In-Process Contracts and Baseline Capabilities
Scope: contracts + baseline behavior for all 10 pillars using Python in-process data plane.

### Phase 2 - Reliability and Safety Hardening
Scope: fail-closed enforcement depth, deterministic fallback behavior, poisoning/replay protections, stronger invariants.

### Phase 3 - Rust Acceleration and Service-Mode Path
Scope: parity-preserving migration of hot data-plane paths to Rust-backed implementations and optional service-mode seam.

## Task List
Each task includes objective, explicit files, owner role, dependencies, validation command(s), and AC mapping.

### Phase 1 Tasks
| Task ID | Phase | Parallel | Objective | Files In Scope | Owner | Dependencies | Validation Commands | Acceptance Criteria Mapping |
|---|---|---|---|---|---|---|---|---|
| T-LGW-001 | 1 | sequential-only | Create gateway envelope contracts and result/error models used across control/data planes. | `src/core/gateway/contracts.py`, `src/core/gateway/__init__.py`, `tests/core/gateway/test_contracts.py` | @6code (tests by @5test) | none | `python -m pytest -q tests/core/gateway/test_contracts.py` | AC-GW-002, AC-GW-003, AC-GW-007 |
| T-LGW-002 | 1 | parallel-safe | Implement `GatewayPolicyEngine` pre/post/tool decision contracts with deny-by-default and policy-version evidence. | `src/core/gateway/gateway_policy_engine.py`, `tests/core/gateway/test_gateway_policy_engine.py` | @6code (tests by @5test) | T-LGW-001 | `python -m pytest -q tests/core/gateway/test_gateway_policy_engine.py` | AC-GW-001, AC-GW-002, AC-GW-004 |
| T-LGW-003 | 1 | parallel-safe | Implement deterministic `GatewayRouter` route-plan contract including safe-default tie-break path. | `src/core/gateway/gateway_router.py`, `tests/core/gateway/test_gateway_router.py` | @6code (tests by @5test) | T-LGW-001 | `python -m pytest -q tests/core/gateway/test_gateway_router.py` | AC-GW-002, AC-GW-003, AC-GW-007 |
| T-LGW-004 | 1 | sequential-only | Implement `GatewayCore` orchestration sequence enforcing pre-policy, reserve-before-execute, and post-policy gates. | `src/core/gateway/gateway_core.py`, `tests/core/gateway/test_gateway_core_orchestration.py` | @6code (tests by @5test) | T-LGW-001, T-LGW-002, T-LGW-003, T-LGW-005, T-LGW-006, T-LGW-007, T-LGW-008, T-LGW-009 | `python -m pytest -q tests/core/gateway/test_gateway_core_orchestration.py` | AC-GW-001, AC-GW-003, AC-GW-004 |
| T-LGW-005 | 1 | parallel-safe | Implement `GatewayBudgetManager` reserve/commit contracts with idempotent commit keys. | `src/core/gateway/gateway_budget_manager.py`, `tests/core/gateway/test_gateway_budget_manager.py` | @6code (tests by @5test) | T-LGW-001 | `python -m pytest -q tests/core/gateway/test_gateway_budget_manager.py` | AC-GW-002, AC-GW-004 |
| T-LGW-006 | 1 | parallel-safe | Implement `GatewaySemanticCache` lookup/write contracts with policy-version route-aware cache key shape. | `src/core/gateway/gateway_semantic_cache.py`, `tests/core/gateway/test_gateway_semantic_cache.py` | @6code (tests by @5test) | T-LGW-001 | `python -m pytest -q tests/core/gateway/test_gateway_semantic_cache.py` | AC-GW-002, AC-GW-004 |
| T-LGW-007 | 1 | parallel-safe | Implement `GatewayFallbackManager` fallback plan contract aligned with routing taxonomy and circuit state inputs. | `src/core/gateway/gateway_fallback_manager.py`, `tests/core/gateway/test_gateway_fallback_manager.py` | @6code (tests by @5test) | T-LGW-001, T-LGW-003 | `python -m pytest -q tests/core/gateway/test_gateway_fallback_manager.py` | AC-GW-002, AC-GW-004, AC-GW-005 |
| T-LGW-008 | 1 | parallel-safe | Implement `ToolSkillCatcher` interception contracts for allow/deny/audit before tool execution. | `src/core/gateway/tool_skill_catcher.py`, `tests/core/gateway/test_tool_skill_catcher.py` | @6code (tests by @5test) | T-LGW-001, T-LGW-002 | `python -m pytest -q tests/core/gateway/test_tool_skill_catcher.py` | AC-GW-002, AC-GW-004 |
| T-LGW-009 | 1 | parallel-safe | Implement `GatewayTelemetryEmitter` correlation-safe event/metric/tracing contract wrapper. | `src/core/gateway/gateway_telemetry_emitter.py`, `tests/core/gateway/test_gateway_telemetry_emitter.py` | @6code (tests by @5test) | T-LGW-001 | `python -m pytest -q tests/core/gateway/test_gateway_telemetry_emitter.py` | AC-GW-002, AC-GW-003, AC-GW-005 |
| T-LGW-010 | 1 | sequential-only | Add backend integration seam for auth/tracing/memory adapters at gateway boundary (no behavior regression). | `backend/app.py`, `backend/auth.py`, `backend/tracing.py`, `backend/memory_store.py`, `tests/backend/test_gateway_integration_seams.py` | @6code (tests by @5test) | T-LGW-004, T-LGW-009 | `python -m pytest -q tests/backend/test_gateway_integration_seams.py` | AC-GW-003, AC-GW-005 |
| T-LGW-011 | 1 | sequential-only | Add provider runtime adapter over existing FLM adapter and typed provider error mapping. | `src/core/gateway/provider_runtime_adapter.py`, `src/core/providers/FlmChatAdapter.py`, `tests/core/gateway/test_provider_runtime_adapter.py` | @6code (tests by @5test) | T-LGW-001, T-LGW-003 | `python -m pytest -q tests/core/gateway/test_provider_runtime_adapter.py` | AC-GW-002, AC-GW-005 |

### Phase 1 Convergence Step
- T-LGW-011.5 (sequential-only, convergence owner: @0master decision + @6code execution)
  - Merge outputs from all phase-1 parallel-safe tasks (`T-LGW-002`, `T-LGW-003`, `T-LGW-005`, `T-LGW-006`, `T-LGW-007`, `T-LGW-008`, `T-LGW-009`) into the canonical orchestration path in `src/core/gateway/gateway_core.py` and integration seam tests.
  - Convergence validation commands:
	 - `python -m pytest -q tests/core/gateway`
	 - `python -m pytest -q tests/backend/test_gateway_integration_seams.py`

### Phase 2 Tasks
| Task ID | Phase | Parallel | Objective | Files In Scope | Owner | Dependencies | Validation Commands | Acceptance Criteria Mapping |
|---|---|---|---|---|---|---|---|---|
| T-LGW-012 | 2 | parallel-safe | Enforce budget/cache/memory atomicity and replay-safe commit semantics. | `src/core/gateway/gateway_budget_manager.py`, `src/core/gateway/gateway_semantic_cache.py`, `src/core/gateway/gateway_core.py`, `tests/core/gateway/test_gateway_atomicity.py` | @6code (tests by @5test) | Phase 1 complete | `python -m pytest -q tests/core/gateway/test_gateway_atomicity.py` | AC-GW-004 |
| T-LGW-013 | 2 | parallel-safe | Harden fallback determinism under provider timeouts/errors and circuit transitions. | `src/core/gateway/gateway_fallback_manager.py`, `src/core/gateway/provider_runtime_adapter.py`, `src/core/resilience/CircuitBreakerRegistry.py`, `tests/core/gateway/test_gateway_fallback_determinism.py` | @6code (tests by @5test) | Phase 1 complete | `python -m pytest -q tests/core/gateway/test_gateway_fallback_determinism.py` | AC-GW-004, AC-GW-005 |
| T-LGW-014 | 2 | parallel-safe | Harden fail-closed policy and tool interception for malformed context, policy outages, and unsafe responses. | `src/core/gateway/gateway_policy_engine.py`, `src/core/gateway/tool_skill_catcher.py`, `src/core/gateway/gateway_core.py`, `tests/core/gateway/test_gateway_fail_closed_paths.py` | @6code (tests by @5test) | Phase 1 complete | `python -m pytest -q tests/core/gateway/test_gateway_fail_closed_paths.py` | AC-GW-001, AC-GW-004 |
| T-LGW-015 | 2 | sequential-only | Add reliability observability dashboards/signals contracts and degraded-telemetry behavior checks. | `src/core/gateway/gateway_telemetry_emitter.py`, `backend/tracing.py`, `tests/core/gateway/test_gateway_telemetry_reliability.py` | @6code (tests by @5test) | T-LGW-009 | `python -m pytest -q tests/core/gateway/test_gateway_telemetry_reliability.py` | AC-GW-003, AC-GW-004 |

### Phase 2 Convergence Step
- T-LGW-015.5 (sequential-only, convergence owner: @0master decision + @6code execution)
  - Consolidate hardening behavior into one deterministic integration slice.
  - Convergence validation commands:
	 - `python -m pytest -q tests/core/gateway/test_gateway_atomicity.py tests/core/gateway/test_gateway_fallback_determinism.py tests/core/gateway/test_gateway_fail_closed_paths.py tests/core/gateway/test_gateway_telemetry_reliability.py`

### Phase 3 Tasks
| Task ID | Phase | Parallel | Objective | Files In Scope | Owner | Dependencies | Validation Commands | Acceptance Criteria Mapping |
|---|---|---|---|---|---|---|---|---|
| T-LGW-016 | 3 | parallel-safe | Introduce Rust-backed semantic cache/budget adapter interfaces with parity contract tests (no behavior drift). | `src/core/gateway/gateway_budget_manager.py`, `src/core/gateway/gateway_semantic_cache.py`, `rust_core/`, `tests/core/gateway/test_gateway_rust_parity.py` | @6code (tests by @5test) | Phase 2 complete | `python -m pytest -q tests/core/gateway/test_gateway_rust_parity.py` | AC-GW-006 |
| T-LGW-017 | 3 | parallel-safe | Add optional service-mode adapter seam while preserving in-process default and envelope compatibility. | `src/core/gateway/gateway_core.py`, `src/core/gateway/provider_runtime_adapter.py`, `backend/app.py`, `tests/core/gateway/test_gateway_service_mode_compat.py` | @6code (tests by @5test) | T-LGW-016 | `python -m pytest -q tests/core/gateway/test_gateway_service_mode_compat.py` | AC-GW-006 |
| T-LGW-018 | 3 | sequential-only | Final parity and migration gate package for Rust/service-mode path with rollback triggers documented. | `docs/architecture/adr/0009-llm-gateway-hybrid-split-plane.md`, `docs/project/prj0000124-llm-gateway/llm-gateway.plan.md`, `tests/core/gateway/test_gateway_phase3_parity_gate.py` | @6code (tests by @5test, governance by @8ql) | T-LGW-016, T-LGW-017 | `python -m pytest -q tests/core/gateway/test_gateway_phase3_parity_gate.py` | AC-GW-006, AC-GW-008 |

## Acceptance Criteria Traceability
| AC ID | Definition | Planned Tasks |
|---|---|---|
| AC-GW-001 | Explicit split-plane fail-closed boundary rules | T-LGW-002, T-LGW-004, T-LGW-014 |
| AC-GW-002 | All 9 interfaces implemented with callable contracts | T-LGW-001, T-LGW-002, T-LGW-003, T-LGW-005, T-LGW-006, T-LGW-007, T-LGW-008, T-LGW-009, T-LGW-011 |
| AC-GW-003 | End-to-end lifecycle covers all 10 pillars | T-LGW-004, T-LGW-009, T-LGW-010, T-LGW-015 |
| AC-GW-004 | Error matrix and fail-closed outcomes verified | T-LGW-004, T-LGW-012, T-LGW-013, T-LGW-014 |
| AC-GW-005 | Existing integration points mapped and wired | T-LGW-007, T-LGW-010, T-LGW-011, T-LGW-013 |
| AC-GW-006 | MVP -> hardening -> Rust/service phase constraints preserved | T-LGW-016, T-LGW-017, T-LGW-018 |
| AC-GW-007 | Interface-to-task traceability implemented | T-LGW-001, T-LGW-003 |
| AC-GW-008 | ADR alignment and architectural continuity | T-LGW-018 |

## Initial RED Slice For @5test
Start with one deterministic RED slice before broad fan-out:

1. RED-SLICE-LGW-001
	- Write: `tests/core/gateway/test_gateway_core_orchestration.py`
	- Assertions to fail first:
	  - no provider execute when pre-policy denies
	  - budget reserve must occur before provider execute
	  - post-policy deny prevents cache write and tool dispatch
	  - result envelope always contains decision/budget/telemetry sections
	- Selector to run first:
	  - `python -m pytest -q tests/core/gateway/test_gateway_core_orchestration.py -k fail_closed`

2. After RED-SLICE-LGW-001, expand to contract unit slices in this order:
	- `python -m pytest -q tests/core/gateway/test_gateway_policy_engine.py`
	- `python -m pytest -q tests/core/gateway/test_gateway_budget_manager.py`
	- `python -m pytest -q tests/core/gateway/test_gateway_semantic_cache.py`

## Execution Gates (@7exec)
@7exec must not mark DONE unless all gates pass with non-interrupted output:

1. Phase-1 integration gate
	- `python -m pytest -q tests/core/gateway tests/backend/test_gateway_integration_seams.py`
2. Policy docs gate (mandatory for project artifact changes)
	- `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py`
3. Targeted regression gate around impacted integration points
	- `python -m pytest -q tests/backend -k "gateway or auth or tracing"`

Failure handling rule: rerun the exact failing selector first after each fix; only then rerun broader suites.

## Quality/Security Gates (@8ql)
@8ql quality closure requires evidence for:

1. Fail-closed coverage for policy/auth/budget/tool paths
	- `python -m pytest -q tests/core/gateway/test_gateway_fail_closed_paths.py`
2. Deterministic fallback and timeout handling
	- `python -m pytest -q tests/core/gateway/test_gateway_fallback_determinism.py`
3. Static quality/security checks on gateway and backend seams
	- `python -m mypy src/core/gateway backend`
	- `python -m ruff check src/core/gateway backend tests/core/gateway tests/backend`

## Git/Handoff Conditions (@9git)
@9git must enforce all of the following before commit/push/PR:

1. Branch gate:
	- `git branch --show-current` must equal `prj0000124-llm-gateway`.
2. Scope gate:
	- staged changes must remain within project-approved boundary for this phase.
3. Narrow staging only:
	- no blanket `git add .`.
4. Required evidence attached to handoff:
	- RED selector evidence from @5test
	- runtime gate evidence from @7exec
	- quality gate evidence from @8ql
5. Commit message format for this plan artifact update:
	- `feat(prj0000124): produce llm-gateway implementation roadmap`

## Milestones
| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | Phase 1 MVP contracts and baseline integration | T-LGW-001..T-LGW-011.5 | PLANNED |
| M2 | Phase 2 reliability/safety hardening | T-LGW-012..T-LGW-015.5 | PLANNED |
| M3 | Phase 3 rust/service evolution with parity gates | T-LGW-016..T-LGW-018 | PLANNED |

## Deterministic Validation Commands
```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1

# Branch and scope evidence
git branch --show-current
git status --short

# Documentation policy gate for project artifacts
python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py

# Initial red slice selector for @5test
python -m pytest -q tests/core/gateway/test_gateway_core_orchestration.py -k fail_closed
```
