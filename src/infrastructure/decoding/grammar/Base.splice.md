# Class Breakdown: Base

**File**: `src\infrastructure\decoding\grammar\Base.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `StructuredOutputOptions`

**Line**: 25  
**Inherits**: Enum  
**Methods**: 0

Types of structured output constraints.

Inspired by vLLM's StructuredOutputOptions.

[TIP] **Suggested split**: Move to `structuredoutputoptions.py`

---

### 2. `StructuredOutputsParams`

**Line**: 40  
**Methods**: 4

Parameters for structured output generation.

Inspired by vLLM's StructuredOutputsParams.
Only one constraint type should be set at a time.

Attributes:
    json: JSON schema (dict or string).
    reg...

[TIP] **Suggested split**: Move to `structuredoutputsparams.py`

---

### 3. `StructuredOutputGrammar`

**Line**: 128  
**Inherits**: ABC  
**Methods**: 8

Abstract base class for grammar-constrained decoding.

Inspired by vLLM's StructuredOutputGrammar interface.
Implementations track state and validate tokens against the grammar.

[TIP] **Suggested split**: Move to `structuredoutputgrammar.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
