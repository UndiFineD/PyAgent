# llm-context-consolidation

**Project ID:** `prj0000004`

## Links

- Plan: `plan.md`
- Design: `brainstorm.md`

## Tasks

- [x] Add `scripts/consolidate_llm_context.py` CLI tool with dry-run default and `--apply`.
- [x] Generate deterministic `llms.txt`, `llms-architecture.txt`, and `llms-improvements.txt`.
- [x] Discover source markdown from `docs/architecture/**/*.md`, `**/*.description.md`, and `**/*.improvements.md`.
- [x] Add optional module docstring migration via `--migrate-docstrings`.
- [x] Produce `consolidation_report.txt` with counts + source/output details.
- [x] Add full test suite ensuring determinism, idempotence, and safe cleanup.

## Status

6 of 6 tasks completed

## Code detection

- Code detected in:
  - `scripts\consolidate_llm_context.py`
  - `scripts\generate_llms_architecture.py`
  - `src\core\ContextTransactionManager.py`
  - `src\transactions\ContextTransactionManager.py`
  - `tests\deploy\test_compose_context_contract.py`
  - `tests\integration\test_context_and_skills.py`
  - `tests\test_consolidate_llm_context_cleanup_report.py`
  - `tests\test_consolidate_llm_context_cli.py`
  - `tests\test_consolidate_llm_context_docstrings.py`
  - `tests\test_consolidate_llm_context_integration.py`
  - `tests\test_consolidate_llm_context_outputs.py`
  - `tests\test_context_components.py`
  - `tests\test_context_manager.py`
  - `tests\test_context_window.py`
  - `tests\test_ContextTransactionManager.py`