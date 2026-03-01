# Class Breakdown: Tree

**File**: `src\infrastructure\speculative_v2\eagle\Tree.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `TreeNode`

**Line**: 14  
**Methods**: 3

Node in speculative decoding tree.

[TIP] **Suggested split**: Move to `treenode.py`

---

### 2. `SpeculativeTree`

**Line**: 59  
**Methods**: 4

Tree structure for tree-based speculative decoding.

[TIP] **Suggested split**: Move to `speculativetree.py`

---

### 3. `TalonTreeBuilder`

**Line**: 124  
**Methods**: 2

Implements Budget-Driven Adaptive Tree Expansion (arXiv:2601.07353).

[TIP] **Suggested split**: Move to `talontreebuilder.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
