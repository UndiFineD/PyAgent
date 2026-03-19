# async-runtime

**Project ID:** `prj001-async-runtime`

## Links

- Plan: `plan.md`
- Design: `brainstorm.md`

## Tasks

- [x] **Installable runtime extension**: Implement `rust_core/runtime` Rust crate with `pyo3` bindings and a global Tokio runtime singleton.
- [x] **Python runtime facade**: Implement `src/runtime_py/__init__.py` as a fallback when the Rust extension is absent.
- [x] **Runtime primitives**: Provide `spawn_task`, `set_timeout`, `create_queue`, and `sleep(ms)` consistently across both runtime implementations.
- [x] **Async helpers**: Provide convenience helpers (`spawn`, `on`, `emit`, `watch_file`, `run_http_server`) that use the runtime primitives.
- [x] **Unit tests**: Add/maintain tests verifying runtime behavior, scheduling, and correct coroutine handling.
- [x] **Lint compliance**: Remove all synchronous loops from runtime-related modules and ensure `tests/test_async_loops.py` passes.
- [x] **Documentation**: Add usage examples for the runtime API and note the fallback behavior.

## Status

✅ Fully implemented — the runtime API and helpers are working, and the full test suite passes on Windows.

## Code detection

- Code detected in:
  - `rust_core/runtime/src/lib.rs`
  - `src/runtime_py/__init__.py`
  - `src/observability/stats/*`
  - `tests/runtime/*`

## Status

11 of 11 tasks completed

## Code detection

- Code detected in:
  - `src\core\runtime.py`