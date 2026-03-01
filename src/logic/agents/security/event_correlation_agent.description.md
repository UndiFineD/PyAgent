# event_correlation_agent

**File**: `src\logic\agents\security\event_correlation_agent.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 9 imports  
**Lines**: 142  
**Complexity**: 11 (moderate)

## Overview

Event correlation agent module.
Correlates security events and agent interactions to identify patterns and threats.
Inspired by AD-Canaries event correlation using KQL queries.

## Classes (2)

### `EventCorrelator`

Core event correlation logic.

**Methods** (5):
- `__init__(self)`
- `add_event(self, event)`
- `correlate_events(self, correlation_rules)`
- `_apply_rule(self, rule)`
- `_events_related(self, event1, event2, conditions, time_window)`

### `EventCorrelationAgent`

**Inherits from**: BaseAgent

Correlates events across the system to identify security threats and patterns.
Based on AD-Canaries event correlation patterns using log analysis.

**Methods** (6):
- `__init__(self, file_path)`
- `add_event(self, event)`
- `define_correlation_rule(self, name, event_type, conditions, time_window)`
- `run_correlation(self)`
- `get_correlations(self)`
- `list_rules(self)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `collections.defaultdict`
- `logging`
- `src.core.base.common.base_utilities.as_tool`
- `src.core.base.lifecycle.base_agent.BaseAgent`
- `src.core.base.lifecycle.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
