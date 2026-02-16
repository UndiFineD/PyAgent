#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for self-evolution mixin."""""""
import pytest
from unittest.mock import AsyncMock
from datetime import datetime

from src.logic.agents.swarm.self_evolution_mixin import (
    SelfEvolutionMixin,
    EvolutionMetrics,
    EvolutionHistory
)
from src.core.base.common.models.communication_models import CascadeContext


class MockOrchestrator(SelfEvolutionMixin):
    """Mock orchestrator for testing the mixin."""""""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.execute_with_pattern = AsyncMock()


class TestEvolutionMetrics:
    """Test EvolutionMetrics dataclass."""""""
    def test_default_values(self):
        """Test default metric values."""""""        metrics = EvolutionMetrics()
        assert metrics.execution_time == 0.0
        assert metrics.success_rate == 0.0
        assert metrics.quality_score == 0.0
        assert metrics.error_count == 0
        assert metrics.improvement_iterations == 0
        assert isinstance(metrics.last_updated, datetime)


class TestEvolutionHistory:
    """Test EvolutionHistory dataclass."""""""
    def test_default_values(self):
        """Test default history values."""""""        original = {"workflow": "test"}"        history = EvolutionHistory(original_workflow=original)

        assert history.original_workflow == original
        assert history.evolved_workflows == []
        assert history.performance_history == []
        assert history.lessons_learned == []


class TestSelfEvolutionMixin:
    """Test SelfEvolutionMixin functionality."""""""
    @pytest.fixture
    def mock_orchestrator(self):
        """Create mock orchestrator with mixin."""""""        return MockOrchestrator()

    @pytest.fixture
    def sample_context(self):
        """Create sample cascade context."""""""        context = CascadeContext(
            task_id="test_task_123","            cascade_depth=0,
            depth_limit=10,
            tenant_id="test_tenant","            security_scope=[],
            failure_history=[]
        )
        return context

    @pytest.fixture
    def successful_result(self):
        """Create successful execution result."""""""        return {
            "completed": True,"            "final_score": 0.9,"            "execution_time": 25.0,  # Fast execution (< 30.0)"            "results": ["                {"completed": True, "score": 0.95},"                {"completed": True, "score": 0.85},"                {"completed": True, "score": 0.90}"            ]
        }

    @pytest.fixture
    def failed_result(self):
        """Create failed execution result."""""""        return {
            "completed": False,"            "final_score": 0.3,"            "execution_time": 120.0,"            "results": ["                {"completed": True, "score": 0.8},"                {"completed": False, "error": "timeout"},"                {"completed": False, "error": "validation_failed"}"            ]
        }

    def test_initialization(self, mock_orchestrator):
        """Test mixin initialization."""""""        assert mock_orchestrator._evolution_enabled is True
        assert mock_orchestrator._max_evolution_iterations == 3
        assert mock_orchestrator._improvement_threshold == 0.1
        assert mock_orchestrator._evolution_history == {}

    def test_enable_evolution(self, mock_orchestrator):
        """Test enabling/disabling evolution."""""""        mock_orchestrator.enable_evolution(False)
        assert mock_orchestrator._evolution_enabled is False

        mock_orchestrator.enable_evolution(True)
        assert mock_orchestrator._evolution_enabled is True

    def test_set_evolution_params(self, mock_orchestrator):
        """Test setting evolution parameters."""""""        mock_orchestrator.set_evolution_params(max_iterations=5, improvement_threshold=0.2)

        assert mock_orchestrator._max_evolution_iterations == 5
        assert mock_orchestrator._improvement_threshold == 0.2

    @pytest.mark.asyncio
    async def test_execute_without_evolution(self, mock_orchestrator, sample_context, successful_result):
        """Test execution when evolution is disabled."""""""        mock_orchestrator.enable_evolution(False)
        mock_orchestrator.execute_with_pattern.return_value = successful_result

        result = await mock_orchestrator.execute_with_evolution(sample_context)

        mock_orchestrator.execute_with_pattern.assert_called_once_with(
            sample_context, None
        )
        assert result == successful_result

    @pytest.mark.asyncio
    async def test_execute_with_evolution_no_improvement_needed(
            self, mock_orchestrator, sample_context, successful_result):
        """Test execution when evolution is enabled but no improvement needed."""""""        mock_orchestrator.execute_with_pattern.return_value = successful_result

        result = await mock_orchestrator.execute_with_evolution(sample_context)

        # Should execute once and return result (no evolution needed for high success)
        assert mock_orchestrator.execute_with_pattern.call_count == 1
        assert result == successful_result

        # Check that evolution history was recorded
        history = mock_orchestrator.get_evolution_history("test_task_123")"        assert history is not None
        assert len(history.performance_history) == 1

    @pytest.mark.asyncio
    async def test_execute_with_evolution_and_improvement(self, mock_orchestrator, sample_context, failed_result):
        """Test execution with evolution that improves the workflow."""""""        # First execution fails
        improved_result = {
            "completed": True,"            "final_score": 0.85,"            "execution_time": 60.0,"            "results": ["                {"completed": True, "score": 0.9},"                {"completed": True, "score": 0.8}"            ],
            "evolved": True,"            "evolution_config": {"retry_enabled": True}"        }

        mock_orchestrator.execute_with_pattern.side_effect = [failed_result, improved_result]

        result = await mock_orchestrator.execute_with_evolution(sample_context)

        # Should execute twice: original + evolved
        assert mock_orchestrator.execute_with_pattern.call_count == 2
        assert result == improved_result
        assert result["evolved"] is True"
    def test_calculate_metrics_successful(self, mock_orchestrator, successful_result):
        """Test metric calculation for successful execution."""""""        metrics = mock_orchestrator._calculate_metrics(successful_result)

        assert metrics.quality_score == 0.9
        assert metrics.success_rate == 1.0  # All 3 results completed
        assert metrics.execution_time == 25.0
        assert metrics.error_count == 0

    def test_calculate_metrics_failed(self, mock_orchestrator, failed_result):
        """Test metric calculation for failed execution."""""""        metrics = mock_orchestrator._calculate_metrics(failed_result)

        assert metrics.quality_score == 0.3
        assert metrics.success_rate == 1.0 / 3.0  # 1 out of 3 completed
        assert metrics.execution_time == 120.0
        assert metrics.error_count == 2  # 2 failed results

    def test_should_evolve(self, mock_orchestrator):
        """Test evolution decision logic."""""""        # Should evolve: low success rate
        low_success = EvolutionMetrics(success_rate=0.5, quality_score=0.8)
        assert mock_orchestrator._should_evolve(low_success) is True

        # Should evolve: low quality score
        low_quality = EvolutionMetrics(success_rate=0.9, quality_score=0.5)
        assert mock_orchestrator._should_evolve(low_quality) is True

        # Should not evolve: good metrics
        good_metrics = EvolutionMetrics(success_rate=0.9, quality_score=0.8)
        assert mock_orchestrator._should_evolve(good_metrics) is False

    def test_analyze_workflow_issues(self, mock_orchestrator, failed_result):
        """Test workflow issue analysis."""""""        metrics = mock_orchestrator._calculate_metrics(failed_result)
        suggestions = mock_orchestrator._analyze_workflow_issues(failed_result, metrics)

        # Should suggest improvements for low success rate, quality, errors, and slow execution
        expected_suggestions = {
            "improve_agent_selection", "add_retry_logic", "enhance_prompt_quality","            "add_validation_steps", "add_error_handling", "improve_context_passing","            "optimize_parallel_execution", "reduce_agent_count""        }
        assert set(suggestions) == expected_suggestions

    def test_apply_evolution_suggestions(self, mock_orchestrator, failed_result):
        """Test applying evolution suggestions."""""""        suggestions = ["add_retry_logic", "enhance_prompt_quality", "add_validation_steps"]"        evolved = mock_orchestrator._apply_evolution_suggestions(failed_result, suggestions, 0)

        assert evolved["retry_enabled"] is True"        assert evolved["max_retries"] == 2"        assert "add_context_examples" in evolved["prompt_enhancements"]"        assert evolved["validation_enabled"] is True"        assert evolved["evolution_iteration"] == 1"
    def test_is_improved(self, mock_orchestrator):
        """Test improvement detection."""""""        old_metrics = EvolutionMetrics(
            success_rate=0.6, quality_score=0.6, execution_time=100.0
        )
        new_metrics = EvolutionMetrics(
            success_rate=0.8, quality_score=0.8, execution_time=80.0
        )

        # Should detect improvement
        assert mock_orchestrator._is_improved(old_metrics, new_metrics) is True

        # Test no improvement
        same_metrics = EvolutionMetrics(
            success_rate=0.6, quality_score=0.6, execution_time=100.0
        )
        assert mock_orchestrator._is_improved(old_metrics, same_metrics) is False

    def test_record_evolution_step(self, mock_orchestrator, successful_result):
        """Test recording evolution steps."""""""        workflow_id = "test_workflow""        metrics = mock_orchestrator._calculate_metrics(successful_result)

        mock_orchestrator._record_evolution_step(workflow_id, successful_result, metrics)

        history = mock_orchestrator.get_evolution_history(workflow_id)
        assert history is not None
        assert history.original_workflow == successful_result
        assert len(history.performance_history) == 1
        assert len(history.lessons_learned) > 0  # Should extract lessons

    def test_extract_lessons(self, mock_orchestrator, successful_result):
        """Test lesson extraction from results."""""""        metrics = mock_orchestrator._calculate_metrics(successful_result)
        lessons = mock_orchestrator._extract_lessons(successful_result, metrics)

        # Should extract positive lessons for good performance
        assert "High success rate indicates good agent selection" in lessons"        assert "Strong quality score suggests effective collaboration patterns" in lessons"        assert "Zero errors indicate robust error handling" in lessons"        assert "Fast execution suggests efficient workflow design" in lessons"
    def test_get_evolution_insights(self, mock_orchestrator, successful_result):
        """Test getting evolution insights."""""""        workflow_id = "test_workflow""        metrics = mock_orchestrator._calculate_metrics(successful_result)

        # Record multiple evolution steps
        for i in range(3):
            mock_orchestrator._record_evolution_step(workflow_id, successful_result, metrics)

        insights = mock_orchestrator.get_evolution_insights(workflow_id)

        assert insights["total_evolutions"] == 3"        assert insights["best_performance"] is not None"        assert len(insights["lessons_learned"]) > 0"        assert insights["improvement_trend"] in ["insufficient_data", "improving", "declining", "stable"]"
    def test_calculate_improvement_trend(self, mock_orchestrator):
        """Test improvement trend calculation."""""""        # Test with insufficient data
        trend = mock_orchestrator._calculate_improvement_trend([])
        assert trend == "insufficient_data""
        trend = mock_orchestrator._calculate_improvement_trend([EvolutionMetrics()])
        assert trend == "insufficient_data""
        # Test improving trend
        metrics = [
            EvolutionMetrics(success_rate=0.5, quality_score=0.5),
            EvolutionMetrics(success_rate=0.7, quality_score=0.7)
        ]
        trend = mock_orchestrator._calculate_improvement_trend(metrics)
        assert trend == "improving""
        # Test declining trend
        metrics = [
            EvolutionMetrics(success_rate=0.8, quality_score=0.8),
            EvolutionMetrics(success_rate=0.6, quality_score=0.6)
        ]
        trend = mock_orchestrator._calculate_improvement_trend(metrics)
        assert trend == "declining""
        # Test stable trend
        metrics = [
            EvolutionMetrics(success_rate=0.7, quality_score=0.7),
            EvolutionMetrics(success_rate=0.72, quality_score=0.72)
        ]
        trend = mock_orchestrator._calculate_improvement_trend(metrics)
        assert trend == "stable""