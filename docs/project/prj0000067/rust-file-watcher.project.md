# rust-file-watcher — Project Overview

_Owner: @1project | Status: In Sprint_

**Goal:** Provide a Rust-powered filesystem watcher exposed to Python, using `walkdir` for polling-based change detection and `notify` for event-based watching, integrated into `rust_core`.

**In scope:**
- `rust_core/src/watcher.rs` — Rust `scan_changed_files(root, since_ms)` function + `register()`
- `rust_core/src/lib.rs` — register `watcher` module
- `rust_core/Cargo.toml` — add `notify = "6"` dependency
- `src/tools/FileWatcher.py` — Python wrapper with graceful fallback if rust_core not compiled
- `tests/test_file_watcher.py` — Python tests (no Rust compilation required)
- `docs/project/prj0000067/` — 9 artifacts
- `data/projects.json` + `docs/project/kanban.md` — lane transitions

**Out of scope:** Hot-reload triggering, project-wide live server, WebSocket push of change events.

## Branch Plan

**Expected branch:** `prj0000067-rust-file-watcher`

**Scope boundary:** Only the files listed above may be modified on this branch.

**Handoff rule:** `@9git` must confirm `OBSERVED_BRANCH == prj0000067-rust-file-watcher` before staging.

**Failure rule:** If tests fail or branch mismatch is detected, stop and notify `@0master`.


## Legacy Project Overview Exception

This project overview predates the modern Project Identity / Goal and Scope / Branch Plan
template. It was authored with an earlier workflow format and has not been migrated.
The project was completed successfully; the deviation is a documentation formatting issue only.

Migration to the modern template is on record with @0master.
