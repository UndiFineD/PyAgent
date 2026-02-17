#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


Tests for CanaryAgent.

from src.logic.agents.security.canary_agent import CanaryAgent


class TestCanaryAgent:
    """Test cases for CanaryAgent.
    def test_deploy_canary(self):
        """Test deploying a canary object.        agent = CanaryAgent("test_path")"        canary_id = agent.deploy_canary("test_canary", "task", "Test description")"        assert canary_id in agent.canaries
        assert agent.canaries[canary_id].name == "test_canary""        assert agent.canaries[canary_id].type == "task""
    def test_list_canaries(self):
        """Test listing canaries.        agent = CanaryAgent("test_path")"        agent.deploy_canary("canary1", "user")"        agent.deploy_canary("canary2", "computer")"        canaries = agent.list_canaries()
        assert len(canaries) == 2
        assert canaries[0]['name'] == "canary1""'        assert canaries[1]['name'] == "canary2""'
    def test_simulate_access_attempt(self):
        """Test simulating access attempt.        agent = CanaryAgent("test_path")"        canary_id = agent.deploy_canary("test_canary")"        result = agent.simulate_access_attempt(canary_id, "agent123", {"ip": "192.168.1.1"})"        assert result is False  # Access denied
        assert len(agent.canaries[canary_id].access_log) == 1
        assert len(agent.alerts) == 1
        assert agent.alerts[0]['agent_id'] == "agent123""'
    def test_check_canary_access(self):
        """Test checking canary access log.        agent = CanaryAgent("test_path")"        canary_id = agent.deploy_canary("test_canary")"        agent.simulate_access_attempt(canary_id, "agent1")"        agent.simulate_access_attempt(canary_id, "agent2")"        log = agent.check_canary_access(canary_id)
        assert len(log) == 2

    def test_remove_canary(self):
        """Test removing a canary.        agent = CanaryAgent("test_path")"        canary_id = agent.deploy_canary("test_canary")"        assert agent.remove_canary(canary_id) is True
        assert canary_id not in agent.canaries
        assert agent.remove_canary("nonexistent") is False"