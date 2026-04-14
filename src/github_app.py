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
"""GitHub App webhook receiver and event router.

Supported events:
  - push
  - pull_request
  - issues
  - ping

All other event types are accepted and acknowledged with ``{"received": True}``.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
import os
from typing import Any, Optional

from fastapi import FastAPI, Header, HTTPException, Request, status

app = FastAPI(title="PyAgent GitHub App", version="1.0.0")
_log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# HMAC-SHA256 webhook signature verification
# ---------------------------------------------------------------------------

WEBHOOK_SECRET: str = os.getenv("GITHUB_WEBHOOK_SECRET", "")
if not WEBHOOK_SECRET:
    _log.warning(
        "GITHUB_WEBHOOK_SECRET is not set — webhook signature verification is DISABLED. "
        "Set this environment variable in production."
    )


def verify_github_signature(
    secret: str,
    body: bytes,
    signature_header: Optional[str],
) -> bool:
    """Return True iff the HMAC-SHA256 signature matches the body.

    Uses hmac.compare_digest for constant-time comparison, preventing
    timing side-channel attacks.
    Returns False if secret is empty, header is None, or header is malformed.
    """
    if not secret or not signature_header:
        return False
    if not signature_header.startswith("sha256="):
        return False
    received = signature_header.split("=", 1)[1]
    computed = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(computed, received)


# ---------------------------------------------------------------------------
# Event routing helpers
# ---------------------------------------------------------------------------


def _handle_push(payload: dict[str, Any]) -> dict[str, Any]:
    ref = payload.get("ref", "")
    repo = payload.get("repository", {}).get("full_name", "unknown")
    commits = len(payload.get("commits", []))
    _log.info("push: repo=%s ref=%s commits=%d", repo, ref, commits)
    return {"event": "push", "repo": repo, "ref": ref, "commits": commits}


def _handle_pull_request(payload: dict[str, Any]) -> dict[str, Any]:
    action = payload.get("action", "")
    pr = payload.get("pull_request", {})
    number = pr.get("number")
    title = pr.get("title", "")
    repo = payload.get("repository", {}).get("full_name", "unknown")
    _log.info("pull_request: repo=%s #%s action=%s", repo, number, action)
    return {"event": "pull_request", "repo": repo, "number": number, "action": action, "title": title}


def _handle_issues(payload: dict[str, Any]) -> dict[str, Any]:
    action = payload.get("action", "")
    issue = payload.get("issue", {})
    number = issue.get("number")
    title = issue.get("title", "")
    repo = payload.get("repository", {}).get("full_name", "unknown")
    _log.info("issues: repo=%s #%s action=%s", repo, number, action)
    return {"event": "issues", "repo": repo, "number": number, "action": action, "title": title}


_HANDLERS = {
    "push": _handle_push,
    "pull_request": _handle_pull_request,
    "issues": _handle_issues,
}

# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@app.get("/v1/health")
@app.get("/health")
def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/webhook")
async def webhook(
    request: Request,
    x_github_event: str = Header(default=""),
    x_hub_signature_256: Optional[str] = Header(default=None),
) -> dict[str, Any]:
    """Receive and route GitHub webhook events.

    GitHub sends the event type in the ``X-GitHub-Event`` header and signs
    the payload with ``X-Hub-Signature-256`` when a webhook secret is set.
    If ``GITHUB_WEBHOOK_SECRET`` is configured, any request whose signature
    is missing or incorrect is rejected with HTTP 401.
    """
    body = await request.body()  # raw bytes — must be read before json() for HMAC

    if WEBHOOK_SECRET:
        if not verify_github_signature(WEBHOOK_SECRET, body, x_hub_signature_256):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing webhook signature",
            )

    try:
        payload: dict[str, Any] = json.loads(body)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    if x_github_event == "ping":
        zen = payload.get("zen", "")
        _log.info("ping received: %s", zen)
        return {"received": True, "event": "ping", "zen": zen}

    handler = _HANDLERS.get(x_github_event)
    if handler:
        return handler(payload)

    # Unknown event — acknowledge gracefully
    _log.debug("unhandled event: %s", x_github_event)
    return {"received": True, "event": x_github_event}
