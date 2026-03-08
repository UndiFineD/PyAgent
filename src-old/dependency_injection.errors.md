# Errors: `dependency_injection.py`

## Scan scope
- Static scan (AST parse) + lightweight compile / syntax check
- VS Code / Pylance Problems are not embedded by this script

## Syntax / compile

- `py_compile` equivalent: FAILED
```
unterminated triple-quoted string literal (detected at line 79) (dependency_injection.py, line 74)
```

## Known issues / hazards
- None detected by the lightweight scan

## Notes
- This report only shows fundamental static analysis errors.
- File: `src\classes\agent_tests\dependency_injection.py`