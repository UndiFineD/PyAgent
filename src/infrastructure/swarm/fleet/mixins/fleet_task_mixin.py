# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from __future__ import annotations
import logging
from typing import Any, TYPE_CHECKING
from src.core.base.common.models import AgentPriority

if TYPE_CHECKING:
    from src.infrastructure.swarm.fleet.fleet_manager import FleetManager

class FleetTaskMixin:
    """Mixin for task execution, preemption, and consensus management in FleetManager."""

    def preempt_lower_priority_tasks(self: FleetManager, new_priority: AgentPriority) -> None:
        """Suspends all tasks with lower priority than the new high-priority task."""
        for tid, data in self.active_tasks.items():
            if data["priority"].value > new_priority.value:
                logging.info(
                    f"Preempting lower-priority task {tid} ({data['priority'].name})"
                )
                for agent in data.get("agents", []):
                    if hasattr(agent, "suspend"):
                        agent.suspend()

    def resume_tasks(self: FleetManager) -> None:
        """Resumes all suspended tasks if no critical tasks are running."""
        # Check if any Critical/High tasks are still active
        critical_active = any(
            d["priority"].value < AgentPriority.NORMAL.value
            for d in self.active_tasks.values()
        )
        if not critical_active:
            for tid, data in self.active_tasks.items():
                for agent in data.get("agents", []):
                    if hasattr(agent, "resume"):
                        agent.resume()

    async def execute_reliable_task(
        self: FleetManager, task: str, priority: AgentPriority = AgentPriority.NORMAL
    ) -> str:
        """Executes a task using the 7-phase inner loop and linguistic articulation."""
        return await self.execution_core.execute_reliable_task(task, priority=priority)

    async def _record_success(self: FleetManager, res_or_prompt: Any, *args: Any, **kwargs: Any) -> None:
        """Records the success of a workflow step (Delegated)."""
        await self.interaction_recorder.record_success(res_or_prompt, *args, **kwargs)

    async def _record_failure(self: FleetManager, prompt: str, error: str, model: str) -> None:
        """Records errors, failures, and mistakes (Delegated)."""
        await self.interaction_recorder.record_failure(prompt, error, model)

    async def execute_workflow(
        self: FleetManager,
        task: str,
        workflow_steps: list[dict[str, Any]],
        priority: AgentPriority = AgentPriority.NORMAL,
    ) -> str:
        """Runs a sequence of agent actions with shared state and signals."""
        return await self.execution_core.execute_workflow(
            task, workflow_steps, priority=priority
        )

    def execute_with_consensus(
        self: FleetManager,
        task: str,
        primary_agent: str | None = None,
        secondary_agents: list[str] | None = None,
    ) -> dict[str, Any]:
        """
        Executes a task across multiple agents and uses ByzantineConsensusAgent to pick the winner.
        """
        return self.consensus_manager.execute_with_consensus(
            task, primary_agent, secondary_agents
        )
