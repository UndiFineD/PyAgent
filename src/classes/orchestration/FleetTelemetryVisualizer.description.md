# FleetTelemetryVisualizer

**File**: `src\classes\orchestration\FleetTelemetryVisualizer.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 60  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for FleetTelemetryVisualizer.

## Classes (1)

### `FleetTelemetryVisualizer`

Phase 37: Swarm Telemetry Visualization.
Visualizes signal flow and task execution paths across the fleet.

**Methods** (4):
- `__init__(self, fleet)`
- `log_signal_flow(self, signal_name, sender, receivers)`
- `generate_mermaid_flow(self)`
- `identify_bottlenecks(self)`

## Dependencies

**Imports** (6):
- `logging`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
