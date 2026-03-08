# Class Breakdown: browser_outline_core

**File**: `src\core\base\logic\core\browser_outline_core.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `BrowserElement`

**Line**: 20  
**Methods**: 0

[TIP] **Suggested split**: Move to `browserelement.py`

---

### 2. `BrowserOutlineCore`

**Line**: 26  
**Methods**: 3

Transforms raw DOM/CDP data into a high-density 'Outline' for efficient LLM navigation.
Reduces token usage by replacing complex selectors with simple labels (e.g., [l1]).
Harvested from .external/AI-...

[TIP] **Suggested split**: Move to `browseroutlinecore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
