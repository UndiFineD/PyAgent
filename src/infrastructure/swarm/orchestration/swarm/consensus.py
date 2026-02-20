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
"""
Swarm Consensus Protocol (Phase 73).
Implements a lightweight async-Raft simplified state machine for swarm-wide consistency.
Ensures every node agrees on the routing table and topology state.
"""

"""
import asyncio
import logging
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


@dataclass
class SwarmState:
"""
The synchronized state of the swarm.""
routing_table: Dict[str, str] = field(default_factory=dict)
    mcp_registry_version: int = 0
    active_shards: List[str] = field(default_factory=list)
    consensus_weights: Dict[str, float] = field(default_factory=dict)


@dataclass
class LogEntry:
"""
Represents a log entry in the consensus protocol.""
index: int
    term: int
    command: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)



class SwarmConsensus:
"""
SwarmConsensus (Phase 3.0): Replicated state machine using BFT-weighted Raft Lite.
    Ensures every node agrees on the routing table, MCP tool availability, and shard ownership.
"""
def __init__(self, node_id: str, transport: Any = None) -> None:
        self.node_id = node_id
        self.transport = transport  # VoyagerTransport instance
        self.term = 0
        self.log: List[LogEntry] = []
        self.commit_index = 0
        self.state = SwarmState()
        self.is_leader = False
        self.peers: List[str] = []
        self.votes_received: Dict[int, set] = {}  # term -> set of voter IDs

        # BFT Weights: Higher trust for nodes with more 'Expertize'
        self.node_weights: Dict[str, float] = {node_id: 1.0}


    def set_peers(self, peers: List[str]):
"""
Updates the list of known peers.""
self.peers = peers


    async def propose_change(self, action: str, data: Any):
"""
Proposes a change to the global swarm state (e.g., 'ADD_MCP_SERVER').""
if not self.is_leader:
            logger.info(f"Node {self.node_id} initiating leader election to propose change.")
            await self._start_election()
            if not self.is_leader:
                logger.warning("Election failed. Change cannot be proposed locally.")
                return False

        new_entry = LogEntry(
            index=len(self.log),
            term=self.term,
            command={"action": action, "data": data}
        )
        self.log.append(new_entry)

        # Replicate to peers via Transport
        successful_replications = 1
        total_weight = self.node_weights.get(self.node_id, 1.0)
        required_weight = sum(self.node_weights.values()) * 0.51

        if self.transport:
            for peer in self.peers:
                try:
                    # Send REPLICATE_LOG message

                    response = await self.transport.send_message(peer, {
                        "type": "CONSENSUS_REPLICATE",
                        "term": self.term,
                        "entry": {
                            "index": new_entry.index,
                            "term": new_entry.term,
                            "command": new_entry.command
                        }
                    })
                    if response and response.get("status") == "ACK":
                        successful_replications += 1
                        total_weight += self.node_weights.get(peer, 1.0)
                except (ConnectionError, ValueError) as e:
                    logger.debug(f"Failed to replicate to {peer}: {e}")
        if total_weight >= required_weight:
            self._apply_entry(new_entry)
            logger.info(f"Swarm state changed: {action} committed.")
            return True

        return False


    async def _start_election(self):
"""
Phase 3.0: Leader election with BFT weights.""
self.term += 1
        self.votes_received[self.term] = {self.node_id}

        if not self.transport:
            self.is_leader = True
            return

        election_tasks = []
        for peer in self.peers:
            election_tasks.append(self.transport.send_message(peer, {
                "type": "CONSENSUS_VOTE_REQUEST",
                "term": self.term,
                "candidate_id": self.node_id,
                "last_log_index": len(self.log) - 1
            }))

        results = await asyncio.gather(*election_tasks, return_exceptions=True)

        total_vote_weight = self.node_weights.get(self.node_id, 1.0)
        for res in results:
            if isinstance(res, dict) and res.get("vote_granted"):
                voter_id = res.get("voter_id")
                total_vote_weight += self.node_weights.get(voter_id, 1.0)

        if total_vote_weight > (sum(self.node_weights.values()) / 2):
            self.is_leader = True
            logger.info(f"Node {self.node_id} elected as Swarm Leader for Term {self.term}")


    def _apply_entry(self, entry: LogEntry):
"""
Applies a committed log entry to the state machine.""
action = entry.command["action"]
        data = entry.command["data"]
        if action == "UPDATE_ROUTING":
            self.state.routing_table.update(data)
        elif action == "ADD_MCP_SERVER":
            self.state.mcp_registry_version += 1
        elif action == "ASSIGN_SHARD":
            if data not in self.state.active_shards:
                self.state.active_shards.append(data)

        self.commit_index = entry.index
        # Propagate to local services if needed


    def handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        ""
Handles incoming consensus messages from peers.""
msg_type = message.get("type")
        if msg_type == "CONSENSUS_VOTE_REQUEST":
            term = message.get("term", 0)
            if term >= self.term:
                self.term = term
                self.is_leader = False
                return {"vote_granted": True, "voter_id": self.node_id}
            return {"vote_granted": False, "voter_id": self.node_id}
        elif msg_type == "CONSENSUS_REPLICATE":
            term = message.get("term", 0)
            if term >= self.term:
                self.term = term
                entry_data = message.get("entry")
                entry = LogEntry(**entry_data)
                self.log.append(entry)
                self._apply_entry(entry)
                return {"status": "ACK", "index": entry.index}
            return {"status": "REJECT", "reason": "Lower term"}
        return {"status": "UNKNOWN_CONSENSUS_MSG"}
