# Class Breakdown: agent_api_server

**File**: `src\infrastructure\services\api\agent_api_server.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `TaskRequest`

**Line**: 44  
**Inherits**: BaseModel  
**Methods**: 0

Schema for incoming task requests via the REST API.

[TIP] **Suggested split**: Move to `taskrequest.py`

---

### 2. `TelemetryManager`

**Line**: 55  
**Methods**: 2

Manages WebSocket connections for real-time fleet telemetry.

[TIP] **Suggested split**: Move to `telemetrymanager.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
