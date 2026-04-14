# 5test Tools Guide

## Preferred Tool Order
- runTests first for focused suites
- run_in_terminal for pytest/ruff/mypy when needed
- apply_patch for test artifact updates only

## Anti-patterns
- Do not modify production code to satisfy tests.
- Do not leave weak/untargeted test claims without command evidence.

## Notes
- Keep actions scoped to project branch and allowed files.
- Prefer deterministic commands with evidence-producing output.

