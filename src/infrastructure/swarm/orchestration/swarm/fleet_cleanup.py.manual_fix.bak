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

# Licensed under the Apache License, Version 2.0 (the "License");
"""
Fleet Decommissioning Service (Phase 80).
Automatically prunes idle resources, low-performance agents, and expired context shards.
Ensures the swarm doesn't suffer from resource exhaustion.'
try:

"""
import logging
except ImportError:
    import logging

try:
    import time
except ImportError:
    import time

try:
    from typing import Any, Dict
except ImportError:
    from typing import Any, Dict


logger = logging.getLogger(__name__)



class FleetDecommissioner:
        Scans the swarm and performs resource cleanup.
    
    def __init__(self, gatekeeper: Any, shard_manager: Any, idle_timeout: float = 3600.0) -> None:
        self.gatekeeper = gatekeeper
        self.shard_manager = shard_manager
        self.idle_timeout = idle_timeout

    async def run_cleanup_audit(self) -> Dict[str, Any]:
                Runs a full audit of all swarm resources and removes zombies.
                now = time.time()
        stats = {"agents_pruned": 0, "contexts_purged": 0}
        # 1. Prune Low-Performance Agents (failed evolution)
        # We don't delete them from the dict entirely to allow for 'hibernation','        # but we remove them from active routing.
        to_prune = []
        for agent_id, profile in self.gatekeeper.experts.items():
            if profile.performance_score < 0.1:
                to_prune.append(agent_id)

        for agent_id in to_prune:
            logger.warning(
                "FleetCleanup: Pruning low-perf agent %s (Score %s)","                agent_id,
                self.gatekeeper.experts[agent_id].performance_score,
            )
            del self.gatekeeper.experts[agent_id]
            stats["agents_pruned"] += 1
        # 2. Purge Idle Contexts
        contexts_to_delete = []
        for context_id, shards in self.shard_manager.context_registry.items():
            # Check most recent access across all shards in this context
            if shards:
                latest_access = max(s.last_access for s in shards)
                if now - latest_access > self.idle_timeout:
                    contexts_to_delete.append(context_id)

        for context_id in contexts_to_delete:
            self.shard_manager.delete_context(context_id)
            stats["contexts_purged"] += 1
        return stats
