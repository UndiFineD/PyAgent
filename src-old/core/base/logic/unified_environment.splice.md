# Class Breakdown: unified_environment

**File**: `src\core\base\logic\unified_environment.py`  
**Classes**: 9

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `EnvironmentStatus`

**Line**: 32  
**Inherits**: Enum  
**Methods**: 0

Environment lifecycle status

[TIP] **Suggested split**: Move to `environmentstatus.py`

---

### 2. `EnvironmentResult`

**Line**: 43  
**Methods**: 0

Result from environment execution

[TIP] **Suggested split**: Move to `environmentresult.py`

---

### 3. `EnvironmentCapabilities`

**Line**: 52  
**Methods**: 0

Capabilities exposed by an environment

[TIP] **Suggested split**: Move to `environmentcapabilities.py`

---

### 4. `EnvironmentProtocol`

**Line**: 60  
**Inherits**: Protocol  
**Methods**: 3

Protocol for environment-like objects

[TIP] **Suggested split**: Move to `environmentprotocol.py`

---

### 5. `BaseEnvironment`

**Line**: 84  
**Inherits**: ABC  
**Methods**: 7

Abstract base class for all environments
Everything can be treated as an environment: tools, agents, benchmarks, etc.

[TIP] **Suggested split**: Move to `baseenvironment.py`

---

### 6. `ToolEnvironment`

**Line**: 147  
**Inherits**: BaseEnvironment  
**Methods**: 2

Environment that wraps a tool/function
Treats individual tools as environments

[TIP] **Suggested split**: Move to `toolenvironment.py`

---

### 7. `AgentEnvironment`

**Line**: 204  
**Inherits**: BaseEnvironment  
**Methods**: 2

Environment that wraps an agent
Treats agents as environments that can be called like tools

[TIP] **Suggested split**: Move to `agentenvironment.py`

---

### 8. `CompositeEnvironment`

**Line**: 268  
**Inherits**: BaseEnvironment  
**Methods**: 4

Environment that composes multiple sub-environments
Enables complex multi-environment orchestration

[TIP] **Suggested split**: Move to `compositeenvironment.py`

---

### 9. `EnvironmentRegistry`

**Line**: 365  
**Methods**: 6

Registry for managing environments
Provides unified access to all environment types

[TIP] **Suggested split**: Move to `environmentregistry.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
