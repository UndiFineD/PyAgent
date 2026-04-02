# backend-authentication — Think / Analysis

_Owner: @2think | Status: DONE_

## Current State of `backend/app.py`

- FastAPI app with CORS middleware.
- Endpoints: `GET /health`, `GET /api/metrics/system`, `GET /api/agent-log/{id}`,
  `PUT /api/agent-log/{id}`, `GET /api/agent-doc/{id}`, `PUT /api/agent-doc/{id}`,
  `GET /api/projects`, `PATCH /api/projects/{id}`, `POST /api/projects`,
  `WebSocket /ws`.
- **None of these endpoints require authentication.**
- `SessionManager` + `handle_message` for WS session management.

## Key Constraints

### WebSocket authentication
HTTP headers are available only during the WS handshake in FastAPI; once upgraded,
normal `Header()` dependencies don't apply to the WS route. The standard pattern is:
- Accept the connection (`await websocket.accept()`)
- Read auth from `websocket.query_params`
- Close with 4401 if invalid

### Backward compatibility
Many tests and the dev workflow send no auth headers. Two mitigations:
1. When neither `PYAGENT_API_KEY` nor `PYAGENT_JWT_SECRET` is set → skip enforcement, warn.
2. Existing tests that do not set env vars will continue to pass.

### Separation of concerns
All auth logic belongs in `backend/auth.py`, not inline in `app.py`. This allows:
- Independent unit testing of auth helpers.
- Easy reuse / extension (e.g., adding OAuth later).

## Design Decisions

### Where to put the global dependency
FastAPI supports `app = FastAPI(dependencies=[Depends(require_auth)])` to protect
**all** routes globally. However, `/health` must remain open for load-balancers.
Preferred approach: apply `require_auth` individually to each route that needs it,
or use a router-level dependency on an authenticated router.

The cleaner pattern is an **APIRouter with dependencies**:
```python
auth_router = APIRouter(dependencies=[Depends(require_auth)])
# register all protected endpoints on auth_router
# register /health directly on app
```

### JWT library
`PyJWT` (`import jwt`) is the standard. We need to check if it is already in
`requirements.txt`. If not, add it.

### API key storage
Single string from env var `PYAGENT_API_KEY`. No key rotation in this scope.
If multiple keys are needed in future, the `verify_api_key` function can be extended
to accept a set.

## Risk: JWT secret strength
A weak / short secret makes HS256 brute-forceable. Document that the secret must be
≥ 32 random bytes in production. `PYAGENT_JWT_SECRET` defaults to empty = dev mode.

## Conclusion
- New file `backend/auth.py` with: `verify_api_key`, `verify_jwt`, `require_auth` (REST), `websocket_auth`.
- In `app.py`: import auth module, apply `require_auth` to all non-health REST routes, apply `websocket_auth` in the WS handler.
- Dev mode: both env vars unset → allow all, warn once at startup.
