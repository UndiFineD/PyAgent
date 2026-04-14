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

"""Module-focused red tests for N8nBridgeMixin."""

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


@pytest.mark.asyncio
async def test_n8n_bridge_mixin_n8n_trigger_delegates_to_core() -> None:
    """Ensure n8n_trigger delegates to _n8n_bridge_core.trigger_workflow."""
    mixin_cls = _load_symbol("N8nBridgeMixin", "N8nBridgeMixin")

    class _Core:
        """Minimal core stub for n8n_trigger delegation tests."""

        async def trigger_workflow(
            self,
            *,
            workflow_id: str,
            event_type: str,
            payload: dict[str, Any],
            correlation_id: str | None = None,
        ) -> dict[str, Any]:
            """Return call details as a canonical result payload."""
            return {
                "ok": True,
                "status": "accepted",
                "http_status": 202,
                "correlation_id": correlation_id,
                "event_id": "evt-1",
                "attempts": 1,
                "retryable": False,
                "error_code": None,
                "message": "accepted",
                "data": {
                    "workflow_id": workflow_id,
                    "event_type": event_type,
                    "payload": payload,
                },
            }

    class _Host(mixin_cls):
        """Host object exposing required _n8n_bridge_core attribute."""

        def __init__(self) -> None:
            """Attach a core stub for delegation behavior tests."""
            self._n8n_bridge_core = _Core()

    host = _Host()
    result = await host.n8n_trigger("wf-1", "agent.task.created", {"x": 1}, correlation_id="corr-1")
    assert result["ok"] is True
    assert result["data"]["workflow_id"] == "wf-1"
    assert result["data"]["event_type"] == "agent.task.created"


@pytest.mark.asyncio
async def test_n8n_bridge_mixin_n8n_handle_callback_delegates_to_core() -> None:
    """Ensure n8n_handle_callback delegates to _n8n_bridge_core.handle_inbound_event."""
    mixin_cls = _load_symbol("N8nBridgeMixin", "N8nBridgeMixin")

    class _Core:
        """Minimal core stub for callback delegation tests."""

        async def handle_inbound_event(
            self,
            raw_payload: dict[str, Any],
            headers: dict[str, str],
        ) -> dict[str, Any]:
            """Return call details as a canonical callback result payload."""
            return {
                "ok": True,
                "status": "processed",
                "http_status": 200,
                "correlation_id": headers.get("X-Correlation-ID", ""),
                "event_id": raw_payload["event_id"],
                "attempts": 1,
                "retryable": False,
                "error_code": None,
                "message": "processed",
                "data": raw_payload,
            }

    class _Host(mixin_cls):
        """Host object exposing required _n8n_bridge_core attribute."""

        def __init__(self) -> None:
            """Attach a core stub for delegation behavior tests."""
            self._n8n_bridge_core = _Core()

    host = _Host()
    payload = {"event_id": "evt-1", "event_type": "workflow.completed"}
    result = await host.n8n_handle_callback(payload, {"X-Correlation-ID": "corr-1"})
    assert result["ok"] is True
    assert result["event_id"] == "evt-1"
    assert result["correlation_id"] == "corr-1"
