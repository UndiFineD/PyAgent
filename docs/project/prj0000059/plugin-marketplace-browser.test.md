# plugin-marketplace-browser — Test Plan
_Owner: @5test | Status: DONE_

## Backend Tests (tests/test_plugin_marketplace.py)

| # | Test Name | What It Verifies |
|---|---|---|
| 1 | `test_plugins_endpoint_returns_200` | `GET /api/plugins` returns HTTP 200 |
| 2 | `test_plugins_response_has_plugins_key` | Response JSON contains a `"plugins"` key |
| 3 | `test_plugins_registry_is_non_empty` | `plugins` list has at least one entry |
| 4 | `test_plugin_has_required_fields` | First plugin has all required fields: id, name, description, author, version, tags, installed |
| 5 | `test_plugins_without_auth_returns_200` | Endpoint accessible without `Authorization` header (public route) |

## Coverage Goals
- Full endpoint reachability verified
- Schema contract validated (required fields)
- Auth-not-required contract explicitly tested

## Fixtures
Uses `httpx.AsyncClient` via the standard `anyio` pattern from `conftest.py`,
or `TestClient` from `starlette.testclient` for synchronous tests.
