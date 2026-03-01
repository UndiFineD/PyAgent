# Class Breakdown: testing_utils

**File**: `src\infrastructure\services\dev\agent_tests\testing_utils.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `VisualRegressionTester`

**Line**: 42  
**Methods**: 5

Visual regression testing for UI components.

[TIP] **Suggested split**: Move to `visualregressiontester.py`

---

### 2. `ContractTestRunner`

**Line**: 105  
**Methods**: 6

Contract testing for API boundaries.

[TIP] **Suggested split**: Move to `contracttestrunner.py`

---

### 3. `ResultAggregator`

**Line**: 185  
**Methods**: 8

Aggregate test results from multiple sources.

[TIP] **Suggested split**: Move to `resultaggregator.py`

---

### 4. `TestMetricsCollector`

**Line**: 343  
**Methods**: 5

Collect test execution metrics.

[TIP] **Suggested split**: Move to `testmetricscollector.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
