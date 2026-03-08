# Class Breakdown: agents

**File**: `src\observability\stats\agents.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `StatsAgent`

**Line**: 26  
**Methods**: 3

Agent that calculates statistics for fleet progress and file maintenance.

[TIP] **Suggested split**: Move to `statsagent.py`

---

### 2. `ReportingAgent`

**Line**: 88  
**Inherits**: BaseAgent  
**Methods**: 1

Observer agent that generates executive dashboards and reports.

[TIP] **Suggested split**: Move to `reportingagent.py`

---

### 3. `TransparencyAgent`

**Line**: 100  
**Inherits**: BaseAgent  
**Methods**: 2

Provides a detailed audit trail of agent thoughts, signals, and dependencies.

[TIP] **Suggested split**: Move to `transparencyagent.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
