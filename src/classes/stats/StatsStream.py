#!/usr/bin/env python3

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations

from typing import Any, List

class StatsStream:
    """Represents a real-time stats stream."""
    def __init__(self, name: str, buffer_size: int = 1000) -> None:
        self.name = name
        self.buffer_size = buffer_size
        self.buffer: List[Any] = []
        self.active = True

    def get_latest(self, count: int = 1) -> List[Any]:
        """Get latest data points."""
        return self.buffer[-count:] if self.buffer else []

    def add_data(self, data: Any) -> None:
        """Add data to stream."""
        self.buffer.append(data)
        # Enforce buffer size limit
        if len(self.buffer) > self.buffer_size:
            self.buffer.pop(0)
