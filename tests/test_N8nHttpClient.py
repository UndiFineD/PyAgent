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

"""Module-focused red tests for N8nHttpClient."""

from __future__ import annotations

from importlib import import_module
from typing import Any

import pytest


def _load_symbol(module_name: str, symbol_name: str) -> Any:
    """Load symbol from src.core.n8nbridge with assertion-style red failures."""
    try:
        module = import_module(f"src.core.n8nbridge.{module_name}")
    except ModuleNotFoundError as exc:
        pytest.fail(f"Missing src.core.n8nbridge.{module_name}: {exc}", pytrace=False)
    if not hasattr(module, symbol_name):
        pytest.fail(
            f"Missing symbol {symbol_name} in src.core.n8nbridge.{module_name}",
            pytrace=False,
        )
    return getattr(module, symbol_name)


def _new_config() -> Any:
    """Build N8nBridgeConfig instance for transport tests."""
    config_cls = _load_symbol("N8nBridgeConfig", "N8nBridgeConfig")
    return config_cls.from_env(
        {
            "N8N_BRIDGE_BASE_URL": "https://n8n.example.test",
            "N8N_BRIDGE_INBOUND_ENABLED": "true",
            "N8N_BRIDGE_OUTBOUND_ENABLED": "true",
            "N8N_BRIDGE_API_KEY_HEADER": "X-API-KEY",
            "N8N_BRIDGE_API_KEY_VALUE": "test-key",
            "N8N_BRIDGE_REQUEST_TIMEOUT_SECONDS": "2.0",
            "N8N_BRIDGE_MAX_RETRIES": "2",
            "N8N_BRIDGE_BACKOFF_SECONDS": "0.1",
            "N8N_BRIDGE_IDEMPOTENCY_TTL_SECONDS": "300",
        }
    )


@pytest.mark.asyncio
async def test_n8n_http_client_post_json_includes_auth_and_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure post_json applies API-key header and configured timeout."""
    http_client_cls = _load_symbol("N8nHttpClient", "N8nHttpClient")
    config = _new_config()
    client = http_client_cls(config)

    captured: dict[str, Any] = {}

    class _Response:
        """Tiny fake urllib response object for transport tests."""

        status = 200

        def read(self) -> bytes:
            """Return JSON payload bytes."""
            return b'{"ok": true}'

        def getheaders(self) -> list[tuple[str, str]]:
            """Return synthetic header tuples."""
            return []

    def _fake_urlopen(request: Any, timeout: float) -> _Response:
        """Capture request and timeout for assertion."""
        captured["request"] = request
        captured["timeout"] = timeout
        return _Response()

    monkeypatch.setattr("src.core.n8nbridge.N8nHttpClient.urllib.request.urlopen", _fake_urlopen)
    await client.post_json("/hooks/trigger", {"x": 1}, correlation_id="corr-1")

    assert captured["request"].headers.get(config.api_key_header) == config.api_key_value
    assert captured["timeout"] == config.request_timeout_seconds


@pytest.mark.asyncio
async def test_n8n_http_client_retries_retryable_failures(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure post_json retries retryable failures before success."""
    http_client_cls = _load_symbol("N8nHttpClient", "N8nHttpClient")
    client = http_client_cls(_new_config())

    calls = {"count": 0}

    class _Response:
        """Tiny fake urllib response object for retry tests."""

        status = 200

        def read(self) -> bytes:
            """Return JSON payload bytes."""
            return b'{"ok": true}'

        def getheaders(self) -> list[tuple[str, str]]:
            """Return synthetic header tuples."""
            return []

    def _fake_urlopen(_: Any, __: float) -> _Response:
        """Raise two retryable errors then succeed."""
        calls["count"] += 1
        if calls["count"] < 3:
            raise OSError("temporary")
        return _Response()

    monkeypatch.setattr("src.core.n8nbridge.N8nHttpClient.urllib.request.urlopen", _fake_urlopen)
    await client.post_json("/hooks/trigger", {"x": 1}, correlation_id="corr-1")

    assert calls["count"] == 3
