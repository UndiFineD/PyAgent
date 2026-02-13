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
streaming.py - Real-time stats streaming engine

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Use StatsStream to hold recent events for a named stream: s = StatsStream("name"); s.add_data(obj); s.get_latest(10)
- Use StatsStreamManager to create/manage streams and subscribers: m = StatsStreamManager(config); m.create_stream("x"); m.subscribe("x", callback); m.publish("x", data)
- Use StatsStreamer for WebSocket-like metric buffering/broadcasting: st = StatsStreamer(config); st.connect(); st.add_subscriber("client1"); st.broadcast(metric)

WHAT IT DOES:
- Provides lightweight in-memory buffering for named real-time statistic streams (StatsStream, StatsStreamManager).
- Allows registration of callbacks to receive published stream data and safely suppresses subscriber exceptions.
- Simulates a WebSocket-style metric streamer (StatsStreamer) with connect/disconnect, buffered writes when disconnected, and simple subscriber counting for broadcasts.

WHAT IT SHOULD DO BETTER:
- Add thread-safety / asyncio support so producers and consumers can run concurrently without races.
- Replace synchronous callbacks with async-compatible interfaces and backpressure handling for slow consumers.
- Persist or checkpoint buffers (or expose pluggable storage) to avoid data loss on restart; implement reconnection replay for StatsStreamer.
- Improve typing (narrow Any), add docstrings to every public method, and increase observability (structured logging, metrics about drops).
- Add unit tests covering subscriber exception handling, buffer overflow behavior, and broadcast semantics under load.

FILE CONTENT SUMMARY:
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
Streaming.py module.
"""
# Real-time stats streaming engine.

from __future__ import annotations

import contextlib
import logging
from typing import Any, Callable

from .metrics import Metric
from .observability_core import StreamingConfig

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
            with contextlib.suppress(Exception):
                cb(data)

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
"""
# Real-time stats streaming engine.

from __future__ import annotations

import contextlib
import logging
from typing import Any, Callable

from .metrics import Metric
from .observability_core import StreamingConfig

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
            with contextlib.suppress(Exception):
                cb(data)

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
