# Prj001 Core System

**Project ID:** prj001-core-system

## Links

- Plan: plan.md
- Design: brainstorm.md

## Tasks

- [x] Implement core runtime module (`src/core/runtime.py`) with `Runtime` and `validate()`.
- [x] Implement core task queue module (`src/core/task_queue.py`) with `TaskQueue` and `validate()`.
- [x] Implement agent registry module (`src/core/agent_registry.py`) with `AgentRegistry` and `validate()`.
- [x] Implement in-memory store module (`src/core/memory.py`) with `MemoryStore` and `validate()`.
- [x] Implement observability helpers (`src/core/observability.py`) with `emit_metric()` and `validate()`.
- [x] Add core hygiene meta-tests (`tests/test_core_quality.py`).
- [x] Ensure core tests are included in CI (`.github/workflows/ci-python-core.yml`).
- [x] Document design and plan in docs.

## Status

8 of 8 tasks completed

## Code detection

- `src/core/runtime.py`
- `src/core/task_queue.py`
- `src/core/agent_registry.py`
- `src/core/memory.py`
- `src/core/observability.py`
- `tests/test_core_quality.py`
- `tests/test_core_runtime.py`
- `tests/test_core_task_queue.py`
- `tests/test_core_observability.py`

## Branch Plan

**Expected branch:** `prj0000040-core-system`
**Scope boundary:** `docs/project/prj0000040/` and associated `src/core/` files.
**Handoff rule:** `@9git` must refuse staging, commit, push, or PR unless the active branch matches the expected branch above and changed files stay within the scope boundary.
