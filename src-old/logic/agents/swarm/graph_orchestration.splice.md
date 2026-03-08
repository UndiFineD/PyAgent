# Class Breakdown: graph_orchestration

**File**: `src\logic\agents\swarm\graph_orchestration.py`  
**Classes**: 14

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ExecutionContext`

**Line**: 37  
**Methods**: 2

Simple execution context for orchestration.

[TIP] **Suggested split**: Move to `executioncontext.py`

---

### 2. `OrchestrationStatus`

**Line**: 61  
**Inherits**: Enum  
**Methods**: 0

Status of orchestration execution.

[TIP] **Suggested split**: Move to `orchestrationstatus.py`

---

### 3. `OrchestrationState`

**Line**: 71  
**Methods**: 1

Base state for orchestration workflows.

[TIP] **Suggested split**: Move to `orchestrationstate.py`

---

### 4. `GraphEdge`

**Line**: 86  
**Methods**: 0

Represents an edge between runners in the orchestration graph.

[TIP] **Suggested split**: Move to `graphedge.py`

---

### 5. `OrchestrationResult`

**Line**: 95  
**Methods**: 0

Result of a runner execution.

[TIP] **Suggested split**: Move to `orchestrationresult.py`

---

### 6. `OrchestrationRunnable`

**Line**: 105  
**Inherits**: ABC  
**Methods**: 3

Abstract base class for orchestration runners (nodes).

[TIP] **Suggested split**: Move to `orchestrationrunnable.py`

---

### 7. `OrchestrationAdvancer`

**Line**: 126  
**Methods**: 2

Handles transitions between runners based on execution results.

Inspired by LLM Tornado's advancer concept.

[TIP] **Suggested split**: Move to `orchestrationadvancer.py`

---

### 8. `OrchestrationGraph`

**Line**: 149  
**Inherits**: Unknown  
**Methods**: 5

Immutable orchestration graph definition.

Based on LLM Tornado's OrchestrationGraph pattern.

[TIP] **Suggested split**: Move to `orchestrationgraph.py`

---

### 9. `OrchestrationGraphBuilder`

**Line**: 191  
**Inherits**: Unknown  
**Methods**: 7

Fluent builder for creating orchestration graphs.

Inspired by LLM Tornado's OrchestrationGraphBuilder pattern.

[TIP] **Suggested split**: Move to `orchestrationgraphbuilder.py`

---

### 10. `Orchestrator`

**Line**: 282  
**Inherits**: Unknown  
**Methods**: 4

Main orchestrator that executes orchestration graphs.

Based on LLM Tornado's orchestrator concept.

[TIP] **Suggested split**: Move to `orchestrator.py`

---

### 11. `AgentTaskState`

**Line**: 475  
**Inherits**: OrchestrationState  
**Methods**: 0

State for agent task orchestration.

[TIP] **Suggested split**: Move to `agenttaskstate.py`

---

### 12. `AgentRunner`

**Line**: 483  
**Inherits**: OrchestrationRunnable  
**Methods**: 1

Runner that executes agent tasks.

[TIP] **Suggested split**: Move to `agentrunner.py`

---

### 13. `ConditionalRunner`

**Line**: 511  
**Inherits**: OrchestrationRunnable  
**Methods**: 1

Runner that executes based on conditions.

[TIP] **Suggested split**: Move to `conditionalrunner.py`

---

### 14. `GraphOrchestrationMixin`

**Line**: 540  
**Methods**: 6

Mixin to add graph-based orchestration capabilities to PyAgent orchestrators.

This provides the LLM Tornado-inspired orchestration framework.

[TIP] **Suggested split**: Move to `graphorchestrationmixin.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
