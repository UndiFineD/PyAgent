# Class Breakdown: OrchestrationManagers

**File**: `src\classes\base_agent\managers\OrchestrationManagers.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `AgentComposer`

**Line**: 30  
**Methods**: 5

Composer for multi-agent workflows.

[TIP] **Suggested split**: Move to `agentcomposer.py`

---

### 2. `ModelSelector`

**Line**: 84  
**Methods**: 3

Selects models for different agent types. Supports GLM-4.7 and DeepSeek V4 (roadmap).

[TIP] **Suggested split**: Move to `modelselector.py`

---

### 3. `QualityScorer`

**Line**: 110  
**Methods**: 2

Scores response quality.

[TIP] **Suggested split**: Move to `qualityscorer.py`

---

### 4. `ABTest`

**Line**: 125  
**Methods**: 2

A/B test for variants.

[TIP] **Suggested split**: Move to `abtest.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
