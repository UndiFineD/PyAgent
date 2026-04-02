# Async Runtime Update
> **2026-03-10:** Project migrated to Node.js-like asynchronous runtime; synchronous loops are prohibited by automated tests.

# Async Runtime / Event Loop Design

This document outlines the proposed Node.js–style runtime for PyAgent.  The
goal is a **single high‑performance loop implemented in Rust** with a thin
Python façade, enabling every subsystem to be written as asynchronous,
event‑driven code.  Python loops are strictly forbidden by the `tests/test_async_loops.py`
check, so anything that would iterate must be migrated or exported to Rust.

## Workspace Layout

```
rust_core/                  # existing top‑level Rust workspace
└── runtime/                # new crate containing the event loop
    ├── Cargo.toml
    └── src/lib.rs          # FFI bindings via pyo3

src/runtime/__init__.py     # Python wrapper around the Rust module
```

The `rust_core` workspace already holds crates such as `metrics`.  The `runtime`
crate will depend on `tokio` and `pyo3` and publish a Python extension module
named `runtime`.

## Rust API Surface (bindings)

- `spawn_task(py_coro: PyObject) -> PyResult<()>` – schedule a Python
  coroutine.  Internally wraps it in `tokio::spawn` and logs any exceptions
  back to the Python logger.
- `set_timeout(ms: u64, callback: PyObject) -> PyResult<()>` – call a Python
  function after a delay.
- `watch_file(path: String) -> PyResult<()>` – emit events when files change.
- `run_http_server(addr: String, handler: PyObject) -> PyResult<()>` – start a
  hyper-based web server invoking the Python handler.
- `create_queue() -> PyResult<(Sender, Receiver)>` – async channel pairs.
- `logger` – a reference to the central Python logger object for use from
  Rust code.

Each function is exposed with `#[pymodule]` and appropriate `#[pyfunction]`
wrappers.  The runtime owns a global `tokio::Runtime` launched via
`once_cell::sync::Lazy`.

## Python Wrapper API

In `src/runtime/__init__.py` we provide ergonomic helpers:

```python
from ._runtime import spawn_task, set_timeout, create_queue, logger

async def spawn(coro):
    """Schedule `coro` and log any uncaught exception."""
    async def wrapper():
        try:
            await coro
        except Exception:
            logger.exception("runtime task failed")
    spawn_task(wrapper())

async def sleep(ms):
    await set_timeout(ms, lambda: None)

# event bus built on top of channels
_event_subscribers: dict[str, list] = {}

def on(event, handler):
    _event_subscribers.setdefault(event, []).append(handler)

def emit(event, *args, **kwargs):
    for h in _event_subscribers.get(event, []):
        spawn(h(*args, **kwargs))
```

## Queue / Channel Abstractions

The runtime provides bounded/unbounded async queues via `create_queue()`.  Any
subsystem (metrics, verification, plugins, swarm manager) can obtain a pair
and use it to send events across the loop without writing loops in Python.

## Logging & Error Handling

`spawn()` wraps tasks and the Rust bindings themselves capture panics/errors
then call back into the shared `logger` object.  Plugins that register hooks
can also emit `runtime.emit("task.error", exc)` for higher‑level handling.

## Migration Strategy

1. **Enable `tests/test_async_loops.py`** in CI.  It will fail on any remaining
   synchronous loops.
2. **Port one core module** as proof of concept: e.g. `metrics_engine.py`.
   Replace loops with `await runtime.sleep(...)` or `runtime.subscribe("tick", ...)
   `. Add corresponding tests to drive the refactor.
3. **Iterate**: next migrate verification, file watcher, subprocess manager,
   http adapter, etc.  Each port will leverage channels or events from the
   Rust runtime.
4. **Write new modules** directly against the runtime API going forward
   — no loops required.

## Event Bus & Interceptors

Plugins may register to named events (`on(event, handler)`) or register
interceptors that wrap core operations (e.g. `runtime.intercept("deploy", my_hook)`).
The runtime will dispatch events on every significant action (file change,
agent spawn, metrics tick, HTTP request) which enables extensibility without
modifying core code.

## Performance Considerations

- All CPU‑heavy loops reside in Rust, eliminating Python GIL contention.
- Tokio’s scheduler handles millions of concurrent tasks with low latency.
- Channels and file watchers are zero‑copy whenever possible.

This design positions PyAgent for a future where the Python layer is purely
orchestration and business logic, while the Rust runtime ensures responsive
and scalable execution.  The `test_async_loops.py` rule enforces gradual
compliance by making every async refactor a failing test until corrected.


## Implementation Roadmap

To turn this design into working code, we follow an incremental roadmap that
prioritizes early feedback and preserves backward compatibility where possible.

1. **Crate bootstrap** – create `rust_core/runtime` with `Cargo.toml`;
   implement FFI stubs returning `NotImplementedError` so the Python package
   builds.  Add CI job that compiles the Rust workspace and runs a basic smoke
   test (`import runtime`).
2. **Global runtime** – add `tokio::Runtime` singleton and the Python
   wrapper that initializes it when the module is imported.  Write unit tests
   in Rust for startup/shutdown semantics and ensure Python import triggers
   initialization exactly once.
3. **Core bindings** – implement `spawn_task`, `set_timeout`, and
   channel creation.  Write comprehensive integration tests exercising each
   API from Python (using `pytest` with `asyncio`).  Confirm that
   `tests/test_async_loops.py` succeeds when tasks are scheduled via `runtime`
   and fails otherwise.
4. **Event bus & helpers** – implement Python `spawn()` helper and the
   `on`/`emit` infrastructure.  Add tests showing multiple handlers receiving
   events concurrently, error propagation, and interceptor support.
5. **Auxiliary services** – add `watch_file`, `run_http_server`, and optional
   `logger` hooking.  Each service should have its own Rust module with
   minimal Python integration tests (e.g. modify a temporary file and await an
   event; start a server on localhost and verify a handler call).
6. **Subsystem migration** – sequentially port existing modules to the new
   runtime using channels/events.  Track progress in a migration tracker file
   (`MIGRATION.md`).  Ensure each port has a corresponding test demonstrating
   loop removal and correct behavior under the runtime.
7. **Documentation & onboarding** – update developer docs with
   `runtime_design.md`, migration guidelines, and examples showing how to
   write new async subsystems with `runtime.spawn`/`on`.
8. **Performance validation** – add benchmarks comparing old Python loops to
   the Rust runtime for representative workloads (metrics ticks, file
   watching, HTTP requests).  Capture results in `performance/` folder.

### Milestones

| Milestone | Criteria |
|-----------|----------|
| Bootstrap complete | `rust_core/runtime` builds on CI and Python wrapper imports. |
| Core API available | `spawn_task`, `set_timeout`, and channels work from Python. |
| Event bus live | `on` and `emit` support multiple subscribers and interceptors. |
| First subsystem ported | `metrics_engine.py` uses runtime and passes tests. |
| All loops eliminated | `tests/test_async_loops.py` passes across the repo. |

### Testing Strategy

- **Unit tests** in Rust for individual bindings and runtime invariants.
- **Integration tests** in Python located under `tests/runtime/` verifying end‑to‑end
  behavior (task scheduling, timeouts, event dispatch).
- **Migration regression suite**: every ported module adds tests to ensure
  parity with previous synchronous behaviour.
- **CI enforcement**: `tests/test_async_loops.py` guarded by a pytest marker
  that fails if any synchronous loops remain; running the full suite before
  and after each migration ensures compliance.

### Risks & Mitigations

- **GIL contention**: heavy Python loops might degrade performance.  Mitigate
  by moving CPU‑bound tasks entirely into Rust or using `tokio::task::spawn_blocking`.
- **FFI stability**: incorrect reference counting could leak or crash.  use
  `pyo3` safe wrappers and add `miri`/`ASAN` checks in Rust CI.
- **Migration scope creep**: porting every module might be large.  keep the
  migration tracker visible and break tasks into bite‑sized PRs with
  independent test coverage.
- **Cross‑platform build**: ensure Rust extension compiles on Windows, macOS,
  Linux by testing via GitHub Actions matrix.

*See `core_design.md`, `swarm_design.md`, and other brainstorm documents for
related architectural context.*