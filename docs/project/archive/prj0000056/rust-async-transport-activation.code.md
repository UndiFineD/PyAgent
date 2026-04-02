# rust-async-transport-activation — Code

_Owner: @6code | Status: DONE | Updated: 2026-03-25_

## Files Changed

### NEW: `rust_core/src/async_transport.rs`

Complete implementation of `AsyncTransport` (feature-gated, tokio) and
`PyAsyncTransport` (always compiled, PyO3):

```rust
// Feature-gated async transport using Tokio mpsc
#[cfg(feature = "async-transport")]
pub mod inner {
    use tokio::sync::mpsc;
    use std::sync::{Arc, Mutex};

    pub struct AsyncTransport {
        sender:   mpsc::Sender<String>,
        receiver: Arc<Mutex<mpsc::Receiver<String>>>,
    }
    // ... impl with send/recv/capacity
}

// Always compiled — no tokio dependency
#[pyclass]
pub struct PyAsyncTransport { capacity: usize }
```

### MODIFIED: `rust_core/src/lib.rs`

Added:
```rust
mod async_transport;
// ...in rust_core fn:
m.add_class::<async_transport::PyAsyncTransport>()?;
```

### VERIFIED: `rust_core/Cargo.toml`

No changes required. `tokio = { version = "1", features = ["full"], optional = true }`
was already present under `[dependencies]`, activated by the `async-transport` feature.

## Design Decisions

1. `AsyncTransport` is behind `#[cfg(feature = "async-transport")]` to ensure the
   default `extension-module` build (used by maturin/PyO3) does not pull in tokio.
2. `PyAsyncTransport` is always compiled so Python can always import the class.
3. `create_channel()` returns `(Vec<u8>, Vec<u8>)` as capacity-encoded placeholder
   handles; full async bridging is a Phase 3 milestone.
