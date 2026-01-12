#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.



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

    def log_signal_flow(self, signal_name: str, sender: str, receivers: List[str]) -> str:
        """Logs a signal flow event for visualization."""
        event = {
            "timestamp": time.time(),
            "signal": signal_name,
            "sender": sender,
            "receivers": receivers
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
        if total == 0: return []
        return [k for k, v in traffic.items() if v / total >= 0.39]
