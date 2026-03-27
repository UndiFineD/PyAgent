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

"""Module-focused red tests for N8nBridgeConfig."""

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


def test_n8n_bridge_config_from_env_loads_expected_values() -> None:
    """Ensure from_env maps required values into config object attributes."""
    config_cls = _load_symbol("N8nBridgeConfig", "N8nBridgeConfig")
    config = config_cls.from_env(
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
    assert config.base_url == "https://n8n.example.test"
    assert config.request_timeout_seconds == 2.0
    assert config.max_retries == 2


def test_n8n_bridge_config_validate_rejects_invalid_runtime_values() -> None:
    """Ensure validate rejects invalid URL, timeout, and retries."""
    config_cls = _load_symbol("N8nBridgeConfig", "N8nBridgeConfig")
    config = config_cls.from_env(
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
    config.base_url = "invalid"
    config.request_timeout_seconds = 0
    config.max_retries = -1
    with pytest.raises(Exception, match=r".+"):
        config.validate()
