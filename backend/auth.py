#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Authentication helpers for the PyAgent backend.

Supports two credential types, either of which satisfies any protected endpoint:

* **API key** — ``X-API-Key: <key>`` request header (REST) or
  ``?api_key=<key>`` query parameter (WebSocket).
* **JWT** — ``Authorization: Bearer <token>`` request header (REST) or
  ``?token=<token>`` query parameter (WebSocket).

Secrets are read from environment variables:

* ``PYAGENT_API_KEY`` — shared API key.
* ``PYAGENT_JWT_SECRET`` — HS256 signing secret for JWTs.

When **neither** variable is set the module enters *dev mode*: all requests are
allowed through and a one-time WARNING is emitted at import time.  Set at
least one variable in production.
"""
from __future__ import annotations

import hmac
import logging
import os
from typing import Any, Optional

import jwt
from fastapi import Header, HTTPException, WebSocket, status

_log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Module-level configuration (read once at import time; monkeypatched in tests)
# ---------------------------------------------------------------------------

API_KEY: str = os.getenv("PYAGENT_API_KEY", "")
JWT_SECRET: str = os.getenv("PYAGENT_JWT_SECRET", "")
JWT_ALGORITHM: str = "HS256"

# Dev mode: neither secret is configured → allow all, warn loudly.
DEV_MODE: bool = not API_KEY and not JWT_SECRET

if DEV_MODE:
    _log.warning(
        "PYAGENT_API_KEY and PYAGENT_JWT_SECRET are not set — "
        "authentication is DISABLED (dev mode). "
        "Set these environment variables before running in production."
    )

# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------


def verify_api_key(expected: str, provided: Optional[str]) -> bool:
    """Return True iff *provided* exactly matches *expected* (timing-safe).

    Returns False immediately when *expected* is empty or *provided* is None,
    without performing a comparison that could leak timing information about
    the expected value.
    """
    if not expected or provided is None:
        return False
    return hmac.compare_digest(expected, provided)


def verify_jwt(token: Optional[str]) -> Optional[dict[str, Any]]:
    """Decode and verify a JWT, returning the payload on success or None.

    Returns None for any error condition: missing token, wrong secret,
    expired token, or malformed input.  Callers should treat None as
    "authentication failed".
    """
    if not token or not JWT_SECRET:
        return None
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError:
        return None

# ---------------------------------------------------------------------------
# FastAPI dependencies
# ---------------------------------------------------------------------------


async def require_auth(
    x_api_key: Optional[str] = Header(default=None),
    authorization: Optional[str] = Header(default=None),
) -> dict[str, Any]:
    """FastAPI dependency that enforces API-key or JWT authentication.

    When ``DEV_MODE`` is True (neither secret is configured) every request is
    allowed through so existing dev/test workflows are not broken.

    Raises HTTP 401 when a secret is configured but neither credential is valid.
    """
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


async def websocket_auth(websocket: WebSocket) -> Optional[dict[str, Any]]:
    """Authenticate an already-accepted WebSocket connection.

    Reads credentials from query parameters (HTTP headers are unavailable after
    the WebSocket upgrade handshake).  On failure the connection is closed with
    code 4401 and None is returned; the caller should return immediately.

    Returns a dict describing the successful auth method, or None on failure.
    """
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
