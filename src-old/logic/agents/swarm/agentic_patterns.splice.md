# Class Breakdown: agentic_patterns

**File**: `src\logic\agents\swarm\agentic_patterns.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `SequentialAgentConfig`

**Line**: 29  
**Methods**: 0

Configuration for sequential agent execution.

[TIP] **Suggested split**: Move to `sequentialagentconfig.py`

---

### 2. `SequentialAgentPattern`

**Line**: 40  
**Methods**: 2

Sequential agent execution pattern.

This pattern executes agents in sequence, where each agent's output
can be used as input for subsequent agents. Inspired by agentic design
patterns from ADK (Agent...

[TIP] **Suggested split**: Move to `sequentialagentpattern.py`

---

### 3. `ParallelAgentPattern`

**Line**: 247  
**Methods**: 2

Parallel agent execution pattern.

This pattern executes multiple agents concurrently and combines their results.
Inspired by agentic design patterns from ADK.

[TIP] **Suggested split**: Move to `parallelagentpattern.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
