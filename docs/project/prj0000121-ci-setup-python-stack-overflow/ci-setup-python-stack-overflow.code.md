# ci-setup-python-stack-overflow - Code Artifacts

_Status: DONE_
_Coder: @6code | Updated: 2026-04-03_

## Implementation Summary
Applied a minimal workflow hotfix for the CI / Lightweight regression by replacing `actions/setup-python@v5` with `actions/setup-python@v4` in `.github/workflows/ci.yml` to avoid the observed runtime stack overflow before tests execute.

## Modules Changed
| Module | Change | Lines |
|---|---|---|
| .github/workflows/ci.yml | Pin setup-python action to stable v4 for lightweight CI job | +1/-1 |
| docs/project/prj0000121-ci-setup-python-stack-overflow/ci-setup-python-stack-overflow.code.md | Record implementation and validation evidence | +18/-5 |

## Test Run Results
```
python -m pytest -q tests/ci/test_placeholder_smoke.py
..                                                                                                                                    [100%]
2 passed in 5.82s

python -m pytest -q tests/ci/test_workflow_count.py
......                                                                                                                                [100%]
6 passed in 6.85s

python -m pytest -q tests/ci/test_ci_parallelization.py
...                                                                                                                                   [100%]
3 passed in 7.72s

python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
.................                                                                                                                     [100%]
17 passed in 9.99s
```

## Implementation Evidence Mapping
| AC ID | Changed module/file | Validating test(s) | Status |
|---|---|---|---|
| AC-1 | .github/workflows/ci.yml | tests/ci/test_placeholder_smoke.py, tests/ci/test_workflow_count.py, tests/ci/test_ci_parallelization.py | DONE |

## Deferred Items
none
