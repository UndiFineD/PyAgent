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
Multi-Channel MUXer for high-speed (120fps) multimodal I/O.
Synchronizes separate channels for video, audio, and text.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

try:
    import rust_core as rc
except ImportError:
    rc = None

logger = logging.getLogger("pyagent.multimodal.muxer")


class ChannelType(Enum):
    """Enumeration of supported modality channel types."""
    TEXT = 0x01
    AUDIO = 0x02
    VIDEO = 0x03
    COMMAND = 0x04


@dataclass
class ModalityChannel:
    """Configuration for a specific modality streaming channel."""
    name: str
    modality_type: str
    fps: float = 120.0
    buffer_size: int = 1024


class Muxer:
    """
    Coordinates multiple high-speed modality channels.
    Supports "DVD-style" separate streams for video, audio, and text.
    """

    def __init__(self, target_fps: float = 120.0) -> None:
        self.target_fps = target_fps
        self.channels: Dict[str, ModalityChannel] = {}
        self.active = False

    def synchronize_tick(self, audio: bytes, video: bytes, text: str) -> bytes:
        """
        Packs separate modalities into a single sync-packet for 120fps DVD-like streaming.
        Uses 0xDEADBEEF binary muxer.
        """
        packets = [
            {"channel_id": 1, "modality_type": "VIDEO", "payload": video},
            {"channel_id": 2, "modality_type": "AUDIO", "payload": audio},
            {"channel_id": 3, "modality_type": "TEXT", "payload": text.encode("utf-8")},
        ]
        return self.mux(packets)

    def add_channel(self, name: str, m_type: str, fps: Optional[float] = None) -> None:
        """Register a new modality channel."""
        self.channels[name] = ModalityChannel(name=name, modality_type=m_type, fps=fps or self.target_fps)
        logger.info(f"Registered channel: {name} ({m_type}) at {fps or self.target_fps} fps")

    def mux(self, raw_packets: List[Dict[str, Any]]) -> bytes:
        """
        Mux multiple inputs into a binary stream.
        """
        if rc and hasattr(rc, "mux_channels_rust") and hasattr(rc, "ModalityPacket"):
            packets = []
            for p in raw_packets:
                packets.append(
                    rc.ModalityPacket(
                        p["channel_id"], p["modality_type"], p.get("timestamp", time.time()), p["payload"]
                    )
                )
            return bytes(rc.mux_channels_rust(packets))

        # Fallback (Slow)
        # 0xDEADBEEF Magic Header for synchronization
        header = b"\xef\xbe\xad\xde"
        return header + b"".join([p["payload"] for p in raw_packets])

    def demux(self, stream_data: bytes) -> List[Dict[str, Any]]:
        """
        Demux a binary stream into individual channel packets.
        """
        if rc and hasattr(rc, "demux_channels_rust"):
            packets = rc.demux_channels_rust(list(stream_data))
            return [
                {
                    "channel_id": p.channel_id,
                    "modality_type": p.modality_type,
                    "timestamp": p.timestamp,
                    "payload": p.payload,
                }
                for p in packets
            ]

        return []

    def synchronize(self, packets: List[Dict[str, Any]], jitter_ms: float = 8.33) -> Dict[int, List[Dict[str, Any]]]:
        """
        Synchronize packets across channels using a jitter window.
        8.33ms = 1 frame at 120fps.
        """
        if rc and hasattr(rc, "synchronize_channels_rust") and hasattr(rc, "ModalityPacket"):
            rust_packets = []
            for p in packets:
                rust_packets.append(
                    rc.ModalityPacket(p["channel_id"], p["modality_type"], p["timestamp"], p["payload"])
                )

            result = rc.synchronize_channels_rust(rust_packets, jitter_ms)

            # Convert back to Python dicts
            sync_map = {}
            for bucket, p_list in result.items():
                sync_map[bucket] = [
                    {
                        "channel_id": p.channel_id,
                        "modality_type": p.modality_type,
                        "timestamp": p.timestamp,
                        "payload": p.payload,
                    }
                    for p in p_list
                ]
            return sync_map

        # Basic Python fallback (simplified)
        sync_map = {}
        window = jitter_ms / 1000.0
        for p in packets:
            bucket = int(p["timestamp"] / window)
            if bucket not in sync_map:
                sync_map[bucket] = []
            sync_map[bucket].append(p)
        return sync_map
