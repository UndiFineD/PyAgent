# Class Breakdown: NgramProposer

**File**: `src\infrastructure\speculative_v2\NgramProposer.py`  
**Classes**: 9

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `NgramConfig`

**Line**: 34  
**Methods**: 0

Configuration for N-gram proposer.

[TIP] **Suggested split**: Move to `ngramconfig.py`

---

### 2. `NgramMatch`

**Line**: 46  
**Methods**: 0

Represents an n-gram match in the context.

[TIP] **Suggested split**: Move to `ngrammatch.py`

---

### 3. `NgramProposalResult`

**Line**: 55  
**Methods**: 0

Result of n-gram proposal.

[TIP] **Suggested split**: Move to `ngramproposalresult.py`

---

### 4. `NgramCache`

**Line**: 62  
**Methods**: 5

Cache for n-gram lookups with position tracking.

Stores n-grams with their positions for fast lookup.

[TIP] **Suggested split**: Move to `ngramcache.py`

---

### 5. `NgramProposer`

**Line**: 116  
**Methods**: 11

N-gram based speculative decoding proposer.

Uses prompt lookup to find matching n-grams and propose
following tokens as draft candidates.

[TIP] **Suggested split**: Move to `ngramproposer.py`

---

### 6. `WeightedNgramProposer`

**Line**: 396  
**Inherits**: NgramProposer  
**Methods**: 3

N-gram proposer with frequency and recency weighting.

Tracks n-gram occurrences and weights matches by frequency.

[TIP] **Suggested split**: Move to `weightedngramproposer.py`

---

### 7. `PromptLookupProposer`

**Line**: 423  
**Methods**: 2

Prompt-lookup based proposer that searches for repetitions.

Specialized for scenarios where the prompt contains repetitive patterns
that are likely to continue in generation.

[TIP] **Suggested split**: Move to `promptlookupproposer.py`

---

### 8. `HybridNgramProposer`

**Line**: 483  
**Methods**: 2

Hybrid proposer combining exact and fuzzy n-gram matching.

Falls back to fuzzy matching when exact matching fails.

[TIP] **Suggested split**: Move to `hybridngramproposer.py`

---

### 9. `NgramProposerFactory`

**Line**: 534  
**Methods**: 3

Factory for creating N-gram proposers.

[TIP] **Suggested split**: Move to `ngramproposerfactory.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
