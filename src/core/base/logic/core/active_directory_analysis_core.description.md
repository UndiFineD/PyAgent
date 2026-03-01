# active_directory_analysis_core

**File**: `src\core\base\logic\core\active_directory_analysis_core.py`  
**Type**: Python Module  
**Summary**: 6 classes, 0 functions, 12 imports  
**Lines**: 810  
**Complexity**: 2 (simple)

## Overview

Active Directory Analysis Core

This core provides comprehensive analysis capabilities for Active Directory environments,
including enumeration, privilege escalation detection, and security assessment.

Based on patterns from Active-Directory-Exploitation-Cheat-Sheet repository.

## Classes (6)

### `PrivilegeLevel`

**Inherits from**: Enum

Active Directory privilege levels

### `ADObjectType`

**Inherits from**: Enum

Active Directory object types

### `ADObject`

Represents an Active Directory object

### `ADEnumerationResult`

Results from AD enumeration

### `ADVulnerability`

Represents a detected AD vulnerability

### `ActiveDirectoryAnalysisCore`

Core for analyzing Active Directory environments and detecting security vulnerabilities.

This core implements patterns from the Active-Directory-Exploitation-Cheat-Sheet
for comprehensive AD security assessment.

**Methods** (2):
- `__init__(self)`
- `_is_base64_like(self, text)`

## Dependencies

**Imports** (12):
- `asyncio`
- `base64`
- `binascii`
- `dataclasses.dataclass`
- `enum.Enum`
- `logging`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`
- `typing.Tuple`

---
*Auto-generated documentation*
