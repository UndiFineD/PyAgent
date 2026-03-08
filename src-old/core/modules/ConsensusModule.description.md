# ConsensusModule

**File**: `src\core\modules\ConsensusModule.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 78  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for ConsensusModule.

## Classes (1)

### `ConsensusModule`

**Inherits from**: BaseModule

Consolidated core module for consensus protocols.
Migrated from ConsensusCore.

**Methods** (5):
- `initialize(self)`
- `execute(self, proposals, weights)`
- `calculate_winner(self, proposals, weights)`
- `get_agreement_score(self, proposals, winner)`
- `shutdown(self)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `src.core.base.modules.BaseModule`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
