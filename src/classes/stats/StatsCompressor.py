#!/usr/bin/env python3

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations

from typing import Any
import json
import zlib

class StatsCompressor:
    """Compresses metric data."""
    def compress(self, data: Any) -> bytes:
        """Compress data.

        Compatibility: tests pass Python objects like `list[float]`.
        """
        if isinstance(data, (bytes, bytearray)):
            payload = b"b" + bytes(data)
        else:
            payload = b"j" + json.dumps(data, separators=(",", ":")).encode("utf-8")
        return zlib.compress(payload)

    def decompress(self, data: bytes) -> Any:
        """Decompress data."""
        payload = zlib.decompress(data)
        if not payload:
            return payload
        tag = payload[:1]
        body = payload[1:]
        if tag == b"b":
            return body
        if tag == b"j":
            return json.loads(body.decode("utf-8"))
        # Best-effort fallback for legacy payloads.
        try:
            return json.loads(payload.decode("utf-8"))
        except Exception:
            return payload
