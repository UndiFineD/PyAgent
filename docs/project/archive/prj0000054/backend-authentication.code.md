# backend-authentication — Code Notes

_Owner: @6code | Status: DONE_

## Implementation Summary

### New file: `backend/auth.py`
- `API_KEY = os.getenv("PYAGENT_API_KEY", "")`
- `JWT_SECRET = os.getenv("PYAGENT_JWT_SECRET", "")`
- `DEV_MODE = not API_KEY and not JWT_SECRET`
- `verify_api_key(expected, provided)` — timing-safe via `hmac.compare_digest`
- `verify_jwt(token)` — PyJWT decode, returns None on any error
- `require_auth(x_api_key, authorization)` — FastAPI dependency, raises 401
- `websocket_auth(websocket)` — reads `?api_key=` or `?token=`, closes 4401 on failure

### Modified: `backend/app.py`
- Added `APIRouter`, `Depends` imports + `from .auth import require_auth, websocket_auth`
- Created `_auth_router = APIRouter(dependencies=[Depends(require_auth)])`
- Re-registered all protected endpoints on `_auth_router` (metrics, agent-log, agent-doc, projects)
- `/health` remains on `app` directly (unauthenticated)
- `app.include_router(_auth_router)` at end
- WS endpoint now calls `await websocket_auth(websocket)` and returns early on None

### Modified: `backend/requirements.txt`
- Added `PyJWT>=2.8.0`

## Test file: `tests/test_backend_auth.py`
- 17 test cases (9 unit + 8 integration)
- All pass: 17/17
