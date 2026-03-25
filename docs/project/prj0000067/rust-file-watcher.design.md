# rust-file-watcher — Design

_Owner: @3design_

## Rust interface (`rust_core/src/watcher.rs`)

```rust
/// Scan `root` for files modified after `since_ms` (Unix epoch ms).
/// Returns a JSON string: ["path1", "path2", ...]
#[pyfunction]
fn scan_changed_files(root: &str, since_ms: u64) -> PyResult<String>
```

## Python interface (`src/tools/FileWatcher.py`)

```python
class FileWatcher:
    def __init__(self, root: str, interval_s: float = 1.0)
    async def start(self) -> None        # begin polling loop
    async def stop(self) -> None         # cancel polling loop
    async def get_changes(self) -> list[str]   # return accumulated changed files
```

Internals:
- Tries to `import rust_core; rust_core.scan_changed_files(root, since_ms)` 
- Falls back to `os.scandir` polling if rust_core unavailable
- Change set is a `set[str]` accumulated since last `get_changes()` call (which clears it)
- Background `asyncio.Task` polls every `interval_s` seconds

## Data flow

```
asyncio.Task (poll every N seconds)
  → scan_changed_files(root, last_check_ms)  [Rust or Python fallback]
  → _pending_changes.update(new_files)
  → last_check_ms = now_ms
```
