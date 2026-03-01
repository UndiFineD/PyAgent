# Class Breakdown: ab_engine

**File**: `src\observability\stats\ab_engine.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ABComparisonResult`

**Line**: 31  
**Methods**: 0

Result of comparing two metric groups.

[TIP] **Suggested split**: Move to `abcomparisonresult.py`

---

### 2. `ABSignificanceResult`

**Line**: 40  
**Methods**: 0

Result of A/B statistical significance calculation.

[TIP] **Suggested split**: Move to `absignificanceresult.py`

---

### 3. `ABComparison`

**Line**: 49  
**Methods**: 0

A / B comparison between code versions.

[TIP] **Suggested split**: Move to `abcomparison.py`

---

### 4. `ABComparisonEngine`

**Line**: 61  
**Methods**: 5

Compare stats between different code versions (A / B testing).

[TIP] **Suggested split**: Move to `abcomparisonengine.py`

---

### 5. `ABComparator`

**Line**: 130  
**Methods**: 2

Compares A/B test metrics.

[TIP] **Suggested split**: Move to `abcomparator.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
