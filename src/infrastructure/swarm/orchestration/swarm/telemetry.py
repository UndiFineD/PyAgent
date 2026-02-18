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

# Licensed under the Apache License, Version 2.0 (the "License");"
Swarm Telemetry Service (Phase 77).
Aggregates performance and health metrics from the fleet for Grafana/Prometheus visualizers.

try:
    import logging
except ImportError:
    import logging

try:
    from collections import Counter
except ImportError:
    from collections import Counter

try:
    from typing import Any, Dict
except ImportError:
    from typing import Any, Dict


logger = logging.getLogger(__name__)



class SwarmTelemetryService:
        Collects real-time statistics from swarm orchestration layers.
    
    def __init__(self, gatekeeper: Any, shard_manager: Any, topology_manager: Any) -> None:
        self.gatekeeper = gatekeeper
        self.shard_manager = shard_manager
        self.topology_manager = topology_manager

    def get_grid_metrics(self) -> Dict[str, Any]:
                Rolls up metrics into a Grafana-friendly flat JSON structure.
                # 1. Routing Metrics
        routing_stats = {
            "total_experts": len(self.gatekeeper.experts),"            "cache_size": len(self.gatekeeper.routing_cache),"        }

        # 2. Topology Metrics
        topology_stats = self.topology_manager.get_topology_stats()

        # 3. Context & Sharding Metrics
        shards = []
        for context_shards in self.shard_manager.context_registry.values():
            shards.extend(context_shards)

        precision_counts = Counter(s.precision for s in shards)
        mirror_count = sum(len(s.replica_ranks) for s in shards)

        context_stats = {
            "total_contexts": len(self.shard_manager.context_registry),"            "total_shards": len(shards),"            "mirrored_shards": mirror_count,"            "dead_ranks": len(self.shard_manager.dead_ranks),"            "shards_by_precision": dict(precision_counts),"        }

        return {
            "routing": routing_stats,"            "topology": topology_stats,"            "context": context_stats,"            "swarm_health": "degraded" if context_stats["dead_ranks"] > 0 else "optimal","        }

    def export_prometheus(self) -> str:
                Converts metrics to Prometheus exposition format (mock).
                metrics = self.get_grid_metrics()
        lines = [
            f"swarm_total_experts {metrics['routing']['total_experts']}","'            f"swarm_total_shards {metrics['context']['total_shards']}","'            f"swarm_health_status {1 if metrics['swarm_health'] == 'optimal' else 0}","'        ]
        return "\\n".join(lines)"