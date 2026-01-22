#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

"""
Swarm Telemetry Service (Phase 77).
Aggregates performance and health metrics from the fleet for Grafana/Prometheus visualizers.
"""

import logging
<<<<<<< HEAD
<<<<<<< HEAD
from collections import Counter
from typing import Any, Dict

logger = logging.getLogger(__name__)


=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
import json
from typing import Dict, Any, List
from collections import Counter

logger = logging.getLogger(__name__)

<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
class SwarmTelemetryService:
    """
    Collects real-time statistics from swarm orchestration layers.
    """
<<<<<<< HEAD
<<<<<<< HEAD

    def __init__(self, gatekeeper: Any, shard_manager: Any, topology_manager: Any) -> None:
=======
    
    def __init__(self, gatekeeper: Any, shard_manager: Any, topology_manager: Any):
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
    
    def __init__(self, gatekeeper: Any, shard_manager: Any, topology_manager: Any):
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        self.gatekeeper = gatekeeper
        self.shard_manager = shard_manager
        self.topology_manager = topology_manager

    def get_grid_metrics(self) -> Dict[str, Any]:
        """
        Rolls up metrics into a Grafana-friendly flat JSON structure.
        """
        # 1. Routing Metrics
        routing_stats = {
            "total_experts": len(self.gatekeeper.experts),
<<<<<<< HEAD
<<<<<<< HEAD
            "cache_size": len(self.gatekeeper.routing_cache),
        }

        # 2. Topology Metrics
        topology_stats = self.topology_manager.get_topology_stats()

=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
            "cache_size": len(self.gatekeeper.routing_cache)
        }
        
        # 2. Topology Metrics
        topology_stats = self.topology_manager.get_topology_stats()
        
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        # 3. Context & Sharding Metrics
        shards = []
        for context_shards in self.shard_manager.context_registry.values():
            shards.extend(context_shards)
<<<<<<< HEAD
<<<<<<< HEAD

        precision_counts = Counter(s.precision for s in shards)
        mirror_count = sum(len(s.replica_ranks) for s in shards)

=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
            
        precision_counts = Counter(s.precision for s in shards)
        mirror_count = sum(len(s.replica_ranks) for s in shards)
        
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        context_stats = {
            "total_contexts": len(self.shard_manager.context_registry),
            "total_shards": len(shards),
            "mirrored_shards": mirror_count,
            "dead_ranks": len(self.shard_manager.dead_ranks),
<<<<<<< HEAD
<<<<<<< HEAD
            "shards_by_precision": dict(precision_counts),
        }

=======
            "shards_by_precision": dict(precision_counts)
        }
        
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
            "shards_by_precision": dict(precision_counts)
        }
        
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        return {
            "routing": routing_stats,
            "topology": topology_stats,
            "context": context_stats,
<<<<<<< HEAD
<<<<<<< HEAD
            "swarm_health": "degraded" if context_stats["dead_ranks"] > 0 else "optimal",
=======
            "swarm_health": "degraded" if context_stats["dead_ranks"] > 0 else "optimal"
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
            "swarm_health": "degraded" if context_stats["dead_ranks"] > 0 else "optimal"
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        }

    def export_prometheus(self) -> str:
        """
        Converts metrics to Prometheus exposition format (mock).
        """
        metrics = self.get_grid_metrics()
        lines = [
<<<<<<< HEAD
<<<<<<< HEAD
            f"swarm_total_experts {metrics['routing']['total_experts']}",
            f"swarm_total_shards {metrics['context']['total_shards']}",
            f"swarm_health_status {1 if metrics['swarm_health'] == 'optimal' else 0}",
=======
            f'swarm_total_experts {metrics["routing"]["total_experts"]}',
            f'swarm_total_shards {metrics["context"]["total_shards"]}',
            f'swarm_health_status {1 if metrics["swarm_health"] == "optimal" else 0}'
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
            f'swarm_total_experts {metrics["routing"]["total_experts"]}',
            f'swarm_total_shards {metrics["context"]["total_shards"]}',
            f'swarm_health_status {1 if metrics["swarm_health"] == "optimal" else 0}'
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        ]
        return "\n".join(lines)
