# Class Breakdown: Registry

**File**: `src\infrastructure\decoding\grammar\Registry.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `GrammarCompiler`

**Line**: 33  
**Methods**: 2

Compiles grammar specifications into grammar objects.

Inspired by vLLM's structured output backends.

[TIP] **Suggested split**: Move to `grammarcompiler.py`

---

### 2. `StructuredOutputManager`

**Line**: 105  
**Methods**: 6

Manages grammar compilation and lifecycle.

Inspired by vLLM's StructuredOutputManager.

[TIP] **Suggested split**: Move to `structuredoutputmanager.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
