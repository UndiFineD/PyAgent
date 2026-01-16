#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Real-time stats streaming engine.

from __future__ import annotations
import logging
from typing import Any, Callable
from .Metrics import Metric
from .ObservabilityCore import StreamingConfig

logger = logging.getLogger(__name__)


class StatsStream:
    """Represents a real-time stats stream."""

    def __init__(self, name: str, buffer_size: int = 1000) -> None:
        self.name = name

        self.buffer_size = buffer_size

        self.buffer: list[Any] = []

    def get_latest(self, count: int = 1) -> list[Any]:
        return self.buffer[-count:]

    def add_data(self, data: Any) -> None:
        self.buffer.append(data)
        if len(self.buffer) > self.buffer_size:
            self.buffer.pop(0)


class StatsStreamManager:
    """Manages real-time stats streaming."""

    def __init__(self, config: StreamingConfig | None = None) -> None:
        self.config = config
        self.streams: dict[str, StatsStream] = {}
        self.subscribers: dict[str, list[Callable[[Any], None]]] = {}

    def create_stream(self, name: str, buffer_size: int = 1000) -> StatsStream:
        s = StatsStream(name, buffer_size)
        self.streams[name] = s
        return s

    def publish(self, name: str, data: Any) -> None:
        if name in self.streams:
            self.streams[name].add_data(data)
        for cb in self.subscribers.get(name, []):
            try:
                cb(data)
            except Exception:
                pass

    def subscribe(self, name: str, callback: Callable[[Any], None]) -> None:
        self.subscribers.setdefault(name, []).append(callback)


class StatsStreamer:
    """Real-time stats streaming via WebSocket (simulated)."""

    def __init__(self, config: StreamingConfig) -> None:
        self.config = config
        self.subscribers: list[str] = []
        self.buffer: list[Metric] = []
        self._connected = False

    def connect(self) -> bool:
        self._connected = True
        return True

    def disconnect(self) -> None:
        self._connected = False

    def stream_metric(self, metric: Metric) -> bool:
        if not self._connected:
            self.buffer.append(metric)
            if len(self.buffer) > self.config.buffer_size:
                self.buffer.pop(0)
            return False
        return True

    def broadcast(self, metric: Metric) -> int:
        return len(self.subscribers) if self.stream_metric(metric) else 0

    def add_subscriber(self, subscriber_id: str) -> None:
        if subscriber_id not in self.subscribers:
            self.subscribers.append(subscriber_id)

    def remove_subscriber(self, subscriber_id: str) -> None:
        if subscriber_id in self.subscribers:
            self.subscribers.remove(subscriber_id)
