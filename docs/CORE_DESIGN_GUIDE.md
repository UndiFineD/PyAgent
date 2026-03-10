# CORE_DESIGN_GUIDE

This guide explains how you design and extend the `src/core` subsystem in PyAgent.

## Purpose

You use `src/core` for reusable, low-level building blocks that multiple agents or services depend on.
Core code should remain:

- small and composable,
- import-safe,
- easy to test,
- independent from specific model/provider behavior.

## Core Design Rules

### 1) Composition over monoliths

Prefer small, focused components over large all-in-one classes.
If behavior can be split into independent concerns, place those concerns in separate modules.

### 2) Stable, typed APIs

Each core module should expose a clear typed API.
Use type hints consistently for inputs, outputs, and public attributes.

### 3) Lightweight validation hooks

Each core module must expose `validate()`.
`validate()` should be fast, deterministic, and side-effect light so it is safe in CI.

### 4) Async-safe runtime behavior

Do not block the event loop from core runtime code.
Use async primitives and explicit timeouts/cancellation paths where needed.

### 5) Transaction-safe state operations

State mutations should use transaction-aware patterns where available, so failures can be rolled back
predictably.

### 6) Observability by default

Core paths should emit structured logs/metrics for key operations, including failures and duration.

## Suggested File Pattern

For a new core module, use this minimum layout:

- `src/core/<module>.py`
- `tests/test_core_<module>.py`

Inside the module:

- main class or functions,
- typed public API,
- `validate()` function.

Inside the test file:

- behavior tests,
- edge-case tests,
- `validate()` smoke test.

## Dependency Boundaries

- Core modules should avoid importing high-level orchestration code.
- Keep provider-specific logic in provider modules, not generic core primitives.
- Avoid circular dependencies across core modules.

## Performance and Rust Offload

When a core path becomes hot (high-frequency or CPU-heavy), keep Python API stable and move the heavy
compute path to `rust_core/` behind a thin boundary.

## Done Criteria for Core Changes

A core change is complete only when:

1. tests pass,
2. quality checks pass (ruff, mypy, pytest),
3. coverage remains at target,
4. new/changed module includes `validate()`.
