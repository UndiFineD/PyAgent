# Description: `test_agent_backend.py`

## Module purpose

Pytest suite covering `agent_backend.py` behaviors (GitHub Models API calls, caching, request/response handling).

## Location

- Path: `src/test_agent_backend.py`

## Public surface

- Test functions/classes: multiple `test_*` functions and `Test*` classes
- Fixtures/helpers: provided via `pytest` + `agent_test_utils`

## Behavior summary

- Pure test module (no CLI/side effects).
- Uses mocking (`unittest.mock`) to isolate external HTTP calls.

## Key dependencies

- `pytest`
- `unittest.mock`
- `agent_test_utils` (path/import helpers)

## File fingerprint

- SHA256(source): `A90A2A0E81A012324B6124A9AF872AE52CEE0C120F53C394A281F7F9DFED239D`
