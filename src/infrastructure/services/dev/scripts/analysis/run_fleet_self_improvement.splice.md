# Class Breakdown: run_fleet_self_improvement

**File**: `src\infrastructure\services\dev\scripts\analysis\run_fleet_self_improvement.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `DirectiveParser`

**Line**: 61  
**Methods**: 4

Parses strategic directives from prompt and context files.

[TIP] **Suggested split**: Move to `directiveparser.py`

---

### 2. `IntelligenceHarvester`

**Line**: 120  
**Methods**: 2

Orchestrates external intelligence harvesting.

[TIP] **Suggested split**: Move to `intelligenceharvester.py`

---

### 3. `CycleOrchestrator`

**Line**: 191  
**Methods**: 3

Manages the execution of multiple improvement cycles.

[TIP] **Suggested split**: Move to `cycleorchestrator.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
