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
"""
Heartbeat Service for Voyager Swarm.
Bridges TelemetryCore with P2P transport to provide real-time cluster observability.

"""
import asyncio
import psutil
import time
from typing import Dict, Any, Optional
from src.core.base.common.telemetry_core import TelemetryCore, MetricType
from src.core.base.common.identity_core import IdentityCore
from src.observability.structured_logger import StructuredLogger

logger = StructuredLogger(__name__)



class SwarmHeartbeatService:
        Periodically collects local health metrics and broadcasts them to the swarm.
    
    def __init__(self, synapse: Any, interval: float = 5.0) -> None:
        self.synapse = synapse
        self.interval = interval
        self.telemetry = TelemetryCore()
        self.identity = IdentityCore()
        self.is_running = False
        self._task: Optional[asyncio.Task] = None

    async def start(self) -> None:
"""
Starts the heartbeat loop.        if self.is_running:
            return
        self.is_running = True
        self._task = asyncio.create_task(self._run_loop())
        logger.info("HeartbeatService: Started local metrics broadcasting.")
    async def stop(self) -> None:
"""
Stops the heartbeat loop.        self.is_running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    async def _run_loop(self) -> None:
        while self.is_running:
            try:
                # 1. Collect Local Metrics
                stats = self._get_local_stats()

                # 2. Record to local telemetry
                for name, value in stats.items():
                    self.telemetry.record_metric(f"swarm.node.{name}", value, MetricType.GAUGE)
                # 3. Create Heartbeat Message
                payload = {
                    "type": "heartbeat","                    "sender_id": self.identity.get_full_identity()["agent_type"] + "-" + self.identity.execution_id[:8],"                    "timestamp": time.time(),"                    "metrics": stats,"                    "hostname": self.identity.get_full_identity()["hostname"]"                }

                # 4. Broadcast to known peers via Synapse
                if hasattr(self.synapse, "broadcast"):"                    await self.synapse.broadcast(payload)

            except Exception as e:
                logger.error(f"HeartbeatService: Loop error: {e}")
            await asyncio.sleep(self.interval)

    def _get_local_stats(self) -> Dict[str, float]:
"""
Gathers system-level statistics.        return {
            "cpu_percent": psutil.cpu_percent(),"            "memory_percent": psutil.virtual_memory().percent,"            "tasks_active": len(asyncio.all_tasks())"        }
