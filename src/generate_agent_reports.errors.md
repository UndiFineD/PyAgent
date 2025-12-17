# Errors: `generate_agent_reports.py`

## Scan scope
- Static scan (AST parse) + lightweight compile/syntax check
- VS Code/Pylance Problems are not embedded by this script

## Syntax / compile
- `py_compile` equivalent: OK (AST parse succeeded)

## Known issues / hazards
- Runs `git` via `subprocess`; will fail if git is not installed or repo has no remote.
- Invokes `copilot` CLI; will be a no-op/fallback if Copilot CLI is not installed.
