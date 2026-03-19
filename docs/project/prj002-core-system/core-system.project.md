# core-system

**Project ID:** `prj002-core-system`

## Links

- Plan: `plan.md`
- Design: `brainstorm.md`

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

## Status

9 of 9 tasks completed

## Code detection

- Code detected in:
  - `rust_core\src\utils\system.rs`
  - `tests\core\test_core.py`
  - `tests\test_core_agent_registry.py`
  - `tests\test_core_agent_state_manager.py`
  - `tests\test_core_helpers.py`
  - `tests\test_core_observability.py`
  - `tests\test_core_providers_FlmChatAdapter.py`
  - `tests\test_core_providers_FlmProviderConfig.py`
  - `tests\test_core_quality.py`
  - `tests\test_core_runtime.py`
  - `tests\test_core_task_queue.py`
  - `tests\test_core_workflow_engine.py`
  - `tests\test_rust_core.py`
  - `tests\test_system_integration.py`