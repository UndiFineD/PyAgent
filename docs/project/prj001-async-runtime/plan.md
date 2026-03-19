# Prj001 Async Runtime

## Goal

Provide a stable, cross-platform async runtime foundation for PyAgent by:

- Exposing a minimal `runtime` Python API backed by a Tokio runtime (Rust) when available.
- Falling back to a pure-Python asyncio implementation when the Rust extension is not installed.
- Ensuring runtime primitives (`spawn_task`, `set_timeout`, `create_queue`, `sleep`) behave predictably in both CI and local dev.

This runtime is used by core tooling (e.g. `runtime_py.spawn`, `watch_file`, `run_http_server`) and by higher-level agents that require background scheduling.

## Tasks

- [x] Define and document the public runtime API surface.
- [x] Implement Rust extension crate at `rust_core/runtime` exposing `spawn_task`, `set_timeout`, and `create_queue`.
- [x] Add a pure-Python fallback wrapper in `src/runtime_py/__init__.py` for environments without the Rust extension.
- [x] Ensure runtime tasks can be scheduled from both synchronous and async contexts without leaking coroutines.
- [x] Create unit tests verifying:
  - The Rust extension is a singleton.
  - `spawn_task` executes coroutines on the active event loop.
  - `set_timeout` triggers callbacks after a delay.
  - `create_queue` returns an asyncio queue + put coroutine.
- [x] Migrate `observability.stats.metrics_engine` and `legacy_engine` to use the runtime API.
- [x] Implement useful helper primitives in `src/runtime_py` (event bus, file watcher, HTTP server).
- [x] Add documentation and examples for consuming the runtime API.
- [x] Keep CI green across platforms (Windows/Linux/Mac) by making runtime behavior deterministic.
