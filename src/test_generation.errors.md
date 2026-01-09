# Errors: `test_generation.py`

## Scan scope
- Static scan (AST parse) + lightweight compile / syntax check
- VS Code / Pylance Problems are not embedded by this script

## Syntax / compile

- `py_compile` equivalent: FAILED
```
unterminated triple-quoted string literal (detected at line 304) (test_generation.py, line 296)
```

## Known issues / hazards
- None detected by the lightweight scan

## Notes
- This report only shows fundamental static analysis errors.
- File: `src\classes\agent_tests\test_generation.py`