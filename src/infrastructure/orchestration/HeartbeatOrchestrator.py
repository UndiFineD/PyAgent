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
import time
import threading
from typing import Dict

__version__ = VERSION

class HeartbeatOrchestrator:
    """
    Ensures the swarm processes remain alive via a distributed watchdog system.
    Monitors agent health and attempts to respawn or alert on failure.
    """
    
    def __init__(self, fleet) -> None:
        self.fleet = fleet
        self.last_seen: dict[str, float] = {}
        self._running = True
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._monitor_heartbeats, daemon=True)
        self._thread.start()

    def record_heartbeat(self, agent_name: str) -> None:
        """Records a timestamp for an agent's heartbeat."""
        self.last_seen[agent_name] = time.time()
        logging.debug(f"Heartbeat: Recorded for {agent_name}")

    def _monitor_heartbeats(self) -> None:
        """Internal loop to check for dead processes."""
        while not self._stop_event.is_set():
            now = time.time()
            for agent_name, last_time in list(self.last_seen.items()):
                if now - last_time > 300:
                    # 5 minutes threshold
                    logging.warning(f"Heartbeat: Agent {agent_name} seems dead (Last seen {now - last_time:.1f}s ago)")
                    # In a real system, we'd trigger a respawn here
            self._stop_event.wait(timeout=60)

    def shutdown(self) -> None:
        self._stop_event.set()