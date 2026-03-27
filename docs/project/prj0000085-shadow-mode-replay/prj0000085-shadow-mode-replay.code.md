# prj0000085-shadow-mode-replay - Code Artifacts

_Status: DONE_
_Coder: @6code | Updated: 2026-03-27_

## Implementation Summary
Implemented the shadow-mode replay core under `src/core/replay/` with deterministic envelope contracts,
JSONL-backed replay session storage, side-effect-blocking shadow execution, orchestration with divergence
tracking, and an agent-facing replay mixin API for envelope emission and replay delegation.

Fix-pass note (prj0000085 blocker): added focused branch-coverage tests in replay scope to raise
`src/core/replay` coverage from `87.81%` to `98.34%`, clearing the `>=90%` gate.

## Modules Changed
| Module | Change | Lines |
|---|---|---|
| src/core/replay/exceptions.py | Added | +68/-0 |
| src/core/replay/ReplayEnvelope.py | Added | +240/-0 |
| src/core/replay/ReplayStore.py | Added | +177/-0 |
| src/core/replay/ShadowExecutionCore.py | Added | +170/-0 |
| src/core/replay/ReplayOrchestrator.py | Added | +159/-0 |
| src/core/replay/ReplayMixin.py | Added | +141/-0 |
| src/core/replay/__init__.py | Added | +47/-0 |
| tests/test_shadow_replay.py | Updated | +252/-0 |
| docs/project/prj0000085-shadow-mode-replay/prj0000085-shadow-mode-replay.code.md | Updated | +24/-10 |

## Test Run Results
```
pytest tests/test_shadow_replay.py -q --tb=short
29 passed in 1.77s

pytest tests/test_shadow_replay.py --cov=src/core/replay --cov-report=term-missing --cov-fail-under=90 -q
TOTAL 98.34% (gate passed)

python -m mypy src/core/replay --strict
Success: no issues found in 7 source files

python -m ruff check src/core/replay tests/test_shadow_replay.py tests/test_ReplayEnvelope.py tests/test_ReplayStore.py tests/test_ShadowExecutionCore.py tests/test_ReplayOrchestrator.py tests/test_ReplayMixin.py
All checks passed!
```

## Deferred Items
None.
