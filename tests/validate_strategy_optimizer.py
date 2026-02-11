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

"""
Simple validation script for StrategyOptimizer
"""

import asyncio
import os
import sys
from typing import Any

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.base.logic.strategy_optimizer import (
    StrategyOptimizer, Strategy, StrategyConfig, ThresholdFilter
)


class SimpleStrategy(Strategy):
    """Simple test strategy"""

    def __init__(self, name: str, accuracy: float, latency: float):
        self._name = name
        self._accuracy = accuracy
        self._latency = latency

    async def execute(self, input_data: Any, **kwargs) -> str:
        """Execute strategy with simulated performance"""
        await asyncio.sleep(self._latency)
        # Return a result that simulates the accuracy level
        if self._accuracy >= 0.8:
            return "expected output"  # High accuracy strategies return correct result
        elif self._accuracy >= 0.5:
            return "partial output"   # Medium accuracy strategies return partial result
        else:
            return "wrong output"     # Low accuracy strategies return wrong result

    def get_config(self) -> StrategyConfig:
        return StrategyConfig(
            name=self._name,
            parameters={"accuracy": self._accuracy, "latency": self._latency}
        )

    @property
    def name(self) -> str:
        return self._name


async def test_basic_optimization():
    """Test basic StrategyOptimizer functionality"""
    print("Testing StrategyOptimizer...")

    # Create optimizer
    optimizer = StrategyOptimizer()
    print("✓ Created StrategyOptimizer instance")

    # Create test strategies
    strategies = [
        SimpleStrategy("fast_approximate", 0.7, 0.1),
        SimpleStrategy("accurate_slow", 0.95, 0.8),
        SimpleStrategy("balanced", 0.85, 0.3),
    ]

    print("✓ Created test strategies")

    # Run optimization
    trial = await optimizer.optimize(
        strategies,
        input_data="Test query: What is machine learning?",
        metric_weights={"accuracy": 0.6, "latency": 0.4}
    )

    print(f"✓ Completed optimization trial: {trial.trial_id}")
    print(f"✓ Best strategy: {trial.best_strategy.name}")
    print(".3f")
    print(f"✓ Evaluated {len(trial.performance_results)} strategies")

    # Verify results
    assert trial.best_strategy is not None, "No best strategy selected"
    assert len(trial.performance_results) == 3, "Not all strategies evaluated"
    assert trial.optimization_score > 0, "Invalid optimization score"

    print("✓ Basic optimization test passed")


async def test_threshold_filtering():
    """Test threshold-based filtering"""
    print("\nTesting threshold filtering...")

    optimizer = StrategyOptimizer()
    # Use very lenient thresholds for testing
    optimizer.threshold_filter = ThresholdFilter({"accuracy": 0.1, "latency": 1.0})

    strategies = [
        SimpleStrategy("excellent", 0.95, 0.2),  # Should pass
        SimpleStrategy("too_slow", 0.9, 0.5),     # Should pass
        SimpleStrategy("inaccurate", 0.05, 0.1), # Should fail accuracy threshold
    ]

    trial = await optimizer.optimize(strategies, "test input", "expected output")

    # Debug: print performance results
    print("Performance results:")
    for result in trial.performance_results:
        print(f"  {result.strategy_name}: {result.metrics}, error: {result.error}")

    # Check what passes filtering
    print("Checking filtering logic:")
    for result in trial.performance_results:
        if result.error:
            print(f"  {result.strategy_name}: SKIPPED (error)")
            continue

        passes = True
        for metric, threshold in optimizer.threshold_filter.thresholds.items():
            if metric in result.metrics:
                value = result.metrics[metric]
                if value < threshold:
                    print(f"  {result.strategy_name}: FAIL {metric} {value} < {threshold}")
                    passes = False
                    break
            else:
                print(f"  {result.strategy_name}: FAIL {metric} not in metrics")
                passes = False
                break

        if passes:
            print(f"  {result.strategy_name}: PASS")

    filtered_results = optimizer.threshold_filter.filter_strategies(trial.performance_results)
    print(f"Filtered results: {len(filtered_results)} (from {len(trial.performance_results)})")

    # Should select one of the passing strategies
    assert trial.best_strategy is not None, "No best strategy selected"
    assert trial.best_strategy.name in ["excellent", "too_slow"], f"Unexpected best strategy: {trial.best_strategy.name}"
    print("✓ Threshold filtering test passed")


async def test_pipeline_optimization():
    """Test pipeline configuration optimization"""
    print("\nTesting pipeline optimization...")

    optimizer = StrategyOptimizer()

    # Define pipeline configurations
    pipeline_configs = [
        {
            "name": "simple_rag",
            "type": "rag",
            "retrieval": {"top_k": 3},
            "generation": {"temperature": 0.7}
        },
        {
            "name": "advanced_rag",
            "type": "rag",
            "retrieval": {"top_k": 10, "rerank": True},
            "generation": {"temperature": 0.3, "max_tokens": 500}
        },
        {
            "name": "minimal_rag",
            "type": "rag",
            "retrieval": {"top_k": 1},
            "generation": {"temperature": 1.0}
        }
    ]

    # Evaluation data
    evaluation_data = [
        ("What is Python?", "Python is a high-level programming language"),
        ("How do neural networks work?", "Neural networks process data through layers of interconnected nodes"),
        ("What is machine learning?", "Machine learning is a subset of AI that enables systems to learn from data"),
    ]

    trial = await optimizer.optimize_pipeline(pipeline_configs, evaluation_data)

    print(f"✓ Pipeline optimization completed: {trial.trial_id}")
    print(f"✓ Best pipeline: {trial.best_strategy.name}")
    print(".3f")

    assert trial.best_strategy is not None, "No best pipeline selected"
    assert trial.best_strategy.name in [config["name"] for config in pipeline_configs], "Invalid pipeline selected"

    print("✓ Pipeline optimization test passed")


async def test_performance_statistics():
    """Test performance statistics tracking"""
    print("\nTesting performance statistics...")

    optimizer = StrategyOptimizer()
    strategy = SimpleStrategy("consistent_strategy", 0.85, 0.2)

    # Run multiple trials
    for i in range(5):
        await optimizer.optimize([strategy], f"Test input {i}")

    # Get statistics
    stats = optimizer.get_strategy_performance_stats("consistent_strategy")

    print(f"✓ Collected statistics over {stats['trial_count']} trials")
    print(f"✓ Average execution time: {stats['avg_execution_time']:.3f}s")
    print(f"✓ Accuracy stats: mean={stats['metrics']['accuracy']['mean']:.3f}")

    # Since we're not providing ground truth, accuracy will be 0.5 (default)
    assert stats["trial_count"] == 5, "Incorrect trial count"
    assert stats["evaluation_count"] == 5, "Incorrect evaluation count"
    assert "accuracy" in stats["metrics"], "Accuracy metrics missing"
    assert abs(stats["metrics"]["accuracy"]["mean"] - 0.5) < 0.01, "Accuracy mean should be default 0.5"

    print("✓ Performance statistics test passed")


async def main():
    """Run all validation tests"""
    print("🚀 Starting StrategyOptimizer validation...")

    try:
        await test_basic_optimization()
        await test_threshold_filtering()
        await test_pipeline_optimization()
        await test_performance_statistics()

        print("\n🎉 All StrategyOptimizer tests passed!")
        print("✅ AutoML framework for pipeline optimization is working correctly.")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
