#!/usr/bin/env python3
# Refactored by copilot-placeholder
# Refactored by copilot-placeholder
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

"""
Event Correlation Agent - Correlates security events and agent interactions

Brief Summary
DATE: 2026-02-13
AUTHOR: Keimpe de Jong
USAGE:
- Instantiate EventCorrelationAgent with the agent's state file path.
- Use add_event(event: Dict[str, Any]) to submit events into the engine.
- Use define_correlation_rule(name, event_type, conditions, time_window=300) to register correlation rules.
- Call run_correlation() to execute rules and return matches.
- Call get_correlations() to retrieve accumulated correlation results.

WHAT IT DOES:
Implements an in-process event correlation engine (EventCorrelator) and an EventCorrelationAgent wrapper exposing tool-decorated methods for adding events, defining rules, running correlation, and retrieving results. Provides a simple rule model (event_type, conditions, time_window) and a proximity-based matching algorithm that groups events sharing attributes within a temporal window. Designed for detect­ing repeating patterns, anomalies or basic threat indicators across agent and security event streams.

WHAT IT SHOULD DO BETTER:
- Persist events and correlations to durable storage or the agent StateTransaction to survive restarts and support larger datasets.
- Support richer rule languages (logical operators, regex, multi-attribute matching), chained/hierarchical rules, and weighting/scoring of correlations rather than binary matches.
- Improve time handling (use timezone-aware datetimes), handle out-of-order timestamps, and optimize performance for high-volume streams (indexing, incremental correlation, or Rust-accelerated cores).
- Add provenance, confidence scores, and metadata linking back to original sources; expose streaming/async APIs with asyncio for non-blocking ingestion; and include comprehensive unit tests and input validation/error handling.

FILE CONTENT SUMMARY:
Event correlation agent module.
Correlates security events and agent interactions to identify patterns and threats.
Inspired by AD-Canaries event correlation using KQL queries.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class EventCorrelator:
    """Core event correlation logic."""

    def __init__(self):
        self.events: List[Dict[str, Any]] = []
        self.correlations: List[Dict[str, Any]] = []

    def add_event(self, event: Dict[str, Any]) -> None:
        """Add an event to the correlation engine."""
        self.events.append(event)

    def correlate_events(self, correlation_rules: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Apply correlation rules to find related events."""
        correlations = []
        for rule in correlation_rules:
            matches = self._apply_rule(rule)
            if matches:
                correlations.extend(matches)
        self.correlations.extend(correlations)
        return correlations

    def _apply_rule(self, rule: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Apply a single correlation rule."""
        matches = []
        event_type = rule.get("event_type")
        conditions = rule.get("conditions", {})
        time_window = rule.get("time_window", 300)  # 5 minutes default

        # Simple correlation: find events matching conditions within time window
        relevant_events = [e for e in self.events if e.get("type") == event_type]

        for i, event in enumerate(relevant_events):
            correlated = [event]
            for other in relevant_events[i + 1 :]:
                if self._events_related(event, other, conditions, time_window):
                    correlated.append(other)
            if len(correlated) > 1:
                matches.append({"rule": rule.get("name", "unknown"), "events": correlated})
        return matches

    def _events_related(
        self, event1: Dict[str, Any], event2: Dict[str, Any], conditions: Dict[str, Any], time_window: int
    ) -> bool:
        """Check if two events are related based on conditions."""
        # Check time proximity
        time1 = event1.get("timestamp", 0)
        time2 = event2.get("timestamp", 0)
        if abs(time1 - time2) > time_window:
            return False

        # Check shared attributes
        for key, value in conditions.items():
            if event1.get(key) == value and event2.get(key) == value:
                return True
        return False


class EventCorrelationAgent(BaseAgent):  # pylint: disable=too-many-ancestors
    """
    Correlates events across the system to identify security threats and patterns.
    Based on AD-Canaries event correlation patterns using log analysis.
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.correlator = EventCorrelator()
        self.correlation_rules: List[Dict[str, Any]] = []
        self._system_prompt = (
            "You are the Event Correlation Agent. Your purpose is to analyze "
            "events from various sources and correlate them to identify "
            "security threats, anomalies, and behavioral patterns."
        )

    @as_tool
    def add_event(self, event: Dict[str, Any]) -> None:
        """Add an event for correlation analysis."""
        self.correlator.add_event(event)

    @as_tool
    def define_correlation_rule(
        self, name: str, event_type: str, conditions: Dict[str, Any], time_window: int = 300
    ) -> None:
        """Define a new correlation rule."""
        rule = {"name": name, "event_type": event_type, "conditions": conditions, "time_window": time_window}
        self.correlation_rules.append(rule)
        logging.info(f"Defined correlation rule: {name}")

    @as_tool
    def run_correlation(self) -> List[Dict[str, Any]]:
        """Run correlation analysis on current events."""
        correlations = self.correlator.correlate_events(self.correlation_rules)
        logging.info(f"Found {len(correlations)} correlations")
        return correlations

    @as_tool
    def get_correlations(self) -> List[Dict[str, Any]]:
        """Get all found correlations."""
        return self.correlator.correlations

    @as_tool
    def list_rules(self) -> List[Dict[str, Any]]:
        """List all defined correlation rules."""
        return self.correlation_rules
