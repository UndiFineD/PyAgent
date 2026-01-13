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
from typing import List, Dict, Any, TYPE_CHECKING

__version__ = VERSION
if TYPE_CHECKING:
    from .knowledge_engine import KnowledgeEngine

class KnowledgePruningEngine:
    """
    Implements neural-inspired pruning for agent knowledge stores (Phase 127).
    Fosters 'Anchoring Strength' by preserving frequently accessed items
    and pruning redundant or stale data to optimize performance.
    """
    def __init__(self, engine: 'KnowledgeEngine') -> None:
        self.engine = engine
        self.access_logs: Dict[str, Dict[str, Any]] = {} # id -> {"count": int, "last_access": float}

    def log_access(self, element_id: str) -> None:
        """Records an access event to an element and updates timestamps."""
        import time
        if element_id not in self.access_logs:
            self.access_logs[element_id] = {"count": 0, "first_seen": time.time()}
        
        self.access_logs[element_id]["count"] += 1
        self.access_logs[element_id]["last_access"] = time.time()

    def get_anchoring_strength(self, element_id: str) -> float:
        """
        Calculates the anchoring strength of a knowledge element (Phase 130).
        Strength = (Access Count) * exp(-decay_constant * (Current Time - Last Access))
        """
        import time
        import math
        
        log = self.access_logs.get(element_id)
        if not log:
            return 0.0
            
        decay_constant = 0.0001 # Adjustable parameter
        age = time.time() - log["last_access"]
        
        strength = log["count"] * math.exp(-decay_constant * age)
        return strength

    def run_pruning_cycle(self, strength_threshold: float = 0.5, compression_threshold: float = 2.0) -> Dict[str, List[str]]:
        """
        Executes a pruning cycle across all engine stores using anchoring strength.
        Items with strength < strength_threshold are considered candidates for eviction.
        """
        logging.info(f"KnowledgePruningEngine: Initiating neural pruning for agent {self.engine.agent_id}")
        
        pruned_report = {
            "btree": [],
            "graph": [],
            "vector": [],
            "compressed": []
        }

        # 1. Prune/Compress based on access logs (vitality)
        for element_id in list(self.access_logs.keys()):
            # Use anchoring strength instead of raw counts
            strength = self.get_anchoring_strength(element_id)
            
            # Deletion path
            if strength <= strength_threshold:
                if self.engine.btree.delete(element_id):
                    pruned_report["btree"].append(element_id)
                if self.engine.graph.delete(element_id):
                    pruned_report["graph"].append(element_id)
                del self.access_logs[element_id]
                
            # Compression path (Phase 128)
            elif strength <= compression_threshold:
                if self.engine.compress_memory(element_id):
                    pruned_report["compressed"].append(element_id)
                    # Reset access stats to allow fresh accumulation
                    self.access_logs[element_id]["count"] = 0
                    self.access_logs[element_id]["last_access"] = time.time()

        # 2. Prune Graph store for orphans (independent search)
        for node in list(self.engine.graph.nodes.keys()):
            if node not in self.engine.graph.nodes or not self.engine.graph.nodes[node]:
                self.engine.graph.delete(node)
                pruned_report["graph"].append(node)

        logging.info(f"KnowledgePruningEngine: Pruning complete. Removed {len(pruned_report['btree'])} BTree items, {len(pruned_report['graph'])} Graph nodes, Compressed {len(pruned_report['compressed'])} items.")
        return pruned_report

    def decay_weights(self, factor: float = 0.8) -> None:
        """Simulates temporal decay of knowledge. Call periodically."""
        for key in self.access_logs:
            # Note: access_logs[key] is a dict, but this legacy logic assumed it was a value.
            # We'll update the 'count' inside the dict.
            self.access_logs[key]['count'] = int(self.access_logs[key]['count'] * factor)