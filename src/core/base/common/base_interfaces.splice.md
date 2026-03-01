# Class Breakdown: base_interfaces

**File**: `src\core\base\common\base_interfaces.py`  
**Classes**: 7

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `AgentInterface`

**Line**: 32  
**Inherits**: Protocol  
**Methods**: 6

Core interface for all AI-powered agents.
Defining this as a Protocol facilitates future Rust implementation (PyO3).

[TIP] **Suggested split**: Move to `agentinterface.py`

---

### 2. `OrchestratorInterface`

**Line**: 72  
**Inherits**: Protocol  
**Methods**: 2

Interface for fleet orchestrators.

[TIP] **Suggested split**: Move to `orchestratorinterface.py`

---

### 3. `CoreInterface`

**Line**: 85  
**Inherits**: Protocol  
**Methods**: 3

Pure logic interface. High-performance, no-IO, candidate for Rust parity.

[TIP] **Suggested split**: Move to `coreinterface.py`

---

### 4. `ContextRecorderInterface`

**Line**: 102  
**Inherits**: Protocol  
**Methods**: 1

Interface for cognitive recording and context harvesting.

[TIP] **Suggested split**: Move to `contextrecorderinterface.py`

---

### 5. `Loadable`

**Line**: 118  
**Inherits**: Protocol  
**Methods**: 1

Protocol for objects that can load their state from disk.

[TIP] **Suggested split**: Move to `loadable.py`

---

### 6. `Saveable`

**Line**: 126  
**Inherits**: Protocol  
**Methods**: 1

Protocol for objects that can save their state to disk.

[TIP] **Suggested split**: Move to `saveable.py`

---

### 7. `Component`

**Line**: 134  
**Inherits**: Protocol  
**Methods**: 0

Base interface for all PyAgent components with a name and version.

[TIP] **Suggested split**: Move to `component.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
