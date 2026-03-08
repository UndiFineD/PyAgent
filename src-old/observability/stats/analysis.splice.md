# Class Breakdown: analysis

**File**: `src\observability\stats\analysis.py`  
**Classes**: 16

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ProfileStats`

**Line**: 54  
**Methods**: 0

Statistics for a single function call profile.

[TIP] **Suggested split**: Move to `profilestats.py`

---

### 2. `ProfilingCore`

**Line**: 63  
**Methods**: 4

Pure logic for cProfile aggregation and bottleneck analysis.

[TIP] **Suggested split**: Move to `profilingcore.py`

---

### 3. `FleetMetrics`

**Line**: 96  
**Methods**: 0

Consolidated metrics for a fleet of agents.

[TIP] **Suggested split**: Move to `fleetmetrics.py`

---

### 4. `StabilityCore`

**Line**: 105  
**Methods**: 6

Pure logic for calculating fleet stability and reasoning coherence.

Phase 14 Rust Optimizations:
- calculate_variance_rust: Fast variance calculation for stasis detection

[TIP] **Suggested split**: Move to `stabilitycore.py`

---

### 5. `DerivedMetricCalculator`

**Line**: 171  
**Methods**: 3

Calculate derived metrics from dependencies using safe AST evaluation.

[TIP] **Suggested split**: Move to `derivedmetriccalculator.py`

---

### 6. `CorrelationAnalyzer`

**Line**: 218  
**Methods**: 4

Analyze correlations between metrics.

[TIP] **Suggested split**: Move to `correlationanalyzer.py`

---

### 7. `FormulaEngineCore`

**Line**: 269  
**Methods**: 3

Pure logic core for formula calculations.

[TIP] **Suggested split**: Move to `formulaenginecore.py`

---

### 8. `FormulaEngine`

**Line**: 315  
**Methods**: 3

Orchestrates formula definition and calculation.

[TIP] **Suggested split**: Move to `formulaengine.py`

---

### 9. `TokenCostCore`

**Line**: 333  
**Methods**: 1

Core logic for calculating token costs.

[TIP] **Suggested split**: Move to `tokencostcore.py`

---

### 10. `TokenCostEngine`

**Line**: 346  
**Methods**: 2

Service for managing token costs.

[TIP] **Suggested split**: Move to `tokencostengine.py`

---

### 11. `ModelFallbackCore`

**Line**: 357  
**Methods**: 2

Logic for determining model fallback chains.

[TIP] **Suggested split**: Move to `modelfallbackcore.py`

---

### 12. `ModelFallbackEngine`

**Line**: 376  
**Methods**: 2

Service for handling model fallbacks.

[TIP] **Suggested split**: Move to `modelfallbackengine.py`

---

### 13. `StatsRollupCalculator`

**Line**: 388  
**Methods**: 3

Calculate rolled-up statistics over time intervals.

[TIP] **Suggested split**: Move to `statsrollupcalculator.py`

---

### 14. `StatsForecaster`

**Line**: 421  
**Methods**: 1

Basic forecasting logic for metrics.

[TIP] **Suggested split**: Move to `statsforecaster.py`

---

### 15. `ABComparator`

**Line**: 435  
**Methods**: 2

Compare sets of metrics for A/B testing.

[TIP] **Suggested split**: Move to `abcomparator.py`

---

### 16. `ResourceMonitor`

**Line**: 460  
**Methods**: 2

Monitor system resources.

[TIP] **Suggested split**: Move to `resourcemonitor.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
