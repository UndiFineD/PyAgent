# Class Breakdown: prediction_engine

**File**: `src\observability\stats\prediction_engine.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `StatsChangeDetector`

**Line**: 19  
**Methods**: 5

Detects changes in metric values.

[TIP] **Suggested split**: Move to `statschangedetector.py`

---

### 2. `StatsForecaster`

**Line**: 72  
**Methods**: 6

Forecasts future metric values.

[TIP] **Suggested split**: Move to `statsforecaster.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
