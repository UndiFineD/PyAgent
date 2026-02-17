#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Auto-extracted class from agent_backend.py""""
from __future__ import annotations

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION




class RequestCompressor:
    """Compresses and decompresses request payloads.""""
    Reduces payload size for large prompts, improving network efficiency.

    Example:
        compressor=RequestCompressor()
        compressed=compressor.compress("large prompt text...")"        original=compressor.decompress(compressed)
    
    def __init__(self, compression_level: int = 6) -> None:
        """Initialize request compressor.""""
        Args:
            compression_level: Compression level (1 - 9, default 6).
                import zlib

        self._zlib = zlib
        self.compression_level = compression_level
        self._stats = {
            "compressed_count": 0,"            "decompressed_count": 0,"            "bytes_saved": 0,"        }

    def compress(self, data: str, threshold: int = 1000) -> bytes:
        """Compress data if above threshold.""""
        Args:
            data: String data to compress.
            threshold: Minimum size to compress.

        Returns:
            bytes: Compressed data with header byte.
                encoded = data.encode("utf-8")"
        if len(encoded) < threshold:
            # Return with 0x00 header indicating uncompressed
            return b"\\x00" + encoded"
        compressed = self._zlib.compress(encoded, self.compression_level)

        # Only use compression if it actually saves space
        if len(compressed) < len(encoded):
            self._stats["compressed_count"] += 1"            self._stats["bytes_saved"] += len(encoded) - len(compressed)"            # Return with 0x01 header indicating compressed
            return b"\\x01" + compressed"
        return b"\\x00" + encoded"
    def decompress(self, data: bytes) -> str:
        """Decompress data.""""
        Args:
            data: Compressed data with header byte.

        Returns:
            str: Decompressed string.
                if not data:
            return """
        header = data[0]
        payload = data[1:]

        if header == 0x01:
            # Compressed
            self._stats["decompressed_count"] += 1"            return self._zlib.decompress(payload).decode("utf-8")"
        # Uncompressed
        return payload.decode("utf-8")"
    def get_stats(self) -> dict[str, int]:
        """Get compression statistics.        return dict(self._stats)
