# Class Breakdown: agent_models

**File**: `src\core\base\common\models\agent_models.py`  
**Classes**: 8

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `AgentConfig`

**Line**: 30  
**Methods**: 0

Agent configuration from environment or file.

[TIP] **Suggested split**: Move to `agentconfig.py`

---

### 2. `ComposedAgent`

**Line**: 48  
**Methods**: 0

Configuration for agent composition.

[TIP] **Suggested split**: Move to `composedagent.py`

---

### 3. `AgentHealthCheck`

**Line**: 58  
**Methods**: 0

Health check result for an agent.

[TIP] **Suggested split**: Move to `agenthealthcheck.py`

---

### 4. `AgentPluginConfig`

**Line**: 72  
**Methods**: 0

Configuration for an agent plugin.

[TIP] **Suggested split**: Move to `agentpluginconfig.py`

---

### 5. `ExecutionProfile`

**Line**: 84  
**Methods**: 0

A profile for agent execution settings.

[TIP] **Suggested split**: Move to `executionprofile.py`

---

### 6. `AgentPipeline`

**Line**: 97  
**Methods**: 2

Chains agent steps sequentially.

[TIP] **Suggested split**: Move to `agentpipeline.py`

---

### 7. `AgentParallel`

**Line**: 115  
**Methods**: 2

Executes agent branches in parallel conceptually.

[TIP] **Suggested split**: Move to `agentparallel.py`

---

### 8. `AgentRouter`

**Line**: 130  
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
