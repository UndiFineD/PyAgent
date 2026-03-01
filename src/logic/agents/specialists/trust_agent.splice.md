# Class Breakdown: trust_agent

**File**: `src\logic\agents\specialists\trust_agent.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `Mood`

**Line**: 43  
**Inherits**: Enum  
**Methods**: 0

Possible emotional moods for the interaction.

[TIP] **Suggested split**: Move to `mood.py`

---

### 2. `TrustLevel`

**Line**: 53  
**Inherits**: Enum  
**Methods**: 0

Ordinal levels of trust based on scores.

[TIP] **Suggested split**: Move to `trustlevel.py`

---

### 3. `EmotionalState`

**Line**: 62  
**Methods**: 0

Represents the current emotional state of an interaction.

[TIP] **Suggested split**: Move to `emotionalstate.py`

---

### 4. `TrustMetrics`

**Line**: 72  
**Methods**: 0

Tracks trust-related metrics over time.

[TIP] **Suggested split**: Move to `trustmetrics.py`

---

### 5. `TrustAgent`

**Line**: 83  
**Inherits**: BaseAgent  
**Methods**: 7

Agent specializing in human-agent alignment, mood detection,
emotional intelligence, and maintaining trust scores for interaction safety.

[TIP] **Suggested split**: Move to `trustagent.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
