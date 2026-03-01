# Class Breakdown: tree

**File**: `src\infrastructure\engine\speculative\decoder\tree.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `SpeculativeToken`

**Line**: 26  
**Methods**: 0

A single speculative token with metadata.

[TIP] **Suggested split**: Move to `speculativetoken.py`

---

### 2. `SpeculativeTree`

**Line**: 37  
**Methods**: 6

Tree structure regarding speculative tokens.

Represents a tree regarding candidate tokens where each node
can have multiple children (branching speculation).

[TIP] **Suggested split**: Move to `speculativetree.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
