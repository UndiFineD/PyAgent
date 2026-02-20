#!/usr/bin/env python3
"""Minimal Crew Orchestrator implementation used for tests."""
from __future__ import annotations


import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set


class AgentRole(Enum):
    LEAD = "lead"
    SPECIALIST = "specialist"
    REVIEWER = "reviewer"
    COORDINATOR = "coordinator"


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass
class AgentConfig:
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
    name: str
    description: str
    expected_output: str
    agent_name: str
    context_tasks: List[str] = field(default_factory=list)
    output_file: Optional[str] = None
    async_execution: bool = False


@dataclass
class TaskResult:
    task_name: str
    status: TaskStatus
    output: Any
    error: Optional[str] = None
    execution_time: float = 0.0
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class CrewAgent:
    def __init__(self, config: AgentConfig, llm_provider: Optional[Any] = None):
        self.config = config
        self.llm_provider = llm_provider
        self.logger = logging.getLogger(f"{__name__}.{config.name}")
        self.task_history: List[TaskResult] = []

    async def execute_task(self, task: TaskConfig, context: Dict[str, Any]) -> TaskResult:
        start = datetime.now()
        result = TaskResult(task_name=task.name, status=TaskStatus.RUNNING, output=None, started_at=start)
        try:
            # Simple deterministic mock output
            output = f"Task {task.name} executed by {self.config.name}"
            result.output = output
            result.status = TaskStatus.COMPLETED
            result.completed_at = datetime.now()
            result.execution_time = (result.completed_at - start).total_seconds()
        except Exception as e:
            result.status = TaskStatus.FAILED
            result.error = str(e)
            result.completed_at = datetime.now()
        self.task_history.append(result)
        return result


class CrewOrchestrator:
    def __init__(self) -> None:
        self.agents: Dict[str, CrewAgent] = {}
        self.tasks: Dict[str, TaskConfig] = {}
        self.task_results: Dict[str, TaskResult] = {}
        self.logger = logging.getLogger(__name__)

    def add_agent(self, agent: CrewAgent) -> None:
        self.agents[agent.config.name] = agent

    def add_task(self, task: TaskConfig) -> None:
        self.tasks[task.name] = task

    async def execute_crew(self, initial_context: Optional[Dict[str, Any]] = None) -> Dict[str, TaskResult]:
        context = initial_context or {}
        pending = set(self.tasks.keys())
        completed: Set[str] = set()

        while pending:
            executable = [t for t in pending if all(dep in completed for dep in self.tasks[t].context_tasks)]
            if not executable:
                break
            coros = []
            for name in executable:
                task = self.tasks[name]
                agent = self.agents.get(task.agent_name)
                if not agent:
                    self.logger.error("Agent not found: %s", task.agent_name)
                    pending.remove(name)
                    continue
                coros.append(agent.execute_task(task, context))
            results = await asyncio.gather(*coros, return_exceptions=True)
            for name, res in zip(executable, results):
                if isinstance(res, Exception):
                    self.logger.error("Task failed: %s", res)
                    pending.remove(name)
                    continue
                self.task_results[name] = res
                completed.add(name)
                pending.remove(name)
                context[name] = res.output

        return self.task_results


__all__ = [
    "AgentRole",
    "TaskStatus",
    "AgentConfig",
    "TaskConfig",
    "TaskResult",
    "CrewAgent",
    "CrewOrchestrator",
]
