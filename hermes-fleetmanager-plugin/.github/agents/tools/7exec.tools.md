# 7exec Tools Guide

## Preferred Tool Order
- run_in_terminal for runtime smoke commands and probes
- runTests for targeted confidence checks
- apply_patch for exec artifact evidence updates

## Anti-patterns
- Do not broaden validation scope beyond project boundary without approval.
- Do not hand off with failed required checks.

## Notes
- Keep actions scoped to project branch and allowed files.
- Prefer deterministic commands with evidence-producing output.

