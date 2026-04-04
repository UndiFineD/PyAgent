# openapi-drift-post-merge-hotfix - Code Artifacts

_Status: DONE_
_Coder: @6code | Updated: 2026-04-04_

## Implementation Summary
Executed the minimal hotfix path by regenerating the committed backend OpenAPI artifact from
the current backend app state using the existing generator command.

No test canonicalization change was required because drift selector
`tests/docs/test_backend_openapi_drift.py::test_ac_oas_003_drift_check_is_read_only_and_semantic`
passed immediately after regeneration.

## Modules Changed
| Module | Change | Lines |
|---|---|---|
| docs/api/openapi/backend_openapi.json | Regenerated from `backend.app.openapi()` via script | 0 net diff in working tree |
| docs/project/prj0000123-openapi-drift-post-merge-hotfix/openapi-drift-post-merge-hotfix.code.md | Updated status and evidence | +23/-4 |

## Implementation Evidence Mapping
| AC ID | Changed module/file | Validating test(s) | Status |
|---|---|---|---|
| AC-OAS-003 | docs/api/openapi/backend_openapi.json | tests/docs/test_backend_openapi_drift.py::test_ac_oas_003_drift_check_is_read_only_and_semantic | PASS |

## Test Run Results
```
...                                                                                                                  [100%]
3 passed in 7.35s
```

## Deferred Items
None. Canonicalization fallback was not needed because regeneration resolved the selector.
