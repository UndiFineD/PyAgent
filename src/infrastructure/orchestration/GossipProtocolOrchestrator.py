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
import asyncio
import logging
import random
import time
from typing import Any, TYPE_CHECKING
from src.core.base.version import VERSION

if TYPE_CHECKING:
    from src.infrastructure.fleet.AsyncFleetManager import AsyncFleetManager

__version__ = VERSION




class GossipProtocolOrchestrator:
    """
    Handles state synchronization across the swarm using an epidemic (gossip) protocol.
    Designed for high-scale, decentralized state consistency where nodes exchange
    knowledge digests asynchronously. (v3.3.0-GOSSIP)
    """

    def __init__(self, fleet: AsyncFleetManager) -> None:
        self.fleet = fleet
        self.state: dict[str, Any] = {}
        self.versions: dict[str, int] = {}
        self.peers: set[str] = set()
        self._lock = asyncio.Lock()
        self._running = False
        self._task: asyncio.Task | None = None

    async def start(self) -> None:
        """Starts the gossip loop."""
        if self._running:
            return
        self._running = True
        self._task = asyncio.create_task(self._gossip_loop())
        logging.info("GossipProtocolOrchestrator: Started epidemic synchronization loop.")

    async def stop(self) -> None:
        """Stops the gossip loop."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logging.info("GossipProtocolOrchestrator: Stopped gossip loop.")

    async def update_state(self, key: str, value: Any) -> None:
        """Updates local state and increments version for gossiping."""
        async with self._lock:
            self.state[key] = value
            self.versions[key] = self.versions.get(key, 0) + 1
            logging.debug(f"Gossip: Local state update [{key}] -> v{self.versions[key]}")

    async def register_peer(self, peer_name: str) -> None:
        """Registers a new peer for gossiping."""
        async with self._lock:
            self.peers.add(peer_name)

    async def _gossip_loop(self) -> None:
        """Periodically selects a random peer to synchronize state with."""
        while self._running:
            try:
                await asyncio.sleep(random.uniform(2.0, 5.0))
                if not self.peers:
                    continue

                async with self._lock:
                    peers_list = list(self.peers)

                target_peer = random.choice(peers_list)
                await self._synchronize_with_peer(target_peer)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logging.error(f"Gossip loop error: {e}")

    async def _synchronize_with_peer(self, peer_name: str) -> None:
        """
        Simulates state synchronization with a peer.
        Exchanges digests (versions) and requests missing data.
        """
        logging.debug(f"Gossip: Syncing with {peer_name}...")

        async with self._lock:
            # Randomly 'learn' something from the virtual peer to simulate convergence
            if random.random() > 0.7:
                mock_key = f"peer_{peer_name}_intel"
                new_ver = self.versions.get(mock_key, 0) + 1
                self.state[mock_key] = f"Intel from {peer_name} at {time.time()}"
                self.versions[mock_key] = new_ver
                logging.info(f"Gossip: [CONVERGENCE] Merged state for {mock_key} v{new_ver}")

    async def get_synced_state(self, key: str) -> Any | None:
        """Returns the current state for a key."""
        async with self._lock:
            return self.state.get(key)
