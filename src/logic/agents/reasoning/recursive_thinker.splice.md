# Class Breakdown: recursive_thinker

**File**: `src\logic\agents\reasoning\recursive_thinker.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `LLMInterface`

**Line**: 18  
**Inherits**: Protocol  
**Methods**: 0

[TIP] **Suggested split**: Move to `llminterface.py`

---

### 2. `RoundResult`

**Line**: 22  
**Methods**: 0

[TIP] **Suggested split**: Move to `roundresult.py`

---

### 3. `RecursiveThinker`

**Line**: 28  
**Methods**: 1

Implements a recursive thinking pattern (CoRT) to improve agent responses by 
generating alternatives and self-evaluating.
Ported logic from 0xSojalSec-Chain-of-Recursive-Thoughts.

[TIP] **Suggested split**: Move to `recursivethinker.py`

---

### 4. `MockThinkerLLM`

**Line**: 98  
**Methods**: 0

[TIP] **Suggested split**: Move to `mockthinkerllm.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
