# Class Breakdown: MetricsCore

**File**: `src\observability\stats\MetricsCore.py`  
**Classes**: 7

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `TokenCostResult`

**Line**: 36  
**Methods**: 0

Result of token cost calculation.

[TIP] **Suggested split**: Move to `tokencostresult.py`

---

### 2. `TokenCostCore`

**Line**: 45  
**Methods**: 3

Pure token cost calculation (Rust-convertible).

Calculates costs based on model pricing without I/O.

[TIP] **Suggested split**: Move to `tokencostcore.py`

---

### 3. `ModelFallbackCore`

**Line**: 145  
**Methods**: 3

Pure logic for model selection and fallback (Rust-convertible).

[TIP] **Suggested split**: Move to `modelfallbackcore.py`

---

### 4. `DerivedMetricCalculator`

**Line**: 224  
**Methods**: 7

Calculate derived metrics from dependencies (pure calculation).

[TIP] **Suggested split**: Move to `derivedmetriccalculator.py`

---

### 5. `StatsRollupCore`

**Line**: 372  
**Methods**: 9

Pure statistics rollup calculations (Rust-convertible).

[TIP] **Suggested split**: Move to `statsrollupcore.py`

---

### 6. `CorrelationCore`

**Line**: 470  
**Methods**: 1

Pure correlation analysis (Rust-convertible).

[TIP] **Suggested split**: Move to `correlationcore.py`

---

### 7. `ABTestCore`

**Line**: 507  
**Methods**: 2

Pure A/B testing calculations (Rust-convertible).

[TIP] **Suggested split**: Move to `abtestcore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
