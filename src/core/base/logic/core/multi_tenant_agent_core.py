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
Multi-Tenant Agent Core

Implements multi-tenant agent orchestration patterns from AgentCloud.
Provides database-driven agent, task, and crew management with resource controls.
Based on AgentCloud's CrewAI platform architecture.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Union, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid

from src.core.base.common.base_core import BaseCore


class ProcessType(str, Enum):
    """Crew process types."""
    SEQUENTIAL = "sequential"
    HIERARCHICAL = "hierarchical"
    CONSENSUAL = "consensual"


class ToolType(str, Enum):
    """Tool types supported."""
    BUILTIN = "builtin"
    FUNCTION = "function"
    RAG = "rag"


class AgentStatus(str, Enum):
    """Agent status states."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"


class TaskStatus(str, Enum):
    """Task execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class TenantConfig:
    """Configuration for a tenant."""
    tenant_id: str
    name: str
    max_agents: int = 10
    max_concurrent_tasks: int = 5
    max_rpm: int = 100  # requests per minute
    allowed_models: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class AgentDefinition:
    """Agent definition with role and capabilities."""
    agent_id: str
    tenant_id: str
    name: str
    role: str
    goal: str
    backstory: str
    model_name: str
    tool_ids: List[str] = field(default_factory=list)
    max_iterations: int = 10
    max_rpm: int = 100
    allow_delegation: bool = False
    verbose: bool = False
    status: AgentStatus = AgentStatus.ACTIVE
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class TaskDefinition:
    """Task definition with requirements and outputs."""
    task_id: str
    tenant_id: str
    name: str
    description: str
    expected_output: str
    agent_id: str
    tool_ids: List[str] = field(default_factory=list)
    context_task_ids: List[str] = field(default_factory=list)
    async_execution: bool = False
    requires_human_input: bool = False
    output_schema: Optional[Dict[str, Any]] = None
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class CrewDefinition:
    """Crew definition for multi-agent orchestration."""
    crew_id: str
    tenant_id: str
    name: str
    agent_ids: List[str]
    task_ids: List[str]
    process_type: ProcessType = ProcessType.SEQUENTIAL
    manager_model: Optional[str] = None
    max_rpm: Optional[int] = None
    memory_enabled: bool = False
    cache_enabled: bool = False
    verbose: bool = False
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class ToolDefinition:
    """Tool definition with capabilities."""
    tool_id: str
    tenant_id: str
    name: str
    description: str
    tool_type: ToolType
    config: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class ExecutionResult:
    """Result of task/crew execution."""
    execution_id: str
    status: TaskStatus
    output: Any
    error_message: Optional[str] = None
    execution_time: float = 0.0
    token_usage: Optional[Dict[str, int]] = None
    completed_at: Optional[datetime] = None


class MultiTenantAgentCore(BaseCore):
    """
    Multi-tenant agent orchestration core based on AgentCloud patterns.

    Features:
    - Tenant isolation with resource limits
    - Database-driven agent/task/crew management
    - Multiple process types (sequential, hierarchical, consensual)
    - Tool management and assignment
    - Rate limiting and resource controls
    - Execution tracking and monitoring
    """

    def __init__(self):
        super().__init__()
        self.tenants: Dict[str, TenantConfig] = {}
        self.agents: Dict[str, AgentDefinition] = {}
        self.tasks: Dict[str, TaskDefinition] = {}
        self.crews: Dict[str, CrewDefinition] = {}
        self.tools: Dict[str, ToolDefinition] = {}
        self.executions: Dict[str, ExecutionResult] = {}

        # Rate limiting tracking
        self.tenant_request_counts: Dict[str, Dict[datetime, int]] = {}
        self.agent_request_counts: Dict[str, Dict[datetime, int]] = {}

        self.logger = logging.getLogger(__name__)

    async def create_tenant(
        self,
        tenant_id: str,
        name: str,
        max_agents: int = 10,
        max_concurrent_tasks: int = 5,
        max_rpm: int = 100,
        allowed_models: Optional[List[str]] = None
    ) -> TenantConfig:
        """
        Create a new tenant with resource limits.

        Args:
            tenant_id: Unique tenant identifier
            name: Human-readable tenant name
            max_agents: Maximum number of agents allowed
            max_concurrent_tasks: Maximum concurrent task executions
            max_rpm: Maximum requests per minute
            allowed_models: List of allowed model names

        Returns:
            Created tenant configuration
        """
        if tenant_id in self.tenants:
            raise ValueError(f"Tenant {tenant_id} already exists")

        tenant = TenantConfig(
            tenant_id=tenant_id,
            name=name,
            max_agents=max_agents,
            max_concurrent_tasks=max_concurrent_tasks,
            max_rpm=max_rpm,
            allowed_models=allowed_models or []
        )

        self.tenants[tenant_id] = tenant
        self.tenant_request_counts[tenant_id] = {}
        self.logger.info(f"Created tenant {tenant_id}: {name}")
        return tenant

    async def create_agent(
        self,
        tenant_id: str,
        agent_id: str,
        name: str,
        role: str,
        goal: str,
        backstory: str,
        model_name: str,
        **kwargs
    ) -> AgentDefinition:
        """
        Create an agent for a tenant.

        Args:
            tenant_id: Tenant that owns the agent
            agent_id: Unique agent identifier
            name: Agent name
            role: Agent role
            goal: Agent goal
            backstory: Agent backstory
            model_name: LLM model to use
            **kwargs: Additional agent configuration

        Returns:
            Created agent definition
        """
        if tenant_id not in self.tenants:
            raise ValueError(f"Tenant {tenant_id} not found")

        if agent_id in self.agents:
            raise ValueError(f"Agent {agent_id} already exists")

        # Check tenant limits
        tenant_agents = [a for a in self.agents.values() if a.tenant_id == tenant_id]
        if len(tenant_agents) >= self.tenants[tenant_id].max_agents:
            raise ValueError(f"Tenant {tenant_id} has reached maximum agent limit")

        # Check model permissions
        tenant = self.tenants[tenant_id]
        if tenant.allowed_models and model_name not in tenant.allowed_models:
            raise ValueError(f"Model {model_name} not allowed for tenant {tenant_id}")

        agent = AgentDefinition(
            agent_id=agent_id,
            tenant_id=tenant_id,
            name=name,
            role=role,
            goal=goal,
            backstory=backstory,
            model_name=model_name,
            **kwargs
        )

        self.agents[agent_id] = agent
        self.agent_request_counts[agent_id] = {}
        self.logger.info(f"Created agent {agent_id} for tenant {tenant_id}")
        return agent

    async def create_task(
        self,
        tenant_id: str,
        task_id: str,
        name: str,
        description: str,
        expected_output: str,
        agent_id: str,
        **kwargs
    ) -> TaskDefinition:
        """
        Create a task for a tenant.

        Args:
            tenant_id: Tenant that owns the task
            task_id: Unique task identifier
            name: Task name
            description: Task description
            expected_output: Expected output description
            agent_id: Agent assigned to the task
            **kwargs: Additional task configuration

        Returns:
            Created task definition
        """
        if tenant_id not in self.tenants:
            raise ValueError(f"Tenant {tenant_id} not found")

        if agent_id not in self.agents or self.agents[agent_id].tenant_id != tenant_id:
            raise ValueError(f"Agent {agent_id} not found or not owned by tenant {tenant_id}")

        if task_id in self.tasks:
            raise ValueError(f"Task {task_id} already exists")

        task = TaskDefinition(
            task_id=task_id,
            tenant_id=tenant_id,
            name=name,
            description=description,
            expected_output=expected_output,
            agent_id=agent_id,
            **kwargs
        )

        self.tasks[task_id] = task
        self.logger.info(f"Created task {task_id} for tenant {tenant_id}")
        return task

    async def create_crew(
        self,
        tenant_id: str,
        crew_id: str,
        name: str,
        agent_ids: List[str],
        task_ids: List[str],
        process_type: ProcessType = ProcessType.SEQUENTIAL,
        **kwargs
    ) -> CrewDefinition:
        """
        Create a crew for multi-agent orchestration.

        Args:
            tenant_id: Tenant that owns the crew
            crew_id: Unique crew identifier
            name: Crew name
            agent_ids: List of agent IDs in the crew
            task_ids: List of task IDs for the crew
            process_type: Type of crew process
            **kwargs: Additional crew configuration

        Returns:
            Created crew definition
        """
        if tenant_id not in self.tenants:
            raise ValueError(f"Tenant {tenant_id} not found")

        # Validate all agents belong to tenant
        for agent_id in agent_ids:
            if agent_id not in self.agents or self.agents[agent_id].tenant_id != tenant_id:
                raise ValueError(f"Agent {agent_id} not found or not owned by tenant {tenant_id}")

        # Validate all tasks belong to tenant
        for task_id in task_ids:
            if task_id not in self.tasks or self.tasks[task_id].tenant_id != tenant_id:
                raise ValueError(f"Task {task_id} not found or not owned by tenant {tenant_id}")

        if crew_id in self.crews:
            raise ValueError(f"Crew {crew_id} already exists")

        crew = CrewDefinition(
            crew_id=crew_id,
            tenant_id=tenant_id,
            name=name,
            agent_ids=agent_ids,
            task_ids=task_ids,
            process_type=process_type,
            **kwargs
        )

        self.crews[crew_id] = crew
        self.logger.info(f"Created crew {crew_id} for tenant {tenant_id}")
        return crew

    async def check_rate_limits(self, tenant_id: str, agent_id: Optional[str] = None) -> bool:
        """
        Check if rate limits are exceeded.

        Args:
            tenant_id: Tenant to check
            agent_id: Optional agent to check

        Returns:
            True if within limits, False if exceeded
        """
        current_time = datetime.now().replace(second=0, microsecond=0)

        # Check tenant RPM
        tenant_counts = self.tenant_request_counts.get(tenant_id, {})
        tenant_rpm = sum(count for time_key, count in tenant_counts.items()
                        if (current_time - time_key).total_seconds() < 60)

        if tenant_rpm >= self.tenants[tenant_id].max_rpm:
            return False

        # Check agent RPM if specified
        if agent_id:
            agent_counts = self.agent_request_counts.get(agent_id, {})
            agent_rpm = sum(count for time_key, count in agent_counts.items()
                           if (current_time - time_key).total_seconds() < 60)

            if agent_rpm >= self.agents[agent_id].max_rpm:
                return False

        return True

    async def execute_task(self, task_id: str) -> ExecutionResult:
        """
        Execute a single task.

        Args:
            task_id: Task to execute

        Returns:
            Execution result
        """
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")

        task = self.tasks[task_id]
        tenant_id = task.tenant_id

        # Check rate limits
        if not await self.check_rate_limits(tenant_id, task.agent_id):
            raise ValueError(f"Rate limit exceeded for tenant {tenant_id} or agent {task.agent_id}")

        execution_id = str(uuid.uuid4())
        start_time = datetime.now()

        try:
            # Record request for rate limiting
            current_time = datetime.now().replace(second=0, microsecond=0)
            self.tenant_request_counts[tenant_id][current_time] = \
                self.tenant_request_counts[tenant_id].get(current_time, 0) + 1
            self.agent_request_counts[task.agent_id][current_time] = \
                self.agent_request_counts[task.agent_id].get(current_time, 0) + 1

            # Simulate task execution (in real implementation, this would use CrewAI)
            await asyncio.sleep(0.1)  # Simulate work
            output = f"Task {task_id} completed: {task.description}"

            execution_time = (datetime.now() - start_time).total_seconds()

            result = ExecutionResult(
                execution_id=execution_id,
                status=TaskStatus.COMPLETED,
                output=output,
                execution_time=execution_time,
                completed_at=datetime.now()
            )

        except Exception as e:
            result = ExecutionResult(
                execution_id=execution_id,
                status=TaskStatus.FAILED,
                output=None,
                error_message=str(e),
                execution_time=(datetime.now() - start_time).total_seconds(),
                completed_at=datetime.now()
            )

        self.executions[execution_id] = result
        return result

    async def execute_crew(self, crew_id: str) -> List[ExecutionResult]:
        """
        Execute a crew with multiple tasks.

        Args:
            crew_id: Crew to execute

        Returns:
            List of execution results
        """
        if crew_id not in self.crews:
            raise ValueError(f"Crew {crew_id} not found")

        crew = self.crews[crew_id]
        results = []

        if crew.process_type == ProcessType.SEQUENTIAL:
            # Execute tasks sequentially
            for task_id in crew.task_ids:
                result = await self.execute_task(task_id)
                results.append(result)
                if result.status == TaskStatus.FAILED:
                    break  # Stop on failure

        elif crew.process_type == ProcessType.HIERARCHICAL:
            # Execute with manager oversight (simplified)
            for task_id in crew.task_ids:
                result = await self.execute_task(task_id)
                results.append(result)

        else:  # CONSENSUAL
            # Execute all tasks concurrently
            tasks = [self.execute_task(task_id) for task_id in crew.task_ids]
            results = await asyncio.gather(*tasks)

        return results

    async def get_tenant_stats(self, tenant_id: str) -> Dict[str, Any]:
        """Get statistics for a tenant."""
        if tenant_id not in self.tenants:
            raise ValueError(f"Tenant {tenant_id} not found")

        tenant_agents = [a for a in self.agents.values() if a.tenant_id == tenant_id]
        tenant_tasks = [t for t in self.tasks.values() if t.tenant_id == tenant_id]
        tenant_crews = [c for c in self.crews.values() if c.tenant_id == tenant_id]

        return {
            "tenant_id": tenant_id,
            "agent_count": len(tenant_agents),
            "task_count": len(tenant_tasks),
            "crew_count": len(tenant_crews),
            "active_agents": len([a for a in tenant_agents if a.status == AgentStatus.ACTIVE])
        }

    async def cleanup_tenant(self, tenant_id: str):
        """Clean up all resources for a tenant."""
        if tenant_id not in self.tenants:
            return

        # Remove all tenant resources
        self.agents = {k: v for k, v in self.agents.items() if v.tenant_id != tenant_id}
        self.tasks = {k: v for k, v in self.tasks.items() if v.tenant_id != tenant_id}
        self.crews = {k: v for k, v in self.crews.items() if v.tenant_id != tenant_id}
        self.tools = {k: v for k, v in self.tools.items() if v.tenant_id != tenant_id}

        # Clean up rate limiting data
        if tenant_id in self.tenant_request_counts:
            del self.tenant_request_counts[tenant_id]

        # Clean up agent rate limiting
        agent_ids_to_remove = [aid for aid, agent in self.agents.items() if agent.tenant_id == tenant_id]
        for agent_id in agent_ids_to_remove:
            if agent_id in self.agent_request_counts:
                del self.agent_request_counts[agent_id]

        del self.tenants[tenant_id]
        self.logger.info(f"Cleaned up tenant {tenant_id}")

    async def cleanup(self):
        """Cleanup all resources."""
        self.tenants.clear()
        self.agents.clear()
        self.tasks.clear()
        self.crews.clear()
        self.tools.clear()
        self.executions.clear()
        self.tenant_request_counts.clear()
        self.agent_request_counts.clear()
