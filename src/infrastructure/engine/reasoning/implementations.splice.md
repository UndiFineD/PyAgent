# Class Breakdown: implementations

**File**: `src\infrastructure\engine\reasoning\implementations.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `DeepSeekReasoningParser`

**Line**: 28  
**Inherits**: ReasoningParser  
**Methods**: 3

Parser for DeepSeek R1-style <think>...</think> blocks.

[TIP] **Suggested split**: Move to `deepseekreasoningparser.py`

---

### 2. `QwenReasoningParser`

**Line**: 125  
**Inherits**: ReasoningParser  
**Methods**: 3

Parser for Qwen3-style reasoning with enable_thinking flag.

[TIP] **Suggested split**: Move to `qwenreasoningparser.py`

---

### 3. `GenericReasoningParser`

**Line**: 169  
**Inherits**: ReasoningParser  
**Methods**: 3

Configurable parser for any reasoning format.

[TIP] **Suggested split**: Move to `genericreasoningparser.py`

---

### 4. `OpenAIToolParser`

**Line**: 251  
**Inherits**: ToolParser  
**Methods**: 3

Parser for OpenAI-style tool calls.

[TIP] **Suggested split**: Move to `openaitoolparser.py`

---

### 5. `HermesToolParser`

**Line**: 297  
**Inherits**: ToolParser  
**Methods**: 3

Parser for Hermes-style tool calls.

[TIP] **Suggested split**: Move to `hermestoolparser.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
