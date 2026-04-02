# prj0000088-ai-fuzzing-security - Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-03-27_

## Overview
Deliver a deterministic, local-only fuzzing core in `src/core/fuzzing/` using strict TDD sequencing.
This plan defines implementation order, acceptance criteria mapping, and the full 18-test matrix required
for handoff to @5test and @6code.

## Scope
- In scope:
	- Deterministic mutation pipeline and replayable case identity.
	- Local-only safety policy enforcement and execution budget controls.
	- Typed result aggregation and explicit exception hierarchy.
	- Public package export surface for fuzzing core modules.
- Out of scope:
	- Model-assisted mutation runtime.
	- Distributed/remote workers.
	- Coverage-guided instrumentation integrations.

## Implementation Order (TDD)
1. Write failing tests for immutable contracts and exception behavior (TEST-01..TEST-04).
2. Implement `exceptions.py`, `FuzzCase.py`, and `FuzzResult.py` until contract tests pass.
3. Write failing policy tests (TEST-05..TEST-07), then implement `FuzzSafetyPolicy.py`.
4. Write failing corpus and mutator tests (TEST-08..TEST-13), then implement `FuzzCorpus.py` and `FuzzMutator.py`.
5. Write failing engine orchestration tests (TEST-14..TEST-18), then implement `FuzzEngineCore.py`.
6. Finalize package exports in `__init__.py`, then run full validation commands.

## Task List
- [ ] T1 - Define typed exceptions and package surface | Files: `src/core/fuzzing/exceptions.py`, `src/core/fuzzing/__init__.py` | Acceptance: AC-01
- [ ] T2 - Implement immutable fuzz case contract | Files: `src/core/fuzzing/FuzzCase.py` | Acceptance: AC-02
- [ ] T3 - Implement result models and campaign aggregation | Files: `src/core/fuzzing/FuzzResult.py` | Acceptance: AC-03
- [ ] T4 - Implement local-only policy checks and budget guards | Files: `src/core/fuzzing/FuzzSafetyPolicy.py` | Acceptance: AC-04, AC-05
- [ ] T5 - Implement corpus normalization and deterministic selection | Files: `src/core/fuzzing/FuzzCorpus.py` | Acceptance: AC-06
- [ ] T6 - Implement deterministic mutator registry and generation | Files: `src/core/fuzzing/FuzzMutator.py` | Acceptance: AC-07
- [ ] T7 - Implement engine campaign orchestration and replay stability | Files: `src/core/fuzzing/FuzzEngineCore.py` | Acceptance: AC-08, AC-09
- [ ] T8 - Author and stabilize all mapped tests before code completion | Files: `tests/core/fuzzing/test_exceptions.py`, `tests/core/fuzzing/test_FuzzCase.py`, `tests/core/fuzzing/test_FuzzResult.py`, `tests/core/fuzzing/test_FuzzSafetyPolicy.py`, `tests/core/fuzzing/test_FuzzCorpus.py`, `tests/core/fuzzing/test_FuzzMutator.py`, `tests/core/fuzzing/test_FuzzEngineCore.py` | Acceptance: AC-10

## Acceptance Criteria (AC)
| AC ID | Requirement |
|---|---|
| AC-01 | Exception hierarchy exists with domain-specific failures for policy, config, and execution. |
| AC-02 | `FuzzCase` is immutable and exposes deterministic replay identity (`replay_key`). |
| AC-03 | `FuzzResult` provides typed per-case outcomes and deterministic campaign summary counts. |
| AC-04 | `FuzzSafetyPolicy` blocks non-local targets and disallowed operators. |
| AC-05 | `FuzzSafetyPolicy` enforces run budget constraints (max cases, max bytes, max duration metadata). |
| AC-06 | `FuzzCorpus` normalizes inputs, deduplicates payloads, and supports deterministic indexed retrieval. |
| AC-07 | `FuzzMutator` produces deterministic payloads for a fixed seed/operator/corpus index. |
| AC-08 | `FuzzEngineCore` schedules, validates, executes, and records bounded campaigns. |
| AC-09 | Re-running the same campaign inputs with same seed yields identical case ordering and IDs. |
| AC-10 | Exactly 18 mapped tests pass under pytest; mypy and ruff checks are clean for planned scope. |

## AC To Task Mapping
| AC ID | Implementing Tasks |
|---|---|
| AC-01 | T1 |
| AC-02 | T2 |
| AC-03 | T3 |
| AC-04 | T4 |
| AC-05 | T4 |
| AC-06 | T5 |
| AC-07 | T6 |
| AC-08 | T7 |
| AC-09 | T7 |
| AC-10 | T8 |

## Test Mapping (18 Tests)
| Test ID | Planned Test File | Verifies | Mapped AC | Depends On Task |
|---|---|---|---|---|
| TEST-01 | `tests/core/fuzzing/test_exceptions.py` | Policy violation exception typing | AC-01 | T1 |
| TEST-02 | `tests/core/fuzzing/test_exceptions.py` | Execution/config exception typing | AC-01 | T1 |
| TEST-03 | `tests/core/fuzzing/test_FuzzCase.py` | FuzzCase immutability contract | AC-02 | T2 |
| TEST-04 | `tests/core/fuzzing/test_FuzzCase.py` | Deterministic replay key generation | AC-02 | T2 |
| TEST-05 | `tests/core/fuzzing/test_FuzzResult.py` | Per-case result typing and state | AC-03 | T3 |
| TEST-06 | `tests/core/fuzzing/test_FuzzResult.py` | Deterministic campaign summary counts | AC-03 | T3 |
| TEST-07 | `tests/core/fuzzing/test_FuzzSafetyPolicy.py` | Reject non-local target | AC-04 | T4 |
| TEST-08 | `tests/core/fuzzing/test_FuzzSafetyPolicy.py` | Reject disallowed operator | AC-04 | T4 |
| TEST-09 | `tests/core/fuzzing/test_FuzzSafetyPolicy.py` | Enforce budget limits | AC-05 | T4 |
| TEST-10 | `tests/core/fuzzing/test_FuzzCorpus.py` | Normalize corpus entries to bytes | AC-06 | T5 |
| TEST-11 | `tests/core/fuzzing/test_FuzzCorpus.py` | Deduplicate repeated payloads | AC-06 | T5 |
| TEST-12 | `tests/core/fuzzing/test_FuzzCorpus.py` | Deterministic indexed selection | AC-06 | T5 |
| TEST-13 | `tests/core/fuzzing/test_FuzzMutator.py` | Registry exposes allowed operators | AC-07 | T6 |
| TEST-14 | `tests/core/fuzzing/test_FuzzMutator.py` | Seeded deterministic mutation equality | AC-07 | T6 |
| TEST-15 | `tests/core/fuzzing/test_FuzzMutator.py` | Mutation output remains bytes and bounded | AC-07 | T6 |
| TEST-16 | `tests/core/fuzzing/test_FuzzEngineCore.py` | Engine schedules bounded case count | AC-08 | T7 |
| TEST-17 | `tests/core/fuzzing/test_FuzzEngineCore.py` | Engine applies policy before execution | AC-08 | T7 |
| TEST-18 | `tests/core/fuzzing/test_FuzzEngineCore.py` | Replay-stable ordering and case IDs | AC-09 | T7 |

## Planned Code Files
1. `src/core/fuzzing/FuzzCase.py`
2. `src/core/fuzzing/FuzzMutator.py`
3. `src/core/fuzzing/FuzzCorpus.py`
4. `src/core/fuzzing/FuzzEngineCore.py`
5. `src/core/fuzzing/FuzzSafetyPolicy.py`
6. `src/core/fuzzing/FuzzResult.py`
7. `src/core/fuzzing/exceptions.py`
8. `src/core/fuzzing/__init__.py`

## Planned Test Files
1. `tests/core/fuzzing/test_exceptions.py`
2. `tests/core/fuzzing/test_FuzzCase.py`
3. `tests/core/fuzzing/test_FuzzResult.py`
4. `tests/core/fuzzing/test_FuzzSafetyPolicy.py`
5. `tests/core/fuzzing/test_FuzzCorpus.py`
6. `tests/core/fuzzing/test_FuzzMutator.py`
7. `tests/core/fuzzing/test_FuzzEngineCore.py`

## Milestones
| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | Contracts and exceptions | T1-T3 | PLANNED |
| M2 | Safety and mutation primitives | T4-T6 | PLANNED |
| M3 | Engine orchestration and replay stability | T7 | PLANNED |
| M4 | TDD matrix complete and validated | T8 | READY_FOR_@5TEST |

## Validation Commands
```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
python -m pytest -q tests/core/fuzzing
python -m pytest -q tests/core/fuzzing/test_FuzzEngineCore.py
python -m mypy src/core/fuzzing
python -m ruff check src/core/fuzzing tests/core/fuzzing
```

## Handoff
- Next agent: @5test
- Handoff command: `agent/runSubagent @5test`
- Required payload: this plan plus full Test Mapping table (TEST-01..TEST-18).
