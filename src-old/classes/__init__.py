"""
LLM_CONTEXT_START

## Source: src-old/classes/__init__.description.md

# __init__

**File**: `src\classes\__init__.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 21 imports  
**Lines**: 35  
**Complexity**: 0 (simple)

## Overview

Core class hierarchy for the PyAgent ecosystem.

## Dependencies

**Imports** (21):
- `base_agent.BaseAgent`
- `coder.ArchAdvisorAgent.ArchAdvisorAgent`
- `coder.DocumentationAgent.DocumentationAgent`
- `coder.LintingAgent.LintingAgent`
- `coder.QualityGateAgent.QualityGateAgent`
- `coder.ReasoningAgent.ReasoningAgent`
- `coder.SecurityGuardAgent.SecurityGuardAgent`
- `coder.SelfHealingAgent.SelfHealingAgent`
- `coder.SelfOptimizerAgent.SelfOptimizerAgent`
- `coder.TypeSafetyAgent.TypeSafetyAgent`
- `context.GlobalContextEngine.GlobalContextEngine`
- `context.GraphContextEngine.GraphContextEngine`
- `context.KnowledgeAgent.KnowledgeAgent`
- `context.MemoryEngine.MemoryEngine`
- `fleet.AsyncFleetManager.AsyncFleetManager`
- ... and 6 more

---
*Auto-generated documentation*
## Source: src-old/classes/__init__.improvements.md

# Improvements for __init__

**File**: `src\classes\__init__.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 35 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `__init___test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

"""
Core class hierarchy for the PyAgent ecosystem.
"""

# Classes package initialization

from .base_agent import BaseAgent
from .context.KnowledgeAgent import KnowledgeAgent
from .context.GraphContextEngine import GraphContextEngine
from .context.MemoryEngine import MemoryEngine

try:
    from .stats.ObservabilityEngine import ObservabilityEngine
    from .stats.ResourceMonitor import ResourceMonitor
except ImportError:
    # Handle cases where stats might have import issues during heavy refactoring
    pass
from .coder.SecurityGuardAgent import SecurityGuardAgent

from .coder.LintingAgent import LintingAgent
from .coder.SelfOptimizerAgent import SelfOptimizerAgent
from .coder.TypeSafetyAgent import TypeSafetyAgent
from .coder.DocumentationAgent import DocumentationAgent
from .coder.QualityGateAgent import QualityGateAgent
from .coder.ArchAdvisorAgent import ArchAdvisorAgent
from .fleet.FleetManager import FleetManager

from .fleet.AsyncFleetManager import AsyncFleetManager
from .fleet.TaskPlannerAgent import TaskPlannerAgent
from .fleet.WorkflowState import WorkflowState
from .coder.ReasoningAgent import ReasoningAgent
from .coder.SelfHealingAgent import SelfHealingAgent
from .orchestration.ToolRegistry import ToolRegistry
from .context.GlobalContextEngine import GlobalContextEngine
