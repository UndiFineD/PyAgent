#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

"""
Swarm Telemetry Service (Phase 77).
Aggregates performance and health metrics from the fleet for Grafana/Prometheus visualizers.
"""

import logging
<<<<<<< HEAD
from collections import Counter
from typing import Any, Dict

logger = logging.getLogger(__name__)


=======
import json
from typing import Dict, Any, List
from collections import Counter

logger = logging.getLogger(__name__)

>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
class SwarmTelemetryService:
    """
    Collects real-time statistics from swarm orchestration layers.
    """
<<<<<<< HEAD

    def __init__(self, gatekeeper: Any, shard_manager: Any, topology_manager: Any) -> None:
=======
    
    def __init__(self, gatekeeper: Any, shard_manager: Any, topology_manager: Any):
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
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
            "cache_size": len(self.gatekeeper.routing_cache),
        }

        # 2. Topology Metrics
        topology_stats = self.topology_manager.get_topology_stats()

=======
            "cache_size": len(self.gatekeeper.routing_cache)
        }
        
        # 2. Topology Metrics
        topology_stats = self.topology_manager.get_topology_stats()
        
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        # 3. Context & Sharding Metrics
        shards = []
        for context_shards in self.shard_manager.context_registry.values():
            shards.extend(context_shards)
<<<<<<< HEAD

        precision_counts = Counter(s.precision for s in shards)
        mirror_count = sum(len(s.replica_ranks) for s in shards)

=======
            
        precision_counts = Counter(s.precision for s in shards)
        mirror_count = sum(len(s.replica_ranks) for s in shards)
        
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        context_stats = {
            "total_contexts": len(self.shard_manager.context_registry),
            "total_shards": len(shards),
            "mirrored_shards": mirror_count,
            "dead_ranks": len(self.shard_manager.dead_ranks),
<<<<<<< HEAD
            "shards_by_precision": dict(precision_counts),
        }

=======
            "shards_by_precision": dict(precision_counts)
        }
        
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        return {
            "routing": routing_stats,
            "topology": topology_stats,
            "context": context_stats,
<<<<<<< HEAD
            "swarm_health": "degraded" if context_stats["dead_ranks"] > 0 else "optimal",
=======
            "swarm_health": "degraded" if context_stats["dead_ranks"] > 0 else "optimal"
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        }

    def export_prometheus(self) -> str:
        """
        Converts metrics to Prometheus exposition format (mock).
        """
        metrics = self.get_grid_metrics()
        lines = [
<<<<<<< HEAD
            f"swarm_total_experts {metrics['routing']['total_experts']}",
            f"swarm_total_shards {metrics['context']['total_shards']}",
            f"swarm_health_status {1 if metrics['swarm_health'] == 'optimal' else 0}",
=======
            f'swarm_total_experts {metrics["routing"]["total_experts"]}',
            f'swarm_total_shards {metrics["context"]["total_shards"]}',
            f'swarm_health_status {1 if metrics["swarm_health"] == "optimal" else 0}'
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        ]
        return "\n".join(lines)
