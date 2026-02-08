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
Enhanced Strategy Optimizer - AutoRAG-inspired optimization algorithms
Based on AutoRAG's sophisticated strategy selection for multi-metric optimization
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class OptimizationStrategy(Enum):
    """Strategy selection algorithms"""
    MEAN = "mean"                    # Simple average across metrics
    RECIPROCAL_RANK = "rank"         # Reciprocal Rank fusion
    NORMALIZE_MEAN = "normalize_mean" # Normalized mean combination
    WEIGHTED_SUM = "weighted_sum"    # Weighted combination
    PARETO_DOMINANCE = "pareto"      # Multi-objective optimization


@dataclass
class OptimizationResult:
    """Result of strategy optimization"""
    best_strategy_index: int
    best_score: float
    scores: List[float]
    metadata: Dict[str, Any]
    strategy_name: str


@dataclass
class StrategyTrial:
    """Single strategy trial result"""
    strategy_id: str
    metrics: Dict[str, float]
    metadata: Dict[str, Any] = None


class EnhancedStrategyOptimizer:
    """
    Enhanced strategy optimizer using AutoRAG-inspired algorithms
    Supports multiple optimization strategies for multi-metric evaluation
    """

    def __init__(self):
        self.trial_history: List[StrategyTrial] = []

    def add_trial(self, trial: StrategyTrial):
        """Add a strategy trial result"""
        self.trial_history.append(trial)

    def optimize_strategies(self,
                          strategy: OptimizationStrategy = OptimizationStrategy.RECIPROCAL_RANK,
                          weights: Optional[Dict[str, float]] = None) -> OptimizationResult:
        """
        Optimize strategies using specified algorithm

        Args:
            strategy: Optimization algorithm to use
            weights: Optional weights for weighted sum strategy

        Returns:
            OptimizationResult with best strategy and scores
        """
        if not self.trial_history:
            raise ValueError("No strategy trials available for optimization")

        # Convert trials to data structures
        strategy_ids, metrics_data = self._trials_to_data()

        if strategy == OptimizationStrategy.MEAN:
            return self._optimize_mean(strategy_ids, metrics_data)
        elif strategy == OptimizationStrategy.RECIPROCAL_RANK:
            return self._optimize_reciprocal_rank(strategy_ids, metrics_data)
        elif strategy == OptimizationStrategy.NORMALIZE_MEAN:
            return self._optimize_normalize_mean(strategy_ids, metrics_data)
        elif strategy == OptimizationStrategy.WEIGHTED_SUM:
            return self._optimize_weighted_sum(strategy_ids, metrics_data, weights or {})
        elif strategy == OptimizationStrategy.PARETO_DOMINANCE:
            return self._optimize_pareto_dominance(strategy_ids, metrics_data)
        else:
            raise ValueError(f"Unknown optimization strategy: {strategy}")

    def _trials_to_data(self) -> Tuple[List[str], List[Dict[str, float]]]:
        """Convert trial history to data structures"""
        strategy_ids = []
        metrics_data = []

        for trial in self.trial_history:
            strategy_ids.append(trial.strategy_id)
            metrics_data.append(trial.metrics)

        return strategy_ids, metrics_data

    def _get_metric_columns(self, metrics_data: List[Dict[str, float]]) -> List[str]:
        """Get all metric column names"""
        all_keys = set()
        for metrics in metrics_data:
            all_keys.update(metrics.keys())
        return sorted(list(all_keys))

    def _optimize_mean(self, strategy_ids: List[str], metrics_data: List[Dict[str, float]]) -> OptimizationResult:
        """Simple mean-based optimization"""
        metric_cols = self._get_metric_columns(metrics_data)

        # Calculate mean across all metrics for each strategy
        mean_scores = []
        for i, metrics in enumerate(metrics_data):
            metric_values = [metrics.get(col, 0.0) for col in metric_cols]
            mean_score = sum(metric_values) / len(metric_values) if metric_values else 0.0
            mean_scores.append(mean_score)

        best_idx = mean_scores.index(max(mean_scores))

        return OptimizationResult(
            best_strategy_index=best_idx,
            best_score=mean_scores[best_idx],
            scores=mean_scores,
            metadata={'metric_contributions': metrics_data},
            strategy_name='mean'
        )

    def _optimize_reciprocal_rank(self, strategy_ids: List[str], metrics_data: List[Dict[str, float]]) -> OptimizationResult:
        """Reciprocal Rank fusion optimization"""
        metric_cols = self._get_metric_columns(metrics_data)

        # Create ranking matrix
        rankings = []
        for col in metric_cols:
            values = [metrics.get(col, 0.0) for metrics in metrics_data]
            # Sort indices by value (descending)
            sorted_indices = sorted(range(len(values)), key=lambda i: values[i], reverse=True)
            # Create rank dictionary
            rank_dict = {idx: rank + 1 for rank, idx in enumerate(sorted_indices)}
            rankings.append([rank_dict[i] for i in range(len(values))])

        # Convert to reciprocal ranks and sum
        rr_scores = []
        for i in range(len(metrics_data)):
            rr_sum = sum(1.0 / rankings[j][i] for j in range(len(metric_cols)))
            rr_scores.append(rr_sum)

        best_idx = rr_scores.index(max(rr_scores))

        return OptimizationResult(
            best_strategy_index=best_idx,
            best_score=rr_scores[best_idx],
            scores=rr_scores,
            metadata={
                'rankings': rankings,
                'reciprocal_ranks': [[1.0 / rank for rank in col_ranks] for col_ranks in rankings]
            },
            strategy_name='reciprocal_rank'
        )

    def _optimize_normalize_mean(self, strategy_ids: List[str], metrics_data: List[Dict[str, float]]) -> OptimizationResult:
        """Normalized mean optimization"""
        metric_cols = self._get_metric_columns(metrics_data)

        # Get min/max for each metric
        mins = {}
        maxs = {}
        for col in metric_cols:
            values = [metrics.get(col, 0.0) for metrics in metrics_data]
            mins[col] = min(values)
            maxs[col] = max(values)

        # Normalize and sum
        normalized_scores = []
        for i, metrics in enumerate(metrics_data):
            normalized_sum = 0.0
            for col in metric_cols:
                value = metrics.get(col, 0.0)
                min_val = mins[col]
                max_val = maxs[col]
                if max_val > min_val:
                    normalized = (value - min_val) / (max_val - min_val)
                else:
                    normalized = 0.5
                normalized_sum += normalized
            normalized_scores.append(normalized_sum)

        best_idx = normalized_scores.index(max(normalized_scores))

        return OptimizationResult(
            best_strategy_index=best_idx,
            best_score=normalized_scores[best_idx],
            scores=normalized_scores,
            metadata={
                'normalized_metrics': normalized_scores,
                'original_ranges': {col: {'min': mins[col], 'max': maxs[col]} for col in metric_cols}
            },
            strategy_name='normalize_mean'
        )

    def _optimize_weighted_sum(self, strategy_ids: List[str], metrics_data: List[Dict[str, float]], weights: Dict[str, float]) -> OptimizationResult:
        """Weighted sum optimization"""
        metric_cols = self._get_metric_columns(metrics_data)

        # Set default weights if not provided
        if not weights:
            weights = {col: 1.0 / len(metric_cols) for col in metric_cols}

        # Normalize weights
        total_weight = sum(weights.values())
        normalized_weights = {k: v / total_weight for k, v in weights.items()}

        # Calculate weighted sum
        weighted_scores = []
        weighted_components = []

        for i, metrics in enumerate(metrics_data):
            weighted_sum = 0.0
            components = {}
            for col in metric_cols:
                weight = normalized_weights.get(col, 1.0 / len(metric_cols))
                value = metrics.get(col, 0.0)
                weighted_sum += value * weight
                components[col] = value * weight
            weighted_scores.append(weighted_sum)
            weighted_components.append(components)

        best_idx = weighted_scores.index(max(weighted_scores))

        return OptimizationResult(
            best_strategy_index=best_idx,
            best_score=weighted_scores[best_idx],
            scores=weighted_scores,
            metadata={
                'weights_used': normalized_weights,
                'weighted_components': weighted_components
            },
            strategy_name='weighted_sum'
        )

    def _optimize_pareto_dominance(self, strategy_ids: List[str], metrics_data: List[Dict[str, float]]) -> OptimizationResult:
        """Pareto dominance-based multi-objective optimization"""
        metric_cols = self._get_metric_columns(metrics_data)

        def dominates(idx_a, idx_b):
            """Check if strategy A dominates strategy B (higher is better)"""
            metrics_a = metrics_data[idx_a]
            metrics_b = metrics_data[idx_b]
            at_least_one_better = False

            for col in metric_cols:
                val_a = metrics_a.get(col, 0.0)
                val_b = metrics_b.get(col, 0.0)
                if val_a < val_b:  # A worse in this metric
                    return False
                if val_a > val_b:  # A better in this metric
                    at_least_one_better = True
            return at_least_one_better

        # Find Pareto front (non-dominated solutions)
        pareto_front = []
        for i in range(len(metrics_data)):
            is_dominated = False
            for j in range(len(metrics_data)):
                if i != j and dominates(j, i):
                    is_dominated = True
                    break
            if not is_dominated:
                pareto_front.append(i)

        # Among Pareto front, select one with best average performance
        if pareto_front:
            pareto_scores = []
            for idx in pareto_front:
                metric_values = [metrics_data[idx].get(col, 0.0) for col in metric_cols]
                avg_score = sum(metric_values) / len(metric_values) if metric_values else 0.0
                pareto_scores.append((idx, avg_score))

            best_idx, best_score = max(pareto_scores, key=lambda x: x[1])
        else:
            # Fallback to mean optimization
            mean_scores = []
            for i, metrics in enumerate(metrics_data):
                metric_values = [metrics.get(col, 0.0) for col in metric_cols]
                mean_score = sum(metric_values) / len(metric_values) if metric_values else 0.0
                mean_scores.append(mean_score)
            best_idx = mean_scores.index(max(mean_scores))
            best_score = mean_scores[best_idx]

        # Calculate scores for all strategies (distance to Pareto front)
        scores = []
        for i in range(len(metrics_data)):
            if i in pareto_front:
                # On Pareto front - use average score
                metric_values = [metrics_data[i].get(col, 0.0) for col in metric_cols]
                scores.append(sum(metric_values) / len(metric_values) if metric_values else 0.0)
            else:
                # Calculate minimum distance to Pareto front
                min_distance = float('inf')
                for p_idx in pareto_front:
                    distance = 0
                    for col in metric_cols:
                        val_i = metrics_data[i].get(col, 0.0)
                        val_p = metrics_data[p_idx].get(col, 0.0)
                        distance += (val_i - val_p) ** 2
                    distance = distance ** 0.5
                    min_distance = min(min_distance, distance)
                scores.append(-min_distance)  # Negative distance as score

        return OptimizationResult(
            best_strategy_index=best_idx,
            best_score=best_score,
            scores=scores,
            metadata={
                'pareto_front_indices': pareto_front,
                'pareto_front_size': len(pareto_front),
                'dominance_analysis': True
            },
            strategy_name='pareto_dominance'
        )

    def get_optimization_history(self) -> List[Dict[str, Any]]:
        """Get history of all optimization runs"""
        return [
            {
                'strategy_id': trial.strategy_id,
                'metrics': trial.metrics,
                'metadata': trial.metadata
            }
            for trial in self.trial_history
        ]

    def clear_history(self):
        """Clear trial history"""
        self.trial_history.clear()

    def get_best_strategies(self, top_k: int = 5,
                          strategy: OptimizationStrategy = OptimizationStrategy.RECIPROCAL_RANK) -> List[Dict[str, Any]]:
        """Get top-k best strategies"""
        if not self.trial_history:
            return []

        result = self.optimize_strategies(strategy)

        # Sort by scores
        strategy_scores = list(enumerate(result.scores))
        strategy_scores.sort(key=lambda x: x[1], reverse=True)

        top_strategies = []
        for idx, score in strategy_scores[:top_k]:
            trial = self.trial_history[idx]
            top_strategies.append({
                'strategy_id': trial.strategy_id,
                'score': score,
                'rank': len(top_strategies) + 1,
                'metrics': trial.metrics,
                'metadata': trial.metadata
            })

        return top_strategies