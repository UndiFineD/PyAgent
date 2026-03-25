# api-versioning — Test Plan

_Owner: @5test_

## Test file: `tests/test_api_versioning.py`

| # | Name | Description |
|---|---|---|
| 1 | `test_v1_health_exists` | GET /health still works (unversioned) |
| 2 | `test_v1_agent_log_routable` | GET /api/v1/agent-log/0master returns 200 |
| 3 | `test_v1_projects_routable` | GET /api/v1/projects returns 200 |
| 4 | `test_v1_returns_version_header` | X-API-Version:1 present on /api/v1/ response |
| 5 | `test_v1_agent_memory_routable` | GET /api/v1/agent-memory/test returns 200 |
| 6 | `test_unversioned_returns_deprecation_header` | Deprecation:true present on /api/ response |

## Notes

- Uses `TestClient(app)` — dev mode auth (no credentials needed)
- Does not test actual data, only routing + headers
