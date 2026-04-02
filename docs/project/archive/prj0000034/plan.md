# Prj0000034 Context Manager

_Status: IN_PROGRESS_
_Planner: @4plan | Updated: 2026-06-13_

## Goal

Build the `src/context_manager` package that creates, merges, diffs, and
shares context objects between agents. Contexts are immutable once created,
hierarchical (global → agent-specific), and privacy-aware.

## Design Principles

- **Immutable snapshots** — contexts versioned and frozen on creation for safe
  concurrent reasoning.
- **Hierarchical structure** — nested contexts with inheritance and overrides.
- **Diff/merge utilities** — efficient sync between nodes and incremental saves.
- **Privacy & access control** — sensitive context data is redacted or access
  is controlled by sharing rules.

## Tasks

- [ ] Define context schema (metadata, tags, content, version, parent_id)
- [ ] Implement `ContextSnapshot` (immutable, hashable, serialisable)
- [ ] Implement hierarchical `ContextTree` with inheritance and override rules
- [ ] Implement `ContextDiffer` for computing diffs between snapshots
- [ ] Implement `ContextMerger` with conflict resolution strategies
- [ ] Implement `ContextSharingManager` with access-control and redaction
- [ ] Add compression strategies for large context payloads (lossless)
- [ ] Integrate with `MemoryTransaction` for atomic context persistence
- [ ] Write tests: `tests/test_context_manager.py`
- [ ] Document design in `docs/architecture/context-manager.md`

## Milestones

| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | Schema and immutable snapshot | T1, T2 | NOT_STARTED |
| M2 | Hierarchy and diff/merge | T3, T4, T5 | NOT_STARTED |
| M3 | Privacy and sharing | T6 | NOT_STARTED |
| M4 | Compression and persistence | T7, T8 | NOT_STARTED |
| M5 | Tests and docs | T9, T10 | NOT_STARTED |
