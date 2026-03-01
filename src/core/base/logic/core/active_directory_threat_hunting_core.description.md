# active_directory_threat_hunting_core

**File**: `src\core\base\logic\core\active_directory_threat_hunting_core.py`  
**Type**: Python Module  
**Summary**: 6 classes, 0 functions, 16 imports  
**Lines**: 745  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for active_directory_threat_hunting_core.

## Classes (6)

### `ThreatLevel`

**Inherits from**: Enum

Threat severity levels

### `ADObjectType`

**Inherits from**: Enum

Active Directory object types

### `ADObject`

Represents an Active Directory object

### `ThreatFinding`

Represents a threat hunting finding

### `HuntingResult`

Results from a threat hunting operation

### `ActiveDirectoryThreatHuntingCore`

**Inherits from**: BaseCore

Active Directory Threat Hunting Core for comprehensive AD security analysis.

Provides capabilities for Active Directory enumeration, threat detection,
permission analysis, and security monitoring based on advanced threat hunting patterns.

**Methods** (1):
- `__init__(self)`

## Dependencies

**Imports** (16):
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `datetime.timedelta`
- `enum.Enum`
- `json`
- `logging`
- `src.core.base.common.base_core.BaseCore`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`
- `typing.Tuple`
- ... and 1 more

---
*Auto-generated documentation*
