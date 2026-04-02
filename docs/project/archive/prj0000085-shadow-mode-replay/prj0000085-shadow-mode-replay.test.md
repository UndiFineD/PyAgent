# prj0000085-shadow-mode-replay - Test Artifacts

_Status: DONE_
_Tester: @5test | Updated: 2026-03-27_

## Test Plan
Write red-phase replay contract tests first, enforce behavior-level assertions, and
execute focused target suite plus structure suite before @6code implementation.

## Test Cases
| ID | Description | File | Status |
|---|---|---|---|
| RT-01 | Envelope round-trip preserves canonical payload | tests/test_shadow_replay.py | RED |
| RT-02 | Envelope rejects missing required fields | tests/test_shadow_replay.py | RED |
| RT-03 | Envelope rejects non-monotonic logical clock | tests/test_shadow_replay.py | RED |
| RT-04 | Envelope checksum mismatch raises schema error | tests/test_shadow_replay.py | RED |
| RT-05 | Store append/load returns ordered envelopes | tests/test_shadow_replay.py | RED |
| RT-06 | Store rejects duplicate sequence per session | tests/test_shadow_replay.py | RED |
| RT-07 | Store load_range returns deterministic subset | tests/test_shadow_replay.py | RED |
| RT-08 | Store corruption raises typed corruption error | tests/test_shadow_replay.py | RED |
| RT-09 | Store delete_session removes persisted events | tests/test_shadow_replay.py | RED |
| RT-10 | Shadow core executes read-only envelope safely | tests/test_shadow_replay.py | RED |
| RT-11 | Shadow core blocks process side effect intents | tests/test_shadow_replay.py | RED |
| RT-12 | Shadow core rolls back on execution exception | tests/test_shadow_replay.py | RED |
| RT-13 | Orchestrator fails on sequence gap | tests/test_shadow_replay.py | RED |
| RT-14 | Orchestrator stop_on_divergence halts first mismatch | tests/test_shadow_replay.py | RED |
| RT-15 | Orchestrator aggregate mode collects divergences | tests/test_shadow_replay.py | RED |
| RT-16 | Mixin emission includes context lineage fields | tests/test_shadow_replay.py | RED |
| RT-17 | Mixin replay API delegates to orchestrator | tests/test_shadow_replay.py | RED |
| RT-18 | End-to-end deterministic output hash contract | tests/test_shadow_replay.py | RED |
| MS-01 | ReplayEnvelope module contract smoke | tests/test_ReplayEnvelope.py | RED |
| MS-02 | ReplayStore module contract smoke | tests/test_ReplayStore.py | RED |
| MS-03 | ShadowExecutionCore module contract smoke | tests/test_ShadowExecutionCore.py | RED |
| MS-04 | ReplayOrchestrator module contract smoke | tests/test_ReplayOrchestrator.py | RED |
| MS-05 | ReplayMixin module contract smoke | tests/test_ReplayMixin.py | RED |


## Validation Results
| ID | Result | Output |
|---|---|---|
| V-RED-TARGET | FAIL (expected red) | `pytest -q tests/test_shadow_replay.py tests/test_ReplayEnvelope.py tests/test_ReplayStore.py tests/test_ShadowExecutionCore.py tests/test_ReplayOrchestrator.py tests/test_ReplayMixin.py` -> 23 failed in 2.61s; all failures point to missing replay behavior modules under `src.core.replay.*` |
| V-STRUCTURE | PASS | `pytest -q tests/structure --tb=short` -> 129 passed in 2.78s |


## Unresolved Failures
Replay implementation is not present yet under `src/core/replay/`; all 23 red-phase target tests are intentionally failing pending @6code implementation.
