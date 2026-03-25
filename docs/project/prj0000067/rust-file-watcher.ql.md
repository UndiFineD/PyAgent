# rust-file-watcher — Security Review

_Owner: @8ql_

## OWASP / security checks

| Risk | Finding |
|------|---------|
| Path traversal | `root` in `FileWatcher.__init__` is resolved via `Path(root).resolve()` — symlinks followed but path is fully resolved |
| Arbitrary file read | `scan_changed_files` only returns file paths, not content — no data leakage |
| Rust unsafe blocks | None used in `watcher.rs` |
| Command injection | No subprocess calls |

## Status: PASS
