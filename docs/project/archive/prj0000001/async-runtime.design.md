# async-runtime - Design

_Status: DONE_
_Designer: @3design | Updated: 2026-03-20_

## Selected Option
Rust-first runtime integration with a Python fallback contract to preserve behavior across all environments.

## Architecture
Expose one runtime API surface consumed by agent code while implementation is selected at runtime:
- Native extension path when Rust bindings are available.
- Asyncio fallback path when native bindings are unavailable.

## Interfaces & Contracts
The runtime surface must keep stable semantics for:
- Task spawn (`spawn_task`): fire-and-forget scheduling from sync or async call sites.
- Delayed callbacks (`set_timeout`): callback execution after a bounded delay.
- Queue creation (`create_queue`): predictable producer/consumer behavior.
- Sleep/timer primitives: deterministic behavior in CI and local development.

## Compatibility Guarantees
- Callers use one API surface regardless of backend implementation.
- Backend selection must not leak into higher-level agent orchestration logic.
- Fallback behavior must avoid coroutine leaks and loop ownership confusion.

## Non-Functional Requirements
- Performance: Keep low scheduling overhead and deterministic behavior in CI.
- Security: Avoid unsafe cross-thread callback patterns and keep callback execution on managed loop context.
- Operability: Keep runtime behavior diagnosable through focused tests and artifact logs.

## Open Questions
Define explicit compatibility tests for edge-case timer, cancellation, and queue backpressure semantics.
