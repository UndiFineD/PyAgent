# Prj002 Core System

## Goal

Create a small, well-tested foundational core system that provides:

- a deterministic runtime for executing agent tasks and workflows
- a lightweight, in-memory task queue for scheduling work
- a registry for agent definitions and lookup
- a simple in-memory store for ephemeral state
- a minimal observability API for emitting metrics and structured events

This core should be easy to reason about, fully unit-tested, and suitable for use by higher-level agent orchestration layers.

## Success criteria

- Core components are implemented in `src/core/` with `validate()` methods for self-checking.
- Core behavior is fully covered by focused unit tests under `tests/test_core_*.py`.
- CI validates core correctness via the unified `ci.yml` / pre-commit pipeline.
- Documentation describes the core abstractions and how they are intended to be used.

## Tasks

- [x] Define core system requirements and architecture in `brainstorm.md`.
- [x] Implement `Runtime` with deterministic scheduling and validation (`src/core/runtime.py`).
- [x] Implement `TaskQueue` with enqueue/dequeue and validation (`src/core/task_queue.py`).
- [x] Implement `AgentRegistry` with registration and lookup functionality (`src/core/agent_registry.py`).
- [x] Implement `MemoryStore` as an in-memory key/value store with `validate()` (`src/core/memory.py`).
- [x] Implement `emit_metric()` and related helpers in `src/core/observability.py`.
- [x] Add meta-tests that assert core modules are importable, validate without side effects, and avoid circular imports.
- [x] Ensure CI runs the core test suite via `ci.yml` and pre-commit.
- [x] Keep docs updated and in sync with the actual implementation.
