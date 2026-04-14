# 9git Tools Guide

## Preferred Tool Order
- run_in_terminal git status/diff/branch validation commands
- get_changed_files for staging scope checks
- run_in_terminal pre-commit + gh auth/pr commands

## Anti-patterns
- Never use blanket staging (git add . / -A).
- Never continue git workflow when branch/scope/pre-commit checks fail.

## Notes
- Keep actions scoped to project branch and allowed files.
- Prefer deterministic commands with evidence-producing output.

