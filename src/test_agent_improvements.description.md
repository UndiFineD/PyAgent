# Description: `test_agent_improvements.py`

## Module purpose

Pytest suite covering `agent-improvements.py` improvement-management APIs (enums, templates, scheduling, validation, workflow, voting, analytics, export, and related helpers).

## Location

- Path: `src/test_agent_improvements.py`

## Public surface

- Test classes: multiple `Test*` classes grouped by feature area
- Fixtures/helpers: provided via `pytest` + `agent_test_utils`

## Behavior summary

- Pure test module (no CLI/side effects).
- Exercises `ImprovementsAgent` plus a set of compatibility APIs expected by the tests.

## Key dependencies

- `pytest`
- `typing`, `datetime`
- `agent_test_utils` (dynamic import helpers)

## File fingerprint

- SHA256(source): `0B3F08D689607CAD5666E2F4F28FD7238C468F914271D200EEEA1FF777932234`
