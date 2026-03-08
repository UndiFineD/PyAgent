# Class Breakdown: TypedPrompts

**File**: `src\core\base\types\TypedPrompts.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `TextPrompt`

**Line**: 21  
**Inherits**: TypedDict  
**Methods**: 0

Schema for a text prompt.

The text will be tokenized before passing to the model.

[TIP] **Suggested split**: Move to `textprompt.py`

---

### 2. `TokensPrompt`

**Line**: 40  
**Inherits**: TypedDict  
**Methods**: 0

Schema for a pre-tokenized prompt.

Token IDs are passed directly to the model.

[TIP] **Suggested split**: Move to `tokensprompt.py`

---

### 3. `EmbedsPrompt`

**Line**: 65  
**Inherits**: TypedDict  
**Methods**: 0

Schema for a prompt provided via embeddings.

Pre-computed embeddings are passed directly to the model.

[TIP] **Suggested split**: Move to `embedsprompt.py`

---

### 4. `DataPrompt`

**Line**: 78  
**Inherits**: TypedDict  
**Methods**: 0

Schema for generic data prompts.

Used for custom IO processor plugins.

[TIP] **Suggested split**: Move to `dataprompt.py`

---

### 5. `ExplicitEncoderDecoderPrompt`

**Line**: 109  
**Inherits**: TypedDict, Unknown  
**Methods**: 0

Schema for encoder/decoder model prompts.

Allows specifying separate encoder and decoder prompts.

[TIP] **Suggested split**: Move to `explicitencoderdecoderprompt.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
