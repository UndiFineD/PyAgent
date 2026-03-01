# Class Breakdown: graph_core

**File**: `src\logic\agents\cognitive\context\engines\graph_core.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `CodeGraphVisitor`

**Line**: 37  
**Inherits**: NodeVisitor  
**Methods**: 5

AST visitor to extract imports, classes, and function calls.

[TIP] **Suggested split**: Move to `codegraphvisitor.py`

---

### 2. `GraphCore`

**Line**: 82  
**Methods**: 2

Pure logic for managing code relationship graphs.

[TIP] **Suggested split**: Move to `graphcore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
