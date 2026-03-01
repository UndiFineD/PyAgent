# Class Breakdown: agent_models

**File**: `src\core\base\models\agent_models.py`  
**Classes**: 8

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `AgentConfig`

**Line**: 33  
**Methods**: 0

Agent configuration from environment or file.

[TIP] **Suggested split**: Move to `agentconfig.py`

---

### 2. `ComposedAgent`

**Line**: 46  
**Methods**: 0

Configuration for agent composition.

[TIP] **Suggested split**: Move to `composedagent.py`

---

### 3. `AgentHealthCheck`

**Line**: 54  
**Methods**: 0

Health check result for an agent.

[TIP] **Suggested split**: Move to `agenthealthcheck.py`

---

### 4. `AgentPluginConfig`

**Line**: 64  
**Methods**: 0

Configuration for an agent plugin.

[TIP] **Suggested split**: Move to `agentpluginconfig.py`

---

### 5. `ExecutionProfile`

**Line**: 74  
**Methods**: 0

A profile for agent execution settings.

[TIP] **Suggested split**: Move to `executionprofile.py`

---

### 6. `AgentPipeline`

**Line**: 84  
**Methods**: 2

Chains agent steps sequentially.

[TIP] **Suggested split**: Move to `agentpipeline.py`

---

### 7. `AgentParallel`

**Line**: 100  
**Methods**: 2

Executes agent branches in parallel conceptually.

[TIP] **Suggested split**: Move to `agentparallel.py`

---

### 8. `AgentRouter`

**Line**: 110  
**Methods**: 3

Routes input based on conditions.

[TIP] **Suggested split**: Move to `agentrouter.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
