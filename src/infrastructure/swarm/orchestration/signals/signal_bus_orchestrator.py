"""
Signal bus for agent-to-agent communication.
(Facade for src.core.base.common.signal_core)
"""

from src.core.base.common.signal_core import SignalCore as SignalBusOrchestrator

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
