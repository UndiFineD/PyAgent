# async-runtime

**Project ID:** `prj001-async-runtime`

## Links

- Plan: `plan.md`
- Design: `brainstorm.md`

## Tasks

- [x] **Failing import test**: Add `tests/runtime/test_runtime_import.py` to assert the `runtime` module is missing initially and then confirm the stub exposes `spawn_task`, `set_timeout`, and `create_queue`.
- [x] **Crate bootstrap**: Create `rust_core/runtime` crate with `Cargo.toml` and `src/lib.rs`, exposing the basic Python bindings (raising `NotImplementedError`).
- [x] **Global runtime initialization**: Implement a global Tokio `Runtime` singleton in Rust using `once_cell::sync::Lazy`. Add Rust tests for singleton behavior.
- [x] **spawn_task binding**: Implement `spawn_task` using `pyo3_asyncio` to run Python coroutines on the Rust runtime, with exception logging.
- [x] **set_timeout & sleep helper**: Implement `set_timeout` in Rust (Tokio sleep) and expose a Python `sleep(ms)` helper.
- [x] **create_queue binding**: Implement `create_queue` in Rust using `tokio::sync::mpsc` and export sender/receiver wrappers to Python.
- [x] **Event bus helpers**: Provide Python helpers `spawn()`, `on()`, and `emit()` for event dispatch; confirm behavior in tests.
- [x] **File watcher**: Add `watch_file` functionality (implemented in Python using `asyncio`/polling after Rust bindings proved brittle).
- [x] **HTTP server binding**: Add `run_http_server` helper in Python using `asyncio` (instead of Rust hyper, to keep cross-platform stable).
- [x] **metrics_engine migration**: Port `src/observability/stats/metrics_engine.py` to use async runtime (`runtime.sleep` + `runtime.spawn`), ensuring `tests/test_async_loops.py` passes.
- [x] **Documentation & CI**: Update README with runtime examples; ensure CI builds Rust and runs full test suite across platforms.

## Status

11 of 11 tasks completed

## Code detection

- Code detected in:
  - `src\core\runtime.py`