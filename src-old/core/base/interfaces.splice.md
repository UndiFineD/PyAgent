# Class Breakdown: interfaces

**File**: `src\core\base\interfaces.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `AgentInterface`

**Line**: 24  
**Inherits**: Protocol  
**Methods**: 6

Core interface for all AI-powered agents. 
Defining this as a Protocol facilitates future Rust implementation (PyO3).

[TIP] **Suggested split**: Move to `agentinterface.py`

---

### 2. `OrchestratorInterface`

**Line**: 49  
**Inherits**: Protocol  
**Methods**: 2

Interface for fleet orchestrators.

[TIP] **Suggested split**: Move to `orchestratorinterface.py`

---

### 3. `CoreInterface`

**Line**: 57  
**Inherits**: Protocol  
**Methods**: 3

Pure logic interface. High-performance, no-IO, candidate for Rust parity.

[TIP] **Suggested split**: Move to `coreinterface.py`

---

### 4. `ContextRecorderInterface`

**Line**: 67  
**Inherits**: Protocol  
**Methods**: 1

Interface for cognitive recording and context harvesting.

[TIP] **Suggested split**: Move to `contextrecorderinterface.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
