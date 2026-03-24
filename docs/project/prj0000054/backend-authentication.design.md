# backend-authentication — Design

_Owner: @3design | Status: DONE_

## Module: `backend/auth.py` (new file)

```python
import hashlib
import hmac
import logging
import os
from typing import Any, Optional

import jwt
from fastapi import Header, HTTPException, status

_log = logging.getLogger(__name__)

API_KEY: str = os.getenv("PYAGENT_API_KEY", "")
JWT_SECRET: str = os.getenv("PYAGENT_JWT_SECRET", "")
JWT_ALGORITHM = "HS256"
DEV_MODE: bool = not API_KEY and not JWT_SECRET

if DEV_MODE:
    _log.warning(
        "PYAGENT_API_KEY and PYAGENT_JWT_SECRET are not set — "
        "authentication is DISABLED (dev mode). Set these in production."
    )


def verify_api_key(expected: str, provided: Optional[str]) -> bool:
    if not expected or provided is None:
        return False
    return hmac.compare_digest(expected, provided)


def verify_jwt(token: Optional[str]) -> Optional[dict[str, Any]]:
    if not token or not JWT_SECRET:
        return None
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError:
        return None


async def require_auth(
    x_api_key: Optional[str] = Header(default=None),
    authorization: Optional[str] = Header(default=None),
) -> dict[str, Any]:
    if DEV_MODE:
        return {"auth": "dev_mode"}
    if verify_api_key(API_KEY, x_api_key):
        return {"auth": "api_key"}
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ", 1)[1]
        payload = verify_jwt(token)
        if payload is not None:
            return {"auth": "jwt", "payload": payload}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized — provide X-API-Key or Authorization: Bearer <token>",
    )


async def websocket_auth(websocket) -> Optional[dict[str, Any]]:
    if DEV_MODE:
        return {"auth": "dev_mode"}
    api_key = websocket.query_params.get("api_key")
    if verify_api_key(API_KEY, api_key):
        return {"auth": "api_key"}
    token = websocket.query_params.get("token")
    payload = verify_jwt(token)
    if payload is not None:
        return {"auth": "jwt", "payload": payload}
    await websocket.close(code=4401)
    return None
```

## Changes to `backend/app.py`

1. Add `from .auth import require_auth, websocket_auth, DEV_MODE` import.
2. Create `auth_router = APIRouter(dependencies=[Depends(require_auth)])`.
3. Move all protected endpoints from `app.*` decorators to `auth_router.*` decorators.
4. Keep `GET /health` directly on `app` (no auth).
5. `app.include_router(auth_router)` at the end of setup.
6. WebSocket endpoint stays on `app.websocket("/ws")` but calls `websocket_auth` early.

## Interface Summary

| Function | Input | Output | Notes |
|---|---|---|---|
| `verify_api_key(expected, provided)` | two strings | bool | timing-safe |
| `verify_jwt(token)` | str or None | dict or None | returns None on any error |
| `require_auth(x_api_key, authorization)` | FastAPI headers | dict | raises 401 |
| `websocket_auth(websocket)` | WebSocket | dict or None | closes 4401 on fail |

## Dev Mode Logic

```
DEV_MODE = not API_KEY and not JWT_SECRET
```

When `DEV_MODE` is True: all auth functions return success immediately, no rejection.
Production deployments must set at least one secret.
