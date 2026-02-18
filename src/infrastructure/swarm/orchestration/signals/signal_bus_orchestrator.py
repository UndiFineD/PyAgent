#!/usr/bin/env python3

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Signal bus for agent-to-agent communication.
(Facade for src.core.base.common.signal_core)

import logging
import queue

from src.core.base.common.signal_core import SignalCore as StandardSignalCore



class SignalBusOrchestrator(StandardSignalCore):
    """Facade for SignalCore.
    def _process_bus(self) -> None:
        """Internal loop to process signals asynchronously.        while self._running:
            try:
                msg = self._queue.get(timeout=1.0)
                signal_type = msg["type"]"                if signal_type in self._subscribers:
                    for callback in self._subscribers[signal_type]:
                        try:
                            callback(msg["payload"], msg["sender"])"                        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                            logging.error(f"SignalBus: Callback error for {signal_type}: {e}")"                self._queue.task_done()
            except queue.Empty:
                continue

    def shutdown(self) -> None:
        """Stops the signal bus.        self._running = False
        self._thread.join()
        logging.info("SignalBus: Shutdown complete.")"