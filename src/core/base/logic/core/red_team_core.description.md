# red_team_core

**File**: `src\core\base\logic\core\red_team_core.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 8 imports  
**Lines**: 75  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for red_team_core.

## Classes (2)

### `RedTeamChallenge`

Class RedTeamChallenge implementation.

### `RedTeamCore`

Manages security 'Challenges' and internal red-teaming scenarios.
Used to stress-test GuardrailCore and identify prompt injection vulnerabilities.
Harvested from .external/AI-Red-Teaming-Playground-Labs pattern.

**Methods** (4):
- `__init__(self, challenges_path)`
- `_load_challenges(self, path)`
- `evaluate_response(self, challenge_id, response_text)`
- `get_metaprompt(self, challenge_id)`

## Dependencies

**Imports** (8):
- `dataclasses.dataclass`
- `json`
- `pathlib.Path`
- `re`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
