# rust-async-transport-activation — Test

_Owner: @5test | Status: DONE | Updated: 2026-03-25_

## Test Strategy

Tests are located in `tests/test_async_transport.py`. They use a forward-compatible
skip guard so they pass (all skipped) in CI environments where `rust_core` is not
compiled, and run fully when the `.pyd`/`.so` is present.

## Test Cases

| # | Test name | What it tests | Expected outcome |
|---|---|---|---|
| 1 | `test_module_importable` | `import rust_core` succeeds | Pass (or skip) |
| 2 | `test_pyasynctransport_instantiation` | `PyAsyncTransport(64)` constructs | Instance created |
| 3 | `test_get_capacity_small` | capacity=4 → `get_capacity()` returns 4 | Returns 4 |
| 4 | `test_get_capacity_large` | capacity=1024 → `get_capacity()` returns 1024 | Returns 1024 |
| 5 | `test_create_channel_returns_tuple` | `create_channel()` returns 2-element tuple | len(result) == 2 |
| 6 | `test_create_channel_send_handle` | first element encodes capacity | result[0][0] == capacity |
| 7 | `test_create_channel_recv_handle` | second element encodes capacity | result[1][0] == capacity |
| 8 | `test_zero_capacity` | capacity=0 — no panic | Returns 0 |

## Coverage Goals

- `PyAsyncTransport.__init__`, `get_capacity`, `create_channel` — 100%
- No tokio runtime required at Python test time
- Skip path verified: `HAS_RUST = False` causes all tests to be skipped with
  message "rust_core not compiled"

## Execution

```powershell
& c:\Dev\PyAgent\.venv\Scripts\python.exe -m pytest tests/test_async_transport.py -v
```
