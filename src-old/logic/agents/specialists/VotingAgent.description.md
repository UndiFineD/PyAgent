# VotingAgent

**File**: `src\logic\agents\specialists\VotingAgent.py`  
**Type**: Python Module  
**Summary**: 5 classes, 0 functions, 17 imports  
**Lines**: 382  
**Complexity**: 7 (moderate)

## Overview

Python module containing implementation for VotingAgent.

## Classes (5)

### `VotingMethod`

**Inherits from**: Enum

Class VotingMethod implementation.

### `VoteStatus`

**Inherits from**: Enum

Class VoteStatus implementation.

### `Vote`

Represents a single vote.

### `VotingSession`

Represents a voting session.

### `VotingAgent`

**Inherits from**: BaseAgent

Agent specializing in evaluation and consensus.
Gathers votes from multiple agents to decide on a 'truth' or 'best path'.
Supports multiple voting methods including ranked choice and quadratic voting.

**Methods** (7):
- `__init__(self, file_path)`
- `_tally_majority(self, session)`
- `_tally_weighted(self, session)`
- `_tally_ranked_choice(self, session)`
- `_tally_borda(self, session)`
- `_tally_approval(self, session)`
- `_tally_quadratic(self, session)`

## Dependencies

**Imports** (17):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `json`
- `logging`
- `math`
- `re`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.BaseUtilities.as_tool`
- `src.core.base.Version.VERSION`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- ... and 2 more

---
*Auto-generated documentation*
