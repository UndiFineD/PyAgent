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
Advanced Asynchronous Request Queue (V2) for Phase 54.
Supports priority, deadlines, and fair-share policies with Rust acceleration.
"""

<<<<<<< HEAD
<<<<<<< HEAD
import heapq
import logging
import time
from typing import Any, Dict, List, Tuple

from src.infrastructure.engine.scheduling.advanced.config import RequestPriority
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
import logging
import heapq
import time
from typing import Dict, List, Optional, Any, Tuple
from ...scheduling.advanced.config import RequestPriority
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

try:
    import rust_core as rc
except ImportError:
    rc = None

logger = logging.getLogger(__name__)

<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
class RequestQueueV2:
    """
    Priority-based async queue for inference requests.
    Uses deadline-aware scheduling and fair-share policies.
    """
<<<<<<< HEAD
<<<<<<< HEAD

    def __init__(self) -> None:
        self._waiting: List[Tuple[float, int, Any]] = []  # (priority_score, timestamp, request)
        self._running: Dict[int, Any] = {}
        self._counter = 0

    def add_request(self, request: Any) -> None:
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    
    def __init__(self):
        self._waiting: List[Tuple[float, int, Any]] = [] # (priority_score, timestamp, request)
        self._running: Dict[int, Any] = {}
        self._counter = 0
        
    def add_request(self, request: Any):
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        """
        Calculates priority and adds request to the waiting queue.
        Uses Rust for high-speed priority calculation if available.
        """
<<<<<<< HEAD
<<<<<<< HEAD
        priority = getattr(request, "priority", RequestPriority.NORMAL)
        deadline = getattr(request, "deadline", time.time() + 60.0)

=======
        priority = getattr(request, 'priority', RequestPriority.NORMAL)
        deadline = getattr(request, 'deadline', time.time() + 60.0)
        
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
        priority = getattr(request, 'priority', RequestPriority.NORMAL)
        deadline = getattr(request, 'deadline', time.time() + 60.0)
        
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        score = 0.0
        if rc and hasattr(rc, "request_priority_compute_rust"):
            score = rc.request_priority_compute_rust(int(priority.value), deadline)
        else:
            # Fallback priority scoring
            urgency = max(0, deadline - time.time())
            score = float(priority.value) - (1.0 / (urgency + 1e-6))
<<<<<<< HEAD
<<<<<<< HEAD

=======
            
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
            
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        self._counter += 1
        heapq.heappush(self._waiting, (score, self._counter, request))
        logger.debug(f"Added request {getattr(request, 'request_id', 'unknown')} with score {score:.4f}")

    def pop_next_batch(self, max_tokens: int) -> List[Any]:
        """
        Pops the highest priority requests that fit within max_tokens.
        """
        batch = []
        current_tokens = 0
<<<<<<< HEAD
<<<<<<< HEAD

        # Temporary storage for requests that don't fit
        skipped = []

        while self._waiting and current_tokens < max_tokens:
            score, count, req = heapq.heappop(self._waiting)
            req_tokens = getattr(req, "num_tokens", 1)

=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        
        # Temporary storage for requests that don't fit
        skipped = []
        
        while self._waiting and current_tokens < max_tokens:
            score, count, req = heapq.heappop(self._waiting)
            req_tokens = getattr(req, 'num_tokens', 1)
            
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
            if current_tokens + req_tokens <= max_tokens:
                batch.append(req)
                current_tokens += req_tokens
            else:
                skipped.append((score, count, req))
                # If it's a priority queue, we might stop here or keep looking for smaller requests
                # For Phase 54 we continue to look for smaller requests to maximize utilization
<<<<<<< HEAD
<<<<<<< HEAD

        # Push skipped back
        for item in skipped:
            heapq.heappush(self._waiting, item)

=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
                
        # Push skipped back
        for item in skipped:
            heapq.heappush(self._waiting, item)
            
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        return batch

    def get_queue_stats(self) -> Dict[str, Any]:
        """Returns statistics on queue depth and urgency."""
        if not self._waiting:
            return {"depth": 0, "max_urgency": 0.0}
<<<<<<< HEAD
<<<<<<< HEAD

        max_urgency = 0.0
        if rc and hasattr(rc, "deadline_urgency_rust"):
            deadlines = [getattr(r[2], "deadline", 0) for r in self._waiting]
            max_urgency = rc.deadline_urgency_rust(deadlines)

        return {"depth": len(self._waiting), "max_urgency": max_urgency, "running_count": len(self._running)}
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
            
        max_urgency = 0.0
        if rc and hasattr(rc, "deadline_urgency_rust"):
            deadlines = [getattr(r[2], 'deadline', 0) for r in self._waiting]
            max_urgency = rc.deadline_urgency_rust(deadlines)
            
        return {
            "depth": len(self._waiting),
            "max_urgency": max_urgency,
            "running_count": len(self._running)
        }
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
