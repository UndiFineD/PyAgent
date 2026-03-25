# live-agent-execution-in-codebuilder — Test Notes
_Owner: @5test | Status: DONE_

## Test File: tests/test_pipeline_execution.py

5 tests covering the two new backend endpoints.

### Auth Strategy

`backend.auth.DEV_MODE` is set to `True` at module level in the test file.
This bypasses the `require_auth` dependency on `_auth_router` without needing
env vars or mock headers, consistent with how other backend tests work in the
test environment (where `PYAGENT_API_KEY` and `PYAGENT_JWT_SECRET` are absent).

### Test Coverage

| Test | Endpoint | Assertion |
|---|---|---|
| test_pipeline_run_endpoint_returns_pipeline_id | POST /api/pipeline/run | 200, pipeline_id present, status=="running" |
| test_pipeline_status_endpoint_returns_pipeline_data | GET /api/pipeline/status/{id} | 200, id matches, task matches |
| test_pipeline_status_404_for_unknown_id | GET /api/pipeline/status/bad-id | 404 |
| test_pipeline_has_10_stages | GET /api/pipeline/status/{id} | stages has exactly 10 keys |
| test_pipeline_stages_have_status_and_log_fields | GET /api/pipeline/status/{id} | each stage has "status"="pending" and "log"="" |

### Test Isolation

Each test that needs a status check first calls POST /api/pipeline/run to create
a fresh pipeline. Tests are independent and do not rely on shared state.

### Pre-existing Test Suite Notes

The following pre-existing failures are NOT caused by this project:
- `test_projects_json_entry_count` — count validator (pre-existing)
- `test_kanban_total_rows` — row count validator (pre-existing)
- `test_all_sarif_files_are_fresh` — SARIF staleness gate (pre-existing)
