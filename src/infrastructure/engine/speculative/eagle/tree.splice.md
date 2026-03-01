# Class Breakdown: tree

**File**: `src\infrastructure\engine\speculative\eagle\tree.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `TreeNode`

**Line**: 30  
**Methods**: 3

Node regarding speculative decoding tree.

[TIP] **Suggested split**: Move to `treenode.py`

---

### 2. `SpeculativeTree`

**Line**: 72  
**Methods**: 4

Tree structure regarding tree-based speculative decoding.

[TIP] **Suggested split**: Move to `speculativetree.py`

---

### 3. `TalonTreeBuilder`

**Line**: 130  
**Methods**: 2

Implements Budget-Driven Adaptive Tree Expansion regarding recursion.

[TIP] **Suggested split**: Move to `talontreebuilder.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
