# bloodhound_integration_core

**File**: `src\core\base\logic\core\bloodhound_integration_core.py`  
**Type**: Python Module  
**Summary**: 8 classes, 0 functions, 17 imports  
**Lines**: 859  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for bloodhound_integration_core.

## Classes (8)

### `RiskLevel`

**Inherits from**: Enum

Risk severity levels

### `ADObjectType`

**Inherits from**: Enum

Active Directory object types

### `SecurityControl`

**Inherits from**: Enum

Security controls that can be assessed

### `ADObject`

Represents an Active Directory object

### `SecurityFinding`

Represents a security finding

### `ControlPath`

Represents a control path in the AD graph

### `AuditReport`

Comprehensive audit report

### `BloodHoundIntegrationCore`

BloodHound Integration Core for graph-based Active Directory security analysis.

Provides comprehensive AD security assessment using graph database patterns,
risk analysis, and security control evaluation based on AD_Miner methodologies.

**Methods** (1):
- `__init__(self)`

## Dependencies

**Imports** (17):
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `datetime.timedelta`
- `enum.Enum`
- `json`
- `logging`
- `pathlib.Path`
- `re`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`
- ... and 2 more

---
*Auto-generated documentation*
