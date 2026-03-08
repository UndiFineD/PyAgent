# Class Breakdown: regression_agent

**File**: `src\logic\agents\specialists\regression_agent.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `RegressionType`

**Line**: 39  
**Inherits**: Enum  
**Methods**: 0

Supported regression model types.

[TIP] **Suggested split**: Move to `regressiontype.py`

---

### 2. `RegressionResult`

**Line**: 49  
**Methods**: 0

Stores regression analysis results.

[TIP] **Suggested split**: Move to `regressionresult.py`

---

### 3. `RegressionAgent`

**Line**: 60  
**Inherits**: BaseAgent  
**Methods**: 6

Agent specializing in predicting continuous values and analyzing relationships
between variables (e.g., predicting code complexity growth, performance trends).

[TIP] **Suggested split**: Move to `regressionagent.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
