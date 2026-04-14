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

"""Validation tests for FLM provider configuration."""

from __future__ import annotations

import pytest

from src.core.providers.FlmProviderConfig import FlmProviderConfig


def test_flm_provider_config_parses_required_and_optional_fields() -> None:
    """Config parser should map required and optional fields correctly."""
    cfg = FlmProviderConfig.from_mapping(
        {
            "base_url": "http://127.0.0.1:52625/v1/",
            "default_model": "llama3.2:1b",
            "timeout": 180,
            "max_retries": 5,
            "health_path": "/v1/health",
            "chat_path": "/v1/chat/completions",
        }
    )

    assert cfg.base_url == "http://127.0.0.1:52625/v1/"
    assert cfg.default_model == "llama3.2:1b"
    assert cfg.timeout == 180
    assert cfg.max_retries == 5
    assert cfg.health_path == "/v1/health"
    assert cfg.chat_path == "/v1/chat/completions"


def test_flm_provider_config_applies_defaults() -> None:
    """Defaults should be applied for optional values when omitted."""
    cfg = FlmProviderConfig.from_mapping(
        {
            "base_url": "http://127.0.0.1:52625/v1/",
            "default_model": "llama3.2:1b",
        }
    )

    assert cfg.timeout == 120
    assert cfg.max_retries == 3
    assert cfg.health_path == "/v1/health"
    assert cfg.chat_path == "/v1/chat/completions"


@pytest.mark.parametrize("missing_key", ["base_url", "default_model"])
def test_flm_provider_config_requires_required_fields(missing_key: str) -> None:
    """Missing required keys should raise actionable validation errors."""
    data = {
        "base_url": "http://127.0.0.1:52625/v1/",
        "default_model": "llama3.2:1b",
    }
    data.pop(missing_key)

    with pytest.raises(ValueError, match=missing_key):
        FlmProviderConfig.from_mapping(data)


def test_flm_provider_config_rejects_invalid_timeout() -> None:
    """Timeout must be a positive integer."""
    with pytest.raises(ValueError, match="timeout"):
        FlmProviderConfig.from_mapping(
            {
                "base_url": "http://127.0.0.1:52625/v1/",
                "default_model": "llama3.2:1b",
                "timeout": 0,
            }
        )


def test_flm_provider_config_rejects_invalid_path() -> None:
    """Path values must start with '/' for API route compatibility."""
    with pytest.raises(ValueError, match="chat_path"):
        FlmProviderConfig.from_mapping(
            {
                "base_url": "http://127.0.0.1:52625/v1/",
                "default_model": "llama3.2:1b",
                "chat_path": "v1/chat/completions",
            }
        )


def test_flm_provider_config_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Configuration can be loaded from environment variables."""
    monkeypatch.setenv("DV_FLM_BASE_URL", "http://192.168.1.128:52625/v1")
    monkeypatch.setenv("DV_FLM_DEFAULT_MODEL", "llama3.2:1b")

    cfg = FlmProviderConfig.from_env()

    assert cfg.base_url == "http://192.168.1.128:52625/v1"
    assert cfg.default_model == "llama3.2:1b"
