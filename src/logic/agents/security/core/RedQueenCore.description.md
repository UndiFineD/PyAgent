# RedQueenCore

**File**: `src\logic\agents\security\core\RedQueenCore.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 4 imports  
**Lines**: 48  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for RedQueenCore.

## Classes (2)

### `AttackVector`

Class AttackVector implementation.

### `RedQueenCore`

Pure logic for the 'Digital Red Queen' adversarial evolution.
Generates and mutates prompts to test security guardrails.

**Methods** (3):
- `mutate_prompt(self, base_prompt, strategy)`
- `evaluate_bypass(self, response, forbidden_patterns)`
- `select_parent_attacks(self, archive, count)`

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `dataclasses.dataclass`
- `re`
- `typing.List`

---
*Auto-generated documentation*
