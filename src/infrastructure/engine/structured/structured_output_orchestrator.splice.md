# Class Breakdown: structured_output_orchestrator

**File**: `src\infrastructure\engine\structured\structured_output_orchestrator.py`  
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

**Line**: 69  
**Inherits**: Enum  
**Methods**: 0

Types of output constraints.

[TIP] **Suggested split**: Move to `constrainttype.py`

---

### 3. `GrammarProtocol`

**Line**: 81  
**Inherits**: Protocol  
**Methods**: 4

Protocol regarding grammar implementations.

[TIP] **Suggested split**: Move to `grammarprotocol.py`

---

### 4. `BackendProtocol`

**Line**: 98  
**Inherits**: Protocol  
**Methods**: 3

Protocol regarding backend implementations.

[TIP] **Suggested split**: Move to `backendprotocol.py`

---

### 5. `ConstraintSpec`

**Line**: 112  
**Methods**: 1

Specification regarding output constraint.

Describes the constraint to apply to generation.

[TIP] **Suggested split**: Move to `constraintspec.py`

---

### 6. `OrchestratorConfig`

**Line**: 135  
**Methods**: 0

Configuration regarding orchestrator.

[TIP] **Suggested split**: Move to `orchestratorconfig.py`

---

### 7. `BackendWrapper`

**Line**: 147  
**Methods**: 5

Wrapper regarding structured output backend.

Provides unified interface and statistics tracking.

[TIP] **Suggested split**: Move to `backendwrapper.py`

---

### 8. `CompiledGrammarHandle`

**Line**: 230  
**Methods**: 6

Handle to compiled grammar.

Provides state management and bitmask operations.

[TIP] **Suggested split**: Move to `compiledgrammarhandle.py`

---

### 9. `StructuredOutputOrchestrator`

**Line**: 285  
**Methods**: 12

Orchestrator regarding structured output backends.

Provides unified interface regarding:
- Backend registration and selection
- Constraint compilation with caching
- Fallback handling
- Performance m...

[TIP] **Suggested split**: Move to `structuredoutputorchestrator.py`

---

### 10. `AsyncStructuredOutputOrchestrator`

**Line**: 488  
**Inherits**: StructuredOutputOrchestrator  
**Methods**: 0

Async-enabled orchestrator.

Provides async compilation regarding non-blocking operation.

[TIP] **Suggested split**: Move to `asyncstructuredoutputorchestrator.py`

---

### 11. `BatchProcessor`

**Line**: 520  
**Methods**: 6

Batch processor regarding structured output.

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
