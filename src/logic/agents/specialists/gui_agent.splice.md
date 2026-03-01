# Class Breakdown: gui_agent

**File**: `src\logic\agents\specialists\gui_agent.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `Framework`

**Line**: 42  
**Inherits**: Enum  
**Methods**: 0

Supported GUI frameworks.

[TIP] **Suggested split**: Move to `framework.py`

---

### 2. `ElementType`

**Line**: 55  
**Inherits**: Enum  
**Methods**: 0

Common UI element types.

[TIP] **Suggested split**: Move to `elementtype.py`

---

### 3. `UIElement`

**Line**: 69  
**Methods**: 0

Represents a UI element with properties.

[TIP] **Suggested split**: Move to `uielement.py`

---

### 4. `UIAction`

**Line**: 82  
**Methods**: 0

Represents an action to perform on a UI.

[TIP] **Suggested split**: Move to `uiaction.py`

---

### 5. `GUIAgent`

**Line**: 91  
**Inherits**: BaseAgent  
**Methods**: 3

Agent specializing in interacting with and designing GUIs.
Can generate layout code (Qt, React, Tkinter) and interpret UI snapshots.

[TIP] **Suggested split**: Move to `guiagent.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
