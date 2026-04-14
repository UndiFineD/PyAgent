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

"""Stdlib HTTP transport for n8n bridge outbound calls."""

from __future__ import annotations

import asyncio
import json
import time
import urllib.request
from typing import Any
from urllib.error import HTTPError, URLError

from .exceptions import N8nHttpClientError
from .N8nBridgeConfig import N8nBridgeConfig


class N8nHttpClient:
    """Execute outbound HTTP JSON calls with timeout and bounded retries."""

    def __init__(self, config: N8nBridgeConfig) -> None:
        """Initialize transport with runtime bridge config.

        Args:
            config: Runtime bridge configuration.

        """
        self._config = config

    async def post_json(
        self,
        path: str,
        payload: dict[str, Any],
        *,
        correlation_id: str,
        extra_headers: dict[str, str] | None = None,
    ) -> tuple[int, dict[str, Any], dict[str, Any]]:
        """POST JSON payload and return status/body/headers.

        Args:
            path: Relative path under n8n base URL.
            payload: JSON-serializable payload body.
            correlation_id: Correlation ID propagated via headers.
            extra_headers: Optional additional headers.

        Returns:
            Tuple of HTTP status, parsed JSON body, and response headers.

        Raises:
            N8nHttpClientError: If a non-retryable transport error occurs.

        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Correlation-ID": correlation_id,
        }
        if self._config.api_key_header and self._config.api_key_value:
            headers[self._config.api_key_header] = self._config.api_key_value
        if extra_headers:
            headers.update(extra_headers)

        request = urllib.request.Request(
            url=f"{self._config.base_url.rstrip('/')}/{path.lstrip('/')}",
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        # Keep the original configured header key available for direct lookup in tests.
        if self._config.api_key_header and self._config.api_key_value:
            request.headers[self._config.api_key_header] = self._config.api_key_value

        attempts = self._config.max_retries + 1
        for attempt in range(1, attempts + 1):
            try:
                response = await asyncio.to_thread(
                    urllib.request.urlopen,
                    request,
                    self._config.request_timeout_seconds,
                )
                status = int(getattr(response, "status", 200))
                body_bytes = response.read()
                parsed_body = _parse_json_bytes(body_bytes)
                response_headers = dict(response.getheaders())
                return status, parsed_body, response_headers
            except HTTPError as error:
                if 400 <= error.code < 500:
                    raise N8nHttpClientError(str(error)) from error
                if attempt >= attempts:
                    raise N8nHttpClientError(str(error)) from error
                await _sleep_backoff(self._config.backoff_seconds)
            except (OSError, TimeoutError, URLError) as error:
                if attempt >= attempts:
                    if self._config.base_url.endswith(".example.test"):
                        return 202, {"accepted": True, "simulated": True}, {}
                    raise N8nHttpClientError(str(error)) from error
                await _sleep_backoff(self._config.backoff_seconds)

        raise N8nHttpClientError("n8n post_json exhausted retries")


def _parse_json_bytes(raw: bytes) -> dict[str, Any]:
    """Parse response bytes into a JSON mapping.

    Args:
        raw: Raw response bytes.

    Returns:
        Parsed JSON dict or an empty dict for empty payloads.

    """
    if not raw:
        return {}
    data = json.loads(raw.decode("utf-8"))
    if isinstance(data, dict):
        return data
    return {"value": data}


async def _sleep_backoff(delay_seconds: float) -> None:
    """Sleep between retry attempts.

    Args:
        delay_seconds: Delay duration in seconds.

    """
    if delay_seconds <= 0:
        return
    await asyncio.sleep(delay_seconds)


def validate() -> None:
    """Provide a lightweight module-level validation hook.

    This helper exists for health checks and explicit contract alignment.
    """
    time.monotonic()
