#!/usr/bin/env python3

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations

from enum import Enum

class StreamingProtocol(Enum):
    """Protocols for real-time stats streaming."""
    WEBSOCKET = "websocket"
    SSE = "server_sent_events"
    GRPC = "grpc"
    MQTT = "mqtt"
