# enhanced_strategy_optimizer

**File**: `src\core\base\logic\enhanced_strategy_optimizer.py`  
**Type**: Python Module  
**Summary**: 4 classes, 0 functions, 10 imports  
**Lines**: 372  
**Complexity**: 13 (moderate)

## Overview

Enhanced Strategy Optimizer - AutoRAG-inspired optimization algorithms
Based on AutoRAG's sophisticated strategy selection for multi-metric optimization

## Classes (4)

### `OptimizationStrategy`

**Inherits from**: Enum

Strategy selection algorithms

### `OptimizationResult`

Result of strategy optimization

### `StrategyTrial`

Single strategy trial result

### `EnhancedStrategyOptimizer`

Enhanced strategy optimizer using AutoRAG-inspired algorithms
Supports multiple optimization strategies for multi-metric evaluation

**Methods** (13):
- `__init__(self)`
- `add_trial(self, trial)`
- `optimize_strategies(self, strategy, weights)`
- `_trials_to_data(self)`
- `_get_metric_columns(self, metrics_data)`
- `_optimize_mean(self, strategy_ids, metrics_data)`
- `_optimize_reciprocal_rank(self, strategy_ids, metrics_data)`
- `_optimize_normalize_mean(self, strategy_ids, metrics_data)`
- `_optimize_weighted_sum(self, strategy_ids, metrics_data, weights)`
- `_optimize_pareto_dominance(self, strategy_ids, metrics_data)`
- ... and 3 more methods

## Dependencies

**Imports** (10):
- `dataclasses.dataclass`
- `enum.Enum`
- `logging`
- `numpy`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
