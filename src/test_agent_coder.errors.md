# Errors: `test_agent-coder.py`

## Scan scope

- Static scan (AST parse) + lightweight compile/syntax check
- VS Code/Pylance Problems are not embedded by this script

## Syntax / compile

- `py_compile` equivalent: OK (AST parse succeeded)

## Known issues / hazards

- Filename is not import-friendly for pytest collection (contains '-' or extra '.') and may fail test discovery/import.
