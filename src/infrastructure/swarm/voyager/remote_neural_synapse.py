
"""
Remote neural synapse.py module.
"""
# Copyright 2026 PyAgent Authors
# Phase 319: Multi-Cloud Teleportation (Remote Neural Synapse)

import asyncio
from typing import Any, Dict, List, Optional

from src.infrastructure.swarm.voyager.teleportation_engine import \
    TeleportationEngine
from src.infrastructure.swarm.voyager.transport_layer import VoyagerTransport
from src.observability.structured_logger import StructuredLogger

logger = StructuredLogger(__name__)


class RemoteNeuralSynapse:
    """
    Manages the 'synaptic' firing of tasks and agents to remote peers.
    Implements the transport layer for Voyager Phase 1.1 using ZMQ.
    """

    def __init__(self, fleet_manager: Any, transport_port: int = 5555, discovery_node: Any = None) -> None:
        self.fleet_manager = fleet_manager
        self.engine = TeleportationEngine()
        self.transport = VoyagerTransport(port=transport_port)
        self.discovery_node = discovery_node
        self.active_transfers: List[str] = []
        self._server_task: Optional[asyncio.Task] = None

    async def start(self) -> None:
        """Starts the transport server to receive remote synaptic fires."""
        if self._server_task:
            return
        self._server_task = asyncio.create_task(self.transport.start_server(self._handle_incoming_synapse))

    async def stop(self) -> None:
        """Stops the transport server."""
        self.transport.stop()
        if self._server_task:
            self._server_task.cancel()
            try:
                await self._server_task
            except asyncio.CancelledError:
                pass
            self._server_task = None

    async def broadcast(self, message: Dict[str, Any]) -> None:
        """Broadcasts a message to all discovered peers."""
        if not self.discovery_node:
            return

        peers = self.discovery_node.get_peers()
        tasks = []
        for peer in peers:
            tasks.append(self.send_to_peer(peer["ip"], peer["port"], message))
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def send_to_peer(self, ip: str, port: int, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Sends a message to a specific peer."""
        try:
            return await self.transport.send_to_peer(ip, port, message)
        except Exception as e:
            logger.error(f"Synapse: Failed to send to {ip}:{port} - {e}")
            return None

    async def _handle_incoming_synapse(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes incoming teleported agents or task requests.
        """
        msg_type = message.get("type", "unknown")
        logger.info(f"Synapse: Incoming {msg_type} from {message.get('sender_id', 'unknown')}")

        if msg_type == "teleport":
            encoded_blob: Any | None = message.get("agent_blob")
            if encoded_blob:
                blob: bytes = self.engine.decode_from_transport(encoded_blob)
                state: Dict[str, Any] = self.engine.restore_agent_state(blob)

                # Logic to 'spawn' the agent in the local fleet
                # if hasattr(self.fleet_manager, "assimilate_agent"):
                #     await self.fleet_manager.assimilate_agent(state)

                return {"status": "success", "message": f"Agent {state.get('name')} assimilated."}

        elif msg_type == "ping":
            return {"status": "pong", "version": "Phase-319"}

        elif msg_type == "heartbeat":
            peer_id = message.get("sender_id", "unknown")
            metrics = message.get("metrics", {})
            logger.debug(f"Synapse: Received heartbeat from {peer_id}: {metrics}")
            
            # Update discovery node with peer metadata
            if self.discovery_node and hasattr(self.discovery_node, "update_peer_metadata"):
                self.discovery_node.update_peer_metadata(peer_id, {
                    "last_heartbeat": message.get("timestamp"),
                    "metrics": metrics,
                    "hostname": message.get("hostname")
                })
            return {"status": "acknowledged"}

        elif msg_type == "task_offload":
            task_desc = message.get("task", "")
            sender = message.get("sender_id", "unknown")
            logger.info(f"Synapse: Received offloaded task from {sender}: {task_desc[:50]}...")
            
            if hasattr(self.fleet_manager, "execute_reliable_task"):
                try:
                    # Execute locally (Task Preemption / Synergy)
                    result = await self.fleet_manager.execute_reliable_task(task_desc)
                    return {"status": "success", "result": result}
                except Exception as e:
                    logger.error(f"Synapse: Execution failed: {e}")
                    return {"status": "error", "message": str(e)}
            else:
                 return {"status": "error", "message": "FleetManager capability missing."}

        elif msg_type == "memory_query":
            # Phase 4.0: Federated Memory Query
            query = message.get("query", "")
            agent_id = message.get("target_agent", "swarm_shared")
            sender = message.get("sender_id", "unknown")
            logger.info(f"Synapse: Processing federated memory query from {sender}: '{query}'")
            
            from src.core.base.common.memory_core import MemoryCore
            try:
                results: List[Dict[str, Any]] = MemoryCore().retrieve_knowledge(agent_id, query, mode="semantic", limit=3)
                return {"status": "success", "results": results}
            except Exception as e:
                logger.error(f"Synapse: Memory query failed: {e}")
                return {"status": "error", "message": str(e)}

        return {"status": "error", "message": "Unsupported synapse type."}

    async def teleport_agent_to_peer(self, agent: Any, peer_address: str, transport_port: int) -> bool:
        """
        Transmits an agent's neural state to a remote peer via ZMQ.
        """
        blob: bytes = self.engine.capture_agent_state(agent)
        payload = {
            "type": "teleport",
            "agent_blob": self.engine.encode_for_transport(blob),
            "sender_id": self.fleet_manager.fleet_id if hasattr(self.fleet_manager, "fleet_id") else "unknown",
        }

        logger.info(f"Synapse: Firing synaptic teleport of {agent.name} to {peer_address}:{transport_port}...")

        response: Dict[str, Any] | None = await self.transport.send_to_peer(peer_address, transport_port, payload)
        if response and response.get("status") == "success":
            logger.info(f"Synapse: Teleportation confirmed by peer: {response.get('message')}")
            return True

        logger.error(f"Synapse: Teleportation failed or unconfirmed: {response}")
        return False

    async def teleport_to_peer_name(self, agent: Any, peer_name: str) -> bool:
        """
        Phase 319: Bridges mDNS discovery with ZMQ transport.
        Resolves peer name to address automatically.
        """
        if not self.discovery_node:
            logger.error("Synapse: Cannot teleport by name - discovery_node not initialized.")
            return False

        target = self.discovery_node.resolve_synapse_address(peer_name)
        if not target:
            logger.error(f"Synapse: Could not resolve peer name '{peer_name}' on local network.")
            return False

        peer_ip, peer_port = target
        return await self.teleport_agent_to_peer(agent, peer_ip, peer_port)

    async def remote_invoke(self, thought_pattern: str, target_peer: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Executes a 'Remote Neural Synapse' - sending a specific reasoning task to another node.
        """
        # Logic to send a task and wait for a result
        logger.info(f"Synapse: Remote invocation triggered on {target_peer.get('name')}")
        # Placeholder for actual result retrieval
        return {"status": "dispatched", "task": thought_pattern[:20]}
