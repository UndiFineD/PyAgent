# rust-file-watcher — Plan

_Owner: @4plan_

## Tasks

1. Create `rust_core/src/watcher.rs`
   - `scan_changed_files(root: &str, since_ms: u64) -> PyResult<String>`
   - Uses `walkdir::WalkDir` to iterate; checks `metadata().modified()`
   - Returns JSON array of changed paths (relative to root)
   - `pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()>`

2. Update `rust_core/src/lib.rs`  
   - Add `mod watcher;` declaration
   - Add `watcher::register(m)?;` in `rust_core()` fn

3. Update `rust_core/Cargo.toml`
   - Add `notify = { version = "6", optional = true }` (optional for future)

4. Create `src/tools/FileWatcher.py`
   - `FileWatcher(root, interval_s=1.0)`
   - `async start() / stop() / get_changes()`
   - Rust import with Python fallback

5. Create `tests/test_file_watcher.py`
   - Test start/stop lifecycle
   - Test change detection with mocked scan
   - Test Python fallback path
   - Test get_changes clears pending set

## Acceptance criteria

- [ ] `FileWatcher` starts, polls, and returns changed files
- [ ] Falls back gracefully when rust_core not compiled
- [ ] All 5 tests pass
