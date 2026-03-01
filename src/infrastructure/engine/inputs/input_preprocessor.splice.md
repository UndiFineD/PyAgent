# Class Breakdown: input_preprocessor

**File**: `src\infrastructure\engine\inputs\input_preprocessor.py`  
**Classes**: 14

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `PromptType`

**Line**: 45  
**Inherits**: Enum  
**Methods**: 0

Types of prompt input.

[TIP] **Suggested split**: Move to `prompttype.py`

---

### 2. `InputFormat`

**Line**: 56  
**Inherits**: Enum  
**Methods**: 0

Input format specifications.

[TIP] **Suggested split**: Move to `inputformat.py`

---

### 3. `TextPrompt`

**Line**: 73  
**Methods**: 2

Text-based prompt.

[TIP] **Suggested split**: Move to `textprompt.py`

---

### 4. `TokensPrompt`

**Line**: 91  
**Methods**: 2

Pre-tokenized prompt.

[TIP] **Suggested split**: Move to `tokensprompt.py`

---

### 5. `EmbedsPrompt`

**Line**: 110  
**Methods**: 2

Pre-computed embeddings prompt.

[TIP] **Suggested split**: Move to `embedsprompt.py`

---

### 6. `EncoderDecoderPrompt`

**Line**: 127  
**Methods**: 1

Prompt for encoder-decoder models (T5, BART, etc.).

[TIP] **Suggested split**: Move to `encoderdecoderprompt.py`

---

### 7. `ChatMessage`

**Line**: 140  
**Methods**: 1

Single message in a conversation.

[TIP] **Suggested split**: Move to `chatmessage.py`

---

### 8. `ChatPrompt`

**Line**: 162  
**Methods**: 2

Multi-turn conversation prompt.

[TIP] **Suggested split**: Move to `chatprompt.py`

---

### 9. `InputMetadata`

**Line**: 188  
**Methods**: 0

Metadata about processed input.

[TIP] **Suggested split**: Move to `inputmetadata.py`

---

### 10. `ProcessedInput`

**Line**: 202  
**Methods**: 1

Fully processed input ready for model.

[TIP] **Suggested split**: Move to `processedinput.py`

---

### 11. `PromptTemplate`

**Line**: 227  
**Methods**: 1

Template for formatting prompts.

[TIP] **Suggested split**: Move to `prompttemplate.py`

---

### 12. `PromptValidator`

**Line**: 275  
**Methods**: 7

Validates prompt inputs.

[TIP] **Suggested split**: Move to `promptvalidator.py`

---

### 13. `ConversationLinearizer`

**Line**: 358  
**Methods**: 3

Linearizes multi-turn conversations to single prompt.

Supports multiple chat formats (ChatML, Llama, Anthropic, etc.)

[TIP] **Suggested split**: Move to `conversationlinearizer.py`

---

### 14. `InputPreprocessor`

**Line**: 415  
**Methods**: 11

Unified input preprocessing for LLM inference.

Features beyond vLLM:
- JSON Schema validation for structured inputs
- Automatic prompt template detection
- Multi-turn conversation linearization
- Emb...

[TIP] **Suggested split**: Move to `inputpreprocessor.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
