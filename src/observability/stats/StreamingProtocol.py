#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_stats.py"""

from enum import Enum


































from src.core.base.version import VERSION
__version__ = VERSION

class StreamingProtocol(Enum):
    """Protocols for real-time stats streaming."""
    WEBSOCKET = "websocket"
    SSE = "server_sent_events"
    GRPC = "grpc"
    MQTT = "mqtt"
