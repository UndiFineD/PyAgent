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
Data Parallel Coordinator (V2) for Phase 55.
Handles ZMQ-based request coordination, wave tracking, and stats publishing.
"""

import logging
import json
import time
from typing import Dict, List, Optional, Any
import zmq
import zmq.asyncio
from .locality_manager import LocalityManager

try:
    import rust_core as rc
except ImportError:
    rc = None

logger = logging.getLogger(__name__)

class DPCoordinatorV2:
    """
    Coordinates inference requests across multiple data-parallel (DP) ranks.
    Uses ZMQ for low-latency state distribution and wave tracking.
    """
    
    def __init__(self, port: int = 5555, is_master: bool = False):
        self.port = port
        self.is_master = is_master
        self.ctx = zmq.asyncio.Context()
        self.socket = self.ctx.socket(zmq.PUB if is_master else zmq.SUB)
        
        self.current_wave = 0
        self.rank_stats: Dict[int, Any] = {}
        self.locality = LocalityManager()
        
        if not is_master:
            self.socket.setsockopt(zmq.SUBSCRIBE, b"")

    async def connect(self, host: str = "localhost"):
        """Connects or binds the ZMQ socket."""
        addr = f"tcp://{host}:{self.port}"
        if self.is_master:
            self.socket.bind(addr)
            logger.info(f"DP Master bound to {addr}")
        else:
            self.socket.connect(addr)
            logger.info(f"DP Worker connected to {addr}")

    async def publish_wave(self, request_ids: List[int]):
        """
        Publishes a new request wave to all active workers.
        """
        if not self.is_master:
            return
            
        self.current_wave += 1
        message = {
            "type": "NEW_WAVE",
            "wave_id": self.current_wave,
            "request_ids": request_ids,
            "timestamp": time.time()
        }
        await self.socket.send_json(message)
        logger.debug(f"Published Wave {self.current_wave} with {len(request_ids)} requests")

    async def publish_wave_to_locality(self, request_ids: List[int], locality_tag: str):
        """
        Phase 59: Targets a specific locality for a wave to reduce inter-rack traffic.
        """
        if not self.is_master:
            return
            
        self.current_wave += 1
        message = {
            "type": "LOCALITY_WAVE",
            "wave_id": self.current_wave,
            "request_ids": request_ids,
            "locality": locality_tag,
            "timestamp": time.time()
        }
        await self.socket.send_json(message)
        logger.info(f"Published Locality Wave {self.current_wave} to {locality_tag}")

    async def receive_update(self) -> Optional[Dict[str, Any]]:
        """Receives a wave update or status message."""
        if self.is_master:
            return None
            
        try:
            msg = await self.socket.recv_json()
            if msg.get("type") == "NEW_WAVE":
                self.current_wave = msg["wave_id"]
            return msg
        except Exception as e:
            logger.error(f"ZMQ Receive failed: {e}")
            return None

    def aggregate_stats(self) -> Dict[str, Any]:
        """
        Aggregates performance stats across all ranks using Rust for speed.
        """
        if rc and hasattr(rc, "dp_stats_aggregate_rust"):
            return rc.dp_stats_aggregate_rust(self.rank_stats)
            
        # Fallback basic aggregation
        if not self.rank_stats:
            return {}
            
        avg_latency = sum(s.get("latency", 0) for s in self.rank_stats.values()) / len(self.rank_stats)
        return {
            "avg_latency": avg_latency,
            "total_throughput": sum(s.get("throughput", 0) for s in self.rank_stats.values()),
            "wave_count": self.current_wave
        }

    async def close(self):
        """Closes the socket and context."""
        self.socket.close()
        self.ctx.term()
        logger.info("DPCoordinator ZMQ context terminated")
