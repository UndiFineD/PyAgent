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

"""Module-focused red tests for N8nBridgeCore."""

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
    """Build N8nBridgeConfig instance for core tests."""
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
async def test_n8n_bridge_core_rejects_duplicate_event_ids_within_ttl() -> None:
    """Ensure duplicate inbound callback IDs are rejected inside TTL."""
    core_cls = _load_symbol("N8nBridgeCore", "N8nBridgeCore")
    adapter_cls = _load_symbol("N8nEventAdapter", "N8nEventAdapter")
    http_client_cls = _load_symbol("N8nHttpClient", "N8nHttpClient")

    core = core_cls(config=_new_config(), adapter=adapter_cls(), http_client=http_client_cls(_new_config()))
    payload = {
        "event_id": "dup-1",
        "event_type": "workflow.completed",
        "workflow_id": "wf-1",
        "execution_id": "exec-1",
        "occurred_at": "2026-03-27T12:00:00Z",
        "source": "n8n",
        "payload": {},
        "auth_context": {},
    }
    first = await core.handle_inbound_event(payload, {"X-Correlation-ID": "corr-1"})
    second = await core.handle_inbound_event(payload, {"X-Correlation-ID": "corr-2"})
    assert first["ok"] is True
    assert second["ok"] is False


@pytest.mark.asyncio
async def test_n8n_bridge_core_trigger_workflow_returns_bridge_result() -> None:
    """Ensure trigger_workflow returns canonical N8nBridgeResult shape."""
    core_cls = _load_symbol("N8nBridgeCore", "N8nBridgeCore")
    adapter_cls = _load_symbol("N8nEventAdapter", "N8nEventAdapter")
    http_client_cls = _load_symbol("N8nHttpClient", "N8nHttpClient")

    core = core_cls(config=_new_config(), adapter=adapter_cls(), http_client=http_client_cls(_new_config()))
    result = await core.trigger_workflow(
        workflow_id="wf-1",
        event_type="agent.task.created",
        payload={"k": "v"},
        correlation_id="corr-1",
    )
    assert isinstance(result, dict)
    assert "ok" in result
    assert "status" in result
    assert "correlation_id" in result
