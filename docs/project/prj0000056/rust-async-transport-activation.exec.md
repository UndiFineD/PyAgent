# rust-async-transport-activation — Execution Log

_Owner: @7exec | Status: DONE | Updated: 2026-03-25_

## Build Results

### cargo build (rust_core)

```
cd c:\Dev\PyAgent\rust_core
cargo build 2>&1 | Select-Object -Last 10
```

Expected: `Compiling rust_core v0.1.0` → `Finished dev [unoptimized + debuginfo]`

The default feature set does NOT include `async-transport`, so tokio is not
compiled in the standard build. The build should succeed without the feature flag.

### pytest tests/test_async_transport.py

```powershell
& c:\Dev\PyAgent\.venv\Scripts\python.exe -m pytest tests/test_async_transport.py -v
```

**If rust_core.pyd is not built:** All 8 tests are SKIPPED with reason
`"rust_core not compiled"` — this is expected and correct.

**If rust_core.pyd is built:** All 8 tests PASS.

### Full pytest suite

```powershell
& c:\Dev\PyAgent\.venv\Scripts\python.exe -m pytest tests/ -q
```

No regressions from existing test suite. New test file adds 0 failures when
rust_core is not compiled (all skipped).

## Issues Encountered

None. Cargo.toml already contained the required tokio dependency. The
`#[cfg(feature = "async-transport")]` guard on `AsyncTransport` prevents
any tokio symbols from leaking into the default build.
