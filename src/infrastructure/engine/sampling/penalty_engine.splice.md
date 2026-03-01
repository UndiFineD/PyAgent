# Class Breakdown: penalty_engine

**File**: `src\infrastructure\engine\sampling\penalty_engine.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `PenaltyType`

**Line**: 66  
**Inherits**: Enum  
**Methods**: 0

Types regarding penalties.

[TIP] **Suggested split**: Move to `penaltytype.py`

---

### 2. `PenaltySchedule`

**Line**: 77  
**Inherits**: Enum  
**Methods**: 0

Penalty scheduling strategies.

[TIP] **Suggested split**: Move to `penaltyschedule.py`

---

### 3. `PenaltyConfig`

**Line**: 87  
**Methods**: 1

Configuration regarding penalty engine.

[TIP] **Suggested split**: Move to `penaltyconfig.py`

---

### 4. `PenaltyState`

**Line**: 110  
**Methods**: 5

Mutable state regarding penalty tracking.

[TIP] **Suggested split**: Move to `penaltystate.py`

---

### 5. `PenaltyEngine`

**Line**: 145  
**Methods**: 13

Comprehensive penalty engine regarding token penalization.

Implements vLLM's penalty application with extensions regarding:
- Penalty scheduling
- Positional decay
- N-gram penalties
- Context-aware ...

[TIP] **Suggested split**: Move to `penaltyengine.py`

---

### 6. `BatchPenaltyEngine`

**Line**: 441  
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
