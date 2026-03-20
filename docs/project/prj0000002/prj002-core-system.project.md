# Prj002 Core System

**Project ID:** prj002-core-system

## Links

- Plan: plan.md
- Design: brainstorm.md

## Tasks

- [x] Define project goal, scope, and acceptance criteria.
- [x] Implement core runtime module (`src/core/runtime.py`) with a `Runtime` API and `validate()` self-check.
- [x] Implement core task queue module (`src/core/task_queue.py`) with `TaskQueue` and `validate()`.
- [x] Implement agent registry module (`src/core/agent_registry.py`) with `AgentRegistry` and `validate()`.
- [x] Implement in-memory store module (`src/core/memory.py`) with `MemoryStore` and `validate()`.
- [x] Implement observability helpers (`src/core/observability.py`) and `validate()`.
- [x] Add meta-tests that enforce core hygiene and detect circular imports.
- [x] Ensure core tests run in CI via the unified `ci.yml` and pre-commit checks.
- [x] Keep the design and plan documentation updated.

## Status

10 of 10 tasks completed

## Code detection

- Core modules are present in `src/core/`.
- Core tests live under `tests/test_core_*.py`.
