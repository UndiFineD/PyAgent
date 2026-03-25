# api-versioning — Plan

_Owner: @4plan_

## Tasks

1. Add `VersionHeaderMiddleware` (BaseHTTPMiddleware) to `backend/app.py`:
   - Injects `X-API-Version: 1` on `/api/v1/` responses
   - Injects `Deprecation: true` + `Link` on bare `/api/` responses

2. Mount `_auth_router` under `/api/v1/` prefix as well as existing `/api/` prefix:
   - Create `_v1_router = APIRouter(prefix="/api/v1", ...)` and assign same routes
   - OR simpler: `app.include_router(_auth_router, prefix="/api/v1")` to avoid duplication

3. Create `tests/test_api_versioning.py`:
   - `GET /api/v1/metrics/system` returns 200
   - `GET /api/v1/agent-log/0master` returns 200
   - `GET /api/v1/agent-memory/test-agent` returns 200
   - `GET /api/v1/projects` returns 200
   - versioned endpoint has `X-API-Version: 1` header
   - unversioned endpoint has `Deprecation: true` header

## Acceptance criteria

- [ ] `GET /api/v1/agent-log/0master` returns 200
- [ ] `X-API-Version: 1` header on `/api/v1/` responses
- [ ] `Deprecation: true` header on bare `/api/` responses
- [ ] All existing tests still pass (no regressions)

## Validation

```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
pytest tests/test_api_versioning.py -v
pytest tests/test_backend_worker.py -v
```
