# rust-async-transport-activation — Think

_Owner: @2think | Status: DONE | Updated: 2026-03-25_

## Problem Statement

`rust_core` already lists `tokio = { version = "1", features = ["full"] }` as an
optional dependency (activated by the `async-transport` feature flag). However, no
actual async transport code exists in `rust_core/src/`. Inter-agent messaging is
currently done entirely in Python, which limits throughput and backpressure control.

## Options Considered

### Option A — Tokio mpsc channel (SELECTED)
Use `tokio::sync::mpsc` for bounded async queues. Pros: first-class backpressure,
well-tested, matches existing tokio dep. Cons: async Rust runtime must be available
at call site.

### Option B — Crossbeam channels
Synchronous multi-producer single-consumer channels. Pros: no async overhead.
Cons: no async await support, not compatible with the planned async Python bridge.

### Option C — Flume (tokio-compatible)
Third-party crate with async/sync dual interface. Pros: ergonomic. Cons: adds
a new dependency for functionality already available in tokio.

## Decision

Option A. Tokio mpsc channels are the correct primitive: they are already depended
upon by the `async-transport` feature, support backpressure via bounded capacity,
and integrate directly with the planned QUIC overlay.

## Key Risks

| Risk | Mitigation |
|---|---|
| `Mutex<Receiver>` contention | Single-consumer design — one receiver per channel |
| Python bridge complexity | PyO3 wrapper uses sync facade with capacity stub only |
| Feature-flag confusion | Strict `#[cfg(feature = "async-transport")]` guards |
| Build failures without feature | PyO3 class does not import tokio |

## Conclusion

Add `async_transport.rs` with `AsyncTransport` (feature-gated) and `PyAsyncTransport`
(always compiled). Register `PyAsyncTransport` in the PyO3 module. Write 5 Python
tests round-tripping capacity and instantiation.
