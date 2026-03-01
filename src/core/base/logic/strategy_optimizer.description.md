# strategy_optimizer

**File**: `src\core\base\logic\strategy_optimizer.py`  
**Type**: Python Module  
**Summary**: 12 classes, 0 functions, 17 imports  
**Lines**: 643  
**Complexity**: 26 (complex)

## Overview

Strategy Optimizer - AutoML framework for pipeline optimization
Based on AutoRAG patterns: threshold filtering, performance measurement, best selection

## Classes (12)

### `OptimizationMetric`

**Inherits from**: Enum

Metrics for evaluating strategy performance

### `StrategyConfig`

Configuration for a strategy

**Methods** (1):
- `__post_init__(self)`

### `PerformanceResult`

Result of evaluating a strategy

**Methods** (1):
- `__post_init__(self)`

### `OptimizationTrial`

A single optimization trial

### `Strategy`

**Inherits from**: ABC

Abstract base class for strategies

**Methods** (2):
- `get_config(self)`
- `name(self)`

### `ThresholdFilter`

Threshold-based filtering for strategy selection
Based on AutoRAG's threshold filtering patterns

**Methods** (3):
- `__init__(self, thresholds)`
- `filter_strategies(self, performance_results)`
- `update_thresholds(self, new_thresholds)`

### `PerformanceMeasurer`

Measures and aggregates strategy performance
Based on AutoRAG's performance measurement patterns

**Methods** (3):
- `__init__(self, metrics)`
- `register_metric_function(self, metric, func)`
- `_default_metric_calculation(self, metric, result, ground_truth, execution_time)`

### `BestSelectionAlgorithm`

**Inherits from**: ABC

Abstract base class for best strategy selection algorithms

**Methods** (1):
- `select_best(self, performance_results, weights)`

### `WeightedAverageSelector`

**Inherits from**: BestSelectionAlgorithm

Select best strategy using weighted average of metrics

**Methods** (2):
- `__init__(self)`
- `select_best(self, performance_results, weights)`

### `ParetoFrontierSelector`

**Inherits from**: BestSelectionAlgorithm

Select best strategy using Pareto frontier (multi-objective optimization)

**Methods** (4):
- `select_best(self, performance_results, weights)`
- `_calculate_pareto_frontier(self, results)`
- `_dominates(self, result1, result2)`
- `_select_from_frontier(self, frontier, weights)`

### `StrategyOptimizer`

AutoML framework for strategy optimization
Based on AutoRAG's strategy optimization patterns

**Methods** (6):
- `__init__(self, threshold_filter, performance_measurer, selection_algorithm)`
- `register_strategy(self, strategy)`
- `unregister_strategy(self, strategy_name)`
- `_calculate_optimization_score(self, result, weights)`
- `get_optimization_history(self, limit)`
- `get_strategy_performance_stats(self, strategy_name)`

### `PipelineStrategy`

**Inherits from**: Strategy

Strategy wrapper for pipeline configurations

**Methods** (3):
- `__init__(self, config)`
- `get_config(self)`
- `name(self)`

## Dependencies

**Imports** (17):
- `abc.ABC`
- `abc.abstractmethod`
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `json`
- `logging`
- `statistics`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- ... and 2 more

---
*Auto-generated documentation*
