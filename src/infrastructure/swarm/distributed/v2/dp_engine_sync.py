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
Data Parallel Engine Sync for Phase 55.
Manages engine state transitions across multiple DP ranks to ensure wave coherence.
"""

import asyncio
import logging
from enum import Enum
from typing import Dict

try:
    import rust_core as rc
except ImportError:
    rc = None

logger = logging.getLogger(__name__)


class SyncState(Enum):
    READY = 0
    WAVE_RUNNING = 1
    WAVE_COMPLETE = 2
    PAUSED = 3


class DPEngineSync:
    """
    Ensures all DP ranks are synchronized before starting or ending a request wave.
    """

    def __init__(self, rank: int, world_size: int):
        self.rank = rank
        self.world_size = world_size
        self.state = SyncState.READY
        self.ready_map: Dict[int, bool] = {i: False for i in range(world_size)}

    def mark_ready(self, rank_id: int):
        """Marks a rank as ready for the next wave."""
        self.ready_map[rank_id] = True

    def all_ready(self) -> bool:
        """Checks if all ranks in the world have signaled readiness."""
        if rc and hasattr(rc, "wave_sync_check_rust"):
            # Efficient bitmask check
            return rc.wave_sync_check_rust(list(self.ready_map.values()))

        return all(self.ready_map.values())

    def reset_ready(self):
        """Resets readiness for the next synchronization point."""
        for i in range(self.world_size):
            self.ready_map[i] = False
        self.state = SyncState.READY

    async def wait_for_barrier(self, timeout: float = 5.0):
        """
        Non-blocking barrier wait. In a real system, this would involve
        nccl/zmq communication.
        """
        start_time = asyncio.get_event_loop().time()
        while not self.all_ready():
            if asyncio.get_event_loop().time() - start_time > timeout:
                logger.warning(f"Rank {self.rank} timed out waiting for barrier")
                return False
            await asyncio.sleep(0.01)
        return True
