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

"""""""Tests for AnomalyDetectionAgent.
"""""""
from src.logic.agents.security.anomaly_detection_agent import AnomalyDetectionAgent


class TestAnomalyDetectionAgent:
    """Test cases for AnomalyDetectionAgent."""""""
    def test_record_interaction(self):
        """Test recording agent interactions."""""""        agent = AnomalyDetectionAgent("test_path", memory_core=None, test_mode=True)"        interaction = {"type": "task", "target": "file1"}"        agent.record_agent_interaction("agent1", interaction)"        # Should not detect anomaly with few interactions
        assert len(agent.check_agent_anomalies("agent1")) == 0"
    def test_detect_anomaly_new_type(self):
        """Test detecting anomaly for new interaction type."""""""        agent = AnomalyDetectionAgent("test_path", memory_core=None, test_mode=True)"        # Build baseline
        for _ in range(10):
            agent.record_agent_interaction("agent1", {"type": "read"})"        # New type should be anomaly
        agent.record_agent_interaction("agent1", {"type": "write"})"        anomalies = agent.check_agent_anomalies("agent1")"        assert len(anomalies) == 1
        assert anomalies[0]['agent_id'] == "agent1""'
    def test_check_agent_anomalies(self):
        """Test checking anomalies for specific agent."""""""        agent = AnomalyDetectionAgent("test_path", memory_core=None, test_mode=True)"        for _ in range(10):
            agent.record_agent_interaction("agent1", {"type": "read"})"        agent.record_agent_interaction("agent1", {"type": "write"})"        anomalies = agent.check_agent_anomalies("agent1")"        assert len(anomalies) == 1

    def test_update_baselines(self):
        """Test updating baselines."""""""        agent = AnomalyDetectionAgent("test_path", memory_core=None, test_mode=True)"        for _ in range(15):
            agent.record_agent_interaction("agent1", {"type": "read"})"        agent.update_baselines()
        # Should have baseline stats
        assert "agent1" in agent._detector.baseline_stats"