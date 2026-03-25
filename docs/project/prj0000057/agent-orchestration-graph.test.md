# agent-orchestration-graph — Test Notes
_Owner: @5test | Status: DONE_

## Test File: `tests/test_orchestration_graph.py`

### Strategy
Backend integration tests via FastAPI `TestClient`. These validate the
`/api/agent-log/{agent_id}` endpoints that the frontend component polls.
All 5 tests are purely backend — no frontend test harness required.

### Authentication
The endpoint requires authentication. Tests use the standard
`Authorization: Bearer test-token` header pattern used in other test files.
We use `X-API-Key: test-key` as set in `conftest.py`.

### Test Coverage

| Test | Method | Path | What is validated |
|---|---|---|---|
| `test_agent_log_endpoint_returns_200` | GET | `/api/agent-log/0master` | HTTP 200 status |
| `test_agent_log_response_has_correct_fields` | GET | `/api/agent-log/0master` | JSON has `"content"` key |
| `test_agent_log_accepts_put_request` | PUT | `/api/agent-log/0master` | HTTP 200 status |
| `test_agent_log_put_stores_data` | PUT | `/api/agent-log/0master` | Response has `"status": "ok"` |
| `test_agent_log_roundtrip` | PUT then GET | `/api/agent-log/0master` | GET returns same content as PUT |

### Known Pre-existing Failures (not this project)
- `test_all_sarif_files_are_fresh` — stale SARIF gate
- `test_projects_json_entry_count` — count mismatch from previous projects
- `test_kanban_total_rows` — count mismatch from previous projects
