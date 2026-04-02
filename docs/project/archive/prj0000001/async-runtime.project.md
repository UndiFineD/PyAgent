# async-runtime

**Project ID:** `prj0000001`

## Links

- Plan: `plan.md`
- Design: `brainstorm.md`

## Tasks

- [x] Define and document the public runtime API surface.
- [x] Implement Rust extension crate at `rust_core/runtime` exposing `spawn_task`, `set_timeout`, and `create_queue`.
- [x] Add a pure-Python fallback wrapper in `src/runtime_py/__init__.py` for environments without the Rust extension.
- [x] Ensure runtime tasks can be scheduled from both synchronous and async contexts without leaking coroutines.
- [x] Create unit tests verifying:
- [x] Migrate `observability.stats.metrics_engine` and `legacy_engine` to use the runtime API.
- [x] Implement useful helper primitives in `src/runtime_py` (event bus, file watcher, HTTP server).
- [x] Add documentation and examples for consuming the runtime API.
- [x] Keep CI green across platforms (Windows/Linux/Mac) by making runtime behavior deterministic.

## Status

9 of 9 tasks completed

## Code detection

- Code detected in:
  - `rust_core\src\async_runtime.rs`
  - `rust_core\src\async_transport.rs`
  - `scripts\prepend_async_note.py`
  - `src\agents\specialization\runtime_feature_flags.py`
  - `src\core\runtime.py`
  - `tests\runtime\test_runtime_import.py`
  - `tests\test_async_loops.py`
  - `tests\test_async_transport.py`
  - `tests\test_core_runtime.py`
  - `tests\test_flm_runtime_errors.py`
  - `tests\test_runtime.py`