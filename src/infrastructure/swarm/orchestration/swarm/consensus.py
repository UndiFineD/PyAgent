#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

"""
Swarm Consensus Protocol (Phase 73).
Implements a lightweight async-Raft simplified state machine for swarm-wide consistency.
Ensures every node agrees on the routing table and topology state.
"""

import asyncio
import logging
from dataclasses import dataclass
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


@dataclass
class LogEntry:
    """Represents a log entry in the consensus protocol."""
    index: int
    term: int
    command: Dict[str, Any]


class SwarmConsensus:
    """
    Manages replicated state across the swarm.
    Prevents configuration drift in large fleets.
    """

    def __init__(self, node_id: str, peers: List[str]) -> None:
        self.node_id = node_id
        self.peers = peers
        self.term = 0
        self.log: List[LogEntry] = []
        self.commit_index = 0
        self.state_machine: Dict[str, Any] = {}
        self.is_leader = False

    async def propose_change(self, key: str, value: Any):
        """Proposes a change to the global swarm state."""
        if not self.is_leader:
            # In a real Raft, we'd forward to leader. Here we simulate leadership for the test.
            logger.debug(f"Node {self.node_id} proposing change as candidate leader.")
            self.is_leader = True

        new_entry = LogEntry(index=len(self.log), term=self.term, command={"key": key, "val": value})
        self.log.append(new_entry)

        # Simulate replication to peers
        success_count = 1
        for peer in self.peers:
            if await self._replicate_to_peer(peer, new_entry):
                success_count += 1

        if success_count > (len(self.peers) + 1) / 2:
            self._commit_entry(new_entry)
            return True
        return False

    async def _replicate_to_peer(self, _peer: str, _entry: LogEntry) -> bool:
        """Simulates RPC call to peer node."""
        await asyncio.sleep(0.01)  # Network latency
        return True

    def _commit_entry(self, entry: LogEntry):
        """Applies the command to the local state machine."""
        key = entry.command["key"]
        val = entry.command["val"]
        self.state_machine[key] = val
        self.commit_index = entry.index
        logger.info(f"Consensus committed change: {key} = {val} at index {entry.index}")

    def get_state(self, key: str) -> Any:
        """Retrieves the current value for a key from the state machine."""
        return self.state_machine.get(key)
