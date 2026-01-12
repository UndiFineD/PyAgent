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



import logging
import random
import time
import threading
from typing import Dict, List, Any, Optional, Set

class GossipProtocolOrchestrator:
    """
    Handles state synchronization across the swarm using an epidemic (gossip) protocol.
    Designed for high-scale, decentralized state consistency where some nodes might be offline.
    """
    
    def __init__(self, fleet) -> None:
        self.fleet = fleet
        self.state: Dict[str, Any] = {}
        self.versions: Dict[str, int] = {}
        self.peers: Set[str] = set()
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._gossip_thread = threading.Thread(target=self._gossip_loop, daemon=True)
        self._gossip_thread.start()

    def update_state(self, key: str, value: Any) -> None:
        """Updates local state and increments version for gossiping."""
        with self._lock:
            self.state[key] = value
            self.versions[key] = self.versions.get(key, 0) + 1
            logging.info(f"Gossip: Local state update [{key}] version {self.versions[key]}")

    def register_peer(self, peer_name: str) -> None:
        """Registers a new peer for gossiping."""
        with self._lock:
            self.peers.add(peer_name)

    def _gossip_loop(self) -> None:
        """Periodically selects a random peer to synchronize state with."""
        while not self._stop_event.is_set():
            if self.peers:
                target_peer = random.choice(list(self.peers))
                self._synchronize_with_peer(target_peer)
            self._stop_event.wait(timeout=random.uniform(1.0, 5.0))

    def _synchronize_with_peer(self, peer_name: str) -> None:
        """
        Simulates state synchronization with a peer.
        In a real implementation, this would involve network calls.
        """
        logging.debug(f"Gossip: Synchronizing state with peer {peer_name}")
        # In reality, we'd exchange (key, version) pairs and pull/push missing data
        pass

    def get_synced_state(self, key: str) -> Optional[Any]:
        """Returns the current state for a key."""
        with self._lock:
            return self.state.get(key)

    def shutdown(self) -> None:
        self._stop_event.set()
