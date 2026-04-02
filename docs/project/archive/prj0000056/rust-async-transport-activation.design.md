# rust-async-transport-activation — Design

_Owner: @3design | Status: DONE | Updated: 2026-03-25_

## Architecture

```
Python (pytest / agent code)
        │  import rust_core
        │  t = rust_core.PyAsyncTransport(capacity=64)
        │  t.get_capacity()  → 64
        │  t.create_channel()  → ([64], [64])
        ▼
PyO3 layer  (rust_core/src/async_transport.rs)
        │  PyAsyncTransport { capacity: usize }
        │  Always compiled — no tokio dependency
        │
        ├── [cfg(feature = "async-transport")]
        │         AsyncTransport { sender, receiver }
        │         Uses tokio::sync::mpsc
        │
        └── Cargo.toml: tokio optional, async-transport feature
```

## Module Design

### `AsyncTransport` (feature-gated)

```rust
#[cfg(feature = "async-transport")]
pub struct AsyncTransport {
    sender:   mpsc::Sender<String>,
    receiver: Arc<Mutex<mpsc::Receiver<String>>>,
}
```

| Method | Signature | Notes |
|---|---|---|
| `new` | `fn new(capacity: usize) -> Self` | Creates bounded channel |
| `send` | `async fn send(&self, msg: String) -> Result<(), String>` | Backpressure: awaits slot |
| `recv` | `async fn recv(&self) -> Option<String>` | Returns `None` on close |
| `capacity` | `fn capacity(&self) -> usize` | Live available capacity |

### `PyAsyncTransport` (always compiled)

```rust
#[pyclass]
pub struct PyAsyncTransport { capacity: usize }
```

| Method | Signature | Notes |
|---|---|---|
| `new` | `#[new] fn new(capacity: usize) -> Self` | Constructor |
| `get_capacity` | `fn get_capacity(&self) -> usize` | Returns stored capacity |
| `create_channel` | `fn create_channel(&self) -> (Vec<u8>, Vec<u8>)` | Placeholder handles |

## Integration Points

- `rust_core/src/lib.rs`: `mod async_transport;` + `m.add_class::<PyAsyncTransport>()?;`
- `Cargo.toml`: no changes required; tokio is already present as optional
- Python tests skip if `rust_core` not compiled (import guard)

## Security Notes

- No use of unsafe code
- Mutex lock is brief (immediate recv call only)
- No network exposure in this module
