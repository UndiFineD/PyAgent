# 10idea Tools Guide

## Preferred Tool Order
- search_subagent or text search for intake research and duplicate discovery
- read_file for candidate idea inspection, lineage, and missing-template analysis
- run_in_terminal for deterministic inventory/validation commands (`rg`, `git mv`, tracker refresh)
- apply_patch/edit for creating/updating idea files and traceability sections

## Anti-patterns
- Do not merge ideas on `main` for project-scoped work.
- Do not delete superseded ideas without moving to archive.
- Do not create merged ideas without `Merged from` and `Source references`.
- Do not mark an idea `ready` when intake answers or validation paths are missing.
- Do not run giant merges without confidence thresholds and rollback notes.

## Notes
- Keep merge clusters small and semantically tight (prefer 2-4 ideas).
- Preserve unique constraints from every input idea.
- Use readiness queues for scale: `ready`, `needs-discovery`, `blocked`.
- Process high-volume sets in batches using tracker offset/limit parameters.
- Always run governance validation after merge/archive operations.
