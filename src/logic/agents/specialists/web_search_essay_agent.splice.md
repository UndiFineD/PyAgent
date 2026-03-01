# Class Breakdown: web_search_essay_agent

**File**: `src\logic\agents\specialists\web_search_essay_agent.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `EssayStyle`

**Line**: 43  
**Inherits**: Enum  
**Methods**: 0

Essay style options.

[TIP] **Suggested split**: Move to `essaystyle.py`

---

### 2. `EssayLength`

**Line**: 53  
**Inherits**: Enum  
**Methods**: 0

Essay length options.

[TIP] **Suggested split**: Move to `essaylength.py`

---

### 3. `Source`

**Line**: 62  
**Methods**: 0

Represents a research source.

[TIP] **Suggested split**: Move to `source.py`

---

### 4. `EssayOutline`

**Line**: 73  
**Methods**: 0

Represents an essay outline.

[TIP] **Suggested split**: Move to `essayoutline.py`

---

### 5. `WebSearchEssayAgent`

**Line**: 83  
**Inherits**: SearchAgent  
**Methods**: 2

Agent that researches complex subjects via web search and
composes structured essays based on findings.

[TIP] **Suggested split**: Move to `websearchessayagent.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
