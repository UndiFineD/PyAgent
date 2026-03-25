# flm-token-throughput-dashboard — Implementation Plan
_Owner: @4plan | Status: DONE_

## Tasks

| # | Task | File | Agent | Status |
|---|---|---|---|---|
| 1 | Create project artifacts (9 files) | docs/project/prj0000060/ | @1project | ✅ |
| 2 | Add GET /api/metrics/flm to backend | backend/app.py | @6code | ✅ |
| 3 | Create FLMDashboard.tsx panel | web/apps/FLMDashboard.tsx | @6code | ✅ |
| 4 | Update AppId union in types.ts | web/types.ts | @6code | ✅ |
| 5 | Wire FLMDashboard into App.tsx | web/App.tsx | @6code | ✅ |
| 6 | Write 5 endpoint tests | tests/test_flm_dashboard.py | @5test | ✅ |
| 7 | Run tests `pytest tests/test_flm_dashboard.py -v` | — | @7exec | ✅ |
| 8 | Run full suite for regression check | — | @7exec | ✅ |
| 9 | CodeQL / security review | — | @8ql | ✅ |
| 10 | Commit, push, PR | — | @9git | ✅ |

## Rollback Plan
If the `/api/metrics/flm` endpoint causes import or startup issues, remove the
route from `backend/app.py`. Frontend change is additive only — removing the
`'flm-dashboard'` case from App.tsx restores previous state.
