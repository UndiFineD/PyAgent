# Prj001 Async Runtime Brainstorm

## Design goals

- **Unified runtime API**: expose a consistent `runtime.*` surface regardless of whether the Rust extension is present.
- **Safe default for CI/local dev**: tests must not depend on building the Rust extension; the Python fallback should behave equivalently.
- **Minimal external dependencies**: avoid heavy native stacks (e.g. avoid hyper in Rust for the bundled HTTP server).
- **Deterministic scheduling**: ensure `spawn_task` works from both inside an active asyncio loop and from plain synchronous code.

## Approach

### Rust runtime (preferred path)
- Use Tokio runtime as a global singleton via `once_cell::sync::Lazy`.
- Expose `spawn_task` via `pyo3` so Python coroutines become asyncio tasks (via `create_task`).
- Provide `set_timeout(ms, callback)` using Tokio `sleep` + `call_soon_threadsafe`.
- Provide `create_queue()` using `tokio::sync::mpsc` or via Python `asyncio.Queue` to keep the binding simple.

### Python fallback (when Rust extension missing)
- Provide `src/runtime_py/__init__.py` that uses `asyncio` and a background event loop thread to guarantee `spawn()` works.
- Implement `sleep(ms)` via `asyncio.get_event_loop().call_later`.
- Ensure no “coroutine never awaited” warnings by always scheduling tasks or closing coroutines.

## Notes / Risks

- Python event loop vs Tokio: mixing isn't safe; we intentionally keep the runtime API in Python so it can schedule on Python's own loop, while Rust runtime provides a standalone executor for Rust tasks.
- `spawn_task` should never block the caller; it must be fire-and-forget.
- Windows file watching is flaky in Rust, which is why `watch_file()` is kept in Python.
