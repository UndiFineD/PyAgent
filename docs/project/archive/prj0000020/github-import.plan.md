# github-import — Design / Plan / Test / Code / Exec / QL / Git

_Consolidated artifact for prj0000020._

## Design

### `github_app.py`
- Dispatch table: `_HANDLERS = {"push": _handle_push, "pull_request": ..., "issues": ...}`
- Each handler extracts structured fields from the payload and returns a typed dict.
- `X-GitHub-Event` header drives dispatch.
- `GET /health` → `{"status": "ok"}`.

### `downloader.py`
- `clone_repo(repo_url, dest, *, depth=1)` → `int` (exit code)
- Uses `shutil.which("git")` to locate binary; raises `FileNotFoundError` if absent.
- `download_repo()` kept as backward-compat shim, now writes a real README.

## Plan
| # | Task | Done |
|---|------|------|
| 1 | Event routing + health endpoint in `github_app.py` | ✅ |
| 2 | `clone_repo()` in `downloader.py` | ✅ |
| 3 | Copyright headers on `config.py` | ✅ |
| 4 | Expand `test_github_app.py` to 7 events | ✅ |
| 5 | Fix `test_importer_flow.py` size assertion | ✅ |
| 6 | Write 9 doc artifacts | ✅ |

## Test Results
`9 passed` ✅

## Code Notes
- All event handlers use `payload.get(...)` safely — no KeyError on partial payloads.
- No `shell=True` in `clone_repo`.
- `TestClient` from `fastapi.testclient` used for all HTTP tests.

## Exec
```powershell
& C:\Dev\PyAgent\.venv\Scripts\python.exe -m pytest tests/test_github_app.py tests/test_importer_flow.py tests/test_importer_config.py -v
# 9 passed ✅
```

## Security (QL)
| Check | Result |
|-------|--------|
| Webhook signature (HMAC) | NOT implemented — deferred. Mark as future work. |
| Path traversal in `clone_repo` dest | Caller-supplied; internal use only |
| No `shell=True` in `clone_repo` | ✅ |
| JSON payload from untrusted source | Parsed by FastAPI/Pydantic; content not executed |

**NOTE**: In production, GitHub webhook payloads should be verified using the `X-Hub-Signature-256` HMAC header to prevent spoofed events. This is a known gap.

## Git
**Expected branch:** `prj0000020-github-import`
**Observed branch:** `prj0000020-github-import` ✅
