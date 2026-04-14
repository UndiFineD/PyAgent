# 6code Tools Guide

## Preferred Tool Order
- apply_patch for minimal implementation deltas
- runTests or run_in_terminal pytest for targeted verification
- get_errors after edits to catch regressions

## Anti-patterns
- Do not modify tests to force green unless explicitly requested by scope.
- Do not leave placeholders/stubs/TODO bodies.

## Notes
- Keep actions scoped to project branch and allowed files.
- Prefer deterministic commands with evidence-producing output.

