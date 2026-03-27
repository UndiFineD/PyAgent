# rust-async-transport-activation — Project Overview

_Status: DONE_
_Owner: @1project | Updated: 2026-03-25_

## Project Identity

**Project ID:** prj0000056
**Short name:** rust-async-transport-activation
**Project folder:** `docs/project/prj0000056/`
**Branch:** `prj0000056-rust-async-transport-activation`
**Date:** 2026-03-25

## Project Overview

Add an async message transport module to `rust_core` using Tokio `mpsc` channels,
expose it via PyO3 to Python, enabling async inter-agent message passing with
backpressure support.

The `rust_core` Cargo.toml already lists `tokio = { version = "1", features = ["full"],
optional = true }` under the `async-transport` feature. This project activates that
dormant feature by:

1. Implementing `AsyncTransport` in `rust_core/src/async_transport.rs` (feature-gated).
2. Adding a `PyAsyncTransport` PyO3 class (always compiled, no tokio dependency).
3. Registering `PyAsyncTransport` in `rust_core/src/lib.rs`.
4. Writing 9 Python tests in `tests/test_async_transport.py`.

## Goal & Scope

**Goal:** Wire Tokio async MPSC channels in `rust_core` and expose via PyO3,
enabling async inter-agent message passing with backpressure support.

**In scope:**
- `rust_core/src/async_transport.rs` — NEW: `AsyncTransport` + `PyAsyncTransport`
- `rust_core/src/lib.rs` — MODIFY: `mod async_transport` + register class
- `rust_core/Cargo.toml` — VERIFY (no changes required; tokio already present)
- `tests/test_async_transport.py` — NEW: 9 Python tests for PyO3 bindings
- `docs/project/prj0000056/` — NEW: 9 artifact files
- `data/projects.json` — UPDATE: lane, branch, pr fields for prj0000056
- `docs/project/kanban.md` — UPDATE: move prj0000056 from Ideas → Review

**Out of scope:**
- Full tokio runtime bridging to Python (Phase 3 milestone)
- Changes to existing `rust_core` transport module
- QUIC overlay activation (remains gated)
- Any other Rust or Python modules

## Branch Plan

**Expected branch:** `prj0000056-rust-async-transport-activation`
**Scope boundary:**
  - `rust_core/src/async_transport.rs` — new module
  - `rust_core/src/lib.rs` — mod declaration + register call only
  - `tests/test_async_transport.py` — new test file
  - `docs/project/prj0000056/` — all project artifacts
  - `data/projects.json` — prj0000056 entry only
  - `docs/project/kanban.md` — prj0000056 lane transition only
**Handoff rule:** Tests pass, PR open → ready for review.
**Failure rule:** Rust compilation error? Check that `tokio` is optional in
`Cargo.toml` and `async_transport.rs` uses `#[cfg(feature = "async-transport")]`.
Do not push broken code.



## Milestones
Legacy milestone details are not specified in this historical document.


## Status
Legacy status details are not specified in this historical document.

