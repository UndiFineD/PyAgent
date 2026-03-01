# Class Breakdown: StructuredOutputOrchestrator

**File**: `src\infrastructure\structured_output\StructuredOutputOrchestrator.py`  
**Classes**: 11

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `StructuredOutputBackendType`

**Line**: 59  
**Inherits**: Enum  
**Methods**: 0

Types of structured output backends.

[TIP] **Suggested split**: Move to `structuredoutputbackendtype.py`

---

### 2. `ConstraintType`

**Line**: 68  
**Inherits**: Enum  
**Methods**: 0

Types of output constraints.

[TIP] **Suggested split**: Move to `constrainttype.py`

---

### 3. `GrammarProtocol`

**Line**: 79  
**Inherits**: Protocol  
**Methods**: 4

Protocol for grammar implementations.

[TIP] **Suggested split**: Move to `grammarprotocol.py`

---

### 4. `BackendProtocol`

**Line**: 100  
**Inherits**: Protocol  
**Methods**: 3

Protocol for backend implementations.

[TIP] **Suggested split**: Move to `backendprotocol.py`

---

### 5. `ConstraintSpec`

**Line**: 117  
**Methods**: 1

Specification for output constraint.

Describes the constraint to apply to generation.

[TIP] **Suggested split**: Move to `constraintspec.py`

---

### 6. `OrchestratorConfig`

**Line**: 139  
**Methods**: 0

Configuration for orchestrator.

[TIP] **Suggested split**: Move to `orchestratorconfig.py`

---

### 7. `BackendWrapper`

**Line**: 150  
**Methods**: 3

Wrapper for structured output backend.

Provides unified interface and statistics tracking.

[TIP] **Suggested split**: Move to `backendwrapper.py`

---

### 8. `CompiledGrammarHandle`

**Line**: 226  
**Methods**: 6

Handle to compiled grammar.

Provides state management and bitmask operations.

[TIP] **Suggested split**: Move to `compiledgrammarhandle.py`

---

### 9. `StructuredOutputOrchestrator`

**Line**: 281  
**Methods**: 9

Orchestrator for structured output backends.

Provides unified interface for:
- Backend registration and selection
- Constraint compilation with caching
- Fallback handling
- Performance monitoring

[TIP] **Suggested split**: Move to `structuredoutputorchestrator.py`

---

### 10. `AsyncStructuredOutputOrchestrator`

**Line**: 465  
**Inherits**: StructuredOutputOrchestrator  
**Methods**: 0

Async-enabled orchestrator.

Provides async compilation for non-blocking operation.

[TIP] **Suggested split**: Move to `asyncstructuredoutputorchestrator.py`

---

### 11. `BatchProcessor`

**Line**: 497  
**Methods**: 6

Batch processor for structured output.

Handles batch-level bitmask operations efficiently.

[TIP] **Suggested split**: Move to `batchprocessor.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
