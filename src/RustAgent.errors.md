# Errors: `RustAgent.py`

## Scan scope
- Static scan (AST parse) + lightweight compile / syntax check
- VS Code / Pylance Problems are not embedded by this script

## Syntax / compile

- `py_compile` equivalent: FAILED
```
invalid syntax (RustAgent.py, line 23)
```

## Known issues / hazards
- None detected by the lightweight scan

## Notes
- This report only shows fundamental static analysis errors.
- File: `src\classes\coder\RustAgent.py`