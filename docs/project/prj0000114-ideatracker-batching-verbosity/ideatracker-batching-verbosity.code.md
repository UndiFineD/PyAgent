# ideatracker-batching-verbosity - Code Artifacts

_Status: DONE_
_Coder: @6code | Updated: 2026-04-02_

## Implementation Summary

Implemented the prj0000114 artifact-driven IdeaTracker pipeline.

1. `scripts/IdeaTracker.py` remains the CLI entrypoint, but it now acts as the record-extraction layer and delegates batch orchestration, artifact persistence, similarity generation, and split-file output to focused helper modules.
2. Each collection batch now writes deterministic incremental artifacts under `docs/project/`: `ideatracker.progress.json`, `ideatracker.mapping.json`, `ideatracker.references.json`, `ideatracker.section_names.json`, `ideatracker.tokens.json`, and `ideatracker.similarities.json`.
3. Final `ideatracker.json` and split `ideatracker-NNNNNN.json` outputs are now rebuilt from persisted artifacts rather than only from transient in-memory state.
4. Artifact writes use entity-key upsert semantics so rerunning the same batch window rewrites rows without duplicating mappings, references, tokens, or similarity pairs.
5. Similarity output is stored separately and remains inspectable, while the CLI summary line and output contract stay backward-compatible apart from preserving the existing `split_files=` suffix already present on this branch.

## Modules Changed
| Module | Change | Lines |
|---|---|---|
| `scripts/IdeaTracker.py` | Kept CLI entrypoint stable, preserved extraction/scoring logic, and delegated orchestration to helper modules | refactor |
| `scripts/idea_tracker_artifacts.py` | Added deterministic artifact pathing, stable JSON writing, and upsert-by-entity persistence for all incremental artifacts | new |
| `scripts/idea_tracker_similarity.py` | Added artifact-based similarity generation with blocking and progress heartbeats | new |
| `scripts/idea_tracker_pipeline.py` | Added batch orchestration, checkpoint payload assembly, artifact-backed final payload assembly, and split-output writing | new |
| `tests/test_idea_tracker.py` | Added artifact-persistence and batch-rerun rewrite coverage while preserving existing tracker regression coverage | extended |

## AC Coverage
| AC | Changed module | Validating test(s) | Status |
|---|---|---|---|
| Keep `scripts/IdeaTracker.py` as CLI entrypoint | `scripts/IdeaTracker.py` | CLI smoke command against a temporary repo root | DONE |
| Persist deterministic per-batch artifacts in `docs/project/` | `scripts/idea_tracker_artifacts.py`, `scripts/idea_tracker_pipeline.py` | `test_build_tracker_payload_persists_incremental_artifacts` | DONE |
| Build final payload from persisted artifacts where practical | `scripts/idea_tracker_pipeline.py` | `test_build_tracker_payload_includes_active_and_archived_ideas`, `test_build_tracker_payload_batch_window` | DONE |
| Store similarity artifacts separately and keep them inspectable | `scripts/idea_tracker_similarity.py` | `test_similarity_blocking_finds_shared_project_duplicates`, `test_similarity_verbose_heartbeat_not_tied_to_large_batch_size` | DONE |
| Preserve backward-compatible main output structure and summary line | `scripts/IdeaTracker.py`, `scripts/idea_tracker_pipeline.py` | Focused pytest file plus CLI smoke command | DONE |
| Rewrite the same batch slice without duplicate persisted rows | `scripts/idea_tracker_artifacts.py`, `scripts/idea_tracker_pipeline.py` | `test_build_tracker_payload_rewrites_existing_batch_rows_without_duplicates` | DONE |

## Test Run Results
```
c:/Dev/PyAgent/.venv/Scripts/ruff.exe check --fix scripts/IdeaTracker.py scripts/idea_tracker_artifacts.py scripts/idea_tracker_similarity.py scripts/idea_tracker_pipeline.py tests/test_idea_tracker.py
-> Found 2 errors (2 fixed, 0 remaining).

c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_idea_tracker.py
-> 13 passed in 5.34s

c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
-> 17 passed in 6.19s

c:/Dev/PyAgent/.venv/Scripts/ruff.exe check --output-format concise scripts/IdeaTracker.py scripts/idea_tracker_artifacts.py scripts/idea_tracker_similarity.py scripts/idea_tracker_pipeline.py tests/test_idea_tracker.py
-> All checks passed!

CLI smoke command (temporary repo root)
-> IDEA_TRACKER_OK total=2 active=2 archived=0 ready=0 needs_discovery=2 blocked=0 merge_candidates=0 review_candidates=1 output=<temp>/docs/project/ideatracker.json split_files=2
-> artifacts=true,true,true,true,true,true,true,true,true
```

## Deferred Items

- **Global cross-window similarity completeness**: similarity rows now persist across runs and upsert by pair key, but the current CLI still emits a scoped final payload for the requested offset/limit window. A future full incremental resume mode could assemble one global final output from previously materialized windows without rereading all markdown files.
- **Streaming markdown collection**: the refactor removes the monolithic final-assembly dependency, but each batch still reads its markdown files directly. A future iterator-based reader could reduce transient batch memory further for very large documents.
