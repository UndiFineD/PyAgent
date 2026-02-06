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
Task Prioritization and Management System

This module implements intelligent task prioritization, assignment, and management
for multi-agent systems. Features include:
- Dynamic priority assignment based on urgency and importance
- Intelligent task routing to appropriate agents
- Workload balancing and resource optimization
- Deadline tracking and escalation mechanisms

Based on patterns from agentic_design_patterns repository.
"""

import asyncio
import heapq
import logging
import threading
import time
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Callable, Tuple, Union
from dataclasses import dataclass, field
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator, ValidationInfo

logger = logging.getLogger(__name__)


class PriorityLevel(Enum):
    """Task priority levels."""
    P0 = 0  # Critical - immediate attention required
    P1 = 1  # High - important but not urgent
    P2 = 2  # Medium - standard priority
    P3 = 3  # Low - nice to have
    P4 = 4  # Defer - can be postponed


class TaskStatus(Enum):
    """Task execution status."""
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    BLOCKED = "blocked"


class TaskType(Enum):
    """Types of tasks that can be managed."""
    CODE_GENERATION = "code_generation"
    CODE_REVIEW = "code_review"
    RESEARCH = "research"
    ANALYSIS = "analysis"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    MAINTENANCE = "maintenance"
    COMMUNICATION = "communication"
    PLANNING = "planning"


class Task(BaseModel):
    """Represents a task in the system."""
    id: str = Field(default_factory=lambda: str(uuid4()), description="Unique task identifier")
    title: str = Field(..., description="Task title")
    description: str = Field(..., description="Detailed task description")
    type: TaskType = Field(..., description="Task category")
    priority: PriorityLevel = Field(default=PriorityLevel.P2, description="Task priority level")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Current task status")

    created_at: datetime = Field(default_factory=datetime.now, description="Task creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    deadline: Optional[datetime] = Field(default=None, description="Task deadline")
    estimated_duration: Optional[int] = Field(default=None, description="Estimated duration in minutes")

    assigned_to: Optional[str] = Field(default=None, description="Assigned agent/worker ID")
    created_by: Optional[str] = Field(default=None, description="Task creator ID")

    tags: List[str] = Field(default_factory=list, description="Task tags for filtering")
    dependencies: List[str] = Field(default_factory=list, description="IDs of prerequisite tasks")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional task metadata")

    @field_validator('deadline')
    @classmethod
    def validate_deadline(cls, v: Optional[datetime], info: ValidationInfo) -> Optional[datetime]:
        if v and v < info.data.get('created_at', datetime.now()):
            raise ValueError('Deadline cannot be in the past')
        return v

    def is_overdue(self) -> bool:
        """Check if task is overdue."""
        if self.deadline and self.status not in [TaskStatus.COMPLETED, TaskStatus.CANCELLED]:
            return datetime.now() > self.deadline
        return False

    def time_remaining(self) -> Optional[timedelta]:
        """Get time remaining until deadline."""
        if self.deadline:
            return self.deadline - datetime.now()
        return None

    def priority_score(self) -> float:
        """Calculate priority score for task ordering."""
        base_score = self.priority.value

        # Boost score for overdue tasks
        if self.is_overdue():
            base_score -= 2  # Higher priority for overdue

        # Boost score for tasks with approaching deadlines
        if self.time_remaining():
            hours_remaining = self.time_remaining().total_seconds() / 3600
            if hours_remaining < 24:  # Less than 24 hours
                base_score -= 1
            elif hours_remaining < 168:  # Less than 1 week
                base_score -= 0.5

        # Boost score for tasks with dependencies
        if self.dependencies:
            base_score -= 0.2

        return base_score


@dataclass(order=True)
class PrioritizedTask:
    """Wrapper for tasks in priority queues."""
    priority_score: float
    task: Task = field(compare=False)

    def __post_init__(self):
        # Ensure proper ordering (lower score = higher priority)
        self.priority_score = self.task.priority_score()


class AgentCapability(BaseModel):
    """Represents an agent's capabilities."""
    agent_id: str
    name: str
    skills: List[TaskType] = Field(default_factory=list)
    current_workload: int = Field(default=0, description="Number of active tasks")
    max_concurrent_tasks: int = Field(default=3, description="Maximum concurrent tasks")
    specialization_score: Dict[TaskType, float] = Field(default_factory=dict, description="Specialization scores 0-1")

    def can_handle_task(self, task: Task) -> bool:
        """Check if agent can handle a specific task."""
        return task.type in self.skills

    def workload_capacity(self) -> float:
        """Get current workload capacity (0-1, where 1 is fully loaded)."""
        if self.max_concurrent_tasks == 0:
            return 1.0
        return self.current_workload / self.max_concurrent_tasks

    def suitability_score(self, task: Task) -> float:
        """Calculate how suitable this agent is for a task."""
        if not self.can_handle_task(task):
            return 0.0

        # Base score from specialization
        base_score = self.specialization_score.get(task.type, 0.5)

        # Adjust for workload (prefer less loaded agents)
        workload_penalty = self.workload_capacity() * 0.3
        adjusted_score = base_score * (1 - workload_penalty)

        return max(0.0, min(1.0, adjusted_score))


class TaskManager:
    """Central task management system."""

    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.task_queue: List[PrioritizedTask] = []
        self.agents: Dict[str, AgentCapability] = {}
        self.task_assignments: Dict[str, str] = {}  # task_id -> agent_id
        self._lock = threading.RLock()
        self._running = False

    def add_task(self, task: Task) -> str:
        """Add a new task to the system."""
        with self._lock:
            self.tasks[task.id] = task
            heapq.heappush(self.task_queue, PrioritizedTask(0, task))
            logger.info(f"Added task: {task.id} - {task.title}")
            return task.id

    def update_task(self, task_id: str, **updates) -> Optional[Task]:
        """Update an existing task."""
        with self._lock:
            task = self.tasks.get(task_id)
            if not task:
                return None

            # Update task fields
            for key, value in updates.items():
                if hasattr(task, key):
                    setattr(task, key, value)

            task.updated_at = datetime.now()
            self.tasks[task_id] = task

            # Re-queue if priority changed
            if 'priority' in updates:
                self._requeue_task(task)

            logger.info(f"Updated task: {task_id}")
            return task

    def remove_task(self, task_id: str) -> bool:
        """Remove a task from the system."""
        with self._lock:
            if task_id not in self.tasks:
                return False

            del self.tasks[task_id]

            # Remove from queue
            self.task_queue = [pt for pt in self.task_queue if pt.task.id != task_id]
            heapq.heapify(self.task_queue)

            # Clean up assignments
            self.task_assignments.pop(task_id, None)

            logger.info(f"Removed task: {task_id}")
            return True

    def assign_task(self, task_id: str, agent_id: str) -> bool:
        """Manually assign a task to an agent."""
        with self._lock:
            task = self.tasks.get(task_id)
            agent = self.agents.get(agent_id)

            if not task or not agent:
                return False

            if not agent.can_handle_task(task):
                return False

            # Update task
            task.assigned_to = agent_id
            task.status = TaskStatus.ASSIGNED
            task.updated_at = datetime.now()

            # Update agent workload
            agent.current_workload += 1

            # Record assignment
            self.task_assignments[task_id] = agent_id

            logger.info(f"Assigned task {task_id} to agent {agent_id}")
            return True

    def auto_assign_tasks(self) -> List[Tuple[str, str]]:
        """Automatically assign pending tasks to suitable agents."""
        assignments = []

        with self._lock:
            # Get unassigned tasks
            unassigned_tasks = [
                pt.task for pt in self.task_queue
                if pt.task.status == TaskStatus.PENDING and not pt.task.assigned_to
            ]

            for task in unassigned_tasks:
                best_agent = self._find_best_agent(task)
                if best_agent:
                    success = self.assign_task(task.id, best_agent.agent_id)
                    if success:
                        assignments.append((task.id, best_agent.agent_id))

        return assignments

    def _find_best_agent(self, task: Task) -> Optional[AgentCapability]:
        """Find the best agent for a task."""
        suitable_agents = [
            agent for agent in self.agents.values()
            if agent.can_handle_task(task) and agent.workload_capacity() < 1.0
        ]

        if not suitable_agents:
            return None

        # Sort by suitability score (highest first)
        suitable_agents.sort(key=lambda a: a.suitability_score(task), reverse=True)
        return suitable_agents[0]

    def complete_task(self, task_id: str, success: bool = True) -> bool:
        """Mark a task as completed."""
        with self._lock:
            task = self.tasks.get(task_id)
            if not task:
                return False

            task.status = TaskStatus.COMPLETED if success else TaskStatus.FAILED
            task.updated_at = datetime.now()

            # Update agent workload
            if task.assigned_to:
                agent = self.agents.get(task.assigned_to)
                if agent:
                    agent.current_workload = max(0, agent.current_workload - 1)

            logger.info(f"Completed task: {task_id} (success: {success})")
            return True

    def get_task_queue(self) -> List[Task]:
        """Get prioritized task queue."""
        with self._lock:
            return [pt.task for pt in sorted(self.task_queue)]

    def get_agent_workload(self) -> Dict[str, Dict[str, Any]]:
        """Get workload information for all agents."""
        with self._lock:
            return {
                agent_id: {
                    "current_workload": agent.current_workload,
                    "max_concurrent_tasks": agent.max_concurrent_tasks,
                    "capacity": agent.workload_capacity(),
                    "active_tasks": [
                        task_id for task_id, assigned_agent in self.task_assignments.items()
                        if assigned_agent == agent_id
                    ]
                }
                for agent_id, agent in self.agents.items()
            }

    def get_overdue_tasks(self) -> List[Task]:
        """Get all overdue tasks."""
        with self._lock:
            return [task for task in self.tasks.values() if task.is_overdue()]

    def register_agent(self, agent: AgentCapability) -> None:
        """Register an agent with the task manager."""
        with self._lock:
            self.agents[agent.agent_id] = agent
            logger.info(f"Registered agent: {agent.agent_id}")

    def unregister_agent(self, agent_id: str) -> None:
        """Unregister an agent."""
        with self._lock:
            if agent_id in self.agents:
                del self.agents[agent_id]
                # Reassign tasks from this agent
                affected_tasks = [
                    task_id for task_id, assigned_agent in self.task_assignments.items()
                    if assigned_agent == agent_id
                ]
                for task_id in affected_tasks:
                    self.task_assignments.pop(task_id, None)
                    task = self.tasks.get(task_id)
                    if task:
                        task.assigned_to = None
                        task.status = TaskStatus.PENDING
                logger.info(f"Unregistered agent: {agent_id}")

    def _requeue_task(self, task: Task) -> None:
        """Re-queue a task with updated priority."""
        # Remove old entries
        self.task_queue = [pt for pt in self.task_queue if pt.task.id != task.id]
        # Add with new priority
        heapq.heappush(self.task_queue, PrioritizedTask(0, task))
        heapq.heapify(self.task_queue)


class TaskScheduler:
    """Background task scheduler for automated task management."""

    def __init__(self, task_manager: TaskManager, check_interval: int = 30):
        self.task_manager = task_manager
        self.check_interval = check_interval
        self._running = False
        self._task: Optional[asyncio.Task] = None

    async def start(self) -> None:
        """Start the scheduler."""
        if self._running:
            return

        self._running = True
        self._task = asyncio.create_task(self._scheduler_loop())
        logger.info("Task scheduler started")

    async def stop(self) -> None:
        """Stop the scheduler."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("Task scheduler stopped")

    async def _scheduler_loop(self) -> None:
        """Main scheduler loop."""
        while self._running:
            try:
                # Auto-assign pending tasks
                assignments = self.task_manager.auto_assign_tasks()
                if assignments:
                    logger.info(f"Auto-assigned {len(assignments)} tasks")

                # Check for overdue tasks and escalate
                overdue_tasks = self.task_manager.get_overdue_tasks()
                for task in overdue_tasks:
                    await self._escalate_overdue_task(task)

                await asyncio.sleep(self.check_interval)

            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")
                await asyncio.sleep(self.check_interval)

    async def _escalate_overdue_task(self, task: Task) -> None:
        """Escalate an overdue task."""
        # Increase priority if not already P0
        if task.priority != PriorityLevel.P0:
            self.task_manager.update_task(task.id, priority=PriorityLevel.P0)
            logger.warning(f"Escalated overdue task {task.id} to P0 priority")

        # Could add notification logic here


# Convenience functions for creating tasks

def create_task(
    title: str,
    description: str,
    task_type: TaskType,
    priority: PriorityLevel = PriorityLevel.P2,
    deadline: Optional[datetime] = None,
    tags: Optional[List[str]] = None,
    dependencies: Optional[List[str]] = None
) -> Task:
    """Create a new task with sensible defaults."""
    return Task(
        title=title,
        description=description,
        type=task_type,
        priority=priority,
        deadline=deadline,
        tags=tags or [],
        dependencies=dependencies or []
    )


def create_agent_capability(
    agent_id: str,
    name: str,
    skills: List[TaskType],
    max_concurrent_tasks: int = 3,
    specialization_scores: Optional[Dict[TaskType, float]] = None
) -> AgentCapability:
    """Create an agent capability profile."""
    return AgentCapability(
        agent_id=agent_id,
        name=name,
        skills=skills,
        max_concurrent_tasks=max_concurrent_tasks,
        specialization_score=specialization_scores or {}
    )


# Example usage patterns

async def example_task_management():
    """Example of using the task management system."""
    # Create task manager
    manager = TaskManager()

    # Register agents
    coder_agent = create_agent_capability(
        "coder_001", "Code Generator",
        skills=[TaskType.CODE_GENERATION, TaskType.CODE_REVIEW],
        specialization_scores={TaskType.CODE_GENERATION: 0.9, TaskType.CODE_REVIEW: 0.8}
    )
    manager.register_agent(coder_agent)

    researcher_agent = create_agent_capability(
        "researcher_001", "Research Specialist",
        skills=[TaskType.RESEARCH, TaskType.ANALYSIS],
        specialization_scores={TaskType.RESEARCH: 0.95, TaskType.ANALYSIS: 0.85}
    )
    manager.register_agent(researcher_agent)

    # Create tasks
    urgent_task = create_task(
        "Fix critical security vulnerability",
        "Address the XSS vulnerability in login form",
        TaskType.CODE_GENERATION,
        priority=PriorityLevel.P0,
        deadline=datetime.now() + timedelta(hours=2)
    )
    manager.add_task(urgent_task)

    research_task = create_task(
        "Research AI trends",
        "Analyze latest developments in AI for Q1 report",
        TaskType.RESEARCH,
        priority=PriorityLevel.P1
    )
    manager.add_task(research_task)

    # Auto-assign tasks
    assignments = manager.auto_assign_tasks()
    print(f"Assigned {len(assignments)} tasks: {assignments}")

    # Start scheduler
    scheduler = TaskScheduler(manager)
    await scheduler.start()

    # Simulate work completion
    await asyncio.sleep(1)
    for task_id, agent_id in assignments:
        manager.complete_task(task_id, success=True)

    await scheduler.stop()


if __name__ == "__main__":
    asyncio.run(example_task_management())
