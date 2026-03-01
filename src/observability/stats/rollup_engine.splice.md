# Class Breakdown: rollup_engine

**File**: `src\observability\stats\rollup_engine.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `StatsRollupCalculator`

**Line**: 34  
**Methods**: 4

Calculates metric rollups using pure logic core.

[TIP] **Suggested split**: Move to `statsrollupcalculator.py`

---

### 2. `StatsRollup`

**Line**: 96  
**Methods**: 9

Aggregate metrics into rollup views.

[TIP] **Suggested split**: Move to `statsrollup.py`

---

### 3. `StatsQueryEngine`

**Line**: 210  
**Methods**: 4

Queries metrics with time range and aggregation.

[TIP] **Suggested split**: Move to `statsqueryengine.py`

---

### 4. `CorrelationAnalyzer`

**Line**: 274  
**Methods**: 4

Analyze correlations between metrics.

[TIP] **Suggested split**: Move to `correlationanalyzer.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
