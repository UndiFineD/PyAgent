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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Auto-extracted class from agent_stats.py"""



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
