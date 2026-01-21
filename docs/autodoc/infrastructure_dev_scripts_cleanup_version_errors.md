# Errors: `cleanup_version.py`

## Scan scope
- Static scan (AST parse) + lightweight compile / syntax check
- VS Code / Pylance Problems are not embedded by this script

## Syntax / compile

- `py_compile` equivalent: FAILED
```
expected 'except' or 'finally' block (cleanup_version.py, line 37)
```

## Known issues / hazards
- None detected by the lightweight scan

## Notes
- This report only shows fundamental static analysis errors.
- File: `infrastructure\dev\scripts\cleanup_version.py`