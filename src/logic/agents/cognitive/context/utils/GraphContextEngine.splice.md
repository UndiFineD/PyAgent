# Class Breakdown: GraphContextEngine

**File**: `src\logic\agents\cognitive\context\utils\GraphContextEngine.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `CodeGraphVisitor`

**Line**: 13  
**Inherits**: NodeVisitor  
**Methods**: 5

AST visitor to extract imports, classes, and function calls.

[TIP] **Suggested split**: Move to `codegraphvisitor.py`

---

### 2. `GraphContextEngine`

**Line**: 50  
**Methods**: 6

Manages an adjacency list of file and class dependencies.

[TIP] **Suggested split**: Move to `graphcontextengine.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
