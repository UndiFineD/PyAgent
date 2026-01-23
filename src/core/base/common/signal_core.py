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
Core logic for signal broadcasting and pub-sub messaging.
"""

from __future__ import annotations
import logging
import queue
import threading
from typing import Any, Dict, List, Callable
from .base_core import BaseCore

logger = logging.getLogger("pyagent.signal")

class SignalCore(BaseCore):
    """
    Authoritative engine for agent signals and inter-process events.
    Standardizes subscription and broadcast logic across the swarm.
    """
    def __init__(self) -> None:
        super().__init__()
        self._subscribers: Dict[str, List[Callable[[Any, str], None]]] = {}
        self._queue: queue.Queue[Dict[str, Any]] = queue.Queue()
        self._running: bool = True
        self._thread: threading.Thread = threading.Thread(target=self._process_bus, daemon=True)
        self._thread.start()

    def subscribe(self, signal_type: str, callback: Callable[[Any, str], None]) -> None:
        """Subscribe to a specific signal type."""
        if signal_type not in self._subscribers:
            self._subscribers[signal_type] = []
        self._subscribers[signal_type].append(callback)

    def publish(self, signal_type: str, payload: Any, sender: str = "System") -> None:
        """Publish a signal to the bus."""
        self._queue.put({"type": signal_type, "payload": payload, "sender": sender})

    def _process_bus(self) -> None:
        """Background thread process for handling the signal queue."""
        while self._running:
            try:
                msg = self._queue.get(timeout=1.0)
                stype = msg["type"]
                payload = msg["payload"]
                sender = msg["sender"]

                if stype in self._subscribers:
                    for callback in self._subscribers[stype]:
                        try:
                            callback(payload, sender)
                        except Exception as err:  # pylint: disable=broad-exception-caught
                            logger.error("SignalCore: Callback failed: %s", err)
                self._queue.task_done()
            except queue.Empty:
                continue

    def stop(self) -> None:
        """Stop the signal bus processing thread."""
        self._running = False
        if self._thread.is_alive():
            self._thread.join(timeout=2.0)
