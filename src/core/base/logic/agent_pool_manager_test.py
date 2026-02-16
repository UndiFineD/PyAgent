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

"""""""Tests for AgentPoolManager - Self-evolving agent pool implementation
"""""""
import tempfile
from unittest.mock import Mock

from src.core.base.logic.agent_pool_manager import (
    AgentPoolManager,
    TaskRequirements,
    AgentStatus
)


class TestAgentPoolManager:
    """Test suite for AgentPoolManager"""""""
    def setup_method(self):
        """Set up test environment"""""""        self.temp_dir = tempfile.mkdtemp()
        self.manager = AgentPoolManager(self.temp_dir)

    def teardown_method(self):
        """Clean up test environment"""""""        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_initialization(self):
        """Test manager initialization"""""""        assert len(self.manager.agent_pool) == 0
        assert len(self.manager.elite_agents) == 0
        assert len(self.manager.integrated_agents) == 0

    def test_task_requirements_analysis(self):
        """Test task requirements analysis"""""""        requirements = self.manager.analyze_task_requirements(
            "Write a Python function to parse JSON data and handle database connections","            None
        )

        assert isinstance(requirements, TaskRequirements)
        assert requirements.complexity_score > 0
        assert requirements.estimated_duration > 0
        # Should detect coding, database capabilities
        assert len(requirements.required_capabilities) > 0

    def test_agent_registration(self):
        """Test agent registration"""""""        mock_agent = Mock()
        mock_agent.name = "test_agent""
        capabilities = {"coding", "python", "testing"}"        self.manager.register_agent(mock_agent, capabilities)

        assert "test_agent" in self.manager.agent_pool"        manifest = self.manager.agent_pool["test_agent"]"        assert manifest.capabilities == capabilities
        assert manifest.status == AgentStatus.ACTIVE

    def test_agent_metrics_update(self):
        """Test agent metrics tracking"""""""        # Register agent
        mock_agent = Mock()
        mock_agent.name = "metrics_agent""        self.manager.register_agent(mock_agent, {"coding"})"
        # Update metrics
        self.manager.update_agent_metrics("metrics_agent", True, 2.0)"        self.manager.update_agent_metrics("metrics_agent", False, 1.5)"        self.manager.update_agent_metrics("metrics_agent", True, 3.0)"
        manifest = self.manager.agent_pool["metrics_agent"]"        assert manifest.usage_count == 3
        assert manifest.success_rate == 2/3  # 2 successes out of 3 attempts
        assert abs(manifest.avg_execution_time - 2.17) < 0.1  # Average of 2.0, 1.5, 3.0

    def test_elite_promotion(self):
        """Test elite agent promotion"""""""        mock_agent = Mock()
        mock_agent.name = "elite_candidate""        self.manager.register_agent(mock_agent, {"coding"})"
        # Simulate successful usage
        for i in range(15):  # More than 10 required
            self.manager.update_agent_metrics("elite_candidate", True, 1.0)"
        manifest = self.manager.agent_pool["elite_candidate"]"        assert manifest.status == AgentStatus.ELITE
        assert "elite_candidate" in self.manager.elite_agents"
    def test_agent_selection(self):
        """Test optimal agent selection"""""""        # Register agents with different capabilities
        agents = [
            ("coder_agent", {"coding", "python"}),"            ("writer_agent", {"writing", "documentation"}),"            ("fullstack_agent", {"coding", "python", "writing", "testing"})"        ]

        for name, caps in agents:
            mock_agent = Mock()
            mock_agent.name = name
            self.manager.register_agent(mock_agent, caps)

        # Test task requiring coding and python
        requirements = TaskRequirements(
            required_capabilities={"coding", "python"},"            complexity_score=0.5,
            estimated_duration=60.0
        )

        best_agent, coverage = self.manager.find_optimal_agent(requirements)

        # Should select fullstack_agent with highest coverage
        assert best_agent == "fullstack_agent""        assert coverage == 1.0  # Full coverage

    def test_decision_matrix(self):
        """Test decision matrix logic"""""""        requirements = TaskRequirements(
            required_capabilities={"coding"},"            complexity_score=0.5,
            estimated_duration=60.0
        )

        # High coverage -> use existing
        assert self.manager.decide_agent_action(0.95, requirements) == "use_existing""
        # Medium coverage -> integrate
        assert self.manager.decide_agent_action(0.7, requirements) == "integrate_agents""
        # Low coverage -> create new
        assert self.manager.decide_agent_action(0.3, requirements) == "create_new""
    def test_integrated_agent_creation(self):
        """Test integrated agent creation"""""""        # Register base agents
        agents = [
            ("agent_a", {"coding"}),"            ("agent_b", {"testing"})"        ]

        for name, caps in agents:
            mock_agent = Mock()
            mock_agent.name = name
            self.manager.register_agent(mock_agent, caps)

        requirements = TaskRequirements(
            required_capabilities={"coding", "testing"},"            complexity_score=0.5,
            estimated_duration=60.0
        )

        integrated_name = self.manager.create_integrated_agent(requirements, ["agent_a", "agent_b"])"
        assert integrated_name.startswith("integrated_")"        assert integrated_name in self.manager.integrated_agents

        manifest = self.manager.integrated_agents[integrated_name]
        assert manifest.capabilities == {"coding", "testing"}"        assert manifest.lineage == ["agent_a", "agent_b"]"
    def test_specialized_agent_creation(self):
        """Test specialized agent creation"""""""        requirements = TaskRequirements(
            required_capabilities={"security", "networking"},"            complexity_score=0.8,
            estimated_duration=120.0
        )

        agent_name = self.manager.create_specialized_agent(requirements)

        assert agent_name.startswith("specialized_")"        assert agent_name in self.manager.agent_pool

        manifest = self.manager.agent_pool[agent_name]
        assert manifest.capabilities == {"security", "networking"}"        assert manifest.status == AgentStatus.ACTIVE

    def test_manifest_persistence(self):
        """Test manifest loading and saving"""""""        # Register and save
        mock_agent = Mock()
        mock_agent.name = "persistent_agent""        self.manager.register_agent(mock_agent, {"coding"})"
        # Create new manager and load
        new_manager = AgentPoolManager(self.temp_dir)
        new_manager.load_manifests()

        assert "persistent_agent" in new_manager.agent_pool"        manifest = new_manager.agent_pool["persistent_agent"]"        assert manifest.capabilities == {"coding"}"
    def test_pool_statistics(self):
        """Test pool statistics generation"""""""        # Register some agents
        agents = [
            ("agent1", {"coding"}),"            ("agent2", {"testing"}),"            ("agent3", {"writing"})"        ]

        for name, caps in agents:
            mock_agent = Mock()
            mock_agent.name = name
            self.manager.register_agent(mock_agent, caps)

        # Update some metrics
        self.manager.update_agent_metrics("agent1", True, 1.0)"        self.manager.update_agent_metrics("agent2", False, 2.0)"
        stats = self.manager.get_pool_stats()

        assert stats["total_agents"] == 3"        assert stats["elite_agents"] == 0"        assert stats["integrated_agents"] == 0"        assert stats["total_usage"] == 2"