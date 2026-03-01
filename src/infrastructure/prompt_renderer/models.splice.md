# Class Breakdown: models

**File**: `src\infrastructure\prompt_renderer\models.py`  
**Classes**: 8

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `TruncationStrategy`

**Line**: 15  
**Inherits**: Enum  
**Methods**: 0

Prompt truncation strategies.

[TIP] **Suggested split**: Move to `truncationstrategy.py`

---

### 2. `InputType`

**Line**: 25  
**Inherits**: Enum  
**Methods**: 0

Input types for prompt rendering.

[TIP] **Suggested split**: Move to `inputtype.py`

---

### 3. `RenderMode`

**Line**: 33  
**Inherits**: Enum  
**Methods**: 0

Rendering modes.

[TIP] **Suggested split**: Move to `rendermode.py`

---

### 4. `PromptConfig`

**Line**: 42  
**Methods**: 1

Configuration for prompt rendering.

[TIP] **Suggested split**: Move to `promptconfig.py`

---

### 5. `TruncationResult`

**Line**: 72  
**Methods**: 1

Result of prompt truncation.

[TIP] **Suggested split**: Move to `truncationresult.py`

---

### 6. `RenderResult`

**Line**: 89  
**Methods**: 1

Result of prompt rendering.

[TIP] **Suggested split**: Move to `renderresult.py`

---

### 7. `EmbeddingInput`

**Line**: 109  
**Methods**: 0

Embedding input for direct embedding injection.

[TIP] **Suggested split**: Move to `embeddinginput.py`

---

### 8. `MultimodalInput`

**Line**: 117  
**Methods**: 1

Multimodal input container.

[TIP] **Suggested split**: Move to `multimodalinput.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
