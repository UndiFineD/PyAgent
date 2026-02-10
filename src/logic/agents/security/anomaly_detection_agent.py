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

"""
Anomaly detection agent module.
Detects anomalous behavior in agent interactions, inspired by AD-Canaries monitoring patterns.
"""

from __future__ import annotations

import logging
import statistics
from collections import defaultdict, deque
from typing import Any, Dict, List

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class AnomalyDetector:
    """Core anomaly detection logic."""

    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.agent_interactions: Dict[str, deque] = defaultdict(lambda: deque(maxlen=window_size))
        self.baseline_stats: Dict[str, Dict[str, float]] = {}

    def record_interaction(self, agent_id: str, interaction: Dict[str, Any]) -> None:
        """Record an agent interaction."""
        self.agent_interactions[agent_id].append(interaction)

    def detect_anomaly(self, agent_id: str, current_interaction: Dict[str, Any]) -> bool:
        """Detect if current interaction is anomalous."""
        if len(self.agent_interactions[agent_id]) < 10:  # Need baseline
            return False

        # Simple anomaly detection based on interaction frequency and types
        interactions = list(self.agent_interactions[agent_id])
        types = [str(i.get("type", "unknown")) for i in interactions]
        frequencies: Dict[str, int] = {}
        for t in types:
            frequencies[t] = frequencies.get(t, 0) + 1

        current_type = current_interaction.get("type", "unknown")
        if current_type not in frequencies:
            return True  # New type

        # Check if frequency deviates significantly
        mean_freq = statistics.mean(frequencies.values())
        std_freq = statistics.stdev(frequencies.values()) if len(frequencies) > 1 else 0
        if std_freq > 0 and abs(frequencies[current_type] - mean_freq) > 2 * std_freq:
            return True

        return False

    def update_baseline(self, agent_id: str) -> None:
        """Update baseline statistics."""
        if len(self.agent_interactions[agent_id]) >= 10:
            interactions = list(self.agent_interactions[agent_id])
            types = [i.get("type", "unknown") for i in interactions]
            self.baseline_stats[agent_id] = {
                "mean_interactions": statistics.mean([len(types)]),
                "common_types": max(set(types), key=types.count),
            }


class AnomalyDetectionAgent(BaseAgent):  # pylint: disable=too-many-ancestors
    """
    Monitors agent behavior for anomalies, using statistical analysis and pattern recognition.
    Inspired by AD-Canaries event monitoring and correlation.
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.detector = AnomalyDetector()
        self.anomalies: List[Dict[str, Any]] = []
        self._system_prompt = (
            "You are the Anomaly Detection Agent. Your purpose is to monitor "
            "agent interactions and detect anomalous behavior that may indicate "
            "security threats or system issues."
        )

    @as_tool
    def record_agent_interaction(self, agent_id: str, interaction: Dict[str, Any]) -> None:
        """Record an agent interaction for analysis."""
        if self.detector.detect_anomaly(agent_id, interaction):
            self._log_anomaly(agent_id, interaction)
        self.detector.record_interaction(agent_id, interaction)

    @as_tool
    def check_agent_anomalies(self, agent_id: str) -> List[Dict[str, Any]]:
        """Check anomalies for a specific agent."""
        return [a for a in self.anomalies if a["agent_id"] == agent_id]

    @as_tool
    def get_all_anomalies(self) -> List[Dict[str, Any]]:
        """Get all detected anomalies."""
        return self.anomalies

    @as_tool
    def update_baselines(self) -> None:
        """Update baseline statistics for all agents."""
        for agent_id in self.detector.agent_interactions:
            self.detector.update_baseline(agent_id)
        logging.info("Updated anomaly detection baselines")

    def _log_anomaly(self, agent_id: str, interaction: Dict[str, Any]) -> None:
        """Log a detected anomaly."""
        anomaly = {"agent_id": agent_id, "interaction": interaction, "timestamp": interaction.get("timestamp", None)}
        self.anomalies.append(anomaly)
        logging.warning(f"ANOMALY DETECTED: Agent {agent_id} - {interaction}")
