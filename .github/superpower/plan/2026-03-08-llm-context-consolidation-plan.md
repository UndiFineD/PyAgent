# LLM Context Consolidation Implementation Plan

**Goal:** Implement `scripts/consolidate_llm_context.py` to consolidate scattered markdown context into a tiered `llms*.txt` structure, optionally migrate component markdown into Python module docstrings, and generate a deterministic consolidation report.

**Architecture:** Single Python CLI utility with deterministic file discovery, dry-run/apply modes, tiered output writers, optional docstring migration, and transactional-like write ordering (write outputs first, cleanup only in apply mode after successful writes).

**Tech Stack:** Python 3.14 stdlib, pytest, pathlib, argparse, re, dataclasses, json, datetime.

---

## 1) Scope and Acceptance Criteria

### In Scope
- Create `scripts/consolidate_llm_context.py`.
- Generate:
  - `llms.txt`
  - `llms-architecture.txt`
  - `llms-improvements.txt`
- Consolidate content from:
  - `docs/architecture/**/*.md` -> `llms-architecture.txt`
  - `**/*.description.md` and `**/*.improvements.md` -> `llms-improvements.txt`
- Optional migration of component markdown into matching Python module docstrings.
- Generate `consolidation_report.txt` with merged/deleted/skipped/errors summary.
- Support dry-run by default and `--apply` for real mutations.

### Out of Scope (for this plan iteration)
- Updating external custom agents at `C:\Users\keimpe\.superpower-copilot\agents`.
- CI workflow file changes beyond local script/test implementation.

### Definition of Done
- All new targeted tests pass.
- Existing sanity tests pass:
  - `tests/test_repo_layout_scaffold.py`
  - `tests/test_dryrun_lists_moves.py`
- Script is idempotent and deterministic.
- Dry-run performs no destructive file operations.

---

## 2) File Map

### Files to Create
- `tests/test_consolidate_llm_context_cli.py`
- `tests/test_consolidate_llm_context_outputs.py`
- `tests/test_consolidate_llm_context_merge.py`
- `tests/test_consolidate_llm_context_docstrings.py`
- `tests/test_consolidate_llm_context_cleanup_report.py`
- `tests/test_consolidate_llm_context_integration.py`

### Files to Modify
- `scripts/consolidate_llm_context.py` (currently whitespace-only)

### Optional Follow-up (separate commit)
- `.github/copilot-instructions.md` (guidance to append context to `llms-*.txt` instead of new stray markdown files)

---

## 3) Implementation Phases (TDD-first)

## Phase 1 — CLI contract and argument parsing

**Objective:** establish a stable CLI with safe defaults and explicit modes.

### Step 1.1: Write failing tests
- File: `tests/test_consolidate_llm_context_cli.py`
- Tests:
  - default mode is dry-run.
  - `--apply` sets apply mode.
  - `--repo-root` and `--output-dir` are honored.
  - invalid combination handling (if any) returns non-zero.

### Step 1.2: Run test (expect fail)
- Command:
  - `.venv\Scripts\python.exe -m pytest tests/test_consolidate_llm_context_cli.py -v`
- Expected:
  - At least one failing test due to missing implementation.

### Step 1.3: Implement minimal CLI
- File: `scripts/consolidate_llm_context.py`
- Add:
  - shebang + required license header.
  - `main()` and argparse parser.
  - dataclass config object.
  - dry-run default.

### Step 1.4: Re-run test (expect pass)
- Command:
  - `.venv\Scripts\python.exe -m pytest tests/test_consolidate_llm_context_cli.py -v`

---

## Phase 2 — Tiered file scaffolding

**Objective:** create deterministic base content for `llms*.txt` outputs.

### Step 2.1: Write failing tests
- File: `tests/test_consolidate_llm_context_outputs.py`
- Assertions:
  - `llms.txt` is generated with high-level project summary and pointers.
  - `llms-architecture.txt` and `llms-improvements.txt` are generated.
  - output ordering is deterministic.

### Step 2.2: Run test (expect fail)
- Command:
  - `.venv\Scripts\python.exe -m pytest tests/test_consolidate_llm_context_outputs.py -v`

### Step 2.3: Implement output writer
- File: `scripts/consolidate_llm_context.py`
- Add:
  - content builder functions for each llms file.
  - normalized line endings (`\n`) and stable section ordering.

### Step 2.4: Re-run test (expect pass)
- Command:
  - `.venv\Scripts\python.exe -m pytest tests/test_consolidate_llm_context_outputs.py -v`

---

## Phase 3 — Discovery and content merge

**Objective:** discover target markdown files and merge content into correct tier.

### Step 3.1: Write failing tests
- File: `tests/test_consolidate_llm_context_merge.py`
- Fixture structure:
  - `docs/architecture/*.md`
  - nested `*.description.md`
  - nested `*.improvements.md`
- Assertions:
  - architecture markdown appears only in `llms-architecture.txt`.
  - description/improvements markdown appears only in `llms-improvements.txt`.
  - source file headings include path labels for traceability.

### Step 3.2: Run test (expect fail)
- Command:
  - `.venv\Scripts\python.exe -m pytest tests/test_consolidate_llm_context_merge.py -v`

### Step 3.3: Implement scanners + merger
- File: `scripts/consolidate_llm_context.py`
- Add:
  - glob scanners using pathlib.
  - normalized reader with UTF-8 fallback handling.
  - deterministic sorted merge by relative path.

### Step 3.4: Re-run test (expect pass)
- Command:
  - `.venv\Scripts\python.exe -m pytest tests/test_consolidate_llm_context_merge.py -v`

---

## Phase 4 — Optional module docstring migration

**Objective:** migrate component markdown into related Python module docstrings safely.

### Step 4.1: Write failing tests
- File: `tests/test_consolidate_llm_context_docstrings.py`
- Assertions:
  - when `foo.py` and `foo.description.md` exist, script injects/updates module docstring section.
  - shebang/license header remains intact.
  - repeated runs are idempotent (no duplicate blocks).

### Step 4.2: Run test (expect fail)
- Command:
  - `.venv\Scripts\python.exe -m pytest tests/test_consolidate_llm_context_docstrings.py -v`

### Step 4.3: Implement migration logic
- File: `scripts/consolidate_llm_context.py`
- Add:
  - mapping from markdown base filename to module path.
  - guarded section markers in docstring (e.g., `LLM_CONTEXT_START/END`).
  - apply only when explicitly enabled (e.g., `--migrate-docstrings`).

### Step 4.4: Re-run test (expect pass)
- Command:
  - `.venv\Scripts\python.exe -m pytest tests/test_consolidate_llm_context_docstrings.py -v`

---

## Phase 5 — Cleanup semantics and report generation

**Objective:** safe deletion behavior and complete reporting.

### Step 5.1: Write failing tests
- File: `tests/test_consolidate_llm_context_cleanup_report.py`
- Assertions:
  - dry-run: no source markdown deleted.
  - apply: consolidated markdown deleted only after successful output write.
  - `consolidation_report.txt` includes counters and path lists.

### Step 5.2: Run test (expect fail)
- Command:
  - `.venv\Scripts\python.exe -m pytest tests/test_consolidate_llm_context_cleanup_report.py -v`

### Step 5.3: Implement cleanup + report
- File: `scripts/consolidate_llm_context.py`
- Add:
  - result model (merged/deleted/skipped/errors).
  - report writer to repo root (or configured output dir).
  - cleanup gate: execute deletions only in `--apply` and only for files successfully merged.

### Step 5.4: Re-run test (expect pass)
- Command:
  - `.venv\Scripts\python.exe -m pytest tests/test_consolidate_llm_context_cleanup_report.py -v`

---

## Phase 6 — End-to-end validation

**Objective:** verify integrated behavior against representative fixture repos.

### Step 6.1: Write failing integration test
- File: `tests/test_consolidate_llm_context_integration.py`
- Scenario:
  - seeded fixture with architecture, improvements, and module markdown.
  - run dry-run then apply.
  - verify outputs, optional docstrings, report, and cleanup rules.

### Step 6.2: Run test (expect fail)
- Command:
  - `.venv\Scripts\python.exe -m pytest tests/test_consolidate_llm_context_integration.py -v`

### Step 6.3: Implement remaining gaps
- File: `scripts/consolidate_llm_context.py`
- Patch integration defects surfaced by Phase 6 test.

### Step 6.4: Run full targeted suite
- Command:
  - `.venv\Scripts\python.exe -m pytest tests/test_consolidate_llm_context_*.py -v`

### Step 6.5: Run existing guard tests
- Command:
  - `.venv\Scripts\python.exe -m pytest tests/test_repo_layout_scaffold.py tests/test_dryrun_lists_moves.py -v`

---

## 4) Command Summary (single-run checklist)

1. `.venv\Scripts\python.exe -m pytest tests/test_consolidate_llm_context_cli.py -v`
2. `.venv\Scripts\python.exe -m pytest tests/test_consolidate_llm_context_outputs.py -v`
3. `.venv\Scripts\python.exe -m pytest tests/test_consolidate_llm_context_merge.py -v`
4. `.venv\Scripts\python.exe -m pytest tests/test_consolidate_llm_context_docstrings.py -v`
5. `.venv\Scripts\python.exe -m pytest tests/test_consolidate_llm_context_cleanup_report.py -v`
6. `.venv\Scripts\python.exe -m pytest tests/test_consolidate_llm_context_integration.py -v`
7. `.venv\Scripts\python.exe -m pytest tests/test_consolidate_llm_context_*.py -v`
8. `.venv\Scripts\python.exe -m pytest tests/test_repo_layout_scaffold.py tests/test_dryrun_lists_moves.py -v`

---

## 5) Risks and Mitigations

- **Risk:** false-positive docstring mapping modifies wrong module.
  - **Mitigation:** only map by strict basename/path rules; log skipped ambiguous matches.
- **Risk:** accidental deletion during consolidation.
  - **Mitigation:** default dry-run; cleanup only in apply and only for successfully merged files.
- **Risk:** non-deterministic outputs creating noisy diffs.
  - **Mitigation:** stable sort by normalized relative path; normalized newlines.
- **Risk:** encoding issues in legacy markdown.
  - **Mitigation:** robust read fallback + error accounting in report.

---

## 6) Handoff

After this plan is approved and saved, execute in `superpower-execute` mode.
Do not implement code changes in `superpower-plan` mode.
