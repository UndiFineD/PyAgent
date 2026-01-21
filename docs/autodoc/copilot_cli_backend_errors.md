# Errors: `CopilotCliBackend.py`

## Scan scope
- Static scan (AST parse) + lightweight compile / syntax check
- VS Code / Pylance Problems are not embedded by this script

## Syntax / compile

- `py_compile` equivalent: OK (AST parse succeeded)

## Known issues / hazards
- Invokes `copilot` CLI; will be a no-op / fallback if Copilot CLI is not installed.

## Notes
- This report only shows fundamental static analysis errors.
- File: `src\infrastructure\backend\llm_backends\CopilotCliBackend.py`