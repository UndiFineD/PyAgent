# standards-docs

**Project ID:** `prj0000034`

## Links

- Plan: `plan.md`
- Design: `brainstorm.md`

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

## Status

0 of 10 tasks completed

## Code detection

- Code detected in:
  - `tests\docs\test_agent_workflow_policy_docs.py`
  - `tests\docs\test_api_docs_exist.py`
  - `tests\docs\test_docs_exist.py`
  - `tests\test_consolidate_llm_context_docstrings.py`
  - `tests\test_flm_provider_docs.py`
  - `tests\tools\test_tools_docs.py`