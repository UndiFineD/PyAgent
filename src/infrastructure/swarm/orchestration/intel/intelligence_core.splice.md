# Class Breakdown: intelligence_core

**File**: `src\infrastructure\swarm\orchestration\intel\intelligence_core.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `SwarmInsight`

**Line**: 44  
**Methods**: 1

Data class representing a derived insight from the swarm.

[TIP] **Suggested split**: Move to `swarminsight.py`

---

### 2. `IntelligenceCore`

**Line**: 58  
**Methods**: 4

Logic-only core for swarm intelligence synthesis.

[TIP] **Suggested split**: Move to `intelligencecore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
