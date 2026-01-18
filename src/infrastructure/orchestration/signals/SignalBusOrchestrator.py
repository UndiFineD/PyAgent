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
from src.core.base.Version import VERSION
import logging
import queue
import threading
from typing import Any
from collections.abc import Callable

__version__ = VERSION


class SignalBusOrchestrator:
    """
    High-speed signal bus for low-latency agent-to-agent communication.
    Uses an internal message queue and a pub-sub pattern to bypass slow JSON/HTTP overhead.
    """

    def __init__(self) -> None:
        self._subscribers: dict[str, list[Callable[[Any, str], None]]] = {}
        self._queue: queue.Queue[dict[str, Any]] = queue.Queue()
        self._running: bool = True
        self._thread: threading.Thread = threading.Thread(target=self._process_bus, daemon=True)
        self._thread.start()

    def subscribe(self, signal_type: str, callback: Callable[[Any, str], None]) -> None:
        """Registers a callback for a specific signal type."""
        if signal_type not in self._subscribers:
            self._subscribers[signal_type] = []
        self._subscribers[signal_type].append(callback)
        logging.debug(f"SignalBus: Subscribed to '{signal_type}'")

    def publish(self, signal_type: str, payload: Any, sender: str = "System") -> None:
        """Publishes a signal to the bus."""
        self._queue.put({"type": signal_type, "payload": payload, "sender": sender})

    def _process_bus(self) -> None:
        """Internal loop to process signals asynchronously."""
        while self._running:
            try:
                msg = self._queue.get(timeout=1.0)
                signal_type = msg["type"]
                if signal_type in self._subscribers:
                    for callback in self._subscribers[signal_type]:
                        try:
                            callback(msg["payload"], msg["sender"])
                        except Exception as e:
                            logging.error(
                                f"SignalBus: Callback error for {signal_type}: {e}"
                            )
                self._queue.task_done()
            except queue.Empty:
                continue

    def shutdown(self) -> None:
        """Stops the signal bus."""
        self._running = False
        self._thread.join()
        logging.info("SignalBus: Shutdown complete.")
