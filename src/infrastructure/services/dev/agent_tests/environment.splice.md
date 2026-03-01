# Class Breakdown: environment

**File**: `src\infrastructure\services\dev\agent_tests\environment.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `EnvironmentProvisioner`

**Line**: 39  
**Methods**: 7

Provision test environments.

[TIP] **Suggested split**: Move to `environmentprovisioner.py`

---

### 2. `DataFactory`

**Line**: 134  
**Methods**: 6

Factory for creating test data.

[TIP] **Suggested split**: Move to `datafactory.py`

---

### 3. `ProvisionedEnvironment`

**Line**: 43  
**Methods**: 0

Represents a provisioned development or testing environment.

[TIP] **Suggested split**: Move to `provisionedenvironment.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
