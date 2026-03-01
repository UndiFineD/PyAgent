# Class Breakdown: BadWordsProcessorV2

**File**: `src\infrastructure\structured_output\BadWordsProcessorV2.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `BadWordsPenaltyMode`

**Line**: 53  
**Inherits**: Enum  
**Methods**: 0

Penalty mode for bad words.

[TIP] **Suggested split**: Move to `badwordspenaltymode.py`

---

### 2. `TrieNode`

**Line**: 61  
**Methods**: 2

Trie node for efficient prefix matching.

[TIP] **Suggested split**: Move to `trienode.py`

---

### 3. `BadWordsProcessorV2`

**Line**: 110  
**Inherits**: LogitsProcessor  
**Methods**: 12

Enhanced bad words filtering processor.

Filters out tokens that would complete a "bad word" sequence.
Supports n-gram matching and speculative decoding.

[TIP] **Suggested split**: Move to `badwordsprocessorv2.py`

---

### 4. `BadPhrasesProcessor`

**Line**: 338  
**Inherits**: BadWordsProcessorV2  
**Methods**: 3

Extended processor for bad phrases with wildcards.

Beyond vLLM: Supports wildcard patterns and phrase variations.

[TIP] **Suggested split**: Move to `badphrasesprocessor.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
