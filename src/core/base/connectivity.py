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
Modern connectivity module providing high-performance binary transport.
Supports MessagePack for serialization and Zstd for compression (Phase 255).
"""

from __future__ import annotations
import msgpack
import zstd
import logging
from typing import Any
from src.core.base.version import VERSION

__version__ = VERSION
logger = logging.getLogger(__name__)







class BinaryTransport:
    """
    Handles binary serialization and compression for agent communication.
    Utilizes MessagePack and Zstd for optimal performance.
    """

    @staticmethod
    def pack(data: Any, compress: bool = False, level: int = 3) -> bytes:
        """
        Serializes data using MessagePack and optionally compresses with Zstd.

        Args:
            data: The data to serialize.
            compress: Whether to apply Zstd compression.
            level: Zstd compression level (1-22).

        Returns:
            bytes: The packed (and possibly compressed) data.
        """
        try:
            packed = msgpack.packb(data, use_bin_type=True)
            if compress:
                return zstd.compress(packed, level)
            return packed
        except Exception as e:
            logger.error(f"BinaryTransport.pack failed: {e}")
            raise











    @staticmethod
    def unpack(payload: bytes, compressed: bool = False) -> Any:



        """
        Decompresses (optionally) and deserializes data using MessagePack.

        Args:

            payload: The bytes to unpack.
            compressed: Whether the payload is Zstd compressed.

        Returns:
            Any: The unpacked data.


        """
        try:
            data = payload
            if compressed:
                data = zstd.decompress(payload)




            return msgpack.unpackb(data, raw=False)
        except Exception as e:
            logger.error(f"BinaryTransport.unpack failed: {e}")
            raise





class HeartbeatSignal:
    """
    Specialized structure for high-frequency heartbeat signals.
    Optimized for BinaryTransport.
    """
    def __init__(self, agent_id: str, status: str, load: float = 0.0) -> None:
        self.agent_id = agent_id
        self.status = status
        self.load = load
        self.timestamp = __import__("time").time()

    def to_dict(self) -> dict:
        return {
            "a": self.agent_id,
            "s": self.status,
            "l": self.load,
            "t": self.timestamp
        }

    @classmethod
    def from_dict(cls, data: dict) -> HeartbeatSignal:
        signal = cls(data["a"], data["s"], data.get("l", 0.0))
        signal.timestamp = data.get("t", 0.0)
        return signal
