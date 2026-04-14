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

"""Runtime configuration for the n8n bridge."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping
from urllib.parse import urlparse

from .exceptions import N8nBridgeConfigError


@dataclass(slots=True)
class N8nBridgeConfig:
    """Configuration model used by n8n bridge runtime components.

    Args:
        base_url: Absolute n8n base URL.
        inbound_enabled: Whether inbound callback handling is enabled.
        outbound_enabled: Whether outbound trigger posting is enabled.
        api_key_header: Header name used for static API key auth.
        api_key_value: Header value used for static API key auth.
        request_timeout_seconds: HTTP timeout in seconds.
        max_retries: Maximum retry attempts for retryable failures.
        backoff_seconds: Backoff delay between retries.
        idempotency_ttl_seconds: Inbound event duplicate detection TTL.

    """

    base_url: str
    inbound_enabled: bool = True
    outbound_enabled: bool = True
    api_key_header: str = "X-API-KEY"
    api_key_value: str = ""
    request_timeout_seconds: float = 5.0
    max_retries: int = 0
    backoff_seconds: float = 0.0
    idempotency_ttl_seconds: int = 300

    @classmethod
    def from_env(cls, env: Mapping[str, str]) -> "N8nBridgeConfig":
        """Build a validated config from environment-like values.

        Args:
            env: Mapping containing `N8N_BRIDGE_*` keys.

        Returns:
            Parsed and validated bridge config.

        Raises:
            N8nBridgeConfigError: If any value is missing or invalid.

        """
        config = cls(
            base_url=env.get("N8N_BRIDGE_BASE_URL", "").strip(),
            inbound_enabled=_parse_bool(env.get("N8N_BRIDGE_INBOUND_ENABLED", "true")),
            outbound_enabled=_parse_bool(env.get("N8N_BRIDGE_OUTBOUND_ENABLED", "true")),
            api_key_header=env.get("N8N_BRIDGE_API_KEY_HEADER", "X-API-KEY").strip(),
            api_key_value=env.get("N8N_BRIDGE_API_KEY_VALUE", "").strip(),
            request_timeout_seconds=float(env.get("N8N_BRIDGE_REQUEST_TIMEOUT_SECONDS", "5.0")),
            max_retries=int(env.get("N8N_BRIDGE_MAX_RETRIES", "0")),
            backoff_seconds=float(env.get("N8N_BRIDGE_BACKOFF_SECONDS", "0.0")),
            idempotency_ttl_seconds=int(env.get("N8N_BRIDGE_IDEMPOTENCY_TTL_SECONDS", "300")),
        )
        config.validate()
        return config

    def validate(self) -> None:
        """Validate runtime constraints for bridge configuration.

        Raises:
            N8nBridgeConfigError: If configuration values are invalid.

        """
        parsed = urlparse(self.base_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise N8nBridgeConfigError("N8N_BRIDGE_BASE_URL must be an absolute http(s) URL")
        if self.request_timeout_seconds <= 0:
            raise N8nBridgeConfigError("N8N_BRIDGE_REQUEST_TIMEOUT_SECONDS must be > 0")
        if self.max_retries < 0:
            raise N8nBridgeConfigError("N8N_BRIDGE_MAX_RETRIES must be >= 0")
        if self.backoff_seconds < 0:
            raise N8nBridgeConfigError("N8N_BRIDGE_BACKOFF_SECONDS must be >= 0")
        if self.idempotency_ttl_seconds <= 0:
            raise N8nBridgeConfigError("N8N_BRIDGE_IDEMPOTENCY_TTL_SECONDS must be > 0")


def _parse_bool(value: str) -> bool:
    """Parse bool-like string values used by environment variables.

    Args:
        value: Source text value.

    Returns:
        Parsed boolean value.

    """
    return value.strip().lower() in {"1", "true", "yes", "on"}
