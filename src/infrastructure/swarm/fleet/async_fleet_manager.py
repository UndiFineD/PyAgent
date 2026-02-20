#!/usr/bin/env python3
from __future__ import annotations

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
AsyncFleetManager
"""
An enhanced FleetManager that supports parallel execution of agent workflows.
"""

"""
import asyncio
import inspect
import logging
import time
from typing import Any

from src.core.base.lifecycle.version import VERSION
from src.core.base.logic.dependency_graph import DependencyGraph

from src.infrastructure.swarm.fleet.workflow_state import WorkflowState

__version__ = VERSION



class AsyncFleetManager:
"""
Enhanced FleetManager that supports parallel execution of agent workflows.
    Inherits from FleetManager at runtime to avoid circular import.
"""
def __init__(self, *args, **kwargs):
        from src.infrastructure.swarm.fleet.fleet_manager import FleetManager
        self.__class__ = type(self.__class__.__name__, (FleetManager,), dict(self.__class__.__dict__))
        super(self.__class__, self).__init__(*args, **kwargs)
"""
Executes agent workflows in parallel using native asyncio.
    Supports dependency-aware batching for optimized execution (Phase 232).
"""
def __init__(self, workspace_root: str, max_workers: int = 4) -> None:
        super().__init__(workspace_root)
        self.max_workers = max_workers
        self.active_workflows: dict[str, WorkflowState] = {}
        self._migration_events: dict[str, asyncio.Event] = {}

    async def execute_workflow_async(
        self,
        task: str,
        workflow_steps: list[dict[str, Any]],
        workflow_id: str | None = None,
    ) -> str:
"""
Runs multiple agent steps in parallel with dependency-aware batching (Phase 232).""
logging.info(f"Starting parallel workflow: {task} with {len(workflow_steps)} steps.")
        if not workflow_id:
            workflow_id = f"async_wf_{int(time.time())}"
        # Phase 239: Initialize or retrieve workflow state
        if workflow_id in self.active_workflows:
            state = self.active_workflows[workflow_id]
            logging.info(f"Resuming workflow {workflow_id} from step index {state.get('next_batch_idx', 0)}")
        else:
            state = WorkflowState(task_id=workflow_id, original_request=task)
            state.set("next_batch_idx", 0)
            state.set("all_results", [])
            self.active_workflows[workflow_id] = state

        # 1. Build Dependency Graph
        graph = DependencyGraph()
        step_map: dict[str, dict[str, Any]] = {}

        for i, step in enumerate(workflow_steps):
            # Ensure unique IDs for graph nodes
            step_id = step.get("id") or f"step_{i}"
            step_map[step_id] = step
            # Phase 242: Add resource hints to graph for refined batching
            graph.add_node(step_id, resources=step.get("resources", []))
            for dep in step.get("depends_on", []):
                graph.add_dependency(step_id, dep)

        # 2. Resolve Batches
        try:
            batches = graph.resolve()
        except ValueError as e:
            logging.error(f"Workflow dependency resolution failed: {e}")
            return f"Error: Invalid workflow graph - {e}"
        logging.info(f"Resolved workflow into {len(batches)} parallel execution batches.")
        all_results = state.get("all_results")
        start_idx = state.get("next_batch_idx")
        # 3. Execute Batches Sequentially (Internal parallelism per batch)
        for batch_idx in range(start_idx, len(batches)):
            batch = batches[batch_idx]

            # Phase 239: Check for migration signal
            if state.get("migration_pending"):
                logging.info(f"Migration signal received for {workflow_id}. Suspending at batch {batch_idx}.")
                state.set("next_batch_idx", batch_idx)
                if workflow_id in self._migration_events:
                    self._migration_events[workflow_id].set()
                return f"WORKFLOW_SUSPENDED: {workflow_id} at batch {batch_idx}"
            logging.info(f"Executing batch {batch_idx + 1}/{len(batches)}: {batch}")
            tasks = [self._run_single_step(step_map[step_id], workflow_id) for step_id in batch]
            responses = await asyncio.gather(*tasks, return_exceptions=True)

            for i, res in enumerate(responses):
                step_id = batch[i]
                agent_name = step_map[step_id].get("agent")
                if isinstance(res, Exception):
                    logging.error(f"Async failure in batch {batch_idx + 1} for {agent_name}: {res}")
                    all_results.append(f"### Error from {agent_name} ({step_id})\\n{str(res)}\\n")
                else:
                    all_results.append(f"### Results from {agent_name} ({step_id})\\n{res}\\n")
        # Cleanup on completion
        if workflow_id in self.active_workflows:
            del self.active_workflows[workflow_id]

        return f"# Parallel Workflow Summary: {task}\\n\\n" + "\\n".join(all_results)


    async def migrate_workflow(self, workflow_id: str, remote_manager: AsyncFleetManager) -> bool:
"""
Phase 239: Migrates an active workflow to another manager without downtime.
"""
if workflow_id not in self.active_workflows:
            logging.error(f"Cannot migrate {workflow_id}: Not found.")
            return False

        state = self.active_workflows[workflow_id]
        state.set("migration_pending", True)
        # Create an event to wait for batch completion
        event = asyncio.Event()
        self._migration_events[workflow_id] = event

        logging.info(f"Waiting for workflow {workflow_id} to suspend...")
        await event.wait()

        # Workflow is now suspended. Move state to remote.
        success = await remote_manager.handoff_state(state)

        if success:
            logging.info(f"Workflow {workflow_id} successfully migrated.")
            del self.active_workflows[workflow_id]
            del self._migration_events[workflow_id]
            return True

        logging.error(f"Migration of {workflow_id} failed during handoff.")
        state.set("migration_pending", False)
        return False


    async def handoff_state(self, state: WorkflowState) -> bool:
"""
Phase 239: Receives a migrated workflow state and prepares for resumption.""
logging.info(f"Received handoff for workflow {state.task_id}")
        state.set("migration_pending", False)
        self.active_workflows[state.task_id] = state
        # In a real system, we'd trigger execute_workflow_async here or wait for a signal
        await self.execute_workflow_async(state.task_id)
        return True


    async def _run_single_step(self, step: dict[str, Any], workflow_id: str) -> str:
"""
Phase 152 Refactor: Native asyncio orchestration with async locking.""
agent_name = step.get("agent")
        action_name = step.get("action")
        args = step.get("args", [])
        resources = step.get("resources", [])
        if not agent_name or agent_name not in self.agents:
            return f"Error: Agent '{agent_name}' not found."
        agent = self.agents[agent_name]
        if not action_name:
            return "Error: Action name is required."
        action_fn = getattr(agent, action_name, None)
        if not action_fn:
            return f"Error: Action '{action_name}' not supported."
        trace_id = f"{workflow_id}_{agent_name}_{action_name}"
        self.telemetry.start_trace(trace_id)

        try:
            from src.infrastructure.swarm.orchestration.system.lock_manager import \
                LockManager

            locker = LockManager()

            # Phase 152: Recursive async lock acquisition
            async def run_with_async_locks(res_list: list[str]) -> Any:
                if not res_list:
                    # Execute task
                    if inspect.iscoroutinefunction(action_fn):
                        return await action_fn(*args)

                    loop = asyncio.get_running_loop()
                    return await loop.run_in_executor(None, action_fn, *args)

                res = res_list[0]
                l_type = "file" if any(c in res for c in "/\\.") else "memory"
                async with locker.acquire_async(res, lock_type=l_type):
                    return await run_with_async_locks(res_list[1:])

            res = await run_with_async_locks(resources)
            self.telemetry.end_trace(trace_id, agent_name, action_name, status="success")
            if isinstance(res, str):
                res = await self._pre_commit_audit(res, agent_name)

            return res
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            self.telemetry.end_trace(
                trace_id,
                agent_name,
                action_name,
                status="error",
                metadata={"error": str(e)},
            )
            raise e


    async def _pre_commit_audit(self, content: str, agent_name: str) -> str:
"""
Phase 240: Runs legal and compliance audits before finalizing output.
"""
if agent_name == "LegalAuditAgent":
            return content

        try:
            # Check if LegalAuditAgent is available
            audit_agent = self.agents.get("LegalAudit")
            if not audit_agent:
                return content

            # 1. License Check (Phase 238)
            compliance = audit_agent.check_license_compliance(content)
            if not compliance["is_compliant"]:
                violations_str = ", ".join(compliance["violations"])
                logging.warning(
                    f"Legal Violation in {agent_name} output: {violations_str}"
                )
                return (
                    f"[LEGAL_BLOCK]: Output from {agent_name} contains blacklisted licenses "
                    f"({violations_str}). REDACTED."
                )

            # 2. Liability Check
            liability = audit_agent.generate_liability_report(content)

            if "WARNING" in liability:
                logging.warning(
                    f"Liability Risk in {agent_name} output: {liability}"
                )
                # Append disclaimer instead of blocking
                return (
                    content
                    + "\n\n---\n*DISCLAIMER: This output contains language flagged for liability risk "
                    "and has not been verified for legal accuracy.*"
                )

        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.debug(f"Audit failed (Agent likely not found or errored): {e}")
        return content


if __name__ == "__main__":
    # Test script
    from src.logic.agents.cognitive.knowledge_agent import KnowledgeAgent
    from src.logic.agents.security import SecurityGuardAgent

    ROOT_PATH = "."
    afleet = AsyncFleetManager(ROOT_PATH)
    afleet.register_agent("K1", KnowledgeAgent)
    afleet.register_agent("S1", SecurityGuardAgent)
    wf = [
        {"agent": "K1", "action": "improve_content", "args": ["agent"]},
        {"agent": "S1", "action": "improve_content", "args": ["clean code"]},
    ]


    async def run_test() -> None:
"""
Executes a test workflow.
        ""
report = await afleet.execute_workflow_async("Parallel Test", wf)
        print(report)

    asyncio.run(run_test())
