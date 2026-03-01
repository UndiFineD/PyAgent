# Class Breakdown: PenaltyEngine

**File**: `src\infrastructure\sampling\PenaltyEngine.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `PenaltyType`

**Line**: 43  
**Inherits**: Enum  
**Methods**: 0

Types of penalties.

[TIP] **Suggested split**: Move to `penaltytype.py`

---

### 2. `PenaltySchedule`

**Line**: 53  
**Inherits**: Enum  
**Methods**: 0

Penalty scheduling strategies.

[TIP] **Suggested split**: Move to `penaltyschedule.py`

---

### 3. `PenaltyConfig`

**Line**: 62  
**Methods**: 1

Configuration for penalty engine.

[TIP] **Suggested split**: Move to `penaltyconfig.py`

---

### 4. `PenaltyState`

**Line**: 84  
**Methods**: 5

Mutable state for penalty tracking.

[TIP] **Suggested split**: Move to `penaltystate.py`

---

### 5. `PenaltyEngine`

**Line**: 118  
**Methods**: 13

Comprehensive penalty engine for token penalization.

Implements vLLM's penalty application with extensions for:
- Penalty scheduling
- Positional decay
- N-gram penalties
- Context-aware strength

[TIP] **Suggested split**: Move to `penaltyengine.py`

---

### 6. `BatchPenaltyEngine`

**Line**: 428  
**Methods**: 1

Batch-optimized penalty engine.

Efficiently applies penalties to multiple sequences
with different configurations.

[TIP] **Suggested split**: Move to `batchpenaltyengine.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
