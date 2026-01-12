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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Auto-extracted class from agent_stats.py"""



from .StatsStream import StatsStream
from .StreamingConfig import StreamingConfig

from typing import Any, Callable, Dict, List, Optional



































class StatsStreamManager:
    """Manages real-time stats streaming."""
    def __init__(self, config: Optional[StreamingConfig] = None) -> None:
        self.config = config
        self.streams: Dict[str, StatsStream] = {}
        self.subscribers: Dict[str, List[Callable[[Any], None]]] = {}

    def create_stream(self, name: str, buffer_size: int = 1000) -> StatsStream:
        """Create a new stream."""
        stream = StatsStream(name=name, buffer_size=buffer_size)
        self.streams[name] = stream
        self.subscribers[name] = []
        return stream

    def get_latest(self, name: str, count: int = 1) -> List[Any]:
        """Get latest data from stream."""
        if name not in self.streams:
            return []
        return self.streams[name].get_latest(count)

    def subscribe(self, stream_name: str, callback: Callable[[Any], None]) -> None:
        """Subscribe to stream updates."""
        if stream_name not in self.subscribers:
            self.subscribers[stream_name] = []
        self.subscribers[stream_name].append(callback)

    def publish(self, stream_name: str, data: Any) -> None:
        """Publish data to stream."""
        if stream_name in self.streams:
            self.streams[stream_name].add_data(data)

        # Notify subscribers
        if stream_name in self.subscribers:
            for callback in self.subscribers[stream_name]:
                try:
                    callback(data)
                except Exception:
                    logging.debug(f"Stream subscriber for {stream_name} failed.")
