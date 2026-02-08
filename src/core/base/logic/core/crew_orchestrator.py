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
CrewAI-style Multi-Agent Orchestration System

Inspired by CrewAI patterns from .external/action repository.
Implements role-based agent coordination with task dependencies and context sharing.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class AgentRole(Enum):
    """Agent roles in the crew orchestration"""
    LEAD = "lead"
    SPECIALIST = "specialist"
    REVIEWER = "reviewer"
    COORDINATOR = "coordinator"


class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass
class AgentConfig:
    """Configuration for a crew agent"""
    name: str
    role: AgentRole
    goal: str
    backstory: str
    skills: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    max_iterations: int = 5
    allow_delegation: bool = False


@dataclass
class TaskConfig:
    """Configuration for a crew task"""
    name: str
    description: str
    expected_output: str
    agent_name: str
    context_tasks: List[str] = field(default_factory=list)  # Dependencies
    output_file: Optional[str] = None
    async_execution: bool = False


@dataclass
class TaskResult:
    """Result of a task execution"""
    task_name: str
    status: TaskStatus
    output: Any
    error: Optional[str] = None
    execution_time: float = 0.0
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class CrewAgent:
    """
    A CrewAI-style agent with role-based capabilities.

    Based on patterns from .external/action repository.
    """

    def __init__(self, config: AgentConfig, llm_provider: Optional[Any] = None):
        self.config = config
        self.llm_provider = llm_provider
        self.logger = logging.getLogger(f"{__name__}.{config.name}")
        self.task_history: List[TaskResult] = []

    async def execute_task(self, task: TaskConfig, context: Dict[str, Any]) -> TaskResult:
        """
        Execute a task with given context.

        Args:
            task: Task configuration
            context: Context from dependent tasks

        Returns:
            TaskResult with execution outcome
        """
        start_time = datetime.now()
        result = TaskResult(
            task_name=task.name,
            status=TaskStatus.RUNNING,
            output=None,
            started_at=start_time
        )

        try:
            self.logger.info(f"Agent {self.config.name} executing task: {task.name}")

            # Build prompt with context
            prompt = self._build_task_prompt(task, context)

            # Execute task (simplified - in real implementation would use LLM)
            if self.llm_provider:
                output = await self.llm_provider.generate(prompt)
            else:
                # Mock execution for demonstration
                output = f"Task {task.name} completed by {self.config.name}"

            result.output = output
            result.status = TaskStatus.COMPLETED
            result.completed_at = datetime.now()
            result.execution_time = (result.completed_at - start_time).total_seconds()

            # Save output to file if specified
            if task.output_file:
                await self._save_output_to_file(task.output_file, output)

        except Exception as e:
            self.logger.error(f"Task {task.name} failed: {str(e)}")
            result.status = TaskStatus.FAILED
            result.error = str(e)
            result.completed_at = datetime.now()
            result.execution_time = (result.completed_at - start_time).total_seconds()

        self.task_history.append(result)
        return result

    def _build_task_prompt(self, task: TaskConfig, context: Dict[str, Any]) -> str:
        """Build execution prompt with context and agent configuration."""
        prompt_parts = [
            f"You are {self.config.name}, a {self.config.role.value}.",
            f"Your goal: {self.config.goal}",
            f"Your backstory: {self.config.backstory}",
            "",
            f"Task: {task.description}",
            f"Expected output: {task.expected_output}",
        ]

        if context:
            prompt_parts.append("")
            prompt_parts.append("Context from previous tasks:")
            for ctx_task, ctx_output in context.items():
                prompt_parts.append(f"- {ctx_task}: {str(ctx_output)[:200]}...")

        return "\n".join(prompt_parts)

    async def _save_output_to_file(self, file_path: str, content: str):
        """Save task output to file."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.logger.info(f"Output saved to {file_path}")
        except Exception as e:
            self.logger.error(f"Failed to save output to {file_path}: {str(e)}")


class CrewOrchestrator:
    """
    Orchestrates multi-agent task execution with dependencies.

    Inspired by CrewAI task coordination patterns.
    """

    def __init__(self):
        self.agents: Dict[str, CrewAgent] = {}
        self.tasks: Dict[str, TaskConfig] = {}
        self.task_results: Dict[str, TaskResult] = {}
        self.logger = logging.getLogger(__name__)

    def add_agent(self, agent: CrewAgent):
        """Add an agent to the crew."""
        self.agents[agent.config.name] = agent
        self.logger.info(f"Added agent: {agent.config.name}")

    def add_task(self, task: TaskConfig):
        """Add a task to the crew."""
        self.tasks[task.name] = task
        self.logger.info(f"Added task: {task.name}")

    async def execute_crew(self, initial_context: Optional[Dict[str, Any]] = None) -> Dict[str, TaskResult]:
        """
        Execute all tasks in the crew with proper dependency resolution.

        Args:
            initial_context: Initial context for task execution

        Returns:
            Dictionary of task results
        """
        context = initial_context or {}
        completed_tasks: Set[str] = set()
        pending_tasks = set(self.tasks.keys())

        while pending_tasks:
            executable_tasks = self._get_executable_tasks(pending_tasks, completed_tasks)

            if not executable_tasks:
                # Check for circular dependencies or blocked tasks
                self.logger.error("No executable tasks found. Possible circular dependency or blocked tasks.")
                break

            # Execute tasks (can be parallel if async_execution is enabled)
            execution_tasks = []
            for task_name in executable_tasks:
                task = self.tasks[task_name]
                agent = self.agents.get(task.agent_name)

                if not agent:
                    self.logger.error(f"Agent {task.agent_name} not found for task {task_name}")
                    continue

                # Build task context from completed dependencies
                task_context = {}
                for dep_task in task.context_tasks:
                    if dep_task in self.task_results:
                        task_context[dep_task] = self.task_results[dep_task].output

                # Merge with global context
                task_context.update(context)

                execution_tasks.append(self._execute_single_task(agent, task, task_context))

            # Wait for all executable tasks to complete
            results = await asyncio.gather(*execution_tasks, return_exceptions=True)

            # Process results
            for task_name, result in zip(executable_tasks, results):
                if isinstance(result, Exception):
                    self.logger.error(f"Task execution failed: {result}")
                    continue

                task_result = result
                self.task_results[task_name] = task_result
                completed_tasks.add(task_name)
                pending_tasks.remove(task_name)

                # Update context with task output
                context[task_name] = task_result.output

        return self.task_results

    def _get_executable_tasks(self, pending_tasks: Set[str], completed_tasks: Set[str]) -> List[str]:
        """Get tasks that can be executed (all dependencies satisfied)."""
        executable = []

        for task_name in pending_tasks:
            task = self.tasks[task_name]
            dependencies_satisfied = all(dep in completed_tasks for dep in task.context_tasks)

            if dependencies_satisfied:
                executable.append(task_name)

        return executable

    async def _execute_single_task(self, agent: CrewAgent, task: TaskConfig, context: Dict[str, Any]) -> TaskResult:
        """Execute a single task."""
        return await agent.execute_task(task, context)

    def get_crew_status(self) -> Dict[str, Any]:
        """Get current status of the crew execution."""
        return {
            "total_agents": len(self.agents),
            "total_tasks": len(self.tasks),
            "completed_tasks": len([r for r in self.task_results.values() if r.status == TaskStatus.COMPLETED]),
            "failed_tasks": len([r for r in self.task_results.values() if r.status == TaskStatus.FAILED]),
            "pending_tasks": len(self.tasks) - len(self.task_results),
            "task_results": {name: {
                "status": result.status.value,
                "execution_time": result.execution_time,
                "error": result.error
            } for name, result in self.task_results.items()}
        }


# Example usage function
async def create_engineering_crew() -> CrewOrchestrator:
    """
    Create an engineering crew similar to the action repository example.

    Returns:
        Configured CrewOrchestrator
    """
    crew = CrewOrchestrator()

    # Create agents
    engineering_lead = CrewAgent(AgentConfig(
        name="engineering_lead",
        role=AgentRole.LEAD,
        goal="Direct engineering work and create detailed designs",
        backstory="Seasoned engineering lead with expertise in system design",
        skills=["system_design", "architecture", "planning"]
    ))

    backend_engineer = CrewAgent(AgentConfig(
        name="backend_engineer",
        role=AgentRole.SPECIALIST,
        goal="Write clean, efficient Python code",
        backstory="Experienced Python engineer who follows design specifications",
        skills=["python", "backend", "api_design"]
    ))

    frontend_engineer = CrewAgent(AgentConfig(
        name="frontend_engineer",
        role=AgentRole.SPECIALIST,
        goal="Create simple, effective UIs",
        backstory="UI/UX expert skilled in Gradio interfaces",
        skills=["ui_design", "gradio", "user_experience"]
    ))

    test_engineer = CrewAgent(AgentConfig(
        name="test_engineer",
        role=AgentRole.REVIEWER,
        goal="Write comprehensive unit tests",
        backstory="QA expert who creates thorough test suites",
        skills=["testing", "pytest", "quality_assurance"]
    ))

    # Add agents to crew
    crew.add_agent(engineering_lead)
    crew.add_agent(backend_engineer)
    crew.add_agent(frontend_engineer)
    crew.add_agent(test_engineer)

    # Create tasks with dependencies
    design_task = TaskConfig(
        name="design_task",
        description="Create detailed design for a Python module",
        expected_output="Detailed design document with classes and methods",
        agent_name="engineering_lead",
        output_file="output/design.md"
    )

    code_task = TaskConfig(
        name="code_task",
        description="Implement the designed Python module",
        expected_output="Working Python module",
        agent_name="backend_engineer",
        context_tasks=["design_task"],
        output_file="output/module.py"
    )

    frontend_task = TaskConfig(
        name="frontend_task",
        description="Create Gradio UI for the backend module",
        expected_output="Gradio application file",
        agent_name="frontend_engineer",
        context_tasks=["code_task"],
        output_file="output/app.py"
    )

    test_task = TaskConfig(
        name="test_task",
        description="Write unit tests for the module",
        expected_output="Test file with comprehensive coverage",
        agent_name="test_engineer",
        context_tasks=["code_task"],
        output_file="output/test_module.py"
    )

    # Add tasks to crew
    crew.add_task(design_task)
    crew.add_task(code_task)
    crew.add_task(frontend_task)
    crew.add_task(test_task)

    return crew