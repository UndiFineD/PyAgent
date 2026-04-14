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

"""Module-focused red tests for N8nEventAdapter."""

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


def test_n8n_event_adapter_maps_valid_inbound_payload() -> None:
    """Ensure inbound payload maps to canonical event and preserves IDs."""
    adapter_cls = _load_symbol("N8nEventAdapter", "N8nEventAdapter")
    adapter = adapter_cls()
    event = adapter.to_inbound_event(
        {
            "event_id": "evt-1",
            "event_type": "workflow.completed",
            "workflow_id": "wf-1",
            "execution_id": "exec-1",
            "occurred_at": "2026-03-27T12:00:00Z",
            "source": "n8n",
            "payload": {"result": "ok"},
            "auth_context": {"mode": "api-key"},
        },
        {"X-Correlation-ID": "corr-1"},
    )
    assert event["event_id"] == "evt-1"
    assert event["correlation_id"] == "corr-1"


def test_n8n_event_adapter_rejects_missing_required_ids() -> None:
    """Ensure inbound schema validation rejects missing identifiers."""
    adapter_cls = _load_symbol("N8nEventAdapter", "N8nEventAdapter")
    adapter = adapter_cls()
    with pytest.raises(Exception, match=r".+"):
        adapter.to_inbound_event(
            {
                "event_type": "workflow.completed",
                "workflow_id": "wf-1",
                "execution_id": "exec-1",
                "occurred_at": "2026-03-27T12:00:00Z",
                "source": "n8n",
                "payload": {},
                "auth_context": {},
            },
            {"X-Correlation-ID": "corr-1"},
        )
