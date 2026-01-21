# Errors: `ReportGenerator.py`

## Scan scope
- Static scan (AST parse) + lightweight compile / syntax check
- VS Code / Pylance Problems are not embedded by this script

## Syntax / compile

- `py_compile` equivalent: OK (AST parse succeeded)

## Known issues / hazards
- Runs `git` via `subprocess`; will fail if git is not installed or repo has no remote.
- Runs GitHub CLI via `subprocess`; requires `gh` to be authenticated.
- Invokes `copilot` CLI; will be a no-op / fallback if Copilot CLI is not installed.

## Notes
- This report only shows fundamental static analysis errors.
- File: `src\observability\reports\ReportGenerator.py`