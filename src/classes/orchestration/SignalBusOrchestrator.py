#!/usr/bin/env python3

import logging
import json
import queue
import threading
from typing import Dict, List, Any, Optional, Callable

class SignalBusOrchestrator:
    """
    High-speed signal bus for low-latency agent-to-agent communication.
    Uses an internal message queue and a pub-sub pattern to bypass slow JSON/HTTP overhead.
    """
    
    def __init__(self) -> None:
        self._subscribers: Dict[str, List[Callable]] = {}
        self._queue = queue.Queue()
        self._running = True
        self._thread = threading.Thread(target=self._process_bus, daemon=True)
        self._thread.start()

    def subscribe(self, signal_type: str, callback: Callable):
        """Registers a callback for a specific signal type."""
        if signal_type not in self._subscribers:
            self._subscribers[signal_type] = []
        self._subscribers[signal_type].append(callback)
        logging.debug(f"SignalBus: Subscribed to '{signal_type}'")

    def publish(self, signal_type: str, payload: Any, sender: str = "System"):
        """Publishes a signal to the bus."""
        self._queue.put({"type": signal_type, "payload": payload, "sender": sender})

    def _process_bus(self):
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
                            logging.error(f"SignalBus: Callback error for {signal_type}: {e}")
                self._queue.task_done()
            except queue.Empty:
                continue

    def shutdown(self):
        """Stops the signal bus."""
        self._running = False
        self._thread.join()
        logging.info("SignalBus: Shutdown complete.")
