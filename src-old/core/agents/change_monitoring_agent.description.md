# change_monitoring_agent

**File**: `src\core\agents\change_monitoring_agent.py`  
**Type**: Python Module  
**Summary**: 4 classes, 0 functions, 16 imports  
**Lines**: 308  
**Complexity**: 10 (moderate)

## Overview

Change Monitoring Agent for PyAgent.

Monitors changes in various data sources using incremental update patterns
inspired by ADSpider's USN-based change detection.

## Classes (4)

### `ChangeDataSource`

**Inherits from**: ABC

Abstract base class for data sources that support change monitoring.

### `FileSystemDataSource`

**Inherits from**: ChangeDataSource

Example data source for file system monitoring.

**Methods** (1):
- `__init__(self, watch_path)`

### `HistoryManager`

Manages change history for comparison and analysis.

**Methods** (5):
- `__init__(self, max_history)`
- `add_change(self, change)`
- `get_previous_value(self, object_id, attribute)`
- `save_to_file(self, filepath)`
- `load_from_file(self, filepath)`

### `ChangeMonitoringAgent`

**Inherits from**: BaseAgent, DataProcessingMixin

Agent for monitoring changes in data sources using incremental patterns.

Inspired by ADSpider's real-time change detection using USN and replication metadata.

**Methods** (4):
- `__init__(self, file_path)`
- `add_data_source(self, name, data_source)`
- `set_output_file(self, filepath)`
- `set_poll_interval(self, interval)`

## Dependencies

**Imports** (16):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `asyncio`
- `json`
- `logging`
- `pathlib.Path`
- `src.core.base.lifecycle.base_agent.BaseAgent`
- `src.core.base.lifecycle.version.VERSION`
- `src.core.base.mixins.data_processing_mixin.DataProcessingMixin`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- ... and 1 more

---
*Auto-generated documentation*
