# structured-logging — Test Plan
_Owner: @5test | Status: DONE_

## Test File: `tests/test_structured_logging.py`

| # | Test Name | What it verifies |
|---|---|---|
| 1 | `test_logging_config_module_imports` | `logging_config` module importable; `setup_logging` and `get_logger` are callable |
| 2 | `test_setup_logging_returns_logger` | `setup_logging()` returns a `logging.Logger` instance |
| 3 | `test_get_logger_returns_named_logger` | `get_logger("pyagent.backend")` returns logger with correct name |
| 4 | `test_logger_has_json_handler` | After `setup_logging()`, logger has ≥1 `StreamHandler` whose formatter is `JsonFormatter` |
| 5 | `test_correlation_id_middleware_adds_header` | Integration: `GET /health` response contains `X-Correlation-ID` header |

## Pass Criteria

- All 5 tests green
- No existing tests broken

## Dependencies

- `pytest`, `httpx` (for TestClient / async client)
- `python-json-logger` installed

## Pre-existing failures (known, not this project)

- `test_projects_json_entry_count` — count mismatch (pre-existing)
- `test_kanban_total_rows` — count mismatch (pre-existing)
- `test_all_sarif_files_are_fresh` — stale SARIF (pre-existing)
