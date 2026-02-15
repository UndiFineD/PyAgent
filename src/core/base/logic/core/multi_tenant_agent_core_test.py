#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Tests for MultiTenantAgentCore

Tests multi-tenant agent orchestration functionality based on AgentCloud patterns.
"""

import pytest
from datetime import datetime

from src.core.base.logic.core.multi_tenant_agent_core import (
    MultiTenantAgentCore,
    ProcessType,
    AgentStatus,
    TaskStatus
)


class TestMultiTenantAgentCore:
    """Test suite for MultiTenantAgentCore."""

    @pytest.fixture
    def core(self):
        """Create a fresh core instance for each test."""
        return MultiTenantAgentCore()

    @pytest.mark.asyncio
    async def test_create_tenant(self, core):
        """Test tenant creation."""
        tenant = await core.create_tenant(
            tenant_id="tenant1",
            name="Test Tenant",
            max_agents=5,
            max_rpm=50
        )

        assert tenant.tenant_id == "tenant1"
        assert tenant.name == "Test Tenant"
        assert tenant.max_agents == 5
        assert tenant.max_rpm == 50
        assert tenant.tenant_id in core.tenants

    @pytest.mark.asyncio
    async def test_create_tenant_duplicate(self, core):
        """Test creating duplicate tenant raises error."""
        await core.create_tenant("tenant1", "Test Tenant")

        with pytest.raises(ValueError, match="Tenant tenant1 already exists"):
            await core.create_tenant("tenant1", "Another Tenant")

    @pytest.mark.asyncio
    async def test_create_agent(self, core):
        """Test agent creation."""
        await core.create_tenant("tenant1", "Test Tenant", max_agents=2)

        agent = await core.create_agent(
            tenant_id="tenant1",
            agent_id="agent1",
            name="Test Agent",
            role="Researcher",
            goal="Find information",
            backstory="I am a research agent",
            model_name="gpt-4"
        )

        assert agent.agent_id == "agent1"
        assert agent.tenant_id == "tenant1"
        assert agent.name == "Test Agent"
        assert agent.role == "Researcher"
        assert agent.status == AgentStatus.ACTIVE

    @pytest.mark.asyncio
    async def test_create_agent_invalid_tenant(self, core):
        """Test creating agent for non-existent tenant."""
        with pytest.raises(ValueError, match="Tenant nonexistent not found"):
            await core.create_agent(
                tenant_id="nonexistent",
                agent_id="agent1",
                name="Test Agent",
                role="Researcher",
                goal="Find information",
                backstory="I am a research agent",
                model_name="gpt-4"
            )

    @pytest.mark.asyncio
    async def test_create_agent_exceeds_limit(self, core):
        """Test creating agent when tenant limit exceeded."""
        await core.create_tenant("tenant1", "Test Tenant", max_agents=1)

        await core.create_agent(
            tenant_id="tenant1",
            agent_id="agent1",
            name="Agent 1",
            role="Researcher",
            goal="Find information",
            backstory="I am a research agent",
            model_name="gpt-4"
        )

        with pytest.raises(ValueError, match="Tenant tenant1 has reached maximum agent limit"):
            await core.create_agent(
                tenant_id="tenant1",
                agent_id="agent2",
                name="Agent 2",
                role="Researcher",
                goal="Find information",
                backstory="I am a research agent",
                model_name="gpt-4"
            )

    @pytest.mark.asyncio
    async def test_create_agent_unauthorized_model(self, core):
        """Test creating agent with unauthorized model."""
        await core.create_tenant("tenant1", "Test Tenant", allowed_models=["gpt-3.5-turbo"])

        with pytest.raises(ValueError, match="Model gpt-4 not allowed for tenant tenant1"):
            await core.create_agent(
                tenant_id="tenant1",
                agent_id="agent1",
                name="Test Agent",
                role="Researcher",
                goal="Find information",
                backstory="I am a research agent",
                model_name="gpt-4"
            )

    @pytest.mark.asyncio
    async def test_create_task(self, core):
        """Test task creation."""
        await core.create_tenant("tenant1", "Test Tenant")
        await core.create_agent(
            tenant_id="tenant1",
            agent_id="agent1",
            name="Test Agent",
            role="Researcher",
            goal="Find information",
            backstory="I am a research agent",
            model_name="gpt-4"
        )

        task = await core.create_task(
            tenant_id="tenant1",
            task_id="task1",
            name="Research Task",
            description="Research the topic",
            expected_output="Research report",
            agent_id="agent1"
        )

        assert task.task_id == "task1"
        assert task.tenant_id == "tenant1"
        assert task.agent_id == "agent1"
        assert task.name == "Research Task"

    @pytest.mark.asyncio
    async def test_create_task_invalid_agent(self, core):
        """Test creating task with invalid agent."""
        await core.create_tenant("tenant1", "Test Tenant")

        with pytest.raises(ValueError, match="Agent invalid not found"):
            await core.create_task(
                tenant_id="tenant1",
                task_id="task1",
                name="Research Task",
                description="Research the topic",
                expected_output="Research report",
                agent_id="invalid"
            )

    @pytest.mark.asyncio
    async def test_create_crew(self, core):
        """Test crew creation."""
        await core.create_tenant("tenant1", "Test Tenant")

        # Create agents
        await core.create_agent(
            tenant_id="tenant1",
            agent_id="agent1",
            name="Researcher",
            role="Researcher",
            goal="Research",
            backstory="Research agent",
            model_name="gpt-4"
        )
        await core.create_agent(
            tenant_id="tenant1",
            agent_id="agent2",
            name="Writer",
            role="Writer",
            goal="Write",
            backstory="Writing agent",
            model_name="gpt-4"
        )

        # Create tasks
        await core.create_task(
            tenant_id="tenant1",
            task_id="task1",
            name="Research",
            description="Research topic",
            expected_output="Research data",
            agent_id="agent1"
        )
        await core.create_task(
            tenant_id="tenant1",
            task_id="task2",
            name="Write",
            description="Write report",
            expected_output="Report",
            agent_id="agent2"
        )

        crew = await core.create_crew(
            tenant_id="tenant1",
            crew_id="crew1",
            name="Research Team",
            agent_ids=["agent1", "agent2"],
            task_ids=["task1", "task2"],
            process_type=ProcessType.SEQUENTIAL
        )

        assert crew.crew_id == "crew1"
        assert crew.agent_ids == ["agent1", "agent2"]
        assert crew.task_ids == ["task1", "task2"]
        assert crew.process_type == ProcessType.SEQUENTIAL

    @pytest.mark.asyncio
    async def test_execute_task(self, core):
        """Test task execution."""
        await core.create_tenant("tenant1", "Test Tenant")
        await core.create_agent(
            tenant_id="tenant1",
            agent_id="agent1",
            name="Test Agent",
            role="Researcher",
            goal="Find information",
            backstory="I am a research agent",
            model_name="gpt-4"
        )
        await core.create_task(
            tenant_id="tenant1",
            task_id="task1",
            name="Test Task",
            description="Test description",
            expected_output="Test output",
            agent_id="agent1"
        )

        result = await core.execute_task("task1")

        assert result.status == TaskStatus.COMPLETED
        assert "Task task1 completed" in result.output
        assert result.execution_time > 0
        assert result.completed_at is not None

    @pytest.mark.asyncio
    async def test_execute_task_rate_limit_exceeded(self, core):
        """Test task execution when rate limit exceeded."""
        await core.create_tenant("tenant1", "Test Tenant", max_rpm=0)
        await core.create_agent(
            tenant_id="tenant1",
            agent_id="agent1",
            name="Test Agent",
            role="Researcher",
            goal="Find information",
            backstory="I am a research agent",
            model_name="gpt-4"
        )
        await core.create_task(
            tenant_id="tenant1",
            task_id="task1",
            name="Test Task",
            description="Test description",
            expected_output="Test output",
            agent_id="agent1"
        )

        with pytest.raises(ValueError, match="Rate limit exceeded"):
            await core.execute_task("task1")

    @pytest.mark.asyncio
    async def test_execute_crew_sequential(self, core):
        """Test crew execution with sequential process."""
        await core.create_tenant("tenant1", "Test Tenant")

        # Create agents
        await core.create_agent(
            tenant_id="tenant1",
            agent_id="agent1",
            name="Agent 1",
            role="Role 1",
            goal="Goal 1",
            backstory="Backstory 1",
            model_name="gpt-4"
        )
        await core.create_agent(
            tenant_id="tenant1",
            agent_id="agent2",
            name="Agent 2",
            role="Role 2",
            goal="Goal 2",
            backstory="Backstory 2",
            model_name="gpt-4"
        )

        # Create tasks
        await core.create_task(
            tenant_id="tenant1",
            task_id="task1",
            name="Task 1",
            description="Description 1",
            expected_output="Output 1",
            agent_id="agent1"
        )
        await core.create_task(
            tenant_id="tenant1",
            task_id="task2",
            name="Task 2",
            description="Description 2",
            expected_output="Output 2",
            agent_id="agent2"
        )

        # Create crew
        await core.create_crew(
            tenant_id="tenant1",
            crew_id="crew1",
            name="Test Crew",
            agent_ids=["agent1", "agent2"],
            task_ids=["task1", "task2"],
            process_type=ProcessType.SEQUENTIAL
        )

        results = await core.execute_crew("crew1")

        assert len(results) == 2
        assert all(r.status == TaskStatus.COMPLETED for r in results)

    @pytest.mark.asyncio
    async def test_execute_crew_consensual(self, core):
        """Test crew execution with consensual process."""
        await core.create_tenant("tenant1", "Test Tenant")

        # Create agents and tasks (same as above)
        await core.create_agent(
            tenant_id="tenant1",
            agent_id="agent1",
            name="Agent 1",
            role="Role 1",
            goal="Goal 1",
            backstory="Backstory 1",
            model_name="gpt-4"
        )
        await core.create_agent(
            tenant_id="tenant1",
            agent_id="agent2",
            name="Agent 2",
            role="Role 2",
            goal="Goal 2",
            backstory="Backstory 2",
            model_name="gpt-4"
        )

        await core.create_task(
            tenant_id="tenant1",
            task_id="task1",
            name="Task 1",
            description="Description 1",
            expected_output="Output 1",
            agent_id="agent1"
        )
        await core.create_task(
            tenant_id="tenant1",
            task_id="task2",
            name="Task 2",
            description="Description 2",
            expected_output="Output 2",
            agent_id="agent2"
        )

        # Create crew with consensual process
        await core.create_crew(
            tenant_id="tenant1",
            crew_id="crew1",
            name="Test Crew",
            agent_ids=["agent1", "agent2"],
            task_ids=["task1", "task2"],
            process_type=ProcessType.CONSENSUAL
        )

        results = await core.execute_crew("crew1")

        assert len(results) == 2
        # Note: Order may vary for consensual execution

    @pytest.mark.asyncio
    async def test_get_tenant_stats(self, core):
        """Test getting tenant statistics."""
        await core.create_tenant("tenant1", "Test Tenant")

        # Create some resources
        await core.create_agent(
            tenant_id="tenant1",
            agent_id="agent1",
            name="Agent 1",
            role="Role 1",
            goal="Goal 1",
            backstory="Backstory 1",
            model_name="gpt-4"
        )
        await core.create_task(
            tenant_id="tenant1",
            task_id="task1",
            name="Task 1",
            description="Description 1",
            expected_output="Output 1",
            agent_id="agent1"
        )
        await core.create_crew(
            tenant_id="tenant1",
            crew_id="crew1",
            name="Crew 1",
            agent_ids=["agent1"],
            task_ids=["task1"]
        )

        stats = await core.get_tenant_stats("tenant1")

        assert stats["tenant_id"] == "tenant1"
        assert stats["agent_count"] == 1
        assert stats["task_count"] == 1
        assert stats["crew_count"] == 1
        assert stats["active_agents"] == 1

    @pytest.mark.asyncio
    async def test_cleanup_tenant(self, core):
        """Test tenant cleanup."""
        await core.create_tenant("tenant1", "Test Tenant")
        await core.create_agent(
            tenant_id="tenant1",
            agent_id="agent1",
            name="Agent 1",
            role="Role 1",
            goal="Goal 1",
            backstory="Backstory 1",
            model_name="gpt-4"
        )

        assert "tenant1" in core.tenants
        assert "agent1" in core.agents

        await core.cleanup_tenant("tenant1")

        assert "tenant1" not in core.tenants
        assert "agent1" not in core.agents

    @pytest.mark.asyncio
    async def test_check_rate_limits(self, core):
        """Test rate limit checking."""
        await core.create_tenant("tenant1", "Test Tenant", max_rpm=2)
        await core.create_agent(
            tenant_id="tenant1",
            agent_id="agent1",
            name="Agent 1",
            role="Role 1",
            goal="Goal 1",
            backstory="Backstory 1",
            model_name="gpt-4",
            max_rpm=1
        )

        # Should be within limits initially
        assert await core.check_rate_limits("tenant1", "agent1")

        # Simulate some requests
        current_time = datetime.now().replace(second=0, microsecond=0)
        core.tenant_request_counts["tenant1"][current_time] = 2  # At limit
        core.agent_request_counts["agent1"][current_time] = 1    # At limit

        # Should be at limits
        assert not await core.check_rate_limits("tenant1", "agent1")
