# FleetTelemetryVisualizer

**File**: `src\infrastructure\orchestration\FleetTelemetryVisualizer.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 105  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for FleetTelemetryVisualizer.

## Classes (1)

### `FleetTelemetryVisualizer`

Phase 37: Swarm Telemetry Visualization.
Visualizes signal flow and task execution paths across the fleet.

**Methods** (6):
- `__init__(self, fleet)`
- `log_signal_flow(self, signal_name, sender, receivers)`
- `generate_mermaid_flow(self)`
- `identify_bottlenecks(self)`
- `get_fleet_version_map(self)`
- `get_version_drift_report(self)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `logging`
- `src.core.base.version.VERSION`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
