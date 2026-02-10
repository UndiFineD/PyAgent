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
Strategy Optimizer - AutoML framework for pipeline optimization
Based on AutoRAG patterns: threshold filtering, performance measurement, best selection
"""

import asyncio
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable, Tuple
from enum import Enum
import statistics
from src.core.base.common.models.core_enums import FailureClassification, OptimizationMetric

logger = logging.getLogger(__name__)


# class OptimizationMetric(Enum):  # Removed duplicate definition
#     """Metrics for evaluating strategy performance"""
#     ACCURACY = "accuracy"
#     PRECISION = "precision"
#     RECALL = "recall"
#     F1_SCORE = "f1_score"
#     LATENCY = "latency"
#     THROUGHPUT = "throughput"
#     COST = "cost"
#     ROBUSTNESS = "robustness"


@dataclass
class StrategyConfig:
    """Configuration for a strategy"""
    name: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: float = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()


@dataclass
class PerformanceResult:
    """Result of evaluating a strategy"""
    strategy_name: str
    metrics: Dict[str, float] = field(default_factory=dict)
    execution_time: float = 0.0
    error: Optional[str] = None
    failure_type: Optional[FailureClassification] = None  # Phase 336
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()


@dataclass
class OptimizationTrial:
    """A single optimization trial"""
    trial_id: str
    strategy_configs: List[StrategyConfig]
    performance_results: List[PerformanceResult] = field(default_factory=list)
    best_strategy: Optional[StrategyConfig] = None
    optimization_score: float = 0.0
    completed_at: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class Strategy(ABC):
    """Abstract base class for strategies"""

    @abstractmethod
    async def execute(self, input_data: Any, **kwargs) -> Any:
        """Execute the strategy with given input"""
        pass

    @abstractmethod
    def get_config(self) -> StrategyConfig:
        """Get the strategy configuration"""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Get strategy name"""
        pass


class ThresholdFilter:
    """
    Threshold-based filtering for strategy selection
    Based on AutoRAG's threshold filtering patterns
    """

    def __init__(self, thresholds: Dict[str, float]):
        self.thresholds = thresholds
        # Define which metrics have "higher is better" vs "lower is better"
        self.higher_is_better = {
            "accuracy", "precision", "recall", "f1_score", "throughput", "robustness"
        }
        self.lower_is_better = {
            "latency", "cost"
        }

    def filter_strategies(self, performance_results: List[PerformanceResult]) -> List[PerformanceResult]:
        """Filter strategies based on threshold criteria"""
        filtered = []

        for result in performance_results:
            if result.error:
                continue  # Skip failed strategies

            passes_thresholds = True
            for metric, threshold in self.thresholds.items():
                if metric in result.metrics:
                    value = result.metrics[metric]
                    if metric in self.higher_is_better:
                        # For metrics where higher is better (accuracy, etc.)
                        if value < threshold:
                            passes_thresholds = False
                            break
                    elif metric in self.lower_is_better:
                        # For metrics where lower is better (latency, cost)
                        if value > threshold:
                            passes_thresholds = False
                            break
                    else:
                        # Default: assume higher is better
                        if value < threshold:
                            passes_thresholds = False
                            break

            if passes_thresholds:
                filtered.append(result)

        return filtered

    def update_thresholds(self, new_thresholds: Dict[str, float]):
        """Update filtering thresholds"""
        self.thresholds.update(new_thresholds)


class PerformanceMeasurer:
    """
    Measures and aggregates strategy performance
    Based on AutoRAG's performance measurement patterns
    """

    def __init__(self, metrics: List[OptimizationMetric]):
        self.metrics = metrics
        self.measurement_functions: Dict[str, Callable] = {}

    def register_metric_function(self, metric: str, func: Callable):
        """Register a custom metric measurement function"""
        self.measurement_functions[metric] = func

    async def measure_performance(
        self, strategy: Strategy, input_data: Any,
        ground_truth: Optional[Any] = None, **kwargs
    ) -> PerformanceResult:
        """Measure performance of a strategy"""
        start_time = time.time()

        try:
            # Execute strategy
            result = await strategy.execute(input_data, **kwargs)
            execution_time = time.time() - start_time

            # Calculate metrics
            metrics = {}
            for metric in self.metrics:
                if metric.value in self.measurement_functions:
                    # Use custom measurement function
                    metrics[metric.value] = self.measurement_functions[metric.value](
                        result, ground_truth, **kwargs
                    )
                else:
                    # Use default measurement
                    metrics[metric.value] = self._default_metric_calculation(
                        metric, result, ground_truth, execution_time
                    )

            return PerformanceResult(
                strategy_name=strategy.name,
                metrics=metrics,
                execution_time=execution_time,
                metadata={"input_size": len(str(input_data)) if input_data else 0}
            )

        except Exception as e:
            execution_time = time.time() - start_time

            # Phase 336: Failure Taxonomy Classification
            failure_type = FailureClassification.UNKNOWN
            error_str = str(e).lower()
            if "timeout" in error_str:
                failure_type = FailureClassification.NETWORK_FAILURE
            elif "memory" in error_str or "oom" in error_str:
                failure_type = FailureClassification.RESOURCE_EXHAUSTION
            elif "recursion" in error_str:
                failure_type = FailureClassification.RECURSION_LIMIT
            elif "shard" in error_str:
                failure_type = FailureClassification.SHARD_CORRUPTION
            elif "ai" in error_str or "llm" in error_str:
                failure_type = FailureClassification.AI_ERROR

            return PerformanceResult(
                strategy_name=strategy.name,
                execution_time=execution_time,
                error=str(e),
                failure_type=failure_type
            )

    def _default_metric_calculation(
        self, metric: OptimizationMetric, result: Any, ground_truth: Any, execution_time: float
    ) -> float:
        """Default metric calculations"""
        if metric == OptimizationMetric.LATENCY:
            return execution_time
        elif metric == OptimizationMetric.THROUGHPUT:
            # Assume result size indicates throughput
            return len(str(result)) / execution_time if execution_time > 0 else 0
        elif metric in [OptimizationMetric.ACCURACY, OptimizationMetric.PRECISION,
                       OptimizationMetric.RECALL, OptimizationMetric.F1_SCORE]:
            # Placeholder for classification metrics
            if ground_truth is not None and result is not None:
                # Simple exact match for demonstration
                return 1.0 if str(result).strip() == str(ground_truth).strip() else 0.0
            return 0.5  # Default neutral score
        elif metric == OptimizationMetric.COST:
            # Placeholder cost calculation
            return execution_time * 0.01  # Cost per second
        elif metric == OptimizationMetric.ROBUSTNESS:
            # Placeholder robustness score
            return 0.8  # Default robustness
        else:
            return 0.0


class BestSelectionAlgorithm(ABC):
    """Abstract base class for best strategy selection algorithms"""

    @abstractmethod
    def select_best(
        self, performance_results: List[PerformanceResult], weights: Optional[Dict[str, float]] = None
    ) -> PerformanceResult:
        """Select the best performing strategy"""
        pass


class WeightedAverageSelector(BestSelectionAlgorithm):
    """Select best strategy using weighted average of metrics"""

    def __init__(self):
        # Define which metrics have "higher is better" vs "lower is better"
        self.higher_is_better = {
            "accuracy", "precision", "recall", "f1_score", "throughput", "robustness"
        }
        self.lower_is_better = {
            "latency", "cost"
        }

    def select_best(
        self, performance_results: List[PerformanceResult], weights: Optional[Dict[str, float]] = None
    ) -> PerformanceResult:
        """Select strategy with highest weighted average score"""
        if not performance_results:
            raise ValueError("No performance results provided")

        if weights is None:
            # Default equal weights for all metrics
            all_metrics = set()
            for result in performance_results:
                all_metrics.update(result.metrics.keys())
            weights = {metric: 1.0 / len(all_metrics) for metric in all_metrics}

        best_result = None
        best_score = float('-inf')

        for result in performance_results:
            if result.error:
                continue

            score = 0.0
            total_weight = 0.0

            for metric, weight in weights.items():
                if metric in result.metrics:
                    value = result.metrics[metric]
                    # For lower_is_better metrics, transform to higher_is_better
                    if metric in self.lower_is_better:
                        value = 1.0 / (1.0 + value)  # Bounded transformation: lower value -> higher score
                    score += value * weight
                    total_weight += weight

            if total_weight > 0:
                score /= total_weight

            if score > best_score:
                best_score = score
                best_result = result

        if best_result is None:
            # Return first non-error result if no clear best
            for result in performance_results:
                if not result.error:
                    return result
            return performance_results[0]  # Return any result as fallback

        return best_result


class ParetoFrontierSelector(BestSelectionAlgorithm):
    """Select best strategy using Pareto frontier (multi-objective optimization)"""

    def select_best(
        self, performance_results: List[PerformanceResult], weights: Optional[Dict[str, float]] = None
    ) -> PerformanceResult:
        """Select strategy on Pareto frontier with best compromise"""
        if not performance_results:
            raise ValueError("No performance results provided")

        # Filter out error results
        valid_results = [r for r in performance_results if not r.error]

        if not valid_results:
            return performance_results[0]

        # Find Pareto frontier
        pareto_frontier = self._calculate_pareto_frontier(valid_results)

        if len(pareto_frontier) == 1:
            return pareto_frontier[0]

        # Among Pareto optimal solutions, select one with best weighted score
        weights = weights or {}
        if not weights:
            # Use equal weights for all metrics present
            all_metrics = set()
            for result in pareto_frontier:
                all_metrics.update(result.metrics.keys())
            weights = {metric: 1.0 for metric in all_metrics}

        return self._select_from_frontier(pareto_frontier, weights)

    def _calculate_pareto_frontier(self, results: List[PerformanceResult]) -> List[PerformanceResult]:
        """Calculate Pareto frontier for multi-objective optimization"""
        if not results:
            return []

        frontier = []

        for result in results:
            is_dominated = False

            # Check if this result is dominated by any in frontier
            for frontier_result in frontier:
                if self._dominates(frontier_result, result):
                    is_dominated = True
                    break

            if not is_dominated:
                # Remove any frontier results dominated by this result
                frontier = [f for f in frontier if not self._dominates(result, f)]
                frontier.append(result)

        return frontier

    def _dominates(self, result1: PerformanceResult, result2: PerformanceResult) -> bool:
        """Check if result1 dominates result2"""
        at_least_one_better = False

        # Define which metrics have "lower is better"
        lower_is_better = {"latency", "cost"}

        for metric in set(result1.metrics.keys()) | set(result2.metrics.keys()):
            val1 = result1.metrics.get(metric, 0)
            val2 = result2.metrics.get(metric, 0)

            # Transform lower_is_better metrics
            if metric in lower_is_better:
                val1 = 1.0 / (1.0 + val1)
                val2 = 1.0 / (1.0 + val2)

            if val1 < val2:
                return False  # result1 is worse in at least one metric
            if val1 > val2:
                at_least_one_better = True

        return at_least_one_better

    def _select_from_frontier(
        self, frontier: List[PerformanceResult], weights: Dict[str, float]
    ) -> PerformanceResult:
        """Select best result from Pareto frontier using weighted scoring"""
        best_result = None
        best_score = float('-inf')

        for result in frontier:
            score = sum(result.metrics.get(metric, 0) * weight
                       for metric, weight in weights.items())

            if score > best_score:
                best_score = score
                best_result = result

        return best_result or frontier[0]


class StrategyOptimizer:
    """
    AutoML framework for strategy optimization
    Based on AutoRAG's strategy optimization patterns
    """

    def __init__(self,
                 threshold_filter: Optional[ThresholdFilter] = None,
                 performance_measurer: Optional[PerformanceMeasurer] = None,
                 selection_algorithm: Optional[BestSelectionAlgorithm] = None):
        self.threshold_filter = threshold_filter or ThresholdFilter({})
        self.performance_measurer = performance_measurer or PerformanceMeasurer([
            OptimizationMetric.ACCURACY,
            OptimizationMetric.LATENCY,
            OptimizationMetric.COST
        ])
        self.selection_algorithm = selection_algorithm or WeightedAverageSelector()

        self.optimization_history: List[OptimizationTrial] = []
        self.strategy_registry: Dict[str, Strategy] = {}

    def register_strategy(self, strategy: Strategy):
        """Register a strategy for optimization"""
        self.strategy_registry[strategy.name] = strategy
        logger.info(f"Registered strategy: {strategy.name}")

    def unregister_strategy(self, strategy_name: str):
        """Unregister a strategy"""
        if strategy_name in self.strategy_registry:
            del self.strategy_registry[strategy_name]
            logger.info(f"Unregistered strategy: {strategy_name}")

    async def optimize(
        self, strategies: List[Strategy], input_data: Any,
        ground_truth: Optional[Any] = None, metric_weights: Optional[Dict[str, float]] = None,
        **kwargs
    ) -> OptimizationTrial:
        """
        Run optimization trial across multiple strategies
        Based on AutoRAG's optimization workflow
        """
        trial_id = f"trial_{int(time.time())}_{len(self.optimization_history)}"

        # Create trial
        trial = OptimizationTrial(
            trial_id=trial_id,
            strategy_configs=[s.get_config() for s in strategies]
        )

        logger.info(f"Starting optimization trial: {trial_id}")

        # Measure performance for each strategy
        performance_results = []
        for strategy in strategies:
            logger.debug(f"Evaluating strategy: {strategy.name}")
            result = await self.performance_measurer.measure_performance(
                strategy, input_data, ground_truth, **kwargs
            )
            performance_results.append(result)

        # Apply threshold filtering
        filtered_results = self.threshold_filter.filter_strategies(performance_results)
        logger.info(f"Threshold filtering: {len(performance_results)} -> {len(filtered_results)} strategies")

        # Select best strategy
        if filtered_results:
            best_result = self.selection_algorithm.select_best(filtered_results, metric_weights)
            best_strategy_config = next(
                config for config in trial.strategy_configs
                if config.name == best_result.strategy_name
            )
            trial.best_strategy = best_strategy_config
            trial.optimization_score = self._calculate_optimization_score(best_result, metric_weights)

        trial.performance_results = performance_results
        trial.completed_at = time.time()

        # Store trial in history
        self.optimization_history.append(trial)

        logger.info(f"Completed optimization trial: {trial_id}")
        logger.info(f"Best strategy: {trial.best_strategy.name if trial.best_strategy else 'None'}")

        return trial

    def _calculate_optimization_score(
        self, result: PerformanceResult, weights: Optional[Dict[str, float]]
    ) -> float:
        """Calculate overall optimization score"""
        if weights is None:
            # Equal weights for all metrics
            weights = {metric: 1.0 / len(result.metrics) for metric in result.metrics}

        score = 0.0
        total_weight = 0.0

        for metric, value in result.metrics.items():
            weight = weights.get(metric, 1.0)
            score += value * weight
            total_weight += weight

        return score / total_weight if total_weight > 0 else 0.0

    async def optimize_pipeline(
        self, pipeline_configs: List[Dict[str, Any]], evaluation_data: List[Tuple[Any, Any]], **kwargs
    ) -> OptimizationTrial:
        """
        Optimize a complete pipeline configuration
        Based on AutoRAG's pipeline optimization
        """
        # Convert pipeline configs to strategies
        strategies = []
        for config in pipeline_configs:
            strategy = PipelineStrategy(config)
            strategies.append(strategy)
            self.register_strategy(strategy)

        # Use ensemble of evaluation data for optimization
        combined_input = evaluation_data
        combined_ground_truth = [gt for _, gt in evaluation_data]

        # Run optimization
        trial = await self.optimize(
            strategies, combined_input, combined_ground_truth, **kwargs
        )

        # Cleanup temporary strategies
        for strategy in strategies:
            self.unregister_strategy(strategy.name)

        return trial

    def get_optimization_history(self, limit: Optional[int] = None) -> List[OptimizationTrial]:
        """Get optimization history"""
        history = self.optimization_history
        if limit:
            history = history[-limit:]
        return history

    def get_strategy_performance_stats(self, strategy_name: str) -> Dict[str, Any]:
        """Get performance statistics for a strategy"""
        relevant_trials = [
            trial for trial in self.optimization_history
            if any(result.strategy_name == strategy_name for result in trial.performance_results)
        ]

        if not relevant_trials:
            return {}

        # Collect all performance results for this strategy
        results = []
        for trial in relevant_trials:
            for result in trial.performance_results:
                if result.strategy_name == strategy_name and not result.error:
                    results.append(result)

        if not results:
            return {"error": "No successful performance results found"}

        # Calculate statistics
        stats = {
            "trial_count": len(relevant_trials),
            "evaluation_count": len(results),
            "avg_execution_time": statistics.mean(r.execution_time for r in results),
            "metrics": {}
        }

        # Calculate per-metric statistics
        all_metrics = set()
        for result in results:
            all_metrics.update(result.metrics.keys())

        for metric in all_metrics:
            values = [r.metrics.get(metric, 0) for r in results if metric in r.metrics]
            if values:
                stats["metrics"][metric] = {
                    "mean": statistics.mean(values),
                    "median": statistics.median(values),
                    "std_dev": statistics.stdev(values) if len(values) > 1 else 0,
                    "min": min(values),
                    "max": max(values)
                }

        return stats


class PipelineStrategy(Strategy):
    """Strategy wrapper for pipeline configurations"""

    def __init__(self, config: Dict[str, Any]):
        self._config = config
        self._name = config.get("name", f"pipeline_{id(self)}")

    async def execute(self, input_data: Any, **kwargs) -> Any:
        """Execute pipeline with configuration"""
        # Placeholder implementation - in real usage, this would
        # execute the actual pipeline with the given config
        pipeline_type = self._config.get("type", "generic")

        if pipeline_type == "rag":
            # Simulate RAG pipeline execution
            return await self._execute_rag_pipeline(input_data, **kwargs)
        elif pipeline_type == "classification":
            # Simulate classification pipeline
            return await self._execute_classification_pipeline(input_data, **kwargs)
        else:
            # Generic pipeline simulation
            return f"Executed {pipeline_type} pipeline on input: {str(input_data)[:100]}"

    async def _execute_rag_pipeline(self, input_data: Any, **kwargs) -> str:
        """Simulate RAG pipeline execution"""
        # Simulate retrieval and generation
        retrieval_config = self._config.get("retrieval", {})
        generation_config = self._config.get("generation", {})

        # Simulate processing time based on config complexity
        processing_time = len(str(retrieval_config)) * 0.001 + len(str(generation_config)) * 0.001
        await asyncio.sleep(min(processing_time, 0.1))  # Cap at 100ms for testing

        return f"RAG result: {str(input_data)[:50]}... (retrieved {retrieval_config.get('top_k', 5)} docs)"

    async def _execute_classification_pipeline(self, input_data: Any, **kwargs) -> str:
        """Simulate classification pipeline execution"""
        model_config = self._config.get("model", {})

        # Simulate processing
        await asyncio.sleep(0.05)

        return f"Classification: {model_config.get('type', 'unknown')} predicted class for: {str(input_data)[:50]}"

    def get_config(self) -> StrategyConfig:
        """Get strategy configuration"""
        return StrategyConfig(
            name=self._name,
            parameters=self._config,
            metadata={"type": "pipeline"}
        )

    @property
    def name(self) -> str:
        """Get strategy name"""
        return self._name
