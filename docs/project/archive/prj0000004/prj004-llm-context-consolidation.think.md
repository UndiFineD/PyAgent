# prj004-llm-context-consolidation — Options

_Status: IN_PROGRESS_
_Analyst: @2think | Updated: 2026-03-19_

---

## 1. Root Cause Analysis

This project exists because the repository currently has *scattered* LLM context sources (documentation, design notes, improvement drafts, etc.) that are difficult for agents and tooling to consume reliably. The desired outcome is a repeatable, deterministic pipeline that consolidates those sources into a small set of well-known context files (`llms.txt`, `llms-architecture.txt`, `llms-improvements.txt`) and produces an audit report.

Existing pain points:

- **Non-deterministic agent context**: Different runs can return different subsets of docs depending on file system order.
- **Manual maintenance**: Authors must remember to update `llms.txt` and related artifacts manually.
- **No audit trail**: There's no record of what was merged, skipped, or deleted when generating context.
- **Risk of destructive changes**: Without a dry-run mode, scripts can accidentally delete or overwrite source documentation.

## 2. Options

### Option A — Single Script Consolidator (Recommended)

**Approach:** Implement `scripts/consolidate_llm_context.py` as a single CLI tool that discovers source files, merges content deterministically, writes standard outputs, optionally migrates component markdown into Python module docstrings, and emits a detailed `consolidation_report.txt`. Supports dry-run by default and `--apply` for destructive changes.

**Pros:**
- ✅ Centralized logic (single source of truth)
- ✅ Easy to validate with unit tests and fixtures
- ✅ Supports safe experimentation (dry-run)
- ✅ Aligns with existing repository pattern (`scripts/*.py` + `tests/test_*.py`)

**Cons:**
- ⚠️ A single script can become complex; needs internal decomposition (small helper functions, dataclasses)

### Option B — Multiple Focused Scripts (Split by Output)

**Approach:** Build separate scripts for each output file (`scripts/generate_llms_txt.py`, `scripts/generate_llms_architecture.py`, etc.), then wrap them in a coordinator.

**Pros:**
- ✅ Smaller, targeted units that are easy to test
- ✅ Reuse existing `generate_llms_architecture.py` patterns

**Cons:**
- ❌ More CLI surface area
- ❌ More integration glue to ensure deterministic ordering and shared report generation

### Option C — Git Hook / CI-Only Generator

**Approach:** Implement generator purely as a CI/PR validation step (e.g., `pre-commit` hook or GitHub Action) rather than a general-purpose CLI.

**Pros:**
- ✅ Ensures updated outputs in CI
- ❌ Not usable locally as a tool for creators (less flexible)

## 3. Decision Matrix

| Criterion | Option A | Option B | Option C |
|---|---|---|---|
| Complete end-to-end workflow (dry-run + apply + report) | ✅ | ⚠️ (needs integration) | ❌ (no local usage) |
| Tests easily expressible (unit/integration) | ✅ | ✅ | ⚠️ (harder to simulate CI) |
| Fits existing repo conventions (scripts + pytest) | ✅ | ✅ | ❌ |
| Future maintenance burden | ⚠️ (complexity) | ⚠️ (more moving parts) | ✅ (simple, but less usable) |

**Recommended:** Option A — Single Script Consolidator.

---

## 4. Recommended Implementation Plan (TDD-first)

This plan is written as a series of concrete tasks that feed directly into the next phase (`@3design` / coding). Each task is a minimal unit of work with a clear test expectation.

### Phase 1 — CLI contract and basic dry-run scaffolding

**Goal:** Provide a stable CLI surface with safe defaults and a deterministic dry-run mode.

#### Tasks
1. **Create failing tests for CLI contract**
   - File: `tests/test_consolidate_llm_context_cli.py`
   - Verify:`
     - Running the script without arguments uses dry-run mode.
     - `--apply` enables mutating behavior (flags in result object).
     - `--repo-root` and `--output-dir` are respected.
     - Unknown args trigger `SystemExit` with non-zero.

2. **Implement CLI parser and config model**
   - File: `scripts/consolidate_llm_context.py`
   - Create `main()` that returns exit code.
   - Use `argparse` with:
     - `--repo-root` (default `.`)
     - `--output-dir` (default repo root)
     - `--apply` (store_true)
     - `--dry-run` (default behavior; `--apply` toggles)
     - `--verbose` (optional logging)
     - `--migrate-docstrings` (optional toggle)

3. **Run CLI contract tests** (should pass after implementation)
   - Command: `python -m pytest tests/test_consolidate_llm_context_cli.py -q`

### Phase 2 — Deterministic Tiered Output Generation

**Goal:** Create the three canonical output files with stable ordering and content structure.

#### Tasks
1. **Write failing tests for output generation**
   - File: `tests/test_consolidate_llm_context_outputs.py`
   - Confirm that after running in dry-run mode, the following are produced in the output directory:
     - `llms.txt`
     - `llms-architecture.txt`
     - `llms-improvements.txt`
   - Confirm each file has a stable header and deterministically sorted section ordering.
   - Confirm repeated runs yield byte-identical output.

2. **Implement content scaffolding**
   - In `scripts/consolidate_llm_context.py`, add helper functions:
     - `_build_llms_txt(...)` (high-level repo summary and pointers)
     - `_build_llms_architecture_txt(...)` (consolidated docs/architecture/* content)
     - `_build_llms_improvements_txt(...)` (consolidated `*.description.md` / `*.improvements.md`)
   - Use a deterministic sort key (e.g., `str(path.relative_to(repo_root))`).
   - Normalize newlines to `\n` and remove trailing whitespace.

3. **Run output generation tests**
   - Command: `python -m pytest tests/test_consolidate_llm_context_outputs.py -q`

### Phase 3 — Source discovery and merge semantics

**Goal:** Discover source files, load their content, and merge into the correct output bucket.

#### Tasks
1. **Write failing tests for file discovery and merge**
   - File: `tests/test_consolidate_llm_context_merge.py`
   - Create a fixture repository structure:
     - `docs/architecture/Alpha.md`, `docs/architecture/sub/Beta.md`
     - `components/foo.description.md`, `components/foo.improvements.md`
   - Assert:
     - Architecture markdown only appears in `llms-architecture.txt`.
     - `*.description.md` and `*.improvements.md` only appear in `llms-improvements.txt`.
     - Each inclusion is annotated with a stable `--- Source: <path> ---` header.
     - No content is duplicated across output files.

2. **Implement discovery + merge**
   - Add functions:
     - `_discover_architecture_files(repo_root)` → sorted list.
     - `_discover_improvement_files(repo_root)` (pattern `**/*.description.md` and `**/*.improvements.md`)
     - `_render_markdown_source(path, repo_root)` returns normalized text with source header.
   - Ensure reading uses `utf-8` and falls back to `utf-8-sig`.

3. **Run merge tests**
   - Command: `python -m pytest tests/test_consolidate_llm_context_merge.py -q`

### Phase 4 — Optional docstring migration (component markdown → Python modules)

**Goal:** Provide a safe, toggleable migration path where `*.description.md` content can be embedded into matching Python module docstrings.

#### Tasks
1. **Write failing tests for migration behavior**
   - File: `tests/test_consolidate_llm_context_docstrings.py`
   - Fixture scenario:
     - `src/example.py` with an existing module docstring.
     - `src/example.description.md` with new text.
   - Assertions:
     - Running with `--migrate-docstrings` inserts/replaces a bounded section within the module docstring.
     - The rest of the file (license header, imports) is unchanged.
     - Second run is idempotent (no duplication of the migration marker block).

2. **Implement migration logic**
   - Define markers, e.g.:
     - `<!-- LLM CONTEXT START -->` / `<!-- LLM CONTEXT END -->` inside triple-quoted module docstring.
   - Strategy:
     - Locate the existing module docstring (PEP 257): first statement in a module.
     - If missing, create one at file top (after any shebang + license header).
     - Replace or insert content between markers.
     - Only touch files when `--apply` is enabled.
   - If `--migrate-docstrings` is set but no matching `.description.md` is found, log and continue.

3. **Run migration tests**
   - Command: `python -m pytest tests/test_consolidate_llm_context_docstrings.py -q`

### Phase 5 — Report generation & cleanup semantics

**Goal:** Provide auditability and safe cleanup behavior without surprising users.

#### Tasks
1. **Write failing tests for reporting and cleanup**
   - File: `tests/test_consolidate_llm_context_cleanup_report.py`
   - Scenarios:
     - Dry-run: no source files deleted, output files are generated in a temporary directory.
     - Apply: after a successful run, source markdown files that were merged are deleted.
     - If a write fails (e.g., read-only output file), no deletions occur.
   - Validate `consolidation_report.txt` includes:
     - `merged_files`, `skipped_files`, `deleted_files`, `errors` sections
     - A timestamp and command-line options used.

2. **Implement report + safe cleanup**
   - Create a result dataclass:
     - `merged: list[pathlib.Path]`
     - `deleted: list[pathlib.Path]`
     - `skipped: list[pathlib.Path]`
     - `errors: list[tuple[pathlib.Path, str]]`
   - Write `consolidation_report.txt` (in repo root by default) even in dry-run.
   - Protection rules:
     - Only delete files in `--apply` mode.
     - Only delete source files that were successfully merged into an output. If an exception occurs during merge, do not delete any files.
     - If output writing fails, do nothing to source files.

3. **Run report+cleanup tests**
   - Command: `python -m pytest tests/test_consolidate_llm_context_cleanup_report.py -q`

### Phase 6 — End-to-end (integration) validation

**Goal:** Verify the entire workflow behaves correctly in a realistic repository snapshot and is deterministic.

#### Tasks
1. **Write failing integration test**
   - File: `tests/test_consolidate_llm_context_integration.py`
   - Setup a realistic mini-repo:
     - `docs/architecture/*` (multiple markdown files)
     - `components/*` with `.description.md` / `.improvements.md`
     - Some Python modules with and without existing docstrings.
   - Assert after dry-run:
     - Output files are created with expected content.
     - No input files deleted.
   - Assert after apply:
     - Output files contain the same content.
     - Marked source files are deleted.
     - Module docstrings updated if migration enabled.
     - `consolidation_report.txt` lists the expected counts.

2. **Run integration test**
   - Command: `python -m pytest tests/test_consolidate_llm_context_integration.py -q`

3. **Validation**
   - Ensure the consolidation is deterministic by running twice and comparing file hashes.
   - Ensure `llms.txt` follows the llms.txt specification (consistent header and link list). For this plan, at minimum verify the expected sections are present.

---

## 5. Failure Modes and Mitigations

### 5.1 Non-deterministic output
**Cause:** filesystem ordering or unstable sort.  
**Mitigation:** Always sort by `path.as_posix()` and normalize newline endings. Unit tests should compare file content byte-for-byte across runs.

### 5.2 Accidental deletion in dry-run
**Cause:** rely on deletion logic without gating by `--apply`.  
**Mitigation:** Dry-run must never delete; enforce via unit tests and an explicit `apply` boolean gate.

### 5.3 Partial write / interrupted run
**Cause:** crash while writing outputs.  
**Mitigation:** Write outputs to `.tmp` files, then atomically rename into place. Only delete sources after all outputs have successfully written.

### 5.4 Encoding errors in source markdown
**Cause:** non-UTF-8 files.  
**Mitigation:** Try `utf-8` first, then `utf-8-sig`. If still failing, capture the error in `consolidation_report.txt` and skip the file.

### 5.5 Incorrect module docstring injection
**Cause:** mis-parsing of module docstring (edge cases, shebang, encoding cookie, `__future__` import statements).  
**Mitigation:** Use a minimal safe parser (regex + heuristic) and keep the migration optional. Add explicit test cases for common patterns.

---

## 6. Validation Checklist (for `@3design` / `@6code` handoff)

✅ `scripts/consolidate_llm_context.py` exists and follows repo script conventions (shebang, license header, `main()` entry point).  

✅ Tests are present under `tests/test_consolidate_llm_context_*.py` covering:
- CLI argument contract
- Output generation & determinism
- Discovery and merging behavior
- Optional docstring migration
- Cleanup & reporting
- End-to-end integration

✅ Outputs are deterministic and idempotent. Running the script twice on the same input produces identical `llms*.txt` and report files.

✅ Dry-run is safe: no source mutations and report indicates what *would* change.

✅ Apply mode mutates the repository only after successful output generation.

✅ Consolidation output files are in the expected locations: `<repo-root>/llms.txt`, `<repo-root>/llms-architecture.txt`, `<repo-root>/llms-improvements.txt`, and `<repo-root>/consolidation_report.txt`.

✅ All new tests pass under the existing test harness (`pytest -q`).

✅ Code style matches repo patterns (pathlib, dataclasses, minimal dependencies, no external libs).

---

## 7. Open Questions

1. **What is the canonical location for `consolidation_report.txt`?** (repo root, `docs/`, or `data/`?)
2. **Should `llms.txt` strictly follow the llms.txt spec (header + link lists), or is a more freeform ‘LLM context dump’ acceptable?**
3. **Should `--apply` only delete source markdown files, or also delete outputs that are no longer produced (i.e., orphan cleanup)?**
4. **Is there a need to support incremental runs where only changed files are re-merged (for performance on large repos)?**

---

*Next step (for @3design): Use this plan to define the exact module/class structure for `scripts/consolidate_llm_context.py` (e.g., `ConsolidationRunner`, `DiscoveryStrategy`, `OutputWriter`, `DocstringMigrator`), and confirm the E2E expectations for file paths and report schema.*
