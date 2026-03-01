# Class Breakdown: models

**File**: `src\infrastructure\services\dev\agent_tests\models.py`  
**Classes**: 19

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `TestCase`

**Line**: 48  
**Methods**: 0

Represents a single test case.

[TIP] **Suggested split**: Move to `testcase.py`

---

### 2. `TestRun`

**Line**: 74  
**Methods**: 0

A test execution run.

[TIP] **Suggested split**: Move to `testrun.py`

---

### 3. `CoverageGap`

**Line**: 95  
**Methods**: 0

Represents a gap in test coverage.

[TIP] **Suggested split**: Move to `coveragegap.py`

---

### 4. `TestFactory`

**Line**: 107  
**Methods**: 0

A test data factory for generating test data.

[TIP] **Suggested split**: Move to `testfactory.py`

---

### 5. `VisualRegressionConfig`

**Line**: 119  
**Methods**: 0

Configuration for visual regression testing.

[TIP] **Suggested split**: Move to `visualregressionconfig.py`

---

### 6. `ContractTest`

**Line**: 132  
**Methods**: 0

A contract test for API boundaries.

[TIP] **Suggested split**: Move to `contracttest.py`

---

### 7. `TestEnvironment`

**Line**: 144  
**Methods**: 0

Test environment configuration.

[TIP] **Suggested split**: Move to `testenvironment.py`

---

### 8. `ExecutionTrace`

**Line**: 158  
**Methods**: 0

Test execution trace for replay.

[TIP] **Suggested split**: Move to `executiontrace.py`

---

### 9. `TestDependency`

**Line**: 170  
**Methods**: 0

A dependency for test injection.

[TIP] **Suggested split**: Move to `testdependency.py`

---

### 10. `CrossBrowserConfig`

**Line**: 181  
**Methods**: 0

Cross-browser testing configuration.

[TIP] **Suggested split**: Move to `crossbrowserconfig.py`

---

### 11. `AggregatedResult`

**Line**: 192  
**Methods**: 0

Aggregated test result from multiple sources.

[TIP] **Suggested split**: Move to `aggregatedresult.py`

---

### 12. `Mutation`

**Line**: 204  
**Methods**: 0

A code mutation for mutation testing.

[TIP] **Suggested split**: Move to `mutation.py`

---

### 13. `GeneratedTest`

**Line**: 217  
**Methods**: 0

A test generated from specification.

[TIP] **Suggested split**: Move to `generatedtest.py`

---

### 14. `TestProfile`

**Line**: 228  
**Methods**: 0

Runtime profiling data for a test.

[TIP] **Suggested split**: Move to `testprofile.py`

---

### 15. `ScheduleSlot`

**Line**: 241  
**Methods**: 0

A scheduled time slot for test execution.

[TIP] **Suggested split**: Move to `scheduleslot.py`

---

### 16. `ProvisionedEnvironment`

**Line**: 252  
**Methods**: 0

A provisioned test environment.

[TIP] **Suggested split**: Move to `provisionedenvironment.py`

---

### 17. `ValidationResult`

**Line**: 262  
**Methods**: 0

Result of a validation operation.

[TIP] **Suggested split**: Move to `validationresult.py`

---

### 18. `Recording`

**Line**: 270  
**Methods**: 0

A recording of test execution.

[TIP] **Suggested split**: Move to `recording.py`

---

### 19. `ReplayResult`

**Line**: 278  
**Methods**: 0

Result of replaying a recorded test.

[TIP] **Suggested split**: Move to `replayresult.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
