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
"""Security-oriented tests for readyz degraded payload safety."""

from __future__ import annotations

import re

import pytest
from fastapi.testclient import TestClient

from backend.app import app

client = TestClient(app, raise_server_exceptions=False)
_REASON_PATTERN = re.compile(r"^[a-z0-9_]{1,64}$")


@pytest.fixture(autouse=True)
def reset_probe_state(monkeypatch: pytest.MonkeyPatch):
    """Reset readiness probe controls between tests for deterministic behavior."""
    monkeypatch.delenv("PYAGENT_READYZ_FORCE_DEGRADED", raising=False)
    monkeypatch.delenv("PYAGENT_READYZ_DEGRADED_REASON", raising=False)
    if hasattr(app.state, "readyz_degraded_reason"):
        delattr(app.state, "readyz_degraded_reason")
    yield
    if hasattr(app.state, "readyz_degraded_reason"):
        delattr(app.state, "readyz_degraded_reason")


def test_readyz_degraded_reason_is_machine_readable_when_safe() -> None:
    """Safe readiness reasons are normalized into machine-readable form."""
    app.state.readyz_degraded_reason = "DB Connection Timeout"

    response = client.get("/v1/readyz")
    payload = response.json()

    assert response.status_code == 503
    assert payload == {
        "status": "degraded",
        "ready": False,
        "reason": "db_connection_timeout",
    }
    assert _REASON_PATTERN.fullmatch(payload["reason"])


def test_readyz_degraded_payload_rejects_unsafe_state_reason() -> None:
    """Unsafe state reasons are replaced with stable sanitized fallback."""
    app.state.readyz_degraded_reason = "password=supersecret token=bearer /etc/passwd"

    response = client.get("/v1/readyz")
    payload = response.json()

    assert response.status_code == 503
    assert payload["status"] == "degraded"
    assert payload["ready"] is False
    assert payload["reason"] == "degraded_reason_sanitized"
    assert set(payload.keys()) == {"status", "ready", "reason"}
    assert _REASON_PATTERN.fullmatch(payload["reason"])


def test_readyz_degraded_payload_rejects_unsafe_env_reason(monkeypatch: pytest.MonkeyPatch) -> None:
    """Unsafe environment-provided degraded reasons are replaced with fallback."""
    monkeypatch.setenv("PYAGENT_READYZ_FORCE_DEGRADED", "1")
    monkeypatch.setenv("PYAGENT_READYZ_DEGRADED_REASON", "Authorization: Bearer abc.def.ghi")

    response = client.get("/v1/readyz")
    payload = response.json()

    assert response.status_code == 503
    assert payload == {
        "status": "degraded",
        "ready": False,
        "reason": "degraded_reason_sanitized",
    }


def test_readyz_degraded_payload_rejects_sensitive_like_fields() -> None:
    """Degraded payload does not expose sensitive diagnostic fields."""
    app.state.readyz_degraded_reason = "secret key leaked"

    response = client.get("/v1/readyz")
    payload = response.json()

    assert response.status_code == 503
    lowered_keys = {key.lower() for key in payload}
    for disallowed in (
        "token",
        "secret",
        "password",
        "stack",
        "traceback",
        "exception",
        "filepath",
        "internal",
        "debug",
    ):
        assert disallowed not in lowered_keys
