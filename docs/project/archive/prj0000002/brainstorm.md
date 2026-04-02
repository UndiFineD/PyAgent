# Prj002 Core System Brainstorm

## Core design principles

- **Minimal dependencies**: Core should use only the standard library (plus any shared internal utilities) so it can be imported early without pulling in heavy external dependencies.
- **Self-validating modules**: Each core module provides a `validate()` function that performs a lightweight, deterministic self-check. This enables fast smoke tests and CI validation.
- **Loose coupling**: Core components (runtime, queue, registry, memory, observability) should be loosely coupled to allow future replacement (e.g., swapping in a different queue implementation).
- **Test-first architecture**: The core is driven by targeted tests that ensure interfaces are stable, prevent circular imports, and verify the minimal contract for each component.

## Key components

### Runtime
- Orchestrates execution of tasks/workflows.
- Provides a stable API for scheduling and cancellation.
- Exposes `validate()` to confirm the runtime can start and shutdown cleanly.

### Task Queue
- Lightweight in-memory FIFO queue.
- Supports enqueuing named tasks and retrieving them in order.
- Includes internal invariants checked by `validate()`.

### Agent Registry
- Simple registry for agent definitions.
- Enables lookup of agents by name.
- Ensures no duplicate registration.

### Memory Store
- In-memory key/value store with simple CRUD semantics.
- Supports namespaced keys / isolation.
- Provides `validate()` to ensure basic operations succeed.

### Observability
- Minimal helper for emitting structured metrics and events.
- Designed to be easy to replace with a richer telemetry backend in the future.

## CI & validation strategy

- Use `pre-commit` as the single source of truth for linting, type checking, and core smoke tests.
- The `ci.yml` workflow is minimal and primarily validates that the repository installs and that core tests run.
- Maintain a small suite of `tests/test_core_*.py` tests that focus only on core invariants.

## Open questions / future enhancements

- Should we introduce a pluggable backend for `TaskQueue` (e.g., Redis)?
- How will the core runtime integrate with the eventual API layer (e.g., FastAPI websocket-driven orchestrator)?
- Should we provide a stable extension point for runtime metrics and tracing?
