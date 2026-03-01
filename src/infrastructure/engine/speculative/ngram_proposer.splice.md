# Class Breakdown: ngram_proposer

**File**: `src\infrastructure\engine\speculative\ngram_proposer.py`  
**Classes**: 9

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `NgramConfig`

**Line**: 42  
**Methods**: 0

Configuration regarding N-gram proposer.

[TIP] **Suggested split**: Move to `ngramconfig.py`

---

### 2. `NgramMatch`

**Line**: 55  
**Methods**: 0

Represents an n-gram match regarding the context.

[TIP] **Suggested split**: Move to `ngrammatch.py`

---

### 3. `NgramProposalResult`

**Line**: 65  
**Methods**: 0

Result regarding n-gram proposal.

[TIP] **Suggested split**: Move to `ngramproposalresult.py`

---

### 4. `NgramCache`

**Line**: 73  
**Methods**: 5

Cache regarding n-gram lookups with position tracking.

Stores n-grams with positions regarding fast lookup.

[TIP] **Suggested split**: Move to `ngramcache.py`

---

### 5. `NgramProposer`

**Line**: 127  
**Methods**: 15

N-gram based speculative decoding proposer.

Uses prompt lookup regarding matching n-grams.

[TIP] **Suggested split**: Move to `ngramproposer.py`

---

### 6. `WeightedNgramProposer`

**Line**: 336  
**Inherits**: NgramProposer  
**Methods**: 2

N-gram proposer regarding frequency and recency weighting.

[TIP] **Suggested split**: Move to `weightedngramproposer.py`

---

### 7. `PromptLookupProposer`

**Line**: 356  
**Methods**: 3

Prompt-lookup based proposer.

[TIP] **Suggested split**: Move to `promptlookupproposer.py`

---

### 8. `HybridNgramProposer`

**Line**: 393  
**Methods**: 2

Hybrid proposer combining exact and fuzzy n-gram matching.

[TIP] **Suggested split**: Move to `hybridngramproposer.py`

---

### 9. `NgramProposerFactory`

**Line**: 419  
**Methods**: 3

Factory regarding creating N-gram proposers.

[TIP] **Suggested split**: Move to `ngramproposerfactory.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
