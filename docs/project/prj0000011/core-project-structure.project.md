# core-project-structure — Project Overview

_Status: COMPLETE_
_Owner: @1project | Updated: 2026-03-22_

## Project Identity
**Project ID:** prj0000011
**Short name:** core-project-structure
**Project folder:** `docs/project/prj0000011/`

## Project Overview
Establish the canonical directory hierarchy and starter files for the PyAgent
repository. The repository root is `C:\Dev\PyAgent`; the `docs/project/` area
holds metadata and documentation. Application source lives under `src/`. This
project defines the structure, verifies it via pytest, and provides a setup
script that recreates the layout in a fresh workspace.

## Goal & Scope
**Goal:** Create and verify the core project directory structure — `src/`,
`tests/structure/`, `scripts/`, `docs/` — with automated tests and a helper
script that builds the layout on demand.

**In scope:**
- `scripts/setup_structure.py` — creates core directory layout
- `scripts/validate_project_implementation.py` — validates layout in CI
- `tests/structure/test_base_dirs.py` — verifies root project dir exists
- `tests/structure/test_config_files.py` — verifies key config files
- `tests/core/test_core.py` — core module smoke tests
- `tests/test_core_agent_registry.py` — agent registry unit tests
- `tests/test_core_agent_state_manager.py` — state manager unit tests
- `tests/test_core_helpers.py` — shared helper unit tests
- `tests/test_core_quality.py` — code quality helper tests
- `docs/project/prj0000011/` — project docs

**Out of scope:** Agent business logic, runtime, frontend, Rust core.

## Branch Plan
**Expected branch:** `prj0000011-core-project-structure`
**Scope boundary:** `scripts/setup_structure.py`, `scripts/validate_project_implementation.py`,
  `tests/structure/`, `tests/core/`, `tests/test_core_*.py`, `docs/project/prj0000011/`
**Handoff rule:** Merge to `main` via PR once all structure tests pass. No downstream agent
  handoff required — this is a structural bootstrapping project.
**Failure rule:** If branch does not match expected, stop immediately and escalate to
  `@0master`. Record blocked status in this file.

## Acceptance Criteria
- `scripts/setup_structure.py` creates `src/`, `tests/`, `docs/`, `scripts/` when run
- `tests/structure/test_base_dirs.py::test_root_project_dir_exists` passes
- `tests/test_core_agent_registry.py` passes
- `tests/test_core_agent_state_manager.py` passes
- All structure tests pass under `pytest tests/structure/ -q`

## Status
COMPLETE — all acceptance criteria met. Code already present in repo.
