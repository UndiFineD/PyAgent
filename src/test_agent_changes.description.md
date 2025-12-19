# Description: `test_agent_changes.py`

## Module purpose

Pytest suite covering `agent-changes.py` / `ChangesAgent` behaviors (parsing, changelog manipulation utilities, preview mode behavior, and delegation paths).

## Location

- Path: `src/test_agent_changes.py`

## Public surface

- Test classes: multiple `Test*` classes grouped by feature area
- Fixtures/helpers: provided via `pytest` + `agent_test_utils`

## Behavior summary

- Pure test module (no CLI/side effects).

## Key dependencies

- `pytest`
- `pathlib`, `typing`
- `agent_test_utils` (dynamic import helpers)

## File fingerprint

- SHA256(source): `54F99F434340536B5764D40FE2A37EE6BEEBB66EE8BBB8E2AFEFECFEC1F2058E`
