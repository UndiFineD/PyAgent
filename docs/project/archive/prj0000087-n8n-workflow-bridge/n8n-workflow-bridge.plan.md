# n8n-workflow-bridge - Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-03-27_

## Overview
Deliver v1 of the n8n bridge using strict TDD sequencing for the selected design (stdlib-only HTTP integration + event adapter).

Scope includes:
1. New bridge package under `src/core/n8nbridge/`.
2. Exactly 18 tests mapped to acceptance criteria before production implementation.
3. Deterministic implementation order with explicit dependency chain for @5test and @6code handoff.

Out of scope:
1. Queue-based durability.
2. External dependency additions beyond existing repository stack.
3. Non-v1 schema contracts.

## Constraints and Conventions
1. Branch must remain `prj0000087-n8n-workflow-bridge`.
2. Keep implementation stdlib-first for transport (`urllib.request`).
3. Use typed error taxonomy from design.
4. No placeholder or skeleton deliverables; each task must produce runnable logic.
5. TDD order is mandatory: tests first, then implementation, then validation gates.

## Implementation Order (TDD)
### Phase P1 - Contract and Config Foundation
- [ ] T1 - Define bridge errors and package exports
	- Files: `src/core/n8nbridge/exceptions.py`, `src/core/n8nbridge/__init__.py`
	- Acceptance: AC-01
- [ ] T2 - Implement config model/env loading/validation
	- Files: `src/core/n8nbridge/N8nBridgeConfig.py`
	- Acceptance: AC-01
- [ ] T3 - Author config tests first (RT-01..RT-03)
	- Files: `tests/core/n8nbridge/test_N8nBridgeConfig.py`
	- Acceptance: AC-01

### Phase P2 - Event Contract Adapter
- [ ] T4 - Author adapter tests first (RT-04..RT-07)
	- Files: `tests/core/n8nbridge/test_N8nEventAdapter.py`
	- Acceptance: AC-02
- [ ] T5 - Implement adapter mappings and schema enforcement
	- Files: `src/core/n8nbridge/N8nEventAdapter.py`
	- Acceptance: AC-02

### Phase P3 - HTTP Transport
- [ ] T6 - Author HTTP client tests first (RT-08..RT-11)
	- Files: `tests/core/n8nbridge/test_N8nHttpClient.py`
	- Acceptance: AC-03
- [ ] T7 - Implement stdlib transport with timeout/retry/header behavior
	- Files: `src/core/n8nbridge/N8nHttpClient.py`
	- Acceptance: AC-03

### Phase P4 - Core Orchestration and Idempotency
- [ ] T8 - Author core tests first (RT-12..RT-15)
	- Files: `tests/core/n8nbridge/test_N8nBridgeCore.py`
	- Acceptance: AC-04
- [ ] T9 - Implement core orchestration and TTL idempotency map
	- Files: `src/core/n8nbridge/N8nBridgeCore.py`
	- Acceptance: AC-04

### Phase P5 - Mixin Integration and End-to-End Contract
- [ ] T10 - Author mixin + contract tests first (RT-16..RT-18)
	- Files: `tests/core/n8nbridge/test_N8nBridgeMixin.py`, `tests/core/n8nbridge/test_n8n_bridge_contract.py`
	- Acceptance: AC-05, AC-06
- [ ] T11 - Implement agent-facing mixin delegation
	- Files: `src/core/n8nbridge/N8nBridgeMixin.py`, `src/core/n8nbridge/__init__.py`
	- Acceptance: AC-05
- [ ] T12 - Final regression and conformance gate
	- Files: `docs/project/prj0000087-n8n-workflow-bridge/n8n-workflow-bridge.plan.md`
	- Acceptance: AC-06

## Acceptance Criteria Mapping
| AC | Requirement | Tasks | Test IDs |
|---|---|---|---|
| AC-01 | Config contract loads defaults and rejects invalid runtime settings | T1, T2, T3 | RT-01, RT-02, RT-03 |
| AC-02 | Event adapter enforces required fields and canonical mapping | T4, T5 | RT-04, RT-05, RT-06, RT-07 |
| AC-03 | HTTP transport applies auth headers, timeout, and bounded retry policy | T6, T7 | RT-08, RT-09, RT-10, RT-11 |
| AC-04 | Core handles inbound idempotency and outbound trigger result shaping | T8, T9 | RT-12, RT-13, RT-14, RT-15 |
| AC-05 | Mixin delegates to core without embedding business logic | T10, T11 | RT-16, RT-17 |
| AC-06 | End-to-end canonical contract and validation command gates pass | T10, T12 | RT-18 |

## Test Mapping (18 Total)
| Test ID | Test Name | File | Covers AC |
|---|---|---|---|
| RT-01 | `test_from_env_loads_required_fields_and_defaults` | `tests/core/n8nbridge/test_N8nBridgeConfig.py` | AC-01 |
| RT-02 | `test_validate_rejects_invalid_base_url` | `tests/core/n8nbridge/test_N8nBridgeConfig.py` | AC-01 |
| RT-03 | `test_validate_rejects_nonpositive_timeout_or_negative_retries` | `tests/core/n8nbridge/test_N8nBridgeConfig.py` | AC-01 |
| RT-04 | `test_to_inbound_event_maps_valid_payload` | `tests/core/n8nbridge/test_N8nEventAdapter.py` | AC-02 |
| RT-05 | `test_to_inbound_event_rejects_missing_required_identifiers` | `tests/core/n8nbridge/test_N8nEventAdapter.py` | AC-02 |
| RT-06 | `test_to_inbound_event_preserves_correlation_id_from_headers` | `tests/core/n8nbridge/test_N8nEventAdapter.py` | AC-02 |
| RT-07 | `test_to_n8n_trigger_payload_maps_outbound_canonical_event` | `tests/core/n8nbridge/test_N8nEventAdapter.py` | AC-02 |
| RT-08 | `test_post_json_includes_api_key_header_when_configured` | `tests/core/n8nbridge/test_N8nHttpClient.py` | AC-03 |
| RT-09 | `test_post_json_applies_timeout_to_request_execution` | `tests/core/n8nbridge/test_N8nHttpClient.py` | AC-03 |
| RT-10 | `test_post_json_retries_retryable_failures_up_to_max_attempts` | `tests/core/n8nbridge/test_N8nHttpClient.py` | AC-03 |
| RT-11 | `test_post_json_does_not_retry_non_retryable_4xx` | `tests/core/n8nbridge/test_N8nHttpClient.py` | AC-03 |
| RT-12 | `test_handle_inbound_event_rejects_duplicate_event_id_inside_ttl` | `tests/core/n8nbridge/test_N8nBridgeCore.py` | AC-04 |
| RT-13 | `test_handle_inbound_event_accepts_same_event_id_after_ttl_expiry` | `tests/core/n8nbridge/test_N8nBridgeCore.py` | AC-04 |
| RT-14 | `test_trigger_workflow_returns_success_result_on_2xx` | `tests/core/n8nbridge/test_N8nBridgeCore.py` | AC-04 |
| RT-15 | `test_trigger_workflow_maps_timeout_to_typed_retryable_failure_result` | `tests/core/n8nbridge/test_N8nBridgeCore.py` | AC-04 |
| RT-16 | `test_n8n_trigger_delegates_to_core_with_passthrough_args` | `tests/core/n8nbridge/test_N8nBridgeMixin.py` | AC-05 |
| RT-17 | `test_n8n_handle_callback_delegates_to_core_and_returns_result` | `tests/core/n8nbridge/test_N8nBridgeMixin.py` | AC-05 |
| RT-18 | `test_contract_outbound_event_to_normalized_bridge_result` | `tests/core/n8nbridge/test_n8n_bridge_contract.py` | AC-06 |

## Deliverable File Map
### Code files (7)
1. `src/core/n8nbridge/N8nBridgeConfig.py`
2. `src/core/n8nbridge/N8nEventAdapter.py`
3. `src/core/n8nbridge/N8nHttpClient.py`
4. `src/core/n8nbridge/N8nBridgeCore.py`
5. `src/core/n8nbridge/N8nBridgeMixin.py`
6. `src/core/n8nbridge/exceptions.py`
7. `src/core/n8nbridge/__init__.py`

### Test files (6)
1. `tests/core/n8nbridge/test_N8nBridgeConfig.py`
2. `tests/core/n8nbridge/test_N8nEventAdapter.py`
3. `tests/core/n8nbridge/test_N8nHttpClient.py`
4. `tests/core/n8nbridge/test_N8nBridgeCore.py`
5. `tests/core/n8nbridge/test_N8nBridgeMixin.py`
6. `tests/core/n8nbridge/test_n8n_bridge_contract.py`

## Milestones
| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | Contracts and config finalized | T1-T3 | PLANNED |
| M2 | Adapter and transport verified by tests | T4-T7 | PLANNED |
| M3 | Core orchestration and idempotency complete | T8-T9 | PLANNED |
| M4 | Mixin + contract integration and final gates | T10-T12 | PLANNED |

## Validation Commands
```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
python -m pytest -q tests/core/n8nbridge/test_N8nBridgeConfig.py
python -m pytest -q tests/core/n8nbridge/test_N8nEventAdapter.py
python -m pytest -q tests/core/n8nbridge/test_N8nHttpClient.py
python -m pytest -q tests/core/n8nbridge/test_N8nBridgeCore.py
python -m pytest -q tests/core/n8nbridge/test_N8nBridgeMixin.py
python -m pytest -q tests/core/n8nbridge/test_n8n_bridge_contract.py
python -m pytest -q tests/core/n8nbridge
python -m mypy src/core/n8nbridge
python -m ruff check src/core/n8nbridge tests/core/n8nbridge
```

## Handoff
Target agent: @5test

Handoff package:
1. Canonical plan complete with TDD implementation order.
2. 18 deterministic tests mapped to AC-01..AC-06.
3. Validation command set defined for pre-implementation and post-implementation gates.
