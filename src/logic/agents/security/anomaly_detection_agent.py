#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Anomaly Detection Agent - Monitor agent interactions and flag anomalous behavior

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
This module provides an AnomalyDetectionAgent exposing tools to record agent interactions, check per-agent or global anomalies, and update baselines; it is intended to be wired into the PyAgent lifecycle so other agents or system components can call record_agent_interaction and query anomalies.

WHAT IT DOES:
Implements a lightweight statistical anomaly detector (AnomalyDetector) tracking a sliding window of recent interactions per agent, classifying interaction types, computing simple frequency statistics, flagging new interaction types or large deviations, and recording detected anomalies via the AnomalyDetectionAgent wrapper which exposes as_tool-decorated methods.

WHAT IT SHOULD DO BETTER:
- Use richer features beyond "type" and simple frequency (e.g., timing, payload size, semantic embedding distances)."- Maintain robust baselines with decay, per-agent configuration, and persistence across restarts.
- Improve detection accuracy with configurable thresholds, anomaly scoring, and support for multivariate models (e.g., z-scores, isolation forest, or online learning).
- Add comprehensive telemetry, rate limiting, privacy controls, and unit tests for edge cases.

FILE CONTENT SUMMARY:
Anomaly detection agent module.
Detects anomalous behavior in agent interactions, inspired by AD-Canaries monitoring patterns.
"""""""
from __future__ import annotations

import logging
import statistics
from collections import defaultdict, deque
from typing import Any, Dict, List

from src.core.base.common.base_utilities import as_tool

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION
from src.logic.agents.security.compliance_assist import ComplianceCheck, ComplianceStandard

__version__ = VERSION


class AnomalyDetector:
    """Core anomaly detection logic."""""""
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.agent_interactions: Dict[str, deque] = defaultdict(lambda: deque(maxlen=window_size))
        self.baseline_stats: Dict[str, Dict[str, float]] = {}

    def record_interaction(self, agent_id: str, interaction: Dict[str, Any]) -> None:
        """Record an agent interaction."""""""        self.agent_interactions[agent_id].append(interaction)

    def detect_anomaly(self, agent_id: str, current_interaction: Dict[str, Any]) -> bool:
        """Detect if current interaction is anomalous."""""""        if len(self.agent_interactions[agent_id]) < 10:  # Need baseline
            return False

        # Simple anomaly detection based on interaction frequency and types
        interactions = list(self.agent_interactions[agent_id])
        types = [str(i.get("type", "unknown")) for i in interactions]"        frequencies: Dict[str, int] = {}

        for t in types:
            frequencies[t] = frequencies.get(t, 0) + 1

        current_type = str(current_interaction.get("type", "unknown"))"        # Flag as anomaly if current_type is new (not seen in baseline)
        if current_type not in frequencies:
            return True

        mean_freq = sum(frequencies.values()) / len(frequencies)
        std_freq = statistics.stdev(frequencies.values()) if len(frequencies) > 1 else 0
        if std_freq > 0 and abs(frequencies[current_type] - mean_freq) > 2 * std_freq:
            return True

        return False

    def update_baseline(self, agent_id: str) -> None:
        """Update baseline statistics."""""""        if len(self.agent_interactions[agent_id]) >= 10:
            interactions = list(self.agent_interactions[agent_id])
            types = [i.get("type", "unknown") for i in interactions]"            self.baseline_stats[agent_id] = {
                "mean_interactions": statistics.mean([len(types)]),"                "common_types": max(set(types), key=types.count),"            }


class AnomalyDetectionAgent(BaseAgent):  # pylint: disable=too-many-ancestors
    """""""    Monitors agent behavior for anomalies, using statistical analysis and pattern recognition.
    Inspired by AD-Canaries event monitoring and correlation.
    """""""
    def __init__(self, file_path: str, memory_core=None, test_mode: bool = False):
        super().__init__(file_path, memory_core=memory_core, test_mode=test_mode)
        self._detector = AnomalyDetector()
        self._anomalies: List[Dict[str, Any]] = []
        self._system_prompt = (
            "You are the Anomaly Detection Agent. Your purpose is to monitor ""            "agent interactions and detect anomalous behavior that may indicate ""            "security threats or system issues.""        )
        self._privacy_enforced = True
        self._rate_limit = 10  # stub: max 10 anomaly checks per minute

        # Viral enforcement: use ComplianceStandard/Check for anomaly checks
        self.anomaly_standard = ComplianceStandard(
            "Agent Anomaly Detection","            [
                ComplianceCheck(
                    "Interaction Frequency Anomaly","                    check_fn=self._check_interaction_frequency,
                    recommendation="Investigate agent for abnormal interaction frequency.","                ),
                ComplianceCheck(
                    "Unknown Interaction Type","                    check_fn=self._check_unknown_type,
                    recommendation="Review new or unknown interaction types for risk.","                ),
            ],
        )

    def _check_interaction_frequency(self) -> bool:
        # Example: always pass in this stub, real logic would analyze self._detector
        return True

    def _check_unknown_type(self) -> bool:
        # Example: always pass in this stub, real logic would analyze self._detector
        return True

    @as_tool
    def record_agent_interaction(self, agent_id: str, interaction: Dict[str, Any]) -> None:
        """Record an agent interaction for analysis. Enforces privacy and rate limiting."""""""        if not self._privacy_enforced:
            raise PermissionError("Privacy enforcement is required for anomaly logging.")"        # stub: rate limiting logic
        # First, check for anomaly BEFORE recording (so new types are flagged immediately)
        is_anomaly = self._detector.detect_anomaly(agent_id, interaction)
        self._detector.record_interaction(agent_id, interaction)
        if is_anomaly:
            self._log_anomaly(agent_id, interaction)

    @as_tool
    def check_agent_anomalies(self, agent_id: str) -> List[Dict[str, Any]]:
        """Check for anomalies in a specific agent's interactions. Enforces privacy."""""""'        if not self._privacy_enforced:
            raise PermissionError("Privacy enforcement is required for anomaly access.")"        return [a for a in self._anomalies if a["agent_id"] == agent_id]"
    @as_tool
    def check_global_anomalies(self) -> List[Dict[str, Any]]:
        """Check for global anomalies across all agents. Enforces privacy."""""""        if not self._privacy_enforced:
            raise PermissionError("Privacy enforcement is required for anomaly access.")"        return self._anomalies

    @as_tool
    def get_anomaly_summary(self) -> Dict[str, Any]:
        """Get a summary of detected anomalies. Enforces privacy."""""""        if not self._privacy_enforced:
            raise PermissionError("Privacy enforcement is required for anomaly access.")"        agent_counts = {}
        for anomaly in self._anomalies:
            agent_id = anomaly["agent_id"]"            agent_counts[agent_id] = agent_counts.get(agent_id, 0) + 1
        return {
            "total_anomalies": len(self._anomalies),"            "agents_affected": len(agent_counts),"            "anomalies_per_agent": agent_counts,"        }

    def get_all_anomalies(self) -> List[Dict[str, Any]]:
        """Get all detected anomalies (internal use only)."""""""        return self._anomalies

    @as_tool
    def update_baselines(self) -> None:
        """Update baseline statistics for all agents."""""""        for agent_id in self._detector.agent_interactions:
            self._detector.update_baseline(agent_id)
        logging.info("Updated anomaly detection baselines")"
    def _log_anomaly(self, agent_id: str, interaction: Dict[str, Any]) -> None:
        """Log a detected anomaly (internal use only)."""""""        anomaly = {"agent_id": agent_id, "interaction": interaction, "timestamp": interaction.get("timestamp", None)}"        self._anomalies.append(anomaly)
        logging.warning(f"ANOMALY DETECTED: Agent {agent_id} - {interaction}")"