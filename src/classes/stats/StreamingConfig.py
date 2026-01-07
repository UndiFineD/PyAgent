#!/usr/bin/env python3

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations

from .StreamingProtocol import StreamingProtocol

from dataclasses import dataclass

@dataclass
class StreamingConfig:
    """Configuration for real-time stats streaming."""
    protocol: StreamingProtocol
    endpoint: str
    port: int = 8080
    auth_token: str = ""
    heartbeat_interval: int = 30
    reconnect_attempts: int = 3
    buffer_size: int = 1000
