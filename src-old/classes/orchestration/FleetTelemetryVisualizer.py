#!/usr/bin/env python3

"""
LLM_CONTEXT_START

## Source: src-old/classes/orchestration/FleetTelemetryVisualizer.description.md

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
## Source: src-old/classes/orchestration/FleetTelemetryVisualizer.improvements.md

# Improvements for FleetTelemetryVisualizer

**File**: `src\classes\orchestration\FleetTelemetryVisualizer.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 60 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `FleetTelemetryVisualizer_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

import logging
import time
from typing import Dict, List, Any, Optional


class FleetTelemetryVisualizer:
    """
    Phase 37: Swarm Telemetry Visualization.
    Visualizes signal flow and task execution paths across the fleet.
    """

    def __init__(self, fleet) -> None:
        self.fleet = fleet
        self.signal_events: List[Dict[str, Any]] = []

    def log_signal_flow(
        self, signal_name: str, sender: str, receivers: List[str]
    ) -> str:
        """Logs a signal flow event for visualization."""
        event = {
            "timestamp": time.time(),
            "signal": signal_name,
            "sender": sender,
            "receivers": receivers,
        }
        self.signal_events.append(event)
        logging.info(f"Telemetry: Logged signal flow '{signal_name}' from {sender}")

    def generate_mermaid_flow(self) -> str:
        """Generates a Mermaid.js diagram of the fleet's recent interaction flow."""
        if not self.signal_events:
            return "graph TD\n  Start[No Signal Traffic Detected]"

        nodes = set()
        edges = []
        # Take last 10 events
        for event in self.signal_events[-10:]:
            sender = event["sender"]
            nodes.add(sender)
            for receiver in event["receivers"]:
                nodes.add(receiver)
                edges.append(f"  {sender} --|{event['signal']}|--> {receiver}")

        mermaid = "graph TD\n"
        for edge in set(edges):
            mermaid += f"{edge}\n"

        return mermaid

    def identify_bottlenecks(self) -> List[str]:
        """Identifies agents that are high-frequency senders or receivers."""
        traffic = {}
        for event in self.signal_events:
            traffic[event["sender"]] = traffic.get(event["sender"], 0) + 1
            for r in event["receivers"]:
                traffic[r] = traffic.get(r, 0) + 1

        # Return agents with >= 40% of traffic
        total = sum(traffic.values())
        if total == 0:
            return []
        return [k for k, v in traffic.items() if v / total >= 0.39]
