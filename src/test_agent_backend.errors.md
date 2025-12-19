# Errors: `test_agent_backend.py`

## Scan scope

- Static scan (AST parse) + lightweight compile/syntax check
- VS Code/Pylance Problems are not embedded by this script

## Syntax / compile

- `py_compile` equivalent: OK (AST parse succeeded)

## Known issues / hazards

- External HTTP calls are mocked; failures are most likely due to mismatched mock expectations or API shape drift.
