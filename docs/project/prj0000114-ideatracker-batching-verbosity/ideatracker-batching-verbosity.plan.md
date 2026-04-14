# ideatracker-batching-verbosity - Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-04-02_

## Current State
- `scripts/IdeaTracker.py` currently owns idea discovery, markdown parsing, scoring, readiness queue generation, similarity blocking, checkpoint writes, split-output writes, and CLI argument handling in one module.
- The active branch already supports `--offset`, `--limit`, `--batch-size`, `--verbose`, split `ideatracker-NNNNNN.json` outputs, and lightweight checkpoint payloads written to the main output path.
- The current checkpoint behavior is useful for progress visibility, but it is not a durable pipeline contract for resuming long runs or consuming intermediate data without reparsing markdown files.
- `tests/test_idea_tracker.py` already covers active/archive discovery, batching windows, blocking similarity, verbosity heartbeats, checkpoint writes, and split output generation.
- `docs/project/prj0000114-ideatracker-batching-verbosity/ideatracker-batching-verbosity.design.md` is still a stub, so this plan treats the user request plus current branch behavior as the working design baseline for this refactor.

## Target State
- Keep `scripts/IdeaTracker.py` as the stable CLI entrypoint while moving orchestration details into small helper modules with snake_case names.
- Write deterministic JSON artifacts to `docs/project/` after every processed batch so long-running runs become resumable and observable without losing current final outputs.
- Preserve the final `docs/project/ideatracker.json` payload and optional split `docs/project/ideatracker-NNNNNN.json` files, but assemble them from incremental artifacts instead of relying on one monolithic in-memory pass.
- Make restart behavior deterministic: rerunning a completed batch must either reuse identical artifact rows or safely overwrite the same batch slice without duplicating records.
- Keep scope pragmatic for this session: no new service, no database, no unrelated project registry work, and no new public CLI beyond flags directly needed for resumable batch processing.

## Affected Files
| Path | Role | Change |
|---|---|---|
| `scripts/IdeaTracker.py` | Existing CLI entrypoint and orchestration layer | Refactor in place; keep current invocation usable during transition |
| `tests/test_idea_tracker.py` | Existing regression suite for tracker behavior | Extend for artifact schemas, resume behavior, and per-batch writes |
| `scripts/idea_tracker_artifacts.py` | Advisable new helper | Deterministic JSON writers, artifact loaders, sorted merge/replace logic |
| `scripts/idea_tracker_pipeline.py` | Advisable new helper | Batch orchestration, resume cursor handling, final payload assembly |
| `scripts/idea_tracker_similarity.py` | Advisable new helper | Similarity candidate generation from persisted token/mapping artifacts |
| `docs/project/ideatracker.json` | Final aggregate output | Preserve current contract as the main consumer-facing output |
| `docs/project/ideatracker.progress.json` | Incremental run state | New resumability and observability artifact |
| `docs/project/ideatracker.mapping.json` | Incremental mapping artifact | New stable per-idea identity and project/file mapping output |
| `docs/project/ideatracker.references.json` | Incremental reference artifact | New normalized source reference output |
| `docs/project/ideatracker.section_names.json` | Incremental section artifact | New normalized section heading output |
| `docs/project/ideatracker.tokens.json` | Incremental token artifact | New blocking and similarity token output |
| `docs/project/ideatracker.similarities.json` | Incremental similarity artifact | New candidate-pair output |

## Incremental Artifact Data Model
| File | Purpose | Deterministic JSON shape |
|---|---|---|
| `docs/project/ideatracker.progress.json` | Resume cursor and batch ledger | `{ schema_version, generated_at, run_args, next_offset, available_total, completed_batches: [{ batch_id, offset, limit, processed_total, stage, status, started_at, completed_at, files_written }] }` |
| `docs/project/ideatracker.mapping.json` | Stable identity, file, and project mapping rows | `{ schema_version, generated_at, source, mappings: [{ idea_id, title, source_path, status, planned_project_ids, readiness_status, sha256, batch_id, updated }] }` |
| `docs/project/ideatracker.references.json` | Source reference rows and inverted reference index | `{ schema_version, generated_at, references: [{ idea_id, reference, batch_id }], reference_index: [{ reference, idea_ids, count }] }` |
| `docs/project/ideatracker.section_names.json` | Normalized section names and missing-section reporting | `{ schema_version, generated_at, sections: [{ idea_id, section_names, missing_required_sections, missing_critical_sections, batch_id }], section_frequency: [{ section_name, count }] }` |
| `docs/project/ideatracker.tokens.json` | Tokenized fields for blocking and similarity reuse | `{ schema_version, generated_at, token_rows: [{ idea_id, title_tokens, project_tokens, source_reference_tokens, blocking_keys, batch_id }] }` |
| `docs/project/ideatracker.similarities.json` | Similarity stage output derived from token rows | `{ schema_version, generated_at, thresholds: { merge, review }, candidate_pairs: [{ left_idea_id, right_idea_id, score, type, signals, batch_id }] }` |
| `docs/project/ideatracker.json` | Final consumer-facing aggregate output | Preserve current top-level keys `schema_version`, `generated_at`, `source`, `summary`, `queues`, `duplicate_candidates`, and `ideas` |

## Phased Execution Plan

### Phase 1 - Stabilize the seam without breaking the CLI
Goal: keep the script usable while extracting deterministic pipeline boundaries.

| Task ID | Execution | Objective | Target files | Acceptance criteria | Validation command |
|---|---|---|---|---|---|
| T-IT-001 | sequential-only | Freeze the existing CLI/output contract and extract a thin orchestration seam so `scripts/IdeaTracker.py` remains the entrypoint while delegating non-CLI work to helpers. | `scripts/IdeaTracker.py`, `tests/test_idea_tracker.py` | Existing flags still work; current final payload keys and stdout success line stay unchanged; no placeholder helpers are introduced. | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_idea_tracker.py` |
| T-IT-002 | sequential-only | Introduce artifact writer/loader helpers with deterministic sorting and replace-by-batch semantics for JSON outputs written under `docs/project/`. | `scripts/idea_tracker_artifacts.py`, `scripts/IdeaTracker.py`, `tests/test_idea_tracker.py` | Each artifact file can be written after a batch, reloaded, and rewritten for the same `batch_id` without duplicate rows; filenames match the planned deterministic names. | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_idea_tracker.py -k artifact` |

### Phase 2 - Persist the incremental collection artifacts per batch
Goal: make collection resumable before changing downstream assembly behavior.

| Task ID | Execution | Objective | Target files | Acceptance criteria | Validation command |
|---|---|---|---|---|---|
| T-IT-003 | sequential-only | Refactor collection so each processed batch writes `progress`, `mapping`, `references`, and `section_names` artifacts immediately after the batch finishes. | `scripts/IdeaTracker.py`, `scripts/idea_tracker_artifacts.py`, `scripts/idea_tracker_pipeline.py`, `tests/test_idea_tracker.py` | A run with `--batch-size 2 --limit 5` produces all four artifacts after every batch; `progress.next_offset` advances deterministically; rerunning the same window rewrites the same rows only. | `c:/Dev/PyAgent/.venv/Scripts/python.exe scripts/IdeaTracker.py --verbose --batch-size 2 --limit 5 --output docs/project/ideatracker.json` |
| T-IT-004 | sequential-only | Persist token artifacts from the collected records so similarity can run from artifact state instead of reparsing markdown content. | `scripts/IdeaTracker.py`, `scripts/idea_tracker_pipeline.py`, `scripts/idea_tracker_artifacts.py`, `tests/test_idea_tracker.py` | `docs/project/ideatracker.tokens.json` is written batch-by-batch with stable `blocking_keys`; token rows are deterministic across repeated runs over the same input set. | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_idea_tracker.py -k token` |

### Phase 3 - Rebuild similarity and final assembly from persisted artifacts
Goal: preserve existing useful outputs while making the heavy pipeline restartable.

| Task ID | Execution | Objective | Target files | Acceptance criteria | Validation command |
|---|---|---|---|---|---|
| T-IT-005 | sequential-only | Move similarity candidate generation behind a helper that consumes `mapping`, `references`, and `tokens` artifacts and writes `ideatracker.similarities.json`. | `scripts/idea_tracker_similarity.py`, `scripts/IdeaTracker.py`, `scripts/idea_tracker_artifacts.py`, `tests/test_idea_tracker.py` | Similarity output preserves existing merge/review thresholds and candidate semantics; repeated runs over unchanged artifacts produce byte-stable candidate ordering. | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_idea_tracker.py -k similarity` |
| T-IT-006 | sequential-only | Assemble final `ideatracker.json` and split `ideatracker-NNNNNN.json` outputs from persisted artifacts, preserving current summary, queues, and duplicate candidate structure. | `scripts/IdeaTracker.py`, `scripts/idea_tracker_pipeline.py`, `scripts/idea_tracker_artifacts.py`, `tests/test_idea_tracker.py` | Final outputs remain backward-compatible for current consumers; split output still uses `-NNNNNN` offsets; assembly can run after a resumed batch job without re-reading already materialized artifact rows. | `c:/Dev/PyAgent/.venv/Scripts/python.exe scripts/IdeaTracker.py --batch-size 2 --limit 5 --output docs/project/ideatracker.json` |

### Phase 4 - Hardening, resume validation, and cutover convergence
Goal: prove the staged refactor is safe to ship and easy to back out.

| Task ID | Execution | Objective | Target files | Acceptance criteria | Validation command |
|---|---|---|---|---|---|
| T-IT-007 | sequential-only | Add regression coverage for interrupted runs, resumed runs, deterministic artifact rewriting, and preservation of current stdout/stderr behavior. | `tests/test_idea_tracker.py` | Tests cover interrupted batch resume, no duplicate artifact rows after rerun, verbose stderr progress, and final output parity on a fixture corpus. | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_idea_tracker.py` |
| T-IT-008 | sequential-only | Converge helper-module outputs back into the stable CLI workflow and document the rollback path: disable artifact-driven assembly by reverting to the pre-refactor orchestration seam while keeping generated artifacts ignorable. | `scripts/IdeaTracker.py`, `scripts/idea_tracker_pipeline.py`, `scripts/idea_tracker_artifacts.py`, `scripts/idea_tracker_similarity.py`, `tests/test_idea_tracker.py` | One end-to-end run produces all planned artifacts plus final outputs; rollback is a bounded revert of helper orchestration changes with no data migration required. | `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_idea_tracker.py && c:/Dev/PyAgent/.venv/Scripts/python.exe scripts/IdeaTracker.py --verbose --batch-size 1000 --output docs/project/ideatracker.json` |

## Validation Strategy
- Unit-level regression stays concentrated in `tests/test_idea_tracker.py` to avoid fragmenting existing tracker coverage during the refactor.
- The first safety gate is contract preservation: existing selectors for batching, verbosity, checkpoint behavior, and split output must stay green before any new artifact-specific tests are trusted.
- Resume validation must include an interrupted run followed by a rerun of the same batch window, confirming deterministic overwrite semantics and absence of duplicate rows.
- Final validation must compare a fresh full run against an equivalent resumed multi-batch run and confirm that `ideatracker.json` and split chunk files preserve current consumer-facing structure.
- Governance validation for this planning artifact remains required before handoff.

## Rollback Considerations
- Keep `scripts/IdeaTracker.py` as the single CLI entrypoint throughout the refactor so rollback does not require caller changes.
- Treat helper modules as internal implementation details; if the refactor stalls, revert helper orchestration while preserving the old `build_tracker_payload()` execution path.
- Make new artifact files additive. If the new pipeline is reverted, downstream consumers can ignore `ideatracker.progress.json`, `ideatracker.mapping.json`, `ideatracker.references.json`, `ideatracker.section_names.json`, `ideatracker.tokens.json`, and `ideatracker.similarities.json` without breaking the existing final output flow.
- Avoid schema churn after the first green batch implementation; if schema adjustments are required, bump `schema_version` once and update tests in the same change.

## Risks/Tradeoffs
- The current design artifact is incomplete, so this plan intentionally stays close to the present script behavior instead of introducing a broader architecture change.
- Persisting multiple artifacts increases I/O cost, but it is the simplest way to make 200k+ idea runs resumable and inspectable without adding an unrelated storage subsystem.
- Reassembling the final output from persisted artifacts adds coordination complexity; the tradeoff is acceptable because it removes the need to hold the full pipeline state in memory for long-running runs.
- Keeping all regression coverage in `tests/test_idea_tracker.py` is fast for this session, but if the file becomes unwieldy a later cleanup can split fixtures or focused test modules without changing the production plan.

## Milestones
| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | Stable CLI seam extracted | T-IT-001, T-IT-002 | PLANNED |
| M2 | Per-batch artifact persistence live | T-IT-003, T-IT-004 | PLANNED |
| M3 | Similarity and final assembly moved to persisted artifacts | T-IT-005, T-IT-006 | PLANNED |
| M4 | Resume and rollback proof complete | T-IT-007, T-IT-008 | PLANNED |

## Validation Commands
```powershell
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_idea_tracker.py
c:/Dev/PyAgent/.venv/Scripts/python.exe scripts/IdeaTracker.py --help
c:/Dev/PyAgent/.venv/Scripts/python.exe scripts/IdeaTracker.py --verbose --batch-size 2 --limit 5 --output docs/project/ideatracker.json
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
```

## Planning Evidence
- Branch gate: `git branch --show-current` -> `prj0000114-ideatracker-batching-verbosity`
- CLI validation: `c:/Dev/PyAgent/.venv/Scripts/python.exe scripts/IdeaTracker.py --help` -> PASS
- Tracker regression selector: `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_idea_tracker.py` -> `11 passed in 5.95s`
- Docs policy gate: `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` -> `17 passed in 10.68s`
