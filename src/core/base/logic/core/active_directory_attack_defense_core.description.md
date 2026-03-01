# active_directory_attack_defense_core

**File**: `src\core\base\logic\core\active_directory_attack_defense_core.py`  
**Type**: Python Module  
**Summary**: 8 classes, 0 functions, 17 imports  
**Lines**: 839  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for active_directory_attack_defense_core.

## Classes (8)

### `KillChainPhase`

**Inherits from**: Enum

Active Directory Kill Chain phases

### `AttackTechnique`

**Inherits from**: Enum

Common AD attack techniques

### `DefenseControl`

**Inherits from**: Enum

Defense and detection controls

### `AttackVector`

Represents an attack vector in AD

### `DefenseAssessment`

Assessment of defensive controls

### `KillChainAnalysis`

Analysis of AD kill chain progression

### `SecurityPosture`

Overall AD security posture assessment

### `ActiveDirectoryAttackDefenseCore`

Active Directory Attack & Defense Core for comprehensive AD security analysis.

Provides kill chain analysis, attack simulation, defense assessment,
and security posture evaluation based on AD-Attack-Defense methodologies.

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
