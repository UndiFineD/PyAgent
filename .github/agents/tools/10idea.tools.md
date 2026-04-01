# 10idea Tools Guide

## Preferred Tool Order
- search_subagent or text search for idea discovery clusters
- read_file for candidate idea inspection and source-reference comparison
- run_in_terminal for deterministic inventory commands (`rg`, `git mv`)
- apply_patch/edit for creating merged idea files and updating traceability

## Anti-patterns
- Do not merge ideas on `main` for project-scoped work.
- Do not delete superseded ideas without moving to archive.
- Do not create merged ideas without `Merged from` and `Source references`.

## Notes
- Keep merge clusters small and semantically tight.
- Preserve unique constraints from every input idea.
- Always run governance validation after merge/archive operations.
