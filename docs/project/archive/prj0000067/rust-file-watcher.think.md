# rust-file-watcher — Think

_Owner: @2think_

## Problem

PyAgent needs real-time change detection in the project directory for hot-reload triggers and incremental builds. Python's watchdog library is an option, but for a Rust-accelerated project, this belongs in `rust_core`.

## Constraints

- Budget M — can add one new Cargo dep (`notify`)
- Python tests must not require compiled Rust (graceful fallback)
- `walkdir` already in Cargo.toml (v2.4)

## Options

| Option | Pros | Cons |
|---|---|---|
| Python watchdog | Easy, battle-tested | Not Rust, separate pip dep |
| Pure polling via `walkdir` | Zero new deps, cross-platform | Polling latency (1s typical) |
| `notify` crate | Event-driven, near-instant | New Cargo dep, OS-specific backends |
| inotify FFI direct | Fast | Linux-only, complex |

## Selected approach

**Two-layer implementation:**

1. `rust_core/src/watcher.rs` — `scan_changed_files(root, since_ms)` using `walkdir` for polling; returns JSON list of changed file paths
2. `src/tools/FileWatcher.py` — async Python wrapper with graceful fallback if rust_core not compiled

The Rust source is included in the repo and will be compiled as part of a future `cargo build`. Python tests mock the Rust layer and test the Python wrapper independently.
