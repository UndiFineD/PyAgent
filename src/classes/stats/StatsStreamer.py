#!/usr/bin/env python3

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations

from .Metric import Metric
from .StreamingConfig import StreamingConfig

from datetime import datetime
from typing import List, Optional
import logging

class StatsStreamer:
    """Real-time stats streaming via WebSocket for live dashboards.

    Provides real - time metric streaming capabilities using various
    protocols for live dashboard updates.

    Attributes:
        config: Streaming configuration.
        subscribers: Active subscribers to the stream.
        buffer: Buffered metrics for batch sending.
    """

    def __init__(self, config: StreamingConfig) -> None:
        """Initialize the stats streamer.

        Args:
            config: The streaming configuration.
        """
        self.config = config
        self.subscribers: List[str] = []
        self.buffer: List[Metric] = []
        self._connected = False
        self._last_heartbeat: Optional[datetime] = None

    def connect(self) -> bool:
        """Establish connection to streaming endpoint.

        Returns:
            True if connection successful.
        """
        # Simulated connection
        self._connected = True
        self._last_heartbeat = datetime.now()
        logging.info(f"Connected to {self.config.endpoint}:{self.config.port}")
        return True

    def disconnect(self) -> None:
        """Disconnect from streaming endpoint."""
        self._connected = False
        self._last_heartbeat = None
        self.buffer.clear()

    def stream_metric(self, metric: Metric) -> bool:
        """Stream a single metric.

        Args:
            metric: The metric to stream.

        Returns:
            True if successfully streamed.
        """
        if not self._connected:
            self.buffer.append(metric)
            if len(self.buffer) >= self.config.buffer_size:
                # Buffer overflow handling
                self.buffer = self.buffer[-self.config.buffer_size // 2:]
            return False

        # Send buffered metrics first
        if self.buffer:
            self._flush_buffer()

        # Simulate streaming
        logging.debug(f"Streamed: {metric.name}={metric.value}")
        return True

    def _flush_buffer(self) -> int:
        """Flush buffered metrics.

        Returns:
            Number of metrics flushed.
        """
        count = len(self.buffer)
        self.buffer.clear()
        return count

    def add_subscriber(self, subscriber_id: str) -> None:
        """Add a subscriber to the stream.

        Args:
            subscriber_id: Unique identifier for the subscriber.
        """
        if subscriber_id not in self.subscribers:
            self.subscribers.append(subscriber_id)

    def remove_subscriber(self, subscriber_id: str) -> bool:
        """Remove a subscriber from the stream.

        Args:
            subscriber_id: The subscriber to remove.

        Returns:
            True if subscriber was removed.
        """
        if subscriber_id in self.subscribers:
            self.subscribers.remove(subscriber_id)
            return True
        return False

    def broadcast(self, metric: Metric) -> int:
        """Broadcast metric to all subscribers.

        Args:
            metric: The metric to broadcast.

        Returns:
            Number of subscribers notified.
        """
        notified = 0
        for _ in self.subscribers:
            if self.stream_metric(metric):
                notified += 1
        return notified
