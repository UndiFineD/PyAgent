# Class Breakdown: bad_words_processor_v2

**File**: `src\infrastructure\engine\structured\bad_words_processor_v2.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `BadWordsPenaltyMode`

**Line**: 54  
**Inherits**: Enum  
**Methods**: 0

Penalty mode regarding bad words.

[TIP] **Suggested split**: Move to `badwordspenaltymode.py`

---

### 2. `TrieNode`

**Line**: 63  
**Methods**: 2

Trie node regarding efficient prefix matching.

[TIP] **Suggested split**: Move to `trienode.py`

---

### 3. `BadWordsProcessorV2`

**Line**: 123  
**Inherits**: LogitsProcessor  
**Methods**: 18

Enhanced bad words filtering processor.

Filters out tokens that would complete a "bad word" sequence.
Supports n-gram matching and speculative decoding.

[TIP] **Suggested split**: Move to `badwordsprocessorv2.py`

---

### 4. `BadPhrasesProcessor`

**Line**: 433  
**Inherits**: BadWordsProcessorV2  
**Methods**: 3

Extended processor regarding bad phrases with wildcards.

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
