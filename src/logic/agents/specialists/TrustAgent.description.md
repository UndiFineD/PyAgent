# TrustAgent

**File**: `src\logic\agents\specialists\TrustAgent.py`  
**Type**: Python Module  
**Summary**: 5 classes, 0 functions, 15 imports  
**Lines**: 260  
**Complexity**: 7 (moderate)

## Overview

Python module containing implementation for TrustAgent.

## Classes (5)

### `Mood`

**Inherits from**: Enum

Class Mood implementation.

### `TrustLevel`

**Inherits from**: Enum

Class TrustLevel implementation.

### `EmotionalState`

Represents the current emotional state of an interaction.

### `TrustMetrics`

Tracks trust-related metrics over time.

### `TrustAgent`

**Inherits from**: BaseAgent

Agent specializing in human-agent alignment, mood detection, 
emotional intelligence, and maintaining trust scores for interaction safety.

**Methods** (7):
- `__init__(self, file_path)`
- `trust_score(self)`
- `mood(self)`
- `trust_level(self)`
- `get_trust_report(self)`
- `_update_trust(self, adjustment, reason)`
- `_map_emotion_to_mood(self, emotion)`

## Dependencies

**Imports** (15):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `json`
- `logging`
- `re`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.BaseUtilities.as_tool`
- `src.core.base.Version.VERSION`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
