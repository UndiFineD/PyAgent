# Class Breakdown: strategy_optimizer

**File**: `src\core\base\logic\strategy_optimizer.py`  
**Classes**: 12

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `OptimizationMetric`

**Line**: 33  
**Inherits**: Enum  
**Methods**: 0

Metrics for evaluating strategy performance

[TIP] **Suggested split**: Move to `optimizationmetric.py`

---

### 2. `StrategyConfig`

**Line**: 46  
**Methods**: 1

Configuration for a strategy

[TIP] **Suggested split**: Move to `strategyconfig.py`

---

### 3. `PerformanceResult`

**Line**: 59  
**Methods**: 1

Result of evaluating a strategy

[TIP] **Suggested split**: Move to `performanceresult.py`

---

### 4. `OptimizationTrial`

**Line**: 74  
**Methods**: 0

A single optimization trial

[TIP] **Suggested split**: Move to `optimizationtrial.py`

---

### 5. `Strategy`

**Line**: 85  
**Inherits**: ABC  
**Methods**: 2

Abstract base class for strategies

[TIP] **Suggested split**: Move to `strategy.py`

---

### 6. `ThresholdFilter`

**Line**: 105  
**Methods**: 3

Threshold-based filtering for strategy selection
Based on AutoRAG's threshold filtering patterns

[TIP] **Suggested split**: Move to `thresholdfilter.py`

---

### 7. `PerformanceMeasurer`

**Line**: 159  
**Methods**: 3

Measures and aggregates strategy performance
Based on AutoRAG's performance measurement patterns

[TIP] **Suggested split**: Move to `performancemeasurer.py`

---

### 8. `BestSelectionAlgorithm`

**Line**: 238  
**Inherits**: ABC  
**Methods**: 1

Abstract base class for best strategy selection algorithms

[TIP] **Suggested split**: Move to `bestselectionalgorithm.py`

---

### 9. `WeightedAverageSelector`

**Line**: 248  
**Inherits**: BestSelectionAlgorithm  
**Methods**: 2

Select best strategy using weighted average of metrics

[TIP] **Suggested split**: Move to `weightedaverageselector.py`

---

### 10. `ParetoFrontierSelector`

**Line**: 309  
**Inherits**: BestSelectionAlgorithm  
**Methods**: 4

Select best strategy using Pareto frontier (multi-objective optimization)

[TIP] **Suggested split**: Move to `paretofrontierselector.py`

---

### 11. `StrategyOptimizer`

**Line**: 404  
**Methods**: 6

AutoML framework for strategy optimization
Based on AutoRAG's strategy optimization patterns

[TIP] **Suggested split**: Move to `strategyoptimizer.py`

---

### 12. `PipelineStrategy`

**Line**: 588  
**Inherits**: Strategy  
**Methods**: 3

Strategy wrapper for pipeline configurations

[TIP] **Suggested split**: Move to `pipelinestrategy.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
