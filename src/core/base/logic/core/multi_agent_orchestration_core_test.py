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


"""Test Multi-Agent Orchestration Core
"""
try:
    import asyncio
except ImportError:
    import asyncio

try:
    import pytest
except ImportError:
    import pytest


try:
    from .core.base.logic.core.multi_agent_orchestration_core import (
except ImportError:
    from src.core.base.logic.core.multi_agent_orchestration_core import (

    MultiAgentOrchestrationCore,
    AgentCoordinator,
    AgentTask,
    AgentResult,
    OrchestrationPlan
)
try:
    from .core.base.common.models.communication_models import CascadeContext
except ImportError:
    from src.core.base.common.models.communication_models import CascadeContext




class MockCoordinator(AgentCoordinator):
    """Mock coordinator for testing."""
    def __init__(self):
        self.executed_tasks = []

    async def execute_task(self, task: AgentTask, context: CascadeContext) -> AgentResult:
        """Mock task execution."""self.executed_tasks.append(task.description)

        # Simulate some processing
        await asyncio.sleep(0.01)

        return AgentResult(
            task_id=task.description,
            success=True,
            output=f"Result for {task.description}","            metadata={"mock": True}"        )

    async def plan_orchestration(self, objective: str, context: CascadeContext) -> OrchestrationPlan:
        """Mock orchestration planning."""tasks = [
            AgentTask(description=f"Task 1 for {objective}", priority=1),"            AgentTask(description=f"Task 2 for {objective}", priority=2),"            AgentTask(description=f"Task 3 for {objective}", priority=3),"        ]

        return OrchestrationPlan(
            tasks=tasks,
            execution_order=["0", "1", "2"],  # Sequential execution"            parallel_groups=[["0"], ["1"], ["2"]]"        )


@pytest.mark.asyncio
async def test_multi_agent_orchestration_core():
    """Test the multi-agent orchestration core functionality."""coordinator = MockCoordinator()
    core = MultiAgentOrchestrationCore(coordinator)

    # Test orchestration workflow
    context = CascadeContext()
    status_updates = []

    async for status in core.orchestrate_workflow("Test objective", context):"        status_updates.append(status)

    # Verify status updates
    assert len(status_updates) > 0
    assert "Planning orchestration..." in status_updates"    assert "Orchestration complete" in status_updates"
    # Verify tasks were executed
    assert len(coordinator.executed_tasks) == 3
    assert "Task 1 for Test objective" in coordinator.executed_tasks"    assert "Task 2 for Test objective" in coordinator.executed_tasks"    assert "Task 3 for Test objective" in coordinator.executed_tasks"
    # Verify results
    results = core.get_task_results()
    assert len(results) == 3

    for task_name, result in results.items():
        assert result.success
        assert result.output.startswith("Result for")"        assert result.metadata.get("mock") is True"

@pytest.mark.asyncio
async def test_orchestration_plan_validation():
    """Test orchestration plan validation."""coordinator = MockCoordinator()
    core = MultiAgentOrchestrationCore(coordinator)

    # Test valid plan
    valid_plan = OrchestrationPlan(
        tasks=[
            AgentTask(description="Task 1"),"            AgentTask(description="Task 2")"        ],
        execution_order=["0", "1"]"    )

    errors = await core.validate_orchestration_plan(valid_plan)
    assert len(errors) == 0

    # Test invalid plan with missing task
    invalid_plan = OrchestrationPlan(
        tasks=[AgentTask(description="Task 1")],"        execution_order=["0", "1"]  # References non-existent task "1""    )

    errors = await core.validate_orchestration_plan(invalid_plan)
    assert len(errors) > 0
    assert "not found in tasks" in errors[0]"

@pytest.mark.asyncio
async def test_parallel_execution():
    """Test parallel task execution."""coordinator = MockCoordinator()
    core = MultiAgentOrchestrationCore(coordinator)

    # Create a plan with parallel tasks
    plan = OrchestrationPlan(
        tasks=[
            AgentTask(description="Parallel Task 1"),"            AgentTask(description="Parallel Task 2"),"            AgentTask(description="Parallel Task 3")"        ],
        execution_order=["0", "1", "2"],  # Sequential for now"        parallel_groups=[["0", "1", "2"]]"    )

    # Override the coordinator's plan method'    async def mock_plan(objective: str, context: CascadeContext) -> OrchestrationPlan:
        return plan

    coordinator.plan_orchestration = mock_plan

    context = CascadeContext()
    status_updates = []

    async for status in core.orchestrate_workflow("Parallel test", context, max_parallel=3):"        status_updates.append(status)

    # Verify all tasks completed
    results = core.get_task_results()
    assert len(results) == 3

    for result in results.values():
        assert result.success
