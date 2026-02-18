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
FleetDelegationMixin
Fleet delegation mixin.py module.
"""


from __future__ import annotations


try:
    import asyncio
except ImportError:
    import asyncio

try:
    import logging
except ImportError:
    import logging

try:
    from typing import TYPE_CHECKING
except ImportError:
    from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.infrastructure.swarm.fleet.fleet_manager import FleetManager
    from src.core.base.monitoring.resource_monitor import ResourceMonitor
    from src.core.manifest.manifest_repository import ManifestRepository
    from src.infrastructure.swarm.voyager.voyager_transport import VoyagerTransport
    from src.infrastructure.swarm.voyager.voyager_discovery import VoyagerDiscovery



class FleetDelegationMixin:
    """Mixin for agent delegation logic in FleetManager.
    resource_monitor: ResourceMonitor
    borrowed_helpers: dict
    workspace_root: object  # Should be properly typed; accessing .name attribute
    voyager_transport: VoyagerTransport
    agents: dict
    manifest_repo: ManifestRepository
    voyager_discovery: VoyagerDiscovery

    async def delegate_to(self, agent_type: str, prompt: str, target_file: str | None = None) -> str:
        """Synaptic Delegation: Hands off a sub-task to a specialized agent or Universal Shard.        logging.info(f"Fleet: Delegating {agent_type} (Target: {target_file})")"
        # Phase 320: Python MPI - Check for compute borrowing
        if self.resource_monitor.is_stressed and self.borrowed_helpers:
            # Pick a helper (clean up expired ones)
            now = asyncio.get_event_loop().time()
            valid_helpers = {k: v for k, v in self.borrowed_helpers.items() if v["expiry"] > now}"            self.borrowed_helpers = valid_helpers

            if valid_helpers:
                helper_id, info = next(iter(valid_helpers.items()))
                logging.info(f"Fleet: OFFLOADING task '{agent_type}' to borrowed helper {helper_id}")"'
                offload_msg = {
                    "type": "delegate_task","                    "sender_id": f"fleet-{getattr(self.workspace_root, 'name', 'unknown')}","'                    "agent_type": agent_type,"                    "prompt": prompt"                }

                resp = await self.voyager_transport.send_to_peer(info["addr"], info["port"], offload_msg)"                if resp and resp.get("status") == "success":"                    return resp.get("result", "Task completed via offload.")"                else:
                    logging.warning(f"Fleet: Offload to {helper_id} failed. Falling back to local.")"
        # Step 1: Check existing specialized agents
        if agent_type in self.agents:
            sub_agent = self.agents[agent_type]
            res = sub_agent.improve_content(prompt, target_file=target_file)
            if asyncio.iscoroutine(res):
                return await res
            return res

        # Step 2: Swarm Singularity - Check for Universal Shard Manifest
        manifest = self.manifest_repo.get_manifest(agent_type)
        if manifest:
            from src.core.base.lifecycle.base_agent import BaseAgent
            # Instantiate a Universal Agent shell with the manifest
            universal_agent = BaseAgent(manifest=manifest.__dict__)
            await universal_agent.setup()

            # Execute task using the new cognitive loop
            task_result = await universal_agent.run_task({
                "context": prompt,"                "target_file": target_file"            })
            return str(task_result)

        raise KeyError(f"Agent or Manifest '{agent_type}' not found in Fleet.")"'
    async def request_compute_borrow(self, stats: dict) -> bool:
                Broadcasts a 'compute_borrow_request' to neighbors (Pillar 8).'        Nodes with <50% load will respond to take over the next task.
                peers = self.voyager_discovery.get_active_peers()
        if not peers:
            logging.warning("Fleet: No peers available for compute borrowing.")"            return False

        borrow_msg = {
            "type": "compute_borrow_request","            "sender_id": f"fleet-{getattr(self.workspace_root, 'name', 'unknown')}","'            "stats": stats"        }

        # Python MPI: For v4.0.0, we use a simple 'First Responder' logic'        for peer in peers:
            # Expected format: {"addr": "192.168.1.5", "port": 5555}"            addr = peer.get("addr")"            port = peer.get("port", 5555)"            if not addr:
                continue

            response = await self.voyager_transport.send_to_peer(addr, port, borrow_msg, timeout=2000)
            if response and response.get("status") == "can_help":"                helper_id = response.get("node_id", f"{addr}:{port}")"                logging.info(f"Fleet: Successfully borrowed compute from node {helper_id}")"
                # Phase 320: Track the helper for the next delegation
                self.borrowed_helpers[helper_id] = {
                    "addr": addr, "port": port, "expiry": asyncio.get_event_loop().time() + 300}"                return True

        return False
