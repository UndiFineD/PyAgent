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

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Tests for graph-based orchestration system."""

import pytest
from typing import Any

from src.logic.agents.swarm.graph_orchestration import (
    OrchestrationState,
    OrchestrationStatus,
    OrchestrationRunnable,
    OrchestrationResult,
    GraphEdge,
    OrchestrationGraph,
    OrchestrationGraphBuilder,
    Orchestrator,
    AgentRunner,
    ConditionalRunner,
    GraphOrchestrationMixin,
    ExecutionContext
)


class MockRunnable(OrchestrationRunnable):
    """Mock runnable for testing."""

    def __init__(self, name: str, result: Any = None, should_fail: bool = False):
        super().__init__(name)
        self.result = result
        self.should_fail = should_fail

    async def execute(self, state: OrchestrationState, context: ExecutionContext) -> OrchestrationResult:
        """Mock execution."""
        if self.should_fail:
            raise Exception("Mock failure")
        return OrchestrationResult(
            runner_name=self.name,
            success=True,
            output=self.result
        )


class TestOrchestrationGraphBuilder:
    """Test the orchestration graph builder."""

    def test_builder_initialization(self):
        """Test builder initialization."""
        builder = OrchestrationGraphBuilder[OrchestrationState]()
        assert builder._runnables == []
        assert builder._edges == []
        assert builder._entry_runnable is None
        assert builder._exit_runnables == []
        assert not builder._is_built

    def test_add_runnable(self):
        """Test adding runnables."""
        builder = OrchestrationGraphBuilder[OrchestrationState]()
        runnable = MockRunnable("test")

        result = builder.add_runnable(runnable)
        assert result is builder
        assert runnable in builder._runnables

    def test_set_entry_runnable(self):
        """Test setting entry runnable."""
        builder = OrchestrationGraphBuilder[OrchestrationState]()
        runnable = MockRunnable("entry")

        result = builder.set_entry_runnable(runnable)
        assert result is builder
        assert builder._entry_runnable is runnable
        assert runnable in builder._runnables

    def test_set_exit_runnable(self):
        """Test setting exit runnable."""
        builder = OrchestrationGraphBuilder[OrchestrationState]()
        runnable = MockRunnable("exit")

        result = builder.set_exit_runnable(runnable)
        assert result is builder
        assert runnable in builder._exit_runnables
        assert runnable in builder._runnables

    def test_add_edge(self):
        """Test adding edges."""
        builder = OrchestrationGraphBuilder[OrchestrationState]()
        source = MockRunnable("source")
        target = MockRunnable("target")

        result = builder.add_edge(source, target)
        assert result is builder
        assert len(builder._edges) == 1
        assert builder._edges[0].source_runner == "source"
        assert builder._edges[0].target_runner == "target"

    def test_build_graph(self):
        """Test building a complete graph."""
        builder = OrchestrationGraphBuilder[OrchestrationState]()

        entry = MockRunnable("entry")
        middle = MockRunnable("middle")
        exit_runnable = MockRunnable("exit")

        builder.set_entry_runnable(entry)
        builder.add_edge(entry, middle)
        builder.set_exit_runnable(exit_runnable)
        builder.add_edge(middle, exit_runnable)

        graph = builder.build()

        assert isinstance(graph, OrchestrationGraph)
        assert graph.entry_runnable is entry
        assert exit_runnable in graph.exit_runnables
        assert len(graph.edges) == 2

    def test_build_after_build_fails(self):
        """Test that building after build fails."""
        builder = OrchestrationGraphBuilder[OrchestrationState]()
        runnable = MockRunnable("test")
        builder.set_entry_runnable(runnable)
        builder.build()

        with pytest.raises(ValueError, match="Graph has already been built"):
            builder.build()

    def test_modify_after_build_fails(self):
        """Test that modifying after build fails."""
        builder = OrchestrationGraphBuilder[OrchestrationState]()
        runnable = MockRunnable("test")
        builder.set_entry_runnable(runnable)
        builder.build()

        with pytest.raises(ValueError, match="Cannot modify graph after build"):
            builder.add_runnable(MockRunnable("new"))


class TestOrchestrationGraph:
    """Test the orchestration graph."""

    def test_graph_initialization(self):
        """Test graph initialization."""
        runnables = [MockRunnable("test")]
        edges = []
        graph = OrchestrationGraph(runnables, edges)

        assert graph.runnables == runnables
        assert graph.edges == edges
        assert graph.entry_runnable is None
        assert graph.exit_runnables == []

    def test_get_runnable(self):
        """Test getting runnable by name."""
        runnable = MockRunnable("test")
        graph = OrchestrationGraph([runnable], [])

        assert graph.get_runnable("test") is runnable
        assert graph.get_runnable("nonexistent") is None

    def test_get_next_runners(self):
        """Test getting next runners."""
        source = MockRunnable("source")
        target1 = MockRunnable("target1")
        target2 = MockRunnable("target2")

        edges = [
            GraphEdge("source", "target1"),
            GraphEdge("source", "target2")
        ]

        graph = OrchestrationGraph([source, target1, target2], edges)
        result = OrchestrationResult("source", True)

        next_runners = graph.get_next_runners("source", result)
        assert set(next_runners) == {"target1", "target2"}

    def test_is_exit_runnable(self):
        """Test checking if runnable is exit."""
        exit_runnable = MockRunnable("exit")
        graph = OrchestrationGraph([], [], exit_runnables=[exit_runnable])

        assert graph.is_exit_runnable(exit_runnable)
        assert not graph.is_exit_runnable(MockRunnable("other"))


class TestOrchestrator:
    """Test the orchestrator."""

    @pytest.mark.asyncio
    async def test_simple_orchestration(self):
        """Test simple orchestration execution."""
        # Create a simple graph: entry -> exit
        entry = MockRunnable("entry", "entry_result")
        exit_runnable = MockRunnable("exit", "exit_result")

        builder = OrchestrationGraphBuilder[OrchestrationState]()
        builder.set_entry_runnable(entry)
        builder.set_exit_runnable(exit_runnable)
        builder.add_edge(entry, exit_runnable)

        graph = builder.build()
        orchestrator = Orchestrator(graph)

        context = ExecutionContext.create_root("test")
        result_state = await orchestrator.execute(context)

        assert result_state.status == OrchestrationStatus.COMPLETED
        assert len(result_state.execution_history) == 2

    @pytest.mark.asyncio
    async def test_orchestration_with_failure(self):
        """Test orchestration with runner failure."""
        entry = MockRunnable("entry", should_fail=True)
        exit_runnable = MockRunnable("exit")

        builder = OrchestrationGraphBuilder[OrchestrationState]()
        builder.set_entry_runnable(entry)
        builder.set_exit_runnable(exit_runnable)
        builder.add_edge(entry, exit_runnable)

        graph = builder.build()
        orchestrator = Orchestrator(graph)

        context = ExecutionContext.create_root("test")
        result_state = await orchestrator.execute(context)

        assert result_state.status == OrchestrationStatus.FAILED
        assert len(result_state.execution_history) == 1
        assert not result_state.execution_history[0]["success"]

    @pytest.mark.asyncio
    async def test_conditional_edges(self):
        """Test conditional edge transitions."""
        entry = MockRunnable("entry")
        success_path = MockRunnable("success")
        failure_path = MockRunnable("failure")

        def success_condition(result: OrchestrationResult) -> bool:
            return result.success

        def failure_condition(result: OrchestrationResult) -> bool:
            return not result.success

        builder = OrchestrationGraphBuilder[OrchestrationState]()
        builder.set_entry_runnable(entry)
        builder.add_edge(entry, success_path, success_condition)
        builder.add_edge(entry, failure_path, failure_condition)
        builder.set_exit_runnable(success_path)
        builder.set_exit_runnable(failure_path)

        graph = builder.build()
        orchestrator = Orchestrator(graph)

        context = ExecutionContext.create_root("test")
        result_state = await orchestrator.execute(context)

        assert result_state.status == OrchestrationStatus.COMPLETED
        # Should have taken the success path
        runner_names = [h["runner"] for h in result_state.execution_history]
        assert "success" in runner_names


class TestAgentRunner:
    """Test the agent runner."""

    @pytest.mark.asyncio
    async def test_agent_runner_success(self):
        """Test successful agent runner execution."""
        async def mock_agent(state, context):
            return "agent_result"

        runner = AgentRunner("test_agent", mock_agent)
        state = OrchestrationState()
        context = ExecutionContext.create_root("test")

        result = await runner.execute(state, context)

        assert result.success
        assert result.runner_name == "test_agent"
        assert result.output == "agent_result"

    @pytest.mark.asyncio
    async def test_agent_runner_failure(self):
        """Test agent runner failure."""
        async def failing_agent(state, context):
            raise Exception("Agent failed")

        runner = AgentRunner("failing_agent", failing_agent)
        state = OrchestrationState()
        context = ExecutionContext.create_root("test")

        result = await runner.execute(state, context)

        assert not result.success
        assert result.error == "Agent failed"


class TestConditionalRunner:
    """Test the conditional runner."""

    @pytest.mark.asyncio
    async def test_conditional_true(self):
        """Test conditional runner with true condition."""
        true_runner = MockRunnable("true_path")
        false_runner = MockRunnable("false_path")

        def condition(state):
            return True

        runner = ConditionalRunner("condition", condition, true_runner, false_runner)
        state = OrchestrationState()
        context = ExecutionContext.create_root("test")

        result = await runner.execute(state, context)

        assert result.success
        assert result.output["condition"] is True
        assert result.output["next_runner"] == "true_path"

    @pytest.mark.asyncio
    async def test_conditional_false(self):
        """Test conditional runner with false condition."""
        true_runner = MockRunnable("true_path")
        false_runner = MockRunnable("false_path")

        def condition(state):
            return False

        runner = ConditionalRunner("condition", condition, true_runner, false_runner)
        state = OrchestrationState()
        context = ExecutionContext.create_root("test")

        result = await runner.execute(state, context)

        assert result.success
        assert result.output["condition"] is False
        assert result.output["next_runner"] == "false_path"


class MockOrchestratorWithMixin(GraphOrchestrationMixin):
    """Mock orchestrator with graph orchestration mixin."""

    pass


class TestGraphOrchestrationMixin:
    """Test the graph orchestration mixin."""

    def test_mixin_initialization(self):
        """Test mixin initialization."""
        orchestrator = MockOrchestratorWithMixin()
        assert hasattr(orchestrator, '_orchestrators')
        assert orchestrator._orchestrators == {}

    def test_create_builders(self):
        """Test creating builders."""
        orchestrator = MockOrchestratorWithMixin()

        builder1 = orchestrator.create_orchestration_builder()
        assert isinstance(builder1, OrchestrationGraphBuilder)

        builder2 = orchestrator.create_agent_task_builder()
        assert isinstance(builder2, OrchestrationGraphBuilder)

    def test_register_and_get_orchestrator(self):
        """Test registering and getting orchestrators."""
        orchestrator = MockOrchestratorWithMixin()

        # Create a simple graph
        builder = orchestrator.create_orchestration_builder()
        runnable = MockRunnable("test")
        builder.set_entry_runnable(runnable)
        builder.set_exit_runnable(runnable)
        graph = builder.build()

        orch = Orchestrator(graph)
        orchestrator.register_orchestrator("test_orch", orch)

        retrieved = orchestrator.get_orchestrator("test_orch")
        assert retrieved is orch

        assert orchestrator.list_orchestrators() == ["test_orch"]

    @pytest.mark.asyncio
    async def test_execute_orchestration(self):
        """Test executing registered orchestration."""
        orchestrator = MockOrchestratorWithMixin()

        # Create and register a simple orchestration
        builder = orchestrator.create_orchestration_builder()
        runnable = MockRunnable("test", "result")
        builder.set_entry_runnable(runnable)
        builder.set_exit_runnable(runnable)
        graph = builder.build()

        orch = Orchestrator(graph)
        orchestrator.register_orchestrator("test", orch)

        context = ExecutionContext.create_root("test")
        result = await orchestrator.execute_orchestration("test", context)

        assert result.status == OrchestrationStatus.COMPLETED
