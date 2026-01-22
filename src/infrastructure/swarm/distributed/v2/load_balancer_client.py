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
Load Balancer Client for Phase 55.
<<<<<<< HEAD
<<<<<<< HEAD
Implements P2C (Power of Two Choices) selection and weighted round-robin for distributing
=======
Implements P2C (Power of Two Choices) selection and weighted round-robin for distributing 
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
Implements P2C (Power of Two Choices) selection and weighted round-robin for distributing 
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
requests across DP ranks.
"""

import logging
import random
<<<<<<< HEAD
<<<<<<< HEAD
from typing import Dict, List
=======
import time
from typing import Dict, List, Optional, Any
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
import time
from typing import Dict, List, Optional, Any
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
class LoadBalancerClient:
    """
    Client-side load balancer for distributing requests.
    Optimizes for peak throughput and minimum latency variance.
    """
<<<<<<< HEAD
<<<<<<< HEAD

    def __init__(self, endpoint_ranks: List[int]):
        self.ranks = endpoint_ranks
        self.stats: Dict[int, Dict[str, float]] = {r: {"load": 0.0, "latency": 0.05} for r in endpoint_ranks}

=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    
    def __init__(self, endpoint_ranks: List[int]):
        self.ranks = endpoint_ranks
        self.stats: Dict[int, Dict[str, float]] = {r: {"load": 0.0, "latency": 0.05} for r in endpoint_ranks}
        
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    def select_rank_p2c(self) -> int:
        """
        Selects a rank using the 'Power of Two Choices' algorithm.
        Reduces maximum load compared to simple round-robin.
        """
        if rc and hasattr(rc, "load_balance_select_rust"):
            return rc.load_balance_select_rust(self.ranks, [s["load"] for s in self.stats.values()])
<<<<<<< HEAD
<<<<<<< HEAD

=======
            
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
            
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        # Fallback Python P2C
        c1, c2 = random.sample(self.ranks, 2)
        load1 = self.stats[c1]["load"]
        load2 = self.stats[c2]["load"]
<<<<<<< HEAD
<<<<<<< HEAD

=======
        
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
        
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        return c1 if load1 < load2 else c2

    def update_rank_stats(self, rank_id: int, load: float, latency: float):
        """Updates internal statistics for a specific rank."""
        if rank_id in self.stats:
            self.stats[rank_id]["load"] = load
            self.stats[rank_id]["latency"] = (self.stats[rank_id]["latency"] * 0.9) + (latency * 0.1)

    def get_health_map(self) -> Dict[int, str]:
        """Returns the health status of all ranks."""
        health = {}
        for r, s in self.stats.items():
<<<<<<< HEAD
<<<<<<< HEAD
            if s["load"] > 0.95:
                health[r] = "CONGESTED"
            elif s["latency"] > 1.0:
                health[r] = "LAGGING"
            else:
                health[r] = "OK"
=======
            if s["load"] > 0.95: health[r] = "CONGESTED"
            elif s["latency"] > 1.0: health[r] = "LAGGING"
            else: health[r] = "OK"
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
            if s["load"] > 0.95: health[r] = "CONGESTED"
            elif s["latency"] > 1.0: health[r] = "LAGGING"
            else: health[r] = "OK"
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        return health
