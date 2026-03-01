# Class Breakdown: test_management

**File**: `src\infrastructure\services\dev\agent_tests\test_management.py`  
**Classes**: 10

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `BaselineComparisonResult`

**Line**: 37  
**Methods**: 1

Result of a baseline comparison.

[TIP] **Suggested split**: Move to `baselinecomparisonresult.py`

---

### 2. `BaselineManager`

**Line**: 45  
**Methods**: 5

Manage test baselines.

[TIP] **Suggested split**: Move to `baselinemanager.py`

---

### 3. `DIContainer`

**Line**: 90  
**Methods**: 5

Dependency injection container.

[TIP] **Suggested split**: Move to `dicontainer.py`

---

### 4. `TestPrioritizer`

**Line**: 135  
**Methods**: 8

Prioritizes tests based on various factors.

[TIP] **Suggested split**: Move to `testprioritizer.py`

---

### 5. `FlakinessDetector`

**Line**: 203  
**Methods**: 4

Detects flaky tests.

[TIP] **Suggested split**: Move to `flakinessdetector.py`

---

### 6. `QuarantineManager`

**Line**: 232  
**Methods**: 4

Manages quarantined flaky tests.

[TIP] **Suggested split**: Move to `quarantinemanager.py`

---

### 7. `ImpactAnalyzer`

**Line**: 257  
**Methods**: 7

Analyzes impact of code changes on tests.

[TIP] **Suggested split**: Move to `impactanalyzer.py`

---

### 8. `ContractValidator`

**Line**: 302  
**Methods**: 1

Validates API contracts.

[TIP] **Suggested split**: Move to `contractvalidator.py`

---

### 9. `TestDocGenerator`

**Line**: 347  
**Methods**: 6

Generates documentation from tests.

[TIP] **Suggested split**: Move to `testdocgenerator.py`

---

### 10. `ValidationResult`

**Line**: 306  
**Methods**: 0

Result of a contract validation.

[TIP] **Suggested split**: Move to `validationresult.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
