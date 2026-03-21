# Prj004 Llm Context Consolidation

**Project ID:** prj004-llm-context-consolidation

## Links

- Plan: plan.md
- Design: rainstorm.md

## Tasks

- [ ] Create `scripts/consolidate_llm_context.py` with dry-run and apply modes.
- [ ] Implement deterministic consolidation into `llms.txt`, `llms-architecture.txt`, and `llms-improvements.txt`.
- [ ] Add support for migrating component markdown into Python module docstrings.
- [ ] Generate `consolidation_report.txt` summarizing merged/skipped/deleted files.
- [ ] Add a suite of unit/integration tests ensuring idempotent, non-destructive behavior.

## Status

0 of 5 tasks completed

## Code detection

- Expected code in:
  - `scripts/consolidate_llm_context.py`
  - `tests/test_consolidate_llm_context_*.py`
  - Generated output: `llms*.txt`, `consolidation_report.txt`

## Branch Plan

**Expected branch:** `prj0000004-llm-context-consolidation`
**Scope boundary:** `docs/project/prj0000004/`, `scripts/consolidate_llm_context.py`, `tests/test_consolidate_llm_context_*.py`.
**Handoff rule:** `@9git` must refuse staging, commit, push, or PR unless the active branch matches the expected branch above and changed files stay within the scope boundary.
