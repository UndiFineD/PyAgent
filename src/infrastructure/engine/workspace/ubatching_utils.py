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
Micro-batching (UBatching) utilities for Phase 52.
Optimizes execution by slicing larger batches into hardware-aligned segments.
"""

import logging
<<<<<<< HEAD
<<<<<<< HEAD
from typing import Any, Dict, List
=======
from typing import List, Any, Optional, Dict
import time
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
from typing import List, Any, Optional, Dict
import time
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
class UBatchingUtils:
    """
    Low-level utilities for micro-batch (UBatch) decomposition and coordination.
    Essential for 120fps synchronized multimodal pipelines.
    """
<<<<<<< HEAD
<<<<<<< HEAD

    def __init__(self) -> None:
        self._stats: Dict[str, Any] = {"total_slices": 0, "avg_slice_size": 0.0, "sync_count": 0}
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    
    def __init__(self):
        self._stats: Dict[str, Any] = {
            "total_slices": 0,
            "avg_slice_size": 0.0,
            "sync_count": 0
        }
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

    @staticmethod
    def slice_batch(batch: List[Any], min_slice: int = 4) -> List[List[Any]]:
        """
        Slices a batch into micro-batches for concurrent processing.
        """
<<<<<<< HEAD
<<<<<<< HEAD
        return [batch[i : i + min_slice] for i in range(0, len(batch), min_slice)]
=======
        return [batch[i:i + min_slice] for i in range(0, len(batch), min_slice)]
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
        return [batch[i:i + min_slice] for i in range(0, len(batch), min_slice)]
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

    @staticmethod
    def compute_optimal_slices(total_tokens: int, num_sms: int = 80) -> List[int]:
        """
        Calculates the optimal micro-batch sizes to saturate hardware SMs.
        """
        if rc and hasattr(rc, "ubatch_slice_optimal_rust"):
            return rc.ubatch_slice_optimal_rust(total_tokens, num_sms)
<<<<<<< HEAD
<<<<<<< HEAD

=======
            
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
            
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        # Fallback: Simple uniform slicing
        slice_size = max(1, total_tokens // num_sms)
        return [slice_size] * (total_tokens // slice_size)

    @staticmethod
<<<<<<< HEAD
<<<<<<< HEAD
    def coordinate_threads(thread_id: int, total_threads: int) -> None:
=======
    def coordinate_threads(thread_id: int, total_threads: int):
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
    def coordinate_threads(thread_id: int, total_threads: int):
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        """
        Ensures strict thread ordering for DBO access within a UBatch.
        """
        if rc and hasattr(rc, "ubatch_thread_wait_rust"):
            rc.ubatch_thread_wait_rust(thread_id, total_threads)
        else:
            # Emulated wait
<<<<<<< HEAD
<<<<<<< HEAD
            import threading
            threading.Event().wait(0.001 * (thread_id / total_threads))
=======
            time.sleep(0.001 * (thread_id / total_threads))
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
            time.sleep(0.001 * (thread_id / total_threads))
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

    def get_ubatch_metrics(self) -> Dict[str, Any]:
        """Returns micro-batching performance metrics."""
        if rc and hasattr(rc, "ubatch_get_stats_rust"):
            return rc.ubatch_get_stats_rust()
        return self._stats
