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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
LM Studio REST API client with HTTP fallback support.
"""

import logging
import os
import time
from typing import Any, Optional

try:
    import httpx
except ImportError:
    httpx = None

logger = logging.getLogger(__name__)


class LMStudioAPIClient:
    """HTTP REST API client for LM Studio with retry and error handling."""

    def __init__(self, base_url: str, api_token: Optional[str] = None, default_model: str = ""):
        """Initialize REST API client.

        Args:
            base_url: Base URL for LM Studio API (e.g., http://localhost:1234 or http://localhost:1234/v1)
            api_token: Optional API token for authentication
            default_model: Default model ID to use
        """
        self.base_url = base_url.rstrip("/")
        self.api_token = api_token or os.getenv("DV_LMSTUDIO_API_TOKEN")
        self.default_model = default_model

    def _normalize_url(self, endpoint: str = "") -> str:
        """Normalize REST API URL, handling both /v1 prefixes.

        Args:
            endpoint: Optional endpoint path (e.g., 'models', 'chat/completions')

        Returns:
            Full normalized URL for the endpoint.
        """
        base = self.base_url
        # Auto-detect: if ends with /v1, use as-is; otherwise assume base is host:port
        if not base.endswith("/v1"):
            api_base = f"{base}/v1"
        else:
            api_base = base

        if endpoint:
            # Handle special cases for endpoint names
            if endpoint == "chat":
                endpoint = "chat/completions"
            return f"{api_base}/{endpoint.lstrip('/')}"
        return api_base

    def _get_headers(self) -> dict[str, str]:
        """Get HTTP headers with API token support."""
        headers = {"Content-Type": "application/json"}
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"
            logger.debug("[LMStudio] Using API token for authorization")
        return headers

    def _http_request_with_retry(
        self, method: str, url: str, max_retries: int = 3, **kwargs
    ) -> Optional[Any]:
        """Make HTTP request with exponential backoff retry for transient errors.

        Args:
            method: HTTP method ('GET', 'POST')
            url: Full URL to request
            max_retries: Maximum number of retry attempts
            **kwargs: Additional args for httpx (json, timeout, etc.)

        Returns:
            Response object if successful, None if failed.
        """
        if httpx is None:
            raise ImportError("httpx is required for LMStudioAPIClient")

        headers = self._get_headers()
        if "headers" in kwargs:
            headers.update(kwargs["headers"])
        kwargs["headers"] = headers

        # Phase 317: Aggressive timeouts for large remote models
        timeout_val = kwargs.get("timeout", 300.0)
        timeout = httpx.Timeout(timeout_val, connect=15.0, read=timeout_val, write=30.0)

        for attempt in range(max_retries):
            try:
                logger.debug(f"[LMStudio] HTTP {method} {url} (attempt {attempt + 1}/{max_retries})")
                if method.upper() == "GET":
                    resp = httpx.get(url, timeout=timeout, headers=headers)
                elif method.upper() == "POST":
                    resp = httpx.post(
                        url,
                        timeout=timeout,
                        headers=headers,
                        **{k: v for k, v in kwargs.items() if k not in ("timeout", "headers")},
                    )
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")

                if resp.status_code >= 400:
                    logger.warning(
                        f"[LMStudio] HTTP {method} {url} returned {resp.status_code}: {resp.text[:500]}"
                    )

                return resp
            except (httpx.TimeoutException, httpx.ConnectError, httpx.NetworkError) as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.warning(
                        f"[LMStudio] HTTP {method} {url} transient error: {e}; retrying in {wait_time}s"
                    )
                    time.sleep(wait_time)
                    continue
                logger.error(f"[LMStudio] HTTP {method} {url} failed after {max_retries} attempts: {e}")
                raise
            except (ValueError, RuntimeError) as e:
                logger.error(f"[LMStudio] HTTP {method} {url} failed: {e}")
                raise

        raise RuntimeError(f"[LMStudio] HTTP {method} {url} failed after {max_retries} attempts")

    def list_models(self) -> list[str]:
        """List available models via REST API.

        Returns:
            List of model identifiers/paths.
        """
        try:
            url = self._normalize_url("models")
            logger.info(f"[LMStudio] Attempting HTTP list models: {url}")
            resp = self._http_request_with_retry("GET", url, max_retries=3, timeout=5.0)

            if resp.status_code == 200:
                data = resp.json()
                models = []
                for item in data:
                    if isinstance(item, dict):
                        models.append(item.get("path") or item.get("id") or item.get("name") or str(item))
                    else:
                        models.append(str(item))
                logger.info(f"[LMStudio] HTTP list_models succeeded: {len(models)} models from {url}")
                return models

            logger.error(
                f"[LMStudio] HTTP list_models returned {resp.status_code} from {url}: {resp.text[:300]}"
            )
        except (httpx.HTTPError, ValueError, RuntimeError) as e:
            logger.error(f"[LMStudio] Failed to list models via HTTP: {e}")

        return []

    def get_info(self) -> dict[str, Any]:
        """Get server info and version.

        Returns:
            Dictionary with server information.
        """
        info = {
            "api_base_url": self._normalize_url(),
            "api_version": None,
        }

        try:
            # Try to fetch server info from common endpoints
            for endpoint in ["info", "version", "status"]:
                try:
                    url = f"{self._normalize_url()}/{endpoint}"
                    resp = self._http_request_with_retry("GET", url, max_retries=1, timeout=2.0)
                    if resp and resp.status_code == 200:
                        data = resp.json()
                        info["api_version"] = (
                            data.get("version") or data.get("api_version") or "unknown"
                        )
                        break
                except (httpx.HTTPError, ValueError, RuntimeError):
                    continue
        except (ValueError, RuntimeError):
            pass

        return info
