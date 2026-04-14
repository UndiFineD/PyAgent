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

"""/v1/models capability probe and auto-selection for the Fastflow Language Model provider.

FLM stands for Fastflow Language Model.
Usage::

    result = await probe_models("http://127.0.0.1:52625", timeout=5)
    model = select_model(result.available_models, preferred="llama3.2:1b")
"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from typing import Sequence
from urllib.parse import urljoin


@dataclass
class FlmModelProbeResult:
    """Outcome of a /v1/models probe against an FLM endpoint."""

    base_url: str
    available_models: list[str]
    selected_model: str | None
    latency_ms: float
    error: str | None = None

    @property
    def reachable(self) -> bool:
        """True when the probe succeeded without errors."""
        return self.error is None

    def to_dict(self) -> dict:
        return {
            "base_url": self.base_url,
            "available_models": self.available_models,
            "selected_model": self.selected_model,
            "latency_ms": self.latency_ms,
            "reachable": self.reachable,
            "error": self.error,
        }


def select_model(available: Sequence[str], preferred: str | None = None) -> str | None:
    """Choose the best model from *available*, optionally honouring *preferred*.

    Selection rules (first match wins):
    1. If *preferred* is in *available*, return it.
    2. If *preferred* is a prefix-substring of any available model, return the
       first such match (useful for partial names like ``"llama3"``).
    3. Return the first element of *available* as a fallback.
    4. If *available* is empty, return ``None``.
    """
    if not available:
        return None
    if preferred is not None:
        if preferred in available:
            return preferred
        match = next(
            (model for model in available if model.startswith(preferred) or preferred in model),
            None,
        )
        if match is not None:
            return match
    return available[0]


async def probe_models(
    base_url: str,
    *,
    timeout: float = 5.0,
    models_path: str = "/v1/models",
    preferred: str | None = None,
) -> FlmModelProbeResult:
    """Async probe of the FLM ``/v1/models`` endpoint.

    Performs a raw HTTP GET using :mod:`asyncio` streams (no third-party
    dependency at runtime) so the probe has minimal overhead and works inside
    the existing async runtime.

    Args:
        base_url:     FLM endpoint root, e.g. ``"http://127.0.0.1:52625"``.
        timeout:      Socket connection + read timeout in seconds.
        models_path:  Path component for the models listing (default ``/v1/models``).
        preferred:    Optional model name hint forwarded to :func:`select_model`.

    Returns:
        :class:`FlmModelProbeResult` describing the outcome.  The *error* field
        is set when the endpoint is unreachable or returns a non-200 status.

    """
    url = urljoin(base_url.rstrip("/") + "/", models_path.lstrip("/"))
    start = time.monotonic()
    try:
        body = await asyncio.wait_for(_http_get(url), timeout=timeout)
        latency_ms = (time.monotonic() - start) * 1000
        models = _parse_models_body(body)
        return FlmModelProbeResult(
            base_url=base_url,
            available_models=models,
            selected_model=select_model(models, preferred),
            latency_ms=round(latency_ms, 2),
        )
    except asyncio.TimeoutError:
        latency_ms = (time.monotonic() - start) * 1000
        return FlmModelProbeResult(
            base_url=base_url,
            available_models=[],
            selected_model=None,
            latency_ms=round(latency_ms, 2),
            error=f"Connection timed out after {timeout}s ({url})",
        )
    except OSError as exc:
        latency_ms = (time.monotonic() - start) * 1000
        return FlmModelProbeResult(
            base_url=base_url,
            available_models=[],
            selected_model=None,
            latency_ms=round(latency_ms, 2),
            error=f"Connection error: {exc} ({url})",
        )
    except ValueError as exc:
        latency_ms = (time.monotonic() - start) * 1000
        return FlmModelProbeResult(
            base_url=base_url,
            available_models=[],
            selected_model=None,
            latency_ms=round(latency_ms, 2),
            error=f"Response parse error: {exc}",
        )


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


async def _http_get(url: str) -> str:
    """Minimal async HTTP GET returning the response body as a string.

    Parses only what we need:  response status + body.  Not a general HTTP
    client — used exclusively for the /v1/models probe path.
    """
    from urllib.parse import urlparse

    parsed = urlparse(url)
    host = parsed.hostname or ""
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    path = parsed.path or "/"
    if parsed.query:
        path = f"{path}?{parsed.query}"

    reader, writer = await asyncio.open_connection(host, port)
    try:
        request = f"GET {path} HTTP/1.0\r\nHost: {host}:{port}\r\nAccept: application/json\r\nConnection: close\r\n\r\n"
        writer.write(request.encode())
        await writer.drain()

        raw = await reader.read(65536)
    finally:
        writer.close()

    text = raw.decode("utf-8", errors="replace")
    # Split headers from body
    if "\r\n\r\n" in text:
        header_section, body = text.split("\r\n\r\n", 1)
    elif "\n\n" in text:
        header_section, body = text.split("\n\n", 1)
    else:
        raise ValueError("Malformed HTTP response: no header/body separator")

    status_line = header_section.splitlines()[0]
    parts = status_line.split(None, 2)
    if len(parts) < 2:
        raise ValueError(f"Malformed HTTP status line: {status_line!r}")
    status_code = int(parts[1])
    if status_code != 200:
        raise ValueError(f"FLM /v1/models returned HTTP {status_code}")
    return body


def validate() -> bool:
    """Confirm the FlmModelProbe module is importable and core symbols are accessible."""
    assert FlmModelProbeResult and probe_models and select_model  # noqa: S101
    return True


def _parse_models_body(body: str) -> list[str]:
    """Extract model id strings from a minimal OpenAI /v1/models JSON body.

    Expected shape::

        {"object": "list", "data": [{"id": "llama3.2:1b", ...}, ...]}

    Uses stdlib :mod:`json` for correctness; falls back to an empty list on
    unexpected shapes.
    """
    import json

    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON decode error: {exc}") from exc

    data = parsed.get("data", [])
    if not isinstance(data, list):
        return []
    return [entry["id"] for entry in data if isinstance(entry, dict) and "id" in entry]
