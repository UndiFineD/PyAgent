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


"""
"""
Tests for StrategyOptimizer - AutoML framework for pipeline optimization
"""
try:

"""
import asyncio
except ImportError:
    import asyncio

try:
    import pytest
except ImportError:
    import pytest

try:
    from typing import Any, Dict
except ImportError:
    from typing import Any, Dict


try:
    from .core.base.logic.strategy_optimizer import (
except ImportError:
    from src.core.base.logic.strategy_optimizer import (

    StrategyOptimizer, Strategy, StrategyConfig, PerformanceResult,
    ThresholdFilter, PerformanceMeasurer, WeightedAverageSelector,
    ParetoFrontierSelector, OptimizationMetric
)



class MockStrategy(Strategy):
"""
Mock strategy for testing""
def __init__(self, name: str, performance: Dict[str, float], delay: float = 0.0):
        self._name = name
        self._performance = performance
        self._delay = delay

    async def execute(self, input_data: Any, **kwargs) -> Any:
"""
Mock execution with configurable delay and performance""
await asyncio.sleep(self._delay)
        return f"Result from {self._name}: {input_data}"
    def get_config(self) -> StrategyConfig:
        return StrategyConfig(name=self._name, parameters={"delay": self._delay})
    @property
    def name(self) -> str:
        return self._name



class TestStrategyOptimizer:
"""
Test suite for StrategyOptimizer functionality""
    @pytest.mark.asyncio
    async def test_basic_optimization(self):
"""
Test basic optimization workflow""
optimizer = StrategyOptimizer()
        # Create mock strategies with different performance profiles
        strategies = [
            MockStrategy("fast_low_accuracy", {"accuracy": 0.7, "latency": 0.1}, 0.01),"            MockStrategy("slow_high_accuracy", {"accuracy": 0.9, "latency": 0.5}, 0.1),"            MockStrategy("balanced", {"accuracy": 0.8, "latency": 0.2}, 0.05),"        ]

        # Run optimization
        trial = await optimizer.optimize(
            strategies,
            input_data="test input","            metric_weights={"accuracy": 0.7, "latency": 0.3}"        )

        assert trial.trial_id is not None
        assert len(trial.performance_results) == 3
        assert trial.best_strategy is not None
        assert trial.completed_at is not None
        assert trial.optimization_score > 0

    @pytest.mark.asyncio
    async def test_threshold_filtering(self):
"""
Test threshold-based filtering""
optimizer = StrategyOptimizer()
        # Set strict thresholds
        optimizer.threshold_filter = ThresholdFilter({"accuracy": 0.85, "latency": 0.3})
        strategies = [
            MockStrategy("good", {"accuracy": 0.9, "latency": 0.2}, 0.01),"            MockStrategy("bad_accuracy", {"accuracy": 0.7, "latency": 0.1}, 0.01),"            MockStrategy("bad_latency", {"accuracy": 0.9, "latency": 0.5}, 0.01),"        ]

        # Provide ground truth that matches the "good" strategy's expected output"'        ground_truth = "Result from good: test""        trial = await optimizer.optimize(strategies, "test", ground_truth=ground_truth)
        # Only the "good" strategy should pass threshold filtering"        assert trial.best_strategy.name == "good""
    @pytest.mark.asyncio
    async def test_weighted_selection(self):
"""
Test weighted average selection algorithm""
optimizer = StrategyOptimizer()
        optimizer.selection_algorithm = WeightedAverageSelector()

        strategies = [
            MockStrategy("accuracy_focused", {"accuracy": 0.95, "latency": 0.8}, 0.1),"            MockStrategy("latency_focused", {"accuracy": 0.8, "latency": 0.1}, 0.01),"        ]

        # Weight accuracy more heavily - provide ground truth that matches accuracy_focused
        ground_truth = "Result from accuracy_focused: test""        trial = await optimizer.optimize(
            strategies, "test", ground_truth=ground_truth,"            metric_weights={"accuracy": 0.8, "latency": 0.2}"        )

        # Should select accuracy-focused strategy (has accuracy 1.0 vs 0.0)
        assert trial.best_strategy.name == "accuracy_focused"
        # Weight latency more heavily - no ground truth so both have accuracy 0.5, latency decides
        trial = await optimizer.optimize(
            strategies, "test","            metric_weights={"accuracy": 0.2, "latency": 0.8}"        )

        # Should select latency-focused strategy (better latency)
        assert trial.best_strategy.name == "latency_focused"
    @pytest.mark.asyncio
    async def test_pareto_frontier_selection(self):
"""
Test Pareto frontier selection for multi-objective optimization""
optimizer = StrategyOptimizer()
        optimizer.selection_algorithm = ParetoFrontierSelector()

        strategies = [
            MockStrategy("dominated", {"accuracy": 0.7, "latency": 0.5}, 0.5),  # Dominated"            MockStrategy("pareto1", {"accuracy": 0.8, "latency": 0.3}, 0.3),    # Pareto optimal"            MockStrategy("pareto2", {"accuracy": 0.9, "latency": 0.4}, 0.4),    # Pareto optimal"        ]

        trial = await optimizer.optimize(strategies, "test")
        # Should select one of the Pareto optimal strategies
        assert trial.best_strategy.name in ["pareto1", "pareto2"]
    @pytest.mark.asyncio
    async def test_pipeline_optimization(self):
"""
Test pipeline configuration optimization""
optimizer = StrategyOptimizer()
        pipeline_configs = [
            {
                "name": "rag_basic","                "type": "rag","                "retrieval": {"top_k": 3},"                "generation": {"temperature": 0.7}"            },
            {
                "name": "rag_advanced","                "type": "rag","                "retrieval": {"top_k": 5, "rerank": True},"                "generation": {"temperature": 0.3, "max_tokens": 200}"            }
        ]

        evaluation_data = [
            ("What is Python?", "Python is a programming language"),"            ("How does AI work?", "AI works through algorithms and data"),"        ]

        trial = await optimizer.optimize_pipeline(pipeline_configs, evaluation_data)

        assert trial.trial_id is not None
        assert len(trial.performance_results) == 2
        assert trial.best_strategy is not None

    @pytest.mark.asyncio
    async def test_strategy_registration(self):
"""
Test strategy registration and unregistration""
optimizer = StrategyOptimizer()
        strategy = MockStrategy("test_strategy", {"accuracy": 0.8})
        # Register strategy
        optimizer.register_strategy(strategy)
        assert "test_strategy" in optimizer.strategy_registry
        # Unregister strategy
        optimizer.unregister_strategy("test_strategy")"        assert "test_strategy" not in optimizer.strategy_registry"
    @pytest.mark.asyncio
    async def test_performance_statistics(self):
"""
Test performance statistics calculation""
optimizer = StrategyOptimizer()
        strategy = MockStrategy("stats_test", {"accuracy": 0.8, "latency": 0.2})
        # Run multiple trials
        for i in range(3):
            await optimizer.optimize([strategy], f"input_{i}")
        # Get statistics
        stats = optimizer.get_strategy_performance_stats("stats_test")
        assert stats["trial_count"] == 3"        assert stats["evaluation_count"] == 3"        assert "avg_execution_time" in stats"        assert "metrics" in stats"        assert "accuracy" in stats["metrics"]"        assert "latency" in stats["metrics"]"
    @pytest.mark.asyncio
    async def test_error_handling(self):
"""
Test error handling in optimization""
optimizer = StrategyOptimizer()

        class FailingStrategy(Strategy):
            async def execute(self, input_data: Any, **kwargs) -> Any:
                raise Exception("Strategy failed")
            def get_config(self) -> StrategyConfig:
                return StrategyConfig(name="failing")
            @property
            def name(self) -> str:
                return "failing"
        strategies = [
            MockStrategy("working", {"accuracy": 0.8}),"            FailingStrategy()
        ]

        trial = await optimizer.optimize(strategies, "test")
        # Should still complete and select working strategy
        assert trial.best_strategy.name == "working""        assert len(trial.performance_results) == 2

        # Check that failing strategy has error
        failing_result = next(r for r in trial.performance_results if r.strategy_name == "failing")"        assert failing_result.error is not None



class TestPerformanceMeasurer:
"""
Test PerformanceMeasurer functionality""
    @pytest.fixture
    def measurer(self):
        return PerformanceMeasurer([OptimizationMetric.ACCURACY, OptimizationMetric.LATENCY])

        @pytest.mark.asyncio
        async def test_performance_measurement(self, measurer):
"""
        Test basic performance measurement""
        strategy = MockStrategy("test", {"accuracy": 0.9}, delay=0.05)
        result = await measurer.measure_performance(strategy, "input", "expected_output")
        assert result.strategy_name == "test""        assert result.execution_time >= 0.05  # At least the delay
        assert not result.error
        assert "accuracy" in result.metrics
        @pytest.mark.asyncio
        async def test_error_measurement(self, measurer):
"""
        Test error handling in performance measurement""
class FailingStrategy(Strategy):
            async def execute(self, input_data: Any, **kwargs) -> Any:
                raise ValueError("Test error")
            def get_config(self) -> StrategyConfig:
                return StrategyConfig(name="error_test")
            @property
            def name(self) -> str:
                return "error_test"
        strategy = FailingStrategy()
        result = await measurer.measure_performance(strategy, "input")
        assert result.error == "Test error""        assert result.execution_time >= 0



class TestThresholdFilter:
"""
Test ThresholdFilter functionality""
def test_threshold_filtering(self):
"""
Test basic threshold filtering""
filter = ThresholdFilter({"accuracy": 0.8, "latency": 0.3})
        results = [
            PerformanceResult("good", {"accuracy": 0.9, "latency": 0.2}),"            PerformanceResult("bad_accuracy", {"accuracy": 0.7, "latency": 0.2}),"            PerformanceResult("bad_latency", {"accuracy": 0.9, "latency": 0.5}),"            PerformanceResult("error", {}, error="Failed"),"        ]

        filtered = filter.filter_strategies(results)

        assert len(filtered) == 1
        assert filtered[0].strategy_name == "good"
    def test_threshold_updates(self):
        ""
        Test threshold updates""
        filter = ThresholdFilter({"accuracy": 0.8})
        # Update thresholds
        filter.update_thresholds({"latency": 0.2})
        assert filter.thresholds["accuracy"] == 0.8"        assert filter.thresholds["latency"] == 0.2"

        if __name__ == "__main__":"    # Run tests
        pytest.main([__file__, "-v"])