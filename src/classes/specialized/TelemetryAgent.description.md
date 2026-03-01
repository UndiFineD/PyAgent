# TelemetryAgent

**File**: `src\classes\specialized\TelemetryAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 87  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for TelemetryAgent.

## Classes (1)

### `TelemetryAgent`

**Inherits from**: BaseAgent

Tier 5 (Maintenance) - Telemetry Agent: Responsible for broadcasting fleet 
telemetry and archiving interactions for swarm intelligence harvesting.

**Methods** (4):
- `__init__(self, api_url, workspace_root)`
- `_record(self, event_type, data)`
- `log_event(self, event_type, source, data)`
- `get_recent_logs(self)`

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `json`
- `pathlib.Path`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.ConnectivityManager.ConnectivityManager`
- `src.core.base.Version.VERSION`
- `src.infrastructure.backend.LocalContextRecorder.LocalContextRecorder`
- `src.observability.StructuredLogger.StructuredLogger`
- `time`
- `typing.Any`

---
*Auto-generated documentation*
