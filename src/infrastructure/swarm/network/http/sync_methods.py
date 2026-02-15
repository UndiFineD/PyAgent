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

"""
Sync methods.py module.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Mapping

if TYPE_CHECKING:
    from src.infrastructure.swarm.network.http.connection import HTTPConnection


class SyncHTTPMixin:
    """Mixin providing synchronous HTTP methods."""

    def get_response(
        self: HTTPConnection,
        url: str,
        *,
        stream: bool = False,
        timeout: float | None = None,
        extra_headers: Mapping[str, str] | None = None,
        allow_redirects: bool = True,
    ) -> Any:
        """Make a GET request and return the response object."""
        self._validate_http_url(url)

        client = self.get_sync_client()
        extra_headers = extra_headers or {}

        return client.get(
            url,
            headers=self._headers(**extra_headers),
            stream=stream,
            timeout=timeout or self.default_timeout,
            allow_redirects=allow_redirects,
        )

    def get_bytes(
        self: HTTPConnection,
        url: str,
        *,
        timeout: float | None = None,
        allow_redirects: bool = True,
    ) -> bytes:
        """GET request returning response body as bytes."""
        with self.get_response(url, timeout=timeout, allow_redirects=allow_redirects) as r:
            r.raise_for_status()
            return r.content

    def get_text(
        self: HTTPConnection,
        url: str,
        *,
        timeout: float | None = None,
        encoding: str | None = None,
    ) -> str:
        """GET request returning response body as text."""
        with self.get_response(url, timeout=timeout) as r:
            r.raise_for_status()
            if encoding:
                r.encoding = encoding
            return r.text

    def get_json(
        self: HTTPConnection,
        url: str,
        *,
        timeout: float | None = None,
    ) -> Any:
        """GET request returning response body as parsed JSON."""
        with self.get_response(url, timeout=timeout) as r:
            r.raise_for_status()
            return r.json()

    def post_json(
        self: HTTPConnection,
        url: str,
        data: Any,
        *,
        timeout: float | None = None,
        extra_headers: Mapping[str, str] | None = None,
    ) -> Any:
        """POST JSON data and return parsed JSON response."""
        self._validate_http_url(url)

        client = self.get_sync_client()
        extra_headers = extra_headers or {}

        r = client.post(
            url,
            json=data,
            headers=self._headers(**extra_headers),
            timeout=timeout or self.default_timeout,
        )
        r.raise_for_status()
        return r.json()

    def download_file(
        self: HTTPConnection,
        url: str,
        save_path: Path | str,
        *,
        timeout: float | None = None,
        chunk_size: int = 8192,
        progress_callback: Callable[[int, int | None], None] | None = None,
    ) -> Path:
        """Download a file from URL to local path."""
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)

        with self.get_response(url, stream=True, timeout=timeout) as r:
            r.raise_for_status()

            total_size = int(r.headers.get("content-length", 0)) or None
            downloaded = 0

            with save_path.open("wb", encoding='utf-8') as f:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    f.write(chunk)
                    downloaded += len(chunk)
                    if progress_callback:
                        progress_callback(downloaded, total_size)

        return save_path
