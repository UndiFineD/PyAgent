# ConsensusCore

**File**: `src\infrastructure\orchestration\ConsensusCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 64  
**Complexity**: 3 (simple)

## Overview

ConsensusCore logic for multi-agent voting.
Contains pure logic for tallying votes, handling ties, and selecting winners.

## Classes (1)

### `ConsensusCore`

Pure logic core for consensus protocols.

**Methods** (3):
- `__init__(self, mode)`
- `calculate_winner(self, proposals, weights)`
- `get_agreement_score(self, proposals, winner)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `src.core.base.version.VERSION`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
