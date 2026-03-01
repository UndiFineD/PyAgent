# Class Breakdown: GuidanceBackend

**File**: `src\infrastructure\structured_output\GuidanceBackend.py`  
**Classes**: 8

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `GuidanceTemplateType`

**Line**: 54  
**Inherits**: Enum  
**Methods**: 0

Types of Guidance templates.

[TIP] **Suggested split**: Move to `guidancetemplatetype.py`

---

### 2. `GuidanceVariable`

**Line**: 64  
**Methods**: 1

Variable in a Guidance template.

[TIP] **Suggested split**: Move to `guidancevariable.py`

---

### 3. `GuidanceTemplate`

**Line**: 83  
**Methods**: 5

Guidance template specification.

Represents a template with embedded generation instructions.

[TIP] **Suggested split**: Move to `guidancetemplate.py`

---

### 4. `GuidanceState`

**Line**: 157  
**Methods**: 4

State for Guidance template execution.

Tracks current position in template and variable values.

[TIP] **Suggested split**: Move to `guidancestate.py`

---

### 5. `CompiledGuidanceProgram`

**Line**: 223  
**Methods**: 4

Compiled Guidance program.

Represents a compiled and ready-to-execute Guidance template.

[TIP] **Suggested split**: Move to `compiledguidanceprogram.py`

---

### 6. `GuidanceGrammar`

**Line**: 257  
**Methods**: 8

Grammar wrapper for Guidance programs.

Provides the standard grammar interface while wrapping
a Guidance program and state.

[TIP] **Suggested split**: Move to `guidancegrammar.py`

---

### 7. `GuidanceBackend`

**Line**: 312  
**Methods**: 8

Guidance library backend for structured output.

Provides template-based constrained generation using the
Guidance library's approach to structured output.

[TIP] **Suggested split**: Move to `guidancebackend.py`

---

### 8. `AsyncGuidanceBackend`

**Line**: 452  
**Inherits**: GuidanceBackend  
**Methods**: 0

Async-enabled Guidance backend.

Provides async template compilation for non-blocking operation.

[TIP] **Suggested split**: Move to `asyncguidancebackend.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
