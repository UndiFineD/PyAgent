# backend-authentication — Implementation Plan

_Owner: @4plan | Status: DONE_

## Task Breakdown

### T1 — Check / add PyJWT dependency
Verify `PyJWT` is in `requirements.txt`. Add if missing.

### T2 — Create `backend/auth.py`
New module with:
- Module-level constants: `API_KEY`, `JWT_SECRET`, `JWT_ALGORITHM`, `DEV_MODE`
- Startup warning log when `DEV_MODE` is True
- `verify_api_key(expected, provided) -> bool`
- `verify_jwt(token) -> Optional[dict]`
- `require_auth(x_api_key, authorization) -> dict` (FastAPI dependency)
- `websocket_auth(websocket) -> Optional[dict]`

### T3 — Update `backend/app.py`
1. Add imports: `from fastapi import APIRouter, Depends` + `from .auth import require_auth, websocket_auth`
2. Create `auth_router = APIRouter(dependencies=[Depends(require_auth)])`
3. Re-register all protected endpoints on `auth_router` (metrics, agent-log, agent-doc, projects)
4. Keep `/health` on `app` directly
5. Add `websocket_auth` call inside `websocket_endpoint`, close 4401 if returned None
6. `app.include_router(auth_router)` after all route definitions

### T4 — Write tests in `tests/test_backend_auth.py`
New file, ≥ 10 test cases:
1. `test_verify_api_key_match` — correct key → True
2. `test_verify_api_key_wrong` — wrong key → False
3. `test_verify_api_key_none` — None provided → False
4. `test_verify_api_key_empty_expected` — empty expected → False
5. `test_verify_jwt_valid` — valid token → payload dict
6. `test_verify_jwt_expired` — expired token → None
7. `test_verify_jwt_bad` — garbage token → None
8. `test_rest_no_auth_returns_401` — no creds, secret configured → 401
9. `test_rest_api_key_auth` — valid X-API-Key → 200
10. `test_rest_jwt_auth` — valid Bearer token → 200
11. `test_health_no_auth` — /health always 200
12. `test_dev_mode_no_secrets` — no env vars → 200 everywhere

### T5 — Validate
```powershell
pytest tests/test_backend_auth.py -v
pytest tests/ -x -q
```

## Files Changed

| File | Change |
|---|---|
| `backend/auth.py` | NEW — all auth logic |
| `backend/app.py` | Add APIRouter, import auth, add WS auth call |
| `requirements.txt` | Add PyJWT if absent |
| `tests/test_backend_auth.py` | NEW — ≥ 12 test cases |
