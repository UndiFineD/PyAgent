#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

"""
Swarm Topology Manager (Phase 70).
Handles dynamic expert cloning and load-based re-assignment.
"""

import asyncio
import logging
from typing import Any, Dict, List

from src.core.base.common.models.communication_models import ExpertProfile

logger = logging.getLogger(__name__)


class TopologyManager:
    """
    Monitors swarm health and automatically scales expert replicas.
    """

    def __init__(self, gatekeeper: Any, clone_threshold: int = 100):
        self.gatekeeper = gatekeeper
        self.clone_threshold = clone_threshold
        self.request_counts: Dict[str, int] = {}
        self.replicas: Dict[str, List[str]] = {}  # master_id -> [replica_id1, ...]

    def record_usage(self, agent_id: str):
        """Increments usage counter and triggers cloning if threshold met."""
        self.request_counts[agent_id] = self.request_counts.get(agent_id, 0) + 1

        if self.request_counts[agent_id] >= self.clone_threshold:
            asyncio.create_task(self.clone_expert(agent_id))
            self.request_counts[agent_id] = 0  # Reset counter after cloning

    async def clone_expert(self, agent_id: str):
        """
        Creates a virtual replica of an expert to distribute load.
        In a real system, this might involve spawning a new container or process.
        Here we register a virtual 'replica' in the gatekeeper.
        """
        if agent_id not in self.gatekeeper.experts:
            return

        master_profile = self.gatekeeper.experts[agent_id]
        replica_id = f"{agent_id}_replica_{len(self.replicas.get(agent_id, [])) + 1}"

        logger.info(f"Cloning expert {agent_id} to {replica_id} due to high demand.")

        # Create replica profile
        replica_profile = ExpertProfile(
            agent_id=replica_id,
            domains=master_profile.domains,
            performance_score=master_profile.performance_score,
            specialization_vector=master_profile.specialization_vector,
            is_replica=True,
            parent_id=agent_id,
        )

        self.gatekeeper.register_expert(replica_profile)

        if agent_id not in self.replicas:
            self.replicas[agent_id] = []
        self.replicas[agent_id].append(replica_id)

    def get_topology_stats(self) -> Dict[str, Any]:
        """Returns the current state of clones and master agents."""
        return {
            "active_masters": len(self.replicas),
            "total_replicas": sum(len(v) for v in self.replicas.values()),
            "clones": self.replicas,
        }
