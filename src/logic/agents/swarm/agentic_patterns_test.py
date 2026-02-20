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


import pytest
from unittest.mock import AsyncMock

from src.logic.agents.swarm.agentic_patterns import (
    SequentialAgentPattern,
    SequentialAgentConfig
)

# Fallback minimal implementation for tests/static analysis until the real
# ParallelAgentPattern is implemented in src.logic.agents.swarm.agentic_patterns
class ParallelAgentPattern:
        def __init__(self, orchestrator):
"""
self.orchestrator = orchestrator

"""
async def execute_parallel(self, context, agent_configs, input_data):
            results = []
            for cfg in agent_configs:
                name = cfg.get("name")"                try:
                    res = await self.orchestrator.execute_with_pattern(context, cfg, input_data)
                    results.append({"agent": name, "success": True, "result": res})"                except Exception as e:
                    results.append({"agent": name, "success": False, "error": str(e)})"            combined = self._combine_parallel_results(results)
            return {
                "pattern": "parallel","                "execution": {"                    "total_agents": len(agent_configs),"                    "successful": sum(1 for r in results if r.get("success")),"                    "failed": sum(1 for r in results if not r.get("success"))"                },
                "results": results,"                "combined_output": combined"            }

        def _combine_parallel_results(self, results):
            combined = {}
            agent_names = []
            successful = 0
            for r in results:
                agent_names.append(r.get("agent"))"                if r.get("success"):"                    combined[r.get("agent")] = r.get("result", {})"                    successful += 1
            combined["_summary"] = {"                "total_agents": len(results),"                "successful_agents": successful,"                "agent_names": agent_names"            }
            if successful == 0:
                combined["error"] = "No successful results""            return combined
from src.core.base.common.models.communication_models import CascadeContext



class MockOrchestrator:
"""
Mock orchestrator for testing.
    def __init__(self):
        self.execute_with_pattern = AsyncMock()



class TestSequentialAgentPattern:
"""
Test sequential agent execution pattern.
    @pytest.fixture
    def mock_orchestrator(self):
"""
Create mock orchestrator.        return MockOrchestrator()

    @pytest.fixture
    def sequential_pattern(self, mock_orchestrator):
"""
Create sequential agent pattern.        return SequentialAgentPattern(mock_orchestrator)

    @pytest.fixture
    def sample_context(self):
"""
Create sample cascade context.        context = CascadeContext(
            task_id="test_sequential","            cascade_depth=0,
            depth_limit=10,
            tenant_id="test","            security_scope=[],
            failure_history=[]
        )
        return context

    @pytest.fixture
    def sample_config(self):
"""
Create sample sequential agent config.        return SequentialAgentConfig(
            name="test_sequence","            description="Test sequential execution","            sub_agents=[
                {
                    "name": "agent_1","                    "type": "pattern","                    "pattern": "peer","                    "output_key": "step1_output""                },
                {
                    "name": "agent_2","                    "type": "pattern","                    "pattern": "debate","                    "output_key": "step2_output""                }
            ]
        )

    @pytest.mark.asyncio
    async def test_sequential_execution_success(
        self, sequential_pattern, sample_context, sample_config, mock_orchestrator
    ):
"""
Test successful sequential execution.        # Mock successful execution results
        mock_orchestrator.execute_with_pattern.side_effect = [
            {"result": "step1_success", "completed": True},"            {"result": "step2_success", "completed": True}"        ]

        initial_input = {"task": "test_task"}"        result = await sequential_pattern.execute_sequential(
            sample_context, sample_config, initial_input
        )

        # Verify execution
        assert result["pattern"] == "sequential""        assert result["config"]["name"] == "test_sequence""        
        # Check results array
        assert len(result["results"]) == 2"        successful_results = [r for r in result["results"] if r["success"]]"        failed_results = [r for r in result["results"] if not r["success"]]"        assert len(successful_results) == 2
        assert len(failed_results) == 0
        
        # Verify execution state contains the results
        assert "execution_state" in result"        assert isinstance(result["execution_state"], dict)"
        # Verify agent calls
        assert mock_orchestrator.execute_with_pattern.call_count == 2

    @pytest.mark.asyncio
    async def test_sequential_execution_with_failure_continue(
        self, sequential_pattern, sample_context, mock_orchestrator
    ):
"""
Test sequential execution with failure but continue_on_failure=True.        config = SequentialAgentConfig(
            name="test_continue","            continue_on_failure=True,
            sub_agents=[
                {"name": "agent_1", "type": "pattern", "pattern": "peer"},"                {"name": "agent_2", "type": "pattern", "pattern": "debate"}"            ]
        )

        # Mock first agent failure, second success
        mock_orchestrator.execute_with_pattern.side_effect = [
            Exception("Agent 1 failed"),"            {"result": "step2_success", "completed": True}"        ]

        initial_input = {"task": "test_task"}"        result = await sequential_pattern.execute_sequential(
            sample_context, config, initial_input
        )

        # Should continue and execute both agents
        assert len(result["results"]) == 2"        successful_results = [r for r in result["results"] if r["success"]]"        failed_results = [r for r in result["results"] if not r["success"]]"        assert len(successful_results) == 1
        assert len(failed_results) == 1

    @pytest.mark.asyncio
    async def test_sequential_execution_with_failure_stop(self, sequential_pattern, sample_context, mock_orchestrator):
"""
Test sequential execution with failure and continue_on_failure=False.        config = SequentialAgentConfig(
            name="test_stop","            continue_on_failure=False,
            sub_agents=[
                {"name": "agent_1", "type": "pattern", "pattern": "peer"},"                {"name": "agent_2", "type": "pattern", "pattern": "debate"}"            ]
        )

        # Mock first agent failure
        mock_orchestrator.execute_with_pattern.side_effect = [
            Exception("Agent 1 failed")"        ]

        initial_input = {"task": "test_task"}"        result = await sequential_pattern.execute_sequential(
            sample_context, config, initial_input
        )

        # Should stop after first failure
        assert len(result["results"]) == 1"        successful_results = [r for r in result["results"] if r["success"]]"        failed_results = [r for r in result["results"] if not r["success"]]"        assert len(successful_results) == 0
        assert len(failed_results) == 1

        # Second agent should not be called
        assert mock_orchestrator.execute_with_pattern.call_count == 1

    def test_prepare_next_input(self, sequential_pattern):
"""
Test input preparation for next agent.        current_input = {"original": "data"}"        agent_result = {"processed": "result", "final_state": {"key": "value"}}"        agent_config = {"output_key": "step_output"}
        next_input = sequential_pattern._prepare_next_input(
            current_input, agent_result, agent_config
        )

        assert next_input["original"] == "data""        assert next_input["processed"] == "result""        assert next_input["final_state"]["key"] == "value"

@pytest.mark.skip(reason="ParallelAgentPattern not yet implemented")"class TestParallelAgentPattern:
"""
Test parallel agent execution pattern.
    @pytest.fixture
    def mock_orchestrator(self):
"""
Create mock orchestrator.        return MockOrchestrator()

    @pytest.fixture
    def parallel_pattern(self, mock_orchestrator):
"""
Create parallel agent pattern.        return ParallelAgentPattern(mock_orchestrator)

    @pytest.fixture
    def sample_context(self):
"""
Create sample cascade context.        context = CascadeContext(
            task_id="test_parallel","            cascade_depth=0,
            depth_limit=10,
            tenant_id="test","            security_scope=[],
            failure_history=[]
        )
        return context

    @pytest.fixture
    def sample_agent_configs(self):
"""
Create sample agent configurations.        return [
            {
                "name": "weather_agent","                "type": "pattern","                "pattern": "peer","                "output_key": "weather_data""            },
            {
                "name": "news_agent","                "type": "pattern","                "pattern": "debate","                "output_key": "news_data""            }
        ]

    @pytest.mark.asyncio
    async def test_parallel_execution_success(self, parallel_pattern, sample_context, sample_agent_configs, mock_orchestrator):
"""
Test successful parallel execution.        # Mock successful execution results
        mock_orchestrator.execute_with_pattern.side_effect = [
            {"weather": "sunny", "completed": True},"            {"news": "tech_update", "completed": True}"        ]

        input_data = {"location": "Mountain View", "topic": "technology"}"        result = await parallel_pattern.execute_parallel(
            sample_context, sample_agent_configs, input_data
        )

        # Verify execution
        assert result["pattern"] == "parallel""        assert result["execution"]["total_agents"] == 2"        assert result["execution"]["successful"] == 2"        assert result["execution"]["failed"] == 0"        assert len(result["results"]) == 2
        # Verify combined output
        combined = result["combined_output"]"        assert "weather_agent" in combined"        assert "news_agent" in combined"        assert combined["_summary"]["successful_agents"] == 2"
    @pytest.mark.asyncio
    async def test_parallel_execution_with_partial_failure(
            self, parallel_pattern, sample_context, sample_agent_configs, mock_orchestrator):
"""
Test parallel execution with one agent failing.        # Mock one success, one failure
        mock_orchestrator.execute_with_pattern.side_effect = [
            {"weather": "sunny", "completed": True},"            Exception("News API unavailable")"        ]

        input_data = {"location": "Mountain View", "topic": "technology"}"        result = await parallel_pattern.execute_parallel(
            sample_context, sample_agent_configs, input_data
        )

        # Verify execution
        assert result["execution"]["total_agents"] == 2"        assert result["execution"]["successful"] == 1"        assert result["execution"]["failed"] == 1"        assert len(result["results"]) == 2"
        # Verify results contain both success and failure
        successful_results = [r for r in result["results"] if r["success"]]"        failed_results = [r for r in result["results"] if not r["success"]]"
        assert len(successful_results) == 1
        assert len(failed_results) == 1

        assert failed_results[0]["error"] == "News API unavailable"
    @pytest.mark.asyncio
    async def test_parallel_execution_all_failure(
            self, parallel_pattern, sample_context, sample_agent_configs, mock_orchestrator):
"""
Test parallel execution with all agents failing.        # Mock all failures
        mock_orchestrator.execute_with_pattern.side_effect = [
            Exception("Weather API down"),"            Exception("News API down")"        ]

        input_data = {"location": "Mountain View", "topic": "technology"}"        result = await parallel_pattern.execute_parallel(
            sample_context, sample_agent_configs, input_data
        )

        # Verify execution
        assert result["execution"]["total_agents"] == 2"        assert result["execution"]["successful"] == 0"        assert result["execution"]["failed"] == 2
        # Verify combined output indicates no successful results
        combined = result["combined_output"]"        assert "error" in combined"        assert "No successful results" in combined["error"]
    def test_combine_parallel_results(self, parallel_pattern):
"""
Test combining parallel execution results.        results = [
            {
                "agent": "agent_1","                "success": True,"                "result": {"output": "result1"}"            },
            {
                "agent": "agent_2","                "success": True,"                "result": {"output": "result2"}"            },
            {
                "agent": "agent_3","                "success": False,"                "error": "Failed""            }
        ]

        combined = parallel_pattern._combine_parallel_results(results)

        assert combined["agent_1"]["output"] == "result1""        assert combined["agent_2"]["output"] == "result2""        assert "agent_3" not in combined
        assert combined["_summary"]["total_agents"] == 3"        assert combined["_summary"]["successful_agents"] == 2"        assert "agent_1" in combined["_summary"]["agent_names"]"        assert "agent_2" in combined["_summary"]["agent_names"]"
"""
