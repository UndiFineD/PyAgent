# Class Breakdown: Parsers

**File**: `src\infrastructure\reasoning\Parsers.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ReasoningParser`

**Line**: 6  
**Inherits**: ABC  
**Methods**: 4

Abstract base for reasoning token extraction.

[TIP] **Suggested split**: Move to `reasoningparser.py`

---

### 2. `ToolParser`

**Line**: 43  
**Inherits**: ABC  
**Methods**: 5

Abstract base for tool/function call parsing.

[TIP] **Suggested split**: Move to `toolparser.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
