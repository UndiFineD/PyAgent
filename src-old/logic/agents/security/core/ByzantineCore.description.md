# ByzantineCore

**File**: `src\logic\agents\security\core\ByzantineCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 75  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for ByzantineCore.

## Classes (1)

### `ByzantineCore`

Pure logic for Byzantine Fault Tolerance (BFT) consensus.
Calculates weighted agreement scores and detect malicious deviations.

**Methods** (4):
- `calculate_agreement_score(self, votes)`
- `select_committee(self, agents_reliability, min_size)`
- `get_required_quorum(self, change_type)`
- `detect_deviating_hashes(self, votes, consensus_hash)`

## Dependencies

**Imports** (3):
- `__future__.annotations`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
