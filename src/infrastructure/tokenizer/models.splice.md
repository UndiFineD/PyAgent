# Class Breakdown: models

**File**: `src\infrastructure\tokenizer\models.py`  
**Classes**: 8

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `TokenizerBackend`

**Line**: 15  
**Inherits**: Enum  
**Methods**: 0

Supported tokenizer backends.

[TIP] **Suggested split**: Move to `tokenizerbackend.py`

---

### 2. `SpecialTokenHandling`

**Line**: 24  
**Inherits**: Enum  
**Methods**: 0

How to handle special tokens.

[TIP] **Suggested split**: Move to `specialtokenhandling.py`

---

### 3. `TruncationStrategy`

**Line**: 33  
**Inherits**: Enum  
**Methods**: 0

Truncation strategies for long sequences.

[TIP] **Suggested split**: Move to `truncationstrategy.py`

---

### 4. `PaddingStrategy`

**Line**: 41  
**Inherits**: Enum  
**Methods**: 0

Padding strategies for batched inputs.

[TIP] **Suggested split**: Move to `paddingstrategy.py`

---

### 5. `TokenizerConfig`

**Line**: 49  
**Methods**: 1

Configuration for tokenizer initialization.

[TIP] **Suggested split**: Move to `tokenizerconfig.py`

---

### 6. `TokenizerInfo`

**Line**: 76  
**Methods**: 1

Information about a loaded tokenizer.

[TIP] **Suggested split**: Move to `tokenizerinfo.py`

---

### 7. `TokenizeResult`

**Line**: 105  
**Methods**: 2

Result of tokenization.

[TIP] **Suggested split**: Move to `tokenizeresult.py`

---

### 8. `BatchTokenizeResult`

**Line**: 128  
**Methods**: 2

Result of batch tokenization.

[TIP] **Suggested split**: Move to `batchtokenizeresult.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
