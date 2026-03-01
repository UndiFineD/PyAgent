# Class Breakdown: change_monitoring_agent

**File**: `src\core\agents\change_monitoring_agent.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ChangeDataSource`

**Line**: 44  
**Inherits**: ABC  
**Methods**: 0

Abstract base class for data sources that support change monitoring.

[TIP] **Suggested split**: Move to `changedatasource.py`

---

### 2. `FileSystemDataSource`

**Line**: 63  
**Inherits**: ChangeDataSource  
**Methods**: 1

Example data source for file system monitoring.

[TIP] **Suggested split**: Move to `filesystemdatasource.py`

---

### 3. `HistoryManager`

**Line**: 110  
**Methods**: 5

Manages change history for comparison and analysis.

[TIP] **Suggested split**: Move to `historymanager.py`

---

### 4. `ChangeMonitoringAgent`

**Line**: 143  
**Inherits**: BaseAgent, DataProcessingMixin  
**Methods**: 4

Agent for monitoring changes in data sources using incremental patterns.

Inspired by ADSpider's real-time change detection using USN and replication metadata.

[TIP] **Suggested split**: Move to `changemonitoringagent.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
