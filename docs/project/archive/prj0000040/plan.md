# Prj001 Core System

## Goal
Provide a stable, testable foundation for PyAgent’s core runtime layer by defining the minimal set of primitives and helpers that all higher-level agents and tools rely on.

## Objectives
- Define a lightweight async runtime abstraction for scheduling work.
- Provide a robust task queue for asynchronous task execution.
- Offer a registry for agent discovery and registration.
- Implement an in-memory shared state store.
- Add observability primitives for metrics and diagnostics.
- Ensure the core system is self-validating via unit tests and meta-tests.

## In Scope
- `src/core/runtime.py`
- `src/core/task_queue.py`
- `src/core/agent_registry.py`
- `src/core/memory.py`
- `src/core/observability.py`
- `tests/test_core_quality.py` + per-module unit tests in `tests/test_core_*.py`

## Out of Scope
- External persistence backends (databases, caches) beyond in-memory store.
- Business logic in individual agents; core system should remain generic.

## Definition of Done
- Core modules exist and export `validate()` self-checks.
- Core meta-tests pass and guard against missing modules / circular imports.
- Documentation clearly describes the core system architecture and rationale.
- CI executes core tests and passes.

## Notes
This project is intentionally small: it exists to make the rest of PyAgent predictable and testable, not to provide business features.
