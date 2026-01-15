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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

from __future__ import annotations
from src.core.base.version import VERSION
import logging
import threading
from typing import Any

__version__ = VERSION




class EntanglementOrchestrator:
    """
    Manages instantaneous state synchronization across distributed agent nodes.
    Ensures that high-priority state changes in one node are mirrored to all entangled peers.
    """

    def __init__(self, fleet) -> None:
        self.fleet = fleet
        self.signal_bus = fleet.signal_bus
        self.shared_state: dict[str, Any] = {}
        self._lock = threading.Lock()

        # Subscribe to entanglement sync signals
        self.signal_bus.subscribe("entanglement_sync", self._handle_sync_signal)

    def update_state(self, key: str, value: Any, propagate: bool = True) -> None:
        """Updates local state and optionally propagates to the swarm."""
        with self._lock:
            self.shared_state[key] = value
            logging.debug(f"Entanglement: Local state update {key}={value}")

        if propagate:
            self.signal_bus.publish("entanglement_sync", {"key": key, "value": value}, sender="EntanglementOrchestrator")

    def get_state(self, key: str) -> Any:
        """Retrieves an entangled state value."""
        with self._lock:
            return self.shared_state.get(key)

    def _handle_sync_signal(self, payload: Any, sender: str) -> None:
        """Internal handler for incoming state synchronization signals."""
        if sender == "EntanglementOrchestrator":
            return  # Ignore local propagation

        key = payload.get("key")
        value = payload.get("value")

        if key is not None:
            with self._lock:
                self.shared_state[key] = value
                logging.info(f"Entanglement: Synced state from {sender}: {key}={value}")

    def get_all_state(self) -> dict[str, Any]:
        """Returns the entire entangled state snapshot."""
        with self._lock:
            return self.shared_state.copy()
