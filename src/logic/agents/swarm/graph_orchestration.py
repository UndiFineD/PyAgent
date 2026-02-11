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
Graph-based agent orchestration system inspired by LLM Tornado.

This module implements a sophisticated orchestration framework with:
- Orchestrator (graph): Manages the overall workflow
- Runner (node): Executes individual agent tasks
- Advancer (edge): Handles transitions between runners

Based on patterns from LLM Tornado's orchestration system.
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable, TypeVar, Generic
from datetime import datetime
from enum import Enum


# Simple execution context for orchestration
@dataclass
class ExecutionContext:
    """Simple execution context for orchestration."""
    context_id: str
    parent_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create_root(cls, context_id: str) -> 'ExecutionContext':
        """Create a root execution context."""
        return cls(context_id=context_id)

    def create_child(self, child_id: str) -> 'ExecutionContext':
        """Create a child execution context."""
        return ExecutionContext(
            context_id=child_id,
            parent_id=self.context_id,
            metadata=self.metadata.copy()
        )


logger = logging.getLogger(__name__)


TState = TypeVar('TState', bound='OrchestrationState')


class OrchestrationStatus(Enum):
    """Status of orchestration execution."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class OrchestrationState:
    """Base state for orchestration workflows."""
    status: OrchestrationStatus = OrchestrationStatus.PENDING
    current_runner: Optional[str] = None
    execution_history: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def update_timestamp(self):
        """Update the last modified timestamp."""
        self.updated_at = datetime.now()


@dataclass
class GraphEdge:
    """Represents an edge between runners in the orchestration graph."""
    source_runner: str
    target_runner: str
    condition: Optional[Callable[['OrchestrationResult'], bool]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OrchestrationResult:
    """Result of a runner execution."""
    runner_name: str
    success: bool
    output: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    execution_time: float = 0.0


class OrchestrationRunnable(ABC):
    """Abstract base class for orchestration runners (nodes)."""

    def __init__(self, name: str, description: Optional[str] = None):
        self.name = name
        self.description = description or name
        self.allow_dead_end = False

    @abstractmethod
    async def execute(self, state: OrchestrationState, context: ExecutionContext) -> OrchestrationResult:
        """Execute this runner with the given state and context."""
        pass

    def can_transition(self, result: OrchestrationResult) -> bool:
        """Check if this runner can transition to the next state."""
        return result.success

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"


class OrchestrationAdvancer:
    """
    Handles transitions between runners based on execution results.

    Inspired by LLM Tornado's advancer concept.
    """

    def __init__(self, edges: List[GraphEdge]):
        self.edges = edges

    def get_next_runners(self, current_runner: str, result: OrchestrationResult) -> List[str]:
        """Get the next runners to execute based on the current result."""
        next_runners = []

        for edge in self.edges:
            if edge.source_runner == current_runner:
                # Check condition if specified
                if edge.condition is None or edge.condition(result):
                    next_runners.append(edge.target_runner)

        return next_runners


class OrchestrationGraph(Generic[TState]):
    """
    Immutable orchestration graph definition.

    Based on LLM Tornado's OrchestrationGraph pattern.
    """

    def __init__(
        self,
        runnables: List[OrchestrationRunnable],
        edges: List[GraphEdge],
        entry_runnable: Optional[OrchestrationRunnable] = None,
        exit_runnables: Optional[List[OrchestrationRunnable]] = None,
        initial_state: Optional[TState] = None
    ):
        self.runnables = runnables
        self.edges = edges
        self.entry_runnable = entry_runnable
        self.exit_runnables = exit_runnables or []
        self.initial_state = initial_state or self._create_default_state()

        # Create lookup dictionaries for efficiency
        self._runnable_map = {r.name: r for r in runnables}
        self._advancer = OrchestrationAdvancer(edges)

    def _create_default_state(self) -> TState:
        """Create a default initial state."""
        return OrchestrationState()  # type: ignore

    def get_runnable(self, name: str) -> Optional[OrchestrationRunnable]:
        """Get a runnable by name."""
        return self._runnable_map.get(name)

    def get_next_runners(self, current_runner: str, result: OrchestrationResult) -> List[str]:
        """Get the next runners to execute."""
        return self._advancer.get_next_runners(current_runner, result)

    def is_exit_runnable(self, runnable: OrchestrationRunnable) -> bool:
        """Check if a runnable is an exit point."""
        return runnable in self.exit_runnables


class OrchestrationGraphBuilder(Generic[TState]):
    """
    Fluent builder for creating orchestration graphs.

    Inspired by LLM Tornado's OrchestrationGraphBuilder pattern.
    """

    def __init__(self):
        self._runnables: List[OrchestrationRunnable] = []
        self._edges: List[GraphEdge] = []
        self._entry_runnable: Optional[OrchestrationRunnable] = None
        self._exit_runnables: List[OrchestrationRunnable] = []
        self._initial_state: Optional[TState] = None
        self._is_built = False

    def with_initial_state(self, state: TState) -> 'OrchestrationGraphBuilder[TState]':
        """Set the initial state for the orchestration."""
        if self._is_built:
            raise ValueError("Cannot modify graph after build() has been called.")
        self._initial_state = state
        return self

    def add_runnable(self, runnable: OrchestrationRunnable) -> 'OrchestrationGraphBuilder[TState]':
        """Add a runnable to the graph."""
        if self._is_built:
            raise ValueError("Cannot modify graph after build() has been called.")
        if runnable not in self._runnables:
            self._runnables.append(runnable)
        return self

    def set_entry_runnable(self, runnable: OrchestrationRunnable) -> 'OrchestrationGraphBuilder[TState]':
        """Set the entry point runnable."""
        if self._is_built:
            raise ValueError("Cannot modify graph after build() has been called.")
        self.add_runnable(runnable)
        self._entry_runnable = runnable
        return self

    def set_exit_runnable(
        self,
        runnable: OrchestrationRunnable,
        allow_dead_end: bool = False
    ) -> 'OrchestrationGraphBuilder[TState]':
        """Set an exit point runnable."""
        if self._is_built:
            raise ValueError("Cannot modify graph after build() has been called.")
        self.add_runnable(runnable)
        if allow_dead_end:
            runnable.allow_dead_end = True
        if runnable not in self._exit_runnables:
            self._exit_runnables.append(runnable)
        return self

    def add_edge(
        self,
        source: OrchestrationRunnable,
        target: OrchestrationRunnable,
        condition: Optional[Callable[[OrchestrationResult], bool]] = None
    ) -> 'OrchestrationGraphBuilder[TState]':
        """Add an edge between two runnables."""
        if self._is_built:
            raise ValueError("Cannot modify graph after build() has been called.")
        self.add_runnable(source)
        self.add_runnable(target)

        edge = GraphEdge(
            source_runner=source.name,
            target_runner=target.name,
            condition=condition
        )
        self._edges.append(edge)
        return self

    def build(self) -> OrchestrationGraph[TState]:
        """Build the orchestration graph."""
        if self._is_built:
            raise ValueError("Graph has already been built.")

        if not self._runnables:
            raise ValueError("Graph must have at least one runnable.")

        if self._entry_runnable is None:
            raise ValueError("Graph must have an entry runnable.")

        self._is_built = True

        return OrchestrationGraph(
            runnables=self._runnables,
            edges=self._edges,
            entry_runnable=self._entry_runnable,
            exit_runnables=self._exit_runnables,
            initial_state=self._initial_state
        )


class Orchestrator(Generic[TState]):
    """
    Main orchestrator that executes orchestration graphs.

    Based on LLM Tornado's orchestrator concept.
    """

    def __init__(self, graph: OrchestrationGraph[TState]):
        self.graph = graph
        self._running = False
        self._cancelled = False

    async def execute(
        self,
        initial_context: ExecutionContext,
        max_iterations: int = 100
    ) -> TState:
        """
        Execute the orchestration graph.

        Args:
            initial_context: Initial cascade context
            max_iterations: Maximum number of iterations to prevent infinite loops

        Returns:
            Final orchestration state
        """
        if self._running:
            raise RuntimeError("Orchestrator is already running.")

        self._running = True
        self._cancelled = False

        try:
            state = self.graph.initial_state
            state.status = OrchestrationStatus.RUNNING
            context = initial_context

            current_runners = [self.graph.entry_runnable.name] if self.graph.entry_runnable else []
            iteration = 0

            while current_runners and iteration < max_iterations and not self._cancelled:
                iteration += 1
                next_runners = []

                # Execute runners in parallel if they don't depend on each other
                tasks = []
                for runner_name in current_runners:
                    runner = self.graph.get_runnable(runner_name)
                    if runner:
                        task = self._execute_runner(runner, state, context)
                        tasks.append(task)

                if tasks:
                    results = await asyncio.gather(*tasks, return_exceptions=True)

                    for i, result in enumerate(results):
                        runner_name = current_runners[i]
                        if isinstance(result, Exception):
                            logger.error(f"Runner {runner_name} failed: {result}")
                            state.status = OrchestrationStatus.FAILED
                            state.execution_history.append({
                                "runner": runner_name,
                                "success": False,
                                "error": str(result),
                                "iteration": iteration
                            })
                            return state
                        else:
                            state.execution_history.append({
                                "runner": runner_name,
                                "success": result.success,
                                "output": result.output,
                                "error": result.error,
                                "iteration": iteration
                            })

                            # Check if this runner failed
                            if not result.success:
                                logger.error(f"Runner {runner_name} failed: {result.error}")
                                state.status = OrchestrationStatus.FAILED
                                return state

                            # Get next runners based on this result
                            next_from_this = self.graph.get_next_runners(runner_name, result)
                            next_runners.extend(next_from_this)

                            # Update state
                            state.current_runner = runner_name
                            state.update_timestamp()

                # Remove duplicates and prepare for next iteration
                current_runners = list(set(next_runners))

                # Check if we've reached exit runnables - execute them but don't continue
                has_exit_runnables = any(
                    self.graph.is_exit_runnable(self.graph.get_runnable(name))
                    for name in current_runners if self.graph.get_runnable(name)
                )
                if has_exit_runnables:
                    # Execute exit runnables but don't get their successors
                    exit_tasks = []
                    non_exit_runners = []
                    for runner_name in current_runners:
                        runner = self.graph.get_runnable(runner_name)
                        if runner and self.graph.is_exit_runnable(runner):
                            task = self._execute_runner(runner, state, context)
                            exit_tasks.append((runner_name, task))
                        elif runner:
                            non_exit_runners.append(runner_name)

                    if exit_tasks:
                        exit_results = await asyncio.gather(*[task for _, task in exit_tasks], return_exceptions=True)
                        for (runner_name, _), result in zip(exit_tasks, exit_results):
                            if isinstance(result, Exception):
                                logger.error(f"Exit runner {runner_name} failed: {result}")
                                state.status = OrchestrationStatus.FAILED
                                state.execution_history.append({
                                    "runner": runner_name,
                                    "success": False,
                                    "error": str(result),
                                    "iteration": iteration
                                })
                                return state
                            else:
                                state.execution_history.append({
                                    "runner": runner_name,
                                    "success": result.success,
                                    "output": result.output,
                                    "error": result.error,
                                    "iteration": iteration
                                })
                                state.current_runner = runner_name
                                state.update_timestamp()

                    # Only continue with non-exit runners
                    current_runners = non_exit_runners
                    break

            # Finalize state
            if self._cancelled:
                state.status = OrchestrationStatus.CANCELLED
            elif iteration >= max_iterations:
                state.status = OrchestrationStatus.FAILED
                logger.warning(f"Orchestration exceeded maximum iterations ({max_iterations})")
            else:
                state.status = OrchestrationStatus.COMPLETED

            return state

        finally:
            self._running = False

    async def _execute_runner(
        self,
        runner: OrchestrationRunnable,
        state: TState,
        context: ExecutionContext
    ) -> OrchestrationResult:
        """Execute a single runner."""
        import time
        start_time = time.time()

        try:
            result = await runner.execute(state, context)
            execution_time = time.time() - start_time
            result.execution_time = execution_time
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            return OrchestrationResult(
                runner_name=runner.name,
                success=False,
                error=str(e),
                execution_time=execution_time
            )

    def cancel(self):
        """Cancel the orchestration execution."""
        self._cancelled = True

    @property
    def is_running(self) -> bool:
        """Check if the orchestrator is currently running."""
        return self._running

    @property
    def is_cancelled(self) -> bool:
        """Check if the orchestrator has been cancelled."""
        return self._cancelled


# Example concrete implementations

@dataclass
class AgentTaskState(OrchestrationState):
    """State for agent task orchestration."""
    task_description: str = ""
    assigned_agents: List[str] = field(default_factory=list)
    completed_tasks: List[str] = field(default_factory=list)
    results: Dict[str, Any] = field(default_factory=dict)


class AgentRunner(OrchestrationRunnable):
    """Runner that executes agent tasks."""

    def __init__(self, name: str, agent_function: Callable, **kwargs):
        super().__init__(name, **kwargs)
        self.agent_function = agent_function

    async def execute(self, state: OrchestrationState, context: ExecutionContext) -> OrchestrationResult:
        """Execute the agent function."""
        try:
            # Create a new context for this runner
            runner_context = context.create_child(f"runner_{self.name}")

            result = await self.agent_function(state, runner_context)
            return OrchestrationResult(
                runner_name=self.name,
                success=True,
                output=result,
                metadata={"context_id": runner_context.context_id}
            )
        except Exception as e:
            return OrchestrationResult(
                runner_name=self.name,
                success=False,
                error=str(e)
            )


class ConditionalRunner(OrchestrationRunnable):
    """Runner that executes based on conditions."""

    def __init__(self, name: str, condition_func: Callable[[OrchestrationState], bool],
                 true_runner: OrchestrationRunnable, false_runner: Optional[OrchestrationRunnable] = None, **kwargs):
        super().__init__(name, **kwargs)
        self.condition_func = condition_func
        self.true_runner = true_runner
        self.false_runner = false_runner

    async def execute(self, state: OrchestrationState, context: ExecutionContext) -> OrchestrationResult:
        """Execute based on condition."""
        try:
            condition_result = self.condition_func(state)
            next_runner = self.true_runner if condition_result else self.false_runner

            return OrchestrationResult(
                runner_name=self.name,
                success=True,
                output={"condition": condition_result, "next_runner": next_runner.name if next_runner else None}
            )
        except Exception as e:
            return OrchestrationResult(
                runner_name=self.name,
                success=False,
                error=str(e)
            )


class GraphOrchestrationMixin:
    """
    Mixin to add graph-based orchestration capabilities to PyAgent orchestrators.

    This provides the LLM Tornado-inspired orchestration framework.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._orchestrators: Dict[str, Orchestrator] = {}

    def create_orchestration_builder(self) -> OrchestrationGraphBuilder[OrchestrationState]:
        """Create a new orchestration graph builder."""
        return OrchestrationGraphBuilder[OrchestrationState]()

    def create_agent_task_builder(self) -> OrchestrationGraphBuilder[AgentTaskState]:
        """Create a new agent task orchestration builder."""
        return OrchestrationGraphBuilder[AgentTaskState]()

    def register_orchestrator(self, name: str, orchestrator: Orchestrator):
        """Register an orchestrator by name."""
        self._orchestrators[name] = orchestrator

    async def execute_orchestration(
        self,
        orchestrator_name: str,
        context: ExecutionContext,
        **kwargs
    ) -> OrchestrationState:
        """Execute a registered orchestrator."""
        if orchestrator_name not in self._orchestrators:
            raise ValueError(f"Orchestrator '{orchestrator_name}' not found.")

        orchestrator = self._orchestrators[orchestrator_name]
        return await orchestrator.execute(context, **kwargs)

    def get_orchestrator(self, name: str) -> Optional[Orchestrator]:
        """Get a registered orchestrator by name."""
        return self._orchestrators.get(name)

    def list_orchestrators(self) -> List[str]:
        """List all registered orchestrator names."""
        return list(self._orchestrators.keys())
