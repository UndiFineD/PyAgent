# Class Breakdown: types

**File**: `src\infrastructure\engine\tokenization\detokenizer\types.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `TokenizerLike`

**Line**: 24  
**Inherits**: Protocol  
**Methods**: 6

Protocol for tokenizer abstraction.

[TIP] **Suggested split**: Move to `tokenizerlike.py`

---

### 2. `DetokenizeResult`

**Line**: 83  
**Methods**: 1

Result of incremental detokenization.

[TIP] **Suggested split**: Move to `detokenizeresult.py`

---

### 3. `Modality`

**Line**: 101  
**Inherits**: Enum  
**Methods**: 0

Enum for different data modalities supported by multimodal tokenizers.

[TIP] **Suggested split**: Move to `modality.py`

---

### 4. `MultimodalToken`

**Line**: 110  
**Methods**: 4

Representation of a token from any modality in a unified token space.

[TIP] **Suggested split**: Move to `multimodaltoken.py`

---

### 5. `MultimodalTokenizedData`

**Line**: 139  
**Methods**: 4

Result of multimodal tokenization with unified token IDs and metadata.

[TIP] **Suggested split**: Move to `multimodaltokenizeddata.py`

---

### 6. `MultimodalTokenizer`

**Line**: 168  
**Methods**: 5

Unified tokenizer for multimodal data (text, images, audio, video).

Uses a unified token vocabulary across all modalities:
- Text tokens: 0-30000 (using SentencePiece/BPE)
- Image tokens: 30001-60000...

[TIP] **Suggested split**: Move to `multimodaltokenizer.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
