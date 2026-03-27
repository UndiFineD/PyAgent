# prj0000085-shadow-mode-replay - Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-03-27_

## Overview
Deliver deterministic, side-effect-free replay capability in TDD order from the approved design by implementing replay contracts, storage, execution core, orchestration, and mixin integration with a strict 18-test suite.

## Requirements And Constraints
- REQ-001: Implement replay package contracts from design without introducing placeholder or pass-only deliverables.
- REQ-002: Keep side-effect blocking strict in shadow mode (no persistent storage/process/network mutation).
- REQ-003: Preserve deterministic ordering and divergence diagnostics for replay sessions.
- CON-001: Branch must match `prj0000085-shadow-mode-replay` before write/handoff.
- CON-002: Plan must be executable by @5test and @6code in atomic task order.
- CON-003: Public API names and module paths must match design contracts.

## Chunking Strategy
Single runnable chunk (`C1`) sized for one focused delivery wave.

- Code files in C1 (10):
  1. `src/core/replay/__init__.py`
  2. `src/core/replay/exceptions.py`
  3. `src/core/replay/ReplayEnvelope.py`
  4. `src/core/replay/ReplayTypes.py`
  5. `src/core/replay/ReplayStore.py`
  6. `src/core/replay/ShadowExecutionCore.py`
  7. `src/core/replay/ReplayOrchestrator.py`
  8. `src/core/replay/ReplayMixin.py`
  9. `src/core/base/base_agent.py` (mixin wiring touchpoint)
  10. `src/core/base/agent_state_manager.py` (replay dependency boot wiring)

- Test files in C1 (10):
  1. `tests/replay/test_replay_envelope_roundtrip.py`
  2. `tests/replay/test_replay_envelope_validation.py`
  3. `tests/replay/test_replay_envelope_checksum.py`
  4. `tests/replay/test_replay_store_append_load.py`
  5. `tests/replay/test_replay_store_range_dedup.py`
  6. `tests/replay/test_replay_store_corruption_delete.py`
  7. `tests/replay/test_shadow_execution_core_policy.py`
  8. `tests/replay/test_replay_orchestrator_sequence_divergence.py`
  9. `tests/replay/test_replay_mixin_integration.py`
  10. `tests/replay/test_replay_e2e_fixture_hash.py`

## Implementation Order (TDD)
1. [ ] T1 - Define replay errors and result types.
	Files: `src/core/replay/exceptions.py`, `src/core/replay/ReplayTypes.py`, `src/core/replay/__init__.py`
	Acceptance:
	- All replay exceptions from design exist and are exported.
	- Result dataclasses/types for step/session validation are importable.
	- No runtime side effects in module import path.

2. [ ] T2 - Build immutable envelope contract and validation.
	Files: `src/core/replay/ReplayEnvelope.py`, `src/core/replay/__init__.py`
	Acceptance:
	- `from_dict`, `to_dict`, `validate` implemented with deterministic checksum behavior.
	- Required field checks and logical-clock checks implemented.
	- Schema mismatch paths raise replay schema errors.

3. [ ] T3 - Implement replay store with deterministic JSONL semantics.
	Files: `src/core/replay/ReplayStore.py`, `src/core/replay/__init__.py`
	Acceptance:
	- Append/load/load_range/delete/session_exists implemented.
	- Duplicate sequence detection and corruption handling implemented.
	- Ordering by `sequence_no` guaranteed.

4. [ ] T4 - Implement shadow execution core with hard policy enforcement.
	Files: `src/core/replay/ShadowExecutionCore.py`, `src/core/replay/ReplayTypes.py`
	Acceptance:
	- Side-effect intents are evaluated and disallowed intents blocked.
	- Transaction rollback guaranteed on execution exceptions.
	- Structured `ReplayStepResult` returned for success/failure.

5. [ ] T5 - Implement orchestrator replay/shadow control flow.
	Files: `src/core/replay/ReplayOrchestrator.py`, `src/core/replay/ReplayTypes.py`
	Acceptance:
	- Session load/order, sequence-gap fail-fast, divergence collection implemented.
	- `stop_on_divergence` behavior for true/false implemented.
	- Shadow and replay session result summaries returned.

6. [ ] T6 - Integrate ReplayMixin and agent boot wiring.
	Files: `src/core/replay/ReplayMixin.py`, `src/core/base/base_agent.py`, `src/core/base/agent_state_manager.py`, `src/core/replay/__init__.py`
	Acceptance:
	- Mixin emission includes context lineage fields.
	- Mixin replay APIs delegate to orchestrator correctly.
	- Agent initialization path injects store/orchestrator dependencies.

7. [ ] T7 - Execute full replay validation command set and close AC traceability.
	Files: `docs/project/prj0000085-shadow-mode-replay/prj0000085-shadow-mode-replay.plan.md`
	Acceptance:
	- All 18 tests pass in deterministic mode.
	- Lint/type/test command set passes for touched replay modules.
	- AC coverage table fully satisfied and updated.

## 18-Test Breakdown And Mapping
| Test ID | Test Name | File | Covers Tasks | Design Scope |
|---|---|---|---|---|
| RT-01 | envelope round-trip preserves payload | `tests/replay/test_replay_envelope_roundtrip.py` | T2 | Envelope serialization |
| RT-02 | missing required fields rejected | `tests/replay/test_replay_envelope_validation.py` | T2 | Envelope validation |
| RT-03 | non-monotonic logical clock rejected | `tests/replay/test_replay_envelope_validation.py` | T2 | Determinism guard |
| RT-04 | checksum mismatch raises schema error | `tests/replay/test_replay_envelope_checksum.py` | T2 | Integrity validation |
| RT-05 | store append/load returns ordered envelopes | `tests/replay/test_replay_store_append_load.py` | T3 | Store ordering |
| RT-06 | duplicate sequence rejected | `tests/replay/test_replay_store_range_dedup.py` | T3 | Store dedup contract |
| RT-07 | load_range enforces bounds/subset determinism | `tests/replay/test_replay_store_range_dedup.py` | T3 | Range retrieval |
| RT-08 | corrupted JSONL line raises corruption error | `tests/replay/test_replay_store_corruption_delete.py` | T3 | Corruption handling |
| RT-09 | delete_session removes persisted events | `tests/replay/test_replay_store_corruption_delete.py` | T3 | Store deletion |
| RT-10 | shadow core executes read-only envelope safely | `tests/replay/test_shadow_execution_core_policy.py` | T4 | Shadow success path |
| RT-11 | shadow core blocks process side effects | `tests/replay/test_shadow_execution_core_policy.py` | T4 | Policy enforcement |
| RT-12 | shadow core rolls back on exception | `tests/replay/test_shadow_execution_core_policy.py` | T4 | Transaction rollback |
| RT-13 | orchestrator fails on sequence gap | `tests/replay/test_replay_orchestrator_sequence_divergence.py` | T5 | Sequence checks |
| RT-14 | orchestrator halts at first divergence | `tests/replay/test_replay_orchestrator_sequence_divergence.py` | T5 | Divergence stop mode |
| RT-15 | orchestrator collects all divergences | `tests/replay/test_replay_orchestrator_sequence_divergence.py` | T5 | Divergence aggregate mode |
| RT-16 | mixin emission includes context lineage | `tests/replay/test_replay_mixin_integration.py` | T6 | Integration lineage |
| RT-17 | mixin replay delegates to orchestrator | `tests/replay/test_replay_mixin_integration.py` | T6 | API delegation |
| RT-18 | end-to-end replay reproduces deterministic hash | `tests/replay/test_replay_e2e_fixture_hash.py` | T5, T6 | End-to-end determinism |

## Acceptance Criteria Coverage
| AC | Definition | Implemented By | Verified By |
|---|---|---|---|
| AC-01 | Replay contract and schema validation implemented | T1, T2 | RT-01, RT-02, RT-03, RT-04 |
| AC-02 | Durable deterministic store semantics implemented | T3 | RT-05, RT-06, RT-07, RT-08, RT-09 |
| AC-03 | Shadow no-side-effect policy enforced | T4 | RT-10, RT-11, RT-12 |
| AC-04 | Replay orchestration and divergence logic implemented | T5 | RT-13, RT-14, RT-15 |
| AC-05 | Mixin/agent integration complete | T6 | RT-16, RT-17 |
| AC-06 | End-to-end deterministic replay proven | T5, T6, T7 | RT-18 + validation commands |

## Milestones
| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | Contracts locked | T1-T2 | DONE |
| M2 | Storage and policy core locked | T3-T4 | DONE |
| M3 | Orchestration and integration locked | T5-T6 | DONE |
| M4 | Validation and AC closure | T7 | DONE |

## Validation Commands
```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
python -m pytest -q tests/replay
python -m pytest -q tests/replay/test_replay_orchestrator_sequence_divergence.py
python -m pytest -q tests/replay/test_replay_e2e_fixture_hash.py
python -m mypy src/core/replay
python -m ruff check src/core/replay src/core/base/base_agent.py src/core/base/agent_state_manager.py
```

## Handoff
- Downstream target: @5test
- Handoff scope: C1 tasks T1-T7 with RT-01..RT-18 mapping above.
