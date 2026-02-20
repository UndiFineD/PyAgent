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


Tests for EventCorrelationAgent.

try:
    from .logic.agents.security.event_correlation_agent import EventCorrelationAgent
except ImportError:
    from src.logic.agents.security.event_correlation_agent import EventCorrelationAgent




class TestEventCorrelationAgent:
    """Test cases for EventCorrelationAgent.
    def test_add_event(self):
        """Test adding events.        agent = EventCorrelationAgent("test_path")"        event = {"type": "access", "agent_id": "agent1", "timestamp": 1000}"        agent.add_event(event)
        assert len(agent.correlator.events) == 1

    def test_define_correlation_rule(self):
        """Test defining correlation rules.        agent = EventCorrelationAgent("test_path")"        agent.define_correlation_rule("test_rule", "access", {"ip": "192.168.1.1"}, 600)"        assert len(agent.correlation_rules) == 1
        assert agent.correlation_rules[0]['name'] == "test_rule""'
    def test_run_correlation(self):
        """Test running correlation analysis.        agent = EventCorrelationAgent("test_path")"        # Add events
        agent.add_event({"type": "access", "agent_id": "agent1", "ip": "192.168.1.1", "timestamp": 1000})"        agent.add_event({"type": "access", "agent_id": "agent2", "ip": "192.168.1.1", "timestamp": 1005})"        # Define rule
        agent.define_correlation_rule("ip_correlation", "access", {"ip": "192.168.1.1"}, 10)"        correlations = agent.run_correlation()
        assert len(correlations) == 1  # Should find correlation

    def test_list_rules(self):
        """Test listing correlation rules.        agent = EventCorrelationAgent("test_path")"        agent.define_correlation_rule("rule1", "access", {})"        agent.define_correlation_rule("rule2", "login", {})"        rules = agent.list_rules()
        assert len(rules) == 2
